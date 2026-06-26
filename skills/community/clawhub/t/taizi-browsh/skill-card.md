## Description: <br>
A modern text-based browser that renders web pages in the terminal using headless Firefox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users use this skill to launch Browsh, open web pages in a PTY-backed terminal browser, and follow setup guidance for required local binaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opening URLs through the terminal browser carries normal browsing risks, including exposure to untrusted sites or sensitive account activity. <br>
Mitigation: Use Browsh and Firefox from trusted sources, keep them updated, and apply normal browser precautions for sensitive or untrusted sites. <br>
Risk: The skill depends on local browsh and firefox binaries, so missing or unexpected binaries can cause failures or unsafe local execution. <br>
Mitigation: Verify the required binaries are installed from trusted sources and that PATH resolves to the expected installations before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-browsh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local browsh and firefox binaries and a PTY-capable terminal session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
