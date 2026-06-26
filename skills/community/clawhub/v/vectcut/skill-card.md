## Description: <br>
VectCut orchestrates cloud video-editing workflows for talking-head edits, remixes, ads, subtitles, audio, effects, picture-in-picture, AI-generated media, platform video ingestion, rendering, and Feishu workflow handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sun-guannan](https://clawhub.ai/user/sun-guannan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to automate VectCut video-production flows, including draft creation, media upload, subtitle and audio processing, effects, AI image or video generation, cloud rendering, draft download, and Feishu workflow setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires VECTCUT_API_KEY and may expose media, draft IDs, transcripts, prompts, and generated outputs to VectCut cloud services. <br>
Mitigation: Install and run it only where VectCut is trusted for the relevant media and project data; use scoped credentials where available and avoid entering secrets into shared transcripts. <br>
Risk: The Feishu workflow generator can embed the real API key instead of using a placeholder or secure secret binding. <br>
Mitigation: Do not use that workflow generator until the generated workflow stores credentials through a secure secret binding or a placeholder that operators replace outside the prompt. <br>
Risk: Automatic workflows can upload files, mutate drafts, and trigger rendering across private or proprietary media. <br>
Mitigation: Review planned uploads, draft IDs, and mutation steps before broad workflow execution, then verify draft output with query-draft before cloud rendering or distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sun-guannan/vectcut) <br>
- [VectCut homepage](https://www.vectcut.com/) <br>
- [VectCut API documentation index](https://docs.vectcut.com/llms.txt) <br>
- [Query draft API documentation](https://docs.vectcut.com/386764616e0) <br>
- [Cloud render task status documentation](https://docs.vectcut.com/321247406e0) <br>
- [Model capabilities reference](references/model_capabilities.json) <br>
- [AI image model capabilities reference](references/ai-image-model_capabilities.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON payloads, draft identifiers, draft URLs, rendered video URLs, and optional workflow prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or mutate VectCut cloud drafts and may write local JSON or Markdown result files for intermediate reports.] <br>

## Skill Version(s): <br>
1.5.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
