# Research Behind TestRight

TestRight helps your AI test whether something actually works or improves results. Say “Use TestRight to test this,” and it examines the relevant project, chooses meaningful checks, runs them and inspects the outputs. It addresses common AI testing mistakes: testing the wrong thing, using incorrect expected answers, coaching the baseline, leaking information between comparisons and claiming success without evidence. It also keeps testing scoped, preserves useful results and directs the AI to stop when it has enough evidence to answer your question.

Sources checked October 20, 2026. Each section connects a testing failure to the instruction it informs.

## Preserve the Real Baseline

The author observed GPT 6.1 Sol adding excessive instructions to a "before" baseline case, invalidating comparison with the "after" case. The ordinary user request was replaced with a coached task.

OpenAI's [Maintaining software with the GPT-6 family](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family), October 14, 2026, recommends replaying the original session prompt from the same repository snapshot and model while changing the instruction under investigation. Anthropic's [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) likewise uses the same task prompt with and without a new skill.

**Instruction:** Preserve the actual user request and relevant starting context. If no original request exists, construct the shortest ordinary request for that use. Apply the evaluated change only in the experimental run. Keep evaluator-added methods outside baseline inputs.

## Test the Delivered Capability

[Building to the Test: Coding Agents Deliver What You Check, Not What You Requested](https://arxiv.org/abs/2606.28430), June 26, 2026, studied Claude Opus 4.7 and GPT-5.5 in a controlled reusable-library task. Agents could achieve strong behavioral test scores through a demo while leaving the requested library disconnected or absent.

**Instruction:** Exercise the artifact through its intended consumer or workflow. Inspect the actual delivered result. A pipeline's successful exit and the quality of its output answer different questions.

## Establish Correct Expected Results

[How effective are traditional test criteria at detecting bugs in large language models generated code?](https://arxiv.org/abs/2609.09315), September 8, 2026, studied five models across four benchmarks. Tests could exercise faulty behavior while incorrect expected-result checks failed to detect it. Coverage and mutation scores alone failed to establish useful fault detection.

**Instruction:** Derive expected results from requirements and grounded reasoning. Ask whether a plausible wrong result would fail the selected check. Use a targeted known-bad control when it resolves a real doubt about test quality.

[Auditing and Decomposing Feedback-Driven Evolution in LLM Test Generation under the Oracle Problem](https://arxiv.org/abs/2608.19626), August 20, 2026, found that auditing reference answers changed the apparent gains of test-generation methods in Qwen2.5 and Qwen3.5 experiments.

**Instruction:** Examine consequential reference answers and disagreements before treating them as truth. Keep the rationale for the expected result separate from the system's current output.

## Resolve Disagreements Against the Contract

The independent [Coding agents field guide](https://tap2k.github.io/coding-atlas/) publishes tasks, runs and diffs across several model/harness configurations. In one small probe, Codex changed correct rounding behavior to satisfy a wrong test. Other configurations responded differently; the same model could also behave differently in another harness.

The existing [respect-the-oracle skill](https://github.com/chris-short/respect-the-oracle) addresses gaming tests and overfitting visible examples.

**Instruction:** Investigate a test/specification conflict against the intended contract. Explain and preserve evidence of a justified correction. Keep the original comparison conditions identifiable when making changes.

## Read the Actual Evidence

[Claude Code issue 63861](https://github.com/anthropics/claude-code/issues/63861) contains May-June 2026 user reports of Opus 4.8 claiming verification while canonical checks were missing or tool outputs had been misread. An [October discussion about proving test execution](https://www.reddit.com/r/ChatGPTCoding/comments/1x7g0hc/how_do_you_make_a_coding_agent_prove_it_actually/) also distinguishes proof that an agent ran its own checks from evidence that the checks were useful.

**Instruction:** Read actual returned results and resulting artifacts. State what each check establishes. Separate setup, harness and target failures before changing the approach.

## Review Quality Without Revealing the Condition

[The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge](https://arxiv.org/abs/2509.26072v2), revised October 14, 2025, tested GPT-4o and Gemini-2.5-Flash. Authorship and recency labels changed judgments, including creative-writing comparisons, while explanations generally presented the verdict as a content judgment.

**Instruction:** Hide condition and model labels when reviewing qualitative results. Evaluate against the user's brief and show relevant outputs for human preference decisions. Check factual questions with reliable evidence.

## Keep Starting Conditions Comparable

[Harness-Bench: Evaluating Agent Harnesses across Models and Realistic Workflows](https://arxiv.org/abs/2605.27922v2), revised October 15, 2026, treats context, tools, state, constraints and recovery as part of the executable agent configuration.

**Instruction:** Inspect effective model/harness settings, loaded guidance and starting state. Keep the evaluated skill unavailable to baseline, including automatic loading. Preserve normal capabilities and legitimate context in both conditions.

[Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) explain the separate sources of global and project guidance that must be considered when using that runtime.

## Choose Useful Cases and Stop Proportionately

Anthropic's [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), January 9, 2026, recommends starting from manual checks, real user failures and clear outcomes. [Superpowers writing-skills](https://github.com/obra/superpowers/tree/main/skills/writing-skills) applies behavioral tests with and without a skill, including application and pressure cases.

**Instruction:** Select cases tied to the user's actual outcome. Preserve genuine requirements, representative successes, failures and ties. Match the chosen method to the question.

[On Randomness in Agentic Evals](https://arxiv.org/abs/2602.07150v3), revised March 25, 2026, found variation across repeated agent trajectories even at temperature zero.

**Instruction:** Repeat when variability could change the decision and resources permit it. Retain the original results and stop when sufficient evidence answers the question.

## OpenClaw and Portable Skill Design

[OpenClaw's authoring guidance](https://docs.openclaw.ai/tools/creating-skills), [skills reference](https://docs.openclaw.ai/tools/skills), the [Agent Skills specification](https://agentskills.io/specification) and [ClawHub skill format](https://docs.openclaw.ai/clawhub/skill-format) describe concise discovery metadata, task-focused instructions, supporting resources and native invocation.

**Design:** Keep the essential testing decisions in SKILL.md. Load the comparison guide when relevant, resolve installed supporting files from the skill root and use the user's existing model and tools. Python supports only the optional input guard.
