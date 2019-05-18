# Progress calculator

This sciprt change your <i>percent indicator</i> to show the percent based on the extruded filament.

## Install
1) Just copy the <b>ProgressCalculator.py</b> sciprt into the <i>CURA_FOLDER/plugins/PostProcessingPlugin/scripts</i>.
2) Then restart the Cura
3) bgIn Cura select Extensions/Post Ptrocessing/Modify G-code
4) In the popup click add script then select <b>Progress Calculator</b>

## Rounding 
Since the percent segment can't display just integers right now the script just cut the numbers after the decimal point (e.g.: 55.75% -> 55%). I'm gonna imporive this part.

## Bugs
I've did some testing but if you found any problem with the script please create an issue.

## Credits 
I've used <b>petercmonaco</b>'s code and modified it.
You can find the original version [here](https://www.thingiverse.com/thing:1220006).
