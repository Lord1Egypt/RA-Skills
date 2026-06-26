## Description: <br>
Analyzes YouTube videos by synchronizing transcript text with extracted visual frames to produce summaries, step-by-step guides, and technical analyses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdrabent](https://clawhub.ai/user/sdrabent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, educators, and content analysts use this skill to understand YouTube tutorials, demos, HowTo videos, and explainers where spoken narration and on-screen visuals both matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads YouTube transcript and video data into a temporary local working directory for frame and transcript analysis. <br>
Mitigation: Run it only for videos the user is allowed to access, keep downloads in a temporary directory, and remove the working directory after analysis. <br>
Risk: Using browser cookies for restricted videos can involve the user's logged-in browser state. <br>
Mitigation: Avoid --cookies-from-browser unless the user deliberately authorizes it for a specific video. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with timestamped sections and inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transcript excerpts, frame descriptions, audio/visual synchronization notes, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
