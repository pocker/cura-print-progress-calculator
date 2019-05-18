# Name: Display Print progress
# Info: During printing, display the percentage of extruded filament
# Type: postprocess

# Written by David Szebdrei May 18, 2019
# Drop in your <CuraInstallation>/plugins/PostProcessingPlugin/scripts directory
# The code is based on https://www.thingiverse.com/thing:1220006.

from UM.Logger import Logger
from ..Script import Script


class Calculator:
    _layer_keyword = ";LAYER:"

    def __init__(self):
        pass

    def calculate(self, data: list):

        last_percent = 0
        zeroing_level = 1
        zeroing, max_extrusion = self.find_zeroing_and_max_extrusion(data)

        for data_index in range(len(data)):
            layer_data = data[data_index].split('\n')

            if not self.is_layer_data(layer_data):
                continue

            new_layer_data = list()
            for cmd in layer_data:
                new_layer_data.append(cmd)

                if self.is_extruder_set_zero(cmd):
                    zeroing_level += 1
                    continue

                e_value = self.find_e_value_in_cmd(cmd)
                if e_value == -1:
                    continue

                zeroing_offset = sum(zeroing[:zeroing_level])
                current_percent = self.round(100.0 * (e_value + zeroing_offset) / max_extrusion)
                if current_percent > last_percent:
                    new_layer_data.append(self.generate_percent_command(current_percent))
                    last_percent = current_percent

            data[data_index] = '\n'.join(new_layer_data)

        return data

    def find_zeroing_and_max_extrusion(self, data: list) -> (list, int):
        zeroing = [0]
        max_extrusion = 0

        for layer in data:
            cmds = layer.split('\n')

            if not self.is_layer_data(cmds):
                continue

            for index, cmd in enumerate(cmds):
                if self.is_extruder_set_zero(cmd):
                    e_value = self.find_e_value_in_cmd(cmds[index - 1])
                    zeroing.append(e_value)
                    max_extrusion = 0
                else:
                    e_value = self.find_e_value_in_cmd(cmd)
                    if e_value > max_extrusion:
                        max_extrusion = e_value

        max_extrusion += sum(zeroing)

        return zeroing, max_extrusion

    def is_layer_data(self, layer_data: list) -> bool:
        first_line = layer_data[0]
        return first_line[:len(self._layer_keyword)] == self._layer_keyword

    @staticmethod
    def find_e_value_in_cmd(cmd: str) -> float:
        tokens = cmd.split()
        for token in tokens:
            if not token.startswith("E"):
                continue

            raw_value = token[1:]

            try:
                v = float(raw_value)
                if v > 0:
                    return v
            except ValueError:
                continue
        return -1

    @staticmethod
    def is_extruder_set_zero(cmd: str) -> bool:
        return cmd.startswith('G92') and 'E0' in cmd

    @staticmethod
    def generate_percent_command(percent: int) -> str:
        return 'M73 P{} ; GENERATED PERCENT'.format(percent)

    def find_largest_extrusion_value(self, cmds: list) -> float:
        for cmd in reversed(cmds):
            e_value = self.find_e_value_in_cmd(cmd)
            if e_value > 0:
                return e_value
        return 1

    @staticmethod
    def round(value: float) -> int:
        return int(value)


class ProgressCalculator(Script):
    _layer_keyword = ";LAYER:"

    def __init__(self):
        super().__init__()
        self.calculator = Calculator()

    def getSettingDataString(self):
        return """{
            "name":"Progress Calculator",
            "key": "ProgressCalculator",
            "metadata": {},
            "version": 2,
            "settings":{}
        }"""

    def execute(self, data: list):
        return self.calculator.calculate(data)
