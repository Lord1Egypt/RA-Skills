## Description: <br>
Quick macOS display snapshot that captures the current screen without opening a browser and saves it to /tmp or a custom path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrentheai](https://clawhub.ai/user/wrentheai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Screengrab to capture the visible state of a macOS desktop for visual debugging, app state checks, output verification, and remote awareness without launching a browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots can capture anything visible on the user's Mac screen, including sensitive windows or data. <br>
Mitigation: Close or hide sensitive windows before capture, prefer targeting a specific display when possible, limit watch mode with --count, and delete saved screenshots from /tmp or custom output folders when no longer needed. <br>


## Reference(s): <br>
- [Screengrab on ClawHub](https://clawhub.ai/wrentheai/screengrab) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and local PNG screenshot file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG screenshots on macOS, usually under /tmp unless a custom path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
