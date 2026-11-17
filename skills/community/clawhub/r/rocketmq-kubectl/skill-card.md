## Description:

Query and manage RocketMQ clusters and messages through kubectl exec, including cluster inspection, topic and consumer administration, message lookup, offset resets, statistics, and test messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peintune](https://clawhub.ai/user/peintune)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect and administer RocketMQ running in Kubernetes, including topic lifecycle operations, consumer backlog checks, message lookup, and controlled test messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RocketMQ administration commands can delete topics, reset consumer offsets, write test messages, or consume messages against live clusters.

Mitigation: Require explicit human approval, confirm namespace, cluster, topic, and consumer group targets, and use non-production or approved production targets only.

Risk: Message lookup and direct pod file reads can expose message payloads or sensitive operational data.

Mitigation: Validate message IDs, keys, topics, and pod paths before use, and limit output to information the requester is authorized to inspect.

## Reference(s):

- [Apache RocketMQ Admin Tool Documentation](https://rocketmq.apache.org/zh/docs/deploymentOperations/02admintool/)
- [ClawHub Skill Page](https://clawhub.ai/peintune/skills/rocketmq-kubectl)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Kubernetes pods running RocketMQ mqadmin and require user-provided topics, consumer groups, message IDs, broker names, queue IDs, offsets, and nameserver values.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
