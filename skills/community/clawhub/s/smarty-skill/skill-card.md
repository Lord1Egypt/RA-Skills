## Description: <br>
Always active in every session. Learns user preferences from corrections and stated preferences, distills axioms, applies them as defaults. Makes every other skill better over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckpxgfnksd-max](https://clawhub.ai/user/ckpxgfnksd-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent capture preference signals, reflect them into a compact profile, and apply those preferences as soft defaults in future sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill quietly stores and reuses local preference signals across sessions. <br>
Mitigation: Install only when persistent preference memory is desired, periodically review or delete memory/context-infra/observations.log and memory/context-infra/context-profile.md, and use explicit retractions when preferences should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckpxgfnksd-max/smarty-skill) <br>
- [Profile Format](profile-format.md) <br>
- [Context Infrastructure](https://yage.ai/context-infrastructure.html) <br>
- [autoresearch method](https://github.com/karpathy/autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance, configuration] <br>
**Output Format:** [Markdown profile entries and pipe-delimited observation log lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local preference observations and applies distilled axioms as soft defaults.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
