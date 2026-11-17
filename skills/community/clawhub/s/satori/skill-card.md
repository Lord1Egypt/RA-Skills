## Description:

Satori provides persistent long-term memory for continuity across AI sessions, providers, and code generation tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelachance](https://clawhub.ai/user/joelachance)

### License/Terms of Use:


## Use Case:

Developers and AI-tool users use Satori to save notable decisions, preferences, deadlines, project context, and other durable facts, then retrieve that context in later sessions. The skill guides agents on when to call the Satori CLI to add or search memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation details, including business or personal context, may be saved to an external memory service without visible confirmation.

Mitigation: Require explicit opt-in before saving, show the exact facts to be stored, and block sensitive data by default.

Risk: Retrieved memories may be incorporated silently, making it hard for users to know when prior context affected an answer.

Mitigation: Disclose retrieval when remembered context materially affects a response and let users inspect the retrieved facts.

Risk: The skill invokes a mutable npm package with `@latest`, so behavior can change between runs.

Mitigation: Pin the Satori CLI package version and review changes before upgrading.

Risk: Automatic credential provisioning may create or reuse local credentials without a clear setup step.

Mitigation: Make authentication explicit, document where credentials are stored, and provide deletion or reset controls.

## Reference(s):

- [Satori Skill Page](https://clawhub.ai/joelachance/skills/satori)
- [Fact Extraction Criteria](artifact/references/fact-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save facts or retrieve prior context through the Satori CLI when triggered by user requests or conversation context.]

## Skill Version(s):

0.0.1 (source: server release metadata, released 2026-01-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
