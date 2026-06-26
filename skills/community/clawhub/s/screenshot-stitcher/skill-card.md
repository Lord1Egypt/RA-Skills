## Description: <br>
Use when the task is to stitch multiple vertically scrolling iPhone screenshots into a single long image with the local screenshot-stitcher CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mate-matt](https://clawhub.ai/user/mate-matt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to combine ordered, same-width vertically scrolling iPhone screenshots into one long local image and to choose crop or edge-margin flags when the default CLI command is not enough. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running a third-party Python package can execute code in the user's Python environment. <br>
Mitigation: Install only in a trusted or isolated Python environment, preferably a virtual environment. <br>
Risk: The fallback `python3 main.py` path can run untrusted source code if used from an unknown checkout. <br>
Mitigation: Use the fallback only from a checkout the user trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mate-matt/screenshot-stitcher) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the stitched output path and any low-confidence overlap warnings produced by the CLI.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
