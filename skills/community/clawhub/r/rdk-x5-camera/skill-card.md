## Description: <br>
配置并启动 RDK X5 上的 MIPI CSI 摄像头、USB 摄像头或双目深度摄像头（RealSense/ZED/Orbbec），通过 Web 浏览器预览实时画面。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure MIPI CSI, USB UVC, or depth cameras on RDK X5 hardware, preview live video in a browser, capture images, and troubleshoot common camera connection issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes package-install and sudo ISP tuning steps that can change the device environment. <br>
Mitigation: Review package installs before accepting them and run the sudo tuning step only when the local tuning tool contents are trusted. <br>
Risk: Browser preview can expose live camera video over the network. <br>
Mitigation: Use the preview only on a trusted network and verify the target RDK X5 address before connecting. <br>
Risk: MIPI camera hardware can be damaged by hot-plugging. <br>
Mitigation: Power off the RDK X5 before connecting or reseating MIPI camera ribbon cables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/rdk-x5-camera) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is specific to RDK X5 camera setup and ROS 2 camera launch workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
