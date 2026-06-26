## Description: <br>
Turn a user goal into the best skill stack. Recommends, compares, and sequences the right skills, with explicit user approval before any install guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, AI beginners, and teams use this skill to translate a goal into a small, practical stack of ClawHub skills. It helps compare candidate skills, explain tradeoffs and trust signals, and gate install guidance behind explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend downstream skills that run code, ask for credentials, modify files, or connect to accounts. <br>
Mitigation: Review and scan each recommended downstream skill separately before installation or use, and require explicit user approval before showing install guidance. <br>
Risk: Poorly matched or low-signal recommendations could lead to unnecessary setup work or misleading workflow choices. <br>
Mitigation: Compare candidates against the user's goal, trust signals, setup cost, and alternatives before adopting a stack. <br>


## Reference(s): <br>
- [Smart Skill Advisor on ClawHub](https://clawhub.ai/ToBeWin/smart-skill-advisor) <br>
- [README](artifact/README.md) <br>
- [Release Notes v2.0.0](artifact/RELEASE_V2.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown recommendation with an execution plan, alternatives considered, tradeoffs, and install guidance only after explicit approval.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downstream skill recommendations should be reviewed separately before installation, especially when a recommended skill runs code, asks for credentials, modifies files, or connects to accounts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
