# Progress calculator
This sciprt changes your <i>percent indicator</i> to show the percent based on the extruded filament.

## Install
1) Copy the <b>ProgressCalculator.py</b> sciprt into <i>CURA_FOLDER/plugins/PostProcessingPlugin/scripts</i>.
2) Then restart the Cura.
3) In Cura select Extensions/Post Ptrocessing/Modify G-code.
4) In the popup click add script then select <b>Progress Calculator</b> and click close.

## Rounding 
Since the percent segment can only display integers the script cuts off the numbers after the decimal point without rounding. (e.g.: 55.75% -> 55%). I'm gonna improve this.

## Bugs
I've done some testing but if you find any problem in the script please create an issue.

## Credits 
I've used <b>petercmonaco</b>'s code and modified it.
You can find the original version [here](https://www.thingiverse.com/thing:1220006).
