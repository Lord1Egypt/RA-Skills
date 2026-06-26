# Step Prompts for Technical Research

## Step 0: Reconnaissance & Feasibility Assessment Prompt

Analyze the following scraped content about [Vendor] [Solution Model] and generate a Research Feasibility Brief.

**Input**: Cleaned text from initial search results.

**Required Output**:
1. Estimated volume of obtainable public information (High/Medium/Low)
2. List of key information sources with URLs
3. Recommended breakdown granularity (Entry/Advanced/Extreme) based on info volume
4. Prompt asking user whether to continue with deep-dive steps

---

## Step 1: Overall Architecture Anchoring & Information Boundary Mapping

**Task**: Based on the provided context, generate a comprehensive overall architecture analysis.

**Required Output Structure**:
1. Solution Core Positioning (what problem does it solve, in what scenario)
2. Overall Technical Architecture (layered breakdown: hardware layer, software layer, communication layer)
3. Public Information Boundary Description (what is publicly available vs. what is proprietary/hidden)
4. Suggested priorities for subsequent research steps

**Annotation Requirements**:
- Each module must be annotated with source: `[Public: URL/Patent#]` or `[Derived]` or `[Info Missing]`
- Never mix facts and derivations without clear labels

---

## Step 2: Hardware System Deep-Dive

**Task**: Generate a full-dimensional hardware breakdown report.

**Required Output Structure**:
1. Hardware System Topology & Signal Flow (how components connect and communicate)
2. Core Module Breakdown (for each module: Function, Internal Composition/Components, Selection Rationale & Parameters, Interface & Protocols)
3. Hardware Full-Link Working Principle (end-to-end operational flow)

**Comprehensibility Check**:
- Check for logical gaps in core function implementation principles
- If unclear after supplementary research, annotate `[Derived: based on similar solutions]` or `[Manual supplement needed]`

---

## Step 3: Software System Deep-Dive

**Task**: Generate a full-dimensional software breakdown report.

**Required Output Structure**:
1. Software Layered Architecture (OS/middleware/application/algorithm layers)
2. Layer-by-Layer Deep Breakdown (for each layer: responsibilities, key components, data flow)
3. Software Foundation Environment (runtime dependencies, frameworks, libraries)

**Depth Cap**:
- Supplementary research depth capped at "block diagram level" or "pseudocode logic level"
- No deep mathematical derivations unless Extreme granularity requested

---

## Step 4: Hardware-Software Co-Design Full-Link Closed-Loop Principles

**Task**: Generate co-design analysis based on prior hardware and software breakdowns.

**Required Output Structure**:
1. Core Co-Design Interfaces & Division of Labor (what each side handles, where they meet)
2. Normal Operation Full-Link Timing Coordination (step-by-step timing diagram in text)
3. Abnormal Condition Coordination Mechanisms (error handling, fallback, recovery)

**Consistency Check**:
- Ensure timing descriptions are complete (data sent → receiver processing → response)
- Only supplement mainline flow gaps; do not expand all exception branches

---

## Step 5 Prompt (includes Credibility Scorecard instruction)

**Task**: Based on the complete preceding breakdown content, complete technical feature extraction and industry benchmarking analysis. At the end of the output, you MUST attach an "Information Credibility Overview" table.

## Mandatory Output Structure
1. Core Technical Features & Differentiators
2. Core Technical Barriers & Patent Protection Points
3. Quantitative Performance Benchmarking
4. Solution Deployment Suitability & Limitations
5. Research Summary (≤100 words)

6. **Information Credibility Overview Table** (New):
   Generate a table in the following format, tallying facts/derivations/gaps per chapter, and assign star ratings (⭐, max five stars).

   | Chapter | Fact Ratio | Derivation Ratio | Gap Count | Credibility Rating |
   |---------|------------|------------------|-----------|--------------------|
   | Overall Architecture | XX% | XX% | X | ⭐⭐⭐⭐ |
   | ... | ... | ... | ... | ... |
   **Overall Credibility Rating**: ⭐...

   Rating Reference:
   - Fact ratio ≥80% and gaps=0: ⭐⭐⭐⭐⭐
   - Fact ratio 60-80%: ⭐⭐⭐⭐
   - Fact ratio 40-60%: ⭐⭐⭐
   - Fact ratio 20-40%: ⭐⭐
   - Fact ratio <20%: ⭐

## Absolute Prohibitions
- Do not fabricate component parameters, algorithm details, or performance metrics
- Do not copy vendor marketing language verbatim
- Do not generalize from industry common knowledge to this specific solution
- Do not produce vague statements without source attribution
