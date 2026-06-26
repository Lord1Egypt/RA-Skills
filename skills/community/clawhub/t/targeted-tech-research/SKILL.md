---
name: 定向技术方案深度拆解调研
description: Comprehensive deep technical research on vendor-specific technical solutions/products. Standardized output covering four core modules: Hardware Breakdown, Software Breakdown, Hardware-Software Co-Design, and Technical Benchmarking. Strictly distinguishes publicly verifiable facts from technical derivations, enabling progressive deep-diving from overall architecture down to core components/algorithms. This Skill orchestrates research logic, information analysis, and report generation. Actual scraping tasks are delegated to web-scraper and playwright-scraper. Use when user asks to research a specific technical solution, product architecture, vendor technology breakdown, or needs deep technical analysis with fact/derivation distinction. Trigger phrases include: 调研技术方案, 拆解某个产品技术, 分析某公司技术方案, 深度调研某产品, technical solution research, vendor technology breakdown, product architecture deep-dive, hardware software co-design analysis.
references:
  - references/prompts.md
  - references/rules.md
  - references/dynamic_sites_whitelist.json
---

# 定向技术方案深度拆解调研 Skill

This Skill performs comprehensive deep technical research on vendor-specific technical solutions/products, thoroughly solving the problems of AI generating shallow webpage summaries and regurgitating marketing language.

## I. Core Principles (Harness Engineering Constraints)

- **Scope Locking**: All outputs must strictly correspond to "Vendor Full Name + Solution Full Model + Application Scenario". Generalized industry common knowledge is prohibited.
- **Source Attribution**: 100% distinction between "Publicly Verifiable Fact" and "Technically Derived Content". Annotate at line endings: `[Public: Source]` or `[Derived]`.
- **Granularity Compliance**: Technical breakdowns must be precise down to "Module - Principle - Function - Interaction Logic".
- **No Marketing Fluff**: Prohibits copying vendor promotional language. Only structured principle breakdowns and objective analysis.
- **Logical Consistency**: Outputs across steps must be fully consistent and correspond with each other.
- **Comprehensibility-Driven**: Perform limited deep-diving for missing explanations of core principles, bounded by user-specified granularity and topic scope.

## II. Pre-Flight Preparation: Interactive Onboarding Questionnaire

Before starting research, confirm the following information through dialogue. Users may answer "skip" to use defaults, or use the quick-start command to bypass the questionnaire.

1. **Research Target Precision** (Required): Vendor full official name, technical solution/product full model, core deployment scenario.
2. **Research Priority**: Hardware / Software / Hardware-Software Co-Design / Technical Features, ordered by importance. (Default: Hardware > Co-Design > Software > Technical Features)
3. **Breakdown Granularity**: Entry-level (module functions only) / Advanced (module working principles) / Extreme (component selection/algorithm logic). (Default: Advanced)
4. **Terminology Explanation Preference**:
   - A. Zero Explanation (assumes reader domain knowledge)
   - B. Minimal Contextual Explanation (≤15-word contextual note for first occurrence of non-generic terms)
   - C. Full Definition (2-3 sentence definition plus relevance to this solution)
   (Default: B)
5. **Provided Sources** (Optional): User may provide patent numbers, whitepaper links, paper DOIs, etc., to be prioritized as primary sources.

### Quick-Start Mode

Users can directly send a command in the following format to skip the questionnaire and use all defaults:

```
research [Vendor Full Name] [Solution Full Model] [Application Scenario] --quick
```

Example: `research Framatome "Reactor Pressure Vessel Bolt Tensioning Robot System" "Nuclear Refueling Outage" --quick`

The Skill will then proceed directly to Step 0 Recon with default configurations.

### Pre-Flight Hook Response Handling

After invoking `hooks/pre_flight_check.py`, determine next actions based on the returned JSON:

- If `status` is `"passed"`: Proceed directly to Step 0 Recon.
- If `status` is `"incomplete"`:
  - Use the returned `prompt_for_user` field to politely ask the user for missing information. Wait for user response.
  - Once user provides missing details, re-invoke the Skill with the complete information for re-validation.

