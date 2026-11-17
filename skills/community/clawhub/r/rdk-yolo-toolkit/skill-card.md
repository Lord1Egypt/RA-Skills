## Description:

Guides agents through end-to-end YOLO training, ONNX export, hb_mapper quantization, RDK X5 BPU deployment, hbm_runtime inference, and optional TROS HobotDnn ROS2 detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxma615](https://clawhub.ai/user/maxma615)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics or edge-AI engineers use this skill to move YOLO models from training through quantization and deployment on D-Robotics RDK X5 boards. It supports board validation, runtime inference checks, and ROS2 integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run broad local and SSH commands on training machines and RDK X5 boards.

Mitigation: Use command-list or manual mode when possible, review every ssh, scp, nohup, tmux, installer, and training command before execution, and run with least-privilege accounts.

Risk: Detached camera, inference, or ROS2 jobs may keep running after the interactive session ends.

Mitigation: Require visible logs, process IDs, and explicit stop commands for nohup or tmux jobs before treating deployment validation as complete.

Risk: Installer guidance uses network downloads and package installation paths that may change or pull unverified artifacts.

Mitigation: Pin package versions, verify hashes where available, and install in an isolated conda or equivalent environment before using the toolchain on shared machines.

Risk: Device-permission shortcuts and root board access can weaken the RDK X5 runtime environment.

Mitigation: Avoid root unless required and replace broad device permissions such as chmod 666 with a dedicated group or udev rule.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/maxma615/skills/rdk-yolo-toolkit)
- [D-Robotics YOLO ROS documentation](https://developer.d-robotics.cc/rdk_doc/Robot_development/boxs/detection/yolo)
- [D-Robotics RDK X5 toolchain manual](https://developer.d-robotics.cc/api/v1/fileData/x5_doc-v126cn/index.html)
- [RDK X5 hbm_runtime Python API](https://developer.d-robotics.cc/rdk_x_doc/Basic_Application/multi_media_sp_dev_api/RDK_X5/pydev_multimedia_api_x5/ai-python-api)
- [D-Robotics rdk_model_zoo ultralytics_yolo sample](https://github.com/D-Robotics/rdk_model_zoo/tree/rdk_x5/samples/vision/ultralytics_yolo)
- [D-Robotics rdk_model_zoo ultralytics_yolo26 sample](https://github.com/D-Robotics/rdk_model_zoo/tree/rdk_x5/samples/vision/ultralytics_yolo26)
- [HobotDnn CHANGELOG](https://github.com/D-Robotics/hobot_dnn/blob/develop/dnn_node/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational Markdown with inline bash, YAML, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local or SSH execution workflows and generated configuration files for RDK X5 deployment.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
