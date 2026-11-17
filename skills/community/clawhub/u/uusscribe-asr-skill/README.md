# UUScribe ASR Skill

Use [UUScribe](https://scribe.uustudio.cc) to transcribe a local audio file or a public, single-video YouTube URL from a compatible agent. The skill includes a Python standard-library client; no Python packages are needed.

## Requirements

- Python 3.9 or newer and network access.
- A UUScribe account with API access and available transcription allowance. Create an API key in the UUScribe website under Settings → API Keys.
- Set `UUSCRIBE_API_KEY` in the agent process environment. The script does not read `skill.env` automatically. Never put a real key in this repository or in a chat message.
- For local audio, install `ffprobe` (part of FFmpeg). A public YouTube URL does not need it.

## Install and use

Install this skill from GitHub with `npx skills add yoyostudio209/uusscribe-asr-skill`. The `SKILL.md` file contains the agent workflow and safety rules. You can also run the bundled client directly:

```bash
python3 scripts/transcribe.py 'https://www.youtube.com/watch?v=VIDEO_ID' --submit-only
python3 scripts/transcribe.py --task-id TASK_ID --output transcript.json
python3 scripts/transcribe.py /path/to/audio.mp3
```

Use the returned task ID to resume an existing task. Submitting the same source again can create another billable task. UUScribe charges or consumes allowance according to the user's account and plan; installing this skill is free.

## License

The files in this repository are licensed under MIT-0. The UUScribe service and its account terms are separate.
