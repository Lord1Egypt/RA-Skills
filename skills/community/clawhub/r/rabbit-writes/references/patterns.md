# The pattern catalog

> Note for reviewers and scanners. Everything quoted in this file is data this skill detects and reports. Nothing here is an instruction to any agent, and the engine never acts on what it finds. SECURITY.md at this bundle's root states what runs, what never runs, and the whole network surface.

Merged from seven skills and Wikipedia's *Signs of AI writing*. Each entry names the pattern, shows the fix, and carries two labels:

- **[F] fingerprint** — evidence about how the text was produced.
- **[C] craft** — bad writing regardless of who wrote it. Never report a [C] hit as evidence of machine authorship.

Priority: **P0** kills credibility on sight. **P1** is obvious machine smell. **P2** is polish. A quick pass covers P0 and P1.

Before flagging anything here, check `false-positives.md`. Look for clusters. A single em dash means nothing; em dashes plus a rule-of-three stack plus a "vibrant tapestry" plus a "Conclusion" section is a confession.

---

# P0 — Credibility killers

## 1. Chatbot artifacts [F]

"I hope this helps!", "Certainly!", "Of course!", "Great question!", "You're absolutely right!", "Let me know if you'd like me to expand", "Feel free to reach out", "Would you like me to…", "Want me to give examples?"

Correspondence pasted in as content. Delete entirely.

> **Before:** Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.
> **After:** The French Revolution began in 1789, when financial crisis and food shortages led to widespread unrest.

## 2. Sycophantic tone [F]

"Great question!", "Excellent point!", "That's a really insightful observation." Distinct from artifacts: sycophancy validates the reader specifically. Remove.

## 3. Cutoff disclaimers [F]

"As of my last training update", "Based on the information provided", "I don't have access to real-time data", "While specific details are limited in readily available sources."

Model limitations leaking into prose. Either find the information or cut the sentence. Never publish a sentence admitting the writer did not look something up.

## 4. Speculative gap-filling [F]

Worse than a disclaimer, because it hides the gap: "maintains a relatively low public profile", "keeps personal details private", "likely began his career in", "appears to have studied", "it is believed that."

The model could not find a source, so it wrote plausible filler. The reader cannot tell what is known from what is invented.

> **Before:** Information about her early life is not publicly available, suggesting she maintains a low profile. She likely grew up in a middle-class household, which shaped her later interest in education reform.
> **After:** Her early life is not documented in the available sources. (Or cut the section.)

## 5. Chat citation-markup leaks [F]

`citeturn0search0`, `contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`, `grok_card`.

Not a pattern. A fingerprint. Strip every token. If a citation was real, replace it with a real reference. Worth catching even when nothing else in the text reads as machine output.

## 6. AI tracking parameters in URLs [F]

