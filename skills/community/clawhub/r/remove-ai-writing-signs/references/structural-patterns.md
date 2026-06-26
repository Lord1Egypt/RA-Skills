# Structural patterns — deep reference

This file catalogs 27 pattern families with extended examples and rewrite
strategies. Organized by the 5-pass architecture. Pass 2 (vocabulary)
patterns live in `vocabulary-by-era.md`.

## Contents

**Pass 1: Artifact removal**
- P01: Conversational framing — chatbot pleasantries to delete
- P02: Knowledge-cutoff disclaimers — "as of my last training update..."
- P03: Markup residue — citation tokens, UTM tags, fenced-code artifacts
- P04: Subject lines and templates — pasted email or wiki scaffolding

**Pass 3: Content deflation**
- P05: Significance inflation — abstract claims with no evidence
- P06: Superficial -ing analyses — trailing participle clauses adding nothing
- P07: Formulaic challenges and future — "despite X, Y faces challenges..."
- P08: Vague attributions — "experts argue," unnamed authorities
- P09: Notability assertion — listing outlets without saying what they reported
- P10: Promotional language — nestled, vibrant, world-class, in the heart of
- P11: Ecosystem/conservation padding — biology articles inflating connections

**Pass 4: Structural reconstruction**
- P12: Copula avoidance — "serves as" instead of "is"
- P13: Negative parallelisms — "not only X, but Y"
- P14: Rule of three — artificial triplets
- P15: Synonym cycling (elegant variation) — same entity, different names
- P16: Title Case headings — convert to sentence case
- P17: Inline-header lists — bold colon items that should be prose
- P18: Unnecessary tables — small tables prose handles better
- P19: Rigid outline structure — intro / background / challenges / future
- P20: Section summaries and conclusions — restated theses

**Pass 5: Texture injection**
- P21: Metronomic rhythm — uniform sentence length
- P22: Absence of opinion — every claim neutrally stated
- P23: False balance — "however" inserted where evidence is one-sided
- P24: Em dash overuse — register-dependent thresholds
- P25: Boldface overuse — mechanical bolding of keywords
- P26: Emoji decoration — emoji as bullet markers or section decorators
- P27: Curly quotes (weak signal) — see entry for nuance

---

## Pass 1 patterns: Artifacts

### P01: Conversational framing
**Detection:** First or last sentence contains chatbot pleasantries.
**Examples:**
- "I hope this helps! Let me know if you'd like more details."
- "Here is a comprehensive overview of sustainable energy."
- "Of course! Here's what you need to know about..."
- "Would you like me to expand on any of these points?"
- "Certainly! Let me break this down for you."

**Fix:** Delete entirely. Start with the first substantive sentence.

### P02: Knowledge-cutoff disclaimers
**Detection:** Phrases acknowledging AI limitations or gaps.
**Examples:**
- "As of my last knowledge update in January 2022..."
- "While specific details are limited in available sources..."
- "Based on available information..."
- "[Person] keeps much of their personal life private" (speculation)
- "The species likely supports..." (hedging on unknown facts)

**Fix:** Delete the disclaimer. Either state the fact with its date, or
remove the claim entirely if it's speculative.

