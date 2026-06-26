## Description: <br>
Query and manage RocketMQ messages via kubectl exec for cluster, topic, consumer, message, offset, statistics, and test-message operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peintune](https://clawhub.ai/user/peintune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate kubectl exec commands for administering RocketMQ deployments in Kubernetes, including inspecting clusters, managing topics, checking consumer progress, querying messages, resetting offsets, and sending test messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose production-capable RocketMQ administration commands that delete topics, reset consumer offsets, skip messages, or send test messages. <br>
Mitigation: Confirm the Kubernetes context, namespace, pod, topic, consumer group, broker, and exact command before execution, and use write operations only with approval, backups or rollback procedures, and a clear operational reason. <br>


## Reference(s): <br>
- [Apache RocketMQ Admin Tool Documentation](https://rocketmq.apache.org/zh/docs/deploymentOperations/02admintool/) <br>
- [ClawHub skill page](https://clawhub.ai/peintune/rocketmq-kubectl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with kubectl and mqadmin command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may include user-supplied Kubernetes namespaces, pods, topics, consumer groups, broker names, offsets, queue IDs, and message identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
