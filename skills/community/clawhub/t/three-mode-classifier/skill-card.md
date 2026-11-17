## Description:

判断产业 Web3 项目属于原生型、产业变革型或链改-资产支持型，并给出模式选型、组织形态和合规路径提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[63619990](https://clawhub.ai/user/63619990)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users, consultants, investors, entrepreneurs, and project teams use this skill to classify a Web3 industrial project by organization-change depth and financing orientation before choosing an implementation path. It is especially relevant when a user is deciding whether a project is native Web3, industrial transformation, or asset-backed chain transformation.

### Deployment Geography for Use:

Global; guidance includes China-specific legal and compliance framing.

## Known Risks and Mitigations:

Risk: Users may treat Web3 financing, RWA, or legal boundary guidance as legal, investment, or compliance advice.

Mitigation: Present conclusions as risk-identification guidance and direct users to qualified legal, compliance, or investment professionals before acting.

Risk: A project may be misclassified if the asset, organization-change depth, or financing orientation is unclear.

Mitigation: Ask the skill's three positioning questions before classifying: what asset is anchored, whether the organization or collaboration model changes, and whether the project has a financing orientation.

Risk: A chain-transformation or asset-backed project aimed at mainland China issuance may cross tokenized financing boundaries.

Mitigation: Stop short of designing domestic token issuance and route the user to compliance review and the appropriate RWA implementation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/63619990/skills/three-mode-classifier)
- [Skill source](artifact/SKILL.md)
- [Pressure test results](artifact/test-results.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with classification results, path recommendations, organization notes, and compliance caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advice-only output; no code execution, persistence, data access, or hidden authority.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