## III. Data Acquisition Strategy & Tool Selection Rules

This Skill does not directly execute network requests. All scraping tasks are delegated to sub-Skills and automatically selected according to the following rules.

### 3.1 Prioritize `web-scraper` (Lightweight Static Scraping)
Applicable for static HTML pages, RSS/Atom feeds, plain-text API responses.

### 3.2 Conditions to Trigger `playwright-scraper` (Any Match Triggers)
- Target URL matches any rule defined in `references/dynamic_sites_whitelist.json`.
- `web-scraper` returns content length < 200 characters, and contains keywords like `loading`, `JavaScript`, `enable`, `please enable JavaScript`.
- User instruction explicitly includes interaction verbs (e.g., "click", "switch tab", "scroll down").
- HTTP 403/406 is returned and response body contains no valid business data.

### 3.3 Low-Value Scenarios Prohibited from Triggering `playwright-scraper` (Blacklist)
- Comment sections or "related articles" widgets on news/blogs (always ignored).
- Pages requiring login or behind paywalls (immediately abandoned and marked as inaccessible).
- Purely visual showcase pages (3D showrooms, panoramas, interactive animations).
- PDF online preview pages (should extract direct PDF link and call `pdf-reader` or download directly).

### 3.4 Failure Handling & Degradation
- If `playwright-scraper` times out (>30s), abandon the URL and continue with available data.
- If 3 consecutive URLs time out, terminate the current scraping round and note the obstruction in the report.
- On scraping failure, **do not block subsequent steps**. Instead, insert a marker in the report at the corresponding position: `[Info Missing: Manual extraction needed from [Source]]` and aggregate all gaps at the end of the report.

## IV. 5-Step Progressive Research Workflow

### Step 0: Reconnaissance & Feasibility Assessment

**Goal**: Quickly assess the volume and usability of public information, generate a Research Feasibility Brief, and **wait for user confirmation** before proceeding to deep-dive steps.

1. Call `web-scraper` to search for `[Vendor Full Name] [Solution Model] whitepaper` and `patent`, obtaining titles, URLs, and snippets.
2. If PDF links exist, attempt to extract direct links; if PDF preview page, abandon and note.
3. If the source is a patent detail page or tech doc site (whitelisted), directly call `playwright-scraper` to extract key text.
4. **Content Cleaning**: Before feeding scraped text to LLM, invoke the cleaning script:
   ```bash
   python scripts/compress_content.py --max-length 3000 < raw_text.txt > cleaned_text.txt
   ```
5. Generate **Research Feasibility Brief** containing:
   - Estimated volume of obtainable public information (High/Medium/Low)
   - List of key information sources
   - Recommended breakdown granularity (dynamically based on info volume)
   - Prompt asking user whether to continue with deep-dive steps

**After user confirmation**, proceed to Steps 1-5.

### Step 1: Overall Architecture Anchoring & Information Boundary Mapping

1. **Context Preparation**: Use the cleaned text from Step 0 as core context. If user provided private PDFs/patents, also process via `scripts/compress_content.py` and merge.
2. The Skill invokes internal LLM, strictly following the **Step 1 Prompt** template in `references/prompts.md`.
3. Output must include: Solution core positioning, layered architecture, public information boundary annotation, suggested priorities for subsequent research.
4. Annotate each module with source: `[Public: URL/Patent#]` or `[Derived]` or `[Info Missing]`.

### Step 2: Full-Dimensional Deep-Dive on Hardware System

1. If Step 1 reveals insufficient public info for specific hardware modules:
   - Call `web-scraper` for supplementary searches using module names (e.g., "controller", "sensor").
   - If target is a whitelisted dynamic page, call `playwright-scraper`.
2. Generate initial hardware breakdown report following **Step 2 Prompt** template in `references/prompts.md`.
3. **Comprehensibility-Driven Deep-Dive Check**:
   - From the user's specified granularity perspective, check for logical gaps or unexplained core principles in the draft.
   - Trigger **limited supplementary research** (max 2 search rounds, strictly within topic scope) for:
     - Core function implementation principles (how hardware achieves its role).
     - Scenario-linked component selection rationale (why this specific part).
   - If still unclear after supplementary research, annotate `[Derived: based on similar solutions]` or `[Manual supplement needed: background knowledge on this tech point]`.