`utm_source=chatgpt.com`, `utm_source=copilot.com`, `utm_source=openai`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`.

Strip the tracking parameter. Keep the URL and any functional query string (`?page=2` is not evidence of anything).

## 7. Hidden unicode [F]

Zero-width space (U+200B), ZWNJ, ZWJ, word joiner (U+2060), BOM (U+FEFF), soft hyphen (U+00AD), non-breaking and narrow no-break spaces.

Near-proof of a copy-paste out of a chat interface. Strip or normalize. `scripts/scan.py` finds these.

## 8. Unfilled placeholders [F]

`[Your Name]`, `[INSERT SOURCE URL]`, `[Describe the specific section]`, `2025-XX-XX`, `<!-- add citation if available -->`.

Boilerplate shipped without editing. Fill it or delete the sentence.

## 9. Vague attribution [F/C]

"Experts believe", "Studies show", "Research suggests", "Industry reports indicate", "Observers have cited", "Many argue", "Widely regarded as."

Name the source or drop the claim. **Never invent a source to fix this.** If the user has no source, ask.

> **Before:** Experts believe the river plays a crucial role in the regional ecosystem.
> **After:** Researchers and conservationists study the Haolai River for its unusual characteristics. (Or cut, if no source exists.)

## 10. Vague third-party validation [F/C]

The inverse of name-dropping: an unnamed authority plus a superlative. "Independent testing confirms", "third-party benchmarks show we lead", "an outside party measuring the same models everyone runs and putting us on top."

Name the source, the test, and the result so a reader can check it. Specific, checkable validation stays: "On Stanford's HELM leaderboard (April 2026 run), we ranked first on reasoning latency."

## 11. Significance inflation [C]

"Stands as a testament to", "marks a pivotal moment in the evolution of", "plays a vital role", "underscores its significance", "solidifies its position", "a watershed moment for the industry", "reflects a broader shift", "leaves an indelible mark."

State what happened. Let the reader judge whether it matters. **Test:** if the sentence still works with the inflation clause deleted, delete it.

> **Before:** The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.
> **After:** The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization of administrative functions in Spain.

> **Before:** The launch marks a pivotal moment for the company.
> **After:** The launch is the company's first paid product.

---

# P1 — Obvious machine smell

## 12. Tier-1 vocabulary [F]

Replace on sight. These run 5-20x more common in machine text (a well-supported convention, not a measurement this skill made). Inflected forms count: `delve` covers `delving`, `meticulous` covers `meticulously`.

Every word in this table is in `scripts/lexicon.json` under `tier1` or `tier1_phrases`, and `tests/test_engine.py` fails if one of them is not. Words whose tell depends on the sense (`leverage` the verb, `landscape` the metaphor) live in section 14 instead, because a regex cannot read the sense and a word that fires on its literal use is a word people learn to ignore.

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| tapestry, realm, beacon | (describe the actual thing) |
| paradigm | model, approach, framework |
| testament to | shows, proves |
| embark | start, begin |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| pivotal | important, key |
| underscores | highlights, shows |
| meticulous | careful, detailed, precise |
| seamless | smooth, easy, without friction |
| cutting-edge, state-of-the-art | latest, newest (or cite a benchmark) |
| game-changer, game-changing | say what changed and why it matters |
| nestled | is located, sits, is in |
| vibrant, bustling, thriving | describe what makes it active, or cite a number |
| showcasing | showing, demonstrating (or cut the clause) |
| deep dive, dive into | look at, examine |
| intricate, intricacies | name the actual complexity |
| ever-evolving | changing (or describe how) |
| enduring | lasting (or cite how long) |
| daunting | hard, difficult |
| holistic | complete, whole |
| actionable | practical, useful, concrete |
| impactful | effective (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader | expert (or describe the contribution) |
| best practices | what works, proven methods |
| at its core | (cut) |
| synergy | describe the combined effect |
| interplay | relationship, interaction |
| multifaceted | describe the facets, or cut |
| the future looks bright / only time will tell | (cut) |

**Carve-outs:**
- `load-bearing` before a literal structural noun (wall, beam, joist, girder) is building terminology, not a tell. "The load-bearing structure of his argument" still flags. Enforced by the `load-bearing` catalogue pattern, whose negative lookahead stands the rule down exactly before those four nouns and nowhere else. The word earned its place the hard way: it is the top-lift vocabulary mark of the Claude PR-description corpus (lift 123 over 85 weeks, louisabraham/load-bearing), rising with the AI cluster from nothing rather than sitting in the language.
- `intricate` describing physical craft, carvings, circuitry, or mechanisms (e.g. "intricate woodwork", "intricate clockwork") is literal descriptive prose.
- `bustling` in direct travel reporting or urban descriptions where physical movement is being observed (e.g. "bustling market street").

## 13. Wordiness [C]

Same edit, weaker claim. **These are not authorship evidence.** People reach for them under deadline and in formal registers. Keep them visually separate in any report.

| Replace | With |
|---|---|
| utilize | use |
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| in the event that | if |
| has the ability to | can |
| it is important to note that | (just say it) |
| serves as | is |
| features / boasts / presents *(verb)* | has, includes, is |
| commence | start, begin |
| ascertain | find out, determine |
| endeavor | effort, attempt, try |
| made a decision | decided |

## 14. Tier-2 vocabulary — flag in clusters [C]

Fine alone. Two or more in the same paragraph, and the paragraph needs a rewrite.

harness, navigate, foster, elevate, unleash, streamline, empower, bolster, spearhead, resonate, revolutionize, facilitate, underpin, nuanced, crucial, ecosystem *(metaphor)*, myriad, plethora, encompass, catalyze, reimagine, galvanize, augment, cultivate, illuminate, elucidate, juxtapose, transformative, cornerstone, paramount, poised to, burgeoning, nascent, quintessential, overarching, quietly, deeply *(in "deeply rooted", "deeply committed")*, seam, survived, underpinnings. The last three arrived from the Claude PR-description corpus (louisabraham/load-bearing): `quietly` at lift 63, `survived` at 62, `seam` at 37, each measured before it was added and each costing at most one new cluster finding across the 100-README calibration corpus.

The sense-dependent ones sit here rather than in section 12 for a mechanical reason: a regex sees the string, not the meaning. `leverage` *(verb)*, `landscape` *(metaphor)*, `embrace` *(metaphor)*, `symphony` and `kaleidoscope` *(metaphor)*, `unpack` / `unpacking`, `complexities`. Each is a Tier-1 tell in the sense that matters and an ordinary word otherwise: real leverage, a literal landscape, unpacking an archive. Read them as replace-on-sight when the metaphorical sense is the one in front of you.

## 15. Tier-3 — flag only at density [C]

Normal words that machine text saturates with. Flag when they run roughly 2%+ of the text, which is the threshold `scan.py` uses.

significant, innovative, effective, dynamic, scalable, compelling, unprecedented, exceptional, remarkable, sophisticated, instrumental, world-class, best-in-class, verbatim, vital, essential.

Fix by replacing some with specifics: numbers, comparisons, examples.

## 16. Negation runways [F]

The single most recognizable sentence tell, in five forms:

| Form | Example |
|---|---|
| Joined | "It's not X, it's Y." / "This isn't about efficiency, it's about transformation." |
| **Split** | "The headline isn't the speed. The real story is the cost." Each sentence looks innocent alone, which is why it slips past checks tuned to the joined form |
| Countdown | "It's not the price. It's not the features. It's the trust." |
| Negative list | "Not a X. Not a Y. A Z." / "It wasn't X. It wasn't Y. It was Z." |
| **Tailing** | "The options come from the selected item, no guessing." A bare negation fragment stapled to a sentence end |

Fix: state the positive claim. "The question isn't the model, it's the eval" becomes "The eval matters more than the model." For the tailing form, write a real clause: "without forcing the user to guess."

**Carve-out:** negations enumerating spec constraints in a list ("no dependencies, no telemetry") are list content, not a reveal. Max one deliberate contrast per piece, and only if it carries the argument.

## 17. Superficial -ing analyses [C]

Present participles stapled on to fake depth: highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, fostering, encompassing, showcasing.

> **Before:** The temple's palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets and the Gulf of Mexico, reflecting the community's deep connection to the land.
> **After:** The temple is painted blue, green, and gold, colors meant to evoke Texas bluebonnets and the Gulf of Mexico.

**The same move without the -ing:** "this represents a broader shift", "the decision symbolizes a commitment to excellence", "it speaks to a larger trend." If the significance is real, show a specific consequence. Otherwise cut.

## 18. False agency [C]

Inanimate things doing human verbs. Machine text reaches for this because it avoids naming an actor.

| Pattern | Why it is wrong |
|---|---|
| "a complaint becomes a fix" | The complaint did nothing. Someone fixed it |
| "the decision emerges" | Someone decided |
| "the culture shifts" | People changed behavior |
| "the conversation moves toward" | Someone steered it |
| "the data tells us" | Data sits there. Someone read it |
| "the market rewards" | Buyers pay for things |
| "a bet lives or dies in days" | Someone kills the project or ships it |

Fix: name the human. If no specific person fits, use "you" and put the reader in the seat.

Related: **moral adjectives on non-agentic nouns.** "An honest shape", "a more honest representation", "flagged honestly." Shapes are not moral agents. State the concrete property: "a more realistic curve", "a clearer picture", "noted."

## 19. Promotional language [C]

Tourism-brochure prose: "nestled within the breathtaking foothills", "a vibrant hub of innovation", "boasts a rich cultural heritage", "renowned", "must-visit", "stunning", "in the heart of."

> **Before:** Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
> **After:** Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

If you would not say it in conversation, cut it.

## 20. Copula avoidance [C]

"Serves as", "stands as", "features", "boasts", "presents", "represents." Press-release verbs standing in for `is` and `has`.

> **Before:** Gallery 825 serves as LAAA's exhibition space. The gallery features four separate spaces and boasts over 3,000 square feet.
> **After:** Gallery 825 is LAAA's exhibition space. It has four rooms totaling 3,000 square feet.

Also: prefer a plain fact over a fake-strong verb. "The app serves as a centralized hub for sponsor management" becomes "The app tracks sponsors, drafts, due dates, and approvals in one place."

## 21. Throat-clearing and fake-candid openers [F]

"Here's the thing", "Here's what I mean", "Let me be clear", "I'll be honest", "The uncomfortable truth is", "Honestly?", "Look,", "Real talk:", "Let's be honest", "It turns out", "Can we talk about."

The tell is the theatrical pause-and-reveal, not the word. "Honestly" mid-sentence in casual prose is ordinary English and stays.

> **Before:** Is it worth the price? Honestly? It depends on how often you'll use it.
> **After:** Whether it's worth the price depends on how often you'll use it.

## 22. Faux-insight setups [C]

"This is the part most people skip", "What most people get wrong", "Here's what nobody tells you", "the failure mode nobody's naming", "the insight everyone's missing."

Flattery of the writer as lone expert, and usually false: if a concept has conference talks from last year, claiming scarcity makes the writer look uninformed. Cut the setup and let the claim stand.

> **Before:** The part everyone misses: distribution is the real moat.
> **After:** Distribution is the moat.

## 23. Infomercial hooks [F]

"The catch?", "The kicker?", "But here's the kicker:", "The best part?", "Plot twist:", "Spoiler:", "The result?", "Here's where it gets interesting."

Mid-flow teasers manufacturing suspense around ordinary information. Delete the hook, state the thing. "The catch? It only works on weekends" becomes "It only works on weekends."

## 24. Signposting and "let's" constructions [F]

"Let's dive in", "Let's explore", "Let's break this down", "Let's take a look", "In this article we will explore", "Now let's look at", "Without further ado", "The rest of this essay explains", "As we'll see."

Announcing the work instead of doing it. Cut and start with the point.

> **Before:** Let's dive into how caching works in Next.js. Here's what you need to know.
> **After:** Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.

## 25. Reasoning-chain artifacts [F]

"Let me think step by step", "Breaking this down", "To approach this systematically", "Step 1:", "Here's my thought process", "First, let's consider."

Chain-of-thought scaffolding leaking into published prose. State the conclusion, then the evidence.

## 26. Acknowledgment loops [F]

"You're asking about…", "To answer your question", "The question of whether…", or opening a section by summarizing the previous one. The reader knows what they asked. Answer.

## 27. Confidence calibration and persuasive authority [C]

Two halves of one move: telling the reader how to feel, and asserting depth.

- **Feeling:** "It's worth noting", "Interestingly", "Surprisingly", "Importantly", "Notably", "Undoubtedly", "Without a doubt."
- **Depth:** "The real question is", "At its core", "Fundamentally", "Make no mistake", "The truth is", "The deeper issue", "The heart of the matter", "This distinction matters", "That last part matters more than it sounds."

One "notably" in 2,000 words is fine. Three in 500 is emphasis stacking. Flag by density.

> **Before:** The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
> **After:** The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.

## 28. Self-labeling significance [C]

Pointing back at your own list to say which item counts: "That last move is the contrarian one", "This is the interesting part", "That third bullet is the real story", "Here's where it gets clever."

If a move is genuinely contrarian, the reader sees it. If it is not recognizable without the label, the label is unearned. Cut the labeling sentence, or restructure so the item you wanted to highlight leads.

## 29. Emotional flatline [C]

Claiming an emotion instead of conveying it: "What surprised me most", "I was fascinated to discover", "What struck me was", "The most interesting part", and the header form "Interesting thing here:".

Not always machine output. Lazy human writing on autopilot does this too. Flag either way. The fix is not "never say surprised." It is: if you claim an emotion, the writing around it should earn it.

Related: "hit differently" / "hits different" as a shortcut to relatability.

## 30. Lingering-attention claims [C]

"The line I keep coming back to", "I can't stop thinking about this", "still thinking about this one", "this has been rattling around in my head all week."

A claim about the writer's attention, arriving before the reader has a reason to care, and unfalsifiable. Delete the frame and open on the thing.

**Carve-out:** leave it when the sentence says *why*. "I keep coming back to Hirschman's exit-voice framing because it predicts which engineers quit and which ones file the RFC" is a claim about the idea's reach.

## 31. Narrated candor [C]

Announcing a disclosure instead of disclosing: "Two caveats I would rather flag than let you discover later:", "I want to be upfront:", "To be fully transparent:", "Rather than bury this, I'll say it plainly:".

**The deletion test:** cut the frame. If nothing is lost, it was never content. "Two caveats I would rather flag than let you discover later: X and Y" and "Two caveats: X and Y" say the same thing.

**Carve-outs:** the disclosure itself stays and is the point ("I haven't tested this on Windows", "this is a mitigation, not a fix"). Conflict-of-interest disclosure stays ("In the interest of full disclosure, I own shares in the company discussed here") because it is a conventional label carrying a material fact.

Judgment only. Every regex tight enough to spare these carve-outs stops matching the tell.

## 32. Recap-flattery openers [C]

Replying to a person by summarizing their own work back at them with praise before getting to the point. "Thanks for all the legwork here, the migration script and the rollback plan you worked through are what made this possible."

They know what they did. Substance first: "Thanks for the legwork. This looks right to me, one comment below."

## 33. Rhetorical question openers [C]

"But what does this mean for developers?", "So why should you care?", "What's next?", "What if I told you…", "Think about it:".

Stalling before the point. If you know the answer, say it.

## 34. Speculative scenario openers [C]

"Imagine a world where…", "Picture a future in which…", "Envision a world where…" The scenario does the persuading; no evidence is offered.

> **Before:** Imagine a world where every deploy is instant.
> **After:** Instant deploys would cut our release cycle from a day to minutes.

**Carve-out:** fiction, a thought experiment with a stated payoff, and instructional "imagine you have a sorted array."

## 35. Aphorism formulas [C]

Slot-fill profundity: "X is the language of Y", "the currency of Z", "the architecture of trust", "X becomes a trap", "X is not a tool but a mirror."

The shape does the persuading instead of the evidence. Replace the formula with the concrete claim it gestures at.

> **Before:** Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
> **After:** Symmetric layouts often feel more predictable to users. Teams can over-optimize workflows and miss how people actually use them.

**Carve-out:** quotations and established idioms ("time is money").

## 36. Vague declaratives [C]

Announcing importance without naming the thing: "The reasons are structural", "The implications are significant", "This is the deepest problem", "The stakes are high", "The consequences are real."

Cut it, or replace it with the specific thing.

## 37. Manufactured punchlines and staccato drama [C]

A run of clipped fragments engineered so every beat lands like a quotable closer.

> **Before:** Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
> **After:** AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made some of the older assumptions less useful.

One short sentence for emphasis is rhythm. Three or more same-shape fragments in a row is a drumroll. Also: **cut quotables.** If a line reads like a pull-quote, rewrite it.

## 38. Fake-profound kickers and summary endings [C]

The final "deep" line that turns the point into an aphorism or mic-drop. And its cousin: "In conclusion", "Ultimately", "Overall", "At the end of the day", "One thing is certain", "As we move forward", "The future looks bright."

Delete the kicker. Do not rewrite it into a better metaphor and do not preserve the rhythm. End on the clearest concrete sentence already in the draft, or add a plain takeaway or next action.

## 39. Template phrases and false breadth [C]

- "A [adjective] step towards [adjective] AI infrastructure" → name the capability, benchmark, or outcome
- "Whether you're a startup founder or an enterprise architect" → false breadth. That means "everyone." Pick the audience you are addressing
- "I recently had the pleasure of…" → "I talked to", "I read", "I attended"
- **False ranges:** "from the Big Bang to dark matter", "from ancient civilizations to modern startups." Pairing unrelated extremes to sound sweeping. List the actual topics.

## 40. Notability name-dropping [C]

"Cited in The New York Times, BBC, Financial Times, and The Hindu." Piling on prestige to manufacture credibility. One reference with context beats four names: "In a 2024 NYT interview, she argued…"

Related: **historical analogy stacking.** "Like the printing press, the telegraph, and the internet before it." The montage substitutes for the argument. Keep the one parallel that does analytical work.

## 41. Hedge stacks and parenthetical hedging [C]

- **Stacked modals:** "could potentially create", "may eventually unlock", "might ultimately transform." Either word alone is fine. The stack asserts nothing while sounding thoughtful. Pick one.
- **Over-qualifying:** "It could potentially possibly be argued that the policy might have some effect" → "The policy may affect outcomes."
- **Parenthetical asides:** "(and, increasingly, Z)", "(or, more precisely, Y)", "(and perhaps more importantly, W)." If the aside matters, give it a sentence. If not, cut it.

## 42. "Real / actual / genuine" inflation [C]

"Real on-chain tokenomics", "actual reward sustainability", "genuine utility", "true product-market fit." An empty intensifier on an abstract noun, implying the rest of the field is fake without saying what makes this one real.

**Carve-out — named contrast:** "Real on-chain settlement, not bridged IOUs" is honest contrastive writing. The tell is the unsaid contrast.

## 43. False concession and invented contrast pairs [C]

- "While X is impressive, Y remains a challenge." Balance-shaped, weighing nothing. Make the concession specific or pick a side.
- **Invented mirroring:** one half of a contrast is a real term of art and the other is fabricated for symmetry. "False precision rather than genuine accuracy" — "false precision" is a statistical term; "genuine accuracy" is a phantom counterpart. If no real opposite exists, drop the contrast and state the positive claim.

## 44. Synonym cycling [C]

"The protagonist… the main character… the central figure… the hero." Repetition-penalty behavior showing through.

> **Before:** The agent reviews the draft. The assistant scores the piece. The tool suggests fixes.
> **After:** The agent reviews the draft, scores it, and suggests fixes.

If the same noun appears three times in a paragraph and it is the right word, keep all three. Same term for the same thing.

## 45. Formulaic challenges sections [C]

"Despite its industrial prosperity, X faces challenges typical of urban areas… Despite these challenges, X continues to thrive." Also the headings that host it: "Challenges and Future Prospects", "Future Outlook", "Challenges and Legacy."

Name the actual challenge and the actual response, or cut.

## 46. Novelty inflation and invented labels [C]

"He introduced a term", "she coined the phrase", "a concept nobody's naming." Most ideas are applications of existing concepts.

Also: pseudo-analytical compounds coined mid-sentence and never defined ("the supervision paradox", "the context-collapse problem", "a coordination tax"). Naming a concept is not explaining it. Define on first use or describe the mechanism.

> **Before:** Michel introduced a term I hadn't heard before: context poisoning.
> **After:** Michel walked through how context poisoning works in practice.

## 47. Generic future-narrative closers [C]

Modal + "become" + "one of the most [adjective]" + narrative/trend/chapter/story. "May become one of the most important narratives of the next market cycle."

Grammatically a prediction, containing nothing testable. Pick the falsifiable version: "DePIN compute may exceed AWS spot pricing for embarrassingly parallel workloads by 2027."

## 48. Social endorsement closers [F]

"This one is worth your time:", "This one's a must-read:", "Do yourself a favor and read this.", "Don't sleep on this one.", "Bookmark this.", "Thank me later."

Performs a recommendation without giving a reason to click, and could sit under any link. Say what the thing is and who it is for, then drop the call to action.

Related, weaker: bare "worth reading", "worth a look", "worth paying attention to." A generic thumbs-up standing in for a reason.

## 49. Em dashes [C]

Machine text uses roughly 10x more em dashes than human writing, and the correctly-spaced form is hard to type, which is itself part of the signal.

**Guidance, not a ban.** Target zero in short copy. In longer drafts, one or two are fine when they clearly beat a comma, period, colon, or parentheses. Remove clusters and decorative dashes. Catch the double-hyphen substitute (`--`) too.

**Two hard rules:**
- A user's writing sample overrides this entirely. If they use em dashes, match their frequency.
- **Never *add* an em dash during a rewrite.**

**Carve-out:** an em dash separating a bolded lead term in a list item (`- **Term** — description`) is typography, not a prose splice.

Replacement order: period, comma, colon, parentheses, restructure.

## 50. Bold overuse, emoji, and inline-header lists [C]

- **Bold:** one bolded phrase per major section at most. If something matters enough to bold, restructure the sentence to lead with it.
- **Emoji in headings:** remove. Social posts may end a line with one or two.
- **Inline-header bullets:** `- **Performance:** Performance has been enhanced through optimized algorithms.` The header restates itself. Write the point, or make them paragraphs.
- **List-label periods:** `**Intros.** Years of conferences and operator network.` A person writes `**Intros:** years of conferences…`. The colon reads as "here's what this means"; the period reads as a sentence the next clause contradicts by continuing.

---

# P2 — Polish

## 51. Rule of three [C]

"Innovation, inspiration, and industry insights." Forced triads to sound comprehensive. **Two items beat three.** Use two, four, or a full sentence. Max one "adjective, adjective, and adjective" per piece.

## 52. Rhythm and uniformity [C]

**The strongest structural signal, and the one that survives every vocabulary fix.** Classifiers weight structural regularity above word choice. Fix every Tier-1 word and leave the rhythm alone, and the text still reads as machine output.

- **Sentence length.** Most sentences at 15-25 words reads robotic. Mix 3-8 word sentences with 20+ word ones. Fragments work. Questions break monotony.
- **Paragraph length.** Some paragraphs should be one sentence. Some should be long.
- **Openings.** Three paragraphs starting the same way is anaphora abuse.
- **Read-aloud test.** If it could be read by a text-to-speech engine without sounding odd, it is too uniform.
- **Do not manufacture variation** by chopping sentences into fragments. Vary the sentences, not the punctuation.

Numeric targets are in `scripts/scan.py`. Human prose typically runs burstiness 0.5-1.0 and type-token ratio 0.50-0.65; machine text trends toward 0.1-0.3 and under 0.40.

## 53. Excessive structure [C]

- More than 3 headings in under 300 words.
- 8+ bullets in under 200 words. That is a paragraph.
- Bullets where two sentences of prose read better.
- Numbered-list inflation: "Three key takeaways", "Five things to know." Only use a number the content actually has.
- Formulaic headers: "Overview", "Key Points", "Summary", "Introduction", "Conclusion." Default scaffolding. Use headers that say something specific.
- **Fragmented headers:** a heading followed by a one-line warm-up restating it. `## Performance` then "Speed matters." Cut the warm-up.

