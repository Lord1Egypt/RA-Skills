## Description: <br>
Redis缓存大师 provides production-oriented Redis guidance for TTL discipline, eviction strategy selection, cluster hash tags, atomic operations, reliable Streams messaging, persistence choices, large-key handling, memory monitoring, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to design, operate, and troubleshoot production Redis caching, locking, rate limiting, messaging, persistence, and cluster patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redis command and configuration examples can change production state, including CONFIG SET, writes, deletes, UNLINK operations, persistence changes, locks, and message processing. <br>
Mitigation: Confirm the target environment and review each command before execution; prefer staging validation and require explicit approval for production changes. <br>
Risk: Operational Redis guidance can be misapplied when workload, persistence, memory, cluster, or failover requirements differ from the examples. <br>
Mitigation: Validate settings against the deployment's workload and recovery requirements, monitor Redis health metrics, and keep backups or rollback steps available before changing production configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/redis-cache-master) <br>
- [Redis download](https://redis.io/download) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Redis command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes redis-cli examples and operational checklists; commands require environment review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
