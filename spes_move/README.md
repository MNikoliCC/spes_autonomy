# Move

> Based on [`mep3_navigation::MoveBehavior`](https://github.com/memristor/mep3/edit/main/mep3_navigation/src/move_behavior/README.md).

Local navigation. Low-level mobile robot motion package for short distances (e.g. up to 1m). Designed for applications such as visual positioning, docking, inplace rotation, and odometry calibration.

Main features:
- **Accurate position control.** Implements the distance-angle controller.
- **Motion generation.** Limits velocity, acceleration, and jerk.
- **Frame transformations.** Receives (x,y,yaw) in a target frame and regulates position in the odom frame.
- **Position based servoing.** Accepts continuous position commands.
- **Latency compensation.** Utilizes odometry + TF buffer to compensate for the latency. 
- **Debouncing.** Regulates position until the robot completely stops.
- **Obstacle detection (WIP).** Integrates Nav2 costmaps to detect obstacles on a simulated path.
- **Stuck detection. (WIP)** Implements a robust stuck detection algorithm.

Published topics:
- `cmd_vel` (geometry_msgs/msg/Twist): velocity commands.
- `~/state` (spes_msgs/msg/MoveState): move status.

Subscribed topics:
- `~/command` (spes_msgs/msg/MoveCommand): position commands.
- `/tf` (tf2_msgs/msg/TFMessage): TF2 transforms.
- `/costmap` (optional, nav2_msgs/msg/Costmap): costmap updates (WIP).

Action servers:
- `~/move` (spes_msgs/action/Move): move to the target pose (WIP).

## Frames

There are four important frames:
- We defined an objective as a `target` frame (2D pose) in the `global` frame.
- The robot (`base` frame) finds the target in the `odom` frame and continues motion in the `odom` frame.

Therefore, there are two stages:
- Once the command is received we calculate the `target` pose in the `odom` frame: $$ T_{odom}^{target} = (T_{global}^{odom})^{-1} * T_{global}^{target} $$
- In the control loop we regulate the position according to the error: $$ T_{base}^{target} = (T_{odom}^{base})^{-1} * T_{odom}^{target} $$

In the typical example `global` = `map` and `odom` = `odom`.
It means the robot moves to the absolute pose, but it uses the `odom` frame to avoid discrete pose jumps.

However, `global` + `odom` frames gives us a flexibility to achieve useful behaviors:
- If `global` = `base_link` and `odom` = `odom` then the robot moves relative to its current pose.
- If `global` = `marker_1` (a fiducial marker) and `odom` = `marker_1` then the robot moves to the marker pose (e.g. to pick the object). 
- However, if the robot loses the `marker_1` from its sight then we can set the following `global` = `marker_1` and `odom` = `odom`.

## Configuration

Find a configuration example below:
```yaml
move:
    ros__parameters:
        update_rate: 50
        command_timeout: 0.5

        # Can be overridden by the command.
        linear:
            kp: 0.5
            kd: 0.0
            max_velocity: 0.5
            max_acceleration: 0.5
            tolerance: 0.1
        angular:
            kp: 0.5
            kd: 0.0
            max_velocity: 0.5
            max_acceleration: 0.5
            tolerance: 0.1
```

## Command Examples

Some ideas on how to utilize the move behavior.

> Make sure to the `move` as `ros2 run spes_move move` before executing the examples.`;

Move 20cm forward and stop:
```bash
ros2 topic pub -1 move/command spes_msgs/msg/MoveCommand '{ "header": { "frame_id": "base_link" }, "odom_frame": "odom", "target": { "x": 0.2 }, "rotate_towards_goal": false, "rotate_at_goal": false }'
```

Keep moving forward until canceled:
```bash
ros2 topic pub -r1 move/command spes_msgs/msg/MoveCommand '{ "header": { "frame_id": "base_link" }, "odom_frame": "odom", "target": { "x": 0.5 }, "rotate_towards_goal": false, "rotate_at_goal": false }'
```

Rotate in place for 90 degrees:
```bash
ros2 topic pub -1 move/command spes_msgs/msg/MoveCommand '{ "header": { "frame_id": "base_link" }, "odom_frame": "odom", "target": { "theta": 1.507 }, "rotate_towards_goal": false, "translate": false }'
```

Move to pose (-0.5, -0.5):
```bash
ros2 topic pub -1 move/command spes_msgs/msg/MoveCommand '{ "header": {"frame_id": "odom" }, "odom_frame": "odom", "target": { "x": -0.5, "y": -0.5 } }'
```

## Usage Examples

Follow a red ball with 300ms+ latency:
```bash
ros2 launch spesbot_webots test_latency_compensation_launch.py
```