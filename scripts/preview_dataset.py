#!/usr/bin/env python3

import os
import cv2
import math
import xmljson
import argparse
import numpy as np
from scipy import interpolate
from lxml.etree import fromstring

import sys
print(sys.version)

# load LMTs
images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
lmt_images = {
    str(i): cv2.imread(os.path.join(images_dir, 'lmt', 'type_{}.png'.format(i)))
    for i in range(8)
}


def draw_spline(image, lane, ys, color=[0, 0, 255]):
    lane = [lane for lane in lane if str(lane) != 'nan']
    pts = [[x, ys[i]]for i, x in enumerate(lane) if not math.isnan(x)]
    if len(pts)-1 > 0:
        spline = interpolate.splrep([pt[1] for pt in pts], [pt[0] for pt in pts], k=len(pts)-1)
        for i in range(min([pt[1] for pt in pts]), max([pt[1] for pt in pts])):
            image[i, int(interpolate.splev(i, spline)), :] = color
    return image


def apply_ipm(img, config, ys):
    # IPM
    y_top, y_bottom = min(ys), max(ys)
    ipm_pts = config['dataset']['ipm_points']
    roi = config['dataset']['region_of_interest']

    src = np.array([
        [ipm_pts['@top_left'], y_top],
        [ipm_pts['@top_right'], y_top],
        [ipm_pts['@bottom_right'], y_bottom],
        [ipm_pts['@bottom_left'], y_bottom],

       ], dtype="float32")

    dst = np.array([
        [ipm_pts['@top_left'], 0],
        [ipm_pts['@top_right'], 0],
        [ipm_pts['@top_right'], roi['@height']],
        [ipm_pts['@top_left'], roi['@height']],
       ], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, M, (roi['@width'], roi['@height']))


def draw_lmt(img, lmt_left, lmt_right):
    lmts_left = str(lmt_left).split(';')
    lmts_right = str(lmt_right).split(';')

    for i, lmt in enumerate(lmts_left):
        lmt_img_start = (i+1)*10 + i*lmt_images[lmt].shape[1]
        lmt_img_end = (i+1)*(10 + lmt_images[lmt].shape[1])
        img[10:10+lmt_images[lmt].shape[0], lmt_img_start:lmt_img_end, :] = lmt_images[lmt]

    for i, lmt in enumerate(lmts_right):
        lmt_img_start = (i+1)*(-lmt_images[lmt].shape[1]-10)
        lmt_img_end = (i+1)*(-10) - i*lmt_images[lmt].shape[1]
        img[10:10+lmt_images[lmt].shape[0], lmt_img_start:lmt_img_end, :] = lmt_images[lmt]

    return img


def main(dataset_dir, fps):

    # read config.xml
    config = None
    config_fname = os.path.join(dataset_dir, 'config.xml')
    if not os.path.isfile(config_fname):
        raise Exception('config.xml not found: {}'.format(config_fname))
    with open(config_fname, 'r') as hf:
        config = xmljson.badgerfish.data(fromstring(hf.read()))['config']

    # read ground truth
    gt = None
    gt_fname = os.path.join(dataset_dir, 'groundtruth.xml')
    if not os.path.isfile(gt_fname):
        raise Exception('groundtruth.xml not found: {}'.format(gt_fname))
    with open(gt_fname, 'r') as hf:
        gt = xmljson.badgerfish.data(fromstring(hf.read()))['groundtruth']

    # display dataset and annotations
    for frame in gt['frames']['frame']:
        img_fname = os.path.join(dataset_dir, 'images/lane_{}.png'.format(frame['@id']))
        img = cv2.imread(img_fname)
        if img is None:
            print('Failed to load image: {}'.format(img_fname))

        # vars
        y, h = config['dataset']['region_of_interest']['@y'], config['dataset']['region_of_interest']['@height']
        ys = [y, math.ceil(y + h / 4.), math.ceil(y + h / 2.), y + h - 1]

        # IPM
        ipm_img = apply_ipm(img, config, ys)

        # draw lanes
        pts = ['p1', 'p2', 'p3', 'p4']
        img = draw_spline(img, [frame['position']['left'][pt]['$'] for pt in pts], ys)
        img = draw_spline(img, [frame['position']['right'][pt]['$'] for pt in pts], ys)

        # show LMT
        img = draw_lmt(img, frame['@lmtLeft'], frame['@lmtRight'])

        cv2.imshow('img', img)
        cv2.imshow('ipm', ipm_img)
        cv2.waitKey(int(1000/float(fps)))
    exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preview annotations of a ELAS dataset')
    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--fps', type=int, required=False, default=30)
    argv = parser.parse_args()

    main(argv.dataset, argv.fps)
