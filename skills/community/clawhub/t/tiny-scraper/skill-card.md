## Description:

TinyScraper mirrors simple static websites by downloading same-domain HTML, JavaScript, CSS, and static assets for offline browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alukardo](https://clawhub.ai/user/alukardo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use TinyScraper to preview and mirror authorized simple static websites into local files for offline browsing or archival review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can make arbitrary HTTP requests from the agent environment and create many local files.

Mitigation: Use it only for trusted, authorized sites, preview crawl scope with dry-run where possible, and run it in a contained workspace.

Risk: Unsafe path handling can write or delete outside the intended mirror folder.

Mitigation: Review the skill before installation and avoid the cleanup command until path validation and containment checks are added.

## Reference(s):

- [TinyScraper Format Specification](references/SPEC.md)
- [ClawHub Skill Page](https://clawhub.ai/alukardo/skills/tiny-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, progress text, and local mirrored website files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local mirror directories under the configured workspace and preserves external links instead of downloading them.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