## 54. Bullet lists of bare noun phrases [C]

Five or more consecutive items, each a short adjective-plus-noun phrase with no verb: "Stable mining efficiency / Reliable pool connectivity / Optimized RandomX performance."

The tell is symmetry: every item the same shape and length, none asserting anything checkable. Rewrite as full claims ("Failed shares stayed under 1% across a 12-hour run") or convert to prose.

**Not applicable** to genuine list content: changelogs, todo lists, parameter docs, ingredient lists.

## 55. Subjectless fragments and agentless passives [C]

"No configuration file needed." "The results are preserved automatically." "Support for nested queries was added."

> **After:** You don't need a configuration file. The CLI preserves results automatically.

**Carve-out:** terse reference registers where the fragment is correct — README feature lists, changelog entries, parameter docs, commit subjects. One deliberate fragment for emphasis is rhythm.

## 56. Transition phrases [C]

"Moreover", "Furthermore", "Additionally", "In today's [X]", "In an era where", "When it comes to", "In terms of", "That being said", "In other words" (when redundant), "Simply put."

Restructure so the connection is obvious, or use "and", "also", "but". Piled up is the tell. One "however" is not.

## 57. Title case headings [C]

`## Strategic Negotiations And Global Partnerships` → `## Strategic negotiations and global partnerships`. Sentence case for subheadings. Also: sentence case after a colon unless grammar, a proper noun, a title, or code requires otherwise.

