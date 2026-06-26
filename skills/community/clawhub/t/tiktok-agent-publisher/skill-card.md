## Description: <br>
Prepare, validate, and explicitly publish TikTok content through the official Content Posting API with dry-run safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install, configure, validate, and troubleshoot TikTok Agent Publisher for official Content Posting API workflows. It emphasizes explicit consent, dry-run checks, OAuth readiness, privacy review, and safe handling of publishing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth tokens, API keys, local token files, or private account data could be exposed in chat or logs. <br>
Mitigation: Keep secrets out of prompts and logs, and use diagnostic surfaces such as connection status, privacy audit, doctor, and dry-run checks before sharing output. <br>
Risk: A live publishing action could post to the wrong account or publish unintended content. <br>
Mitigation: Authorize only the intended TikTok account, review OAuth scopes, and use dry-run or preview flows before any live publishing call. <br>
Risk: The skill could be misused for spam, fake engagement, scraping, ban evasion, or other platform-abusive workflows. <br>
Mitigation: Use it only for user-owned TikTok accounts through official API flows with explicit user consent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/tiktok-agent-publisher) <br>
- [Repository](https://github.com/davidmosiah/tiktok-agent-publisher) <br>
- [npm Package](https://www.npmjs.com/package/tiktok-agent-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dry-run and diagnostic flows before live publishing or provider calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
