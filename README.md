# shape-detection-for-drone-images-
Given with the images dataset captured from drones, this can segment the required shapes from sliding window technique.

# Instructions:
1. Place the dataset images in ‘./dataset’ folder.
2. If the image are taken from a different dataset i.e., if it contains a differently structure
GCP, other than the given dataset. It is needed to be segmented manually and stored in
‘./others’ folder as the algorithm can only detect changes in zooming and angle and not for
the complete change in posture. Then run preprocessing.py to get the masks of different
angle and scale.
3. Run localization.py
4. The segmented image will be stored in ‘./chucks’ folder.
5. The GCP plotted image will be stored in ‘./GCP_marked’ folder.
6. The output will be stored in ‘./Sample_output.csv’ file.

# Benefits:
1. To find the GCP on the ‘L’ shaped object, the use of difference in centroid and the farrest
convexity hull is benificial as it will be more accurate even if the posture of the object
changes to minimum extend. The farrest convexity hull which are near the centre are
retained and the once that are away are cut out. So that the only possible go will be the hull
formed between the two arms of ‘L’ and it is considered as GCP.
2. The use of template matching algorithm is based on the fact that these shapes are stationary
for a paricular land and its image is easily acquirable. The possible changes to the image
will be the varying scales due to different zooming factor of the camera on drones and the
angle from where it is captured. If the algorithm is provided with images of all the possible
scaling and angles, it can detect the GCP’s more accurately.

# Drawbacks:
1. Execution time of the program is high as it will compare all the masks with all the sliding
windows. If provided with a large dataset, haar cascade detector can be employed for image
localization to reduce the execution time to a considerable extend.
(In the file i had attached the output and xml file of haar classifer for this dataset. As the
training images are very less and i don’t have any high processing power i can’t able to train
a better classifer)
2. If used for a new dataset, it requires manual segmentation of GCP’s chucks(Atleast one for a
dataset).

