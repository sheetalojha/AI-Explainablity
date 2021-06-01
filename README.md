# AI-Explainablity
Expalaintion about why a machine learning model predicts a particular class for a given image. 

## About the model
Super pixels are generated for the input image. It is then modified by masking out differnt superpixels to find which are the ones of importance for the prediction. A group of pixels in close vicinity that share the same charachterisitics(like pixel intensity) is called a super pixel.

## How does it work?

- Upload the image to be explained in the content folder of your colab notebook. Rename it to "1.jpg"
- Import Inceptionv3 model from TF Hub for classifying our image
- Get top 5 classes predicted for the image by the above classifier
- Segment the image into superpixels using the quickshift segmentation algorithm
- Generate pertuberations of the origination image by randomly masking some of the superpixels
- Get predictions for the pertuberations generted in step5 using the pretrained classifier (Inception V3) from step2  
- Calculate the distances between the generated images and the original image
- Generate the weights to decide the importance factor for each generated/perturbed image 
- Use perturbations, predictions and weights to fit an explainable linear model
- Superpixels with larger coefficients have more importace, compute the top 4 super pixels



Try right now : https://colab.research.google.com/drive/1CXi7mjZbVlOXCXez1e9I4Jhvb-QmkGQ8?usp=sharing
