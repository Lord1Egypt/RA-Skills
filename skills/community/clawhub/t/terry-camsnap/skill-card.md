## Description: <br>
Take camera snapshots and save them to disk. Use when the user asks to take a photo, capture an image from webcam, or take a snapshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to capture a snapshot from the default webcam, optionally choosing an output path or preview mode, and receive confirmation of the saved file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses a webcam and can leave captured images on disk. <br>
Mitigation: Install and run it only where camera access and local image storage are appropriate; review saved paths and delete sensitive captures when no longer needed. <br>
Risk: The artifact invokes a local camsnap.py script that is not included, so users cannot inspect the camera-capture implementation from this release alone. <br>
Mitigation: Use the skill only in environments where the local camsnap.py script can be inspected or is already trusted before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, files] <br>
**Output Format:** [Plain text status confirmation with a saved image file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save an image file to disk; optional output path, output directory, and preview flags are accepted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
