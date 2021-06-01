# -*- coding: utf-8 -*-
"""AIExplainability.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CXi7mjZbVlOXCXez1e9I4Jhvb-QmkGQ8
"""

import os
import PIL
import numpy as np
from PIL import Image
from imageio import imread
import tensorflow as tf
import matplotlib.pyplot as plt
import keras
from keras.applications.imagenet_utils import decode_predictions
import skimage.io
from skimage import segmentation
import copy
import sklearn
import sklearn.metrics
from sklearn.linear_model import LinearRegression

#pretrained Inception V3 model
inceptionV3 = tf.keras.applications.InceptionV3(
    include_top=True,
    weights="imagenet",
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation="softmax",
)

path = "/content/1.jpg"
img = skimage.io.imread(path)
#resize to (299, 299) for inception V3 
img=skimage.transform.resize(img, (299, 299))
img1 = (img-0.5)*2
skimage.io.imshow(img)

#get prediction for this image top 5 predicted classes
preds = inceptionV3.predict(img1[np.newaxis,:,:,:])
decode_predictions(preds)[0] 
top_pred_classes = preds[0].argsort()[-5:][::-1]
top_pred_classes

superpixels = skimage.segmentation.quickshift(img1, kernel_size=4,max_dist=200, ratio=0.2)
skimage.io.imshow(skimage.segmentation.mark_boundaries(img, superpixels))

#creating 150 random pertuberations
num_perturb = 150
num_superpixels = np.unique(superpixels).shape[0]
perturbations = np.random.binomial(1, 0.5, size=(num_perturb, num_superpixels))

def perturb_image(img,perturbation,superpixels):
  active_pixels = np.where(perturbation == 1)[0]
  mask = np.zeros(superpixels.shape)
  for active in active_pixels:
      mask[superpixels == active] = 1 
  perturbed_image = copy.deepcopy(img)
  perturbed_image = perturbed_image*mask[:,:,np.newaxis]
  return perturbed_image

skimage.io.imshow(perturb_image(img,perturbations[0],superpixels))

predictions = []
for pert in perturbations:
  perturbed_img = perturb_image(img,pert,superpixels)
  pred = inceptionV3.predict(perturbed_img[np.newaxis,:,:,:])
  predictions.append(pred)

predictions = np.array(predictions)
predictions.shape

#distance b/w the generated images and original image
#the original image has all the superpixels active
og_img = np.ones(num_superpixels)[np.newaxis,:] 
distances = sklearn.metrics.pairwise_distances(perturbations,og_img, metric='euclidean').ravel()

distances.shape

#using kernel function to calculate weights for superpixels
kernel_width = 0.25
weights = np.sqrt(np.exp(-distances**2)/(kernel_width**2))

weights.shape

#simpler model to explain the predictions
class_to_explain = top_pred_classes[0]
model = LinearRegression()
model.fit(X=perturbations, y=predictions[:,:,class_to_explain], sample_weight=weights)
coeff = model.coef_[0]
coeff

#top 4 super pixels
num_top_features = 4
top_features = np.argsort(coeff)[-num_top_features:] 
top_features

mask = np.zeros(num_superpixels)
#Activate top superpixels 
mask[top_features]= True 
skimage.io.imshow(perturb_image(img,mask,superpixels))

