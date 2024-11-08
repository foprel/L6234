from machine import Pin, PWM
import math
import time

frequency_pwm = 50_000 # 50 kHz (operating voltage of L6234)
resolution_bit = 10
resolution_int = (2 ** resolution_bit) - 1 

ena_pins = [Pin(17), Pin(18), Pin(21)]

for ena in ena_pins:
  ena.value(0)

pwm_pins = [Pin(8), Pin(9), Pin(10)]
pwms = [PWM(pin) for pin in pwm_pins]

for pwm in pwms:
    pwm.freq(frequency_pwm)


table_size = 360
sine_table = [(math.sin(math.radians(z)) + 1) / 2 * resolution_int for z in range(table_size + 1)]

def update_pwm(angle):

    # 1. Get three-phase indices
    index_a = angle % table_size
    index_b = (angle + 120) % table_size
    index_c = (angle + 240) % table_size

    # 2. Get PWM value from sine table
    duty_a = int(sine_table[index_a])
    duty_b = int(sine_table[index_b])
    duty_c = int(sine_table[index_c])

    # 3. Set pwm duty cycle
    pwms[0].duty(duty_a)
    pwms[1].duty(duty_b)
    pwms[2].duty(duty_c)

def main():
    angle = 0
    steps = 1
    while True:
        update_pwm(angle)
        angle += steps
        time.sleep_ms(100)
main()