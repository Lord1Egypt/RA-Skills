## Description: <br>
Aligns columns in plain text tables using specified or auto-detected delimiters for improved readability and consistent spacing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analysts use this skill to reformat delimiter-separated text, logs, and CSV-like data into aligned columns for easier reading and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Piped input may fail until the stdin seek behavior is fixed. <br>
Mitigation: Prefer direct file input or test stdin handling in the target environment before relying on piped workflows. <br>
Risk: Server-resolved import provenance is unavailable for this version. <br>
Mitigation: Review the publisher profile and release metadata before using the skill in provenance-sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/txt-col-align) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The formatter reads a file path or stdin and writes aligned column text to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
