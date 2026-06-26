## Description: <br>
Transform AI-generated content into natural, human-sounding writing, measure the improvement, and optionally verify the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nutstrut](https://clawhub.ai/user/nutstrut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to rewrite stiff or formulaic AI-assisted drafts into clearer, more natural prose while preserving meaning. It also produces before/after evaluation metrics and can optionally verify structured metrics without sending original or rewritten text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional verification could expose sensitive content if raw original or rewritten text is sent outside the local workflow. <br>
Mitigation: Use verification only for structured metrics such as counts, deltas, boolean checks, and receipt status; keep original and rewritten text local. <br>
Risk: A style rewrite could be mistaken for proof of human authorship, AI detection, or an undetectable-content claim. <br>
Mitigation: Present the result as a writing transformation with measurable changes, not as proof of authorship or detector bypass. <br>
Risk: Rewriting may change the user's intended voice or introduce unsupported facts. <br>
Mitigation: Review the output against the checklist for meaning preservation, tone match, and absence of false facts before returning it. <br>
Risk: The packaged metadata version differs from the registry release metadata. <br>
Mitigation: Use the server-resolved release version for the public card and verify publisher and version before installation. <br>
Risk: The OpenClaw hook changes session behavior by adding a bootstrap reminder. <br>
Mitigation: Review the hook before enabling it and confirm that its reminder matches the intended local, privacy-focused workflow. <br>


## Reference(s): <br>
- [Verified Humanizer release page](https://clawhub.ai/nutstrut/verified-humanizer) <br>
- [Publisher profile](https://clawhub.ai/user/nutstrut) <br>
- [Verified Humanizer examples](references/examples.md) <br>
- [OpenClaw integration notes](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [JSON and Markdown guidance with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces rewritten text, a change summary, before/after evaluation metrics, and optional verification status.] <br>

## Skill Version(s): <br>
0.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
