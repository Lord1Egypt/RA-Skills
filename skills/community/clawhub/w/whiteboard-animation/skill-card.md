## Description: <br>
Generates whiteboard-style hand-drawing animation videos from image files, converting color images into line-drawing and coloring phases with optional hand overlay and H.264 MP4 output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangagent](https://clawhub.ai/user/yangagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn one or more local image files into whiteboard animation videos, choosing duration, output directory, and whether to include the hand overlay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local setup can create a .venv and download Python packages from PyPI. <br>
Mitigation: Run the setup only in environments where local virtualenv creation and PyPI downloads are acceptable; pin or pre-review dependencies in stricter environments. <br>
Risk: Default hand-overlay generation may fail because drawing-hand.png is not included in the artifact. <br>
Mitigation: Supply the missing hand asset before using the overlay, or run generation with --no-hand. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangagent/whiteboard-animation) <br>
- [YangAgent publisher profile](https://clawhub.ai/user/yangagent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated MP4 file paths or batch summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local H.264 MP4 videos in the selected output directory; batch mode reports success and failure counts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
