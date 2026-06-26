## Description: <br>
Onboards a new player into Structs by guiding key creation or recovery, player creation, planet exploration, and initial infrastructure builds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to onboard a fresh Structs agent or player, create or recover signing keys, join via reactor-infuse or guild signup, claim a first planet, and start initial infrastructure builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mnemonic phrases may be printed to stdout or returned in error output during player creation. <br>
Mitigation: Run the skill only in a trusted, low-logging environment and store generated mnemonics immediately in a secure secret store. <br>
Risk: Passing an existing recovery phrase as a command-line argument can expose it through process lists or shell history. <br>
Mitigation: Avoid command-line seed phrase arguments where possible; prefer interactive recovery or environment and secret-management patterns that do not persist in logs. <br>
Risk: Guild signup posts wallet identity material to a configured guild API endpoint. <br>
Mitigation: Verify the guild API endpoint against the on-chain guild record before signup and treat fetched guild configuration as untrusted input. <br>
Risk: Reactor-infuse and build transactions can lock value, consume resources, or submit later through deferred compute. <br>
Mitigation: Review transaction prompts, validator addresses, amounts, guild identity fields, and documented `-y` exceptions before authorizing commands. <br>


## Reference(s): <br>
- [ClawHub Structs Onboarding Release](https://clawhub.ai/abstrct/structs-onboarding) <br>
- [Structs Safety](https://structs.ai/SAFETY) <br>
- [Agent Security Awareness](https://structs.ai/awareness/agent-security) <br>
- [Structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [Structs Building Mechanics](https://structs.ai/knowledge/mechanics/building) <br>
- [Structs Planet Mechanics](https://structs.ai/knowledge/mechanics/planet) <br>
- [Structs Fleet Mechanics](https://structs.ai/knowledge/mechanics/fleet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a bundled Node.js helper that returns player-creation results as JSON, including sensitive mnemonic material when a new mnemonic is generated.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