## 58. Curly quotes and immaculate typography [F, weak]

Curly quotes (U+201C/D, U+2018/9) are a **weak** paste-from-chat signal, meaningful mainly in plain-text contexts — code comments, commit messages, plaintext drafts — where nothing auto-curls. Word, Google Docs, macOS, and iOS curl by default, so most human prose has them too. **Never flag curly apostrophes alone.** Corroborating, never conclusive.

Same tier: flawless spacing, punctuation, and capitalization in a register where people type fast (issue comments, chat, DMs).

**The inverse matters more.** When editing someone's casual text, preserve their typos, contractions, and idiosyncratic capitalization. Smoothing the rough edges erases the fingerprint that marks it as theirs.

## 59. Hyphenated-pair overuse [C]

Two problems. **Density:** "a high-quality, well-architected, future-proof solution." Keep the modifier that matters. **Position:** a compound is hyphenated before the noun ("a high-quality report") and not after a linking verb ("the report is high quality"). Machine text hyphenates uniformly.

Watch: third-party, cross-functional, client-facing, data-driven, decision-making, well-known, real-time, long-term, end-to-end.

## 60. Boilerplate phrase clusters [C]

Individually unobjectionable, stacked heavily in generated content (crypto, web3, AI-infra reviews are the worst offenders): "emerging sector", "the integration of X with Y", "the intersection of X and Y", "community-driven", "long-term sustainability", "user engagement", "designed for long-term X".

