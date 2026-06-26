## Description: <br>
Gmail platform skill for SurfAgent, covering mailbox checks, mailbox triage, latest-thread opening, compose and reply task runners, tab hygiene, sent-message verification, proof rules, and when to use the Gmail adapter over raw browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surfagentapp](https://clawhub.ai/user/surfagentapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide SurfAgent-style browser agents through Gmail mailbox checks, triage, compose, reply, and send-verification workflows. It is intended for agents operating Gmail through SurfAgent/browser adapter tooling with explicit proof checks before claiming completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports sensitive email actions through a separate SurfAgent/browser adapter and an active Gmail session. <br>
Mitigation: Require explicit user confirmation before sending or replying to email, and treat adapter permissions and the active Gmail session as separate trust decisions. <br>
Risk: A clicked send control or draft state alone can be mistaken for successful delivery. <br>
Mitigation: Verify Gmail send confirmation and confirm the resulting message in Sent Mail or the opened sent thread before claiming success. <br>
Risk: Mailbox triage is heuristic and may rank visible threads imperfectly. <br>
Mitigation: Use triage as action guidance only, keep proof tied to visible mailbox or thread evidence, and avoid presenting it as a full Gmail classification engine. <br>


## Reference(s): <br>
- [SurfAgent homepage](https://surfagent.app) <br>
- [ClawHub skill page](https://clawhub.ai/surfagentapp/surfagent-gmail) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for Gmail mailbox, compose, reply, triage, and verification workflows.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