4. On scraping failure, insert `[Info Missing]` marker and log to gap list.

### Step 3: Full-Dimensional Deep-Dive on Software System

1. Similar to Step 2, perform supplementary scraping for software layers.
2. Generate initial software breakdown following **Step 3 Prompt** template.
3. **Comprehensibility-Driven Deep-Dive Check**:
   - Focus on core algorithm principles: are inputs/outputs/core steps clear?
   - Supplementary research depth capped at "block diagram level" or "pseudocode logic level"; no deep mathematical derivations (unless user requested Extreme granularity).
   - If unclear, annotate `[Derived]`.

### Step 4: Hardware-Software Co-Design Full-Link Closed-Loop Principles

1. Based on prior hardware and software breakdowns, generate initial co-design analysis.
2. Follow **Step 4 Prompt** template, breaking down normal and abnormal operating conditions by time steps.
3. **Comprehensibility-Driven Deep-Dive Check**:
   - Check for logical gaps in timing descriptions (e.g., data sent but no receiver processing described).
   - Only supplement mainline flow gaps; do not expand all exception branches.
   - If gap info is completely missing, mark `[Info Missing]`.

### Step 5: Technical Features & Industry Benchmarking (with Credibility Scorecard)

1. Extract core technical features, barriers, quantitative performance benchmarks, and deployment suitability.
2. Follow **Step 5 Prompt** template.
3. **Concurrently generate Credibility Scorecard** (embedded in Step 5 output):
   - Based on preceding content, tally the ratio of facts/derivations/gaps per chapter.
   - Present as a Markdown table with star ratings (⭐) per chapter.
   - If table formatting fails, silently omit this card; do not block report generation.
4. Output a core conclusion summary under 100 words.

### Step 5.6: Generate Auxiliary Enhancements

After the main report is generated:

1. **Generate Researcher's Narrative**:
   ```bash
   python scripts/generate_narrative.py --meta /path/to/execution_meta.json --output /tmp/narrative.txt
   ```
   Insert the output into the report as `Appendix C: Researcher's Narrative`.

2. **Generate Reproducible Research Recipe**:
   Extract `input` and `config` fields from `execution_meta.json` and format per `Appendix B` in `assets/report_template.md`.

3. **Aggregate Information Gaps**:
   Compile the gap list recorded during execution into a table per `Appendix A` format in the template.

## V. Report Output & Auxiliary Enhancement Features

### 5.1 Main Report Structure (User-Facing)

```markdown
# [Vendor] - [Solution Full Model] Technical Research Report

## Executive Summary (≤100 words)

## Chapter 1: Overall Architecture Anchoring & Information Boundaries

## Chapter 2: Hardware System Deep-Dive

## Chapter 3: Software System Deep-Dive

## Chapter 4: Hardware-Software Co-Design Principles

## Chapter 5: Technical Features & Industry Benchmarking (incl. Credibility Scorecard)

## Appendix A: Information Gaps & Manual Intervention Suggestions
| Gap ID | Target URL | Missing Description | Suggested Manual Action |

## Appendix B: Research Recipe (Reproducible Config)
(code block)

## Appendix C: Researcher's Narrative (First-Person Reflection)
(≤150 words)

## Appendix D: Source Attribution Summary (Optional)
```

### 5.2 Auxiliary Enhancement Features (Non-Core; Fail Silently)

| Feature | Implementation | Degradation Strategy |
| :--- | :--- | :--- |
| **Credibility Scorecard** | Generated inline by LLM in Step 5. Zero extra calls. | Silently omit if formatting fails. |
| **Researcher's Narrative** | Generated by `scripts/generate_narrative.py` from meta JSON using templates. **Zero LLM calls.** | Omit appendix if script fails or meta missing. |
| **Reproducible Recipe** | Extracted from `execution_meta.json` fields. **Zero LLM calls.** | Omit if meta missing. |
| **Silent Evidence Package** | Async save of raw scraped text to `evidence/` directory. Report links with `[Evidence]` anchors. **Zero LLM calls.** | Log only; omit links if save fails. |

