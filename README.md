# GIMP Plugins

This repository contains plugins I coded for GIMP.
All these plugins have been tested with GIMP v2.10.

## Luminosity Masks

This plugin automates the creation of luminosity masks, as illustrated in [this tutorial](https://www.gimp.org/tutorials/Luminosity_Masks/).

To install it, copy the `luminosity_masks.py` file into the `~/.config/GIMP/2.10/gimp-plugins` folder, change its permission to allow executing as a program (using the command `chmod +x luminosity_mask.py`).

Then open GIMP and load the image you are interested to modify. You can find the plugin in the menu `Layer/Luminosity Masks...`.  

You can create any number of luminosity masks: just select the layer of interest, and apply the plugin. A small dialog windows will open, where you can choose the number of luminosity masks to create! By default, the plugin will create 3 darks channels, 3 lights channels and 3 midtones channels.

The luminosity masks will appear in the `Channels Dialog`.
