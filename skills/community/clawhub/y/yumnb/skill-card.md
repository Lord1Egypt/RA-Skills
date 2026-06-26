## Description: <br>
Yum NoteBook turns a URL, YouTube video, screenshot, or raw text into a local notebook folder with source material, an AI summary, a dual-host audio recap, a slide deck, and optional delivery links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumyumtum](https://clawhub.ai/user/yumyumtum) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, knowledge workers, and agent users use this skill to capture a supplied source into an inspectable local notebook package with notes, audio, slides, and optional sharing. It is suited for study notes, article and video recaps, meeting-ready decks, and reusable local knowledge libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private source material may be sent to external AI, upload, webhook, text-to-speech, or chat delivery services when those integrations are enabled. <br>
Mitigation: Review config.yaml before use and keep upload.provider, notify.webhook_url, deliver.provider, and external AI providers disabled for private material unless outbound sharing is intended. <br>
Risk: User-configurable commands and helper paths can run local programs under the user's account. <br>
Mitigation: Use only trusted values for ai.cli.command, --fetcher, rclone_bin, deliver.openclaw.binary, and upload.onedrive_graph.uploader_path. <br>
Risk: Dependency drift may introduce avoidable security or reliability issues. <br>
Mitigation: Install current patched dependencies or use a lockfile for safer deployments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yumyumtum/yumnb) <br>
- [rclone Documentation](https://rclone.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Audio, Presentation] <br>
**Output Format:** [Local notebook folder containing source files, summary.md, talkshow.txt, talkshow.mp3, deck.json, deck.pptx, and links.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External AI, upload, webhook, and chat delivery integrations are optional and controlled by user configuration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and RELEASE_NOTES_v0.1.1.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
