import argparse
import os
import shutil
import random
# import time

from nnunet.inference.predict import predict_from_folder


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Inference using nnU-Net predict_from_folder Python API')
    parser.add_argument('-i', '--input_list', help='Input image file_list.txt')
    parser.add_argument('-t', '--tmp_folder', help='Temporary folder', required=True)
    parser.add_argument('-o', '--output_folder', help='Output Segmentation folder', required=True)
    parser.add_argument('-m', '--model', help='Trained Model', required=True)
    parser.add_argument('-v', '--verbose', help='Verbose Output', action='store_true', default=False)
    args = vars(parser.parse_args())

    # Append 8bit random hex string to ensure tmp_folder is unique
    args['tmp_folder'] += f'_{str(hex(random.getrandbits(8)))}'

    # Create temp directory
    os.mkdir(args['tmp_folder'])

    # Read input filelist
    with open(args['input_list']) as f:
        image_list = f.read().splitlines()

    # Make destination file paths to tmp_folder
    image_list_link = [os.path.join(args['tmp_folder'], os.path.basename(x).replace('.nii.gz', '_0000.nii.gz'))
                       for x in image_list]

    # Create hard link or copy
    for src, dst in zip(image_list, image_list_link):
        try:
            os.link(src, dst)
        except:
            shutil.copyfile(src, dst)

    # Run nnU-Net predict on tmp_folder
    # start = time.time()
    predict_from_folder(args['model'], args['tmp_folder'], args['output_folder'], folds=None, save_npz=False,
                        num_threads_preprocessing=6, num_threads_nifti_save=2,
                        lowres_segmentations=None, part_id=0, num_parts=1, tta=False,
                        overwrite_existing=False, mode="fastest", overwrite_all_in_gpu=None,
                        mixed_precision=True, step_size=0.5, checkpoint_name="model_final_checkpoint")
    # end = time.time()
    # print(f"pred time: {end - start}")

    # Cleanup and delete tmp_folder
    shutil.rmtree(args['tmp_folder'])
