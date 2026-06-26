## Description: <br>
Run RoughCut headlessly on macOS to generate Final Cut Pro (FCPXML) rough-cut timeline variants from a talking-head video, local-first with no media upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samerGMTM22](https://clawhub.ai/user/samerGMTM22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Video editors and creator-workflow agents use RoughCut to run local macOS processing for talking-head footage and return Final Cut Pro XML rough-cut variants for import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running RoughCut depends on a configured local repository path, so an unintended or untrusted checkout could execute code the user did not expect. <br>
Mitigation: Install only from a trusted RoughCut repository and confirm repo_root points to the intended local checkout before running. <br>
Risk: Direct video downloads can retrieve untrusted or unexpected media when a URL is supplied. <br>
Mitigation: Prefer local video files for sensitive recordings; when using a download URL, use trusted HTTPS links and provide video-sha256 when available. <br>
Risk: Fluff removal can use Gemini-based analysis, which may send derived video content outside the local machine. <br>
Mitigation: Keep fluff removal disabled for sensitive recordings unless the user approves Gemini use and understands how GEMINI_API_KEY is handled. <br>


## Reference(s): <br>
- [RoughCut repository](https://github.com/samerGMTM22/OpenClaw-RoughCut) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON result paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the path to a RoughCut.xml_variants.zip file, the input video path, and optional debug output on failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
