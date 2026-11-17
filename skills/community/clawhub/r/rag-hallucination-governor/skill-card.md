## Description:

Provides Chinese-language RAG hallucination troubleshooting guidance from current metrics, symptoms, or retrieval log excerpts, producing root-cause diagnosis, threshold tuning advice, and governance recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

Delivery teams, product managers, and RAG system engineers use this skill to classify hallucination symptoms, diagnose retrieval and knowledge-base causes, tune thresholds, and plan practical governance steps for production RAG systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieval logs may contain private customer or business data.

Mitigation: Redact sensitive identifiers and confidential content before sharing logs with the skill.

Risk: Operational tuning advice may be inappropriate for a specific production system without validation.

Mitigation: Test threshold, retrieval, and routing changes in a staging or replay environment before production rollout.

Risk: The skill can classify symptoms without logs, but root-cause analysis may be incomplete when evidence is missing.

Mitigation: Provide representative metrics or retrieval-log excerpts when asking for diagnosis, and treat unsupported conclusions as hypotheses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william202404/skills/rag-hallucination-governor)
- [Server-resolved GitHub source](https://github.com/william202404/tob-skills/tree/main/rag-hallucination-governor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic report with tables and prioritized repair steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language operational guidance; does not install code, change systems, or handle credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
