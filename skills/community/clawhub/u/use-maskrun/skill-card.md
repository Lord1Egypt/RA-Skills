## Description: <br>
Use Maskrun guides agents to wrap secret-prone shell commands with `maskrun --` so stdout and stderr are filtered before they reach logs or transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctxinf](https://clawhub.ai/user/ctxinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before running commands that may print credentials, environment variables, API keys, or other sensitive values. It helps reduce accidental exposure in terminal output, logs, and transcripts while preserving the wrapped command's normal behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat output masking as a sandbox or credential-access control. <br>
Mitigation: Use maskrun only to reduce accidental stdout and stderr exposure; review commands separately for file, network, and credential access. <br>
Risk: Secrets can remain unmasked if the relevant environment variable names are not covered by maskrun configuration. <br>
Mitigation: Configure exact, glob, or regex masking rules for the secret variable names used by the project before running sensitive commands. <br>
Risk: Installing a command wrapper from an untrusted source can introduce supply-chain risk. <br>
Mitigation: Install maskrun only from a trusted source and verify the tool before using it with sensitive commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ctxinf/use-maskrun) <br>
- [agent-env-guard repository](https://github.com/ctxinf/agent-env-guard) <br>
- [agent-env-guard latest release](https://github.com/ctxinf/agent-env-guard/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and TOML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advises output masking only; it does not sandbox child commands or prevent network, file, or credential access.] <br>

## Skill Version(s): <br>
0.1.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
