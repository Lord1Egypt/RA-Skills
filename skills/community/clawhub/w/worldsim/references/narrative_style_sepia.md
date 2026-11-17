# 通用叙事风格参考（sepia 原文搬运）

> 适用范围：通用——⑥作家各轮通用参考，按需查阅。
> 来源：skills/sepia（sepia v0.7.0）原文搬运（悬空引用已删）。
> 裁决：与 phase_writer.md或 SKILL.md 通用约束冲突处，以 worldsim 为准（POV 过滤/数据忠诚/卡里记的事不得增减·怎么讲全归作家/gate 不变）。
> 不在本文：professional-pass.md（含 domains/）、agents/、model-fingerprints.md、voices/ 正文——默认不加载；voice 叠加仅 opt-in（用户明示才用）。
> 用法：按需查。

---

## 原文搬运出处：skills/sepia/SKILL.md

# Sepia — de-AI writing

This skill combines measured findings with marked editorial heuristics. In fiction, StoryScope's narrative-only classifier reached 93.2% macro-F1, while its Core Only 30-feature XGBoost held-out classifier reached 84.8% macro-F1 (AUPRC .828); the manual rubric is neither classifier. The professional path combines measured studies with editorial heuristics, and its prescriptions are Sepia inferences unless a source explicitly tested the intervention. Route first, then operate.

## Routing（仅 fiction 行·其余路由文件不在本文）

| Text type | Load, in order |
|---|---|
| Fiction / stories / narrative essays | 本文件 Pass 1 → Pass 2 → Pass 3；diagnose with 本文件 Rubric |

中文叙事在 style-pass 步加挂本文件 Chinese calibration 节。

## Operations（权责注：结构性决策归①②③上游；⑥作家只取呈现技法）

Any request maps to one of four operations:

| Operation | Contract |
|---|---|
| **write** | New content. Read the domain file *before* drafting — architecture and register decisions come first, they cannot be retrofitted cheaply. For fiction, follow Workflow A below. |
| **review** | Diagnose only — no edits. Produce the defect list (fiction: rubric report) and stop. Report findings; apply nothing until asked. |
| **refactor** | Minimal in-place revision preserving structure, voice, and intent. Two-stage: full defect list first, then fix item by item, deepest layer first. Skew replace/delete over insert (measured editor ratio 74/18/8). The `Voice fit:` line is not a defect and is excluded from the fix list. |
| **recreate** | Full rewrite. Extract the facts, claims, and intent from the original into a bare list; verify nothing invented; write fresh under the domain rules. Use when defects are structural and the text is short enough that surgery costs more than rebuilding. |

The two-stage protocol is not optional for refactor/recreate: paraphrasing without a defect list makes AI fingerprints *more* visible, not less (measured on expert detectors).

## Fiction workflows（权责注：结构性决策归①②③上游；⑥作家只取呈现技法）

**A — writing new fiction:** (1) premise, genre, length — genre sets calibration targets; (2) fill the architecture sheet in 本文件 Pass 1; (3) select 3–5 human-leaning moves + one rarity move; (4) outline, run the outline/QUD checks in 本文件 Pass 2 and the echo test in 本文件 Pass 1 §2; (5) draft; (6) self-diagnose with 本文件 Rubric, one group at a time; (7) style pass last.

**B — revising existing fiction:** (1) diagnose completely first (rubric → discourse → style), no edits; (2) triage — architecture defects need scene-level surgery; (3) fix deepest first; (4) verify: re-run changed rubric groups, read key passages aloud, echo-test any added twist.

## Calibration — the rule that governs all rules

| Principle | Meaning |
|---|---|
| Aim at the band, not the opposite pole | Human values are moderate (chronological discontinuity 2.4/5, not 5). Inverting every AI tell creates a new fingerprint. In professional prose the equivalent: match the venue's register, don't overshoot into forced casualness — informality alone fools no trained reader. |
| Select, don't accumulate | Human writing is diverse. Fiction: 3–5 moves per story, chosen for the premise, varied across works. |
| Leave slack | Ordinary sentences, an underdeveloped thought, a plain paragraph. Do not sand every surface. |

## Hard guardrails

- **Never invent specifics.** Fiction: intertextual references, brands, places must be real and correct. Confident wrong facts are themselves a top-tier tell.
- **Deletion beats addition** (74% replace / 18% delete / 8% insert). The only additive fix is real specificity, and no register drift: a rewrite must not come out more promotional than its source.
- **Respect the author's voice and the venue's corpus.** Extract habits from the user's samples or the venue's recent artifacts before editing; edit toward *that* profile. Do not remove a mannerism they actually use.
- **Dialogue quotes and quoted material are load-bearing** — do not regularize them.
- **Check the whitelists** (本文件 Pass 3 §7) before flagging: clean grammar, formal tone in formal venues, and conventional templates are not evidence of AI.
---

## 原文搬运出处：skills/sepia/references/narrative-pass.md

# Pass 1 — Narrative architecture

Seven decision groups. Each lists the measured human-vs-AI gap, what to do when **generating**, and what to check when **revising**. Numbers are from StoryScope (S), Beguš 2024 (B), Xu et al. PNAS 2025 (X), Nonaka & Perry 2025 (N), and QUDsim (Q); percentages read *human vs AI*. Single-letter aliases in this file are file-local. Generate/Revise prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention.

（权责注：支线/结局/时序等结构决策归①②③上游；⑥作家只取呈现技法，不改事实。）

Work through all seven groups when filling the architecture sheet, but **enact only 3–5 human-leaning moves per story** (见本文 Calibration 节). The groups marked ⚑ were absent from the tools sampled in the repository's 2026-08-27 ecosystem snapshot; treat that as a bounded product observation, not proof of universal zero coverage.

