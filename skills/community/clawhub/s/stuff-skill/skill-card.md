## Description:

Stuff Skill - 秩。告诉 AI 你想管理什么,它给你生成一个专属 App。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirayang-max](https://clawhub.ai/user/kirayang-max)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn a natural-language description of a personal collection, inventory, tracker, or list into a local-first or Cloudflare-synced personal data PWA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud templates can expose private personal records through unauthenticated public APIs and vulnerable generated pages.

Mitigation: Use local-only mode for sensitive data; before cloud deployment add authentication, owner-level authorization, restricted CORS, input validation, safe DOM rendering, and pinned deployment tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kirayang-max/skills/stuff-skill)
- [Inspiration scenarios](references/inspiration.md)
- [Field inference rules](references/field-inference.md)
- [Design proposal guide](references/design-proposal.md)
- [UI component specification](references/components.md)
- [Cloudflare Pages and D1 deployment guide](references/deploy-guide.md)
- [Validation rules](references/validation.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with generated HTML, CSS, JavaScript, JSON, shell commands, and deployment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local PWA files by default and may add Cloudflare Pages Functions, D1 schema/configuration, service worker, and app icons for cloud mode.]

## Skill Version(s):

1.1.0 (source: release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
