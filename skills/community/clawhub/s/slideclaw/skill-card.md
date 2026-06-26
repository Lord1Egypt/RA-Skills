## Description: <br>
Use this for SlideClaw/Marp deck tasks, including creating decks, rendering Marp slides, and saving slide templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akamichikota](https://clawhub.ai/user/akamichikota) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to produce Marp slide decks with SlideClaw, from project setup and requirements capture through HTML/PDF rendering and optional template reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may execute the SlideClaw CLI through a local binary or npx package resolution. <br>
Mitigation: Install and review a trusted or pinned SlideClaw package version before use in stricter environments. <br>
Risk: Rendered slide files may be copied to the operating system Downloads folder. <br>
Mitigation: Use SLIDECLAW_NO_DOWNLOADS=1 or --no-copy-to-downloads when outputs should remain only in the workspace. <br>


## Reference(s): <br>
- [SlideClaw ClawHub Listing](https://clawhub.ai/akamichikota/slideclaw) <br>
- [SlideClaw Homepage](https://github.com/akamichikota/SlideClaw) <br>
- [Akamichi Publisher Profile](https://clawhub.ai/user/akamichikota) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and generated slide project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Marp source files, rendered HTML/PDF outputs, template updates, and durable profile preference updates.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
