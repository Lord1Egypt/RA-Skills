## Description: <br>
User-invoked reflection for recording approved project learnings, generating evidence-based engineering retrospectives, and codifying recurring patterns into reusable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkenny0](https://clawhub.ai/user/kkenny0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Taku Reflect to preserve user-approved project lessons, search, prune, and export those lessons, generate weekly retrospectives from git evidence, and turn recurring practices into reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved learnings or retrospectives could include secrets or sensitive personal data if a user approves that content. <br>
Mitigation: Review proposed entries before saving and avoid storing secrets or sensitive personal data in learnings. <br>
Risk: Bootstrap changes to AGENTS.md or CLAUDE.md can affect how future agents consult local learnings. <br>
Mitigation: Only approve bootstrap changes when future agents should consult the project-local learnings file. <br>
Risk: Incorrect or low-quality learnings could mislead later planning or review work. <br>
Mitigation: Use the skill's review, confidence, search, and prune flows to keep only useful user-approved entries. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kkenny0/taku-reflect) <br>
- [Retrospective Report Scaffold](references/retro-report.md) <br>
- [Taku Write Skill - TDD for Documentation](references/writing-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSONL records, shell commands, and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are project-local and require user approval before learnings, bootstrap changes, or skill-writing changes are saved.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
