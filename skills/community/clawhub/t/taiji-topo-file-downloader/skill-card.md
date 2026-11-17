## Description:

在太极平台 a.taiji.woa.com 工作流页面自动定位节点侧边栏、打开配置文件面板并下载文件。用于“下载太极拓扑配置文件/模型文件”“在太极页面里找到文件并保存到本地”等任务，特别适合需要先校验页面是否已正确打开、再稳定定位侧边栏与文件列表的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-final](https://clawhub.ai/user/m-final)

### License/Terms of Use:

MIT

## Use Case:

Developers and workflow operators use this skill to guide browser automation that opens Taiji workflow file panels, downloads selected topology or model files, and saves them to a timestamped local directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local shell step can mishandle or overwrite files in the user's Downloads directory.

Mitigation: Use a unique fixed download directory, confirm the selected file before moving it, and require confirmation before overwriting local files.

Risk: Filename or topology-name inputs can affect local paths.

Mitigation: Reject path separators in filenames and sanitize directory names before creating folders or moving files.

Risk: The shell snippet uses eval to expand the base download path.

Mitigation: Replace eval-based path expansion with a fixed, explicit download directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m-final/skills/taiji-topo-file-downloader)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation steps and local file-handling commands for the agent to execute or adapt.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
