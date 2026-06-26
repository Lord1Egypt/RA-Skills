## Description: <br>
Guides agents through bundling React Native JavaScript for Android and iOS and publishing release or debug bundles to GitHub Releases with versioning and changelog steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvtong199881](https://clawhub.ai/user/lvtong199881) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to prepare React Native bundle artifacts, increment release or debug versions, and publish GitHub Releases for hot update delivery. It is intended for projects where commits, tags, pushes, and release asset uploads are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to run a mutable remote shell script with GitHub repository credentials and publish authority. <br>
Mitigation: Inspect and pin the publish.sh script before execution, then run it only from a clean branch where commits, tags, pushes, and GitHub Releases are intended. <br>
Risk: The workflow requires a GitHub token with repository release permissions. <br>
Mitigation: Use a fine-grained GitHub token limited to the intended repository and store it with restrictive local file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvtong199881/rn-bundle-to-github) <br>
- [publish.sh script referenced by the skill](https://raw.githubusercontent.com/lvtong199881/MyRNApp/refs/heads/main/publish.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets, release workflow steps, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that create or update project files, commits, tags, GitHub Releases, and uploaded bundle assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
