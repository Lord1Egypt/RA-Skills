## Description: <br>
This skill helps agents perform web UI automation tests by running browser actions, capturing screenshots at each step, recording a session, and producing replayable scripts plus a standalone HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[94lfj](https://clawhub.ai/user/94lfj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and agents use this skill to turn natural-language web testing requests into executed browser test steps, recorded sessions, replayable shell or JSON scripts, and screenshot-backed HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save browser screenshots, typed values, URLs, selectors, commands, and errors to disk. <br>
Mitigation: Use staging sites and test accounts when possible, keep generated sessions and reports private, and avoid recording sensitive production data. <br>
Risk: The skill generates replayable shell and batch files from recorded browser commands. <br>
Mitigation: Inspect generated .sh and .bat files before running them and execute them only in an appropriate test environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/94lfj/ui-test-agent) <br>
- [Publisher profile](https://clawhub.ai/user/94lfj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON session data, replay scripts, and standalone HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may embed screenshots and recorded browser evidence; replay files may include executable shell or batch commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
