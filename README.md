# Ascites Segmentation with nnUNet

## Ascites Dataset (TCGA-OV-AS)

This dataset is derived from [TCGA-OV](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=7569497) Dataset. Download the data from TCIA with **Descriptive Directory Name** download option.

### Converting Images

Convert the DICOMs to NIFTI format using `dcm2niix` and `GNU parallel`.

1. Create the directory structure required for each NIFTI file:
   1. `find TCGA-OV -type d -exec mkdir -p -- /tmp/{} \;`
   2. `mv /tmp/TCGA-OV ./TCGA-OV-NIFTI`

2. Convert DICOMs to NIFTI
   1. `parallel --jobs $n < jobs.txt` where `$n` is number of parallel jobs.

### Ascites Labels

285 images that are free of corruption have been hand-picked for use, images mostly consist of **ABDOMEN-PELVIS** scans. Labels can be downloaded [here](https://nihcc.box.com/s/uea6qbmrd5rgdup7jufga1k7pavas671).

### Clinical Information

Patient clinical data can be downloaded from TCIA: [TCGA-OV Clinical Data.zip
](https://wiki.cancerimagingarchive.net/download/attachments/7569497/TCGA-OV%20Clinical%20Data%201516.zip?version=1&modificationDate=1452105785692&api=v2)


## Method 1: Run Inference using `nnunet_predict.py`

1. Install the latest version of [nnUNet](https://github.com/MIC-DKFZ/nnUNet#installation) and [PyTorch](https://pytorch.org/get-started/locally/).

```shell
user@machine:~/ascites_segmentation$ pip install torch torchvision torchaudio nnunet matplotlib
```

2. Download model and weights:

- [ascites_model.tar.gz](https://nihcc.app.box.com/s/oc81mic9k8vre30fq0eanxqp9kdwern2) 
<br> Size: 1.1G <br> MD5: `d39aa7f8d29bddd4edf9e4b24a8f55a1`

3. Run inference with command:

```shell
user@machine:~/ascites_segmentation$ python nnunet_predict.py -i file_list.txt -t TMP_DIR -o OUTPUT_FOLDER -m /path/to/nnunet/model_weights
```

```shell
usage: tmp.py [-h] [-i INPUT_LIST] -t TMP_FOLDER -o OUTPUT_FOLDER -m MODEL [-v]

Inference using nnU-Net predict_from_folder Python API

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_LIST, --input_list INPUT_LIST
                        Input image file_list.txt
  -t TMP_FOLDER, --tmp_folder TMP_FOLDER
                        Temporary folder
  -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                        Output Segmentation folder
  -m MODEL, --model MODEL
                        Trained Model
  -v, --verbose         Verbose Output
```



N.B. 
- `model_weights` folder should contain `fold0`, `fold1`, etc...
- WARNING: the program will try to create file links first, but will fallback to filecopy if fails


## Method 2: Run Inference using `nnUNet_predict` from shell

1. Install the latest version of [nnUNet](https://github.com/MIC-DKFZ/nnUNet#installation) and [PyTorch](https://pytorch.org/get-started/locally/).

```shell
user@machine:~/ascites_segmentation$ pip install torch torchvision torchaudio nnunet matplotlib
```

2. Download model and weights:

- [ascites_model.tar.gz](https://nihcc.app.box.com/s/oc81mic9k8vre30fq0eanxqp9kdwern2) 
<br> Size: 1.1G <br> MD5: `d39aa7f8d29bddd4edf9e4b24a8f55a1`

3. Place checkpoints in directory tree:

```shell
user@machine:~/ascites_segmentation$ tree .
.
├── nnUNet_preprocessed
├── nnUNet_raw_data_base
└── nnUNet_trained_models
    └── nnUNet
        └── 3d_fullres
            └── Task505_TCGA-OV
                └── nnUNetTrainerV2__nnUNetPlansv2.1
                    ├── fold_0
                    │   ├── debug.json
                    │   ├── model_final_checkpoint.model
                    │   ├── model_final_checkpoint.model.pkl
                    │   └── progress.png
                    ├── fold_1
                    │   ├── debug.json
                    │   ├── model_final_checkpoint.model
                    │   ├── model_final_checkpoint.model.pkl
                    │   └── progress.png
                    ├── fold_2
                    │   ├── model_final_checkpoint.model
                    │   ├── model_final_checkpoint.model.pkl
                    │   └── progress.png
                    ├── fold_3
                    │   ├── model_final_checkpoint.model
                    │   ├── model_final_checkpoint.model.pkl
                    │   └── progress.png
                    ├── fold_4
                    │   ├── model_final_checkpoint.model
                    │   ├── model_final_checkpoint.model.pkl
                    │   └── progress.png
                    └── plans.pkl
```

4. Setup environment variables so that nnU-Net knows where to find trained models: 

```shell
user@machine:~/ascites_segmentation$ export nnUNet_raw_data_base="/absolute/path/to/nnUNet_raw_data_base"
user@machine:~/ascites_segmentation$ export nnUNet_preprocessed="/absolute/path/to/nnUNet_preprocessed"
user@machine:~/ascites_segmentation$ export RESULTS_FOLDER="/absolute/path/to/nnUNet_trained_models"
```

5. Run inference with command:

```shell
user@machine:~/ascites_segmentation$ nnUNet_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -t 505 -m 3d_fullres -f N --save_npz 
```

where:
- `-i`: input folder of `.nii.gz` scans to predict. NB, filename needs to end with `_0000.nii.gz` to tell nnU-Net only one kind of modality
- `-o`: output folder to store predicted segmentations, automatically created if not exist
- `-t 505`: (do not change) Ascites pretrained model name
- `-m 3d_fullres` (do not change) Ascites pretrained model name
- `N`: Ascites pretrained model fold, can be `[0, 1, 2, 3, 4]`
- `--save_npz`: save softmax scores, required for ensembling multiple folds 

### Optional [Additional] Inference Steps

a. use `nnUNet_find_best_configuration` to automatically get the inference commands needed to run the trained model on data.

b. ensemble predictions using `nnUNet_ensemble` by running:

```shell
user@machine:~/ascites_segmentation$ nnUNet_ensemble -f FOLDER1 FOLDER2 ... -o OUTPUT_FOLDER -pp POSTPROCESSING_FILE
```

where `FOLDER1` and `FOLDER2` are predicted outputs by nnUNet (requires `--save_npz` when running `nnUNet_predict`).

## Method 3: Docker Inference

Requires `nvidia-docker` to be installed on the system ([Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)). This `nnunet_docker` predicts ascites with all 5 trained folds and ensembles output to a single prediction.

1. Build the `nnunet_docker` image from `Dockerfile`:

```shell
user@machine:~/ascites_segmentation$ sudo docker build -t nnunet_docker .
```

2. Run docker image on test volumes:

```shell
user@machine:~/ascites_segmentation$ sudo docker run \
--gpus 0 \
--volume /absolute/path/to/INPUT_FOLDER:/tmp/INPUT_FOLDER \
--volume /absolute/path/to/OUTPUT_FOLDER:/tmp/OUTPUT_FOLDER \
nnunet_docker /bin/sh inference.sh
```



- `--gpus` parameter:
  - `0, 1, 2, ..., n` for integer number of GPUs 
  - `all` for all available GPUs on the system
  - `'"device=2,3"'` for specific GPU with ID

- `--volume` parameter
  - `/absolute/path/to/INPUT_FOLDER` and `/absolute/path/to/OUTPUT_FOLDER` folders on the host system needs to be specified
  - `INPUT_FOLDER` contains all `.nii.gz` volumes to be predicted
  - predicted results will be written to `OUTPUT_FOLDER`

