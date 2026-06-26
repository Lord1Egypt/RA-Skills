## Description: <br>
Create, schedule, and manage social media posts via Typefully for X/Twitter, LinkedIn, Threads, Bluesky, and Mastodon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankdilo](https://clawhub.ai/user/frankdilo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to draft, schedule, publish, and manage Typefully posts across connected social accounts from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, schedule, or publish public social posts for connected accounts. <br>
Mitigation: Review the selected social set and final post content before scheduling or publishing, and create drafts when approval is needed. <br>
Risk: An API endpoint override could send API keys and post content to an unintended endpoint if misconfigured. <br>
Mitigation: Keep TYPEFULLY_API_BASE unset unless the endpoint is intentionally configured and trusted. <br>
Risk: Setup may store the Typefully API key in local or global configuration. <br>
Mitigation: Store credentials only in trusted locations and avoid committing local Typefully configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankdilo/typefully-social-media) <br>
- [Typefully API documentation](https://typefully.com/docs/api) <br>
- [Typefully API key settings](https://typefully.com/?settings=api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON responses, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Typefully API key and selected social set before API operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
