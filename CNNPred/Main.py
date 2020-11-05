import math
import os
import subprocess
import sys
import torch
import numpy as np
from numba import jit
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset

sample_path = 'test_psfmPssILBR'
lib_path_01 = "CNNPred_Prod"

max_epoch = 100
bach_size = 50
LR = 1e-2
height = 17
width = 25

save_model_01 = "model_01"
save_model_02 = "model_02"
save_model_03 = "model_03"
save_model_04 = "model_04"
save_model_05 = "model_05"
save_model_06 = "model_06"
save_model_07 = "model_07"
save_model_08 = "model_08"

def mkdir(path):
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
    return path


class CnnModel(nn.Module):
    def __init__(self):
        super(CnnModel, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=width, out_channels=width * 2, kernel_size=(3, 3), stride=1),
            nn.BatchNorm2d(width * 2),
            nn.ReLU(inplace=True)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=width * 2, out_channels=width * 2, kernel_size=(5, 5), stride=1),
            nn.BatchNorm2d(width * 2),
            nn.ReLU(inplace=True)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=width * 2, out_channels=width * 4, kernel_size=(height - 8, height - 8), stride=1),
            nn.BatchNorm2d(width * 4),
            nn.ReLU(inplace=True)
        )
        #
        self.fc = nn.Sequential(
            nn.Linear(9 * width * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(256, 2),
        )
        self.sm = nn.Sigmoid()

    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        out = self.sm(out)
        return out


def Ensemble_model(CNNPred_result, test_loader, model_01, model_02, model_03, model_04, model_05, model_06, model_07, model_08):
    f1 = open(CNNPred_result + "/" + lib_path_01, 'w')

    model_01.eval()
    model_02.eval()
    model_03.eval()
    model_04.eval()
    model_05.eval()
    model_06.eval()
    model_07.eval()
    model_08.eval()

    for i, data in enumerate(test_loader):
        features = data

        features = Variable(features, requires_grad=False)

        output_01 = model_01(features)
        output_02 = model_02(features)
        output_03 = model_03(features)
        output_04 = model_04(features)
        output_05 = model_05(features)
        output_06 = model_06(features)
        output_07 = model_07(features)
        output_08 = model_08(features)

        # 输出模型预测样本类别的索引值
        _, pre1 = torch.max(output_01.data, 1)
        _, pre2 = torch.max(output_02.data, 1)
        _, pre3 = torch.max(output_03.data, 1)
        _, pre4 = torch.max(output_04.data, 1)
        _, pre5 = torch.max(output_05.data, 1)
        _, pre6 = torch.max(output_06.data, 1)
        _, pre7 = torch.max(output_07.data, 1)
        _, pre8 = torch.max(output_08.data, 1)

        pre_pos = (output_01[0][1] + output_02[0][1] + output_03[0][1] + output_04[0][1] + output_05[0][1] + output_06[0][1] + output_07[0][1] + output_08[0][1]) / 8
        pre_neg = (output_01[0][0] + output_02[0][0] + output_03[0][0] + output_04[0][0] + output_05[0][0] + output_06[0][0] + output_07[0][0] + output_08[0][0]) / 8

        if (pre1.item() + pre2.item() + pre3.item() + pre4.item() + pre5.item() +pre6.item() + pre7.item() + pre8.item()) >= 4:
            pre = 1
        else:
            pre = 0

        f1.write(format(pre, '.6f') + '  ')
        f1.write(format(pre_pos, '.6f') + '  ')
        f1.write(format(pre_neg, '.6f') + '\n')

    f1.close()


class DataPreparation(Dataset):
    def __init__(self, path, transform=None):
        super(DataPreparation, self).__init__()
        self.data_info = self.get_protein_info(path)  # data_info is a list, storage feature and/or label

    def __getitem__(self, index):
        feature = self.data_info[index]
        return feature

    def __len__(self):
        return len(self.data_info)

    @staticmethod
    def get_protein_info(path):
        data_info = []
        file = open(path, "r+")
        for each_line in file:
            each_line = each_line.split(',')
            xy = np.loadtxt(each_line)
            # A row represents a sample, convert feature into a height*width matrix
            fea_line = torch.from_numpy(xy[:]).view(height, width)
            Matrix_con3d = get_data_info(fea_line)
            # feature tensor
            Matrix_con3d = torch.tensor(Matrix_con3d).view(width, height, height).float()
            data_info.append(Matrix_con3d)
        return data_info


@jit
def get_data_info(fea_line):
    Matrix_con2d = np.zeros((height, height))
    Matrix_con3d = []
    # Matrix transpose height*width ------> width *height
    fea_line = torch.transpose(fea_line, 1, 0)
    # width *height-----> width * height *height
    for i in range(len(fea_line)):
        line = fea_line[i]
        for j in range(len(line)):
            Matrix_con2d[j][j] = line[j]
            for k in range(j + 1, len(line)):
                #  dimension change 1*height -----> height*height
                if i < 20:
                    Matrix_con2d[j][k] = math.sqrt(line[j].item() * line[k].item())
                else:
                    Matrix_con2d[j][k] = (line[j].item() + line[k].item()) / 2.0
                Matrix_con2d[k][j] = Matrix_con2d[j][k]
        Matrix_con3d.append(Matrix_con2d)
        
        # set  empty
        Matrix_con2d = np.zeros((height, height))
    return Matrix_con3d


if __name__ == '__main__':

    result_path = sys.argv[1]
    model_train_by = sys.argv[2]
    
    System_path = os.path.dirname(os.path.abspath(__file__))
    fixed_model_path=System_path+"/" + model_train_by + "/" 
    
    """ =================   the construction of test set    =================== """
    valid_dataset = DataPreparation(result_path + "/" + sample_path)
    valid_loader = DataLoader(dataset=valid_dataset, batch_size=1, shuffle=False, drop_last=False)

    """ =================   load model  =================== """
    model_load_01 = CnnModel()
    model_load_01.load_state_dict(torch.load(fixed_model_path + save_model_01, map_location=lambda storage, loc: storage))

    model_load_02 = CnnModel()
    model_load_02.load_state_dict(torch.load(fixed_model_path + save_model_02, map_location=lambda storage, loc: storage))

    model_load_03 = CnnModel()
    model_load_03.load_state_dict(torch.load(fixed_model_path + save_model_03, map_location=lambda storage, loc: storage))

    model_load_04 = CnnModel()
    model_load_04.load_state_dict(torch.load(fixed_model_path + save_model_04, map_location=lambda storage, loc: storage))

    model_load_05 = CnnModel()
    model_load_05.load_state_dict(torch.load(fixed_model_path + save_model_05, map_location=lambda storage, loc: storage))

    model_load_06 = CnnModel()
    model_load_06.load_state_dict(torch.load(fixed_model_path + save_model_06, map_location=lambda storage, loc: storage))

    model_load_07 = CnnModel()
    model_load_07.load_state_dict(torch.load(fixed_model_path + save_model_07, map_location=lambda storage, loc: storage))

    model_load_08 = CnnModel()
    model_load_08.load_state_dict(torch.load(fixed_model_path + save_model_08, map_location=lambda storage, loc: storage))
    print("prediction  phase... ")
    """ =================   prediction  phase  =================== """
    Ensemble_model(result_path, valid_loader, model_load_01, model_load_02, model_load_03, model_load_04, model_load_05, model_load_06, model_load_07, model_load_08)
    print("finish prediction...")