### 5.3 Audit Trail Metadata (Not User-Facing; For Audit & Evaluation)

Each run generates `execution_meta.json` in the output directory, containing:
- Input parameters
- Execution statistics
- Scraping details
- Information boundary counts
- Compliance check results

## VI. Resource Policy & Token Efficiency Principles

This Skill adheres to the following efficiency principles to control usage costs:

1. **Minimal LLM Calls**: Only the 5 core analysis steps invoke LLM. All enhancements use deterministic scripts or templates with zero extra LLM overhead.
2. **Context Compression**: All scraped text is cleaned via `scripts/compress_content.py` before entering LLM context (tags stripped, single-source capped at 3000 chars).
3. **Step-Wise Context Reuse**: Subsequent steps only reference summary conclusions from prior steps, avoiding context bloat.
4. **User-Controlled Verbosity**: Users may select "Brief Mode" in the questionnaire (output compressed ~50%), or append `--brief` flag in quick-start.
5. **Auxiliary Features Silent Degradation**: All non-core enhancements fail silently without retries or remedial LLM calls.

**Estimated Token Consumption** (GPT-4o equivalent, medium-info scenario):
- Detailed report mode: ~8,000 – 15,000 tokens
- Brief mode: ~4,000 – 7,000 tokens

## VII. Quick-Start Example

Simulated complete interaction:

**User**:
`research Framatome "Reactor Pressure Vessel Bolt Tensioning Robot System" "Nuclear Refueling Outage" --quick`

**Skill (Internal)**:
1. Adopts default config, enters Step 0 Recon.
2. Discovers Google Patents link, triggers Playwright.
3. Generates Feasibility Brief and automatically proceeds to deep steps (due to `--quick`).
4. Executes Steps 1-5; in hardware section, notes missing hydraulic valve specs, performs one supplementary search without success, marks gap.
5. Generates final report with scorecard, narrative, recipe, and evidence links.

**Final Report Snippet**:
> ### 2.3 Hydraulic Control Unit
> **Core Components**: Proportional servo valve [Public: Patent USXXXX].
> **Specific Model & Key Parameters: [Info Missing: Manual check from equipment nameplate or supplier]**
> *(See Appendix A: Information Gap GAP-01)*

## VIII. Capability Boundary Statement

**This Skill Accepts**:
- Full-dimensional breakdown of targeted technical solutions (vendor+model+scenario clear).
- Automated research based on public internet information.
- User-provided patents/whitepapers as priority sources.

**This Skill Rejects**:
- Generalized industry analysis, market research, financial analysis.
- Bypassing login walls, paywalls, CAPTCHAs.
- Fabricating undisclosed component parameters or algorithm details.
- Infinite recursive deep-diving into a single technical detail (strict depth limits).

**Boundary Behaviors**:
- Vague input → Guide user to refine.
- Dynamic scraping failure → Mark gap, do not block workflow.
- Insufficient info for specified granularity → Degrade output and inform user.

## IX. Execution Directives & Exception Handling

Detailed directives and checklists are in `references/rules.md`. Core requirements:
1. Scope Locking: Strict correspondence to target solution.
2. Source Attribution: Clear distinction between fact and derivation.
3. Granularity Compliance: No vague statements.
4. No Marketing: No copying promotional text.
5. Logical Consistency: Consistency across steps.
6. Comprehensibility: Core principles must be explained within topic boundaries.

Common exceptions:

| Scenario | Handling |
| :--- | :--- |
| Playwright interaction failure (tab not found) | Record gap, insert `[Info Missing]`, aggregate in Appendix A. |
| All scraping sub-Skills return empty | Pause workflow, request user to provide private sources or adjust keywords. |
| Output judged as vague or marketing fluff | Re-invoke step prompt with additional emphasis directive. |

---
*This Skill follows Harness Engineering design principles, ensuring reliability, controllability, and measurability.*
