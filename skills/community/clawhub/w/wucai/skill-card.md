## Description: <br>
WuCai lets an agent search, summarize, and manage a user's WuCai highlights, annotations, clipped articles, and diary entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makediff](https://clawhub.ai/user/makediff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to connect an agent to WuCai so it can retrieve recent highlights, search private notes, answer questions from saved web content, manage article status, and append diary entries when requested. <br>

### Deployment Geography for Use: <br>
Global, with CN, EU, and US region selection and physically isolated data stores. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive WuCai OpenClaw token that can access private highlights, notes, clippings, and diary data. <br>
Mitigation: Use a dedicated revocable token, store it in platform secret storage when available, and avoid sharing it in ordinary chat. <br>
Risk: Selecting the wrong CN, EU, or US region can connect the agent to the wrong isolated WuCai data store or make expected data unavailable. <br>
Mitigation: Confirm WUCAI_REGION before use and match user-facing links and instructions to the selected region. <br>
Risk: Write actions can append diary entries, update article notes, change article status, or move articles to trash. <br>
Mitigation: Ask for confirmation before write or trash actions and summarize the target record and intended change before executing. <br>


## Reference(s): <br>
- [WuCai documentation](https://doc.wucai.site) <br>
- [WuCai global site](https://wucainote.com) <br>
- [WuCai API details](references/api-details.md) <br>
- [WuCai ClawHub listing](https://clawhub.ai/makediff/wucai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Agent-facing text or Markdown, shell command invocations, and JSON API responses from the WuCai helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WUCAI_API_TOKEN and optionally WUCAI_REGION; list and search requests are constrained to a maximum 14-day range.] <br>

## Skill Version(s): <br>
26.3.37 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
