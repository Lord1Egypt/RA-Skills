## Description: <br>
ROS 2 专家助手，提供工程开发辅助、架构分析、学习教学、环境配置、项目实战引导五大能力；当用户需要开发 ROS 2 应用、分析工程代码、学习 ROS 2 知识、安装配置环境或通过项目实战学习时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessy-huang](https://clawhub.ai/user/jessy-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, robotics engineers, and learners use this skill to build and analyze ROS 2 Humble applications, understand ROS 2 concepts, configure environments, troubleshoot issues, and plan guided practice projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest one-line installer and package-manager commands that change system sources or packages. <br>
Mitigation: Review commands before execution, prefer verified HTTPS sources, inspect installer scripts first, and use a VM or container when possible. <br>
Risk: Troubleshooting workflows may involve logs or robotics data that contain sensitive locations, maps, voice data, or credentials. <br>
Mitigation: Redact logs and data before sharing them with external AI services, and avoid sending API keys or other secrets. <br>
Risk: APT source changes or lock-file deletion can disrupt a host system when package-manager operations are already running. <br>
Mitigation: Back up APT configuration before changing sources and confirm no package process is active before touching package-manager locks. <br>


## Reference(s): <br>
- [ROS 2 Humble documentation](http://fishros.org/doc/ros2/humble/) <br>
- [FishROS one-click installer documentation](https://fishros.org.cn/forum/topic/20/) <br>
- [ROS 2 core concepts reference](references/ros2-core-concepts.md) <br>
- [ROS 2 development best practices](references/best-practices.md) <br>
- [ROS 2 installation guide](references/installation-guide.md) <br>
- [ROS 2 project analysis guide](references/project-analysis-guide.md) <br>
- [ROS 2 practical tasks reference](references/practical-tasks.md) <br>
- [ros2_control documentation](https://control.ros.org/master/index.html) <br>
- [MoveIt 2 tutorials](https://moveit.picknik.ai/main/doc/tutorials/tutorials.html) <br>
- [Vosk speech recognition](https://alphacephei.com/vosk/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ROS 2 Python or C++ snippets, package commands, environment checks, troubleshooting steps, architecture summaries, and learning plans.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence, created 2026-04-02T03:44:16Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
