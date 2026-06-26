## Description: <br>
Gives any AI agent persistent memory of who the user is, including patterns, preferences, personality traits, and behavioral evolution, by maintaining and referencing a workspace-local soul_ledger.json file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to let an agent maintain a persistent, local model of a user's traits, communication preferences, drives, and meaningful interaction history so future conversations can adapt from the start. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently creates and reuses a persistent personal profile about the user, including inferred traits and behavior patterns. <br>
Mitigation: Install only when persistent personal memory is intentional, keep the workspace private, inspect soul_ledger.json regularly, and require explicit user consent before reading or writing the ledger. <br>
Risk: A forget request may be undermined if removed details are retained indirectly or re-inferred from previous entries. <br>
Mitigation: Fully delete requested information from the ledger and review remaining traits, history, and growth notes for indirect retention before continuing to use the profile. <br>


## Reference(s): <br>
- [Soul Ledger Skill Page](https://clawhub.ai/albionaiinc-del/soul-ledger) <br>
- [Publisher Profile](https://clawhub.ai/user/albionaiinc-del) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON, Files] <br>
**Output Format:** [Markdown instructions and a JSON ledger schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, reads, and updates a workspace-local soul_ledger.json profile when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
