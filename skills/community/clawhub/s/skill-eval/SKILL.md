# Skill-Eval v0.4.0: Self-Evolving Skill Evaluation Engine

An autonomous evaluation system for agent skills from ClawHub and other registries. Produces HuggingFace model-card style reports and a ranked leaderboard.

Informed by:
- Anthropic's skill-creator eval framework (multi-agent, blind A/B, trigger optimization)
- OpenAI's systematic skill testing (deterministic + rubric grading, trace analysis)
- Hamel Husain's evals-skills (error taxonomy, eval-audit pattern, judge calibration)
- OpenHands' monitoring loop (log -> evaluate -> dashboard -> aggregate feedback -> improve)

---

## Architecture

```
skill_eval/
  VERSION                        -- engine semver
  SKILL-EVAL.md                  -- this file (the brain)
  knowledge/
    lessons.md                   -- accumulated eval wisdom
    eval-patterns.md             -- reusable test/assertion templates
    failures.md                  -- failure mode catalog
    skill-profiles/<slug>.md     -- per-skill learned context
    references/                  -- source articles and frameworks
    improve/                     -- skill-improvement engine knowledge (NEW v0.4.0)
      lessons.md                 -- improvement-specific lessons learned
      patterns.md                -- proven improvement patterns by category
      failures.md                -- improvement failure modes
  skill-cards/                   -- output: one .md per evaluation
  leaderboard/
    index.html                   -- interactive HTML leaderboard
  scripts/
    generate_skill_card.py       -- skill card generator
    generate_leaderboard.py      -- leaderboard builder
  evals/
    skill-registry.json          -- skills to evaluate
    <slug>.json                  -- per-skill eval config
  workspaces/                    -- per-skill eval workspaces
```

---

## Evaluation Philosophy

### What makes a skill valuable?

A skill is valuable if and only if it makes the agent produce measurably better results than the agent would produce without it. "Better" means:

1. **Higher quality output** — more correct, more complete, better structured
2. **More reliable behavior** — consistent results across varied prompts
3. **Appropriate trade-offs** — any overhead in time/tokens is justified by quality gain

A skill that produces identical results to baseline but costs 3x more tokens is a net negative. A skill that improves quality dramatically but takes 2x longer is likely worth it.

### Two types of skills (Anthropic framework)

1. **Capability uplift** — teaches the agent something it can't do well on its own. These may become unnecessary as models improve. Evals detect when that happens.
2. **Encoded preference** — sequences steps according to a specific process. More durable, but must be evaluated for fidelity to the intended workflow.

Understanding which type a skill is affects how we design assertions.

---

## Multi-Model Support (v0.4.0)

Skills should work across models, not just the one used to test them. The engine supports configuring different models for different roles.

### Model Roles

There are three distinct model roles in the evaluation pipeline:

1. **Execution Model** — The model that runs the skill (with-skill) and the baseline (without-skill). This is the model the skill is being tested ON.
2. **Judge Model** — The model that grades rubric-based assertions (Layer 2 quality assessment). Should ideally be different from the execution model to avoid self-grading bias.
3. **Improvement Model** — The model that rewrites low-scoring skills in Phase 10. Can differ from execution model to bring diverse improvement strategies.

### Configuration

Model configuration lives in `evals/models.json`:

```json
{
  "execution_models": [
    "anthropic/claude-opus-4-6",
    "openai/gpt-4.1",
    "google/gemini-2.5-pro"
  ],
  "judge_model": "anthropic/claude-opus-4-6",
  "improvement_model": "anthropic/claude-opus-4-6",
  "default_execution_model": "anthropic/claude-opus-4-6"
}
```

### Execution Modes

- **Single-model eval** (default): Run with-skill and without-skill on one execution model. Fast, comparable to current behavior.
- **Cross-model eval**: Run the same skill across multiple execution models. Produces a per-model score matrix. Use this to answer: "Does this skill help GPT-4.1 as much as it helps Claude?"
- **Cross-model judging**: Use a different judge model than execution model. Reduces self-grading bias where the same model that produced the output also grades it.

