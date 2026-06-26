## Description: <br>
Turns ideas, notes, articles, reports, or technical material into X posts or threads with tone matching, character-limit handling, and factual-risk checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, founders, researchers, and content teams use this skill to turn source material into X posts or threads, refine hooks and voice, and decide whether a supporting text/data graphic would help. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use web search on topic text the user provides, which can expose sensitive or private source material if included in the prompt. <br>
Mitigation: Use only the minimum topic text needed for research, avoid credentials or personal data, and keep uncertain or sensitive claims clearly qualified. <br>
Risk: Optional image rendering can install or use Puppeteer and launch local Chrome to turn self-contained HTML/CSS into PNG assets. <br>
Mitigation: Render only trusted, self-contained HTML, keep network assets out of render files, and avoid custom Chrome flags unless they are needed for the local environment. <br>
Risk: Opt-in draft saving can write generated X drafts to a user-selected location. <br>
Mitigation: Save only after explicit opt-in and review the resolved absolute target path before writing. <br>
Risk: Drafted X posts can overstate real-time, financial, legal, medical, political, scientific, or other high-stakes claims if source evidence is incomplete. <br>
Mitigation: Verify current and high-stakes claims when tools are available, state uncertainty plainly, and avoid invented sources, numbers, quotes, screenshots, or firsthand experience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/x-post-strategist) <br>
- [README](README.md) <br>
- [Render Image Setup](render-image-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional code blocks, shell commands, and image briefs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally propose or generate self-contained HTML/CSS graphics and save drafts only after user opt-in.] <br>

## Skill Version(s): <br>
0.14.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
