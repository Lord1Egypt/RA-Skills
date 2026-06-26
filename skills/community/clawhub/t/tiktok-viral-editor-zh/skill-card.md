## Description: <br>
Helps agents use Sparki to turn source videos into TikTok-style short videos with stronger hooks, faster pacing, and attention-focused edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill when they want an agent to prepare TikTok-style video edits through Sparki. It is suited for short-form video workflows that need prompt-driven editing, uploads, project status checks, and downloaded results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos are uploaded to Sparki for cloud processing. <br>
Mitigation: Use this skill only for videos that are acceptable to process with Sparki, and ask explicitly for local or manual editing when cloud processing is not acceptable. <br>
Risk: The Sparki API key may be saved in the local OpenClaw configuration file. <br>
Mitigation: Prefer SPARKI_API_KEY as an environment variable when the key should not be persisted locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/tiktok-viral-editor-zh) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON command results, and downloaded video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads MP4 or MOV files to Sparki, stores local configuration and project history, and downloads edited MP4 results when projects complete.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter, release evidence, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
