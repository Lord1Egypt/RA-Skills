# Video Object Remover for OpenClaw

Remove an unwanted person, object, logo, or distraction from a video through OpenClaw. The Skill submits the video to [Video Object Remover](https://videoobjectremover.com), shows the AI-selected mask for approval, and only starts the final erase after the user confirms.

## Install

Send this to OpenClaw:

```bash
mkdir -p ~/.openclaw/workspace/skills/video-object-remover
curl -sL https://videoobjectremover.com/skills/video-object-remover/SKILL.md -o ~/.openclaw/workspace/skills/video-object-remover/SKILL.md
```

Start a new OpenClaw session after installation so it loads the Skill.

## Connect your account

1. Sign in at [Video Object Remover](https://videoobjectremover.com).
2. Open **My Workspace** and create an API key.
3. Copy the key and send it to OpenClaw. Configure it as `VIDEO_OBJECT_REMOVER_API_KEY`.

Keep the API key private. It can use your Video Object Remover account balance and access your processed jobs.

## Use

Ask OpenClaw to remove one specific target from a local video, for example:

> Remove the woman in the red jacket on the right from `clip.mp4`.

OpenClaw will create a mask preview. Review it and explicitly confirm before it performs the final erase.

## Limits

- MP4, MOV, and WebM up to 100 MB
- One free 5-second watermarked preview for new accounts
- Paid videos up to 60 seconds; each full video uses 10 credits

Only edit videos you own or are authorized to edit. Do not use this tool to impersonate people, misrepresent events, violate privacy, or remove rights information.

## Links

- [Website](https://videoobjectremover.com)
- [OpenClaw setup guide](https://videoobjectremover.com/blog/remove-objects-from-video-with-openclaw)
- [Skill instructions](./SKILL.md)
