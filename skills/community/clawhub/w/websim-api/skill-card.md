## Description:

Access WebSim's REST API to retrieve public user profiles, projects, comments, trending feeds, social graphs, and project assets, with comment posting only when explicitly requested and authenticated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upintheairsheep](https://clawhub.ai/user/upintheairsheep)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to look up WebSim users, projects, comments, trending content, social relationships, and public assets. It can also support user-directed community interaction by posting a comment with a user-supplied WebSim bearer token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting comments requires a user-supplied WebSim bearer token and could act on a user's account.

Mitigation: Only post comments when the user explicitly asks, avoid storing or exposing the token, and confirm the target project and comment content before sending.

Risk: Project detail responses can include internal reasoning fields such as site.yapping that may be inappropriate to disclose.

Mitigation: Do not retrieve, repeat, or summarize internal reasoning fields unless the user specifically requests them and disclosure is appropriate.

Risk: Rapid sequential API requests may create unnecessary load or trigger rate limits.

Mitigation: Use one request at a time and paginate deliberately based on user need.

## Reference(s):

- [WebSim](https://websim.com)
- [ClawHub skill page](https://clawhub.ai/upintheairsheep/skills/websim-api)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or concise text with API request details and summarized WebSim data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links to WebSim profiles, projects, comments, assets, and pagination guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
