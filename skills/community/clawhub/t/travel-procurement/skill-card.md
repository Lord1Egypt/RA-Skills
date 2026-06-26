## Description: <br>
Source, compare, and recommend travel transport options (bus/train/shuttle/taxi/private transfer) from user-provided trip constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austineyapp](https://clawhub.ai/user/austineyapp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travel planners, operations teams, and individual travelers use this skill to compare transport options against route, timing, passenger, luggage, budget, and comfort constraints. It supports decision-ready recommendations for value, convenience, and fallback travel choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel prices, schedules, cancellation terms, or availability may be stale or incorrect. <br>
Mitigation: Verify live provider details before relying on an option or presenting it for purchase. <br>
Risk: A recommended provider or booking channel may not be legitimate or suitable for the traveler. <br>
Mitigation: Check provider legitimacy, payment details, route fit, passenger capacity, and luggage capacity before booking. <br>
Risk: The skill can prepare next-step execution after a user chooses an option, which may lead toward booking or payment. <br>
Mitigation: Require separate explicit approval before any booking, payment, or irreversible travel commitment. <br>


## Reference(s): <br>
- [Option Format](references/option-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown comparison with normalized options, recommendations, fallback, and decision ask] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each option should include total price, practical caveat, cancellation terms, capacity fit, and a risk note.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
