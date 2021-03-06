import numpy as np
import cv2
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from os import listdir
import time


def loadImages():
    imgs = []
    labels = np.repeat([i for i in range(0, 5)], 20)
    
    # Percorre todos os diretorios de data e carrega as imagens
    for folder in listdir("../dataset_num_camera"):
        for img in listdir("../dataset_num_camera/" + folder):
            imgs.append(cv2.imread("../dataset_num_camera/" + folder + "/" + img))

    return np.asarray(imgs).reshape(len(imgs), -1), labels
        
def sklearnSVM(train_data, test_data, train_labels, test_labels):
    print("########### Sklearn ###########\n")

    svm = SVC(kernel="poly", C = 1.0, degree = 3, random_state = None)

    start = time.clock()
    svm.fit(train_data, train_labels)
    end = time.clock()
    print("Traning took {:.3f}s\n".format(end-start))

    pred = svm.predict(test_data)
    
    print("Report: \n{}".format(classification_report(test_labels, pred)))
    
    print("Confusion Matrix: \n{}\n".format(confusion_matrix(test_labels, pred)))

def SVMParams(svm):
    print("SVM parameters:")
    print("Kernel type: %s" % svm.getKernelType())
    print("Type       : %s" % svm.getType())
    print("C          : %s" % svm.getC())
    print("Degree     : %s" % svm.getDegree())
    print("Nu         : %s" % svm.getNu())
    print("Gamma      : %s\n" % svm.getGamma())

def opencvSVM(train_data, test_data, train_labels, test_labels, trainAuto=False):
    print("########### OpenCV ###########\n")

    svm = cv2.ml.SVM_create()

    # Set SVM type
    svm.setType(cv2.ml.SVM_C_SVC)
    # Set SVM Kernel to Polynomial
    svm.setKernel(cv2.ml.SVM_POLY)
    # Set parameter C
    svm.setC(1)
    # Set parameter Degree
    svm.setDegree(0.6)
    # Set parameter Gamma
    svm.setGamma(0.50625)

    print("Traning...")
    start = time.clock()
    if(trainAuto):
        svm.trainAuto(np.float32(train_data), cv2.ml.ROW_SAMPLE, train_labels)
    else:
        svm.train(np.float32(train_data), cv2.ml.ROW_SAMPLE, train_labels)
    end = time.clock()
    print("Traning took {:.3f}s\n".format(end-start))

    svm.save("weights/opencv_svm.yml")
    
    pred = svm.predict(np.float32(test_data))[1]

    SVMParams(svm)

    print("Report: \n{}".format(classification_report(test_labels, pred)))
    
    print("Confusion Matrix: \n{}\n".format(confusion_matrix(test_labels, pred)))   

def loadSVM():
    svm = cv2.ml.SVM_load("weights/opencv_svm.yml")

    img = cv2.imread("./saida.jpg")

    img = np.array([np.reshape(img, (2352,))])

    #cv2.imshow("saida", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
   
    pred = svm.predict( np.float32(img) )[1]

    print(pred)

if __name__ == "__main__":
    imgs, labels = loadImages()
    
    train_data, test_data, train_labels, test_labels = train_test_split(imgs, labels, test_size = 0.2, random_state = None)

    sklearnSVM(train_data, test_data, train_labels, test_labels)

    opencvSVM(train_data, test_data, train_labels, test_labels, trainAuto=True)

    loadSVM()