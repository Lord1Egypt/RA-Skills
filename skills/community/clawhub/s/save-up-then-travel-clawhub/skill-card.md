## Description: <br>
A Chinese travel-points journaling skill that turns daily high-energy actions into travel progress and shows how close the user is to 50, 100, and 300 point travel goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyikoi](https://clawhub.ai/user/keyikoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to record one daily high-energy behavior, receive travel points, and see progress toward nearby travel rewards. It is intended for lightweight reward journaling, not trip planning, booking, visa advice, or general life coaching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may collect or discuss personal behavior history and point totals during journaling. <br>
Mitigation: Confirm how the host stores point totals and history before using it with personal data. <br>
Risk: One bundled reference broadens the concept into general reward suggestions, which may not match a strictly travel-only tracker. <br>
Mitigation: Review the reward scope before deployment and keep user-facing responses focused on travel-point progress. <br>


## Reference(s): <br>
- [Product Principles](artifact/references/product_principles.md) <br>
- [Reward Pool Configuration](artifact/assets/reward_pool.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/keyikoi/save-up-then-travel-clawhub) <br>
- [Mobile Preview](https://save-up-then-travel-home.pages.dev/?viewport=mobile) <br>
- [Web Preview](https://save-up-then-travel-home.pages.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chinese structured Markdown or a short link-first response when an interactive preview is available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should confirm the behavior, points earned, current travel progress, and a concise emotional reinforcement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
