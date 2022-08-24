import time
import odrive
from odrive.enums import *


def main():
    odrv0 = odrive.find_any()
    print('Setting a sample speed...')
    odrv0.axis1.controller.config.vel_gain = 0.05
    odrv0.axis1.controller.config.vel_integrator_gain = 0.1

    odrv0.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis1.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
    odrv0.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis1.controller.input_vel = 0.1
    print('Axis in closed loop control')
    time.sleep(10)
    odrv0.axis1.requested_state = AXIS_STATE_IDLE


if __name__ == '__main__':
    main()
