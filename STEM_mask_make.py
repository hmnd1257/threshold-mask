import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import os

def fill_color(img, canvas):
    a = np.arange(0, img.shape[0])
    b = np.arange(0, img.shape[1])
    filter_idx=[]
    filter_col=[]

    for i in a:
        for j in b:
            filter = canvas[i:i+5, j:j+5]
            filter_mean = filter.mean()

            if filter_mean > 30:
                # print(filter_mean)
                filter_idx.append(i)
                filter_col.append(j)
    for i in range(len(filter_idx)):
        canvas[filter_idx[i]:filter_idx[i]+6, filter_col[i]:filter_col[i]+6] = 255
    return canvas

def img_segmentation(img):
    mask = np.zeros(shape=img.shape, dtype=np.uint8)

    img1 = img[:51, :51]  # 왼쪽 위
    img2 = img[236 - 34:, :41 + 35]  # 왼쪽 아래
    img3 = img[:28 + 27, 225 - 25:]  # 오른쪽 위
    img4 = img[215 - 25:, 200 - 25:]  # 오른쪽 아래

    mask[:51, :51] = img1.astype(np.float32)
    mask[236 - 34:, :41 + 35] = img2.astype(np.float32)
    mask[:28 + 27, 225 - 25:] = img3.astype(np.float32)
    mask[215 - 25:, 200 - 25:] = img4.astype(np.float32)

    return mask

def fig_show(img, mask, thresh, fill_mask, masked):
    fig = plt.figure(figsize=(15, 15))
    plt.subplot(1, 5, 1)
    plt.imshow(img)  # BGR -> RGB
    plt.title('original img')
    # plt.title(i)
    plt.xticks([])
    plt.yticks([])
    #
    plt.subplot(1, 5, 2)
    plt.imshow(mask)  # BGR -> RGB
    plt.title('mask')
    plt.xticks([])
    plt.yticks([])
    #
    plt.subplot(1, 5, 3)
    plt.imshow(thresh)  # BGR -> RGB
    plt.title('thresh 200')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 5, 4)
    plt.imshow(fill_mask)  # BGR -> RGB
    plt.title('fill_mask')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 5, 5)
    plt.imshow(masked)  # BGR -> RGB
    plt.title('masked')
    plt.xticks([])
    plt.yticks([])

    plt.show()

# 영역마다 객체가 없다면 mask에 추가하지 않고.. 있다면 추가하고.. 이런식으로 가능한지 생각해보기..
def main(img_path, save_path, segmentation=True, img_show=True, img_fill=True, save_fig=True):
    for i in os.listdir(img_path):
        print(i)
        img = cv2.imread(img_path + '{}'.format(i))
        img = cv2.resize(img, (256,256))
        # img = cv2.imread(img_path + '100056.png')
        h, w, _ = img.shape

        # print(i)
        img = np.array(img)
        print('img.shape :', img.shape)

        if segmentation:
            img_seg = img_segmentation(img)
        else:
            img_seg = img

        mask = np.zeros(shape=img.shape, dtype=np.uint8)

        mask[np.where((img_seg > [200, 200, 200]).all(axis=2))] = [255, 255, 255]
        thresh = mask.copy()

        if img_fill:
            fill_mask = fill_color(img, mask)
        else:
            fill_mask = mask

        masked = img.copy()

        masked[np.where((fill_mask > [230, 230, 230]).all(axis=2))] = [255, 255, 255]

        if img_show:
            fig_show(img, img_seg, thresh, fill_mask, masked)

        if save_fig:
            if os.path.exists(save_path) is False:
                os.makedirs(save_path)
            cv2.imwrite(save_path + '{}'.format(i), thresh)

if __name__ == "__main__":
    img_path = './STEMimg/'
    save_path = './STEMimg_results/'

    segmentation = False # False
    img_show = True
    img_fill = True
    save_fig = False

    main(img_path, save_path, segmentation=segmentation, img_show=img_show, img_fill=img_fill, save_fig=save_fig)