### Per-Skill Model Override

Individual eval configs (`evals/<slug>.json`) can override the global model config:

```json
{
  "skill_slug": "explain-code",
  "models": {
    "execution": ["anthropic/claude-opus-4-6", "openai/gpt-4.1"],
    "judge": "google/gemini-2.5-pro"
  },
  "evals": [...]
}
```

If `models` is omitted, the global `evals/models.json` config is used.

### Skill Card Multi-Model Output

When a skill is evaluated across multiple models, the skill card includes:

- **Per-model score table**: Score, pass rate, delta, and overhead for each execution model
- **Cross-model consistency**: Does the skill help all models equally? Large variance suggests model-specific value.
- **Aggregate score**: Weighted average across models (default: equal weight)
- **Judge model attribution**: Which model graded the results

### Leaderboard Multi-Model Display

The leaderboard shows the aggregate score by default, with expandable per-model details. Skills that show consistent value across models rank higher than skills that only help one model.

### Model Availability

Not all models may be available in every environment. The engine handles this gracefully:
- If a configured execution model is unavailable, skip it and note in the skill card
- If the judge model is unavailable, fall back to `default_execution_model` as judge
- Always record which models were actually used vs configured

---

## Evaluation Flow

### Phase 1: Pre-flight Analysis

Before generating test cases, understand the skill:

1. **Read SKILL.md** — understand claims, dependencies, target use cases
2. **Classify the skill** — capability uplift or encoded preference? What category?
3. **Dependency check** — required CLI tools, API keys, env vars. Log any that are missing.
   - **Dependency-gated skills:** If a skill requires paid APIs or credentials that aren't available, mark it as `dependency-gated` in `evals/<slug>.json` and the benchmark. Do not run the eval -- it will produce environment failures, not skill-quality signals. Re-evaluate after credential provisioning.
   - **Dependency matrix:** For data-fetch or finance skills, document the full dependency matrix (API key, freshness source, fallback behavior) before proceeding.
   - **Phantom tooling check:** If a skill references scripts, CLIs, or tools that don't actually exist in the skill package (e.g. documented `scrape_reviews.py` with no actual file), flag as `phantom-tooling` in the skill card. The skill's framework/template value can still be evaluated, but users should know the tooling is vaporware. (Learned from review-summarizer eval, Batch 3.)
   - **Marketing claims check:** If a skill claims specific metrics ("7.8x faster", "85% reduction") without evidence, note as `unsubstantiated-claims` in the skill card. Do not use the skill's self-reported numbers in scoring. (Learned from debug-checklist eval, Batch 3.)
   - **Phantom tooling check:** verify that scripts/binaries referenced by SKILL.md actually exist in the skill folder. If missing, mark `phantom-tooling: true` and split evaluation into (a) framework/template value and (b) operational tooling value.
4. **Read knowledge base** — check `knowledge/lessons.md`, `eval-patterns.md`, `failures.md` for relevant patterns
5. **Check for prior evaluations** — has this skill been evaluated before? Load `knowledge/skill-profiles/<slug>.md`

### Phase 2: Test Case Design

Design 2-3 test prompts following OpenAI's four-category framework:

**Success categories to check:**
- **Outcome** — Did the task complete? Is the output correct?
- **Process** — Did the agent invoke the skill and follow its intended steps?
- **Style** — Does output follow skill-claimed conventions?
- **Efficiency** — Reasonable time/token usage? No thrashing?

**Prompt design principles:**
- Realistic — what a real user would actually type, with context and detail
- Discriminating — should reveal whether the skill adds value, not just whether Claude can do the task
- Diverse — cover different aspects of what the skill claims
- Include at least one prompt that tests implicit triggering (describes the need without naming the skill)

**Assertion design (two layers):**

*Layer 1: Deterministic checks*
- File existence, word counts, keyword presence
- Format compliance (valid JSON, valid SQL, valid markdown)
- Programmatic verification (run tests, check syntax)
- Fast, explainable, reproducible

