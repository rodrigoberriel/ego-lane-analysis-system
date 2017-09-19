## Ego-Lane Analysis System

Rodrigo F. Berriel, Edilson de Aguiar, Alberto F. de Souza, and Thiago Oliveira-Santos

Published in *Image and Vision Computing*: [10.1016/J.IMAVIS.2017.07.005](https://doi.org/10.1016/J.IMAVIS.2017.07.005)

[![Graphical-Abstract](https://github.com/rodrigoberriel/ego-lane-analysis-system/blob/master/images/graphical-abstract.png)](http://www.sciencedirect.com/science/article/pii/S0262885617301130)

#### Abstract

Decreasing costs of vision sensors and advances in embedded hardware boosted lane related research – detection, estimation, tracking, etc. – in the past two decades. The interest in this topic has increased even more with the demand for advanced driver assistance systems (ADAS) and self-driving cars. Although extensively studied independently, there is still need for studies that propose a combined solution for the multiple problems related to the ego-lane, such as lane departure warning (LDW), lane change detection, lane marking type (LMT) classification, road markings detection and classification, and detection of adjacent lanes (i.e., immediate left and right lanes) presence. In this paper, we propose a real-time Ego-Lane Analysis System (ELAS) capable of estimating ego-lane position, classifying LMTs and road markings, performing LDW and detecting lane change events. The proposed vision-based system works on a temporal sequence of images. Lane marking features are extracted in perspective and Inverse Perspective Mapping (IPM) images that are combined to increase robustness. The final estimated lane is modeled as a spline using a combination of methods (Hough lines with Kalman filter and spline with particle filter). Based on the estimated lane, all other events are detected. To validate ELAS and cover the lack of lane datasets in the literature, a new dataset with more than 20 different scenes (in more than 15,000 frames) and considering a variety of scenarios (urban road, highways, traffic, shadows, etc.) was created. The dataset was manually annotated and made publicly available to enable evaluation of several events that are of interest for the research community (i.e., lane estimation, change, and centering; road markings; intersections; LMTs; crosswalks and adjacent lanes). Moreover, the system was also validated quantitatively and qualitatively on other public datasets. ELAS achieved high detection rates in all real-world events and proved to be ready for real-time applications.

### ELAS Database

To request access to the datasets, read the instructions [here](https://github.com/rodrigoberriel/ego-lane-analysis-system/blob/master/datasets/).

### Videos

Demonstration video of ELAS:

[![Video1](https://github.com/rodrigoberriel/ego-lane-analysis-system/blob/master/images/thumb-video-1.png)](https://youtu.be/NPU9tiyA8vw)

ELAS was weakly integrated into [IARA](http://www.lcad.inf.ufes.br/wiki/index.php/IARA) (our autonomous vehicle). The video below shows ELAS performing on IARA (without tuning any parameter):

[![Video2](https://github.com/rodrigoberriel/ego-lane-analysis-system/blob/master/images/thumb-video-2.png)](https://youtu.be/R5wdPJ4ZI5M)

### Source-code

I'm working on the source-code to make it easier to use. Meanwhile, you can use [this code](https://github.com/LCAD-UFES/carmen_lcad/tree/master/src/lane_analysis).

### BibTeX

    @article{berriel2017imavis,
        Author  = {Rodrigo F. Berriel and Edilson de Aguiar and Alberto F. de Souza and Thiago Oliveira-Santos},
        Title   = {{Ego-Lane Analysis System (ELAS): Dataset and Algorithms}},
        Journal = {Image and Vision Computing},
        Year    = {2017},
        DOI     = {10.1016/J.IMAVIS.2017.07.005},
        ISSN    = {0262-8856},
    }