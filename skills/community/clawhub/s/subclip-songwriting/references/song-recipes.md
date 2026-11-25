# Writing for sung output

Use a short musical brief and separate lyrics. Specify vocal language, clear diction, approximate register/timbre and emotional delivery when relevant. A brief like “warm conversational alto, close and understated verse, open confident chorus” is more actionable than “great vocals.” For Lyria, parentheses can suggest backing echoes; treat this as creative direction, not guaranteed arrangement control.

| Song purpose | Structure and lyrical direction | Music direction |
|---|---|---|
| Product launch jingle | Two-line problem/setup → four-line benefit hook → short brand landing. Use only supplied product claims. | Bright indie pop, 110–120 BPM, warm clear lead, guitar and claps, a memorable chorus. |
| SaaS ad | Start with the useful outcome, repeat a concise original hook, end on the authorized product name. | Modern electro-pop, 105–115 BPM, clean vocal, restrained synths and punchy drums. |
| Story / travel memory | Verse describes one concrete place/moment; chorus carries the feeling; second verse adds a change. | Acoustic folk-pop, 95–105 BPM, intimate verse and open warm chorus. |
| Sad experience | First-person concrete images, short breathing spaces, emotional movement toward acceptance. | Piano ballad, 65–80 BPM, restrained lead and gentle strings, no exaggerated climax. |
| Celebration / happy experience | A small detail in the verse, collective joyful hook, brief repeating outro. | Soul-pop or disco, 110–125 BPM, bright harmony and buoyant bass. |
| Educational sung hook | One accurate idea, simple repeated mnemonic, no added factual claims. | Playful light pop, clear diction, sparse accompaniment, moderate pace. |

## Three different modes

- **Instrumental**: no lyrics and no vocals. Route to background-music skill.
- **Custom lyrics**: the exact approved words go in `settings.lyrics`. Do not rely on the provider to invent missing required copy.
- **Generated lyrics**: request theme, language, tone and structure in prompt. The words are not approved in advance; tell the user if exact wording is important and choose custom lyrics instead.

## Small revisions

For awkward phrasing, simplify syllable count and stresses, then propose the changed lines. For unclear names, ask for desired pronunciation and use a readable phonetic guide in the music direction. Do not insert arbitrary spelling changes into required brand copy without approval. For an overlong song, edit the existing track when the user wants shortening; a different lyric performance needs a new generation.

## Output review

Check actual duration, opening/ending, apparent instrumental/vocal mode and lyrical intelligibility before calling the song ready. Do not claim lyrics are verbatim merely because the request contains them. If playback is unavailable, state that limitation and provide the completed asset for listening.
