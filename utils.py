import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import librosa
import torch
import torch.nn as nn
from eval import STFTMag 

def plot_tensor(tensor):
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 3))
    im = ax.imshow(tensor, aspect="auto", origin="lower", interpolation='none')
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    fig.canvas.draw()
    data = save_figure_to_numpy(fig)
    plt.close()
    return data

def save_figure_to_numpy(fig):
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data

def save_plot(tensor, savepath):
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 3))
    im = ax.imshow(tensor.cpu(), aspect="auto", origin="lower", interpolation='none')
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    fig.canvas.draw()
    
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    plt.savefig(savepath)
    plt.close()
    return

def save_plot_(tensor, savepath):
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 3))
    im = ax.imshow(tensor.cpu(), aspect="auto", origin="lower", interpolation='none')
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    fig.canvas.draw()
    plt.savefig(savepath)
    plt.close()
    return

def save_stft_plot(audio, savepath):
    
    secs = audio.size(0) / 48000
    stft = STFTMag(1024,256,1024).cuda()

    spec = stft(audio.squeeze(0)) # spec = [1, Channel, Time]
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    
    fig = plt.figure(figsize=(12, 3))

    plt.imshow(librosa.amplitude_to_db(spec.cpu().numpy(),
               ref=np.max, top_db = 80.),
               aspect='auto',
               origin='lower',
               interpolation='none',
               extent=(0,secs,0,24),)
            #    cmap='magma')
    plt.ylabel('Frequency (kHz)')
    plt.xticks([])
    plt.tight_layout()
    fig.savefig(savepath, format='png', dpi=400)
    plt.close()

    return
    

def sequence_mask(length, max_length=None):
    if max_length is None:
        max_length = length.max()
    x = torch.arange(int(max_length), dtype=length.dtype, device=length.device)
    return x.unsqueeze(0) < length.unsqueeze(1)
