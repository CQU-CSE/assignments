#coding:utf8

import sys
import numpy as np
from math import *
from numpy import *
import re

dimension=3

def predict(parameterALLnew, xset):#将参数向量代入模型，得出预测值
    predictvalue=parameterALLnew[0]
    for i in range(1,dimension+1):
        parameter=parameterALLnew[i]
        xsetnow=xset**i
        predictvalue=predictvalue+np.dot(parameter,xsetnow)
    return predictvalue

def scaling1(trainingSet_ndarray):#通过特征缩放使特征的范围缩放到接近的范围（min-max标准化）
    return (trainingSet_ndarray - trainingSet_ndarray.min())/(trainingSet_ndarray.max() - trainingSet_ndarray.min())

def scaling2(trainingSet_ndarray,testSet_ndarray):#通过特征缩放使特征的范围缩放到接近的范围（min-max标准化）
    return (testSet_ndarray - trainingSet_ndarray.min())/(trainingSet_ndarray.max() - trainingSet_ndarray.min())

def gradientDescent(xtrain, ytrain, eta, degree, xtest, testLabel,regularizationTerm):#使用梯度下降法求解最优参数向量，并求解损失函数的值
    loss = []#损失函数值组成的列表
    theta0 = zeros(1)#初始化第一维的参数为0，第一维的参数为一个常数
    parameterAll =[]#整个参数向量的列表
    parameterAll.append(theta0)#首先将第一维的参数添加进列表
    for i in range(1,dimension+1):#对于n（n>1）维的参数，是一个五维向量，分别对应于x**n特征矩阵
        parameter=zeros(5)#初始化该维度的参数向量，都赋初值为0
        parameterAll.append(parameter)#有多少维，就有多少个五维的参数向量
    parameterAllnew = np.array(parameterAll)#将整个参数向量的列表转换为数组，便于计算

    length = len(ytrain)
    iter_num = 0
    while iter_num <= degree:#在迭代次数内更新参数向量
        lossDerivative = [0]*(dimension+1)#梯度，赋初值为0，有多少维，就有多少维加1个参数需要在负梯度方向上更新
        for i in range(1,dimension+1):#在每一维上计算该维度的参数向量需要更新的负梯度
            predictChazhi = 0#模型预测值减去真实值
            for row in range(length):
                predictvalue = predict(parameterAllnew,xtrain[row])
                predictChazhi += predictvalue - ytrain[row]
                lossDerivative[i] +=(predictvalue - ytrain[row])*(xtrain[row]**i)
            parameterAllnew[i] = parameterAllnew[i] - (eta/length) * lossDerivative[i] - (regularizationTerm/length)*parameterAllnew[i]
            #参数向量中的第i列的梯度更新（i>1）
        parameterAllnew[0]= parameterAllnew[0] - (eta/length) * predictChazhi - (regularizationTerm/length)*parameterAllnew[0]
        #参数向量的第一列的梯度更新
        iter_num += 1

        zhengzehua = 0#参数向量二范数的平方
        for j in range(len(parameterAllnew)):  # 计算各个参数之和
            parametersingle = parameterAllnew[j]  # 将参数向量依次取出
            zhengzehua = zhengzehua + np.dot(parametersingle,parametersingle)  # 将参数向量的平方θ^2累加

        a = 0
        length1 = len(testLabel)
        for row in range(length1):#计算测试集上的测试误差
            b = predict(parameterAllnew,xtest[row])
            a = a + (predict(parameterAllnew,xtest[row])-testLabel[row])**2
        print a/(2*length1)
        A=a/(2*length1)+regularizationTerm/(2*length1)*zhengzehua
        print iter_num
        loss.append(A)
    return loss

def arrayXtrain(dataSet):#特征缩放处理训练集的X特征向量矩阵
    for x in range(len(dataSet)):
        x1 = scaling1(dataSet[:,0])#处理数据集第一列
        # x0 = ones(x1.shape)#根据x1的shape（行数和列数）生成元素全为1的数组
        x2 = scaling1(dataSet[:, 1])
        x3 = scaling1(dataSet[:, 2])
        x4 = scaling1(dataSet[:, 3])
        x5 = scaling1(dataSet[:, 4])
        Xm = column_stack((x1, x2, x3, x4, x5))#沿着列将数组堆叠
        return Xm

def arrayXtest(trainSet,testSet):#特征缩放处理测试集的X特征向量矩阵
    for x in range(len(testSet)):
        x1 = scaling2(trainSet[:,0],testSet[:,0])#处理数据集第一列
        x2 = scaling2(trainSet[:,1],testSet[:,1])
        x3 = scaling2(trainSet[:,2],testSet[:,2])
        x4 = scaling2(trainSet[:,3],testSet[:,3])
        x5 = scaling2(trainSet[:,4],testSet[:,4])
        Xm = column_stack((x1, x2, x3, x4, x5))#沿着列将数组堆叠
        return Xm

def arrayY(dataset):#Y值不特征缩放
    Ym = dataset[:, 5]
    return Ym

def classify():
    trainingSet = []
    with open('./noise_train.txt') as f:
        for line in f:
            trainingSet.append(line.split(','))
    for x in range(len(trainingSet)):
        for y in range(6):
            trainingSet[x][y] = float(trainingSet[x][y])
    mtrainingSet = np.array(trainingSet)#将数据集的从列表形式转换为数组形式

    testSet = []
    with open('./noise_test.txt') as f:
        for line in f:
            testSet.append(line.split(','))
    for x in range(len(testSet)):
        for y in range(5):
            testSet[x][y] = float(testSet[x][y])
    mtestSet = np.array(testSet)

    with open('./testLabel.txt') as f:
        Label=f.read()
        testLabel=map(float,Label.split(','))

    Xmtrain = arrayXtrain(mtrainingSet)
    Ymtrain = arrayY(mtrainingSet)
    Xmtest = arrayXtest(mtrainingSet,mtestSet)

    gradientDescent(Xmtrain, Ymtrain, 0.5, 10000, Xmtest, testLabel, 0.1)

if __name__ == '__main__':
    classify()
