## Description: <br>
Hermetic divination CLI for astrology, tarot, gematria, and numerology that instructs the agent to run the CLI before interpreting calculated or drawn results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aklo360](https://clawhub.ai/user/aklo360) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to install and run the thoth CLI for astrology charts, transits, electional timing, tarot draws, gematria comparisons, and numerology calculations before producing an interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may receive misleading astrology, tarot, gematria, or numerology interpretations if the agent fabricates CLI outputs. <br>
Mitigation: Run the thoth CLI first and base interpretations on the returned positions, draws, or calculated values. <br>
Risk: Birth data, names, locations, and personal questions can be sensitive. <br>
Mitigation: Only provide the minimum inputs needed for the requested command and avoid unnecessary retention or sharing of personal details. <br>
Risk: The release depends on installing and trusting a third-party npm package. <br>
Mitigation: Confirm that npm package thoth-cli and publisher aklo360 are the intended package and publisher before installation. <br>
Risk: Optional paid services or wallet-related actions could create unintended financial authority. <br>
Mitigation: Do not grant wallet or payment authority unless the user explicitly requests and understands that behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aklo360/thoth-cli) <br>
- [thoth-cli documentation](https://thothcli.com/skill.md) <br>
- [thoth-cli website](https://thothcli.com) <br>
- [npm package](https://www.npmjs.com/package/thoth-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI result interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent is expected to execute thoth CLI commands before interpreting astrology, tarot, gematria, or numerology outputs.] <br>

## Skill Version(s): <br>
0.2.27 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
