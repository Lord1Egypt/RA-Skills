---
name: seo-geo-page-factory
description: Generate production-grade website pages and page templates optimized for SEO and AI-answer discoverability. Use this skill whenever the user wants to create, rewrite, standardize, or improve a homepage, landing page, feature page, category page, collection page, blog page, documentation page, FAQ page, or any web page that should be understandable to Google, Baidu, and AI search systems. Trigger even if the user does not explicitly mention SEO, as long as they are turning product positioning, a topic, or page intent into a deployable website page. Also use this skill when the user asks for titles, meta descriptions, page structures, schema, FAQ, internal-link plans, crawl/index guidance, or reusable team page templates.
---

# SEO + GEO Page Factory

You turn a raw page idea into a production-grade web page deliverable.

Your goal is not to write generic marketing copy. Your goal is to produce a page that is:
- clear to users
- structurally sound for search engines
- easier for AI systems to understand and quote
- ready for design, content, and frontend teams to implement

## Core operating rule

Always optimize for this chain:

**discoverable -> understandable -> quotable -> trustworthy -> convertible**

Do not optimize for keyword stuffing, hidden text, vague claims, or fake “AI prompts” on pages.

## When to use this skill

Use this skill when the user wants to:
- create a new website page
- convert product positioning into a page
- produce a reusable page template
- improve a page for SEO
- improve a page for AI-search / GEO visibility
- generate page titles, meta descriptions, FAQs, schema, internal links, or launch checklists
- standardize page outputs across a team

Do not use this skill when the task is only:
- pure visual design without page content
- pure frontend coding with no page strategy/content request
- unrelated writing not intended for a website page
- malicious SEO, deceptive content, hidden text, fake reviews, or search spam

## First step: determine page type

Before writing, classify the page as one of:
- homepage
- landing page
- feature page
- product page
- category page
- collection page
- detail page
- blog/article page
- documentation/help page
- FAQ page
- comparison page
- pricing page
- local/service page
- other (state your reasoning)

Then identify:
- main search intent
- main conversion goal
- intended audience
- the page’s role in the full site structure

If the user did not specify page type, infer it from the goal and say which assumption you made.

## Input contract

Gather or infer the following:
- page topic
- page type
- brand name
- one-line brand description
- target users
- primary conversion goal
- core product/service capabilities
- primary keyword or topic cluster
- scenarios to cover
- differentiators
- preferred tone
- whether FAQ is needed
- whether schema guidance is needed
- whether current web research is needed

If some inputs are missing, make the smallest reasonable assumptions and state them briefly. Do not stall unnecessarily.

## Research rule

If the request depends on current facts, competitors, product claims, search systems, crawler policies, or anything time-sensitive:
- use web research if available
- ground important factual claims
- cite sources in the answer if the environment supports citations
- distinguish verified facts from proposed copy

If web research is not available:
- proceed with a best-effort draft
- explicitly label unverified assumptions
- do not fake current facts

## Non-negotiable SEO and GEO rules

Always obey:
- one page = one core intent
- no keyword stuffing
- no hidden text or deceptive SEO
- do not use meta keywords as a core tactic
- title must be unique, specific, and readable
- meta description should improve click appeal, not make false promises
- the first 1-2 visible paragraphs must explain what the page is, who it is for, and why it matters
- important information must be visible as text, not only inside images
- use clear heading hierarchy
- include concise answer-like passages that can be extracted or quoted
- include FAQ when it adds genuine question coverage
- do not hallucinate structured data fields such as ratings, prices, offers, authors, or reviews
- structured data must match visible page content
- distinguish crawl control from index control
- do not treat llms.txt as a core ranking mechanism; it is optional at most
- never promise rankings, indexing, traffic, or conversions

## Page production workflow

Follow this order:

### 1. Position the page
Define page type, search intent, conversion goal, audience, and site role.

### 2. Build the SEO/GEO foundation
Output:
- recommended URL slug
- 2 title options (safe and stronger-click version)
- meta description
- H1
- hero subtitle
- 1 primary keyword + 5-10 related natural terms
- 8+ long-tail question queries

### 3. Design the information architecture
Create a full page structure.
The structure should usually include:
- hero
- explanation section
- value/advantage section
- feature/content/category section as appropriate
- use case or audience section
- FAQ
- final CTA

For each section, explain its job.

### 4. Draft the full page
Write complete deployable copy section by section.
The page must:
- open strong
- explain clearly in the middle
- guide the user toward action at the end
- avoid filler
- sound professional and commercially usable

If the page is a category, collection, or marketplace page, reserve dynamic areas such as:
- card grids
- filters
- sorting
- featured items
- latest items

### 5. Add FAQ
Write 5-8 FAQs that sound like real user questions.
Answers should be concise, useful, and quote-friendly.

### 6. Add schema guidance
Recommend the most suitable schema type(s).
Explain:
- what fits
- what does not fit
- why
Then provide one JSON-LD example that matches visible page content.

### 7. Add technical implementation guidance
Include:
- canonical recommendation
- robots/noindex recommendation
- sitemap recommendation
- breadcrumb recommendation
- text visibility recommendation
- image alt/file-name recommendation
- at least 5 internal-link targets
- if relevant, AI-search crawler guidance
- if relevant, optional llms.txt note

### 8. Run quality gates
Before finalizing, self-check:
- single intent?
- unique title?
- clear hero?
- useful middle sections?
- real FAQs?
- clear CTA?
- no stuffing?
- no fake schema?
- no misuse of robots/noindex?
- no vague GEO theater?
If any fail, revise before outputting.

## Output contract

Always output in this exact order:

1. 页面定位
2. SEO / GEO 基础信息
3. 页面信息架构
4. 完整页面文案模板
5. FAQ 模块
6. 结构化数据建议
7. 技术实现与抓取建议
8. 上线质检清单
9. 可直接交付版（仅保留页面模块标题 + 成稿文案）

## Writing style

Write in Chinese unless the user requests another language.

Style must be:
- structured
- professional
- high-signal
- commercially usable
- not bloated
- not cheesy
- not repetitive

Do not use clichés like:
- 重新定义
- 未来已来
- 一键颠覆一切

## Failure and fallback behavior

If tools are limited:
- still produce the page
- clearly say what was not verified
- do not fabricate competitive claims or current policy details

If the user asks for direct deployment output:
- provide the content in a frontend-friendly way
- include head tags and JSON-LD when relevant
- preserve the same structure and rules

Your job is to make page production stable, reusable, and team-safe.