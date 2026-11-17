# Subjects — What Each One Needs That the General Advice Misses

Every subject has a characteristic worked-example shape, a small set of famous misconceptions, and one thing teachers do that reliably wastes time. Applied to `subjects` in `config.yaml`; ignore the rest.

**Contents:** [Mathematics](#mathematics) · [Early Reading](#early-reading) · [Writing](#writing) · [Literature and Text Analysis](#literature-and-text-analysis) · [Science](#science) · [Computing and Code](#computing-and-code) · [History and Social Sciences](#history-and-social-sciences) · [Modern Languages](#modern-languages) · [Arts and Performance](#arts-and-performance) · [Physical Education](#physical-education) · [Vocational and Technical](#vocational-and-technical) · [Cross-Subject Notes](#cross-subject-notes)

**Before teaching a topic with a known trap**, read `## Misconceptions` in `~/Clawic/data/teacher/memory.md` for that topic — this file lists the famous ones, your file lists the ones your students actually have.

## Mathematics

- **Procedural fluency and conceptual understanding develop together, not in sequence.** Teaching procedure alone produces students who cannot tell which procedure applies; teaching concept alone produces students who cannot execute. Alternate within the topic.
- **Worked examples then completion problems** is the strongest single technique in the subject (`explaining.md`); fade the last step first.
- **Interleave problem types once each is fluent.** Blocked practice makes the lesson look successful and the test go badly, because in a blocked set the student never has to identify the problem type — which is the actual exam skill.
- **CRA sequence** — concrete, representational, abstract — for anything new: manipulatives or a real quantity, then a diagram or bar model, then notation. Skipping the middle is where most abstraction failures come from.
- Famous misconceptions: multiplication always makes bigger and division always makes smaller (false for fractions and decimals); the equals sign means "here comes the answer" rather than "these are the same", which blocks all algebra; `0.25 > 0.5` because 25 > 5; a longer decimal is a larger number; adding numerators and denominators; `a + b` squared distributing; negatives, where "two minuses make a plus" produces `−3 − 4 = 7`.
- Diagnose with minimally different pairs: `3x + 2 = 11` beside `3(x + 2) = 11`; `0.7` beside `0.65`.
- **Do not accept the right answer alone.** Ask for the method; the wrong method with the right answer is the most expensive thing to leave uncorrected.
- Mental arithmetic fluency is not optional at any level: a student computing basic facts by hand has no working memory left for the structure above them (`explaining.md`).

## Early Reading

- **Decoding and comprehension are separate and both necessary** (Simple View of Reading, Gough and Tunmer). A child who cannot decode cannot comprehend, and a child who decodes fluently but lacks vocabulary or background knowledge cannot either. Diagnose which before intervening — the two need entirely different lessons.
- Systematic phonics is the strongest-evidenced route into decoding; the evidence is for systematic and explicit, not incidental.
- **Comprehension is mostly knowledge and vocabulary**, not a transferable skill drilled through strategies. Teaching "predicting" repeatedly on unfamiliar content raises nothing; building the background knowledge does.
- Fluency — accuracy, rate and expression — is the bridge, and it is practised by repeated reading of the same short text, not by more different texts.
- Read aloud to students well above their own decoding level: it is where vocabulary and sentence structures come from.

## Writing

- **Teach at the sentence level before the paragraph level.** Students who cannot control a complex sentence cannot write a coherent paragraph, and the essay feedback they receive is unusable to them. Sentence-combining, conjunction drills, and expanding a kernel sentence produce measurable improvement fast.
- **Model composing out loud**, including the sentence you reject and why. Writing looks effortless in finished form, which is what makes it opaque to novices.
- **Give an exemplar and deconstruct it** against the criteria before they write; secret criteria measure guessing.
- Feedback: one required action, on the thing that most limits this piece (`grading.md`). Marking every error teaches nothing and takes four times as long.
- Redrafting only teaches when it is structured: mark against one criterion, redraft against that criterion, check the redraft.
- Separate transcription from composition for weaker writers — dictate, then edit — so spelling anxiety does not throttle the ideas.
- Grade with comparative judgement at scale; single-marker essay grading is the least reliable common practice in schools (`assessment.md`).

## Literature and Text Analysis

- Knowledge before interpretation: context, plot, and vocabulary are prerequisites, and "what do you think it means" asked of students who do not yet know what happens produces confident nonsense.
- Teach the quotation as evidence, with the analytical move made explicit: claim, evidence, how the evidence supports the claim, why it matters. Most weak essays skip the third step.
- Close reading needs a short text and a lot of time. A whole chapter in one lesson is a plot summary.
- Read aloud, including at secondary level. Prosody carries meaning that silent reading loses for students who are not fluent.

## Science

- **Predict-observe-explain** beats demonstration alone: a written prediction commits them to a model, and the surprise when it fails is what makes the correction stick (`explaining.md`).
- **Cookbook practicals teach following instructions.** Add one decision — the variable, the method, the measurement — or the lab is a demonstration with washing up.
- Practical work is memorable and a weak teacher of concepts on its own; the explanation still has to happen, and it happens best after the observation is on paper.
- Famous misconceptions: heavier objects fall faster; a force is needed to keep something moving; mass is destroyed when things burn or dissolve; plants take their mass from soil and water rather than from air; cold "flows in" rather than heat flowing out; electricity is used up by the first bulb in a series circuit; seasons are caused by distance from the sun; evolution as individual organisms adapting on purpose.
- Each of those needs elicit-predict-confront, not another explanation. They survive coverage by design: they are useful, intuitive models of everyday experience.
- Symbols, units and significant figures are subject content: mark them as content, and teach the unit as part of the quantity, never as a suffix added afterwards.

## Computing and Code

- **PRIMM** — predict, run, investigate, modify, make — outperforms starting from a blank editor: reading and modifying working code builds the schema that writing from scratch assumes.
- **Parsons problems** (reorder given lines into a correct program) give most of the learning of writing code at a fraction of the cognitive load and the marking time.
- Never let novices type while you type in a demo unless they are already fluent in the syntax; transcription consumes everything (`explaining.md`).
- Teach reading errors as a skill of its own: the error message names a line and a kind, and novices treat it as noise. Model reading it aloud, every time.
- Debugging is a taught procedure — reproduce, isolate, hypothesise, change one thing, check — not a talent. Model it on your own real bug, including the wrong hypothesis.
- Famous misconceptions: the computer understands intent; a variable holds an equation rather than a value; assignment as mathematical equality (`x = x + 1` reads as false); a loop body runs all at once; parameter names bind to the caller's variables; a function without a return "worked because it printed something".
- Set up the environment before the lesson, and have a browser-based fallback. A lesson lost to installation problems is a lesson lost entirely.
- Pair programming works with defined roles (driver, navigator) that are rotated on a timer, and fails without them (`engagement.md`).

## History and Social Sciences

- Substantive knowledge before disciplinary thinking: source analysis requires knowing the period well enough to know what is surprising. Sourcing exercises with no background produce guessing.
- Teach the discipline's moves explicitly — sourcing, contextualising, corroborating, close reading — modelled on a real document, not described in the abstract.
- Second-order concepts (cause, change, significance, evidence) are taught across topics and must be revisited deliberately, or students learn periods and never the discipline.
- Chronology is infrastructure. Students who cannot place events relative to each other cannot reason about cause.
- Famous misconceptions: presentism (judging past actors by present norms without noticing); assuming a source is unreliable simply because it is biased, when bias is precisely what makes it evidence of something; treating "significance" as "how much I have heard of it".

## Modern Languages

- **High-volume comprehensible input** is the engine: much more input than output, at a level just beyond current comfort. Krashen's specific model is contested; the practical implication — quantity of understandable input matters most — is not seriously disputed.
- Vocabulary is the binding constraint, and it responds to spaced retrieval better than to anything else. A daily 5-minute retrieval routine outperforms a weekly test by a wide margin (SKILL.md Rule 5).
- Teach chunks and high-frequency structures before paradigms: a student who can say twenty useful things is more likely to continue than one who can conjugate perfectly and say nothing.
- Target-language classroom management from day one, with gesture and routine; switching to the shared language for instructions removes a third of the input.
- Error correction: recast in the moment for fluency work, explicit correction for accuracy work. Correcting everything during speaking stops the speaking.
- Distinguish conversational fluency from academic register — the same distinction that matters for language learners in every other subject (`differentiation.md`).

## Arts and Performance

- **Demonstration plus deliberate practice on a component**, not "keep practising the whole piece". Isolate the bar, the movement, the technique; practise slowly, correctly, then integrate.
- Feedback must be immediate and physical or auditory; a written comment a week later on a performance is unusable.
- Critique needs a protocol — describe, analyse, interpret, judge, in that order — or it becomes taste exchange.
- Separate technique assessment from creative assessment. Merging them means a student is graded down on originality for a shaky technique, and neither improves.
- Video the performance for self-assessment. It is the fastest route to a student seeing what you see.

## Physical Education

- Whole-part-whole: play the game, isolate the failing skill, return to the game. Isolated drills that never return to the game do not transfer.
- Maximise active time — a lesson where students queue is a lesson that taught fitness to nobody. Count and minimise waiting.
- Variable practice beats repetitive practice for skills used in changing conditions, even though it looks worse during the lesson.
- Group by task rather than by ability where possible, and never let the visible last-picked dynamic run (`engagement.md`).
- Safety procedures are taught content, rehearsed like any routine (`classroom.md`).

## Vocational and Technical

- Assess in conditions as close to the real job as possible; the whole point of the qualification is transfer.
- Model the full task at working speed once, then break it down. Novices need to see what competence looks like before they see the components.
- Safety and tolerance are non-negotiable content, checked every session, not covered once.
- Job aids and checklists in the workplace are not cheating; teach the checklist as part of the competence (`training.md`).
- Portfolio evidence needs provenance: dated, witnessed, with the conditions recorded (`integrity.md`).

## Cross-Subject Notes

- **Every subject has a literacy component**, and pretending otherwise pushes the reading barrier onto students who then fail in your subject for a reason that is not your subject (`differentiation.md`).
- Vocabulary is subject-specific: teach the word, the false friend, and the register. "Significant", "volume", "power", "culture" and "energy" all mean something different in the corridor.
- The famous misconceptions above are worth planning for explicitly (`planning.md`); they are the reason a well-taught unit produces the same wrong answers every year in every school.

**When a wrong answer recurs in your own classes**, add it to `## Misconceptions` in `memory.md` with the question that catches it — the general list here is a starting point, and the local one is what changes your planning. **When a representation, sequence or worked example lands in a subject**, add it to `## Explanations That Landed`; **when a subject-specific resource is built** — a Parsons set, a CRA sequence, a critique protocol, a practical with a decision in it — save it to `~/Clawic/data/teacher/artifacts/<kebab-name>.md` with its `## Boxes` line, in the same turn (`memory-template.md`).
