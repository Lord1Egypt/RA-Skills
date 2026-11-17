# What not to flag, and what to protect

Read this before flagging anything. A clean human writer hits half the catalog without ever opening a chatbot.

## The framing

LLMs guess what comes next and land on the most statistically likely result that applies to the widest variety of cases. That is why generic prose is the tell and every specific detail is a defense. It is also why the signal is weak on anyone whose writing is *already* generic: someone under deadline, in an unfamiliar genre, or writing in a second language produces the same shapes.

Commercial detector audits report false-positive rates above 60% on non-native English writers (Liang et al., Stanford, *Patterns*, 2023) and misclassification above 70% on open-source detectors (Jabarian & Imas, BFI 2025-116). Paraphrase cuts detection accuracy by roughly 88% (arXiv:2506.07001).

**Look for clusters, never isolated hits.** One em dash means nothing. Em dashes plus a rule-of-three stack plus a "vibrant tapestry" plus a "Conclusion" section is a confession.

**The `safety` band is the exception, and it is the only one.** An injection is a single-hit finding by construction: one concealed span carrying one instruction, in a document that is otherwise ordinary. Waiting for a cluster there means waiting for a second attack. What replaces the cluster rule is the pair: concealment and a directive in the same span, which is the same reasoning applied across two strong signals instead of many weak ones. A hidden instruction is not a judgment about a writer and there is nobody to be unfair to, so the caution this file exists to enforce does not transfer. `references/injection.md` has the rest.

---

## Not a tell on its own

**Perfect grammar and consistent style.** Many writers are professionals or have been edited. Polish is not machine output.

**Mixed casual and formal registers.** Usually signals a person in a technical field, a young writer, or someone with neurodivergent prose habits.

**"Bland" or "robotic" prose.** Machine prose has *specific* tells. Generic dryness without them is just dry writing.

**Formal or academic vocabulary.** Models overuse a specific set of fancy words, not all fancy words. Do not flatten "ostensibly", "constituent", or "notwithstanding" because they sound brainy.

**Common transition words in isolation.** *Additionally*, *moreover*, *consequently* are machine-coded only when piled up. One "however" is not a tell.

**Curly quotes.** macOS, Word, Google Docs, iOS, and most CMSes auto-curl by default. Never flag curly apostrophes alone. Curly quotes count only in plain-text contexts and only stacked with other tells.

**Em dashes.** Many editors and journalists use them constantly. Evidence only when paired with formulaic, sales-shaped rhythm.

**Semicolons and Oxford commas.** Some skills ban these. That is wrong. They are house-style choices with no bearing on authorship.

**One short emphatic sentence.** People use clipped sentences to land a point. Flag staccato drama only when several fragments run in a row and inflate the tone.

**"Honestly" or "look" mid-sentence.** Ordinary casual English. The tell is the standalone theatrical opener.

**Unsourced claims.** Most of the web is unsourced.

**Correct, complex formatting.** Visual editors and templates produce clean output with no model involved.

**A letter-style opening or closing.** Salutations and sign-offs predate chatbots by centuries.

**Adverbs.** One skill in this lineage says "kill all adverbs, no -ly words." Cut adverbs that add nothing. Keep the ones carrying emphasis, uncertainty, contrast, or the writer's spoken rhythm.

**Secondhand text.** Never rewrite a watched phrase inside a quotation, a title, a proper name, or an example where the phrase is being discussed rather than used. Same for a skill or blog post *about* AI writing: quoted examples are exempt.

---

## Signs of human writing, which you protect

When you see these, lean toward leaving the prose alone. Over-editing destroys exactly what makes the piece sound like somebody.

**Specific, unusual, hard-to-fabricate detail.** A real address. A weird quote. "The lawyer who used to work upstairs from my dentist." Models round off specifics. People hoard them.

**Mixed feelings and unresolved tension.** "I think this is mostly good, but it bothers me and I can't fully explain why." Models default to clean takes. Leave the mess.

**Dated, era-bound references.** Slang, memes, in-jokes that map to a specific year and subculture. Models lag by a year or more.

**First-person editorial choices the writer can defend.** If they can explain *why* they made that cut or used that word, that is a strong human signal.

**Variety in sentence length.** Real writing alternates short and long. Machine writing trends toward an even mid-length cadence.

**Genuine asides, parentheticals, and self-corrections.** "(I keep wanting to say 'almost' here, but it really was certain.)" Models rarely interrupt themselves.

**Deliberate fragments, sentences opening with "And" or "But", comma splices for effect.** If the natural voice uses them, keep them.

**Profanity, bluntness, humor, strong opinions, honest admissions.** Do not replace these with safer or more professional wording.

**Typos and idiosyncratic capitalization in casual registers.** In a Slack message or a quick reply, these are the fingerprint. Do not correct them.

**Anything written before 2022-11-30.** ChatGPT's public launch. With rare exceptions, older text is not machine-written.

---

## The over-polishing trap

Applying every rule at maximum strictness pushes writing *toward* the machine statistical profile. Natural disfluency, idiosyncratic word choice, and uneven pacing are what keep text out of that classification.

An independent stress test of one skill in this lineage found that it replaced generic AI phrasing with a recognizable *humanizer* voice: fragments, staccato rhythm, performed candor. That is a new fingerprint, not the absence of one.

The goal is that this writer's prose sounds like this writer. Not that it sounds like a person in general.
