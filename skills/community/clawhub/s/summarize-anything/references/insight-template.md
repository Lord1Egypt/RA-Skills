# Insight Quality

This file defines the minimum analytical work a strong memo should do.
It is not primarily a section template.

## Long-Form Rule

If the source is long-form, expand the memo instead of compressing it into a few bullets.

Treat anything roughly over 90 minutes or clearly multi-topic as long-form unless the user explicitly asks for a short summary.

## Minimum Analysis Actions

For long-form interviews or conversations, the final memo must do more than summarize topics.

It should:

- identify the source's real central question, not just its visible topics
- explain the speaker's actual answer to that question
- identify a few cross-cutting patterns that recur across different parts of the source
- explain what larger narrative, assumption, or worldview the speaker seems to be reinforcing or pushing against
- connect biographical details, research choices, and stated beliefs into causal or interpretive links where supported by the source
- surface implications that are useful beyond this one conversation
- explain why specific moments matter instead of merely noting that they occurred
- distinguish between the speaker's explicit claims and the deeper frame those claims imply
- identify what the speaker is reacting against, not just what the speaker advocates
- assess which parts of the argument are robust, under-argued, romanticized, or strategically useful
- identify what remains unresolved, weakly supported, or strategically framed

## What Counts As Insight

A strong insight is not a restatement of a point made in one passage.

A strong insight usually does at least one of the following:

- synthesizes multiple moments into a higher-level claim
- identifies an unstated pattern behind explicit remarks
- explains why a detail matters rather than merely noting it
- translates biography or anecdote into a broader model of how the speaker thinks or decides
- connects one strand of the conversation to another that the speaker did not explicitly tie together

## Shallow Outputs To Avoid

- chapter-by-chapter recap with little synthesis
- bullet lists that merely restate claims already explicit in the source
- generic praise of the speaker without identifying what is structurally distinctive
- isolated observations that are not connected into a broader interpretation
- summaries that name topics but do not explain the speaker's deeper logic
- polished paraphrases that improve clarity but do not add judgment
- writing that feels like a table of contents with commentary

## Depth Guardrail

- Short content can use a compact memo.
- Long content should surface enough structure that a reader can recover the flow of the original conversation without reading the full transcript.
- If chapters or timestamps exist, use them.
- If chapters do not exist, infer major segments from topic shifts.
- For multi-hour interviews or podcasts, the default answer should feel like a serious analytical briefing, not a teaser.
- Go beyond topic listing. Explain why major sections matter, how the arguments connect, and where the deepest tensions are.
- Name the strongest claims, supporting logic, hidden assumptions, and implications.
- If the speaker is pushing against a dominant narrative, explain both the critique and the alternative worldview.
- If the source exceeds roughly 3 hours, the memo should usually recover:
  - a top-level thesis
  - the central question being answered
  - the conversation arc
  - several cross-cutting patterns, tensions, or recurring contrasts
  - contradictions, speculative leaps, or unresolved questions
  - audience-specific implications when relevant
- Do not compress a 4-8 hour source into a few paragraphs unless the user explicitly asks for brevity.
- Prefer synthesis over coverage, but never lose the spine of the source.
- Analytical density matters more than length. A long memo that mostly recaps is still shallow.

## Format Flexibility

- You do not need to force a fixed heading structure if another structure serves the source better.
- Chronological breakdowns are useful, but they are not sufficient by themselves.
- Use whatever structure best supports synthesis, interpretation, and decision-relevant takeaways.

## Preferred Editorial Shape

- For detailed summary requests, especially in Chinese, prefer an editorial long-form shape rather than a memo that reads like internal notes.
- A strong default shape is:
  - a short framing paragraph
  - `总摘要`
  - a detailed analytical breakdown organized by major content arcs, layered themes, or argument clusters
  - a short closing synthesis such as `最核心的观点`, `最有价值的地方`, or `值得注意的局限`
- The opening paragraph should quickly answer:
  - what the source appears to be about
  - what it is really about
  - what answer the speaker or source ultimately gives
- Prefer prose-first writing. Use bullets to compress enumerations, not as the main delivery vehicle unless the user asks for a list.
- Section headings should sound interpretive and human, not like machine labels or timestamp buckets.
- The result should feel like a strong edited article or analytical feature, not a transcript recap with formatting.

## Delivery Guardrail

- Put the main analysis directly in the response body.
- Mention transcript files after the analysis when relevant.
- Do not replace the analysis with "I saved a memo to a file" unless the user explicitly asked for that format.
- When the user asked for a detailed summary, bias toward more explanation and interpretation than terseness.
- When useful, anchor an interpretation in 2-4 representative moments from different parts of the source instead of relying on one local passage.

## Recommended Deep Memo Moves

Use several of these for long-form interviews:

- identify the source's main argumentative spine before describing its parts
- reconstruct the speaker's worldview in plain language
- identify a repeated contrast, such as "what the speaker rejects" versus "what the speaker wants instead"
- connect early biographical material to later technical or strategic claims
- separate durable beliefs from situational opinions
- explain what is signal versus what may be style, branding, or performance
- name where the conversation is rhetorically strongest and where it outruns its evidence
- distinguish between the person's self-narrative and the deeper structure revealed by the conversation
- identify which passages are doing real conceptual work versus branding, mood-setting, or myth-making

## Style Failure Modes To Avoid

- writing that sounds like a cleaned transcript with headings
- a section-per-chapter format that never steps back to say what the whole conversation is doing
- repetitive phrasing such as "the speaker then said" or "next they discussed"
- analysis that is technically correct but emotionally flat, with no sense of why the source is worth reading
- overusing bullets when connected prose would produce a more convincing argument

## For Codex / OpenClaw Users

When relevant, add:

- workflow takeaways
- agentic or tool-use takeaways
- memory, long-context, evaluation, or automation implications
- operational suggestions that can be tried immediately

## Personalization

Use personalization only when supported by:

- explicit user instruction in the current prompt
- or a trusted memory artifact available in the environment

If there is no reliable signal, write the best general insight memo instead.
