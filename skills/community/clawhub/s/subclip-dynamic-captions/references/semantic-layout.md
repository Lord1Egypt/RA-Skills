# Dynamic caption semantic layout

## Preset choice

- `ivory-spotlight` (Spotlight): the DEFAULT for newly generated captions, with no word highlight. Editorial serif, italic emphasis, 2–3 words.
- `bold-clean`: general high-impact social speech; readable 3–4 word phrases (it has the yellow word-highlight box; choose it explicitly).
- `serif-storyteller`: narrative, personal story, or cinematic delivery; usually 2–3 words.
- `authority`: educational, expert, business, or technical explanation; 2–3 words and coherent labeled phrases.
- `composite`: very bold Difference-composite treatment when the footage supports strong contrast.
- `minimalist` / `minimalist-white`: restrained clean presentation when captions should support rather than dominate.
- `kinetic` / `kinetic-yellow`: energetic, fast social delivery; normally no more than 3 words.
- `one-word` / `composite-one-word`: deliberate one-word-at-a-time treatment only when requested or clearly appropriate for a very short, forceful clip.
- `justified`: calmer long-form excerpts with meaningful 6–7 word pages; do not isolate hook words. The desktop/web completeness gate has a hard maximum of 7 even though an older prompt described a looser 6–10 target.

An explicit creator selection wins. Keep an existing saved preset when the request is only to improve priorities or grouping.

## Priority tiers

Default priority `0` is implicit. Use Medium `1` for key nouns, action verbs, salient adjectives, entities, and supporting outcomes. Use Important `2` sparingly for the strongest concrete outcomes, numbers, stakes, differentiators, emotional pivots, or central entities.

- Important is normally about 8–18% of words, not a quota.
- Potential one-word hooks are normally about 3–8% and must also be Important.
- Avoid articles, conjunctions, generic pronouns, prepositions, verbal fillers, and repeated low-signal words unless one is genuinely the semantic anchor.
- Mix useful signal types when available: outcome, number, entity, stake, and pivot. Do not highlight every noun or every number.
- Preserve manual speaker labels and never render speaker names unless requested.

## Page construction

- Every caption word ID appears exactly once and stays in transcript order.
- Never place words from different `clipId` owners in one page.
- Preserve natural chunks: subject + verb, verb + object, short named entities, quantities, and negation.
- Avoid an orphan setup word such as “I,” “The,” “And,” or “To.”
- Prefer page starts with setup/default words and endings on meaningful Medium or Important words.
- Do not allow long stretches of visually flat pages when semantic emphasis exists, but never invent emphasis to satisfy a pattern.
- One-word pages are selective hook events. Avoid consecutive one-word pages unless the chosen one-word preset explicitly requires them.
- For `authority`, keep adjacent emphasized words together when they form one concept and avoid mixing that concept with filler.
- For `justified`, keep phrase meaning intact at 6–10 words and use priority styling inside the page rather than one-word isolation.
- Punctuation is grouping context, not a reason to create empty or punctuation-only captions.

For long transcripts, use the exact chunking, normalization, and completeness gate in [intelligence-contract.md](intelligence-contract.md), retain a compact summary of each chunk, then submit one complete ordered priority/page result. Do not overwrite a completed earlier source while analyzing a later one.
