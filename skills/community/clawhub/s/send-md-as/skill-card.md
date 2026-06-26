## Description: <br>
Render Markdown as polished JPEG, PNG, WebP, or PDF media for messaging apps, with support for code highlighting, LaTeX, Mermaid diagrams, tables, themes, and optional page splitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enc-hanted](https://clawhub.ai/user/enc-hanted) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert Markdown into shareable media for chat channels that do not natively render Markdown. It can produce full single-page images by default, optional paginated images on request, or PDFs for longer content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local renderer processes user-provided Markdown in Chromium and the security summary flags that Chromium compatibility fallback can weaken sandboxing. <br>
Mitigation: Run the skill only for trusted or reviewed Markdown in an isolated environment, and review the rendered output before sharing it. <br>
Risk: Setup installs Python and npm dependencies and may download Chromium or optional rendering tools. <br>
Mitigation: Review setup.sh before running it, pin or mirror dependencies according to local policy, and install in an isolated user or virtual environment. <br>
Risk: The optional message-send command can send generated media to a channel or target selected by the user. <br>
Mitigation: Confirm the channel, target, and generated media file before invoking the send command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/enc-hanted/send-md-as) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/enc-hanted) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [JPEG, PNG, WebP, or PDF files with optional Markdown shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports light, dark, sepia, and nord themes; image page splitting is optional and disabled by default.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
