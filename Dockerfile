FROM nvidia/cuda:11.6.2-base-ubuntu20.04

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3 python3-pip
RUN pip install torch torchvision torchaudio nnunet matplotlib

ENV RESULTS_FOLDER="/root/results"

COPY inference.sh inference.sh
COPY nnUNet_trained_models /root/results

RUN chmod +x inference.sh
