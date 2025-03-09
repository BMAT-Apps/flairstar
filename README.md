# flairstar

This pipeline allows to reconstruct the FLAIR* sequence by multiplying the FLAIR sequence with the magnitude T2star sequence. This pipeline is especially usesful to observe the Central Vein Sign for Multiple Sclerosis studies. This is based on the following docker of Blake Dewey: blakedewey/flairstar.

## How to cite
1. Sati P, George IC, Shea CD, Gaitán MI, Reich DS. FLAIR*: A Combined MR Contrast Technique for Visualizing White Matter Lesions and Parenchymal Veins. Radiology. 2012 Dec;265(3):926–32. 

## Utilization

The first figure below shows the window of this pipeline. This window contains the following information:

* "Select FLAIR image": open a File explorer and allow the user to specify the path towards the FLAIR image to use for the pipeline

* "Select T2starw magnitude image": open a File explorer and allow the user to specify the path towards the T2starw image to use for the pipeline

* "ouput derivative folder" input: precise the name of the derivative folder to store the ouput of the pipeline (default: flairstar)

* "output img name" input: precise the name of the output file (default: FLAIRstar)

* "Select subjects" input: allows the user to script the computation of the Flair* image for other subjects of the dataset by adding a list BIDS ID (without "sub-") separated by a comma. Possible values are: single BIDS ID (e.g. "001,002,006,013"), multiple folowing BIDS ID (e.g. "001-005" is the same as '001,002,003,004,005"), or all subjects ("all").

* "Select sessions" input: allows the user to script the computation of the Flair* image for other sessions of subjects of the dataset by adding a list session ID (without "ses-") separated by a comma. Possible values are: single session ID (e.g. "01,02,06,13"), multiple folowing session ID (e.g. "01-05" is the same as '01,02,03,04,05"), or all sessions ("all").

* "Compute FLAIRstar" button: launch the flairstar script based on all information given by the user.

**Typically, the computation of a Flair* image takes about 30 minutes**

![Flairstar Pipeline window](/Readme_pictures/flairstar_win.png)


