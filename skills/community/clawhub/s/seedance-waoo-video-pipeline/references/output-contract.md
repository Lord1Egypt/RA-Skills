# Output Contract

## Purpose

This document defines canonical input/output shapes between pipeline steps.

## Resolved Clip Context

```json
{
  "projectId": "",
  "episodeId": "",
  "panelId": "",
  "panelIndex": 0,
  "imageUrl": "",
  "videoPrompt": "",
  "subtitleText": "",
  "existingVideoUrl": "",
  "isMainClip": true,
  "stateLabel": "first-image-direction-approved|image-approved"
}
```

## Video Task Output

```json
{
  "taskId": "",
  "status": "queued|processing|success|fail",
  "fileId": "",
  "downloadUrl": "",
  "isProbe": false
}
```

## Audio Output

```json
{
  "ttsAudio": "",
  "ambienceAudio": "",
  "subtitleText": ""
}
```

## Final Delivery Output

```json
{
  "rawVideo": "",
  "subtitledVideo": "",
  "subtitleTtsVideo": "",
  "finalVideo": "",
  "status": "partial|final",
  "formal": true,
  "probe": {
    "input": {
      "file": "",
      "durationSeconds": 0,
      "hasVideo": true,
      "hasAudio": true
    },
    "output": {
      "file": "",
      "durationSeconds": 0,
      "hasVideo": true,
      "hasAudio": true
    },
    "validation": {
      "ok": true,
      "errors": [],
      "warnings": []
    }
  }
}
```

## Delivery Manifest Output

```json
{
  "rawVideo": "",
  "subtitledVideo": "",
  "subtitleTtsVideo": "",
  "finalVideo": "",
  "status": "partial|final",
  "formal": true,
  "notes": [],
  "probes": {
    "rawVideo": {
      "file": "",
      "durationSeconds": 0,
      "hasVideo": true,
      "hasAudio": false
    },
    "finalVideo": {
      "file": "",
      "durationSeconds": 0,
      "hasVideo": true,
      "hasAudio": true
    }
  }
}
```

## Guard Checkpoint Output

```json
{
  "stage": "panel-guard|merge-guard|seedance-four-pack|first-image-approved",
  "status": "pass|stop|confirm",
  "summary": "",
  "reasons": [],
  "nextStep": ""
}
```

Use this structure when a guard is meant to be shown to the user or surfaced as a confirmation checkpoint.
- `pass`: safe to continue automatically
- `stop`: must stop and fix a hard conflict
- `confirm`: can continue only after user confirmation

## Seedance Confirmation Bundle Output

```json
{
  "title": "",
  "topic": "",
  "episode": "E01",
  "files": {
    "intentBrief": "",
    "script": "",
    "assets": "",
    "storyboard": ""
  },
  "previews": {
    "intentBrief": "",
    "script": "",
    "assets": "",
    "storyboard": ""
  },
  "fullText": {
    "intentBrief": "",
    "script": "",
    "assets": "",
    "storyboard": ""
  },
  "userPrompt": "请确认这套正式 Seedance 四件套。未确认前，流程不会继续进入首图/视频生成。"
}
```

Use this bundle when the pipeline must send formal Seedance four-pack content to the user for confirmation before downstream production.

## Naming Guidance

Prefer stable names that make stage and clip identity obvious:
- `video1-raw.mp4`
- `video1-subtitled.mp4`
- `video1-tts.mp3`
- `video1-ambience.mp3`
- `video1-final.mp4`
