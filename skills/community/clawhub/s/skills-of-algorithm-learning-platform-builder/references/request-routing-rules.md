# Request Routing Rules

This file defines how to route user requests into the correct output mode for the algorithm-learning-platform-builder skill.

Its purpose is to help the skill decide:
- what the user is really asking for
- whether the result should be planning-only or full generation
- whether the request is best handled as a single algorithm page, comparison page, or reusable platform
- whether html should be generated immediately or after planning
- how to handle ambiguous, mixed, or overly broad requests

---

# Table of Contents

1. Purpose
2. Core routing principle
3. Step-by-step routing order
4. Request type routing
5. Scope routing
6. Audience routing
7. Output mode routing
8. Ambiguous request routing
9. Upgrade request routing
10. Html generation routing
11. Comparison routing
12. Reusable platform routing
13. Final routing checklist

---

# 1. Purpose

Not every request should be handled the same way.

Some users want:
- a simple explanation
- a structured plan
- a single teaching page
- a comparison page
- a reusable learning platform
- complete runnable html
- an upgrade path for an existing page

This file helps the skill choose the correct response mode before generating output.

---

# 2. Core Routing Principle

Always route in this order:

1. identify what the user wants now
2. identify how broad the algorithm scope is
3. identify whether the user wants explanation, planning, generation, or upgrading
4. identify whether the request should stay focused or become modular
5. choose the smallest correct output that still has strong teaching value

General rule:
- do not overbuild
- do not under-explain
- do not generate full html too early when planning is clearly needed
- do not return planning only when the user explicitly asks for complete runnable code

---

# 3. Step-by-Step Routing Order

When a request arrives, decide in this sequence:

## Step 1
Determine whether the request is mainly:
- explanation
- planning
- generation
- comparison
- upgrade

## Step 2
Determine whether the algorithm scope is:
- one algorithm
- several algorithms
- one family of algorithms
- a general reusable platform

## Step 3
Determine whether the expected output is:
- structured outline
- teaching page content
- complete runnable html
- architecture or upgrade advice

## Step 4
Determine whether the user level suggests:
- beginner-first explanation
- advanced mathematical detail
- mixed teaching + implementation output

Then choose the final route.

---

# 4. Request Type Routing

## 4.1 Planning-only requests

Use planning mode when the user asks for:
- a design plan
- a page structure
- a section arrangement
- what should be included
- how to improve a page
- how to build a platform before code generation

Typical signals:
- “帮我规划”
- “给我一个结构”
- “先设计一下”
- “先不要代码”
- “先给我方案”
- “how should I build this”
- “what should this page include”

### Output mode
Return:
- page goal
- page type
- teaching structure
- formulas to explain
- numerical substitution points
- interactions
- charts
- upgrade path

Do not jump straight to full html unless the user also clearly requests it.

---

## 4.2 Direct generation requests

Use generation mode when the user clearly asks for:
- a complete page
- page content
- full html
- a runnable demo
- directly usable code

Typical signals:
- “直接给我 html”
- “生成完整页面”
- “给我完整代码”
- “做一个可运行 demo”
- “build the page”
- “generate runnable html”

### Output mode
Return:
- structured teaching content first if needed
- then full runnable html if requested

If the scope is complex, planning can still be brief, but do not refuse the full generation request.

---

## 4.3 Explanation-first requests

Use explanation mode when the user mainly wants:
- algorithm understanding
- formula explanation
- derivation explanation
- intuition and computation explanation

Typical signals:
- “讲清楚这个算法”
- “解释公式”
- “推导一下”
- “一步一步讲”

### Output mode
Return:
- concept explanation
- formula explanation
- numerical substitution
- optional page proposal if useful

Do not force html generation unless the user wants a page or demo.

---

## 4.4 Upgrade requests

Use upgrade mode when the user asks:
- how to improve an existing page
- what is missing
- how to make it more reusable
- how to evolve from one page to a platform
- what should be modified in the current design

Typical signals:
- “怎么升级”
- “哪里要改”
- “帮我增强”
- “怎么改成平台”
- “如何泛化”
- “what should I improve”

### Output mode
Return:
- current strengths
- missing pieces
- maturity level
- upgrade priorities
- recommended target structure
- updated version if requested

---

# 5. Scope Routing

## 5.1 Single algorithm route

Use a single algorithm page when:
- the user names one algorithm
- the user wants one method explained deeply
- the algorithm already has enough teaching depth by itself

Examples:
- TOPSIS
- PCA
- KMeans
- gradient descent
- Newton interpolation

### Default output
- one algorithm page
- one set of formulas
- one computation flow
- one focused interaction set

