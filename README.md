# SpesBot

Spes Robotics reference platform.

## Quick Start

```bash
mkdir -p $HOME/spesbot_ws/src
git clone git@github.com:SpesRobotics/spesbot.git $HOME/spesbot_ws/src/spesbot

# Build the Docker image
make -f $HOME/spesbot_ws/src/spesbot/docker/Makefile build
make -f $HOME/spesbot_ws/src/spesbot/docker/Makefile run
make -f $HOME/spesbot_ws/src/spesbot/docker/Makefile exec-<pc or sbc>

# Build packages
vcs import src < src/spesbot/spesbot.repos
colcon build
source install/local_setup.bash
```

## Parts

- Baseus Blade USB C 100W ([link](https://us.baseus.com/p/baseus-blade-usb-c-100w-20000mah-power-bank-107))
- Intel® RealSense™ Depth Camera D435 ([link](https://www.intelrealsense.com/depth-camera-d435/))
- 360 Laser Distance Sensor LDS-01 ([link](https://www.robotis.us/360-laser-distance-sensor-lds-01-lidar/), [alternative](https://www.ebay.com/sch/i.html?_nkw=robot+2d+lidar+360), [docs](https://emanual.robotis.com/assets/docs/LDS_Basic_Specification.pdf))
- Raspberry Pi 4 ([link](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/))
- ODrive v3.6 ([link](https://odriverobotics.com/shop/odrive-v36), [alternative](https://www.aliexpress.com/wholesale?SearchText=odrive))
- PD Decoy Board ([link](https://www.aliexpress.com/wholesale?SearchText=PD+decoy))
- Hoverboard Wheel ([link](https://www.aliexpress.com/wholesale?SearchText=hoverboard+motor+6.5inch))
- Aluminium Strut Profiles and Connections ([link](https://www.boschrexroth.com/en/xc/products/product-groups/assembly-technology/topics/aluminum-profiles-solutions-components/aluminum-profiles-products/index))
