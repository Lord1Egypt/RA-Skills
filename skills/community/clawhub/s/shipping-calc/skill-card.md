## Description: <br>
Calculate shipping costs with zone-based rates and duty estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to estimate shipping rates, compare service levels, estimate dimensional weight, calculate duty, and run simple tracking or batch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted numeric inputs could cause the shell script to run unintended local commands. <br>
Mitigation: Review or patch the script before installation; validate numeric fields and pass values to awk as data rather than executable source. <br>
Risk: Shipping details copied from untrusted messages, files, or websites may trigger unsafe script behavior. <br>
Mitigation: Avoid running the script on untrusted shipping details unless inputs are sanitized first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/shipping-calc) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local data under ~/.local/share/shipping-calc when executed.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
