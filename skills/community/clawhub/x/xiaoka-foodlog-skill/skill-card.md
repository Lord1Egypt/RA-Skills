## Description:

Records meals in Xiaoka Health through its API, including meal type, calorie details, food-item details, and daily food-log summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baojuqiang](https://clawhub.ai/user/baojuqiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users who track meals with Xiaoka Health use this skill to bind an API key, log breakfast, lunch, dinner, snacks, and other food entries, and review today's calorie totals and food details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an API key locally.

Mitigation: Install only when local credential storage is acceptable, keep the credential file private, and remove the credential if account access should be revoked.

Risk: Environment variables can redirect the script to a different API endpoint.

Mitigation: Use the default Xiaoka Health endpoint and avoid running the skill where untrusted processes can set XIAOKA_API_BASE or XIAOKA_API.

Risk: Food entries are sent to Xiaoka Health for logging and calorie analysis.

Mitigation: Use the skill only when the user is comfortable sharing dietary entries with Xiaoka Health, and prefer explicit food-log commands over casual meal mentions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baojuqiang/skills/xiaoka-foodlog-skill)
- [Xiaoka Health API endpoint](https://cal-cn.ishuohua.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON-derived summaries with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; stores a local API key for authenticated requests.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
