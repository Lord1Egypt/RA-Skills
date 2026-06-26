## Description: <br>
Looks up Xiaohongshu, XHS, and RedNote creator profile data through SocialDataX using a configured API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to retrieve creator profile facts such as account identifiers, bio, verification, follower counts, engagement totals, IP location, and gender when available. It supports read-only creator profile lookup by user ID or profile URL/share text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SocialDataX API key for profile lookups. <br>
Mitigation: Provide SOCIALDATAX_API_KEY only in environments where the agent is authorized to make SocialDataX read-only data calls. <br>
Risk: The preferred direct CLI uses the socialdatax-skills npm package, commonly invoked with @latest in the artifact guidance. <br>
Mitigation: Review npm package provenance separately or pin the package version when dependency immutability is required. <br>
Risk: Creator profile fields may be incomplete, unavailable, or unsuitable as standalone strategic advice. <br>
Mitigation: Report returned profile facts separately from any interpretation and avoid presenting derived strategy as source data. <br>


## Reference(s): <br>
- [SocialDataX API access homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-xhs-creator-profile) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON profile data from SocialDataX tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY and node/npm; profile facts should be separated from strategic interpretation.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