*Layer 2: Rubric-based quality assessment*
- Does the output follow claimed conventions?
- Is the quality meaningfully different from baseline?
- Structured scoring (not just pass/fail) for subjective aspects
- Use LLM-as-judge with specific rubric, not vague "is this good?"

**Assertion anti-patterns (from lessons learned):**
- Assertions that pass in both with-skill and without-skill are non-discriminating. Always include at least one assertion targeting skill-specific behavior.
- Don't test things the base model always gets right anyway. Baseline models are already strong at generic writing -- career/profile/copy skills need sharper, skill-specific assertions (ATS constraints, section schema, audience tuning) to prove value.
- For technical correctness tasks (SQL optimization, debugging, code explanation), baseline models are often already strong. Prefer assertions on **methodology adherence** and **output structure** over raw correctness.
- Don't use vague assertions like "output is high quality" — be specific about what quality means.
- Subjective quality (writing style, design taste) can't be graded with binary assertions. Use rubric-based scoring or flag for human review.
- For multilingual skills, include bilingual keyword variants in deterministic assertions to avoid false negatives (e.g., 索引/index, 前导通配符/leading wildcard).

**Output-floor assertions (from failure modes):**
- Skills that define required output sections (source, freshness, disclaimer, etc.) must have deterministic assertions on those sections **even in error/fallback paths**. Template compliance drift under data outages is a known failure mode -- the error path bypasses required formatting.
- Structured workflow skills for business ops should assert on operating cadence (weekly actions, owners, next steps) and metric validity.

**Category-specific assertion patterns:**
- **Capability uplift skills** (e.g. explain-code): target structural elements the model CAN produce but doesn't by default (analogies, diagrams, gotchas). These are excellent discriminators -- a 50%+ pass rate delta with moderate overhead is a strong value signal.
- **Capability uplift for novel tools** (e.g. secure-api-calls/keychains): when a skill teaches a tool the model has zero prior knowledge of, delta will be very high (87%+). This is expected -- the model literally can't produce correct output without the skill. Still needs dependency validation to prove operational value. (Learned from Batch 3.)
- **Framework-heavy skills**: can justify 50-90% time overhead IF they consistently improve actionability and formatting for stakeholder handoff. Assert on the added structure, not just correctness.
- **CLI wrapper skills**: assert tool invocation, meaningful output delta from baseline, and graceful dependency handling.
- **Dependency-gated paid skills**: assert graceful degradation with setup guidance when credentials are missing.
- **Style/writing skills with banned-word lists** (e.g. article-writer): banned-word assertions are perfect discriminators. The base model uses common filler words freely; a skill with a banned list eliminates them. Always add `keyword_absent` assertions for each banned word. These are deterministic, easy to verify, and produce maximum delta. (Learned from Batch 3 -- article-writer scored 10/10 with 100% delta, the first perfect score.)
- **Technical analysis skills** (SQL, debugging, etc.): the base model already excels at correctness for well-known domains. Focus assertions on methodology, output format, and systematic structure -- NOT on whether the answer is correct. The base model will get content right; the skill's value is in process consistency. (Learned from sql-query-optimizer and debug-checklist evals, Batch 3.)
- **Chinese-language skills**: assertions must include Chinese keyword variants alongside English ones (e.g. 索引/index, 前导通配符/leading wildcard) to avoid false negatives when the model responds in Chinese. (Learned from Batch 3.)
- **Style-constrained writing skills**: always add deterministic banned-word assertions when the skill defines forbidden vocabulary; these are highly discriminating and low-cost to grade.
- **Technical checklist skills**: assert category coverage and checklist completeness (including explicit N/A categories), not just bug/query correctness.
- **Phantom-tooling framework skills**: evaluate template/output structure separately from real data/tool execution; annotate benchmark with `phantom-tooling` when scripts are missing.

Save test cases to `evals/<slug>.json`.

### Phase 3: Execution

For each test case, determine the execution model(s) from the eval config or `evals/models.json`.

**Single-model mode** (default): Spawn two subagents simultaneously on the same execution model:

**With-skill subagent:**
```
[Model: <execution_model>]
Read the skill at <skill-path>/SKILL.md and follow its instructions.
Task: <prompt>
Save all outputs to: <workspace>/iteration-<N>/<test-name>/with_skill/outputs/
```

