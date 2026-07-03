## Description: <br>
Helps agents retrieve read-only Weibo post details, content, author information, media, publish time, and interaction metrics through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch structured Weibo post detail data for content research and analysis when they have a post ID, post URL, short link, or share text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill requires providing a SocialDataX API key to the socialdatax-skills npm CLI. <br>
Mitigation: Install only if comfortable with SocialDataX, and use account controls such as scoped keys or billing limits where available. <br>
Risk: The runtime package is fetched from npm, so package trust remains part of deployment risk. <br>
Mitigation: Review and trust the npm package before use, and run the CLI in a controlled agent environment. <br>


## Reference(s): <br>
- [SocialDataX homepage](https://socialdatax.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON from the SocialDataX CLI or structured text summary from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Weibo post detail output; requires SOCIALDATAX_API_KEY and node/npm for direct CLI use.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
