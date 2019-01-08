#!/usr/bin/python

# GIMP Luminosity Masks
# This plugin automates the creation of luminosity masks, as illustrated in this
# tutorial: https://www.gimp.org/tutorials/Luminosity_Masks/
# Copyright (c) 2019 Davide Sandona'
# sandona [dot] davide [at] gmail [dot] com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

from gimpfu import *

def luminosity_masks(image, n_channels):
    if image != None:
        # Set up an undo group, so the operation will be undone in one step.
        pdb.gimp_image_undo_group_start(image)

        # get active layer
        layer = image.active_layer
        # get name of the active layer
        name = pdb.gimp_item_get_name(layer)
        # copy the selected layer
        layer_copy = pdb.gimp_layer_new_from_drawable(layer, image)
        # insert the layer_copy on top of the layers stack
        pdb.gimp_image_insert_layer(image, layer_copy, None, 0)
        # desaturate the layer
        pdb.gimp_drawable_desaturate(layer_copy, DESATURATE_LIGHTNESS)

        # copy the red channel (at this point it could also be the blue or green, it does not matter). This is the Lightness channel (L1)
        L1 = pdb.gimp_channel_new_from_component(image, CHANNEL_RED, name + "-L1")
        # insert it at the top of the channels stack
        pdb.gimp_image_insert_channel(image, L1, None, 1)

        # create the Darkness channel (D1)
        D1 = copy_channel(image, L1, name + "-D1", 0)
        pdb.gimp_invert(D1)

        # collect the masks
        dark_channels = []
        light_channels = []
        mid_channels = []
        light_channels.append(L1)
        dark_channels.append(D1)

        more_channels = list(range(2, n_channels + 1))

        # create darker channels
        prev_ch = D1
        for i in more_channels:
            prev_ch = copy_channel(image, prev_ch, name + "-D" + str(i), i - 1)
            pdb.gimp_channel_combine_masks(prev_ch, L1, CHANNEL_OP_SUBTRACT, 0, 0)
            dark_channels.append(prev_ch)

        # create lighter channels
        prev_ch = L1
        for i in more_channels:
            prev_ch = copy_channel(image, prev_ch, name + "-L" + str(i), (n_channels + 1) + i - 1)
            pdb.gimp_channel_combine_masks(prev_ch, dark_channels[0], CHANNEL_OP_SUBTRACT, 0, 0)
            light_channels.append(prev_ch)

        # create midtones channels
        for i in range(len(dark_channels)):
            prev_ch = copy_channel(image, light_channels[i], name + "-M" + str(i + 1), n_channels + i)
            pdb.gimp_channel_combine_masks(prev_ch, dark_channels[i], CHANNEL_OP_INTERSECT, 0, 0)
            mid_channels.append(prev_ch)

        # remove the desaturated copy of the active layer
        pdb.gimp_image_remove_layer(image, layer_copy)

        # Close the undo group.
        pdb.gimp_image_undo_group_end(image)
        # End progress.
        pdb.gimp_progress_end()
    else:
        pdb.gimp_message("An image must be open to use Luminosity Masks.")

def copy_channel(image, ch, ch_name, pos):
    new_ch = pdb.gimp_channel_copy(ch)
    pdb.gimp_image_insert_channel(image, new_ch, None, pos)
    pdb.gimp_item_set_name(new_ch, ch_name)
    return new_ch

register(
        "python_fu_luminosity_mask",
        "Create luminosity masks.",
        "Create a given number of dark, light, midtone luminosity masks.",
        "Davide Sandona'",
        "Davide Sandona'",
        "2019",
        "Luminosity Masks...",
        "RGB*, GRAY*", # Alternately use RGB, RGB*, GRAY*, INDEXED etc.
        [
            (PF_IMAGE, "image", "Input image", None),
            (PF_INT, "n_channels", "Number of channels", 3)
        ],
        [],
        luminosity_masks,
        menu="<Image>/Layer/")

main()