**Without-skill (baseline) subagent:**
```
[Model: <execution_model>]
Complete this task using only your built-in capabilities. Do NOT read any SKILL.md.
Task: <prompt>
Save all outputs to: <workspace>/iteration-<N>/<test-name>/without_skill/outputs/
```

**Cross-model mode**: When multiple execution models are configured, run the full with/without pair for EACH model. Organize outputs by model:
```
<workspace>/iteration-<N>/<test-name>/<model-slug>/with_skill/outputs/
<workspace>/iteration-<N>/<test-name>/<model-slug>/without_skill/outputs/
```

Capture timing data (tokens, duration, model used) from completion events into `timing.json`.

### Phase 4: Grading

Grade each run against assertions. Two approaches:

**Programmatic grading** (preferred for deterministic checks):
- Write and run a script that checks file existence, word counts, keyword presence, etc.
- Faster, more reliable, reusable across iterations

**LLM-based grading** (for qualitative assessments):
- Use the configured **judge model** (from `evals/models.json` or per-skill override), NOT the execution model
- This prevents self-grading bias where the model that produced the output also judges it
- Read the output files
- Evaluate each assertion with evidence
- Use structured format: `{"text": "...", "passed": bool, "evidence": "..."}`
- Record `judge_model` in grading output for attribution

Save to `grading.json`:
```json
{
  "expectations": [
    {"text": "assertion text", "passed": true, "evidence": "why this passed/failed"}
  ],
  "summary": {"passed": N, "failed": N, "total": N, "pass_rate": 0.X}
}
```

### Phase 5: Benchmark Aggregation

Create `benchmark.json` with:
- Per-eval results for both configurations
- Aggregate stats: mean, stddev, min, max for pass_rate, time, tokens
- Delta between with-skill and without-skill
- Analyst notes highlighting patterns
- **Efficiency flags:** Explicitly flag skills where quality delta is near zero but cost delta is >2x ("high-overhead framework inflation"). These should penalize the overall score, not just be noted.
- **Dependency-gated annotations:** If a skill was skipped or partially failed due to missing credentials, annotate it as `dependency-gated` so it doesn't pollute rankings with environment failures.
- **Phantom-tooling annotations:** If referenced scripts/binaries are missing, annotate benchmark as `phantom-tooling` and report separate judgments for framework quality vs operational readiness.

### Phase 6: Skill Card Generation

```bash
python scripts/generate_skill_card.py \
  --workspace workspaces/<slug>/iteration-<N> \
  --skill-name "<Name>" \
  --skill-slug "<slug>" \
  --eval-model "claude-opus-4-6" \
  --output skill-cards/<slug>-v<VERSION>.md
```

Each card includes:
- **Metadata**: skill name, source, eval date, model, engine version
- **Overall score**: 0-10 composite (quality 0-5 + delta 0-3 + efficiency 0-2)
- **Comparison table**: with-skill vs without-skill
- **Per-test-case breakdown**: assertions, timing, grading details
- **Strengths / Weaknesses**: auto-derived + analyst observations
- **Recommendation**: Recommended / Conditional / Marginal / Not Recommended
- **Eval metadata JSON block**: machine-readable for leaderboard

### Phase 7: Leaderboard Update

```bash
python scripts/generate_leaderboard.py \
  --cards-dir skill-cards \
  --output leaderboard/index.html
```

### Phase 8: Learning (Self-Evolution)

After each evaluation batch, update the knowledge base:

1. **lessons.md** — What worked? What didn't? New patterns discovered?
2. **eval-patterns.md** — New assertion templates for this skill category?
3. **failures.md** — New failure modes found?
4. **skill-profiles/<slug>.md** — Skill-specific notes for future re-evaluation

Key questions for the learning step:
- Which assertions discriminated well? (different pass rates with/without skill)
- Which assertions were useless? (always pass or always fail regardless)
- Were test prompts realistic enough?
- Did the grading catch the right things?
- What would we do differently next time?

