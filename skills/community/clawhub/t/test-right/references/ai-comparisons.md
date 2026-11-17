# AI Comparisons

TestRight helps your AI test whether something actually works or improves results. Say “Use TestRight to test this,” and it examines the relevant project, chooses meaningful checks, runs them and inspects the outputs. It addresses common AI testing mistakes: testing the wrong thing, using incorrect expected answers, coaching the baseline, leaking information between comparisons and claiming success without evidence. It also keeps testing scoped, preserves useful results and directs the AI to stop when it has enough evidence to answer your question.

Use this guide when testing involves AI subjects or comparisons of AI behavior.

## Construct the Ordinary Baseline

Start from the real user request and relevant starting context. Preserve the request's wording. If the user said "Test this," provide the target and context they were referring to. If no original request exists, construct the shortest ordinary request for the intended use and record that it was constructed.

Preserve the baseline's normal tools, policies and legitimate user requirements. Identify whether it represents a configured production agent, a fresh installation or another control. Keep the evaluated change absent from baseline and apply it only in the experimental run.

Put evaluator-authored methods, expected answers, suspected causes and grading notes outside subject inputs. Before running, compare added directions with the capability being measured. Asking a baseline planner to specify exact condition prompts and evaluation criteria can supply part of an evaluation-design skill. Genuine user instructions remain valid context; assess what the change adds beyond them.

Build both conditions from the same source. Inspect the actual dispatched messages and condition differences. Keep evaluator records separate from subject workspaces, including filenames and helper files. Preserve inputs at meaningful stages. The optional [input guard](input-guard.md) checks declared changes after preparation; inspect source fairness before preparing the bundle.

## Separate the Testing Agent From the Subjects

TestRight guides the agent arranging and interpreting the test. The subjects perform the task being evaluated. Evaluators inspect the outcomes against the criteria.

When testing another skill, the baseline subject performs the ordinary task without that skill; the experimental subject performs it with the skill. When testing TestRight, the baseline agent receives the ordinary testing request without TestRight; the experimental agent receives that task with TestRight. Keep the evaluator's desired methods outside baseline instructions.

Check effective instruction sources, installed skills, retrieved context, model/harness settings, tools and session state. A fresh folder or omitted skill name alone does not establish that guidance is absent. Restore equivalent starting conditions between runs, preserving state within an episode when required. Prevent files, answers and memories from one condition entering the other. Record inaccessible boundaries accurately.

## Select and Evaluate Informative Cases

Use real requests and source incidents where available. Distinguish captured incidents, adapted cases and constructed probes. Keep development cases identifiable when used again. Freeze case selection and evaluation criteria before inspecting results, and retain every outcome.

Check what the supplied material already reveals. A case containing the diagnosis or resolution tests using that information; it does not establish independent discovery. Match the claim accordingly. Keep legitimate task information and make the intended task understandable.

Compare actual outcomes: correctness, useful findings, preserved behavior, output quality, effort, latency or cost as relevant. A wording preference can itself be the outcome. Separate preferences and authorized policies from factual beliefs. Explicitly asking to save a note tests that operation rather than automatic memory extraction.

For qualitative review, hide condition/model identities where practical and assess the user's brief. Inspect decisive disagreements. AI judges assist evaluation; use reliable checks for factual questions and human preference for preference claims.

Investigate unexpectedly identical outputs by checking actual messages, model settings, execution and returned responses. Do not invent a cause for a tie. A baseline success remains useful evidence. Ties and small wins do not justify an automatic larger matrix or a broad reliability claim. Repeat only when variability could change the decision and resources permit it.

Report actual outputs, failures and regressions. Distinguish agent responses from underlying model requests and measured usage from monetary estimates. Keep checkpointing and records proportionate. Continue already-authorized work, honor explicit stops and preserve valid completed results after a justified repair.

The [research guide](../REFERENCES.md) explains the evidence for original-request replay, independent expected results, matched harnesses and label-blind review.
