#Name: Display Print progress
#Info: During printing, display the percentage of extruded filament
#Type: postprocess

# Written by David Szebdrei May 18, 2019
# Drop in your <CuraInstallation>/plugins/PostProcessingPlugin/scripts directory
# The code is based on https://www.thingiverse.com/thing:1220006.

from typing import Optional, Tuple

from UM.Logger import Logger
from ..Script import Script

class ProgressCalculator(Script):

    _layer_keyword = ";LAYER:"

    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Progress Calculator",
            "key": "ProgressCalculator",
            "metadata": {},
            "version": 2,
            "settings":{}
        }"""

    def execute(self, data: list):
        max_extrusion = None
        last_percent = None
        
        for data_index in reversed(range(len(data))):
            layer_data = data[data_index].split('\n')
            
            if not self.is_layer_data(layer_data):
                continue
            
            if max_extrusion is None:
                max_extrusion = self.find_largest_extrusion_value(layer_data)
            
            new_layer_data = list()
            for cmd_index in reversed(range(len(layer_data))):
                cmd = layer_data[cmd_index]
                e_value = self.find_e_value_in_cmd(cmd)
                
                if e_value > -1:
                    current_percent = int(100.0 * e_value / max_extrusion)
                    if last_percent is None or current_percent < last_percent :
                        new_layer_data.append(self.generate_percent_command(current_percent))
                        last_percent = current_percent
                    
                new_layer_data.append(cmd)
                
            data[data_index] = '\n'.join(reversed(new_layer_data))
                    
        return data
        
    def is_layer_data(self, layer_data):
        first_line = layer_data[0]
        return first_line[:len(self._layer_keyword)] == self._layer_keyword

    def generate_percent_command(self,percent):
        return 'M73 P{} ; GENERATED PERCENT'.format(percent)

    def find_e_value_in_cmd(self, cmd):
        tokens = cmd.split()
        for token in tokens:
            if not token.startswith("E"):
                continue

            raw_value = token[1:]
            
            try:
                v = float(raw_value);
                if (v > 0):
                    return v
            except ValueError:
                continue
        return -1

    def find_largest_extrusion_value(self, cmds):
        for cmd in reversed(cmds):
            e_value = self.find_e_value_in_cmd(cmd)
            if (e_value > 0):
                return e_value
        return 1