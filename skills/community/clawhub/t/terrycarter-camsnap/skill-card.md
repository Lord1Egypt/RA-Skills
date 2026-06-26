## Description: <br>
Take camera snapshots and save them to disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent capture an image from the default webcam and return the saved file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses the default webcam and saves photos locally. <br>
Mitigation: Install and run it only when webcam capture is intended, and review where output files are written. <br>
Risk: The command template may allow specially crafted filenames to trigger unintended shell behavior. <br>
Mitigation: Use simple output paths without shell metacharacters until command invocation is hardened. <br>
Risk: The Python utility depends on OpenCV for camera access and image writing. <br>
Mitigation: Install OpenCV only from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/terrycarter1985/terrycarter-camsnap) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell command and saved image file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local image file in a user-provided path or the snapshots directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
