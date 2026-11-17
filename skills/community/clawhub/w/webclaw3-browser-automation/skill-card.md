## Description:

webclaw3 lets an agent drive a user's already-logged-in Chrome for browser automation and web scraping, then turn successful browser explorations into reusable local skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and agent users use this skill to automate browser tasks and web data extraction in their own Chrome session, including pages that require login. After a successful exploration, they can distill the workflow into a local repeatable skill for scheduled or recurring use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive an already-logged-in Chrome session, including clicks, form submissions, and JavaScript execution on private pages.

Mitigation: Use it only with accounts and browser profiles where that access is acceptable, and supervise actions on sensitive admin, payment, financial, or production systems.

Risk: Local browser-control services are started on localhost and the security scan reports them as unauthenticated.

Mitigation: Run the skill only on a trusted machine, stop the services when not in use, and prefer a release that authenticates local service calls.

Risk: The setup flow can download or install executable components and the scan warns about mutable remote code.

Mitigation: Review installation commands and downloaded artifacts before running them, and prefer pinned or verified artifacts when available.

Risk: An Access Key is stored locally for generation quota and site-knowledge features.

Mitigation: Protect the local webclaw3 configuration file, avoid sharing logs or config snapshots that may include credentials, and rotate the key if exposed.

## Reference(s):

- [README](README.md)
- [Inside the webclaw3 skill](docs/webclaw3-skill-intro.md)
- [Setup guide](references/setup.md)
- [Distillation workflow](references/brief.md)
- [CDP fallback](references/cdp-fallback.md)
- [Repair playbook](references/repair.md)
- [webclaw3 site](https://webclaw3.com)
- [wc3 Chrome extension](https://github.com/fatmind/wc3-chrome)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON API examples, and generated local skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include browser automation results, generated requirement and primer documents, local skill code, and repair guidance.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
