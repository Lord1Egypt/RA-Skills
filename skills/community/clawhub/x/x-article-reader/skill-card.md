## Description: <br>
Read X (Twitter) Articles aloud using macOS text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ewangchong](https://clawhub.ai/user/ewangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to extract text from X Articles and have it read aloud on macOS, with automatic Chinese or English voice selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a reusable X login session inside the skill directory. <br>
Mitigation: Use only on a trusted local machine, restrict access to data/browser_state, and delete the stored browser state when access is no longer needed. <br>
Risk: The article reader opens user-supplied URLs in a logged-in browser session without tight URL safeguards. <br>
Mitigation: Use only intended x.com article URLs and avoid arbitrary or untrusted links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ewangchong/x-article-reader) <br>
- [Homepage](https://github.com/ewangchong/x-article-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal output and optional AIFF audio file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads extracted article text aloud with macOS say; can save audio when an output path is provided.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
