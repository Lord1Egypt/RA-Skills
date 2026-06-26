## Description: <br>
t0cksn1per helps an agent prepare and run Tock reservation sniper commands for timed releases or cancellation watches on a local Mac or remote node. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[murphykobe](https://clawhub.ai/user/murphykobe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to collect restaurant, party size, date, time, and execution preferences, then have an agent prepare and run a single t0cksn1per CLI command for a timed release or cancellation watch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external t0cksn1per CLI package that was not included for review. <br>
Mitigation: Install only if you trust the package, review the exact command before execution, and prefer a visible local browser for first use. <br>
Risk: Remote, headless, or CDP-based polling can continue beyond the intended reservation watch. <br>
Mitigation: Use CDP only with a temporary Chrome profile, and stop any remote or headless polling job when finished. <br>


## Reference(s): <br>
- [Command Examples](references/commands.md) <br>
- [CDP Mode](references/cdp.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one concrete t0cksn1per command and may include CDP setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
