## Description:

Reads WeChat official account articles by opening the URL with the built-in browser, normalizing it with ?scene=1, and extracting the body text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernylinville](https://clawhub.ai/user/bernylinville)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve readable text from WeChat official account articles for summarization, review, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from an unpinned GitHub main-branch URL can differ from the reviewed ClawHub artifact.

Mitigation: Install from the reviewed ClawHub artifact or from a pinned commit.

Risk: The skill opens the user-provided WeChat article URL in a browser to extract page text.

Mitigation: Provide only article URLs intended for retrieval and review the extracted text before using it in downstream workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bernylinville/skills/wechat-mp-reader)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text article content with concise troubleshooting guidance when extraction fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser navigation for the provided WeChat article URL and closes the opened tab after extraction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
