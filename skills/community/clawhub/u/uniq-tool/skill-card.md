## Description: <br>
Report or filter repeated lines in sorted text for deduplication, frequency counting, and data cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data cleanup workflows use this skill to remove repeated lines from sorted text or count repeated lines in local files or standard input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation lists -d, -u, -i, and output-file behavior, while the included script implements only basic unique-line output and count mode. <br>
Mitigation: Verify the available command-line behavior before relying on those documented options in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/uniq-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text lines or count-prefixed text lines from command-line usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Works best with sorted input. The included script supports basic unique-line output and count mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
