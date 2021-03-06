"""
visualize results for test image
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from torch.autograd import Variable

# import transforms as transforms
from torchvision import transforms
import skimage
from skimage import io
from skimage import transform

# from models import VGG
import models

cut_size = 44

transform_test = transforms.Compose([
    transforms.TenCrop(cut_size),
    transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
])

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


test_image_path = os.path.join('images', '3.jpg')
raw_img = skimage.io.imread(test_image_path)  # skimage

gray = rgb2gray(raw_img)
gray = skimage.transform.resize(gray, (48,48), mode='symmetric').astype(np.uint8)  # skimage

img = gray[:, :, np.newaxis]

img = np.concatenate((img, img, img), axis=2)
img = Image.fromarray(img)

print(len(img.mode), img.size)

inputs = transform_test(img)

print(inputs.size())

class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

net = models.VGG19()
if torch.cuda.is_available():
    checkpoint = torch.load(os.path.join('FER2013_VGG19', 'PrivateTest_model.t7'))
else:
    checkpoint = torch.load(
        os.path.join('FER2013_VGG19', 'PrivateTest_model.t7'),
        map_location=torch.device('cpu'),
    )

net.load_state_dict(checkpoint['net'])
if torch.cuda.is_available():
    net.cuda()
net.eval()

ncrops, c, h, w = np.shape(inputs)

inputs = inputs.view(-1, c, h, w)
if torch.cuda.is_available():
    inputs = inputs.cuda()

torch.no_grad()
inputs = Variable(inputs)
outputs = net(inputs)

print(outputs)

print(outputs.size())

outputs_avg = outputs.view(ncrops, -1).mean(0)  # avg over crops

score = F.softmax(outputs_avg, dim=-1)

_, predicted = torch.max(outputs_avg.data, 0)

plt.rcParams['figure.figsize'] = (13.5,5.5)
axes=plt.subplot(1, 3, 1)
plt.imshow(raw_img)
plt.xlabel('Input Image', fontsize=16)
axes.set_xticks([])
axes.set_yticks([])
plt.tight_layout()


plt.subplots_adjust(left=0.05, bottom=0.2, right=0.95, top=0.9, hspace=0.02, wspace=0.3)

plt.subplot(1, 3, 2)
ind = 0.1+0.6*np.arange(len(class_names))    # the x locations for the groups
width = 0.4       # the width of the bars: can also be len(x) sequence
color_list = ['red','orangered','darkorange','limegreen','darkgreen','royalblue','navy']
for i in range(len(class_names)):
    plt.bar(ind[i], score.data.cpu().numpy()[i], width, color=color_list[i])
plt.title("Classification results ",fontsize=20)
plt.xlabel(" Expression Category ",fontsize=16)
plt.ylabel(" Classification Score ",fontsize=16)
plt.xticks(ind, class_names, rotation=45, fontsize=14)

axes=plt.subplot(1, 3, 3)
emojis_img = io.imread('images/emojis/%s.png' % str(class_names[int(predicted.cpu().numpy())]))
plt.imshow(emojis_img)
plt.xlabel('Emoji Expression', fontsize=16)
axes.set_xticks([])
axes.set_yticks([])
plt.tight_layout()
# show emojis

#plt.show()
os.makedirs('images/results', exist_ok=True)
path, file = os.path.split(test_image_path)

results_path = os.path.join('images', 'results', 'results_' + file)
plt.savefig(results_path)
plt.close()

print(f"The expression in {test_image_path} is {str(class_names[int(predicted.cpu().numpy())])}")
