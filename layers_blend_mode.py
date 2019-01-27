#!/usr/bin/python

# GIMP Layers Blend Mode
# This plugin automates the application of a specific blend mode to all layers
# or only the visible layers.
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

def get_blend_mode_value(b):
    blend_modes = {
        0: LAYER_MODE_NORMAL,
        1: LAYER_MODE_COLOR_ERASE,
        2: LAYER_MODE_ERASE,
        3: LAYER_MODE_MERGE,
        4: LAYER_MODE_SPLIT,
        5: LAYER_MODE_LIGHTEN_ONLY,
        6: LAYER_MODE_LUMA_LIGHTEN_ONLY,
        7: LAYER_MODE_SCREEN,
        8: LAYER_MODE_DODGE,
        9: LAYER_MODE_ADDITION,
        10: LAYER_MODE_DARKEN_ONLY,
        11: LAYER_MODE_LUMA_DARKEN_ONLY,
        12: LAYER_MODE_MULTIPLY,
        13: LAYER_MODE_BURN,
        14: LAYER_MODE_LINEAR_BURN,
        15: LAYER_MODE_OVERLAY,
        16: LAYER_MODE_VIVID_LIGHT,
        17: LAYER_MODE_PIN_LIGHT,
        18: LAYER_MODE_LINEAR_LIGHT,
        19: LAYER_MODE_HARD_MIX,
        20: LAYER_MODE_DIFFERENCE,
        21: LAYER_MODE_EXCLUSION,
        22: LAYER_MODE_SUBTRACT,
        23: LAYER_MODE_GRAIN_EXTRACT,
        24: LAYER_MODE_GRAIN_MERGE,
        25: LAYER_MODE_DIVIDE,
        26: LAYER_MODE_HSV_HUE,
        27: LAYER_MODE_HSV_SATURATION,
        28: LAYER_MODE_HSL_COLOR,
        29: LAYER_MODE_HSV_VALUE,
        30: LAYER_MODE_LCH_HUE,
        31: LAYER_MODE_LCH_CHROMA,
        32: LAYER_MODE_LCH_COLOR,
        33: LAYER_MODE_LCH_LIGHTNESS,
        34: LAYER_MODE_LUMINANCE
    }
    print(b)
    if b in blend_modes.keys():
        return blend_modes[b]
    else:
        return None

def set_blend_mode(image, blend_mode, opacity, which_layers):
    if image != None:
        # Set up an undo group, so the operation will be undone in one step.
        pdb.gimp_image_undo_group_start(image)

        for layer in image.layers:
            if which_layers == "All" or layer.visible:
                layer.mode = get_blend_mode_value(blend_mode) # pdb.gimp_layer_set_mode
                layer.opacity = opacity

        # Close the undo group.
        pdb.gimp_image_undo_group_end(image)
        # End progress.
        pdb.gimp_progress_end()
    else:
        pdb.gimp_message("An image must be open to use Luminosity Masks.")

register(
        "python_fu_layers_blend_mode",
        "Applies the same blend mode and opacity to multiple layers.",
        "Applies the same blend mode and opacity to multiple layers.",
        "Davide Sandona'",
        "Davide Sandona'",
        "2019",
        "Layers Blend Mode...",
        "RGB*, GRAY*", # Alternately use RGB, RGB*, GRAY*, INDEXED etc.
        [
            (PF_IMAGE, "image", "Input image", None),
            (PF_OPTION, "blend_mode", "Blend Mode", 0, ( "Normal", "Color Erase", "Erase", "Merge", "Split", "Lighten Only", "Luma Lighten Only", "Screen", "Dodge", "Addition", "Darken Only", "Luma Darken Only", "Multiply", "Burn", "Linear Burn", "Overlay", "Vivid Light", "Pin Light", "Linear Light", "Hard Mix", "Difference", "Exclusion", "Subtract", "Grain Extract", "Grain Merge", "Divide", "HSV Hue", "HSV Saturation", "HSL Color", "HSV Value", "LCH Hue", "LCH Chroma", "LCH Color", "LCH Lightness", "Luminance" )),
            (PF_SLIDER, "opacity",  "Opacity", 100, (0, 100, 1)),
            (PF_RADIO, "all_layers", "Which Layers", "Visible",
          (("Visible", "Visible"), ("All", "All"))),
        ],
        [],
        set_blend_mode,
        menu="<Image>/Layer/")

main()
