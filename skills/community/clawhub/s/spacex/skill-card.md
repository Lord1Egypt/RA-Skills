## Description: <br>
CLI for AI agents to lookup SpaceX launches and rockets for their humans. No auth required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent answer questions about SpaceX launches, rockets, launch details, and crew using the community SpaceX API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed bundle does not include the actual CLI executable described by the README. <br>
Mitigation: Inspect and pin the external GitHub repository before running the installed command. <br>
Risk: Launch data comes from a community-maintained API and may lag behind real-time SpaceX status. <br>
Mitigation: Treat answers as public lookup results and verify time-sensitive launch status against authoritative sources before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffaf/spacex) <br>
- [Publisher profile](https://clawhub.ai/user/jeffaf) <br>
- [SpaceX API repository](https://github.com/r-spacex/SpaceX-API) <br>
- [SpaceX API documentation](https://github.com/r-spacex/SpaceX-API/tree/master/docs) <br>
- [SpaceX API v4 base URL](https://api.spacexdata.com/v4) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Concise terminal text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, and jq; uses the unauthenticated community SpaceX API.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
