## Description:

Zh Semantic Enhancer enriches Chinese-language user input with tokenization, entity detection, idiom and slang recognition, cultural context cues, ambiguity handling, and structured intent output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxcg](https://clawhub.ai/user/andyxcg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to prepare Chinese-language requests for downstream agent workflows by producing normalized text, semantic annotations, confidence scores, and suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled monetization and self-rewriting utilities can alter installed skill code if run.

Mitigation: Review the bundled monetization scripts before installation and avoid running scripts/revenue_optimize.py unless code rewriting is intentional.

Risk: The skill stores local trial and credit state under the user's home directory.

Mitigation: Remove or fix the local persistence code before use in shared or production environments, and avoid using sensitive user identifiers.

Risk: Promotional pricing copy is stale because the advertised offer ended on 2026-03-31.

Mitigation: Update or remove expired pricing and trial claims before presenting the skill to users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andyxcg/skills/zh-semantic-enhancer)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes normalized text, tokens, entities, expression matches, domain classification, confidence, and suggested actions.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact files contain conflicting 1.3.0, 1.1.0, and 1.0.0 version strings)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
