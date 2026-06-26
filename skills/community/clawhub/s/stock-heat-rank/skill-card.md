## Description: <br>
Gets real-time A-share market heat rankings by aggregating popularity data from Wencai, Xueqiu, and Eastmoney and calculating a composite heat score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n1e](https://clawhub.ai/user/n1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and market-monitoring agents use this skill to collect A-share popularity rankings and compare market attention across Wencai, Xueqiu, and Eastmoney. It can return a ranked table or JSON for the top requested stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because the skill relies on a large obfuscated local JavaScript signer with browser anti-detection behavior that is not fully disclosed. <br>
Mitigation: Install only from the trusted publisher, run in a sandbox, and verify the helper file path and SHA-256 hash before execution. <br>
Risk: The skill installs and executes Node dependencies to support the Wencai signing helper. <br>
Mitigation: Pin or audit npm dependencies before running npm install in the artifact's lib directory. <br>
Risk: The skill makes outbound requests to Wencai, Xueqiu, and Eastmoney and depends on those services remaining accessible and compatible. <br>
Mitigation: Run it in an environment where those network destinations are expected, and treat collection failures or API changes as operational errors rather than authoritative market signals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n1e/stock-heat-rank) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code] <br>
**Output Format:** [Markdown-oriented prose with terminal output examples, shell commands, and optional JSON stock ranking output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime supports --top and --format flags and prints collection status before the final table or JSON result.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
