## Description:

DeepLink Agentic helps agents create, monitor, retrieve, and iterate on complex real-estate research tasks such as market analysis, land assessment, developer analysis, project case studies, policy interpretation, property-industry reports, and tender monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirleydddd](https://clawhub.ai/user/shirleydddd)

### License/Terms of Use:

MIT-0

## Use Case:

Real-estate professionals and external agents use this skill to delegate long-running industry research workflows to the DeepLink Agentic service. It is suited for creating research tasks, checking progress, handling human-in-the-loop questions, retrieving deliverables, and refining results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded reference files, task history, and bearer tokens are handled through agentic.dichanai.com.

Mitigation: Install and run the skill only when the user accepts that service trust boundary, and avoid sending confidential real-estate materials unless that is appropriate.

Risk: Token renewal can print a NEW_TOKEN value that may be exposed in logs or transcripts.

Mitigation: Treat printed tokens as secrets, avoid sharing them publicly, and rotate any token that may have been exposed.

Risk: The share command can make task content publicly accessible through a share link.

Mitigation: Do not use sharing for sensitive tasks unless the user explicitly approves public access.

Risk: The update check may direct users to replace local skill files from a service-provided URL.

Mitigation: Verify updates independently before replacing installed files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shirleydddd/skills/realestate-deep-research)
- [DeepLink Agentic service](https://agentic.dichanai.com)
- [DeepLink Agentic API documentation](https://agentic.apifox.cn/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and service-generated research deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task identifiers, status summaries, file listings, temporary download links, and token-renewal messages.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
