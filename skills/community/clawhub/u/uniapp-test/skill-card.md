## Description: <br>
Guides agents through analyzing uni-app or uni-app x pages, creating or updating corresponding *.test.js cases, running platform test commands, and iterating on failures until tests pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengzy321](https://clawhub.ai/user/dengzy321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to add or improve automated tests for uni-app and uni-app x pages, then run the appropriate Web, mobile, or mini-program test command and fix failing cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide file edits and test command execution in a user's uni-app project. <br>
Mitigation: Use it in trusted project folders, review diffs before keeping changes, and confirm the exact npm command before running browser, emulator, or device tests. <br>
Risk: Generated tests may be brittle if the target page lacks stable selectors or if device and simulator prerequisites are unavailable. <br>
Mitigation: Prefer data-testid or semantic class selectors, verify connected devices before mobile test runs, and rerun only the targeted test file after fixes. <br>


## Reference(s): <br>
- [uni-app automated testing API](https://uniapp.dcloud.net.cn/worktile/auto/api.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown guidance with JavaScript test code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update page-adjacent *.test.js files and propose targeted page changes when test failures indicate application bugs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
