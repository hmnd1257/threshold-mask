import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

def createFolder(args):
    if os.path.exists(args) is False:
        os.makedirs(args)

def fill_color(img, canvas):
    idx_range = np.arange(0, img.shape[0])
    col_range = np.arange(0, img.shape[1])
    filter_idx=[]
    filter_col=[]

    for idx in idx_range:
        for col in col_range:
            filter = canvas[idx:idx+5, col:col+5]
            filter_mean = filter.mean()

            if filter_mean > 30:
                # print(filter_mean)
                filter_idx.append(idx)
                filter_col.append(col)

    for i in range(len(filter_idx)):
        canvas[filter_idx[i]:filter_idx[i]+6, filter_col[i]:filter_col[i]+6] = 255

    return canvas

def img_segmentation(img):
    mask = np.zeros(shape=img.shape, dtype=np.uint8)

    img1 = img[:51, :51]  # top-left
    img2 = img[236 - 34:, :41 + 35]  # bottom-left
    img3 = img[:28 + 27, 225 - 25:]  # top-right
    img4 = img[215 - 25:, 200 - 25:]  # bottom-right

    mask[:51, :51] = img1.astype(np.float32)
    mask[236 - 34:, :41 + 35] = img2.astype(np.float32)
    mask[:28 + 27, 225 - 25:] = img3.astype(np.float32)
    mask[215 - 25:, 200 - 25:] = img4.astype(np.float32)

    return mask

def fig_show(img, segmented_img, thresh, filled_mask, masked_img):
    fig = plt.figure(figsize=(8, 8))

    plt.subplot(1, 5, 1)
    plt.imshow(img)
    plt.title('original img')
    plt.xticks([])
    plt.yticks([])
    #
    plt.subplot(1, 5, 2)
    plt.imshow(segmented_img)
    plt.title('segmented img')
    plt.xticks([])
    plt.yticks([])
    #
    plt.subplot(1, 5, 3)
    plt.imshow(thresh)
    plt.title('thresh_img')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 5, 4)
    plt.imshow(filled_mask)
    plt.title('filled_mask')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 5, 5)
    plt.imshow(masked_img)
    plt.title('masked_img')
    plt.xticks([])
    plt.yticks([])

    plt.show()

def main(args):
    img_path = args.baseroot
    save_path = args.save_dir
    for file_name in os.listdir(img_path):
        print(file_name)
        img = cv2.imread(img_path + '{}'.format(file_name))
        img = cv2.resize(img, (256,256))

        h, w, _ = img.shape

        img = np.array(img)
        print('img.shape :', img.shape)

        if args.segmentation:
            img_seg = img_segmentation(img)
        else:
            img_seg = img

        mask = np.zeros(shape=img.shape, dtype=np.uint8)
        mask[np.where((img_seg > [args.threshold, args.threshold, args.threshold]).all(axis=2))] = [255, 255, 255]

        thresh = mask.copy()

        if args.img_fill:
            fill_mask = fill_color(img, mask)
        else:
            fill_mask = mask

        masked = img.copy()

        masked[np.where((fill_mask > [230, 230, 230]).all(axis=2))] = [255, 255, 255]

        if args.img_show:
            fig_show(img, img_seg, thresh, fill_mask, masked)

        if args.save_fig:
            # Create a folder if it does`t folder
            createFolder(save_path)
            cv2.imwrite(save_path + '{}'.format(file_name), fill_mask)
