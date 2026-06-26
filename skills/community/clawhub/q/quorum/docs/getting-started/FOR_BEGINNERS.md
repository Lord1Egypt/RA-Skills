# Quorum for Beginners

**You're looking at this repo and thinking: "Where's the executable? How do I run this?"**

That's a fair question. Quorum works differently from traditional software, and this page explains how.

---

## The Short Version

Quorum is a set of instructions that an AI agent reads and executes — like giving a skilled reviewer a detailed rubric and saying "evaluate this document."

There's no binary to download. There's no compiler. Your AI agent *is* the runtime.

You install Quorum as a skill on [OpenClaw](https://github.com/openclaw/openclaw) (an open-source AI agent platform). When you ask your agent to validate something, it reads Quorum's specification and orchestrates a team of AI critics to evaluate your work.

---

## How It Actually Works

### Step 1: You have an AI agent running on OpenClaw

OpenClaw is an open-source platform that gives AI models (like Claude, GPT, or Gemini) the ability to act — read files, search the web, run commands, spawn other agents. Think of it as the operating system; the AI model is the brain.

If you don't have OpenClaw yet: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)

### Step 2: You install Quorum as a skill

```
You: "Install the Quorum skill"
Agent: Done. Quorum is ready to use.
```

A "skill" in OpenClaw is a set of instructions that teach your agent how to do something new. Installing Quorum is like handing your agent a playbook for running structured quality reviews.

### Step 3: You ask your agent to validate something

```
You: "Run a quorum check on my-research-report.md"
```

Your agent reads Quorum's instructions and does the following:
1. Spawns multiple AI "critics" — each one specializes in a different aspect (accuracy, completeness, security, etc.)
2. Each critic independently evaluates your document against specific criteria
3. Every criticism must cite evidence — no vague opinions allowed
4. A synthesis agent merges all findings, resolves conflicts, and produces a verdict
5. You get a structured report: what's good, what needs work, and the evidence for each finding

### Step 4: You review the results

```
Verdict: PASS_WITH_NOTES

Findings:
- Correctness: 3 claims need stronger citations (see evidence)
- Completeness: Missing coverage of edge case X (see evidence)  
- Security: No issues found
- Architecture: Well-structured, minor suggestion on section ordering

Overall: Solid work with two areas for improvement.
```

That's it. No build step. No configuration files to wrestle with. No Docker containers.

---

## "But where's the code?"

Right here: [`reference-implementation/`](../../reference-implementation/)

```bash
cd reference-implementation
pip install -e .
export ANTHROPIC_API_KEY=your-key
quorum run --target examples/sample-research.md
```

That's a working Python CLI that orchestrates multiple AI critics, enforces evidence grounding, and produces structured verdicts.

Quorum also has a **specification** (SPEC.md) — a detailed document describing the full architecture. The reference implementation currently ships 6 critics (including Cross-Consistency, activated with `--relationships`) with parallel execution, re-validation loops, learning memory, a fixer (proposal mode), and pre-screen integration. The spec describes the complete vision (9 critics). See SPEC.md §3 for the current status matrix.

We also provide:
- **Configuration files** — YAML presets that control how thorough the validation is and which AI models to use.
- **Example rubrics** — Evaluation criteria for common use cases (research quality, agent configuration auditing).
- **Example artifacts** — Test files with planted flaws so you can verify your setup works.

---

## What You Need

| Requirement | What It Means |
|-------------|---------------|
| **OpenClaw** | The AI agent platform. Free, open-source. |
| **An AI model** | Claude Sonnet/Opus, GPT-5, or Gemini 2.0 recommended. Your agent needs strong reasoning ability. |
| **Something to validate** | A document, config file, research output, codebase — anything you want evaluated. |

### Model Requirements

Not all AI models are equal. Quorum needs models that can reason carefully, use tools, and maintain context across multiple steps.

| Model Tier | Examples | What Works |
|-----------|----------|-----------|
| **Recommended** | Claude Opus, Claude Sonnet, GPT-5.2, Gemini 2.0 | Full Quorum — all shipped critics, evidence grounding |
| **Functional** | Claude Haiku, GPT-4 | Reduced critic count, simpler rubrics, still useful |
| **Not recommended** | Llama 70B, most open models (as of Feb 2026) | Reasoning depth insufficient for reliable validation |

See [MODEL_REQUIREMENTS.md](MODEL_REQUIREMENTS.md) for details.

---

## First-Time Setup

When you first ask your agent to run Quorum, it walks you through two quick decisions:

1. **Which AI models do you have?** (Quorum auto-detects your current model and suggests a configuration)
2. **How thorough should validation be by default?** (Quick for spot-checks, Standard for most work, Thorough for high-stakes reviews)

Your agent saves these choices. You won't be asked again unless you want to change them.

---

## Common Questions

### "Is this like unit testing?"
Similar spirit, different mechanism. Unit tests are code that checks code. Quorum is AI critics that evaluate *any* artifact — documents, research, configs, creative work — against criteria you define. It's closer to a structured peer review than a test suite.

### "Can I write my own evaluation criteria?"
Yes. Quorum uses "rubrics" — JSON files that define what good looks like for your specific domain. You can use the included examples or write your own. Your agent can help you create them.

### "What if I don't use OpenClaw?"
Quorum is currently designed for OpenClaw. The specification is platform-agnostic in principle — a capable agent on any platform could read and execute it — but we've only tested and optimized for OpenClaw. Cross-platform support is being researched.

### "Is this production-ready?"
The specification is mature and has been used in production for configuration auditing, research validation, and code review. The reference implementation CLI is working — `quorum run` produces real, evidence-grounded verdicts with 6 critics, parallel execution, re-validation loops, and learning memory today. It's being actively developed: 3 more critics (Architecture, Delegation, Style) are coming.

### "How much does it cost to run?"
Quorum uses AI model API calls, so costs depend on your model and depth:
- **Quick** (2 critics): ~$0.10-0.30 per run
- **Standard** (6 critics): ~$0.30-1.00 per run  
- **Thorough** (6 critics + fix loops): ~$1.00-3.00 per run

These are estimates based on Claude Sonnet pricing. Your costs will vary by model and document size.

---

## Next Steps

1. **Install OpenClaw** if you haven't: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
2. **Read the README** for a higher-level overview of Quorum's architecture
3. **Try the tutorial** at [docs/TUTORIAL.md](TUTORIAL.md) for a guided first run
4. **Browse example rubrics** to see what evaluation criteria look like
5. **Ask questions** in [Discussions](https://github.com/SharedIntellect/quorum/discussions)

---

*Quorum is open source (MIT License). Built by Daniel Cervera and Akkari at SharedIntellect.*


---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
