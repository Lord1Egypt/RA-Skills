## Description: <br>
Tvs Inksnow Arch guides developers through a Chinese-language architecture refactor workflow that produces an approval-gated RFC and then creates Cursor rules for the approved architecture boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when they need to turn architecture refactor ideas into a concrete RFC and persist the approved decisions as Cursor rule files for future AI-assisted coding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent Cursor rule files that influence later AI edits in the repository. <br>
Mitigation: Review the generated RFC and planned .cursor/rules files carefully before approving the rule-generation stage. <br>
Risk: Architecture guidance may be incomplete if the optional deep interview skill is unavailable and the simplified protocol is used. <br>
Mitigation: Use the approval gate to review the RFC for missing constraints, topology decisions, and rollout risks before allowing rule files to be generated. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/inksnowhailong/tvs-inksnow-arch) <br>
- [Publisher profile](https://clawhub.ai/user/inksnowhailong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown RFC content and Cursor .mdc rule-file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow gates rule-file generation on explicit user approval of the generated RFC.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
