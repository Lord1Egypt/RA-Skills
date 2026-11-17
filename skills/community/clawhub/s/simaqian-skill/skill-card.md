## Description:

Turns a person's existing materials, answers, or optional interview into a concise Personal OS: a Markdown persona document for AI agents and a polished HTML personal homepage for humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaohuadavidlee](https://clawhub.ai/user/shaohuadavidlee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize personal materials, optional interview answers, and public-facing links into reusable identity assets for AI collaboration and human collaboration discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad memory-based personal profiling can include details the user did not intend to publish.

Mitigation: Use long-term memory, past chats, resumes, and private materials only with explicit user intent, and review generated persona content before sharing or reuse.

Risk: Generated profile pages and links can expose personal or third-party private information.

Mitigation: Keep generated persona and homepage files private by default, remove secrets and private third-party details, and publish only after user review.

Risk: Unpinned external skill installation can make the installed behavior differ from the reviewed release.

Mitigation: Pin the reviewed release or manually inspect the installed source before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaohuadavidlee/skills/simaqian-skill)
- [司马迁.skill public site](https://simaqian.caojuege.com)
- [Intake and interview framework](references/intake-and-interview.md)
- [Output specification](references/output-spec.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown persona document and single-file HTML personal homepage, with optional interview questions and revision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated personal profile content should be reviewed before sharing and kept private unless the user intentionally publishes it.]

## Skill Version(s):

1.3.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
