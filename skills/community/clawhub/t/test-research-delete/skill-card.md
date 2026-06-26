## Description: <br>
Orchestrate parallel codebase research. Spawns multiple researcher subagents to investigate different areas, then synthesizes findings into research.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flip-in](https://clawhub.ai/user/flip-in) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate a codebase by decomposing a research question into parallel investigation areas and synthesizing findings into a research.md report. It is intended for technical mapping of existing code, including file:line references and open questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository content and can include sensitive code details or repository metadata in research.md. <br>
Mitigation: Run it only on codebases intended for review, inspect the generated report before sharing it, and make sure repository remote URLs do not contain credentials. <br>
Risk: The skill writes research.md in the current directory and may replace an existing local report. <br>
Mitigation: Check for an existing research.md before running the skill, or run it in a clean working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flip-in/test-research-delete) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report plus brief text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes research.md in the current directory; the report includes file:line references, git metadata, findings, architecture notes, and open questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
