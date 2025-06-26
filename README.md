# Text Component for Eyetracking Experiments in PsychoPy

A Text component for psychopy that computes and records each (space-separated) word's bounding box (i.e., a word-level ROI) in PsychoPy pixel coordinates. 

## Installation and Use
The easiest method of installation is to install directly from PsychoPy through pip/git. 

1. Open the PsychoPy Builder and navigate to "Tools > Plugin/packages Manager" froom the toolbar.

2. Open the "packages" tab and click "Open PIP terminal," in the bottom left of the screen.

![Install_OpenPipTerminal](https://github.com/user-attachments/assets/8a956cee-f259-4d1f-aeef-0d31b0df02dc)

3. In the box at the bottom of the new window, type `pip install git+https://github.com/SArehalli/psychopy-ETReading.git` to install the plugin from this repository.
   
![Install_PIP](https://github.com/user-attachments/assets/e4a25a7f-a49f-468d-95f7-5bea82173840)

5. Restart PsychoPy. You should see the "ETText" component in the component panel on the right.

The relevant options under "Formatting" are "Word Padding Width," which determines the size of spaces between words, "Alignment/Anchoring," which allows text to be aligned and anchored to the left or right of it's bounding box, and "Debug Bounding Box," which displays the recorded word ROI bounding boxes on-screen for testing. Otherwise, features match the standard "Text" component.
