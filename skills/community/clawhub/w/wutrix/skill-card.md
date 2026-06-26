## Description: <br>
Wutrix connects an OpenClaw agent to a film pre-production workspace to save ideas and query projects, scenes, characters, and story materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwneox](https://clawhub.ai/user/kwneox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative teams use this skill to let an OpenClaw agent record Wutrix inbox ideas and retrieve project, scene, character, and worldbuilding information through the configured Wutrix backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses INSPIRESTUDIO_API_KEY to read Wutrix project data and add inbox ideas. <br>
Mitigation: Install only against a Wutrix backend you operate or trust, use the narrowest scoped key available, and avoid pointing the skill at untrusted services. <br>


## Reference(s): <br>
- [Wutrix ClawHub skill page](https://clawhub.ai/kwneox/wutrix) <br>
- [Wutrix project homepage](https://github.com/kwneox/inspirestudio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON from helper scripts and concise Chinese text or Markdown summaries from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INSPIRESTUDIO_URL and INSPIRESTUDIO_API_KEY; query results should be summarized for the user rather than dumped as raw JSON.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
