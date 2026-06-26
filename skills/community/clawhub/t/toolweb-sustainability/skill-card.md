## Description: <br>
AI-powered platform that generates personalized career roadmaps for entry-level sustainability professionals based on skills assessment and goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate personalized sustainability career roadmaps from career assessment data, current skills, and goals. It also exposes specialization and learning-path lookups for sustainability career planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Career assessment data is sent to an external API provider. <br>
Mitigation: Limit inputs to the information needed for roadmap generation, avoid secrets or highly sensitive personal data, and confirm the destination endpoint before using real profiles. <br>
Risk: Generated career roadmaps may be incomplete or unsuitable for a user's professional context. <br>
Mitigation: Review roadmap recommendations before acting on them and adapt milestones, learning paths, and timelines to the user's circumstances. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-sustainability) <br>
- [Kong route](https://api.mkkpro.com/career/sustainability) <br>
- [API docs](https://api.mkkpro.com:8178/docs) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [JSON responses and human-readable roadmap guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Roadmap responses may include phases, objectives, learning paths, milestones, recommended resources, specialization options, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
