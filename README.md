# flairstar

This pipeline allows to reconstruct the FLAIR* sequence by multiplying the FLAIR sequence with the magnitude T2star sequence. This pipeline is especially usesful to observe the Central Vein Sign for Multiple Sclerosis studies. This is based on the following docker of Blake Dewey: blakedewey/flairstar.

The first figure below shows the window of this pipeline. This window contains the following information:

* "Select subjects" input: allows the user to script the computation of the Flair* image for other subjects of the dataset by adding a list BIDS ID (without "sub-") separated by a comma. Possible values are: single BIDS ID (e.g. "001,002,006,013"), multiple folowing BIDS ID (e.g. "001-005" is the same as '001,002,003,004,005"), or all subjects ("all").

* "Select sessions" input: allows the user to script the computation of the Flair* image for other sessions of subjects of the dataset by adding a list session ID (without "ses-") separated by a comma. Possible values are: single session ID (e.g. "01,02,06,13"), multiple folowing session ID (e.g. "01-05" is the same as '01,02,03,04,05"), or all sessions ("all").

* "Computation of the Flair Star" button: launch the flairstar script based on all information given by the user.

**Typically, the computation of a Flair* image takes about 30 minutes**

![Flairstar Pipeline window](/Readme_pictures/flairstar_win.png)

The user needs to specify the name of the FLAIR sequence and the magnitude T2satr used in this dataset via the "add_info" dictionnary in the json file of the pipeline (cf. figure below). By default, the FLAIR sequence is "FLAIR" and the magnitude sequence is "part-mag_T2starw".

![Flairstar json file](/Readme_pictures/flairstar_json.png)
