## Description: <br>
Creates automated video podcasts from a topic by guiding research, script writing, TTS audio synthesis, Remotion video composition, background music mixing, subtitles, thumbnails, and final MP4 output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and content teams use this skill to turn a topic into scripted, narrated, rendered video podcast assets for publishing platforms such as YouTube, Bilibili, Douyin, Xiaohongshu, and WeChat Channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports high-impact local actions and unrelated deployment files that need review before installation. <br>
Mitigation: Install only in a disposable or well-backed-up workspace and review bundled files before running skill commands. <br>
Risk: Bundled Onyx deployment files may run a separate Docker-based stack. <br>
Mitigation: Do not run the Onyx deployment assets unless intentionally needed, and avoid granting Docker socket access. <br>
Risk: The workflow can use cloud TTS or search providers and API credentials. <br>
Mitigation: Do not send confidential scripts, prompts, or audio to providers until their data policies are reviewed, and scope credentials to the minimum required. <br>
Risk: The skill may involve update checks, git pulls, process termination, rendering, and cleanup steps. <br>
Mitigation: Confirm before git pulls, process termination, final rendering, or cleanup, and keep intermediate video outputs until reviewed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/agents365-ai/video-podcast-maker) <br>
- [Homepage](https://github.com/Agents365-ai/video-podcast-maker) <br>
- [Design Guide](references/design-guide.md) <br>
- [Workflow Steps](references/workflow-steps.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated project files, Remotion/TypeScript code, TTS assets, subtitle files, thumbnails, and MP4 video outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Remotion project, Python, Node.js, FFmpeg, and optional TTS or thumbnail provider credentials depending on selected backends.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
