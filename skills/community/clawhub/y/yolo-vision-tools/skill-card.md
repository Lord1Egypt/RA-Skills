## Description: <br>
Use Ultralytics YOLO to perform computer vision tasks, such as detecting people or objects in images and videos, classifying images, estimating human poses, and tracking cars, people, or animals in videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ruoyu05](https://clawhub.ai/user/Ruoyu05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose, configure, run, troubleshoot, and train Ultralytics YOLO models for image and video analysis tasks including detection, segmentation, classification, pose estimation, and object tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model and package setup can download dependencies or model files. <br>
Mitigation: Install in a virtual environment and use preloaded local models when downloads are not intended. <br>
Risk: Image, video, webcam, dataset, and generated output files may contain sensitive content and can be saved locally. <br>
Mitigation: Avoid private media unless local copies and generated outputs are acceptable; set an explicit output directory and review saved files. <br>
Risk: Environment diagnostics can expose local paths, hardware details, and package information. <br>
Mitigation: Redact environment reports before sharing them outside the local workspace. <br>
Risk: Cache cleanup or dataset upload actions can change local state or move data when used unintentionally. <br>
Mitigation: Run cleanup or upload options only after confirming that the operation is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ruoyu05/yolo-vision-tools) <br>
- [Ultralytics Documentation](https://docs.ultralytics.com) <br>
- [Ultralytics Configuration Reference](https://docs.ultralytics.com/usage/cfg/) <br>
- [YOLO Configuration Examples](references/configuration_samples.md) <br>
- [YOLO Dataset Preparation Guide](references/dataset_preparation.md) <br>
- [Ultralytics YOLO Environment Check Guide](references/environment_check.md) <br>
- [Ultralytics YOLO Installation Guide](references/installation_guide.md) <br>
- [YOLO Model Names Reference](references/model_names.md) <br>
- [YOLO Model Selection Guide](references/model_selection.md) <br>
- [YOLO Parameter Reference](references/parameter_reference.md) <br>
- [YOLO Task Types Explained](references/task_types.md) <br>
- [YOLO Model Training Guide](references/training_basics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file outputs under a yolo-vision workspace folder and local model/cache operations.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
