## Description:

Publishes research and analysis content as visually rich HTML pages, pushes them to a configured GitHub repository, and returns an htmlpreview link backed by jsDelivr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2239721014-ops](https://clawhub.ai/user/2239721014-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, analysts, and agents use this skill to convert completed research reports or HTML documents into public web pages with preview links. It is intended for workflows that intentionally publish report files to a GitHub-hosted public delivery path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms may start a publishing workflow when a user only intended research or analysis.

Mitigation: Require explicit confirmation that the user wants publication before creating commits, pushing to GitHub, or sharing a public preview URL.

Risk: Published reports are routed through a named GitHub repository and public preview/CDN links.

Mitigation: Confirm the exact source file, destination repository, branch, path, commit contents, and public URL before any git push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2239721014-ops/skills/research-web-publisher)
- [Configured GitHub publishing repository](https://github.com/2239721014-ops/ai-hardwork-report)
- [Configured jsDelivr delivery path](https://cdn.jsdelivr.net/gh/2239721014-ops/ai-hardwork-report@master/workplace-doc/{filename})
- [Configured htmlpreview preview path](https://htmlpreview.github.io/?https://cdn.jsdelivr.net/gh/2239721014-ops/ai-hardwork-report@master/workplace-doc/{filename})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML preview links and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an htmlpreview URL for the published report and may describe the generated file path or publishing status.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
