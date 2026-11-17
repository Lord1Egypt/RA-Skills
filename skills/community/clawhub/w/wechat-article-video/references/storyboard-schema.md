# Storyboard And Timeline Schema

## Storyboard

Use this shape for `storyboard.json`:

```json
{
  "version": 2,
  "title": "本期推荐｜示例药企入驻行业平台",
  "mode": "compact-standard",
  "renderer": "hyperframes",
  "canvas": {"width": 1080, "height": 1920, "fps": 30},
  "voice": {
    "provider": "edge-tts",
    "name": "zh-CN-XiaoxiaoNeural",
    "rate": "+18%"
  },
  "required_disclaimer": "仅供医学人士学习、交流使用，不具有任何商业用途",
  "scenes": [
    {
      "id": "s00",
      "type": "cover",
      "layout": "cover",
      "narrative_job": "首帧说明本期企业和两款重点产品",
      "source_refs": ["title"],
      "caption_entries": [],
      "headline": "示例药企入驻行业平台",
      "supporting_text": "携产品甲、产品乙重点品种",
      "focal_asset": "source/images/company.jpg",
      "secondary_assets": [
        "source/images/eye-drops.jpg",
        "source/images/gel.jpg"
      ],
      "asset_fit": "cover",
      "asset_width_pct": 78,
      "first_meaningful_sec": 0,
      "motion": "still-then-slow-push"
    },
    {
      "id": "s01",
      "type": "company",
      "layout": "company-profile",
      "narrative_job": "建立企业资质和领域积累",
      "source_refs": ["section-1-paragraph-1", "section-1-paragraph-2"],
      "caption_entries": [1, 2, 3],
      "headline": "示例药企",
      "facts": ["成立于2001年", "注册资本5,000万元", "长期专注重点领域"],
      "focal_asset": "source/images/company.jpg",
      "asset_fit": "cover",
      "asset_width_pct": 100,
      "first_meaningful_sec": 0,
      "motion": "image-hold-fact-reveal"
    }
  ]
}
```

## Required Top-Level Fields

- `version`: must be `2`
- `mode`: `brief`, `compact-standard`, `standard`, or `detail`
- `renderer`: `hyperframes` or `remotion`
- `canvas`: default 1080x1920 at 30 fps
- `voice.provider`: must default to `edge-tts`
- `scenes`: ordered scene list

## Required Scene Fields

- `id`
- `type`
- `layout`
- `narrative_job`
- `source_refs`
- `caption_entries`
- `headline`
- `first_meaningful_sec`
- `motion`

`caption_entries` are one-based subtitle entry numbers. The cover usually has no caption entry and receives its duration from `scene-map.json`.

`focal_asset` must be one verified project-relative path string. Put additional verified path strings in `secondary_assets`. Do not put asset candidates, selection rules, or placeholder IDs into these fields; make those decisions during content briefing.

## Scene Map

Use this input for `subtitles_to_timeline.py`:

```json
{
  "cover": {
    "id": "s00",
    "duration_sec": 1.5
  },
  "scenes": [
    {"id": "s01", "caption_start": 1, "caption_end": 3},
    {"id": "s02", "caption_start": 4, "caption_end": 5},
    {"id": "s03", "caption_start": 6, "caption_end": 7},
    {"id": "s04", "caption_start": 8, "caption_end": 9},
    {"id": "s05", "caption_start": 10, "caption_end": 11}
  ]
}
```

Caption ranges must be contiguous, ordered, non-overlapping, and cover every narration caption exactly once.

## Timeline

The generated `timeline.json` contains:

```json
{
  "version": 2,
  "audio_start_sec": 1.5,
  "audio_duration_sec": 69.519,
  "total_duration_sec": 71.819,
  "captions": [
    {"index": 1, "start_sec": 1.6, "end_sec": 8.264, "text": "字幕"}
  ],
  "scenes": [
    {"id": "s00", "start_sec": 0, "end_sec": 1.5, "duration_sec": 1.5},
    {"id": "s01", "start_sec": 1.6, "end_sec": 36.357, "duration_sec": 34.757}
  ]
}
```

Renderers use the generated numbers directly. Do not maintain a second hand-authored timing table in HTML or TypeScript.

## Critical Claim Coverage

When `content-brief.json` declares `critical_claim_ids`, every referenced claim must exist in `claims`, and that claim's `source_ref` must appear in at least one storyboard scene. This is mandatory for `compact-standard`.

Use scene text hierarchy to decide whether a critical claim is narrated or only displayed. Coverage does not mean every critical claim must be spoken.

## Renderer Adapters

HyperFrames uses timeline seconds directly:

- scene clip `data-start` and `data-duration`
- root `data-duration = total_duration_sec`
- voiceover `<audio>` as a direct root child at `audio_start_sec`
- caption clips from each caption's `start_sec` and `end_sec`

Remotion converts timeline values at the adapter boundary:

```ts
const toFrame = (seconds: number, fps: number) => Math.round(seconds * fps);

const remotionCaptions = timeline.captions.map((caption) => ({
  text: caption.text,
  startMs: Math.round(caption.start_sec * 1000),
  endMs: Math.round(caption.end_sec * 1000),
  timestampMs: null,
  confidence: null,
}));
```

Do not recalculate timing from narration character counts inside either renderer.
