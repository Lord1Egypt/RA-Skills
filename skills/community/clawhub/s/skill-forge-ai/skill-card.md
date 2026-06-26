## Description: <br>
Skill Forge guides agents through creating, evaluating, and publishing ClawHub skills with trigger-based phases for interviews, validation, benchmarking, and GitHub or ClawHub release steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to turn a skill idea or existing skill into a structured ClawHub release, including requirements interviews, validation checks, peer benchmarking, and publishing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes publishing workflows that can push content to GitHub and ClawHub. <br>
Mitigation: Require the agent to show the exact repository, slug, version, and file list for approval before any push or publish command. <br>
Risk: The security evidence flags unsafe credential-reuse guidance and token-extraction content. <br>
Mitigation: Remove or ignore token-extraction guidance and use gh or credential-helper authentication only. <br>
Risk: The security verdict is suspicious because remote publishing steps need clearer user control. <br>
Mitigation: Review and scan the skill before deployment, and execute publishing only after explicit user confirmation. <br>


## Reference(s): <br>
- [Interview Flow Reference](references/interview-flow.md) <br>
- [Interview Methods Reference](references/interview-methods.md) <br>
- [SkillHub Peer Benchmarking Guide](references/benchmarking-guide.md) <br>
- [Publishing Guide](references/publishing-guide.md) <br>
- [Meeting Action Extractor Example](references/meeting-action-extractor-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated skill files, review checklists, benchmark comparisons, and publish commands for user approval.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release and CHANGELOG, released 2026-06-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
