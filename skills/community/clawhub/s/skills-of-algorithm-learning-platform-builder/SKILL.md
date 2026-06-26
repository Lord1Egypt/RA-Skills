---
name: algorithm-learning-platform-builder
description: build interactive algorithm learning pages, comparison pages, and reusable teaching platforms for algorithms. use when chatgpt needs to plan, route, structure, explain, compare, or generate educational algorithm content with formulas, derivations, numerical substitution, step-by-step calculations, charts, interaction controls, family-aware teaching patterns, upgrade guidance, or complete runnable html demos. especially useful for turning algorithm explanations into interactive course pages, visualization-heavy study tools, or extensible algorithm learning platforms.
---

# Core behavior

Use this skill when the user wants to:
- turn an algorithm explanation into an interactive teaching page
- generate a runnable html algorithm demo
- build a dynamic algorithm learning platform
- compare multiple algorithms in one teaching page
- create formula-driven, chart-rich, step-by-step educational content for any algorithm
- upgrade an existing algorithm page into a stronger teaching platform
- generalize a one-off algorithm page into a reusable platform structure

This skill is for educational page generation, not production deployment.
Default output should be structured, interactive, browser-runnable, and teaching-oriented.

# Workflow

Follow this order unless the user explicitly asks to skip planning:

1. identify the request type
2. identify the algorithm scope
3. identify the intended audience
4. decide the page type
5. design the teaching structure
6. identify formulas that must be explained
7. identify steps that must include numerical substitution
8. identify interaction controls
9. identify charts and visual components
10. generate structured content
11. generate runnable html if requested
12. run final quality checks

## 1. Identify the request type

Classify the request into one of these types:
- single algorithm teaching page
- multi-algorithm comparison page
- reusable algorithm learning platform
- planning-only request
- full runnable html request
- upgrade request for an existing page or platform

If the request is broad or ambitious, plan first.
If the user explicitly asks for complete code, provide complete runnable html after planning.
If the request mixes planning, comparison, and generation, use `references/request-routing-rules.md` to decide the best output mode.

## 2. Identify the algorithm scope

Determine whether the requested content is about:
- one specific algorithm
- a family of related algorithms
- a comparison between multiple algorithms
- a generic reusable platform that should work for many algorithms

If the user names a specific algorithm, preserve algorithm-specific formulas and workflow.
If the user asks for a reusable platform, make the page architecture modular and extensible.

Then map the request to an algorithm family using `references/algorithm-family-maps.md`.

Use that mapping to decide:
- what the page should emphasize
- what formulas are central
- what numerical substitution is required
- what interactions are most useful
- what charts best fit the algorithm family
- whether the request should become a single page, a comparison page, or a reusable platform page

## 3. Identify the intended audience

Adapt the output to the user's level.

For beginners:
- use simpler language
- reduce jargon
- explain intuition before formulas
- always include more numerical substitution
- prefer more visible step-by-step interaction

For advanced users:
- allow more mathematical detail
- include formula comparisons
- include parameter interpretation
- include stronger theoretical distinctions

## 4. Decide the page type

Use one of these page structures:
- single algorithm page
- comparison page
- algorithm learning platform

Use the references in:
- `references/page-architecture.md`
- `references/algorithm-page-template.md`
- `references/comparison-page-template.md`
- `references/request-routing-rules.md`

If the request is ambiguous, mixed, or overly broad, prefer the page type recommended by `references/request-routing-rules.md`.

## 5. Design the teaching structure

Every algorithm page should combine:
- intuition
- formulas
- symbol explanation
- why the formula is used
- numerical substitution
- dynamic interaction
- charts
- results and summary

Do not produce concept-only pages unless the user explicitly asks for conceptual explanation only.

## 6. Identify formulas that must be explained

For each important formula, explain it in four layers:
1. write the formula
2. explain each symbol
3. explain why the formula is used
4. substitute concrete numbers whenever possible

This is a required output pattern for any algorithm teaching page.

