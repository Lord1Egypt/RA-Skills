## Description: <br>
AI/DevOps 유튜브 숏츠 자동 생성. 트렌드 수집 → 스크립트 → 이미지 → Veo 영상 → TTS 나레이션 → Remotion 합성 → YouTube 업로드 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangjjang](https://clawhub.ai/user/kangjjang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, developer advocates, and automation-focused teams use this skill to generate Korean YouTube Shorts about AI or DevOps topics, from trend collection through script, media, narration, final video, SEO metadata, and upload preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to download and run mutable external code. <br>
Mitigation: Audit the linked repository, setup script, dependencies, uploader, and credential storage before use; run it first in an isolated workspace or VM. <br>
Risk: The workflow can upload generated videos to YouTube with under-declared credential and control requirements. <br>
Mitigation: Review Google OAuth files and uploader behavior, keep uploads private by default, and require manual confirmation before upload. <br>
Risk: Paid Gemini and Veo generation may incur cost. <br>
Mitigation: Require manual confirmation before any paid generation and review the expected per-video cost before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kangjjang/youtube-shorts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated media or metadata files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY plus python3 and node; generated artifacts may include scripts, frames, clips, narration audio, a final MP4, and SEO metadata.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
