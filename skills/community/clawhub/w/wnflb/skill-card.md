## Description:

福利吧 helps an agent fetch recent posts from selected wnflb forum sections, extract thread content, summarize key information, and perform forum check-in using a configured cookie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nsnake](https://clawhub.ai/user/nsnake)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to review recent 福利吧 forum activity, summarize thread contents, extract useful links or passwords mentioned in posts, and run the forum check-in flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles forum login cookies and may update cookie.txt during scraping.

Mitigation: Use a dedicated low-privilege forum account, keep cookie.txt tightly permissioned, and avoid placing unrelated cookies in the file.

Risk: The security scan reports unsafe cookie handling and remote JavaScript execution during scraping.

Mitigation: Review before installing and avoid using the skill on untrusted redirects or sensitive sessions unless redirect parsing and cookie-origin checks are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nsnake/skills/wnflb)
- [福利吧 forum](https://www.wnflb2023.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, with JSON returned from Node.js commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22+ and a configured cookie.txt for authenticated forum access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
