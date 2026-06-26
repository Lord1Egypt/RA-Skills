## Description: <br>
Shed provides context-window hygiene guidance for long-running LLM agents, including when to compress, mask, switch, or delegate context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compass-soul](https://clawhub.ai/user/compass-soul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Shed to manage context growth during extended agent sessions and to design agent architectures with explicit context-management rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated memory notes could contain secrets, credentials, private transcripts, or unnecessary personal data. <br>
Mitigation: Keep notes in a known workspace, review them for accuracy, and avoid saving sensitive or unnecessary personal information. <br>
Risk: Context-compression guidance could preserve incorrect or misleading summaries if applied without review. <br>
Mitigation: Review condensed notes and retained breadcrumbs before relying on them for future agent work. <br>


## Reference(s): <br>
- [Shed on ClawHub](https://clawhub.ai/compass-soul/shed) <br>
- [The Complexity Trap](https://arxiv.org/abs/2508.21433) <br>
- [OpenHands Context Condensation](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents) <br>
- [Letta Memory Blocks](https://www.letta.com/blog/memory-blocks) <br>
- [LLMLingua-2](https://aclanthology.org/2024.acl-long.91/) <br>
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) <br>
- [Found in the Middle](https://arxiv.org/abs/2406.16008) <br>
- [MEM1 Dynamic State Management](https://arxiv.org/abs/2506.15841) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with decision rules and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no code execution or external tool calls are required by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
