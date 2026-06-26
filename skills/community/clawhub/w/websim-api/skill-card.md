## Description: <br>
Access WebSim's REST API to retrieve user profiles, projects, comments, trending feeds, social graphs, and searchable public project assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upintheairsheep](https://clawhub.ai/user/upintheairsheep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to discover and inspect WebSim users, projects, community comments, trending feeds, social graphs, and public uploaded assets. It can also guide a user-requested authenticated comment post when the project, reply target, and comment text are confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated comment posting can publish user-visible content to WebSim. <br>
Mitigation: Only provide a WebSim Bearer token when intending to post a comment, and require the agent to show the exact project, reply target, and comment text before sending it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/upintheairsheep/websim-api) <br>
- [WebSim](https://websim.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown summaries with endpoint URLs, request examples, and structured API result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTP request details; authenticated comment posting requires explicit user intent and a WebSim Bearer token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
