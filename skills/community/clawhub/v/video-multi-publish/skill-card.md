## Description: <br>
One-stop multi-platform video publishing workflow. From video clipping to multi-platform publishing, full process automation. Supports automatic clipping for platform formats, intelligent title optimization, tag recommendation, best publish time recommendation, one-click publishing to WeChat, Bilibili, Xiaohongshu, Douyin, YouTube, TikTok and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earthwalking](https://clawhub.ai/user/earthwalking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and developers can use this skill to prepare platform-specific video clips, generate platform-adapted titles and tags, and coordinate a multi-platform publishing workflow. The provided implementation should be treated as a local ffmpeg clipping and simulated publishing utility unless production publishing safeguards are added. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises real multi-platform publishing and analytics, but the security summary identifies the implementation as a local ffmpeg clipping/demo utility. <br>
Mitigation: Treat it as local clipping and simulated publishing only; do not rely on it for public posting until accurate documentation and production publishing controls are added. <br>
Risk: Public posting workflows can expose platform credentials or publish content unintentionally if authentication, data flow, confirmation, and dry-run behavior are unclear. <br>
Mitigation: Do not provide platform credentials; require clear authentication and data-flow disclosures, per-platform confirmation, and safe dry-run behavior before using it with real accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earthwalking/video-multi-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance, shell command examples, Python API examples, console status text, and generated video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg/ffprobe for video analysis and clipping; publishing behavior in the provided script is simulated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
