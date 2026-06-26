## Description: <br>
Incrementally AI-labels unmarked Feishu Bitable records for public-opinion categories such as type, sentiment, competitor mention, device, brand safety, and content safety using an OpenAI-compatible model provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankieway](https://clawhub.ai/user/frankieway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and public-opinion analysis teams use this skill to batch-label Feishu Bitable rows for sentiment, product relevance, competitor mentions, device category, and safety review. The skill is intended for records that can be shared with the configured Feishu app and OpenAI-compatible model provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu table content is sent to the configured OpenAI-compatible model provider. <br>
Mitigation: Use only data approved for that provider and confirm the provider's retention, privacy, and compliance terms before running the skill. <br>
Risk: The skill can write AI-generated labels back to the target Bitable. <br>
Mitigation: Start with a small limit, use a Feishu app restricted to the intended Bitable, and review updated rows before broader use. <br>
Risk: Allowed model-provider inputs, network destinations, and rollback behavior are under-disclosed. <br>
Mitigation: Ask the publisher to declare provider inputs, allowed destinations, privacy behavior, and a dry-run or rollback process before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankieway/yuqing-label-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status output and updated Feishu Bitable fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes labels back to the target Feishu Bitable and prints labeling_updated_count.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
