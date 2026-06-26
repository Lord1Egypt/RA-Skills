## Description: <br>
Automatically loads Slack channel context files into session context for Slack channels and threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hirebrianm](https://clawhub.ai/user/hirebrianm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw with Slack use this skill to load channel-specific project context, rules, and recent activity into agent sessions when working in a Slack channel or thread. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack channel context files can contain private internal notes or personal data that may be added to an AI session. <br>
Mitigation: Keep secrets, credentials, private personal data, and sensitive internal notes out of channel context files; review each context file before enabling it for a channel. <br>
Risk: Automatic context loading and caching can add stale or unintended channel information to a session. <br>
Mitigation: Use explicit per-channel allowlists, disable loading in threads when appropriate, and force reload after editing context files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hirebrianm/slack-channel-context) <br>
- [Context template](references/context-template.md) <br>
- [Example channel context](examples/EXAMPLE_CHANNEL_CONTEXT.md) <br>
- [Troubleshooting guide](TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON result containing loaded Markdown context and status metadata, plus Markdown guidance in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Loads channel context by channel ID before channel name, can skip threaded messages, and caches context reads for a configurable duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
