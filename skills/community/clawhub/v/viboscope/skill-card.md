## Description: <br>
Viboscope helps users find compatible people for cofounding, projects, groups, friendships, and other relationship contexts through psychological compatibility matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivankoriako](https://clawhub.ai/user/ivankoriako) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to build a Viboscope profile, run questionnaires or profile-deepening flows, search for compatible people, manage messages, and maintain privacy settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to inspect local files, git config, prior chats, or profile data for psychological profiling before clear consent. <br>
Mitigation: Require explicit user approval before context scans or reading personal/local data, and show the findings before using them in a profile. <br>
Risk: The skill stores and uses sensitive psychological profile data for matching. <br>
Mitigation: Review the exact profile text before upload, proceed only after explicit consent, and use privacy settings to limit public fields. <br>
Risk: The skill relies on a local API key file for authenticated requests. <br>
Mitigation: Keep data/.api_key private, set restrictive file permissions, avoid embedding the key in visible commands, and rotate it if exposed. <br>
Risk: The generic trigger 'inbox' can invoke Viboscope when the user may mean another mailbox. <br>
Mitigation: Confirm intent before handling ambiguous inbox or message requests as Viboscope actions. <br>


## Reference(s): <br>
- [Viboscope ClawHub listing](https://clawhub.ai/ivankoriako/viboscope) <br>
- [Viboscope API base](https://viboscope.com/api/v1) <br>
- [Viboscope skill download endpoint](https://viboscope.com/api/v1/skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown conversation output with inline shell commands, JSON API payloads, and saved local profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local data files for API keys, prompts, raw questionnaire answers, and profile data when the user consents.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
