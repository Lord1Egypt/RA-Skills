## Description: <br>
TELOS helps an agent initialize, read, update, and back up a user's local personal life framework so advice can reference missions, goals, beliefs, challenges, and related context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sauldataman](https://clawhub.ai/user/sauldataman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use TELOS to create and maintain a local personal context workspace for life planning. The skill lets an agent tailor advice and updates around the user's stated missions, goals, beliefs, priorities, and related life context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can maintain and consult a local personal life profile that may contain sensitive goals, beliefs, health, trauma, or relationship information. <br>
Mitigation: Confirm which TELOS directory is active, keep secrets and highly sensitive health or trauma details out unless the user accepts the privacy risk, and review local files and backups regularly. <br>
Risk: Installing the optional hook can automatically inject personal TELOS context into sessions. <br>
Mitigation: Install the hook only after explicit opt-in, and use the default on-demand mode when automatic context injection is not desired. <br>
Risk: The security evidence reports that restore and restore-file commands can write outside the intended TELOS area if invoked with crafted inputs. <br>
Mitigation: Avoid restore and restore-file commands until path validation is fixed, and review any backup or restore command before execution. <br>


## Reference(s): <br>
- [TELOS onboarding guide](references/onboarding.md) <br>
- [TELOS update workflow](references/update-workflow.md) <br>
- [Daniel Miessler Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local Markdown file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update local TELOS Markdown files and run Bun scripts when triggered by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
