# Integrity — Cheating, AI, and Assessment That Survives Both

Two facts govern this whole area: unsupervised written work no longer evidences authorship, and detection tools cannot establish it. Everything workable follows from designing assessment that does not depend on either.

**Contents:** [Why Detection Does Not Work](#why-detection-does-not-work) · [What Evidence Actually Establishes](#what-evidence-actually-establishes) · [Designing Assessment That Holds](#designing-assessment-that-holds) · [Writing an AI Policy Students Can Follow](#writing-an-ai-policy-students-can-follow) · [Teaching With AI Rather Than Against It](#teaching-with-ai-rather-than-against-it) · [The Conversation](#the-conversation) · [Plagiarism and Collusion](#plagiarism-and-collusion) · [Exams and Supervised Conditions](#exams-and-supervised-conditions) · [Contract Cheating](#contract-cheating) · [Why Students Cheat](#why-students-cheat)

**Before raising a concern about a specific piece of work**, read that student's rows in the class file: their prior work is the only baseline you have, and the school's policy — recorded under the assessment posture preference area — decides who owns the process from the first conversation onward.

## Why Detection Does Not Work

- **AI text detectors produce false positives at rates no disciplinary process can absorb**, and they are disproportionately wrong about writing by non-native English speakers (Liang et al. 2023). A student who writes plainly, uses a grammar checker, or has been taught a formulaic structure is the classic false positive.
- Detector scores are probabilistic outputs with no ground truth behind them. **Never open a conversation with a percentage**, never put one in a report, and never let one be the evidence. Several major providers have withdrawn or heavily caveated their own tools for exactly this reason.
- Similarity scores from plagiarism software are equally misread: a 30% match is quoted material, references and common phrasing until a human has read what matched.
- The asymmetry is what matters: a false accusation is catastrophic for a student and for the relationship, while a missed case costs a mark. Design so you never have to make the call from a score.

## What Evidence Actually Establishes

In roughly descending order of strength:

| Evidence | What it shows |
|---|---|
| An oral check on their own submission | Whether they can explain their choices, defend a decision, extend it one step. Strongest and fastest evidence there is |
| Draft and version history | The work forming over time; near-impossible to fabricate convincingly after the fact |
| In-class supervised writing on the same topic | A direct comparison of capability under known conditions |
| Process artifacts — notes, sources, a plan, code commits | The route, not the destination |
| Sharp discontinuity with all prior work in that student's file | A prompt to look, never a conclusion by itself |
| Content the course never covered, or citations that do not exist | Concrete and checkable — fabricated references are the most common tell |
| A detector or similarity score | A prompt to read the work. Nothing more |

The rule: **evidence about the process, not inference about the text.**

## Designing Assessment That Holds

Ordered by how much unsupervised authorship risk each removes:

1. **Move the high-stakes evidence in-class**, supervised, on paper or on a locked device. If a grade must be defensible, it needs at least one supervised component.
2. **Assess the process**: plan, draft, feedback response, final. Grade the movement between them, which is also better teaching (`grading.md`).
3. **Require an oral component** — three minutes on their own submission. It scales worse than anything else here and settles authorship faster than anything else here.
4. **Personalise the task**: their own data, their own local case, this week's class discussion, the specific text annotated in the lesson. Generic prompts get generic answers from anywhere.
5. **Assess what a model does badly**: a defence of a choice, reflection on their own error, application to a case only they have, critique of a supplied AI answer.
6. **Weight the components honestly.** If an unsupervised essay is 40% of a grade, that is a decision to accept unverifiable authorship for 40% of the grade — say so explicitly rather than pretending otherwise.
7. **Lower the stakes of homework.** Homework is practice; when it carries a large grade weight, the incentive to outsource is the design, not the student.

## Writing an AI Policy Students Can Follow

Blanket rules fail because they are unenforceable at one end and absurd at the other. Write it **per assignment type**, and put it in the brief itself, not only in the syllabus (`curriculum.md`). Where `ai_policy` is set, it is the default for every brief generated.

| Policy | Wording that works | Where it fits |
|---|---|---|
| `banned` | "No generative AI at any stage. This task is assessed in class under supervision." | Anything where the assessed skill is the writing or the reasoning itself |
| `limited` | "Permitted for brainstorming, checking grammar and explaining concepts. Not permitted to draft or edit submitted text. Add a one-line note saying what you used it for." | Most coursework |
| `open` | "Permitted at any stage, with a short appendix: what you asked, what it produced, what you changed and why." | Tasks where the assessed skill is judgement about the output |
| `unset` | Say so, ask the department, and state the interim rule per task | Never leave students guessing — ambiguity is what produces both cheating and false accusations |

- **Say what the assessed skill is** in each brief. "You are being assessed on the argument, so the argument must be yours" is enforceable and, more importantly, comprehensible.
- Make disclosure normal and costless. A policy that punishes honest disclosure guarantees non-disclosure.
- Teach the policy as content, once, with examples of compliant and non-compliant use. Nobody follows a rule they cannot picture.

## Teaching With AI Rather Than Against It

- **Critique tasks**: give students an AI-generated answer with a plausible error and have them find, explain and correct it. Excellent assessment of the underlying knowledge, and immune to being outsourced back to the same tool.
- **Comparison tasks**: their own attempt first, then the generated version, then a written analysis of the differences. The first attempt is what does the teaching.
- **Prompting as a taught skill** in subjects where it is genuinely part of the work; assess the judgement about the output, not the output.
- Be explicit about what the machine is bad at in your subject — fabricated sources, confidently wrong arithmetic, plausible but ahistorical claims, code that runs and is wrong. Students overtrust in exactly the areas where they cannot yet evaluate.
- Never require students to use a tool that needs a personal account, a payment, or that shares their work without consent.

## The Conversation

Follow the school or institution's process from the first step; what follows fits inside it, never around it.

1. **Prepare**: their prior work, the specific passages, the process evidence, the exact policy wording. Never a detector score.
2. **Open with curiosity, not accusation**: "walk me through how you approached this". Then ask about a specific choice: why this source, why this structure, what this term means.
3. **Listen for the answer that resolves it.** Plenty of these end with a student explaining their work perfectly, which is exactly why you asked first.
4. **If they cannot explain their own submission**, say what you observe and what the policy says. Do not demand a confession; a process that depends on confession is a process that punishes anxiety.
5. **Follow the formal route** the moment it becomes a case: the school owns the outcome, not the classroom teacher. Guardians are informed through the policy's channel, not by you improvising (`parents.md`).
6. **Record facts only** — dates, what was submitted, what was asked, what was said, the policy applied — in the class file. Never a characterisation of the student.
7. **Then fix the assessment**, because a task that could be outsourced will be again.

## Plagiarism and Collusion

- Much of it is a skills gap, not dishonesty: students who were never taught paraphrase, citation and the boundary between help and collusion will cross it and be surprised. Teach it explicitly, with examples, before the first assignment that depends on it.
- **Define collusion for each task**: "discuss the approach, write alone" is clear; "work together" is not, and produces identical submissions from students who thought they were following instructions.
- Group work needs an individually assessed component or it makes collusion structural (`engagement.md`).
- Self-plagiarism and reused work from another module: state the rule; most students have never heard of it.

## Exams and Supervised Conditions

- Supervised conditions remain the only environment that reliably evidences individual capability. Use them for the load-bearing claim and design everything else knowing it.
- Seating, invigilation, phone and smartwatch rules, and materials permitted: follow the exam board or institutional procedure exactly. Irregularities are usually procedural, not criminal.
- Access arrangements are not a loophole and must be delivered exactly as specified (`differentiation.md`).
- Retire circulated papers and rotate contexts; assume anything sent home exists online (`assessment.md`).
- Remote proctoring is invasive, error-prone, biased in its flagging and legally contested. It is an institutional policy decision, never a teacher's improvisation.

## Why Students Cheat

Fixing the cause removes more cases than any detection ever will:

| Cause | Fix |
|---|---|
| Stakes too high on one piece | Distribute the weight across more, smaller pieces |
| Task feels pointless or arbitrary | Say what it is for; make the product real or personal |
| They cannot do it and are out of time | The gap was there weeks earlier; interventions exist for this (`struggling.md`) |
| Everyone else appears to be doing it | Make the norm visible: state what most students actually do, and be consistent |
| The policy was unclear | Per-task rules in the brief, taught with examples |
| No time — jobs, caring, three deadlines the same week | The calendar is a design choice; stagger it (`curriculum.md`) |
| Grade pressure from home | An earlier and different conversation with the guardians (`parents.md`) |

**When an integrity concern arises**, record only facts — the date, the submission, what was asked, what was said, the policy applied and the outcome — in that student's rows in the class file, never a characterisation, and never a detector score. **When an assessment is redesigned in response**, write it as a decision in `~/Clawic/data/teacher/artifacts/<kebab-name>.md` with what was rejected and why, plus its `## Boxes` line, and record the changed task in `assessments/<year>.md`. **When the AI policy for a task type is settled**, it is a declared preference: `ai_policy` in `config.yaml` (`memory-template.md`).
