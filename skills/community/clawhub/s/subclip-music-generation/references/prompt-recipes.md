# Instrumental prompt recipes

These are original starting briefs informed by the providers' guides. Adapt tempo, duration arc and density to the actual edit. Say “instrumental, no vocals” and choose instrumental mode. Timing requests are approximate; trim the final asset to fit.

| Use case | Starting brief |
|---|---|
| Product demo / live walkthrough | Optimistic minimal electronic underscore, 105 BPM. Soft synth pulse, muted piano, warm bass and light percussion. Stay steady beneath narration, add a small lift at the feature reveal, and finish cleanly. Sparse midrange, no big drops. |
| SaaS launch / product reveal | Confident modern electronic instrumental, 118 BPM. Rounded synth bass, bright arpeggios, tight kick and restrained claps. Begin with a curious pulse; build in layers toward the reveal, then end on an uplifting resolved chord. |
| Short ad / CTA | Playful indie-pop instrumental, 120 BPM. Plucked guitar, crisp handclaps and bouncy bass. Establish a memorable motif immediately, create a brief lift for the product, leave a short clean landing for the call to action. |
| Talking head / educational explainer | Calm warm ambient instrumental, 80 BPM. Felt piano, soft pads, occasional brushed percussion. Low density, even dynamics, little melodic movement; plenty of space for the speaker. No vocals or dramatic transitions. |
| Explainer short | Clear and curious downtempo instrumental, 98 BPM. Marimba motif, muted synth pulse and light clicks. Immediate gentle groove, subtle accents for the explanation, concise resolving finish. |
| Storytelling / narrative | Intimate cinematic instrumental, 76 BPM. Felt piano and warm low strings. Begin uncertain and sparse, build emotional warmth in the middle, then resolve with a hopeful piano phrase. Avoid overpowering the narrator. |
| Travel vlog / good experience | Sunlit indie-folk instrumental, 104 BPM. Acoustic guitar, hand percussion, warm bass and airy keys. Open and relaxed; a lively lift for the scenic montage, then a soft outro. |
| Sad experience / reflection | Restrained melancholic instrumental, 65 BPM. Sparse felt piano, cello and soft room ambience. Minor-key opening, long pauses and gentle dynamics, ending with quiet acceptance. No epic percussion or sudden climax. |
| Happy memory / celebration | Joyful soul-pop instrumental, 112 BPM. Bright electric piano, finger snaps, buoyant bass and small horn accents. A warm catchy motif, rising energy, satisfying final cadence. |
| Luxury / fashion | Elegant restrained downtempo instrumental, 92 BPM. Clean electric piano, brushed drums and deep warm bass. Spacious production, subtle texture and measured confidence. |
| Focus / coding timelapse | Cozy lo-fi instrumental, 84 BPM. Rhodes chords, soft vinyl texture, gentle bass and relaxed drum groove. Repetitive understated motif with slight variations; no vocals or sharp transitions. |
| Adventure / dramatic reveal | Cinematic orchestral instrumental, 100 BPM. Low strings, measured toms and ascending brass. Quiet anticipation, gradual rise, one clear reveal accent, then a controlled resolution. |

## Lyria image-inspired briefing

Describe the relationship, not merely “music for this picture”: “Use these coastal travel images for a breezy, spacious mood. Acoustic guitar and soft hand percussion at 102 BPM, with a warm sunset outro. Instrumental only.” Up to ten authorized project images may be attached. Images are inspiration, not a guaranteed visual-to-audio synchronization mechanism.

## Lyria timed structure

Approximate cues are supported through descriptive prompting: `[0:00–0:10] sparse pulse; [0:10–0:30] introduce light piano and percussion; [0:30–0:50] uplifting reveal; [0:50–1:00] resolve and fade.` State genre, instruments and vocal intent too. Review and trim the generated track; do not claim exact timestamps or loop-perfect output.

## Official example patterns

Replicate's Lyria examples demonstrate a C-major 140 BPM chiptune instrumental, a dreamy 110 BPM indie-pop song with structured lyrics, and a timed 85 BPM lo-fi arrangement. MiniMax examples demonstrate acoustic custom lyrics, cinematic and lo-fi instrumentals, generated summer-pop lyrics and disco/funk lyrics. Refer to the official examples rather than copying their lyrics into an unrelated user project:
- https://replicate.com/google/lyria-3-pro/examples
- https://replicate.com/minimax/music-2.6/examples

## Refine deliberately

If too busy: fewer instruments, restrained drums, sparse melody, even dynamics. If too flat: specify a controlled build and one payoff. If timing misses: trim/crossfade locally before proposing a paid rerun. If unwanted singing appears: first confirm instrumental mode and explicit no-vocals direction; explain that a new generation costs credits. Do not promise isolated stems, exact song length, deterministic seeds or a guaranteed seamless loop.


## ElevenLabs duration-directed briefs

Start with the scene’s purpose and choose genre, mood, instruments, tempo, and production texture. Describe the arrangement in order. Reserve quiet space explicitly for narration. Send the chosen length in `settings.music_length_ms`, rather than relying on prompt text alone.

- Product launch, 30 seconds (`30000`): “Modern electronic instrumental for a SaaS launch, 112 BPM. Warm synth pulse, muted piano and tight soft percussion. First 8 seconds: sparse curiosity. Add a confident groove for the reveal, then leave a clean ending for the call to action. No vocals; keep the midrange open for narration.”
- Talking head, 60 seconds (`60000`): “Quiet ambient underscore, 78 BPM, felt piano and soft sustained pads. Even dynamics and slow harmonic movement beneath a speaker. No lead melody, voices or dramatic fills. Gentle ending.”
- Travel memory, 45 seconds (`45000`): “Breezy indie-folk instrumental, 102 BPM, acoustic guitar and brushed hand percussion. Start intimate, brighten for the scenic montage, then soften into a warm sunset ending.”
- Sung jingle, 15 seconds (`15000`): Describe language, vocal delivery and musical style in `prompt`; put a short approved two- or four-line hook in `settings.lyrics` with `mode: custom_lyrics`. Do not squeeze a full verse and chorus into five seconds.

Official Replicate examples use “Upbeat electronic dance music” with 5- and 30-second targets, MP3/WAV output, and both instrumental-only and vocals-allowed settings. Vocals-allowed alone is not a guarantee of singing; describe the singer and lyric intent explicitly. Example cards retain the original provider inputs.

Sources: https://replicate.com/elevenlabs/music/examples and https://elevenlabs.io/docs/overview/capabilities/music/best-practices . The native ElevenLabs API has additional features that this Replicate wrapper does not expose.