---

## 5.2 Comparison route

Use a comparison page when:
- the user names two or more algorithms
- the user asks for differences
- the user asks which algorithm is better
- the teaching value comes from contrast

Typical signals:
- “比较”
- “区别”
- “优缺点”
- “哪个更好”
- “vs”
- “compare”

### Default output
- shared problem setup
- visible formula differences
- visible workflow differences
- parameter comparison
- chart comparison
- recommendation section

---

## 5.3 Reusable platform route

Use platform mode when:
- the user wants a general platform
- the user wants one structure for many algorithms
- the user wants extension, switching, or modularity

Typical signals:
- “平台”
- “通用”
- “可扩展”
- “支持多个算法”
- “切换算法”
- “algorithm selector”
- “reusable”

### Default output
- stable page shell
- shared input area
- shared parameter area
- switchable algorithm module area
- reusable chart and result area

---

# 6. Audience Routing

## 6.1 Beginner route

Use beginner-first teaching when the user appears to need:
- lower jargon
- clearer intuition
- more visible examples
- more step-by-step substitution

Beginner outputs should:
- explain intuition before formulas
- reduce symbolic density
- show more local numerical substitution
- keep interactions simple and visible

---

## 6.2 Advanced route

Use advanced teaching when the user clearly wants:
- derivations
- detailed formulas
- parameter interpretation
- theory comparison
- stronger mathematical structure

Advanced outputs should:
- include more formula detail
- compare variants where relevant
- explain deeper tradeoffs
- remain structured and readable

---

# 7. Output Mode Routing

Choose among these output modes:

## Mode A — Concept Explanation
Use when the user mainly wants understanding.

## Mode B — Structured Plan
Use when the user mainly wants design, architecture, or preparation.

## Mode C — Teaching Page Content
Use when the user wants a page structure and educational content, but not necessarily full html yet.

## Mode D — Complete Runnable Html
Use when the user explicitly wants directly runnable output.

## Mode E — Upgrade Analysis
Use when the user wants to improve an existing page or platform.

---

# 8. Ambiguous Request Routing

When a request is ambiguous, apply these rules:

## 8.1 If the user asks broadly for a “page” or “platform”
Default to:
- a structured plan first
- then html if explicitly requested

## 8.2 If the user asks for “完整代码” or “直接可运行”
Return runnable html after a brief structural setup.

## 8.3 If the user asks for “讲解 + 页面 + 对比” all at once
Use:
- comparison page plan first
- then structured content
- then html if requested

## 8.4 If the request is too broad to implement cleanly in one step
Prefer:
- reusable platform plan
instead of
- prematurely generating a weak all-in-one page

---

# 9. Upgrade Request Routing

If the user is improving something that already exists, do not treat it as a blank-page request.

Instead:
1. identify the current page type
2. identify current maturity level
3. identify missing teaching value
4. identify best next upgrade
5. propose or generate the upgraded version

Use `platform-upgrade-rules.md` for upgrade prioritization.

---

# 10. Html Generation Routing

Generate html immediately when:
- the user explicitly asks for html
- the user asks for runnable code
- the user asks for a browser demo
- the page scope is already clear

Do not generate html immediately when:
- the request is mostly architectural
- the user explicitly wants planning only
- the request is highly ambiguous and would likely produce poor code without routing first

When html is generated:
- use a single-file page by default
- keep the output runnable in a browser
- preserve teaching structure
- ensure formulas, interactions, and charts are coherent

---

# 11. Comparison Routing

If the request includes multiple algorithms, decide whether the output should be:
- multiple isolated single pages
or
- one true comparison page

Default rule:
If the user is trying to understand differences, choose one comparison page.

Only separate them into isolated pages when:
- the user explicitly asks for separate pages
- each algorithm requires a very deep standalone treatment

---

# 12. Reusable Platform Routing

If the request contains both:
- multiple algorithms
- desire for extension or switching

Then default to reusable platform mode instead of a one-time comparison page.

A reusable platform should:
- keep the shell stable
- allow algorithm switching
- separate common and algorithm-specific logic
- support future expansion

---

# 13. Final Routing Checklist

Before generating output, confirm:

- Is the selected mode correct for the user’s actual request?
- Is the scope correct: single page, comparison page, or platform?
- Is the output level correct: explanation, plan, content, html, or upgrade?
- Is the audience level reflected correctly?
- Is the response too broad or too narrow?
- Would a smaller but stronger output serve the user better?

If several answers are uncertain, prefer:
- planning before code
- comparison before scattered summaries
- reusable platform before hard-coded overgrowth
- educational clarity over feature quantity