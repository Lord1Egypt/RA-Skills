# AI Writing Signs Reference

Source: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

This reference adapts the Wikipedia field guide into a general writing-audit checklist. The original page is Wikipedia-specific and describes observations, not proof. Use it to find editing risks, not to accuse authors.

## Core Caution

- Style signs are probabilistic signals, not proof of AI authorship.
- AI detectors and human intuition both have false positives.
- Many signs also appear in marketing copy, essays, non-native English, corporate prose, SEO writing, and human-edited AI-assisted drafts.
- The useful goal is better writing: specificity, source integrity, grounded claims, and natural voice.

## High-Signal Artifacts

These are stronger findings because they are less likely to be ordinary prose:

- Chatbot residue: phrases that address the user, mention a knowledge cutoff, refer to "provided sources", or explain how to submit/edit the text.
- Placeholder text: fill-in fields, bracketed instructions, fake dates, "insert source here", "your name", or unfinished template language.
- Citation residue: `turn0search0`, `oai_citation`, `contentReference`, `utm_source=chatgpt.com`, `utm_source=openai`, unused named references, or citation markup that does not resolve.
- Broken markup: Markdown pasted into a target format that does not support it, malformed templates, hallucinated categories, or bogus policy/reference shortcuts.
- Source anomalies: fabricated-looking citations, irrelevant links, invalid DOI/ISBN/PMID-style references, sources that do not support the claim, or book citations with no usable locator when a locator is required.

## Content Tells

Look for clusters, not isolated examples:

- Significance inflation: ordinary details are framed as pivotal, vital, enduring, transformative, or part of a broader legacy without evidence.
- Generic "broader trend" claims: the text keeps zooming out to global impact, cultural heritage, innovation, resilience, ecosystems, or future prospects without concrete support.
- Superficial analysis: added clauses explain what a fact "highlights", "reflects", "underscores", "symbolizes", or "contributes to" without a real source or argument.
- Promotional tone: travel-guide, press-release, brand, founder, product, or tourism language appears where neutral prose is expected.
- Vague attribution: "experts say", "observers note", "industry reports suggest", "critics argue", or similar claims appear without specific attribution.
- Notability theatre: the text tries to prove importance by listing media coverage or source types instead of stating sourced facts directly.
- Future-prospects filler: sections end with generic challenges, opportunities, innovation, expansion, or ongoing relevance.

## Language Tells

Words are weak alone but useful in dense clusters:

- Overused vocabulary: additionally, align with, boasts, bolstered, crucial, delve, enduring, enhance, fostering, garner, highlight, interplay, intricate, key, landscape, meticulous, pivotal, robust, showcase, tapestry, testament, underscore, valuable, vibrant.
- Inflated verbs replacing simple ones: "serves as", "stands as", "marks", "represents", "features", "offers", "maintains", "refers to".
- Negative parallelisms: "not just X but also Y", "not only X but Y", "rather than X, Y", or similar contrast patterns used repeatedly.
- Rule-of-three phrasing: repeated triplets that sound balanced but add little precision.
- Elegant variation: forced synonym swapping to avoid repeating the correct concrete noun.

## Style And Formatting Tells

- Title-case headings where sentence case or ordinary headings would fit better.
- Excessive boldface or "key takeaway" styling.
- Inline-header vertical lists: bullet plus bold phrase plus colon plus explanation, repeated mechanically.
- Heavy em-dash use, especially spaced dashes used to punch up clauses.
- Unnecessary small tables where prose would be clearer.
- Curly quotation marks or unusual punctuation pasted into a context that normally uses plain characters.
- Markdown artifacts in non-Markdown contexts.
- Emoji or decorative formatting in serious prose.

## Comment Or Discussion Tells

- Canned civility language: repeated assurance of good faith, quality, neutrality, policy compliance, or willingness to receive constructive feedback.
- Excessive policy/legalistic framing that sounds generated rather than responsive to the actual issue.
- Generic complaints that accusations are speculative without addressing concrete text problems.
- Plain-text section headers that segment a comment like a generated memo.

## False-Positive Guards

- Do not flag a single word as meaningful by itself.
- Do not treat polished grammar as suspicious.
- Do not treat all em dashes as suspicious.
- Do not treat non-native English, formal education style, corporate writing, or translation residue as AI by default.
- Do not remove useful structure just because LLMs can produce structure.
- Do not make a provenance claim unless there is direct evidence beyond style.

## Practical Fixes

- Replace abstract importance with concrete consequence.
- Replace generic adjectives with observable details.
- Replace inflated verbs with direct verbs.
- Remove filler conclusions that summarize without adding information.
- Verify all citations, links, identifiers, and claims.
- Keep distinctive voice, compression, opinion, or friction when it serves the piece.
- Prefer the user's actual point over smooth neutrality.
