## Description:

Get random fun content (joke, funny story/duanzi, poisonous chicken soup/dujitang) from public APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aolinlu](https://clawhub.ai/user/aolinlu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to fetch a random joke, funny story, or dujitang quote when a user asks for light humorous content. It is suited for conversational assistants that can run a small Python script and return plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill contacts api.pearktrue.cn to retrieve content, which may be unsuitable in restricted or privacy-sensitive environments.

Mitigation: Use the skill only where that external API access is acceptable, or block network execution for this skill in restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aolinlu/skills/request-random-jokes)
- [Random joke API endpoint](https://api.pearktrue.cn/api/jdyl/xiaohua.php)
- [Random funny story API endpoint](https://api.pearktrue.cn/api/random/duanzi/)
- [Dujitang API endpoint](https://api.pearktrue.cn/api/dujitang)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text returned by a Python script, with Markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contacts fixed public API endpoints at api.pearktrue.cn and prints the response text.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
