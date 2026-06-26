## Description: <br>
Systematically reviews and refines an agent's draft responses for logic, accuracy, completeness, conciseness, actionability, and consistency before delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhou22](https://clawhub.ai/user/thomaszhou22) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add an internal self-review loop before final responses, with deeper review for complex, factual, code, or high-stakes outputs. It can also persist brief reflection notes so later sessions can avoid repeated response-quality mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist brief task-derived reflection notes, which may retain information from sensitive prompts, proprietary code, or regulated data. <br>
Mitigation: Review the memory behavior before installing and disable or periodically delete memory/reflections.md when persistent self-correction notes are not acceptable. <br>


## Reference(s): <br>
- [Reflection Prompt Templates](references/reflection-templates.md) <br>
- [Academic Sources](references/sources.md) <br>
- [Benchmark Report](BENCHMARK.md) <br>
- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) <br>
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) <br>
- [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) <br>
- [ClawHub Skill Page](https://clawhub.ai/thomaszhou22/self-refine-reflection) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands] <br>
**Output Format:** [Refined agent responses in the format requested by the user, commonly plain text or Markdown with optional code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Internal critique is not shown to the user; optional local reflection notes may be appended for cross-session memory.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
