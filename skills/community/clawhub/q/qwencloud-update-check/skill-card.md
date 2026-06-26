## Description: <br>
Checks the qwencloud/qwencloud-ai skill pack for newer releases and reports whether an update is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents using qwencloud/qwencloud-ai skills use this skill to check installed version metadata, limit update checks, and surface update commands for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Update notices depend on a GitHub version check and may reflect a changed repository setting. <br>
Mitigation: Install only if you trust QwenCloud update notices and review QWEN_SKILLS_REPO before relying on the result. <br>
Risk: Printed npx skills add commands could install unintended skills if the lockfile or repository setting has been changed. <br>
Mitigation: Review the printed command and installed skill list before running it. <br>
Risk: The skill writes a persistent .agents/state.json timestamp and preference file. <br>
Mitigation: Expect that local state file and inspect or reset it when changing update-check preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cuixiaoyang123/qwencloud-update-check) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands, guidance] <br>
**Output Format:** [JSON response or stderr notice text with a proposed npx command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not run installs itself; writes a small local state file for timestamps and preferences.] <br>

## Skill Version(s): <br>
0.2.1 (source: evidence.release.version and artifact/version.json, released 2026-04-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
