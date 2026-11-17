## Description:

Shed gives long-running LLM agents decision rules for managing context windows by compressing, masking, switching, or delegating context when sessions grow large.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compass-soul](https://clawhub.ai/user/compass-soul)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Shed to keep extended LLM sessions manageable by extracting key facts from large tool outputs, condensing context before overflow, and handing off work when context becomes stale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived memory or breadcrumb files could retain secrets or sensitive raw tool output if an agent follows the guidance without filtering.

Mitigation: Extract only necessary facts, redact credentials and sensitive values, and avoid storing raw command output or private data in persistent memory files.

## Reference(s):

- [Lindenbauer et al., The Complexity Trap](https://arxiv.org/abs/2508.21433)
- [OpenHands Context Condensation](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents)
- [Letta/MemGPT Memory Blocks](https://www.letta.com/blog/memory-blocks)
- [LLMLingua-2](https://aclanthology.org/2024.acl-long.91/)
- [Liu et al., Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Hsieh et al., Found in the Middle](https://arxiv.org/abs/2406.16008)
- [MEM1 Dynamic State Management](https://arxiv.org/abs/2506.15841)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance and concise operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short checklists, decision rules, or file-writing guidance for context handoff.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
