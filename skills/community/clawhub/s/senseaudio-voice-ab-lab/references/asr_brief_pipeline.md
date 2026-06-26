## AudioClaw ASR brief intake

Use this when a marketer, sales lead, or content producer records a spoken brief instead of typing one.

Official findings confirmed from AudioClaw-aligned sources:

- The public site exposes a speech recognition workspace at `/workspace/speech-recognition`.
- The official HTTP API endpoint is `POST https://api.senseaudio.cn/v1/audio/transcriptions`.
- Official open API models are `sense-asr-lite`, `sense-asr`, `sense-asr-pro`, `sense-asr-deepthink`.
- Open API request fields include `file`, `model`, optional `language`, and optional `response_format`.
- Official open API `response_format` supports `json` and `text`.
- The official HTTP API page states a `10MB` file limit.
- The workspace frontend also posts to `/audio/transcriptions` on `https://platform.senseaudio.cn/api`.
- The web page shows an estimated ASR cost of `30 * durationInSeconds` points.

Model choice for this skill:

- Default to `sense-asr-deepthink`.
- Reason: this skill ingests spoken briefs, which are often messy and conversational; in real testing it returned the cleanest transcript shape for downstream field extraction.

Recommended spoken brief format for reliable parsing:

`活动名：春季保温杯测款。产品：316不锈钢保温杯。人群：早八通勤女生。卖点：一键开盖，轻，保温八小时。优惠：第二件半价。行动：点进来看看适不适合你。证明：已经卖了三万单。`

Pipeline:

1. Run `scripts/senseaudio_asr.py` on the audio file.
2. Run `scripts/extract_spoken_brief.py` on the transcript JSON.
3. If `missing_fields` is empty, feed the resulting brief JSON to `scripts/build_voice_ab_variants.py --brief-json ...`.
4. Synthesize all variants with one fixed `voice_id`.
