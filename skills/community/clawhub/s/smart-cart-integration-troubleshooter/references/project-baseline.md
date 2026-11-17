# Project baseline

Use this file as the authoritative baseline for the intelligent mobile cart project. Do not infer missing pinouts, ports, protocols, or performance values.

## Project goal

Build a lightweight, low-cost indoor cart that closes the loop from natural-language instruction to large-model planning and hardware execution. Support text or voice control, fixed-point movement, steady movement, obstacle avoidance, in-place turning, emergency stop, and basic path adjustment.

## Hardware baseline

| Component | Project specification | Role |
| --- | --- | --- |
| Cart body | Custom structural assembly | Main frame |
| Battery | 12V, 5100mAh lithium battery | Whole-system power |
| Charger | Compatible with 12V battery | Charging |
| Servo controller | Multi-channel | Receive commands and control servos |
| USB camera | 1080P | Visual environment sensing |
| Chassis print | PLA, about 270g | Chassis structure |
| Chassis servos | ST3215, 12V, three units | Drive omnidirectional wheels |
| Flange shafts | Three units | Connect servos and wheels |
| Omnidirectional wheels | 85mm with 6mm coupler, three sets | Forward, lateral, and turning motion |
| Fasteners | M3 screws and nuts | Hardware fixation |

The project estimate states that the body and chassis kit costs about CNY 1,280 and the MiniMax API debugging allowance is about CNY 100. These are planning estimates, not measured performance data.

## Software baseline

- Python runtime on a control computer or development board.
- OpenClaw agent framework.
- MiniMax large-model API for instruction parsing and behavior planning.
- USB camera driver and video acquisition.
- Communication between the agent and servo controller.
- A simple visual interface for command input and state display.

## Integration order

1. Assemble the 3D-printed chassis, servos, shafts, couplers, and omnidirectional wheels.
2. Install the cart body, battery, controller, and camera; verify stable 12V power.
3. Calibrate the zero position and direction of all three servos; verify basic movement.
4. Deploy Python, OpenClaw, the model API, and camera driver; test video and command communication.
5. Connect agent commands to the controller, add camera input, test path adjustment, and tune latency and stability.

## Known unknowns

The project document does not specify the servo-controller protocol, serial-port name, baud rate, pin mapping, camera device index, obstacle-detection algorithm, map format, or exact motion-to-wheel equations. Ask for these values when they are necessary; never invent them.

