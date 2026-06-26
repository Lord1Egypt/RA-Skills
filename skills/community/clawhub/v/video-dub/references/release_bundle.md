# Release Bundle Layout

This skill is meant to be published together with the pipeline code that it drives.

## Recommended layout

```text
video-dub-clawhub/
  SKILL.md
  agents/
    openai.yaml
  references/
    troubleshooting.md
    release_bundle.md
  video_pipeline/
    scripts/
      quick_deliver.py
      download.py
      prepare_video.py
      extract_audio.py
      transcribe.py
      enrich_subtitles.py
      dub_video.py
      retime_video.py
      add_subtitles.py
      services/
    requirements.txt
    data/
      channel_rules.json
      proper_nouns.json
```

## Exclude from the release bundle

Do not include generated outputs or caches:

- `data/raw/`
- `data/covers/`
- `data/processed/`
- `data/audio/`
- `data/subs/`
- `data/structured/`
- `data/tts/`
- `data/dubbed_audio/`
- `data/subtitles/`
- `data/output/`
- `data/state/`

## Runtime expectation

The skill assumes the pipeline root is available locally and that `quick_deliver.py` is the main controller.

If the release is meant to be portable, document the pipeline root as a configurable local path or as a repository checkout that the user can place alongside the skill folder.

