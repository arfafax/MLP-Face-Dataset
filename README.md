# MLP Faces Dataset
 A dataset of cropped MLP faces from Derpibooru.

![Preview grid](./docs/grid.jpg)

This dataset constains ~104k cropped MLP faces from Derpibooru. It was created by training a YOLOv3 network on annotated facial features from about 1500 faces.

Rather than provide the cropped images, this repo contains CSV files with the bounding boxes of the detected faces from my trained network, and a script to download the images from Derpibooru and crop them based on these CSVs.

The dimensions of the detected faces are shown in the following histogram:
![Dimensions](./docs/dimensions.png)

The distribution of characters is shown below:
![Characters](./docs/pony_counts.png)
