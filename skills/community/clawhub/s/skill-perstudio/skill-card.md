## Description: <br>
Studio-grade AI image and video generation for photorealistic portraits, product shots, stickers, animations, and related media from natural-language prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[montenegronyc](https://clawhub.ai/user/montenegronyc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate, transform, upscale, animate, and synthesize media through Perstudio from natural-language requests and optional uploaded inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation requests require a Perstudio API key and can consume paid Perstudio tokens. <br>
Mitigation: Use a dedicated API key where possible, monitor token usage, and check balance before running high-cost media generation. <br>
Risk: Uploaded images, masks, voice references, or other media are sent to Perstudio for processing. <br>
Mitigation: Upload only media you are comfortable sending to Perstudio, and rely on the documented upload directory allowlist to limit accidental file exposure. <br>
Risk: The skill depends on the third-party Perstudio service and perstudio-openclaw npm package. <br>
Mitigation: Install only if you trust Perstudio and the package publisher, and review the open-source package before deployment when required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/montenegronyc/skill-perstudio) <br>
- [Perstudio homepage](https://perstudio.ai) <br>
- [Perstudio OpenClaw repository](https://github.com/montenegronyc/perstudio-openclaw) <br>
- [perstudio-openclaw npm package](https://www.npmjs.com/package/perstudio-openclaw) <br>
- [Perstudio pricing](https://perstudio.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Generated media, API responses, Configuration guidance] <br>
**Output Format:** [Perstudio action calls and JSON-like responses, including generated image, video, audio, balance, and uploaded asset results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PERSTUDIO_API_KEY or plugins.entries.perstudio.config.apiKey; generation consumes Perstudio tokens.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
