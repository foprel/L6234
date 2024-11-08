from machine import Pin, PWM
import math
import time


class BLDCMotorDriver:

    def __init__(
        self,
        pwm_frequency: int,
        pwm_resolution: int,
        sine_table_size: int,
        pwm_pins: list,
        ena_pins: list,    
    ):
        self.pwm_frequency = pwm_frequency
        self.pwm_resolution = pwm_resolution
        self.sine_table_size = sine_table_size
        self.pwm_pins = self._enable_pwm_pins(pwm_pins)
        self.ena_pins = self._enable_ena_pins(ena_pins)
        self.sine_table = self._create_sine_table(sine_table_size)

    def _enable_pwm_pins(self, pwm_pins) -> list:
        return [PWM(Pin(pwm_pin), self.pwm_frequency) for pwm_pin in pwm_pins]
    
    def _enable_ena_pins(self, ena_pins) -> list:
        return [Pin(ena_pin, Pin.OUT, Pin.PULL_UP) for ena_pin in ena_pins]

    def _create_sine_table(self, sine_table_size) -> list:
        sine_table = []
        for angle in range(sine_table_size):
            sine_value = math.sin(2 * math.pi * angle / sine_table_size)
            normalized_value = (sine_value + 1) / 2  # Normalize sine value to range [0, 1]
            scaled_value = int(normalized_value * self.pwm_resolution)  # Scale to integer resolution
            sine_table.append(scaled_value)
        return sine_table

    def set_motor_phases(self, angle) -> None:
        index_a = angle % self.sine_table_size
        index_b = (angle + 120) % self.sine_table_size
        index_c = (angle + 240) % self.sine_table_size
        
        duty_a = int(self.sine_table[index_a])
        duty_b = int(self.sine_table[index_b])
        duty_c = int(self.sine_table[index_c])
        
        print(f'{angle}, {duty_a}, {duty_b}, {duty_c}')
        
        self.pwm_pins[0].duty(duty_a)
        self.pwm_pins[1].duty(duty_b)
        self.pwm_pina[2].duty(duty_c)

if __name__ == '__main__':

    bldc_motor_driver = BLDCMotorDriver(
        pwm_frequency = 1000,
        pwm_resolution = (2 ** 8) - 1,
        sine_table_size = 360,
        pwm_pins = [8, 9, 10],
        ena_pins = [4, 5, 6],
    )
    
    angle = 0
    while True:
        set_motor_phases(angle % 360)
        angle += 1
        time.sleep_ms(1)  # Increased speed for smoother operation




# pwm_pins = [Pin(15), Pin(2), Pin(4)]
# pwms = [PWM(pin) for pin in pwm_pins]

# frequency = 1000 # 1 kHz

# for pwm in pwms:
#     pwm.freq(frequency)

# table_size = 360
# sine_table = [(int((math.sin(2 * math.pi * i / table_size))))]

# def set_pwm_duty_cycle(pwm, value):
#     duty_cycle = int(value / 255 * 1023)
#     pwm.duty(duty_cycle)

# def update_pwm(angle):
#     index = int(angle % table_size)
#     set_pwm_duty_cycle(pwms[0], sine_table[index])
#     set_pwm_duty_cycle(pwms[1], sine_table[index])
#     set_pwm_duty_cycle(pwms[1], sine_table[index])

# def main():
#     angle = 0
#     steps = 1
#     while True:
#         update_pwm(angle)
#         angle += steps
#         time.sleep_ms(1)