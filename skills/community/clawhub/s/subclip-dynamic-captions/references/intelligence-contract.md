# Dynamic caption intelligence contract

This is the agent-facing port of the semantic prompt, post-processing, and validation used by Subclip-web’s dynamic-caption intelligence. Apply it to exact caption word IDs before calling the priority and page tools. Do not reduce it to keyword frequency or highlight every noun.

## Internal analysis result

For each bounded transcript unit, derive exactly four things:

1. `summary`: a short local context summary used to judge words in meaning, not isolation.
2. `importantWordIds`: priority 2, the strongest high-impact words.
3. `mediumWordIds`: priority 1, supportive noteworthy words.
4. `hookWordIds`: a selective subset of Important used to create rare hook pages when the preset permits them.

Default priority 0 is implicit for every word not selected as Important or Medium. Hook is a page-layout role, not a third persisted style priority. Use only IDs from the current caption list, retain each occurrence’s exact ID, and never invent, paraphrase, or globally match every occurrence of the same text.

## Semantic prompt

Act as an expert subtitle semantic formatter for short-form video. First understand what the speaker is saying and summarize the local passage. Then rank words by their contribution to the passage’s hook, clarity, stakes, and payoff.

### Important, priority 2

Important words are the strongest hook moments and should remain sparse. Prefer:

- concrete outcomes or transformations
- standout numbers, percentages, dates, quantities, or measurable proof
- stakes, risk, loss, urgency, conflict, or a meaningful contrast
- differentiators, revelations, conclusions, or emotional pivots
- central entities, product/category terms, or high-impact nouns without which the point loses its identity
- decisive action or result verbs when the action itself is the payoff

Good contextual candidates include “Launch,” “Breakthrough,” “10x,” “Finally,” “Proof,” “Results,” “Momentum,” and “Conversion,” but these are examples, not a vocabulary list. Transcript-specific unusual words outrank generic marketing words. Usually select roughly 8–18% of transcript words; this is guidance, not a quota.

### Medium, priority 1

Medium words support the Important words and improve scanning without competing with the hook. Prefer:

- key nouns and named concepts
- meaningful action verbs
- salient adjectives or adverbs
- process, method, audience, or category terms needed to understand the result
- supporting outcomes and secondary entities

Examples of useful Medium words when context supports them: “faster,” “clearer,” “stable,” “repeatable,” “qualified,” “stronger,” “practical,” “measurable,” “improved,” and “consistent.” Do not make every noun, verb, adjective, or number Medium.

### Hook subset

Hook words must also be Important. Select only the strongest concrete outcomes, numbers, stakes, differentiators, key entities, or emotional pivots that deserve an isolated visual beat. Usually this is about 3–8% of words. For a clip with at least 40 words, aim for at least three hook words only when the meaning genuinely supports them.

Mix signal types when available. A set containing an outcome, an entity, and a pivot is usually stronger than selecting only numbers. Minimize consecutive hook pages; isolation is punctuation for attention, not the default reading mode.

### Default and rejected emphasis

Keep ordinary grammar at priority 0. Do not select articles, conjunctions, generic pronouns, prepositions, auxiliaries, or verbal filler merely because they occur near a hook. The Subclip-web normalization rejects these English tokens after punctuation/case normalization:

`a`, `an`, `the`, `and`, `or`, `but`, `so`, `to`, `of`, `in`, `on`, `at`, `for`, `from`, `with`, `by`, `as`, `is`, `are`, `was`, `were`, `be`, `been`, `being`, `it`, `its`, `this`, `that`, `these`, `those`, `you`, `your`, `we`, `our`, `they`, `their`, `he`, `she`, `i`, `me`, `my`, `there`, `here`, `then`, `than`, `just`, `have`, `has`, `had`, `do`, `does`, `did`, `can`, `could`, `would`, `should`, `until`, `if`, `because`, `while`, `when`, `where`, `who`, `what`, `which`.

Numbers are never rejected by that filter. Preserve a negation or other functional-looking word inside its phrase page when it changes meaning, but normally do not style it Important or isolate it. Spoken fillers such as “um,” “uh,” and “ah” remain unimportant unless a separate rough-cut request removes them.

Before finalizing, ask:

- Would the passage still mean the same thing if this highlighted word were visually ordinary?
- Is this word specific to this transcript, or merely a generic high-energy word?
- Does the mix include the actual result, entity, stake, or pivot?
- Are Important words meaningfully rarer and stronger than Medium words?

## Worked selection examples

### Onboarding result

Transcript: “After six weeks of testing, our new onboarding flow cut drop-offs and improved trial activation. We removed two confusing steps, clarified pricing language, and added progress cues. In yesterday’s cohort, activation rose from 28% to 41%, and support tickets dropped noticeably.”

- Summary: onboarding changes produced a measurable activation gain and fewer support problems.
- Important: `activation`, `28%`, `41%`, `dropped`.
- Medium: `testing`, `onboarding`, `improved`, `clarified`, `pricing`, `progress`, `cohort`, `tickets`.
- Hook subset: `41%`, `activation`.
- Why: `41%` and `activation` express the main proof; process words provide context but are not the payoff.

### Editor launch

Transcript: “We launched the redesigned editor on Monday and monitored retention daily. The new timeline controls reduced editing friction, and creators finished drafts faster. By week’s end, median completion time fell by 19%, while publish rate increased across both short and long-form projects.”

