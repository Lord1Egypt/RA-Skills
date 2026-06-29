## Description: <br>
Guides agents to apply adversarial review before non-trivial decisions so overconfident assumptions, edge cases, and contract failures are challenged while changes are still cheap to correct. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when correctness matters more than speed, especially for architecture decisions, non-trivial code changes, production deployments, data migrations, public API changes, or claims about safety, scalability, or specification compliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Important decisions may involve artifacts or contracts that contain sensitive information and may be shared with reviewer subagents or other models. <br>
Mitigation: Avoid including secrets in review artifacts unless the user intentionally wants that data reviewed, and require explicit authorization before cross-model review. <br>
Risk: Adversarial reviewers can produce noisy or context-limited findings that may mislead the main agent if accepted without reconciliation. <br>
Mitigation: Classify each finding against the artifact text as a contract misread, valid and actionable issue, valid tradeoff, or noise before changing the artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/qqyougit-doubt-driven-development) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance, checklists, adversarial-review prompts, and reconciliation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce claims, artifact and contract summaries, reviewer prompts, finding classifications, tradeoff notes, and stopping-condition decisions.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