## 7. Identify steps that must include numerical substitution

Whenever the algorithm has a real computation flow, include numerical substitution for at least these stages when possible:
- initialization
- key update rule
- scoring or loss calculation
- iteration result
- final conclusion or ranking

If exact numbers are not provided by the user, create a small teaching example dataset.

## 8. Identify interaction controls

Use interaction when it materially improves understanding.

Good candidates for interaction:
- parameter sliders
- dropdowns for task switching
- stepper buttons for multi-stage computation
- algorithm toggles for comparison pages
- chart updates linked to user input

Do not add interaction just for decoration.
Use it where the algorithm changes across steps, parameters, or variants.

## 9. Identify charts and visual components

Charts should reinforce the mathematics.
Prefer clear, educational visualizations.

Examples:
- loss curves
- score comparison bars
- probability curves
- radar charts
- residual charts
- cumulative update charts
- comparison tables

## 10. Generate structured content

When the user asks for planning only:
- provide a structured plan
- explain the page architecture
- explain how to upgrade it further
- identify the current maturity level if the user is improving an existing page
- identify the best next upgrade

When the user asks for content:
- produce structured, teaching-oriented content
- keep sections modular
- ensure mathematical consistency across sections

Before finalizing a plan or page, use `references/platform-upgrade-rules.md` to determine:
- the current maturity level of the output
- the most valuable next upgrade
- whether the page should remain single-algorithm or evolve into comparison/platform mode
- which improvements add teaching value first

## 11. Generate runnable html if requested

When generating html:
- prefer a single-file html page
- keep the output directly runnable in a browser
- use chart.js and mathjax when helpful
- keep the layout presentation-ready
- keep interaction smooth and beginner-friendly
- ensure the final output is complete and internally consistent
- do not omit required closing tags or script blocks

Use the html starter file in `assets/html-starter-template.html` when building a new single-file page.

## 12. Run final quality checks

Before returning any major output, validate it against `references/output-quality-checklist.md`.

Check:
- structural clarity
- educational value
- formula explanation quality
- numerical substitution completeness
- interaction usefulness
- chart relevance
- html completeness
- reusability when platform mode is requested

If several of these are weak, improve the output before finalizing.

# Design rules

Use the guidance from these references:
- `references/page-architecture.md`
- `references/explanation-patterns.md`
- `references/interaction-patterns.md`
- `references/algorithm-page-template.md`
- `references/comparison-page-template.md`
- `references/writing-rules.md`
- `references/algorithm-family-maps.md`
- `references/platform-upgrade-rules.md`
- `references/request-routing-rules.md`
- `references/output-quality-checklist.md`

# Output rules

## For planning requests
Output should include:
- page goal
- page type
- teaching structure
- formulas to explain
- numerical substitution points
- interactive controls
- chart list
- current maturity level if relevant
- best next upgrade
- upgrade path

## For html requests
Output should include:
- complete runnable html
- all required sections
- formulas and numerical explanation
- interaction controls if useful
- charts if useful
- a coherent teaching flow
- internal consistency between formulas, data, controls, charts, and results

## For upgrade requests
Output should include:
- what the current page already does
- what it is missing
- the current maturity level
- the most valuable upgrades in order
- the recommended target structure
- updated content or updated html if requested

# Important boundaries

- This skill is for learning pages, demos, course pages, algorithm explainers, and study tools.
- This skill is not for production-grade model training infrastructure.
- This skill should favor clarity, structure, and educational value over engineering complexity.
- If a request is better handled as a static outline rather than a full page, provide the outline first.
- If the request is ambiguous, broad, or mixes several goals, route it using `references/request-routing-rules.md` before generating output.

# Quality standard

A good output from this skill should make the user feel:
- the algorithm is understandable
- the formulas are not abstract anymore
- the numerical process is visible
- the page is runnable and presentable
- the structure is reusable for future algorithms
- the upgrade path is clear when the user wants to improve the platform