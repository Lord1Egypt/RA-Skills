## Description: <br>
Score startup idea through S.E.E.D. niche check + STREAM 6-layer analysis + Devil's Advocate inversion, auto-pick stack, and generate PRD with acceptance criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, founders, and product builders use this skill to evaluate startup ideas, identify kill signals, choose an implementation stack, and generate a PRD with measurable acceptance criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write or replace docs/prd.md while generating a PRD. <br>
Mitigation: Run it only in the intended project workspace and confirm before any file write, especially before creating or replacing docs/prd.md. <br>
Risk: The skill requests broad shell access and may propose commands during validation or stack selection. <br>
Mitigation: Review each shell command before execution and decline commands that are unnecessary for the validation task. <br>
Risk: The skill can use web search, which may disclose sensitive product names or idea details. <br>
Mitigation: Avoid submitting confidential product names or sensitive idea details to web searches unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fortunto2/solo-validate) <br>
- [Manifest Alignment Checklist](references/manifest-checklist.md) <br>
- [STREAM 6-Layer Framework](references/stream-layers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Configuration guidance] <br>
**Output Format:** [Markdown summary and a generated PRD file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local knowledge, web search, and optional MCP search tools when available.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
