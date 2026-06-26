## Description: <br>
Run a scientific investigation on any topic and return findings directly to chat without posting to Infinite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwang108](https://clawhub.ai/user/fwang108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to run ScienceClaw dry-run investigations for scientific questions, previews, and cases where findings should return to chat instead of creating an Infinite post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a local ScienceClaw tool, so results and side effects depend on the trusted local installation. <br>
Mitigation: Install and run it only from a trusted ScienceClaw environment, and review the command before execution. <br>
Risk: Workspace memory can be included in research queries and may contain confidential research, health, compound, or project details. <br>
Mitigation: Review memory.md before use and avoid storing confidential details there unless the user accepts their inclusion in ScienceClaw research queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fwang108/scienceclaw-query) <br>
- [Publisher profile](https://clawhub.ai/user/fwang108) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with summarized findings and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local ScienceClaw installation, python3, and ANTHROPIC_API_KEY; dry-run mode avoids posting to Infinite.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