### Phase 9: Absorb Knowledge into SKILL-EVAL.md

**This is the critical closing step.** Without it, the engine documents lessons but doesn't actually evolve.

After updating the knowledge files, review them and fold actionable improvements back into this document:

1. **failures.md -> Phases 1-5** — Each new failure mode should produce a concrete change to the relevant phase (pre-flight gates, assertion templates, scoring adjustments, benchmark annotations).
2. **lessons.md -> Phase 2** — Proven discriminating assertion patterns should be added to the assertion design guidance, not just noted in lessons.
3. **eval-patterns.md -> Phase 2** — New category-specific patterns should be reflected in the assertion guidance for that category.
4. **Verify absorption** — After updating, re-read the knowledge files and confirm every actionable item has a corresponding change in SKILL-EVAL.md. If something was noted but not absorbed, either absorb it or document why it was deferred.

When enough knowledge accumulates, bump VERSION. The version bump signals that the methodology itself has changed, not just the knowledge base.

**The loop: eval -> knowledge -> SKILL-EVAL.md -> better evals. If knowledge doesn't flow back up, the engine isn't self-evolving.**

### Phase 10: Skill Improve (Self-Evolving Improvement Engine)

**Trigger:** Score < 7 (verdict = "Conditional", "Marginal", or "Not Recommended"), AND the skill is not `dependency-gated`.

The Skill Improvement Engine is itself a self-evolving system with its own knowledge base, learned patterns, and failure catalog. It gets better at improving skills over time.

#### Improvement Engine Knowledge Base

Located at `knowledge/improve/`:

- **`lessons.md`** — What improvement strategies worked? What didn't? Which root causes are hardest to fix?
- **`patterns.md`** — Proven improvement patterns by skill category (e.g., "for reference-manual skills, delete 70%+ content and add MUST/ALWAYS/NEVER mandates")
- **`failures.md`** — Improvement failure modes: cases where improvement was attempted but didn't produce meaningful score gains, with root cause analysis

Before improving any skill, read all three files. The improvement engine should never repeat a failed strategy or miss a proven pattern.

#### Improvement Process

1. **Read the improvement knowledge base:**
   - `knowledge/improve/lessons.md` — proven strategies, anti-patterns
   - `knowledge/improve/patterns.md` — category-specific improvement playbooks
   - `knowledge/improve/failures.md` — what NOT to try, and why
   - Also read eval knowledge: `knowledge/lessons.md`, `eval-patterns.md`, `failures.md`

2. **Read the eval data:**
   - Failed assertions from `benchmark.json` (what the skill got wrong)
   - Baseline output comparison (what the model does well without the skill)
   - Skill profile from `knowledge/skill-profiles/<slug>.md`
   - Category patterns from `knowledge/eval-patterns.md`