Flag at 2+ uses of the same phrase, or 3+ distinct phrases from this family in one piece.

## 61. Hashtag stuffing [F]

Six or more hashtags on a short post. Human posts rarely exceed five; generated social posts default to 10-15. The block usually mixes one project tag with broad category tags (#AI #Innovation #FutureTech).

**Not hashtags:** issue references (`#88`), hex colors with a digit (`#1a2b3c`), preprocessor directives (`#include`), URL fragments, markdown headings, anything in code.

Fix: two or three specific tags, or none.

## 62. Wall-of-text replies [F]

In conversational registers only. Reply-length text (under ~150 words) with four or more sentences and no line break anywhere. People break at thought boundaries; models default to one dense block.

**Carve-out:** a single dense paragraph is correct in formal long-form. Never flag continuous prose for lacking internal breaks.

## 63. Diff-anchored writing [C]

Documentation narrating a change instead of describing the thing: "This function was added to replace the previous approach of iterating through all items."

> **After:** This function uses a hash map for O(1) lookups, avoiding the O(n²) cost of naive iteration.

**Carve-out:** changelogs, release notes, migration guides, decision records narrate change correctly.

---

# Writer-side tests

No regex catches these. Run them by reading.

## The portability test

Could this sentence move unchanged to another person, company, country, or product? Then it is filler. Cut it or make it specific to this subject.

This paragraph is the definition. `SKILL.md` and the checklist point at it rather than restating it, and a voice profile that wants the rule cites it too. It was written out in full in three places once, and the copies had already stopped agreeing about whether "country" was on the list.

## Paragraph-reshuffle immunity

Swap two body paragraphs. Does anything break? If the order does not matter, you have a list of points, not an argument that builds. Fix structurally: give each paragraph a connection that does real work with the one before it.

## The treadmill test

Read each paragraph and name the one fact, claim, or turn it contributes. If there is not one, cut it. Machine prose restates the premise in fresh words instead of advancing it. The tell: you could cut 40-60% and lose no information.

## The deletion test

For any frame ("Two caveats I'd rather flag than let you discover later:", "What's interesting here is"), delete it. If nothing is lost, it was never content.

## When to rewrite instead of patch

Any two of these three mean the structure itself is generated, not just the wording: five or more flagged vocabulary hits across multiple categories, three or more distinct pattern categories triggered, uniform sentence and paragraph length. Patching phrases will not fix that. State the core point in one sentence and rebuild.

This is advice for the preview, not a gate you pass silently. When it fires on a document someone asked you to edit, say so in the offer and recommend the full conversion. The user decides, and they decide better knowing the wording is not the problem.
