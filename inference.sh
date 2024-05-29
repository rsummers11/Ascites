#! /bin/bash

nnUNet_predict -i /tmp/INPUT_FOLDER/ -o output_fold_0 -t 505 -m 3d_fullres -f 0 --save_npz
nnUNet_predict -i /tmp/INPUT_FOLDER/ -o output_fold_1 -t 505 -m 3d_fullres -f 1 --save_npz
nnUNet_predict -i /tmp/INPUT_FOLDER/ -o output_fold_2 -t 505 -m 3d_fullres -f 2 --save_npz
nnUNet_predict -i /tmp/INPUT_FOLDER/ -o output_fold_3 -t 505 -m 3d_fullres -f 3 --save_npz
nnUNet_predict -i /tmp/INPUT_FOLDER/ -o output_fold_4 -t 505 -m 3d_fullres -f 4 --save_npz

nnUNet_ensemble -f output_fold_0 output_fold_1 output_fold_2 output_fold_3 output_fold_4 -o /tmp/OUTPUT_FOLDER/
