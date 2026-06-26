## Description: <br>
Creates, edits, evaluates, benchmarks, and optimizes agent skills using Opencode-based evaluation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pwu0125](https://clawhub.ai/user/pwu0125) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to draft new agent skills, improve existing skills, run evaluation loops, compare skill behavior, and package finished skills for release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit local skill files and create evaluation workspaces. <br>
Mitigation: Run it in a version-controlled workspace and review generated file changes before packaging or publishing. <br>
Risk: The skill invokes the Opencode executable for evaluation and description optimization workflows. <br>
Mitigation: Verify the Opencode path or OPENCODE_PATH value before use, and only run trusted executables. <br>
Risk: Evaluation prompts and skill files may contain sensitive or proprietary information. <br>
Mitigation: Do not include secrets or proprietary data in eval prompts, skill drafts, or generated review artifacts. <br>
Risk: The review viewer can start a local HTTP server. <br>
Mitigation: Prefer static viewer output or an unused local port, and stop the viewer after review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pwu0125/skill-creator-opencode) <br>
- [Publisher profile](https://clawhub.ai/user/pwu0125) <br>
- [Evaluation schema reference](references/schemas.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON files, shell commands, generated reports, and local workspace artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local skill files, evaluation workspaces, benchmark reports, static HTML review pages, and packaged skill artifacts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
