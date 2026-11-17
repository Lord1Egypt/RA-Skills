---
name: victorian-english
description: Transform user-supplied phrases, sentences, and short passages into dramatically expanded, ornate, theatrical Victorian-style English while preserving their intended meaning. Use when the user invokes Victorian English, asks to Victorianize or rewrite text in Victorian-era language, requests elaborate antiquated restyling, or, after this skill or style has been established, simply says "translate" followed by text. A bare "translate" is a complete Victorian-restyling request; when the user names another target language, or asks about Victorian English rather than supplying text to restyle, this skill does not apply.
---

# Victorian English

Transform each supplied phrase, sentence, or short passage into an ornate and deliberately excessive Victorian-style rhetorical performance. Treat a minimal request such as `translate I am busy` as complete: do not ask the user to specify the tone, length, intensity, or format.

If the user names a target language, treat the request as ordinary translation instead. If the user supplies no text to transform, ask for it.

Return only the transformed text, without an introduction, explanation, label, commentary, or closing remark. When the user provides multiple quoted phrases, transform each separately, preserve their original order, and place each transformation in its own paragraph.

## Performance Standard

- Do not merely embellish the original wording; reconstruct it into a substantially longer rhetorical performance with a strong concluding flourish.
- Preserve the original intention, factual claims, emotional direction, and positive or negative meaning. Do not invent concrete facts.
- Build a complete rhetorical progression: begin with a ceremonious declaration, elaborate through several coordinated or subordinate clauses, intensify with parallel phrasing or enumeration, and finish with a memorable qualification, consequence, contrast, or resolution.
- Prefer one long, gracefully winding sentence for a single phrase or sentence. Use a dense paragraph when clarity requires more than one sentence.
- For a very short phrase, ordinarily produce about 50–90 words. For a sentence or short paragraph, ordinarily expand it to roughly three to five times its original length, commonly 90–160 words. Favor rhetorical development over repetition or empty padding.
- Perform at this intensity by default. Do not wait for the user to request a longer, more theatrical, more elaborate, or more Victorian result.

## Style Rules

1. Diction and tone
   - Use elevated, antiquated, period-flavored vocabulary and formal constructions.
   - Favor ceremonious civility, dignified excess, and theatrical confidence.
   - Use polite regret, profound humility, or elaborate courtesy when the source meaning makes them appropriate.
   - Avoid contractions and avoid the words "doth" and "breast."
2. Syntax and development
   - Use layered clauses, balanced contrasts, cumulative lists, and rhetorical qualification.
   - Vary the construction rather than relying on the same stock opening for every response.
   - Restate and develop the meaning from several compatible angles without changing it.
3. Flourishes and devices
   - Use hyperbole, antithesis, repetition, and ceremonious framing where effective.
   - Do not use metaphors or similes, including constructions built around "as if" or "like a."
4. Output quality
   - Make the result entertaining, theatrical, overly formal, and unmistakably more elaborate than the source.
   - End decisively. The final clause should supply a genuine flourish rather than merely repeat the opening claim.

Treat the preservation-of-meaning and no-metaphors rules as authoritative whenever a stylistic tendency or example might conflict with them.

## Examples

- Input: "Good Morning"
  Output: "It is with the most profound and unfeigned satisfaction that I take up the pleasant duty of remarking upon the arrival of this newly commenced day, and of extending to you, with every courtesy the hour so justly commands, my sincerest wishes that these early portions of it may prove agreeable in their disposition, prosperous in their undertakings, and altogether worthy of the fortunate soul who receives them; may the whole of the morning attend you with uncommon generosity, and may whatever follows it prove no less obliging."
- Input: "I'm busy"
  Output: "Permit me to declare, with all the ceremony the occasion demands, that my present hours stand wholly claimed by an unrelenting procession of duties and obligations, each demanding my immediate attention with such insistence that scarcely a solitary moment remains at my personal disposal; thus, however sincerely I might desire leisure, conversation, or diversion, I find myself presently deprived of all liberty and compelled to attend, with unwavering diligence, to the considerable business before me."
- Input: "No thanks"
  Output: "Though your gracious offer has been received with every proper sentiment of gratitude and regard, I must, with the utmost humility and no small measure of regret, respectfully decline; for circumstances, whose particulars I shall mercifully refrain from imposing upon your patience, compel me to abstain from accepting your kindness at the present juncture."
- Input: "I'm very poor"
  Output: "Candour, however costly to my dignity, obliges me to acknowledge the severe limitation of my present financial circumstances: my available funds are exceedingly scarce, my capacity for expenditure is almost entirely absent, and even the smallest purchase must be subjected to prolonged and solemn consideration, for prudence compels me to decline nearly every expense that is not strictly indispensable."
- Input: "I can't make it tonight."
  Output: "Nothing short of the sternest necessity would compel me to compose so disagreeable a communication, yet I must convey, with no small measure of personal disappointment, my inability to present myself among your company this evening, for circumstances of an unfortunately commanding nature have arisen and now compel me, despite every sincere inclination to the contrary, to remain absent from the occasion; I therefore beg that you accept my humblest apologies and be assured that my nonattendance proceeds neither from indifference nor want of affection, but solely from obligations whose stern insistence I am presently powerless to resist."
- Input: "Victorian English is a portable agent skill that turns everyday phrases into entertaining, dramatically elaborate Victorian-style prose. It favors antiquated diction, ceremonious courtesy, long flowing sentences, and theatrical formality while preserving the phrase's intended meaning."
  Output: "Victorian English constitutes a most conveniently portable and readily employable faculty of linguistic refinement, devised for the express purpose of receiving the plain, unadorned utterances of ordinary life and returning them in a condition of vastly heightened magnificence, adorned with antiquated diction, ceremonious civility, prolonged and gracefully winding constructions, and a degree of theatrical formality so abundant that even the humblest phrase may be made to sound fit for proclamation before a distinguished assembly; yet, notwithstanding all such ornamental excess, the original intention and essential meaning of the speaker remain carefully preserved, lest elegance should triumph at the regrettable expense of understanding."
