## Description: <br>
Long Term Memory 长期记忆 helps agents store, search, organize, and compress durable memory notes across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain local long-term context such as user preferences, decisions, important events, lessons, and knowledge notes. It is suited to workflows that need searchable memory across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes SkillPay billing behavior that can charge an external service without a clear per-call confirmation step. <br>
Mitigation: Install only when paid SkillPay-backed memory use is intended, confirm the SKILLPAY_USER_ID mapping, and verify when charges occur before running the skill. <br>
Risk: Long-term memory can retain sensitive personal, financial, health, credential, or secret material and later expose it through search or reuse. <br>
Mitigation: Avoid storing highly sensitive information, review memory files regularly, and delete or archive records that should not be retained. <br>
Risk: The security guidance calls out a hardcoded billing key as a review concern. <br>
Mitigation: Review whether the bundled billing key is acceptable for the deployment environment before enabling the skill. <br>


## Reference(s): <br>
- [Memory Taxonomy](references/memory-taxonomy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shenmeng/shenmeng-long-term-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown memory files and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and searches local memory files under the agent workspace, with optional archive summaries for older memories.] <br>

## Skill Version(s): <br>
2025.4.15 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
