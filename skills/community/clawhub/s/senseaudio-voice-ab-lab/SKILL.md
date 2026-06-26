---
name: senseaudio-voice-ab-lab
description: Use when a team wants to generate multiple ad, spoken-copy, sales, or promo voice variants from one typed or spoken creative brief, transcribe voice memos with AudioClaw ASR, and synthesize the variants with the same AudioClaw voice_id for A/B testing, regional wording experiments, or rapid commercial validation.
---

# AudioClaw Voice AB Lab

## What this skill is for

This skill is for commercial teams who need to test **which spoken script performs best**, while keeping the **same voice** across all variants.

That matters because otherwise too many variables change at once:

- copy
- tone
- rhythm
- voice persona

This skill keeps the voice fixed and lets you vary:

- ad tone
- hook style
- urgency level
- trust level
- conversational warmth
- regional wording style

## Best business scenarios

### 1. Short-video ad hooks

Generate 4 to 8 spoken openers for the same product:

- trust-first
- benefit-first
- urgency-first
- concise-direct

Then synthesize all of them with the same voice for fast creative screening.

### 2. Livestream and promo voiceovers

Use the same host-like voice to test:

- stronger urgency
- softer recommendation
- more premium wording
- more sales-driven wording

### 3. Sales or private-domain follow-up

Generate multiple voice-note versions for:

- reopening a lead
- reminding a customer
- sending a soft CTA
- reducing pushiness while keeping conversion intent

### 4. Regional wording experiments

This skill can generate **regional phrasing styles** for comparison, while keeping the same voice.

Important:
- this is **wording-level regional style**, not guaranteed full dialect TTS
- it is useful for testing “which phrasing feels closer to the target audience”

## Workflow

1. Start from either:
   - a typed campaign brief
   - or a spoken voice memo that follows labeled fields such as `产品 / 人群 / 卖点 / 优惠 / 行动`
2. If the input is audio, run `scripts/senseaudio_asr.py`, then `scripts/extract_spoken_brief.py`.
3. If the input is already typed and structured enough, run `scripts/run_typed_brief_pipeline.py` directly, or call `scripts/build_voice_ab_variants.py` yourself.
4. Run `scripts/build_voice_ab_variants.py` to generate variants.
5. Pick one fixed `voice_id`.
   - If you have already created a cloned voice on the AudioClaw platform, use that cloned `voice_id`.
   - A prepared cloned voice id commonly looks like `vc-...`, and can be passed directly with `--clone-voice-id`.
   - If not, use one validated system voice.
6. If you want faster perceived processing for spoken briefs, enable stream ASR in `scripts/senseaudio_asr.py` or `scripts/run_spoken_brief_pipeline.py`.
7. Run `scripts/batch_tts_variants.py` to synthesize every variant with the same voice. This skill already uses AudioClaw streaming TTS under the hood and now records stream chunk metadata.
   - If the chosen voice is a clone id like `vc-...`, the batch TTS step now auto-routes to `SenseAudio-TTS-1.5`.
8. If the user wants to hear the results directly in Feishu or AudioClaw, run `scripts/send_ab_variants_to_feishu.py` after synthesis, or use `scripts/run_spoken_brief_pipeline.py --send-feishu-audio` / `scripts/run_typed_brief_pipeline.py --send-feishu-audio`.
   - This step reuses the previously built Feishu voice-reply path instead of sending plain files.
   - It transcodes the generated `.mp3` variants into `.ogg/.opus` and sends them one by one as real `audio` messages.
9. Review:
   - generated copy
   - estimated points
   - output audio files
   - variant metadata for A/B tracking
   - optional Feishu send results

## AudioClaw Trigger Pattern

Use this skill as an explicit task mode, not as a hidden background guess.

Recommended user trigger:

```text
用 $senseaudio-voice-ab-lab 处理我刚发的语音。
产品：轻量保温杯
人群：通勤上班族
卖点：轻便保温不漏水
优惠：第二件半价
行动：现在点击下单
clone voice_id：your_clone_voice_id
生成 4 条口播，输出到 /tmp/voice_ab_run
```

