## Description:

Ruankao SPGM QA helps candidates for the Advanced System Planning and Management Engineer exam answer policy, concept, past-paper, preparation, and IT service management questions with source-aware Markdown guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and exam-prep assistants use this skill to classify System Planning and Management Engineer questions, retrieve or apply relevant reference material, and produce concise Markdown answers with source notes and policy caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Every answer is directed to include publisher branding and WeChat contact promotion.

Mitigation: Review this behavior before installation and remove or constrain promotional wording if it is not acceptable for the deployment context.

Risk: IMA lookup may send the current exam question to an external knowledge-base workflow.

Mitigation: Require explicit user authorization before lookup and avoid submitting sensitive personal information or private exam-prep notes.

Risk: Exam policies and preparation guidance can become outdated or be mistaken for official answers.

Mitigation: Keep the skill's official-announcement caveats in responses and verify policy claims against current official notices before relying on them.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/chesaram/skills/ruankao-spgm-qa-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/chesaram)
- [README](artifact/README.md)
- [Q&A routing guide](artifact/references/qa_routing.md)
- [IMA knowledge-base guide](artifact/references/ima_kb_guide.md)
- [SPGM terminology guide](artifact/references/spgm_terminology.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown Q&A with a direct conclusion, bullet-point explanation, source notes, policy or boundary caveats, signature, and disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use external IMA knowledge-base lookup when the user authorizes searching; every answer is directed to include publisher signature and contact promotion.]

## Skill Version(s):

1.0.0 (source: manifest.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
