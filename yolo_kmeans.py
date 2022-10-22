import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

def iou(box, clusters):
    """
    Calculates the Intersection over Union (IoU) between a box and k clusters.
    :param box: tuple or array, shifted to the origin (i. e. width and height)
    :param clusters: numpy array of shape (k, 2) where k is the number of clusters
    :return: numpy array of shape (k, 0) where k is the number of clusters
    """
    x = np.minimum(clusters[:, 0], box[0])
    y = np.minimum(clusters[:, 1], box[1])
    if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
        raise ValueError("Box has no area")

    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[:, 0] * clusters[:, 1]

    iou_ = intersection / (box_area + cluster_area - intersection)

    return iou_


def avg_iou(boxes, clusters):
    """
    Calculates the average Intersection over Union (IoU) between a numpy array of boxes and k clusters.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param clusters: numpy array of shape (k, 2) where k is the number of clusters
    :return: average IoU as a single float
    """
    return np.mean([np.max(iou(boxes[i], clusters)) for i in range(boxes.shape[0])])


def kmeans(boxes, k, dist=np.median):
    """
    Calculates k-means clustering with the Intersection over Union (IoU) metric.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param k: number of clusters
    :param dist: distance function
    :return: numpy array of shape (k, 2)
    """
    rows = boxes.shape[0]
    row = int(rows/(k+1))
    indexes = np.empty(k)
    for i in range (1,k+1):
        indexes[i-1] = int(rows-i)#int(row*i)


    distances = np.empty((rows, k))
    last_clusters = np.zeros((rows,))
    indexes = indexes.astype(int)
    np.random.seed()
    # the Forgy method will fail if the whole array contains the same rows
    clusters = boxes[indexes]

    #clusters = boxes[indexes]

    while True:
        for row in range(rows):
            distances[row] = 1 - iou(boxes[row], clusters)

        nearest_clusters = np.argmin(distances, axis=1)

        if (last_clusters == nearest_clusters).all():
            break

        for cluster in range(k):
            clusters[cluster] = dist(boxes[nearest_clusters == cluster], axis=0)

        last_clusters = nearest_clusters

    return clusters

txt_path = 'train'
xml_path = ''
jpg_path = ''
dataset = []

xml = True
txt = not xml

if xml:
    for i in os.listdir(xml_path):
        tree = ET.parse(os.path.join(xml_path,i))
        for elem in tree.iter():
            if 'object' in elem.tag or 'part' in elem.tag:
                # initalize obj dict            
                for attr in list(elem):       
                    if 'bndbox' in attr.tag:
                        for dim in list(attr):
                            if 'xmin' in dim.tag:
                                xmin = int(round(float(dim.text)))
                            if 'ymin' in dim.tag:
                                ymin = int(round(float(dim.text)))
                            if 'xmax' in dim.tag:
                                xmax = int(round(float(dim.text)))
                            if 'ymax' in dim.tag:
                                ymax = int(round(float(dim.text)))
                        dataset.append([xmax-xmin,ymax-ymin])

'''
for i,j in zip(os.listdir(txt_path),os.listdir(jpg_path)):
    txt_file = os.path.join(txt_path,i)
    jpg_file = os.path.join(jpg_path,j)
    img = cv2.imread(jpg_file)
    height, width,_ = img.shape
    with open(txt_file,'r') as f:
        objects = f.readlines()
        for o in objects:
            o = o.strip().split(' ')
            w = int(width * float(o[3]))
            h = int(height * float(o[4]))
            dataset.append([w,h])
'''
if txt:
    for i in os.listdir(txt_path):
        txt_file = os.path.join(txt_path,i)
        width = 540
        height = 360
        with open(txt_file,'r') as f:
            objects = f.readlines()
            for o in objects:
                o = o.strip().split(' ')
                w = int(width * float(o[3]))
                h = int(height * float(o[4]))
                dataset.append([w,h])
dataset = np.array(dataset)
dataset = dataset[np.argsort(dataset.sum(axis=1))[:]]


out = kmeans(dataset, k=9)
print("Accuracy: {:.2f}%".format(avg_iou(dataset, out) * 100))
print("Boxes:\n {}".format(out))

ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
print("Ratios:\n {}".format(sorted(ratios)))
