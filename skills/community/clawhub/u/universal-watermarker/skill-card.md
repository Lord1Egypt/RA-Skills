## Description: <br>
Adds customizable text watermarks with adjustable opacity, responsive scaling, color handling, and layout modes to PDFs and common image files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cribug](https://clawhub.ai/user/cribug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to apply visible anti-counterfeiting, confidentiality, or review-status watermarks to batches of PDFs and images while preserving outputs next to the originals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes wm_-prefixed files next to the original PDFs and images, which may place derived files in sensitive directories. <br>
Mitigation: Run it only on intended local files and review the output paths reported after processing. <br>
Risk: Environment setup can download a font from GitHub, creating a supply-chain dependency during setup. <br>
Mitigation: Use an isolated environment for sensitive work and prefer a pinned, pre-reviewed local font path when possible. <br>
Risk: PDFs and images can be untrusted or sensitive inputs. <br>
Mitigation: Process untrusted or confidential files in an isolated workspace with audited dependency versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cribug/universal-watermarker) <br>
- [Publisher profile](https://clawhub.ai/user/cribug) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Python function calls and local files saved with a wm_ filename prefix] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes PDF, JPG, JPEG, PNG, and BMP inputs; writes output files beside the source files.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