## Architecture sheet template

Fill this before drafting (Workflow A) or as the diagnosis summary (Workflow B):

| Decision | Choice for this story | Target band |
|---|---|---|
| Theme handling | stated / implied / withheld | implied by default |
| Subplot | none / parallel / contrasting / independent | one subplot, ~40% of stories |
| Resolution driver | protagonist choice / mixed / external | mixed or external ~50% |
| Ending mode | external act / internal acceptance / partial / open / catastrophic | avoid internal-acceptance default |
| Time structure | linear / moderate anachrony / braided | moderate (2–3 on a 1–5 scale) |
| Revelation pacing | front-loaded / even / back-loaded | back-loaded |
| Emotion strategy | mix of: explicit labels / behavior / embodied / ambiguous | behavior-led mix; embodied only at peaks |
| Protagonist introduction | description / in-action / in-dialogue / thought / others' reports | in-dialogue or in-action |
| Moral stance on protagonist | affirmative / tragic-flaw / ambivalent / antiheroic | ambivalent ~60% |
| Real-world anchors | list actual works, places, brands to name | ≥1 explicit named reference |
| Network shape | who never meets whom; who dislikes whom | sparse, net-neutral affect |
| Rarity move | the one structural choice atypical for this premise | exactly one |

## 1 ⚑ Theme: stop explaining it

| Feature | Human | AI |
|---|---|---|
| Narrator explicitly states the theme (S) | 52% | 77% |
| Thematic explicitness, 1–5 (S) | 3.28 | 3.94 |
| Dialogue used for philosophical debate (S) | 34% | 59% |
| Moral/philosophical weighting, 1–5 (S) | 3.26 | 3.68 |
| Thematic unity, 1–5 (S) | 4.41 | 4.74 |

**Generate:** Decide the theme, then trust the events to carry it. The narrator never summarizes the lesson; the grieving character's arc does **not** end with what she learned. Dialogue does plot and relationship work — characters argue about the rent, not about the nature of grief. Let one scene or image exist for texture alone, serving no theme (humans score 4.4/5 on unity, not 5/5 — near-total unity is the tell, total unity is worse).

**Revise:** Search the last three paragraphs and any narrator generalization ("That is how people are", "It was then she learned…", "In the end, what mattered was…") — cut or convert to a concrete action or image. Where dialogue debates ideas, rewrite so the disagreement is about something specific the characters want. If a symbol is explained in-text, delete the explanation and keep the symbol.

> Beguš reports recurring moralizing final lines such as "love knows no boundaries" in the tested model stories. Treat that pattern as a candidate signal, not evidence that a conclusive ending is necessarily machine-written.

## 2 ⚑ Plot: loosen the single track

| Feature | Human | AI |
|---|---|---|
| No subplots at all (S) | 57% | 79% |
| Subplot thematically parallel to main plot (S) | 42% | 21% |
| Causal-chain continuity, 1–5 (S) | 3.92 | 4.20 |
| Plot elements that reappear on regeneration — "drop ratio" (X) | 3.7% | 9–11% |

**Generate:** Give roughly two in five stories a subplot; when present, let it echo the main theme obliquely rather than restate it. Allow the causal chain to break once: an episode that isn't caused by the inciting incident, a consequence that arrives from offstage. Plant one detail that never fires — humans leave loose ends; the fully-paid-off setup inventory is machine bookkeeping.

**Revise:** Outline the draft as a beat list. If every beat is caused by the previous beat in one unbroken line to the climax, sever one link: move a cause offstage, or insert an event with its own origin. If the story has no second thread and its length can carry one, braid one in.

**Echo test (X):** for each turning point ask — *if this premise were regenerated twenty times, would this same turn appear again?* The helpful stranger, the problem that solves cleanly, the reconciliation on schedule: these reappear. Replace inevitable turns with one that requires this story's particulars. Kafka's traffic cop says "Give it up!" and walks away; twenty regenerations produce twenty cops giving directions.

## 3 Endings and resolution

| Feature | Human | AI |
|---|---|---|
| Resolution driven by protagonist's own choice (S) | 46% | 69% |
| Resolution via internal understanding/acceptance (S) | 27% | 47% |
| Morally ambivalent protagonist (S) | 59% | 38% |

**Generate:** Do not default to the arc where the protagonist, having grown, chooses the resolution and makes peace with it — that compound default (agency + acceptance + growth) is the strongest ending fingerprint in the data. Half the time, let chance, other people, or institutions decide the outcome. Endings may be partial, open, or catastrophic. The protagonist's final moral position can stay mixed: vindicated in the event, wrong in the act.

**Revise:** If the draft ends with the protagonist deciding + accepting + understanding, change at least one leg of the tripod. Cut denouement paragraphs that settle every account; ending one beat *earlier* than feels complete is usually the fix.

## 4 ⚑ Time: linearity is a choice, not a default

| Feature | Human | AI |
|---|---|---|
| Chronological discontinuity, 1–5 (S) | 2.40 | 2.12 |
| Anachrony (flashback/flash-forward) intensity, 1–5 (S) | 2.58 | 2.31 |
| Nonlinear framing used to delay disclosure, 1–5 (S) | 1.96 | 1.68 |
| Recontextualization depth after a reveal, 1–5 (S) | 3.28 | 2.95 |
| Revelation pacing (human fingerprint, S) | back-loaded | even/front-loaded |