If the user already sent a voice memo, the agent should:

1. Save the audio locally.
2. Run `scripts/run_spoken_brief_pipeline.py`.
3. Return:
   - a short summary of the extracted brief
   - the output directory
   - the best 2 to 4 audio variants for review

If the user says "一条一条发语音给我听" or "直接发到飞书里试听", the agent should:

1. Run the normal A/B pipeline first.
2. Then run `scripts/send_ab_variants_to_feishu.py`, or add `--send-feishu-audio` to `scripts/run_spoken_brief_pipeline.py`.
3. Prefer sending the variants one by one as Feishu `audio` messages instead of replying with local paths.
4. If the user only wants part of the set, use `--limit` or `--variant-ids`.

If the user gave a typed brief and also says "直接一条一条发语音给我听", the agent should:

1. Extract or confirm these fields:
   - `campaign_name`
   - `product`
   - `audience`
   - `key_message`
   - `cta`
   - optional `offer`
   - optional `proof`
2. Run `scripts/run_typed_brief_pipeline.py`.
3. Add `--send-feishu-audio`.
4. Do not stop at returning local audio paths unless the user explicitly asked for files only.

If the user does not provide a cloned voice, ask for either:

- a prepared clone `voice_id`
- or permission to fall back to a validated system `voice_id`

## Design rules

- Keep each script short enough to test quickly.
- Change one creative dimension at a time if possible.
- For spoken briefs, keep the input structured enough for deterministic extraction.
- For real A/B testing, keep:
  - the same voice
  - the same audio format
  - the same sample rate
  - similar script length
- Treat `regional_style` as a wording choice, not an official dialect model.
- Official clone support is a two-step chain:
  - create the clone on the AudioClaw platform first
  - then pass the prepared clone `voice_id` into this skill for generation

## API key lookup

For the generation side of this skill:

- TTS-oriented scripts now default to `SENSEAUDIO_API_KEY`

Practical rule:
- `scripts/run_spoken_brief_pipeline.py`, `scripts/run_typed_brief_pipeline.py`, and `scripts/batch_tts_variants.py` now default to `SENSEAUDIO_API_KEY`
- If the host app injects `SENSEAUDIO_API_KEY` as a login token such as `v2.public...`, the shared bootstrap replaces it with the real `sk-...` value from `~/.audioclaw/workspace/state/senseaudio_credentials.json` before the synthesis step starts
- The ASR scripts keep their own existing defaults and are intentionally not changed here

## Resources

- `scripts/build_voice_ab_variants.py`
  - Builds an A/B manifest from one campaign brief
- `scripts/senseaudio_asr.py`
  - Calls AudioClaw ASR using either the official open API host or the official platform endpoint
  - Defaults to the official `sense-asr-deepthink` model for spoken briefs
- `scripts/extract_spoken_brief.py`
  - Extracts a structured campaign brief from an ASR transcript
- `scripts/run_spoken_brief_pipeline.py`
  - Runs the full spoken-brief pipeline end to end
  - Supports `--stream-asr`, `--clone-voice-id`, and `--send-feishu-audio`
- `scripts/run_typed_brief_pipeline.py`
  - Runs the full typed-brief pipeline end to end
  - Supports `--clone-voice-id` and `--send-feishu-audio`
- `scripts/batch_tts_variants.py`
  - Generates all audio variants with the same `voice_id`
- `scripts/send_ab_variants_to_feishu.py`
  - Reuses the Feishu voice-reply delivery path to transcode and send the generated variants one by one as audio messages
- `scripts/export_ab_review_csv.py`
  - Produces a review sheet for creative, growth, or Feishu-based internal scoring
- `references/commercial_ab_patterns.md`
  - High-value use cases, testing advice, and regional-style notes
- `references/asr_brief_pipeline.md`
  - Official ASR findings, constraints, and the recommended spoken brief format