- Summary: an editor launch improved completion speed and publishing outcomes.
- Important: `launched`, `retention`, `19%`, `publish`.
- Medium: `redesigned`, `timeline`, `controls`, `reduced`, `friction`, `faster`, `completion`, `increased`, `projects`.
- Hook subset: `19%`, `publish`.
- Why: `19%` is the quantitative proof and `publish` is the business-action result; product/process words support them.

### Sales process

Transcript: “Our sales team revised qualification criteria and rebuilt the outreach sequence. Instead of broad targeting, we focused on high-intent accounts and personalized first messages. Pipeline quality improved, meeting-to-close velocity increased, and this month we recorded our highest win-rate since Q1.”

- Summary: a more focused sales process improved pipeline quality and win rate.
- Important: `high-intent`, `velocity`, `highest`, `win-rate`.
- Medium: `revised`, `qualification`, `rebuilt`, `outreach`, `focused`, `personalized`, `pipeline`, `improved`, `month`.
- Hook subset: `win-rate`, `highest`.
- Why: the superlative and result are the strongest payoff; method words remain supportive.

Use these examples to learn ranking, not to copy their vocabulary.

## Long transcript analysis

Analyze chronologically in bounded chunks. Match Subclip-web’s operating bounds:

- target no more than about 45 seconds per chunk
- split at no more than 220 words even when 45 seconds has not elapsed
- retain each chunk summary while evaluating the next chunk
- merge exact Important, Medium, and hook IDs only after all chunks are understood

Never let a later chunk overwrite a completed earlier source. After merging:

1. Remove rejected filler/function IDs.
2. Remove any Medium ID also selected as Important; Important wins.
3. Remove any hook ID that is not still Important.
4. Assign every remaining transcript word one priority: 2, 1, or implicit 0.
5. Keep the summaries in the director brief so later revisions retain context without reloading the entire transcript.

## Page construction

Pages control reading rhythm. Build them from the unchanged chronological word-ID sequence after priorities and hook IDs are final.

### Hard bounds by preset

Treat `composite` like `kinetic` for grouping and `composite-one-word` like `one-word`. Always obey the maximum returned by `list_dynamic_caption_presets` when it is stricter.

- `one-word`, `composite-one-word`: exactly 1 word.
- `justified`: prefer 7 words and keep meaningful pages around 6–7; never create isolated hook pages.
- `authority`: 2–3 words, prefer 3, and keep adjacent priority-1/2 concept words together.
- `bold-clean`: 2–6 words, normally 3–4.
- `ivory-spotlight`: 2–3 words.
- `minimalist`, `minimalist-white`: 2–3 words; use 3 mainly when all three words are short, otherwise prefer 2.
- `kinetic`, `kinetic-yellow`, `composite`: 2–3 words, normally 3.
- `serif-storyteller`: normally 2–3 words; never exceed the preset maximum returned by the tool.

### Phrase and rhythm rules

- Keep subject + verb, verb + object, short named entities, quantities, and negation together when possible.
- Treat punctuation as grouping context, not a semantic word or a reason for an empty page.
- Start pages with lower-emphasis setup words when natural and end on Medium or Important words for a stronger transition.
- Do not strand setup words such as “I,” “The,” “And,” or “To.”
- Priority-0 words normally stay in multi-word pages with adjacent speech.
- Do not allow more than two consecutive pages containing only priority-0 words when semantic emphasis exists. In a rolling block of three pages, include at least one Medium or Important word when the transcript genuinely provides one.
- A silence gap of 250 ms or more is a preferred page boundary. Never cross a source `clipId` ownership boundary even when the gap is shorter.
- Consecutive labeled words in `authority` form one concept run and should be grouped up to the preset maximum rather than mixed with filler.
- A single hook may become a one-word page only for a preset that permits selective hook isolation and only when the preceding page was not already a singleton.
- If two or more hook words are consecutive with gaps below 250 ms, keep the hook run together up to the preset maximum instead of producing a strobe of singleton pages.
- `one-word` presets intentionally make every word a singleton. `justified` never isolates hooks.

### Orphan repair

After initial grouping:

1. Move one or two default setup words at the start of a page onto the preceding 2–3-word page when it stays under the maximum and leaves the emphasized phrase intact.
2. For `authority`, merge a labeled word at the next page start into a preceding labeled page when it stays under the maximum.
3. A non-hook singleton is invalid. Merge it into the previous page when possible, otherwise the next page, while preserving chronology and the hard maximum.
4. Repair a final page below the preset minimum by merging it backward when the combined page remains legal.

## Tool translation

The web analysis returned JSON, but the desktop agent translates it directly into native tools:

1. Call `set_dynamic_caption_priorities` with `importantWordIds`, `mediumWordIds`, and `resetUnspecified=true`.
2. Keep `hookWordIds` in working memory/director brief; use them only to decide legal page isolation.
3. Call `arrange_dynamic_caption_pages` with the complete ordered `{wordIds}` list.

Do not send word text where an exact ID is available. Do not call the priority tool once per word or the page tool once per chunk; analyze chunks, merge, validate, then submit one complete operation per tool.

## Completeness gate and safe fallback

Before arranging pages, prove all of these:

- the priority result contains every current input word exactly once through Important, Medium, or implicit Default
- Important and Medium do not overlap
- every hook is Important
- every page is non-empty and within the selected preset maximum
- flattened page IDs equal the current caption IDs exactly, including order and multiplicity
- no page contains unknown IDs or crosses source ownership

If semantic grouping cannot pass this gate, do not submit a partial page list. Keep the preset’s safe deterministic regrouping, correct the analysis, and retry the complete arrangement. Never erase captions or silently omit words to make validation pass.