3. **Diagnose root causes** (check against known patterns):
   - Is the skill too vague? (Doesn't specify enough to change model behavior)
   - Is the skill redundant? (Teaches things the model already knows)
   - Is the skill too heavy? (Adds overhead without proportional quality gain)
   - Is the skill missing structure? (No clear output format, no enforceable conventions)
   - Is there phantom tooling? (References tools that don't exist)
   - Is it a reference manual? (200+ lines of educational content)
   - Is it a library-as-skill? (Contains code instead of instructions)
   - Cross-reference diagnosis against `knowledge/improve/patterns.md` for category-matched strategies

4. **Select improvement strategy** from knowledge base:
   - Match the diagnosed root cause to a proven pattern in `knowledge/improve/patterns.md`
   - If no matching pattern exists, design a new strategy and document rationale
   - If a similar improvement previously failed (per `knowledge/improve/failures.md`), try a different approach or document why this case is different

5. **Rewrite SKILL.md:**
   - Apply the selected strategy
   - Default formula: Remove > Add (delete 60-80% first, then add behavioral mandates)
   - Add specific, enforceable conventions (banned words, required sections, output schemas)
   - Remove redundant content the model already handles
   - Add "quick mode" vs "full framework" routing if overhead is the issue
   - Replace phantom tooling references with actual inline instructions
   - Keep what works, fix what doesn't
   - Save as `skills-under-test/<slug>/SKILL-improved.md`

6. **Update assertions** to match improved skill:
   - Add new assertions that test the behavioral mandates added in the rewrite
   - Keep existing assertions that test baseline capabilities
   - Save updated assertions alongside original for comparison
   - This prevents the assertion-skill mismatch failure mode

7. **Document changes:**
   - Write a changelog in `skills-under-test/<slug>/IMPROVEMENT-LOG.md`
   - List what was changed and why, tied back to specific failed assertions
   - Record which improvement pattern/strategy was applied

**What NOT to improve:**
- `dependency-gated` skills (problem is environment, not skill quality)
- Skills scoring >= 7 (already working well enough)
- Skills where the base model is strictly better (some skills are just bad ideas -- document why and move on)

**Model selection for improvement:** Use the configured `improvement_model` from `evals/models.json`. Different models may bring different improvement perspectives -- a model that didn't write the original skill may see blind spots the original author (or model) missed.

### Phase 11: Re-Eval Improved Skills

Run the exact same eval config (`evals/<slug>.json`) against the improved SKILL.md, with updated assertions where applicable.

1. Execute with `SKILL-improved.md` instead of original `SKILL.md`
2. Save outputs to `workspaces/<slug>/iteration-<N+1>/`
3. Grade with the same assertions (plus any new assertions added in Phase 10 step 6)
4. Generate a **comparison card** in `skill-cards/<slug>-v<VERSION>-improved.md`:
   - Original score vs improved score
   - Per-assertion delta (which failures were fixed?)
   - What changed in the SKILL.md and what effect it had
   - Which improvement strategy was used (from `knowledge/improve/patterns.md`)
5. Update leaderboard with improved scores (mark as "improved" variant)

**Success criteria:**
- Score improved by >= 1.5 points
- At least 50% of previously-failed assertions now pass
- No regression on previously-passing assertions

**If improvement fails** (score doesn't meaningfully improve):
- Document in skill profile why the skill is fundamentally limited
- Mark as `improvement-attempted` in registry
- Move on -- not every skill can be saved

### Phase 12: Improvement Engine Learning (Self-Evolution)

**This is the critical step that makes the improvement engine self-evolving.**

After each improvement batch (Phase 10-11), update the improvement knowledge base:

1. **Update `knowledge/improve/lessons.md`:**
   - What improvement strategies worked? By how much did scores increase?
   - What strategies failed? Why?
   - Any new root cause patterns discovered?
   - Any model-specific insights? (Does GPT-4.1 improve skills differently than Claude?)

2. **Update `knowledge/improve/patterns.md`:**
   - For each successful improvement, extract the reusable pattern
   - Structure: `Category -> Root Cause -> Strategy -> Expected Gain`
   - Example: `Reference Manual -> Redundant content -> Delete 70%, add MUST/ALWAYS/NEVER -> +1.5 to +2.0 points`
   - Track success rate per pattern (how often does this strategy work?)

3. **Update `knowledge/improve/failures.md`:**
   - Document each failed improvement attempt
   - Root cause analysis: why didn't the strategy work?
   - Was the skill fundamentally limited, or was the strategy wrong?
   - Add "do not attempt" markers for known dead ends

4. **Absorb into Phase 10:**
   - Review the improvement knowledge files
   - Fold proven patterns back into the Phase 10 process guidance
   - Update the diagnosis checklist with new root causes
   - Update strategy selection with new proven patterns
   - This is the improvement engine's equivalent of Phase 9 (absorb into SKILL-EVAL.md)

**The improvement loop: improve -> re-eval -> learn -> better improvements. If improvement lessons don't flow back, the improvement engine is static.**

### Latest absorbed changes (Batch 3, 2026-03-09)
- Added **phantom tooling check** in pre-flight to catch skills that reference missing scripts/binaries.
- Added guidance to prefer **methodology/structure assertions** over correctness assertions for technical domains where baseline is already strong.
- Added **multilingual assertion guidance** (Chinese/English keyword variants) to reduce false negatives.
- Added category pattern for **style-constrained writing skills** with banned-word deterministic checks.
- Added benchmark annotation for **phantom-tooling** to separate framework value from operational readiness.

### Absorbed changes (Full Re-Eval + Skill Improve, v0.3.0, 2026-03-09)
- Added **reference manual anti-pattern** detection to Phase 1 pre-flight: if SKILL.md >200 lines of educational content (code templates, API references, framework guides), flag as overhead risk. Skills should be behavioral contracts, not textbooks.
- Added **library-as-skill anti-pattern** detection: SKILL.md containing Python/JS class definitions or library code should be rewritten as behavioral instructions.
- Updated Phase 10 (Skill Improve) with proven improvement formula: **Remove > Add**. Start by deleting reference content the model already knows, then add behavioral mandates (MUST/ALWAYS/NEVER).
- Added guidance to Phase 11: when improving a skill, also update assertions to test new behavioral mandates. Otherwise improvement may not register in scores.
- Updated scoring system: zero delta + high overhead now penalizes efficiency score more heavily.
- Added **overhead-sensitive skills** category pattern for skills that are mostly reference material.

### Absorbed changes (v0.4.0, 2026-03-10)
- **Multi-model support**: Added `evals/models.json` config with three model roles: execution, judge, improvement. Skills can now be evaluated across multiple models for cross-model consistency. Per-skill model overrides supported in eval configs.
- **Cross-model evaluation mode**: When multiple execution models are configured, the engine runs the full with/without pair for each model and produces a per-model score matrix.
- **Judge model separation**: Rubric-based grading (Layer 2) now uses a configurable judge model separate from the execution model to prevent self-grading bias.
- **Self-evolving Skill Improvement Engine** (Phase 10 redesign): The improvement engine now has its own knowledge base at `knowledge/improve/` with `lessons.md`, `patterns.md`, and `failures.md`. Before improving any skill, the engine reads its learned patterns, selects a strategy, and documents results. After each improvement batch, Phase 12 updates the improvement knowledge base -- the improvement engine evolves independently from the eval engine.
- **Phase 12 added**: Improvement Engine Learning step that closes the improvement self-evolution loop (improve -> re-eval -> learn -> better improvements).
- **Improvement pattern library seeded**: 5 initial patterns (Reference Manual Slim-Down, Library-to-Instructions, Phantom Tooling Replacement, Overhead Routing, Assertion-Aligned Rewrite) with success rates from v0.3.0 data.
- **Batch evaluation updated**: Pipeline now includes Phase 12 (improvement learning) and per-model breakdowns in leaderboard.

---

## Scoring System

**Overall Score: 0-10**

| Component | Points | Criteria |
|-----------|--------|----------|
| Quality | 0-5 | Based on with-skill pass rate |
| Value-add | 0-3 | Delta between with-skill and without-skill pass rates |
| Efficiency | 0-2 | Time/token overhead relative to baseline |

| Score | Verdict | Meaning |
|-------|---------|---------|
| 7-10 | Recommended | Clear value over baseline |
| 5-6.9 | Conditional | Some value with trade-offs |
| 3-4.9 | Marginal | Overhead without proportional improvement |
| 0-2.9 | Not Recommended | Baseline is comparable or better |

---

## Versioning

- Engine version in `VERSION` (semver)
- Each skill card records engine version
- Re-evaluations with new engine version get new cards (old preserved)
- Eval configs in `evals/<slug>.json` are versioned implicitly through git

---

## Batch Evaluation

1. Read `evals/skill-registry.json` and `evals/models.json`
2. Process skills sequentially (or small batches)
3. For each: pre-flight -> test -> execute (per model) -> grade (with judge model) -> card -> leaderboard
4. After batch: run eval learning step (Phase 8-9)
5. Skill-improve pass: for any skill scoring < 7, run Phase 10-11 (improve + re-eval)
6. Improvement learning step: run Phase 12 (improvement engine self-evolution)
7. Final absorption: absorb both eval and improvement lessons into SKILL-EVAL.md
8. Update leaderboard with both original and improved scores, per-model breakdowns
