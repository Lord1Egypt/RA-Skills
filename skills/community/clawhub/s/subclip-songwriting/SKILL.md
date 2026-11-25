---
name: subclip-songwriting
description: Write or adapt original lyrics and generate sung music in Subclip using MiniMax Music 2.6, Google Lyria 3 Pro or ElevenLabs Music. Use for songs, sung hooks, jingles, custom lyrics, generated lyrics, vocal language/style and verse/chorus structure; not spoken narration or instrumental background beds.
---

# Lyrics and songs

Read `$subclip-music-generation` for discovery, authorization, async generation, storage and importing. Read [song recipes](references/song-recipes.md) before drafting. Lyrics are distinct from the music description; speech synthesis is not song generation.

Default to **Google Lyria 3 Pro** (`modelId: "lyria-3-pro"`) for all music and song generation. Switch to another music model only when the user explicitly requests that model or asks to switch. Do not switch automatically for duration, output format, cost, lyrics, or after a failure. If Lyria cannot meet a requirement or is unavailable, explain the limitation and ask which model the user wants before generating with another model.

1. Identify purpose, language, lyrical theme, audience, approximate length, genre, mood, tempo, vocal character and the required brand/product words. Ask only for material missing choices. Preserve user-supplied lyrics unless editing is requested.
2. If asked only to write lyrics, deliver a draft and stop without spending generation credits. Draft concise singable lines, a memorable hook, consistent perspective and an intentional emotional progression. Prefer natural phrasing over forced rhyme. Bracket section headings such as `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`; keep production instructions in the prompt.
3. Choose `settings.mode: custom_lyrics` and put lyrics in `settings.lyrics` when the user supplied or approved exact words. For `auto_lyrics`, describe the theme and language in prompt and explain that exact wording is generated. Do not silently replace approved custom lyrics with automatic lyrics.
4. Match live model limits:
   - MiniMax: prompt ≤2,000 characters; custom lyrics ≤3,500 characters. The adapter uses `lyrics`, `is_instrumental: false`, `lyrics_optimizer: false` for custom lyrics. Auto mode uses `lyrics_optimizer: true`; instrumental mode is not for songs. No seed/images.
   - Lyria: the adapter composes music direction and a marked lyrics section into `prompt`. No standalone provider lyrics field. Optional seed and up to ten authorized image references. Use the catalog for current application limits.
   - ElevenLabs: choose `music_length_ms` (5,000–300,000) and an `output_format` preset. The adapter appends custom lyrics to the description and disables `force_instrumental`. Combined description, lyrics and added instructions must fit 4,100 characters. Keep lyrics short enough to sing at the chosen tempo and target length. Auto mode requests original lyrics but does not promise exact words. No composition-plan JSON or isolated stems via this tool.
5. Before generating, verify exact lyrics and requested language, required text, vocal direction, model and live credit estimate against the user's request. If these are already authorized, call `generate_music` once with `confirmed: true`. Otherwise present the prepared draft and concrete choices for confirmation.
6. End the in-app turn after acceptance; use the operation ID when resumed. Review the result before claiming words, pronunciation, exact duration or musical cues are correct. For revisions, explain the changed words/direction and new generation cost; never silently overwrite the original song.

## Example

```json
{"confirmed":true,"modelId":"lyria-3-pro","prompt":"An original uplifting indie-pop jingle in English at 112 BPM. Clear warm lead vocal, acoustic guitar, handclaps and rounded bass. Intimate verse, brighter memorable chorus, short clean ending. Sing the supplied lyrics.","settings":{"mode":"custom_lyrics","lyrics":"[Verse]\nOne small spark, a place to start\nMake a little room for art\n[Chorus]\nTake the thought and let it shine\nBuild a brighter day, one line at a time\n[Outro]\nOne small spark, a place to start"}}
```

Do not claim output licenses, monetization eligibility or exclusive ownership without applicable evidence. This workflow does not clone a singer, guarantee exact pronunciation, return separate stems or publish the song.

References: [ElevenLabs prompting](https://elevenlabs.io/docs/overview/capabilities/music/best-practices), [ElevenLabs Replicate schema](https://replicate.com/elevenlabs/music/api/schema), [MiniMax Music 2.6](https://replicate.com/minimax/music-2.6), [Lyria 3 Pro](https://replicate.com/google/lyria-3-pro), [Google's lyric/vocal prompting guidance](https://deepmind.google/models/lyria/prompt-guide/).
