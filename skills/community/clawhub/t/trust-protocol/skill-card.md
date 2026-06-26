## Description: <br>
Manage agent trust graphs with Bayesian scoring, domain-specific scores, revocation, forgetting curves, challenge-response verification, and a local dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FELMONON](https://clawhub.ai/user/FELMONON) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain local trust records for AI agents, update scores after interactions, verify identity through challenge-response flows, and inspect trust graphs before relying on another agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell command construction in the Moltbook integration can treat crafted usernames, domains, or post IDs as local shell commands. <br>
Mitigation: Avoid untrusted Moltbook values until the helper uses subprocess argument lists and validates inputs. <br>
Risk: The skillsign dependency is referenced without a pinned version. <br>
Mitigation: Review and pin a trusted skillsign revision before using ATP in a sensitive workflow. <br>
Risk: ATP stores trust history, interaction notes, challenge files, and Moltbook links persistently under ~/.atp. <br>
Mitigation: Avoid recording secrets or sensitive personal data in notes, and protect or clean ~/.atp according to the environment's retention needs. <br>
Risk: The dashboard serves local trust and interaction data on localhost:8420 when started. <br>
Mitigation: Run the dashboard only on trusted machines and stop it when review is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FELMONON/trust-protocol) <br>
- [skillsign identity integration](https://github.com/FELMONON/skillsign) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with CLI command examples and JSON or graph exports from local commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write local trust records, interactions, challenge files, and dashboard data under ~/.atp when run.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; package.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