### P03: Markup residue
**Detection:** Platform-specific code fragments.
**Catalog:**
- ChatGPT citations: `turn0search0`, `citeturn0search0`
- ChatGPT references: `contentReference[oaicite:N]{index=N}`
- ChatGPT attribution: `oai_citation:N`, `({"attribution":{"attributableIndex":"X-Y"}})`
- ChatGPT UTM: `utm_source=chatgpt.com`, `utm_source=openai`
- Copilot UTM: `utm_source=copilot.com`
- Grok: `referrer=grok.com`, `<grok-card data-id="..." data-type="citation_card">`
- Perplexity: `[attached_file:1]`, `[web:1]`
- Footnote markers: `↩`, `↩2`
- Placeholder dates: `2025-XX-XX`, `PASTE_URL_HERE`, `INSERT_SOURCE_URL`
- Fenced code blocks: ` ```wikitext ` artifacts

**Fix:** Delete all. If a citation is needed, find the actual source.

### P04: Subject lines and templates
**Detection:** Email-style subjects pasted into content.
**Examples:**
- "Subject: Request for Permission to Edit..."
- "Dear Wikipedia Editors, I hope this message finds you well."
- "Here's a template for your wiki user page."

**Fix:** Delete or convert to appropriate format.

---

## Pass 3 patterns: Content deflation

### P05: Significance inflation
**Detection:** Abstract claims about importance with no evidence.
**Signal phrases:** "marking a pivotal moment in the evolution of",
"a significant shift toward", "part of a broader movement",
"indelible mark on", "shaping the future of", "setting the stage for",
"key turning point", "focal point", "deeply rooted"

**Before:**
> The founding of Idescat represented a significant shift toward regional
> statistical independence, enabling Catalonia to develop a statistical
> system tailored to its unique socio-economic context. This initiative was
> part of a broader movement across Spain to decentralize administrative
> functions.

**After:**
> Catalonia established Idescat to run its own surveys and publish regional
> data without depending on Spain's national statistics agency. Other
> Spanish regions created similar institutes around the same time.

**Strategy:** Extract the specific fact buried inside the inflation.
"Significant shift toward regional statistical independence" = 
"run its own surveys." Say that.

### P06: Superficial -ing analyses
**Detection:** Trailing present-participle clauses that add no information.
**Signal constructions:**
- "...highlighting/underscoring/emphasizing its importance/significance"
- "...ensuring/reflecting/symbolizing its ongoing/enduring..."
- "...contributing to/cultivating/fostering..."
- "...showcasing/encompassing/aligning with..."

**Before:**
> The inscriptions record the names of key craftsmen, highlighting the
> collaborative nature of mosque construction and emphasizing the
> contributions of skilled artisans.

**After:**
> The inscriptions name the craftsmen: mason Ahmad b. Muhammad and
> tile-cutter Hajji Muhammad from Tabriz.

**Strategy:** The -ing clause usually restates the sentence in vaguer terms.
Delete it and check if meaning survives. It almost always does.

### P07: Formulaic challenges and future
**Detection:** "Despite X, Y faces challenges... Despite these challenges..."
followed by vague optimism or future speculation.

**Before:**
> Despite its industrial and residential prosperity, Korattur faces
> challenges typical of urban areas, including traffic congestion and
> water management issues. With its strategic location and ongoing
> initiatives, Korattur continues to thrive as an integral part of the
> Ambattur industrial zone.

**After:**
> Korattur has traffic congestion and seasonal water shortages, problems
> common in Chennai's industrial suburbs.

**Strategy:** Cut the "despite" framing. State the challenges directly.
Delete the vague positive ending unless it has specific support.

### P08: Vague attributions
**Detection:** Claims attributed to unnamed authorities.
**Signal phrases:** "Experts argue", "Industry reports suggest",
"Observers have cited", "Studies show", "Some critics argue",
"several publications" (when citing few), "widely regarded"

**Before:**
> Due to its unique characteristics, the river is of interest to
> researchers and conservationists. Efforts are ongoing to monitor its
> ecological health.

**After:**
> A 2021 survey by the Mongolian Academy of Sciences found three
> undescribed fish species in the river's upper reaches.

**Strategy:** Either name the source or delete the claim. If you don't know
the source, flag it for the author to fill in or remove.

### P09: Notability assertion
**Detection:** Listing media outlets without saying what they reported.
Also: "maintains an active social media presence", "independent coverage",
"profiled in".

**Before:**
> She has been featured in Vogue, Wired, Toronto Star, and other media
> outlets. Her insights have also been featured in Refinery29 and other
> prominent media outlets.

**After:**
> In a 2024 Wired interview, she argued that AI governance should
> prioritize outcomes over input controls.

**Strategy:** Pick the most substantive source. Say what it actually
reported. Drop the laundry list.

### P10: Promotional language
**Detection:** Tourism-brochure or press-release tone.
**Signal words:** nestled, breathtaking, stunning, renowned, world-class,
boasts, vibrant, rich cultural heritage, diverse tapestry, commitment to
excellence, natural beauty, in the heart of, groundbreaking, featuring,
diverse array, captivates

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata
> Raya Kobo stands as a vibrant town with a rich cultural heritage and a
> significant place within the Amhara region.

**After:**
> Alamata Raya Kobo is a market town in the Gonder area of Ethiopia's
> Amhara region, with about 12,000 residents.

**Strategy:** Strip every adjective that isn't earned by a specific fact.
Replace "vibrant" with a population number. Replace "rich cultural
heritage" with the name of an actual cultural element.

### P11: Ecosystem/conservation padding
**Detection:** In biology articles, overemphasis on ecosystem connections
and conservation status, especially when status is unknown.

**Before:**
> Currently, there is no specific conservation assessment by the IUCN.
> However, the general health of the Lake Malawi ecosystem is crucial for
> the survival of this and other endemic species. Factors such as
> overfishing, pollution, and habitat destruction could potentially impact
> their populations.

**After:**
> The IUCN has not assessed the species. It is endemic to Lake Malawi.

**Strategy:** If conservation status is unknown, say so in one sentence.
Don't speculate about hypothetical threats.

---

## Pass 4 patterns: Structural reconstruction

### P12: Copula avoidance
**Detection:** AI replaces "is/are/has" with elaborate constructions.
**Documented decrease:** >10% drop in "is" and "are" usage in academic
writing after 2023 (Geng & Trotta, 2025).

| AI construction | Human equivalent |
|-----------------|------------------|
| serves as | is |
| stands as | is |
| functions as | is |
| marks / represents | is / was |
| holds the distinction of being | is |
| boasts | has |
| features | has / includes |
| offers | has / provides |
| ventured into politics as a candidate | was a candidate / ran for office |

### P13: Negative parallelisms
**Detection:** "Not just X, but Y" / "Not only X, but also Y" /
"It's not X, it's Y" / "No X, no Y, just Z"

**Before:**
> Self-Portrait constitutes not only a work of self-representation, but a
> visual document of her obsessions and psychobiographical narratives.

**After:**
> The Self-Portrait documents Kusama's obsessions through visual
> repetition and pattern.

**Strategy:** Identify which claim matters more — X or Y. Usually the text
only needs one of them.

### P14: Rule of three
**Detection:** Ideas artificially grouped into triplets.

**Before:**
> The conference brings together SEO professionals, marketing experts, and
> growth hackers to discuss the latest trends. The event features keynote
> sessions, panel discussions, and networking opportunities.

**After:**
> The conference runs talks and panels for digital marketers, with
> informal networking between sessions.

**Strategy:** Merge, cut, or expand. Two items is fine. Four is fine.
The number should match the content, not a rhetorical template.

### P15: Synonym cycling (elegant variation)
**Detection:** Same entity called by different names in consecutive sentences.

**Before:**
> Yankilevsky faced obstacles in expressing his creativity. The
> non-conformist artist struggled against state norms. These creative
> individuals found ways to work around censorship.

**After:**
> Yankilevsky faced state censorship. He worked around it by exhibiting
> privately and circulating work through samizdat networks.

**Strategy:** Pick one term. Use pronouns naturally. Humans repeat words;
AI avoids them.

### P16: Title Case headings
**Detection:** Every Main Word Capitalized In Headings.

**Fix:** Convert to sentence case (capitalize first word and proper nouns).
Exception: titles of works, proper names.

### P17: Inline-header lists
**Detection:** Lists where each item starts with a bold header and colon.

**Before:**
> - **SEO:** Traditional methods for improving visibility
> - **AEO:** Techniques for voice assistants
> - **GEO:** Strategies for LLM citations

**After:**
> The framework covers three areas: traditional search optimization (SEO),
> voice assistant targeting (AEO), and optimization for AI-generated
> responses (GEO).

### P18: Unnecessary tables
**Detection:** Small tables (<5 rows, <3 cols) where prose works better.

**Before:**
> | Metric | Figure |
> | Market Valuation | ~USD 2.1 billion |
> | Major Facilities | NLDB, CBR, THSTI |

**After:**
> India's biobanking market was valued at roughly $2.1 billion in 2024,
> with major facilities including the NLDB, CBR Biobank, and THSTI.

### P19: Rigid outline structure
**Detection:** Articles that follow: Introduction → History → Significance
→ Challenges → Future Outlook → Conclusion.

**Fix:** Reorganize around the most interesting or important aspects of the
topic. Not every article needs the same skeleton.

### P20: Section summaries and conclusions
**Detection:** Sections that restate the article's thesis: "In summary...",
"In conclusion...", "Overall..."

**Fix:** Delete unless the text is long enough (>3000 words) that a
summary genuinely helps the reader. Even then, add new information or
a forward-looking specific claim, not a restatement.

---

## Pass 5 patterns: Texture injection

### P21: Metronomic rhythm
**Detection:** Sentences cluster around the same word count (low CoV).
AI typically produces sentences of 15-25 words with little variation.

**Fix:** Introduce deliberate variation. A 5-word sentence. Then a
40-word sentence with a subclause and a parenthetical aside. Then a
medium one. The rhythm should feel like breathing, not a metronome.

### P22: Absence of opinion
**Detection:** Every claim is stated neutrally with no authorial stance.

**Fix:** Where appropriate to the genre, add evaluative language: "the
results were mixed", "this approach has obvious limitations", "the data
is thin but suggestive". This is context-dependent — encyclopedia prose
should be neutral, but blog posts, analyses, and reports benefit from
authorial voice.

### P23: False balance
**Detection:** "On the other hand" / "However" inserted to create
artificial balance when evidence is one-sided.

**Fix:** If the evidence is clear, state the conclusion. Mention
dissent only if it is substantive and sourced.

### P24: Em dash overuse
**Detection:** More than 1 em dash per 500 words. AI uses them to
create punchy, sales-like rhythm.

**Fix:** Replace most with commas, parentheses, or sentence breaks.
Keep em dashes only for genuine parenthetical insertions that benefit
from strong separation.

### P25: Boldface overuse
**Detection:** Mechanical bolding of terms throughout the text, especially
every instance of a keyword.

**Fix:** Remove most boldface. Bold only the first mention of a defined
term, or use it for genuine emphasis (sparingly).

### P26: Emoji decoration
**Detection:** Emoji used as bullet markers or section decorators.

**Fix:** Remove all emoji from headers and list markers. Keep only if the
text is genuinely casual (chat, social media) and the emoji adds meaning.

### P27: Curly quotes (weak signal — handle with care)
**Detection:** Unicode curly quotes ("...") or curly apostrophes (') in
contexts where straight quotes are standard.

**Signal strength:** Weak and getting weaker. Curly quotes are the default
output of macOS keyboards, Microsoft Word, Google Docs, iOS keyboards, and
many CMS platforms. A document with curly quotes is overwhelmingly more
likely to have been touched by one of those tools than to be unedited AI
output. ChatGPT and DeepSeek do tend to emit curly quotes; Claude and
Gemini typically use straight. But none of that is conclusive on its own.

**Fix:** Do not treat curly quotes as evidence of AI on their own. Only
correct them when:
- The context is code or technical (where straight quotes are required)
- The target publication's style guide mandates straight quotes
- Curly quotes appear inconsistently mid-document (a real AI tell — humans
  and tools are usually consistent)

Otherwise leave them alone. Aggressively swapping curly for straight in
prose looks like a process artifact, not a humanization.

---

## Compound pattern: The AI paragraph

The most detectable AI pattern is not any single tell — it's the
combination. A classic AI paragraph looks like:

> [Significance claim] + [Promotional language] + [Vague attribution] +
> [Trailing -ing clause] + [Rule of three] + [Generic conclusion]

Example:
> The temple serves as a testament to the region's rich cultural heritage,
> highlighting the enduring legacy of traditional craftsmanship.
> Experts have noted its significance in fostering community bonds,
> showcasing architectural innovation, and preserving historical memory.
> The future of this landmark looks promising as restoration efforts
> continue.

Rewritten:
> The temple was built in 1847 using local sandstone. A 2019 restoration
> project repaired the eastern wall, which had been crumbling since the
> 1960s. The project cost $2.3 million and took three years.

The rewrite replaces six patterns with three specific facts. That's the
entire method in miniature.
