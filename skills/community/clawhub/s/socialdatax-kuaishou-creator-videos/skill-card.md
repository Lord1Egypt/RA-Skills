## Description: <br>
Helps agents retrieve and summarize Kuaishou/Kwai creator video lists and recent creator-content activity through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect creator video lists, recent publishing behavior, content style, and account benchmarks for Kuaishou/Kwai creators. The artifact also documents SocialDataX commands for related Weibo and WeChat Channels creator-post lookups, so users should confirm the intended platform before running collection commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a third-party SocialDataX npm CLI and SOCIALDATAX_API_KEY for external creator-content lookups. <br>
Mitigation: Install only if that third-party dependency and API-key use are acceptable; provide the key through SOCIALDATAX_API_KEY and review commands before running them. <br>
Risk: The Kuaishou-focused release also documents Weibo and WeChat Channels commands, which may cause users to collect from a broader platform scope than intended. <br>
Mitigation: Confirm the exact platform and command before execution, and use --max-items or explicit page limits instead of --all unless broad collection is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-kuaishou-creator-videos) <br>
- [SocialDataX API access homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only SocialDataX lookups require SOCIALDATAX_API_KEY, node, and npm; CLI output is JSON.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
