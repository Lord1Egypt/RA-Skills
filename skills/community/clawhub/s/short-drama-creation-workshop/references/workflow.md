# Short drama workshop

The bible and the beat sheet are free. Lock them before any still.

## Bible

Write three layers, and keep permanent facts apart from one beat's state.

- Character: age range, face, hair, wardrobe, accessories, posture, and the voice note. A ring that identifies someone is permanent. A rain-soaked coat belongs to one beat.
- Location: layout, entrances, materials, light, and where people stand.
- Prop: anything the ending needs. Note who holds it and when the audience first sees it.

## Beat sheet

Six to eight beats. Each row has one dramatic job (establish, reveal, react, shift power, act, or land), the anchors to carry, the 9:16 framing, the spoken line, and a duration. Faces and props stay large enough for a phone. The first beat is the hook.

## Stills

Upload a supplied photo with `python3 scripts/mcp_client.py upload <path> --mime-type <exact MIME>` and pass the returned artifact. Never send a local path to a remote tool.

The first reference with no photo:

```json
{"prompt": "<permanent character or location>", "canvas": {"type": "preset", "tier": "2K", "aspect": "9:16"}, "count": 1, "client_request_id": "opaque-ref-id"}
```

Call `beatra.images.generate` only for that first reference. Every later still is `beatra.images.transform`. Pass the accepted character and location artifacts, in that order, at most four. Change the action and the framing, and leave the identity words alone.

One wrong still is one `beatra.images.edit` on that artifact: correct the face, wardrobe, or prop, and keep the rest. Then stop.

## Voice and bed

`beatra.voices.list` is free. Freeze one ready voice id per speaker on the materials card and reuse it. A clone is a separate card, `consent_attested` true, and only for a sample the user has the rights to.

Each line is one `beatra.speech.synthesize` with that speaker's `voice_id`. The bed is one instrumental `beatra.music.generate`.

## Motion

Wait for the video card. For a beat with a line, read `image_to_video` and keep a model whose combinations admit `[image, driving_audio]`. Set `duration` to the smallest whole second at or above the real line. Omit `aspect_ratio`.

```json
{
  "image": {"type": "artifact", "artifact_id": "art_beat_still"},
  "driving_audio": {"type": "artifact", "artifact_id": "art_line"},
  "model": "<the admitted model>",
  "prompt": "<one motion that keeps the framing>",
  "duration": 4,
  "client_request_id": "opaque-shot-id"
}
```

A silent beat omits `driving_audio` and may use `model` `auto`. An accepted end frame uses `beatra.videos.interpolate` instead. Character plus location references and no opening still use `beatra.videos.generate_from_references`.

## The cut

After every moving shot has succeeded, one `beatra.videos.compose`. No card and no charge; it was named on the video card. At most 12 clips and 120 seconds. Each clip keeps its own sound (`keep_audio` true) because the line is already inside it. Do not pass `narration` again. Music `volume` is 0.25. Canvas `9:16`. Subtitles are the lines.

```json
{
  "clips": [
    {"source": {"type": "artifact", "artifact_id": "art_hook"}, "start": 0, "end": 4.0, "keep_audio": true},
    {"source": {"type": "artifact", "artifact_id": "art_turn"}, "start": 0, "end": 5.0, "keep_audio": true},
    {"source": {"type": "artifact", "artifact_id": "art_land"}, "start": 0, "end": 4.0, "keep_audio": true}
  ],
  "music": {"source": {"type": "artifact", "artifact_id": "art_bed"}, "volume": 0.25},
  "subtitles": [{"start": 0.0, "end": 4.0, "text": "<hook line>"}],
  "canvas": "9:16",
  "client_request_id": "opaque-cut-id"
}
```

If a clip came back shorter than its span, deliver the parts and name the shot to redo. One redo is a new card and a new id.

## Worked episode

Premise: a night-shift nurse finds her own name on tomorrow's surgery list. Permanent anchors: short black hair, navy scrubs, a cracked watch. The rain starts only in beat 4.

Six beats. Picture all six from the nurse still and the ward still. Move three: the hook (the list), the turn (she hides the watch), the landing (she clocks in). Three lines, one bed, one 9:16 cut. The other three beats stay stills in the delivery.