**Generate:** The human band is *moderate* nonlinearity — a story that opens at the funeral and spirals back through decades, not a shuffled puzzle-box. Use time jumps to **stage information**: hold back the cause, open with the effect. Aim reveals so they force rereading — the best twist recolors earlier scenes (target 3/5, not a twist that changes nothing and not a total inversion). Keep the biggest disclosure late (back-loaded pacing is a measured human fingerprint).

**Revise:** If the draft narrates first-cause-to-final-effect in order, find the scene whose impact grows when withheld and move it. Check that DeepSeek-style front-loading (all context delivered before the story starts moving) isn't present: cut the briefing, let context leak out mid-motion.

## 5 ⚑ Emotion and senses: break the show-don't-tell dogma

| Feature | Human | AI |
|---|---|---|
| Emotion conveyed mainly via embodied sensation/metaphor (S) | 38% | 81% |
| Emotion conveyed mainly via explicit labels (S) | 29% | 8% |
| Olfactory imagery among dominant senses (S) | 57% | 82% |
| Setting mirrors characters' inner states, 1–5 (S) | 3.58 | 4.07 |
| Sensory density, 1–5 (S) | 3.66 | 3.93 |
| Depth of interior access, 1–5 (S) | 3.67 | 3.93 |

**Generate:** AI executes "show don't tell" as dogma: fear is always a tightening chest, cold sweat, dimming lamplight. Humans mix four modes and lean on the plainest two — behavior first, plain naming second ("She was afraid" is a human sentence; models almost never write it). Reserve embodied rendering for one or two peaks per story. Let weather be weather: not every storm carries the marriage. Ration smell — it has become the connoisseur sense of machine prose.

**Revise:** Inventory every emotion beat and classify its mode. If embodied dominates, convert most to behavior (what she does) or plain statement (what she feels, named), keeping the strongest one or two embodied. Strip pathetic fallacy where the environment shadows mood scene after scene. Thin sensory description toward moderate density — cut the third sense in three-sense sentences.

## 6 ⚑ Characters and the social network

| Feature | Human | AI |
|---|---|---|
| Protagonist introduced via external description (S) | 30% | 52% |
| Human fingerprint: introduced in-dialogue (S) | strongest human marker | rare |
| Network density — share of character pairs that interact (N) | 0.18 | 0.34–0.47 |
| Mean relationship affect (N) | −0.06 (net neutral) | +0.24 to +0.66 (all positive) |
| Clustering among antagonistic ties (N) | 0.395 | 0.07–0.21 |
| Investment built before putting a character in danger, 1–5 (S) | 2.76 | 2.99 |

**Generate:** Bring the protagonist on stage talking or doing, not described ("The dog arrived on a Tuesday" beats a paragraph of appearance-and-backstory). Keep the cast graph sparse: some characters never meet; some know each other only through a third. Sum of relationship affect should sit near neutral — real casts contain dislike that has nothing to do with the plot. Give antagonism *structure*: the antagonist has allies, internal rifts, their own network — not a lone hostile node pointed at the hero. It's fine to endanger a character the reader barely knows.

**Revise:** Draw the cast graph with signed edges. If everyone connects to everyone, delete edges. If every edge is warm, cool several. If the villain is isolated, give them one relationship that doesn't involve the protagonist.

## 7 ⚑ The outside world and the reader

| Feature | Human | AI |
|---|---|---|
| Explicit named references to real texts/authors (S) | 47% | 24% |
| Balanced mix of explicit + implicit reference (S) | 37% | 16% |
| Any fourth-wall permeability (S) | 67% | 39% |
| Direct reader address (S) | 28% | 7% |
| Distinct meaningful locations (S, ordinal) | 1.34 | 1.08 |
| Dialogue-to-narration proportion, 1–5 (S) | 2.95 | 2.70 |

**Generate:** Name real things — an actual novel on the shelf, a real band, the specific highway (worldsim 以 W4 数据忠诚为准：scene_state/CHAR_.md 无源不写). Mix named references with unnamed echoes. An occasional aside that admits a reader exists ("you know the kind of house") is a human move — *occasional*: an aside or two, not a metafictional frame. Let scenes happen in one or two more places than the premise strictly needs. Give dialogue slightly more floor than exposition.

**Revise:** If the draft gestures at "a famous poet" or "an old song," make one of them specific and real. If the story visits a single room for 5,000 words and the premise doesn't demand confinement, move one scene. Vague allusion everywhere = machine caution.

## The rarity move

Human stories are structurally *rarer* than AI stories (rarity percentile 0.71 vs 0.49; the five models cluster in one region of narrative space and humans scatter). Beyond the band-calibrated rules above, make **exactly one** structural choice that is genuinely atypical for the premise — an unexpected narrator distance, a resolution mode the genre rarely uses, a frame that recasts the genre (crossover literary ambition is a measured human fingerprint). One. More than one reads as performance.
---

## 原文搬运出处：skills/sepia/references/discourse-pass.md

# Pass 2 — Discourse flow

The layer between plot and sentences: how paragraphs advance, where the energy sags, and where things sit on the page. Evidence: QUDsim/COLM 2025 (Q), Tripto et al. EMNLP 2025 (T), Russell et al. ACL 2025 (R), Beguš 2024 (B), asavvin's outline test (A). Single-letter aliases in this file are file-local. Prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention.

## 1 The QUD check — what question does each paragraph answer?

Every paragraph implicitly answers a question. In QUDsim's tested samples, two models given the same premise independently reused the sequence *scene briefing → justifying the deception → social consequences → the weight of responsibility* (Q). Surface rewording does not change that question sequence; changing it requires reordering or replacing the underlying moves.

**Check:** List one implicit question per paragraph/scene of the outline or draft. Flags:

| Flag | Symptom |
|---|---|
| Linear interview | Each question follows administratively from the last (what happened → why → what resulted → what it means) |
| The reflection tail | Final paragraphs answer "what does this mean / how does she feel about it now" — the machine's closing move |
| Missing move types | No paragraph *compares* (two times, two characters, two versions of an event), none *verifies* (doubts or contradicts an earlier paragraph's account), none *digresses* (memory or association that earns its place later) |

**Fix:** Reorder so at least one question arrives before its setup. Replace one consequence-paragraph with a comparison or a contradiction — LLMs use consequence/procedure moves ~19% of the time and comparison/verification moves ~0.2–0.3% (Q); a single "but that isn't how her sister remembers it" paragraph does more de-AI work than a page of rewording.

**Outline test (A):** extract the first sentence of every paragraph and read them as a list. If they form a clean summary of the piece, the structure is machine-shaped — a human outline has gaps, jumps, and sentences that make no sense out of context.

## 2 The middle is the choke point

Detectors and human judges find AI text most identifiable in the **body**, least in openings and endings — models imitate the formulaic bookends well and expose themselves in the long middle (T). LLM stories also show a measured mid-story collapse into predictable filler, rushing pace and leaving suspense unexplored (X, cited in narrative pass). Though this section speaks in fiction terms, the choke-point evidence was measured on news, essays, and email as well — for non-fiction, read "scene" as section and "event" as claim or finding.

**Fix, aimed at the middle third:**

- Put at least one event there that the opening does not predict.
- Vary texture between adjacent scenes: a dense scene then a fast one, a dialogue-heavy stretch then summary narration. Human writing shows high cross-paragraph variance ("burstiness"); models hold one register for the whole text (T).
- Let one thread slow down instead of resolving on schedule — the machine failure mode is acceleration past the interesting part.

## 3 Structural positions on the page

Position patterns survive paraphrase better than word choice does — after full paraphrasing, position tells became *more* visible to expert detectors, not less (R).

| Position tell | Machine habit | Human habit |
|---|---|---|
| Paragraph lengths | Uniform | Ragged — including a one-sentence paragraph |
| Quoted speech / key lines | Always closing a paragraph | Anywhere, including mid-paragraph |
| Lists of qualities, reasons, images | Exactly three items | Two, four, one — three sometimes |
| Scene transitions | Same connective formula each time | Varied: hard cut, time skip, dialogue pickup |
| Emphasis | Evenly distributed | Clustered where it matters, absent elsewhere |

The paragraph-length row means uniformity *within the text*. Paragraph length and paragraph count on their own are not signals: measured directions contradict across corpora (LLM paragraphs longer in how-to text, shorter in generated papers, more numerous in Chinese answers) and follow prompt limits and venue conventions.

## 4 Openings

The machine opening: establish time + place + weather, introduce the character with description, then start the story (B: "Once upon a time"-style detachment; R: the "On a drab November morning" scene-setting lead; S: AI over-grounds the opening spatially, 2.33 vs 2.12).

**Fix:** open inside the situation — mid-conflict, mid-conversation, mid-error ("Sam didn't know she wasn't human"). Ground space with one working detail, not an establishing shot. Delay the character's appearance-and-backstory paragraph indefinitely; most stories never need it.

## 5 Names

The tested model outputs converged on recurring names such as Elara, Ava, and Amelia; Emily or Sarah appeared in 63–70% of the AI articles, and formal titles were overrepresented (B, R).

**Fix:** name characters from the story's specific world (ethnicity, region, generation, class), let surnames and nicknames do social work, drop titles except where the fiction needs them, and let different characters call the same person different things.
---

## 原文搬运出处：skills/sepia/references/style-pass.md

# Pass 3 — Surface style

Run last, after structure is fixed. Evidence: LAMP/CHI 2025 (L), Reinhart et al. PNAS 2025 (P), Russell et al. ACL 2025 (R), Shaib et al. slop taxonomy (S), fiction/RP community ban lists (F), Desaire et al. 2023 (D), Gude et al. 2026 (G), Muñoz-Ortiz et al. 2024 (M), 朱君輝 et al. CCL 2023 on Chinese (Z), Freeburg 2026 (E). Single-letter aliases in this file are file-local. Prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention. Editing operations should skew **replace 74% / delete 18% / insert 8%** (L) — when in doubt, cut. The one exception that may grow text: adding concrete specificity.

## 1 The seven artifacts (professional-editor taxonomy, L)

Ordered by how often professional writers actually fixed each, which is the priority order:

| # | Artifact | Fix |
|---|---|---|
| 1 | Awkward word choice (28%) | Replace misused or off-register words. "Seem to + verb" → the verb itself, unless uncertainty is real. Fix unclear pronouns and excess passives. |
| 2 | Poor sentence structure (20%) | Split run-ons into two sentences. One tangled thought = two plain ones. |
| 3 | Redundant exposition (18%) | Delete what the scene already implies. The pattern "[main clause], [trailing participial phrase restating it]" → delete after the comma ("cast long shadows over the desolate landscape" → "cast a long shadow"). |
| 4 | Cliché (17%) | Replace with fresh, scene-specific language — **never with a blander paraphrase** (that is the documented machine failure). If nothing fresh is available, delete the line. |
| 5 | Lack of specificity | The only additive fix: real names, objects, numbers, actions from lived detail. If you lack the material, ask the user — filling in more generic description makes it worse. |
| 6 | Purple prose | Simplify. Long abstract-noun sentences conveying one feeling → short concrete sentences ("She cried. She cried for unfairness. She cried without relief."). |
| 7 | Tense inconsistency | Pin the tense; hunt drift inside paragraphs. |

## 2 Syntax templates to hunt

These part-of-speech shapes are 2–5× overrepresented in LLM prose and heavily edited out by professionals (L, P):

| Template | Examples | Fix |
|---|---|---|
| a/the [abstract noun] of [noun] (and [noun]) | a mix of pride and fear · a sense of wonder · a pang of nostalgia · the weight of expectation | Name the concrete thing or cut the wrapper noun |
| the [adj] [noun] of [possessive] | the intricate tapestry of its · the unspoken plea in her | Rewrite from scratch |
| Trailing/leading participial clause | "…, evading Show's heavy blows" · "Stuffing his mouth, Joe ran" | Break into its own short sentence with a finite verb (LLM usage: up to 5× human) |
| Nominalization | realization, determination, transformation as sentence subjects | Turn back into verbs (2× human rate) |
| Paired abstractions "X and Y" | desperation and resolve · curiosity and caution | Keep one |
| not only X but also Y · it's not X, it's Y | — | Say the one thing you mean |
| Rule of three | three parallel adjectives/clauses/images, everywhere | Two or four; break the rhythm |

## 3 Vocabulary

Merged ban list (R Table 12 + P excess-vocab + L signature phrases + F fiction slop). A single hit is not a verdict — **slop is cumulative** (S): count hits, and rewrite when they cluster.

| Class | Words/phrases |
|---|---|
| Abstract-grandeur nouns | tapestry, testament, symphony, kaleidoscope, landscape, realm, journey, beacon, camaraderie, solace, resilience, nuance, myriad |
| Performance verbs | delve, underscore, foster, harness, navigate, resonate, elevate, embrace, transcend, unravel, ignite, grapple, weave/weaving |
| Inflation adjectives | intricate, vibrant, palpable, profound, pivotal, crucial, seamless, robust, transformative, multifaceted, fleeting, bustling |
| Fiction slop (F) | ozone, petrichor, shimmering, thrums, gossamer, "barely above a whisper", "eyes gleam/glint/alight", "despite herself", "breath catches", "heart skips", "shivers down the spine", "voice like [material]" |
| Signature phrases (L) | unspoken, the weight of, hung in the air, the air was thick, in the pit of her/my stomach, a constant reminder of |
| Formula phrases (R) | paving the way, it's important to note, in a world of/where, a testament to, cautionary tale, "amidst" |
| Filter words (F) | felt, seemed, realized, noticed, knew, watched as — delete the filter, render the thing directly |

## 4 What to add back — the underused human register

Instruct-tuned models systematically suppress these (P: usage 13–80% of human rate). Restore them *to the degree the genre and the author's voice allow* — sprinkled, not poured:

| Restore | Examples |
|---|---|
| Contractions | don't, it's, wouldn't |
| Discourse particles and fillers | well, anyway, just, really, actually |
| Plain causal connectives | because (GPT-4o uses it at 20% of human rate), so |
| Hedges and emphatics | almost, sort of, for sure, obviously |
| Negation | "no answer was good enough" — synthetic negation runs at half human rate |
| Pro-verb do | "and she did" |
| Plain speech tags | *says/said* on repeat is human; rotating *notes, observes, remarks, muses* is machine elegance |
| First/second person, direct questions | where POV permits |
| Coarse or blunt language | where the register genuinely calls for it |

## 5 Genre alignment and sentence rhythm

Reinhart et al. report that instruction-tuned models favor an informationally dense, noun-heavy style and struggle to match genre-aligned variation (P). Before editing, state the target register (literary / pulp / YA / essayistic) and edit toward *that* — a de-AI'd thriller and a de-AI'd literary story should not end up in the same voice. Sentence length variance, contraction rate, and vocabulary plainness are genre parameters, not universal constants.

**What is measured about sentence length.** The *spread* of sentence lengths inside a text is smaller in LLM output than in human writing in each of the four studies that measured it, across two model generations and two languages: within-paragraph standard deviation and the length difference between consecutive sentences both run higher in human paragraphs (D, values not printed); sentences of 1–15 tokens make up 32–33% of human news sentences against 1–4% for 2025 instruction-tuned models (G); sentences of 41 tokens or more are 12.0% of human sentences against 5.5% for a 2023 base model (M); Chinese answers show a per-answer sentence-length SD of 9.248 vs 6.729 words (Z). Three further English studies find the same direction only *between* texts (the spread of per-essay means), which is consistent but is not evidence for a within-text check and is not counted here. The *mean* is not a signal: against 2023 base models human sentences were about 10–20% longer, while 2025 aligned models write sentences 15–30% longer than humans (G, the paper's own wording), and on one Chinese corpus the direction flips with the unit of count (Z). No English study prints a within-text SD for humans versus LLMs, and the Chinese figure above comes from one corpus and one 2023 model, so no numeric threshold exists to quote, and none is set here.

**Check (Sepia inference).** Look for runs of adjacent sentences of about the same length — three or more in a row; "three" and "about the same" are reading conventions, not measured limits. This is the within-text form of D's consecutive-sentence-difference feature, and it works in any language and any unit of count as long as the unit is used consistently. Such a run is a *candidate* signal that counts only alongside other hits (slop is cumulative, §3). Do not score a passage by counting sentences under or over a length cutoff: the tail rates above are corpus-level and genre-specific, measured in tokens on news leads (G, M) and in words on science paragraphs (D), so a paragraph with no very short or very long sentence is ordinary human prose, and no per-passage cutoff can be derived from them. The check needs running prose of at least paragraph length, which is the unit D measured: a one-line reply, a bullet list, a table, or a commit-style release note has no rhythm to measure, and the scan reports `none`. For Chinese, `languages/zh.md` gives the same check with the Chinese numbers.

**Fix.** Break the run by moving words, never by adding them (the 74/18/8 rule above): split one long sentence, merge two short ones, or delete a clause. Which way to break it comes from the text — a run of long sentences wants one short one, a run of short ones wants one long one. Do not shorten everything: a passage of uniformly short sentences is the same defect seen from the other side, and it reads as pastiche. One measured prior may inform the direction: when the model that produced the text under check — the author on review and on refactor's diagnostic stage, the executor on write — is one of the four 2025 aligned releases G measured (Qwen 2.5, LLaMA 3.3, Mistral v0.3, GPT-4o, on news leads), the short sentences are the ones that went missing; for every other family, including Claude and Gemini, no sentence-length study exists, and a current executor reviewing human or older-model text does not import the prior either.

## 6 The read-aloud test

Grammatically correct but unsayable is a distinct slop dimension (S: "the earthen area that formerly held the puddle was now dry"). Read dialogue and any sentence you rewrote aloud (mentally): if no native speaker would say it or write it in a letter, redo it in speech-shaped syntax.

## 7 False-positive whitelist

Do **not** flag or "fix" these — over-correction is its own fingerprint:

| Not evidence of AI | Why |
|---|---|
| Correct grammar and clean punctuation | Plenty of humans write cleanly; imperfection-injection is a detectable gimmick |
| A single em-dash, semicolon, or "delve" | One hit means nothing; only clusters count |
| Neutral or formal tone in a formal genre | Register match beats forced casualness |
| A banned word inside quoted dialogue or an in-world document | Quoted material keeps its texture |
| The author's own verified habits | If the user's samples use em-dashes or "moreover," those stay |
| Moderate ordinary sentences | Slack is human; do not polish every line to distinctiveness |
| Punctuation density, or a comma/period count | Measured directions contradict: on one Chinese Q&A corpus, punctuation density reads 0.135 human vs 0.136 ChatGPT (Z) while the punctuation share of tokens reads 16.0% vs 13.4% (Guo et al. 2023, same corpus); in English news the human share is 11.88% against 10.77–12.14% for four base models, one of them above human (M). No per-type human-vs-LLM count (comma, period, semicolon) exists for English or Chinese |
| Em dash frequency as a model-agnostic tell | Measured per 1,000 words across 2025–26 releases: 10.62 (GPT-4.1), 9.09 (Claude Opus 4.6), 1.43 (GPT-5.4), 0.00 (Llama 3.x), against a human mean of 3.23 from eight essays (E). It is a release property, so only the cluster rule above applies — never a blanket rule |
| Paragraph count or average paragraph length | Directions contradict across corpora: LLM paragraphs longer in how-to text (82.01 vs 68.83 words), shorter in generated papers (39.82 vs 51.12), and more numerous in Chinese answers (3.681 vs 1.442). Only uniformity of paragraph length *within* the text is a signal (`discourse-pass.md` §3) |

> Informality is not a disguise. In Russell et al.'s tested humanization conditions, expert readers still detected other machine-patterned cues; adding casual language alone did not remove them. The claim does not establish that every informal model output is detectable.
---

## 原文搬运出处：skills/sepia/references/languages/zh.md

# Chinese calibration for the style pass

Load this file at the style-pass step whenever the target text is Chinese, in any variant, on any route. It changes nothing else about the route. The English ban lists in `style-pass.md` §3 do not transfer word for word; what transfers is the *shape* of the checks — the syntax templates of §2, the restore list of §4, the rhythm check of §5, the whitelist of §7 — and this file says what each shape looks like in Chinese.

Evidence: one measured corpus, HC3-Chinese — 6,586 human and 6,586 ChatGPT answers to the same open-domain questions, GPT-3.5-era ChatGPT, Simplified Chinese, 2023 — analysed with 159 Chinese CTAP features by 朱君輝 et al., CCL 2023 (Z), with Guo et al. 2023 (H) supplying a second measure on the same corpus; a 2025 joke-generation study by 蔣彥廷 and 應以周, CCL 2025 (J), is used only where it contradicts Z. Everything else below is a Sepia inference or a marked editorial heuristic.

## 1 Measured (Z, per-answer means; H where named)

| Feature | Human | ChatGPT | Unit and note |
|---|---|---|---|
| Sentence-length SD | 9.248 | 6.729 | words (詞); in characters (字) 15.150 vs 12.842 — the gap holds in both units |
| Mean sentence length | 25.067 | 21.823 | words — humans *longer*; in characters 40.893 vs 42.396, the direction flips, so length itself is not a signal |
| Paragraphs per answer | 1.442 | 3.681 | ChatGPT wrote *more* paragraphs; mean paragraph length 123.907 vs 92.747 characters |
| Punctuation density | 0.135 | 0.136 | Z; the same corpus measured as punctuation share of tokens reads 16.0% vs 13.4% (H) — contradictory measures, not a signal |
| 語氣詞 density | 0.016 | 0.003 | five times higher in human answers |
| 連詞 density | 0.013 | 0.036 | 「和」 alone: 4.13 vs 11.76 per answer |
| Pronoun density | 0.052 | 0.069 | second person 0.010 vs 0.021 |
| Monosyllabic word share | 0.483 | 0.379 | disyllabic share 0.445 vs 0.532; disyllabic word count was selected as a key feature by both of Z's filters |
| Type-token ratio | 0.725 | 0.543 | content-word richness 0.822 vs 0.647 |
| Mean dependency distance | 3.900 | 3.659 | longest 29.452 vs 23.991 |

## 2 What to hunt (Sepia inferences from §1; shapes of `style-pass.md` §2)

| Shape | Chinese form | Fix |
|---|---|---|
| Connective stacking (連詞 density 0.036 vs 0.013) | 「和／以及／並且／同時／此外／因此／然而」 chained across clauses; 「和」 joining whole clauses rather than nouns | Delete the connective and let juxtaposition carry the link; Chinese parataxis is the human default |
| Second-person address outside dialogue or instructions | 「你會發現」「您可以」 in expository prose | Delete or recast as a statement |
| Disyllabic padding where a monosyllable is idiomatic | 「進行討論」「加以說明」「予以處理」「做出決定」 | 「討論」「說明」「處理」「決定」 — the verb alone |
| Flat sentence length (SD 6.729 vs 9.248 words) | Runs of adjacent sentences of about the same length | Apply the §5 check as written (runs of three or more adjacent near-equal sentences): split one long sentence, merge two short ones, delete a clause. §5 sets no length cutoff in any language; no Chinese short- or long-sentence share is measured, and none is invented here. Count in whichever unit you use consistently — the SD gap holds in both 詞 and 字 |

## 3 What to restore (Sepia inferences; shape of `style-pass.md` §4)

Sprinkled, never poured, and only where the register allows: sentence-final and mid-sentence 語氣詞 (啊、吧、呢、嘛、喔、啦、耶) — the largest measured gap in §1; monosyllabic verbs and adjectives; a spread of sentence lengths; subject ellipsis and colloquial contraction where a native writer would drop the subject, the Chinese counterpart of §4's contractions. Formal venues keep their register: a legal notice does not get 「嘛」.

## 4 Editorial heuristics — unmeasured, marked

Reported by Taiwan editors and readers in 2026 (自由時報 2026-07-12; 數位時代 2026-04-22; ledger "Consulted" table); none has a corpus number, and each is a Chinese form of a template already in `style-pass.md` §2:

| Reported tell | Maps to |
|---|---|
| 「不是…而是…」「這不是 X，而是 Y」 | §2 "it's not X, it's Y" |
| Nominalized subjects 「○○性／○○感／○○化」 (「自我的探索」 for 「找自己」) | §2 nominalization |
| Three parallel clauses or images, everywhere | §2 rule of three |
| Paragraph openers 「其實…」「事實上…」; abstractions in quotation marks (「趨勢」「關鍵」「必然」) | §3 formula phrases |

## 5 Not signals in Chinese

Punctuation density and comma or period counts (§1: contradictory measures); long sentences counted in words (humans are longer); paragraph count (ChatGPT split *more*, the reverse of the folk belief that AI writes one block); word-frequency level (Z finds humans using commoner words, J finds LLMs doing so — two corpora, two eras, no rule). Mainland Chinese lexicon in a Taiwan venue (視頻、軟件、質量 for 影片、軟體、品質) is a register mismatch (worldsim 以 SETTING/CHAR_ 档案 venue 为准）, not an AI tell: fix it only when the venue is Taiwanese and the author's own samples do not use it.

## 6 Evidence boundary

One corpus, one model era, Simplified Chinese question answering, default un-prompted ChatGPT of 2023. No study measures 2024–2026 models on Chinese narrative or expository prose; J covers single-sentence jokes from four 2025 models and reports lexical richness (human 0.547 vs 0.384–0.461) but no sentence or punctuation statistics. No Taiwan academic study compares human and machine Traditional Chinese; the Taiwan sources above are editorial. Treat every number here as a direction observed once, not a calibration constant.
---

## 原文搬运出处：skills/sepia/references/rubric.md

# Diagnosis rubric — the 30 core features

The 30 narrative features below come from StoryScope's released taxonomy and corpus summary (AI-core and human-core tables 14–15; all-30 means and gaps, Table 16). StoryScope's Core Only 30-feature XGBoost held-out classifier reached 84.8% macro-F1 (AUPRC .828); this manual rubric is heuristic triage, not that classifier or an authorship detector. See [StoryScope arXiv v6](https://arxiv.org/abs/2604.03136v6) for the pinned study.

Use the Human and AI columns as corpus calibration references, not targets for an individual story. Observed signals are not authorship probabilities. This rubric makes no validated aggregate-detector or revision-threshold claim; any future aggregate claim requires a separate, documented evaluation.

## Protocol

1. Read **one group at a time**, in five separate passes. Never assess the whole rubric in one read: models self-evaluating text collapse onto one or two salient dimensions and go blind to the rest (measured on the slop taxonomy — span precision 0.13–0.16 across tested prompting conditions).
2. For each observed signal, quote the short passage that justifies it. No quote, no signal.
3. Record numeric, ordinal, and categorical observations beside the corpus references; do not convert them into authorship probabilities or a combined score.
4. Mark a feature **n/a** when the text offers no occasion to assess it, and record over-correction separately.

## Reading rules

| Case | Rule |
|---|---|
| Numeric rows (scale/ordinal) | Record the story's observed score and compare it qualitatively with the Human and AI corpus references. Do not apply a numeric cutoff. |
| Percentage rows (categorical/binary) | Record whether the AI-column option appears and quote its context. The corpus percentages are calibration context, not per-story probabilities or ratio cutoffs; absence of a human-leaning option is not itself a finding. |
| Group D | Record each human-positive marker separately with its quoted evidence. Do not collapse the markers into a group score. |
| Not applicable | A feature with no occasion in the text (no jeopardy → pre-threat investment; no reveal → recontextualization) is **n/a** and does not force a judgment. Reference explicitness is n/a only when the story makes no allusive gesture at all — an unnamed borrowed quotation or a recognizable unattributed retelling *is* an occasion (record it as implicit). Short texts produce several n/a — that is expected, not a defect of the story. |
| Over-correction | A numeric score at the far extreme *away* from the AI direction (e.g. discontinuity 5/5, thematic explicitness 1/5) → flag as **over-correction advisory**. Report it separately as a humanizer-fingerprint failure mode; do not reinterpret it as an AI-leaning signal. |

## Group A — Thematic over-determination (AI drifts high)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Thematic explicitness | 1 = themes stay implicit; 5 = thesis-like statements tell the reader how to interpret events | ~3.3 | 3.9 |
| Moral/philosophical weighting | How far ethical debate and thematic exposition outweigh story pleasure; check narrator commentary and climactic speeches | ~3.3 | 3.7 |
| Thematic unity | 5 = every scene, subplot, image reinforces one thematic core | ~4.4 | 4.7 |
| Narrator thematic commentary | Does the narrating voice generalize about what events mean ("That is how people are")? | yes in ~52% | 77% |
| Dialogue as philosophical debate | Do key dialogues argue ideas rather than advance want/conflict? | dominant in ~34% | 59% |
| Reference explicitness | Vague unnamed allusion as the dominant intertext mode (the human-leaning state is a balanced mix of named + implicit, 37% vs 16%) | implicit-only ~50% | 72% |

## Group B — Sensory & embodied performativity (AI drifts high)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Dominant emotion mode | Classify strong-affect scenes: explicit label / embodied sensation / behavior / ambiguous; flag embodied dominance as an AI-leaning signal | embodied dominant in ~38% | 81% |
| Setting as psychological mirror | Do weather/landscape/architecture consistently externalize inner states? | ~3.6 | 4.1 |
| Environmental emphasis | Landscape and ecology beyond backdrop | ~2.8 | 3.2 |
| Olfactory imagery | Smell among regularly engaged senses — judge salience relative to length (one prominent instance counts in flash-length text; recurring use in longer work) | ~57% | 82% |
| Sensory density | Proportion of text doing multi-sense description; 5 = lush, pace-slowing | ~3.7 | 3.9 |
| Depth of interior access | 1 = external only; 5 = stream of consciousness | ~3.7 | 3.9 |

## Group C — Structural streamlining (AI drifts high/tidy)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Causal-chain continuity | 5 = every event tightly linked in one line from incitement to end | ~3.9 | 4.2 |
| Subplots *(advisory signal)* | Absence of any subplot; too common in human stories (57%) to interpret without context | no-subplot ~57% | 79% |
| Resolution agency | Turning point triggered by protagonist choice vs chance/others | choice ~46% | 69% |
| Resolution mode | External act / internal acceptance / partial / open / catastrophic; flag internal acceptance as an AI-leaning signal | internal ~27% | 47% |
| Protagonist introduction | Device at first substantial appearance — one of: external description / in-action / in-dialogue / inner thought / others' reports. Flag external description as an AI-leaning signal; the other four are not signals by themselves (in-dialogue is the strongest human marker) | description ~30% | 52% |
| Opening spatial grounding | How completely the first scene fixes local + global place (1–4) | ~2.1 | 2.3 |
| Spatial granularity | Density of place names, rooms, routes (1–4) | ~2.3 | 2.5 |
| Pre-threat investment | Interiority/backstory built before jeopardy | ~2.8 | 3.0 |

## Group D — Human-positive markers

| Marker | How to judge | Human | AI |
|---|---|---|---|
| Named intertextuality | Any real text/author/work explicitly named | present in ~47% | 24% |
| Fourth-wall gesture | Any wink, aside, or reader acknowledgement anywhere | present in ~67% | 39% |
| Direct reader address | Any "you"/"dear reader" moment | present in ~28% | 7% |

## Group E — Temporal complexity & diversity (AI drifts low/tidy)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Chronological discontinuity | Frequency/sharpness of time jumps | ~2.4 | 2.1 |
| Anachrony intensity | Scene-level flashbacks/flash-forwards as structure | ~2.6 | 2.3 |
| Nonlinear framing for disclosure | Time devices used to stage revelations | ~2.0 | 1.7 |
| Recontextualization after surprise | How much earlier text a reveal recolors | ~3.3 | 3.0 |
| Location variety *(Sepia heuristic advisory)* | Optional editorial check: flag a 3,000+ word story that never leaves one locale unless the premise demands confinement | measured ordinal mean 1.34 | 1.08 |
| Dialogue proportion | Fraction of text in quoted speech (1 = none, 3 = balanced, 5 = dominates) | ~3.0 | 2.7 |
| Moral polarity toward protagonist | Narrative's final stance; flag a clearly affirmative or clearly condemning stance as an AI-leaning signal | ambivalent ~59% | clear 62% |

## Report format

Cite by quoting a short phrase, not by paragraph number. Keep the report descriptive: it records candidate signals for editorial review, not authorship probabilities or an aggregate action score.

```text
SEPIA DIAGNOSIS — <title>
Scope: heuristic triage; corpus references only; no authorship probability or validated aggregate detector
Group A: <row heading> — <quoted evidence>; …; n/a <row heading> …   (name every observed signal by its rubric row heading, verbatim)
Group B: observed signals … (…)
Group C: observed signals …; n/a … (…)
Group D: marker observations … (named intertextuality present — "…")
Group E: observed signals … (…)
Advisories: over-correction …; subplots …; single-location …
Quoted evidence: <short phrase for each reported signal>
Plan: <ordered fixes, deepest layer first, each tied to a quoted passage>
```
