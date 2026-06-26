## Description: <br>
A personal diary automation skill for OpenClaw that detects configuration, initializes local paths, writes daily journal entries from local SOUL and memory files, and generates 1080px-wide diary images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1204TMax](https://clawhub.ai/user/1204TMax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to automate a personal daily journal workflow from local persona and memory files, then render the resulting entry as text and a shareable image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads personal SOUL, MEMORY, daily memory, and optional news-summary files from configured local paths. <br>
Mitigation: Review or create config.yaml before use and point it only at files appropriate for diary generation. <br>
Risk: Generated diary text and images may contain private personal details. <br>
Mitigation: Keep the diary output directory private and exclude config.yaml and generated diary files from version control. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown diary text, HTML render file, and PNG image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured local paths; image output defaults to 1080px width.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
