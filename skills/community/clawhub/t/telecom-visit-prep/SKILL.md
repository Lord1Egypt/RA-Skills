---
name: telecom-visit-prep
version: 1.0.1
description: China Telecom account manager enterprise visit preparation assistant. Input company name to auto-search info, generate business opportunities and visit scripts.
author: KeyangWang0726
homepage: https://github.com/KeyangWang0726/telecom-visit-prep
---

# Telecom Visit Prep

One-stop enterprise visit preparation for China Telecom account managers: input a company name, automatically search enterprise information, intelligently recommend business opportunities, generate visit scripts, and output a complete visit preparation report.

## Trigger Scenarios

Use this skill when the user mentions: "走访" (visit), "拜访" (call on), "准备报告" (prepare report), "了解一下这家公司" (learn about this company), "看看什么商机" (check business opportunities), "拜访准备" (visit preparation), "客户信息" (customer info), "市场开拓" (market development), or directly inputs an enterprise name requesting a visit preparation report.

## Prerequisites

### Search Tool

This skill requires a **web search capability** to collect enterprise information. Ensure one of the following is available:

- **MCP search server** (recommended): Install an MCP search tool such as `@anthropic/mcp-web-search` or `@anthropic/mcp-brave-search`
- **Built-in web search**: If your agent platform provides native web search (e.g., `web_search`, `baidu_search`), use it directly
- **WebFetch + Shell**: Fallback to fetching web pages via HTTP requests

If no search tool is available, the skill can operate in **degraded mode**: ask the user to provide enterprise information manually, then proceed with profile building, opportunity recommendation, and report generation.

### Document Generation (Optional)

Word document export is optional. If available:

- **python-docx**: Run `pip install python-docx` to enable .docx export
- **MCP document server**: If an MCP docx server is configured, use it for document generation
- **Fallback**: Output the report in Markdown format within the conversation

## Workflow

```
Prerequisites check -> Input enterprise name -> Search enterprise info -> Build customer profile -> Match business opportunities -> Create visit plan -> Generate communication scripts -> Output report
```

Execute the following 6 steps in order:

### Step 1: Multi-dimensional Enterprise Information Search

Use your available web search tool to conduct multiple rounds of searches. Search dimensions and strategy:

| Search Round | Search Keywords Template | Information Target |
|---------|--------------|---------|
| Round 1 | `"{Enterprise Full Name}" 工商信息 简介` | Basic business registration, founding date, registered capital, business scope |
| Round 2 | `"{Enterprise Full Name}" 新闻 最新动态` | Recent business developments, news events, development plans |
| Round 3 | `"{Enterprise Full Name}" 公众号 抖音 官网` | Enterprise official channels, brand presence |
| Round 4 | `"{Enterprise Name}" {Industry} 数字化 转型` | Industry trends, digital transformation needs |

Search strategy:
- Use different keyword combinations for each round to ensure coverage
- "Enterprise Full Name" refers to the name input by the user; if results are limited, try abbreviations or industry+region combinations
- Focus on: employee scale, business expansion, IT investment, bidding activities, supply chain relationships
- Maximum 2 searches per round (parallel within the same round), 4 rounds total, no more than 8 searches
- Identify: negative sentiment (legal disputes, business anomalies) and positive highlights (honors, industry standing)

### Step 2: Integrate Enterprise Information, Build Customer Profile

Consolidate search results into a structured profile:

**Required fields** (fill as much as possible, mark as "未获取到" if missing):
- Enterprise full name, abbreviation, industry, founding date, registered capital, employee scale
- Main business, business model (B2B/B2C/Mixed), industry position
- Registered address, office address (if different), branch offices

**Key analysis dimensions**:
- **Scale assessment**: Determine large/medium/small/micro based on registered capital, employee count, revenue
- **IT maturity estimation**: Infer from industry attributes and IT-related news found in search
- **Business growth trend**: Judge from recent news, hiring activity, expansion information
- **Communication needs signals**: Identify needs for remote work, multi-site collaboration, high internal communication volume

### Step 3: Intelligent Business Opportunity Recommendation

Read [references/telecom-products.md](references/telecom-products.md) for the complete product knowledge base, then match opportunities based on customer profile:

Matching logic:
1. Match industry solutions based on "industry attributes"
2. Match product tier (basic/standard/advanced) based on "scale characteristics"
3. Match specific products based on "business characteristics" (e.g., multi-site -> SD-WAN, manufacturing -> 5G+Industrial Internet)
4. Recommend advanced products based on "IT maturity" (e.g., low IT maturity -> start with basic communications+cloud; high maturity -> recommend AI+security)

Output requirements:
- Recommend 3-5 products/service solutions, sorted by priority
- Each recommendation must cite **specific information** about the enterprise as the reasoning basis. No generic statements.
- For enterprises with special industry characteristics or business models, prioritize strongly correlated solutions

### Step 4: Create Visit Plan

Based on customer profile and opportunity analysis, create a structured visit plan (6 modules):

1. **Visit objective setting**: Define outcome level (establish relationship / explore needs / advance proposal / close deal), based on information maturity
2. **Visit rhythm scheduling**: Plan phased visit rhythm (first visit -> follow-up -> proposal presentation), each phase's goals and specific actions
3. **Conversation topics and scripts sequence**: Design complete script chain from ice-breaking to advancement (ice-break -> need exploration -> product introduction -> deep recommendation -> next step)
4. **Pre-visit preparation checklist**: Materials to bring, industry info to review in advance, who to bring along, appointment tips
5. **Risk assessment and contingency**: Possible challenges (decision-maker unavailable / competitor present / no budget), competitor analysis, response strategies
6. **Follow-up plan**: What to do X days after visit, next visit timing and goals, customer tier classification

### Step 5: Generate Customized Communication Scripts

Read [references/speech-scripts.md](references/speech-scripts.md) for the script template library, then generate communication scripts based on the enterprise's actual situation and visit plan:

Generate content:
- **Ice-breaker script**: Must mention specific information about the enterprise (e.g., recent news, industry achievements), demonstrating "homework done"
- **Needs exploration scripts**: Design 3-5 targeted questions based on recommended product directions
- **Product pitch scripts**: Select top 2-3 priority products and generate customized pitch scripts
- **Transition and advancement scripts**: Transitional phrases between each stage
- **Objection response plans**: Anticipate likely objections based on industry characteristics and prepare responses
- Each script type provides both a **Business Formal** version and a **Friendly Natural** version

### Step 6: Output Complete Report in Conversation

Read [references/report-template.md](references/report-template.md) for the output template, and organize the report according to the template structure.

**Output sequentially in conversation** (no file generation):
1. **Summary**: Enterprise positioning (industry + scale + main business), core opportunities list (3-5 items), recommended entry point
2. **Full report**: Output all sections in template order

**Closing question**: After outputting the report, ask the user: "Do you need to export this report as a Word document? If so, reply 'yes' and I will generate a .docx file."
- If the user confirms, generate a Word file named `{Enterprise Name}走访准备报告.docx` using python-docx, saving to the current working directory
- If not needed, end the process

**Report content standards**:
- Report is presented from the account manager's first-person perspective
- Enterprise information includes source attribution
- Opportunity recommendations cite specific enterprise information; reasons are concrete, not generic
- Scripts demonstrate thoroughness with a "homework done" quality
- Insufficient information honestly marked as "Recommended to verify during visit"

## Important Notes

- This skill is designed for China Telecom enterprise account managers' daily visit preparation work
- Search results may be outdated or incomplete; remind the account manager to verify with latest information
- Opportunity recommendations are for reference only; actual solutions should be determined based on in-depth communication between the account manager and the customer
- In external materials, do NOT mention "selling overseas models" or "Claude/Gemini sales" -- use "premium model expansion capability" or "high-quality international link" instead
- Product recommendations focus on domestic products (Tianyi Cloud, Dedicated Line, V-Network, etc.); for the Xingchen AI Platform, overseas models are described as "premium model expansion capability" only

## Cross-Platform Adaptation

This skill was originally developed for the Xingchen Super Agent. To migrate to other agent platforms (Claude Code, Codex CLI, etc.), note the following core dependency replacements:

| Dependency | Level | Xingchen Super Agent Native | Cross-Platform Alternative |
|--------|---------|------------------|--------------|
| Web Search | **Core** | `baidu_search` (built-in) | MCP search server / Shell + Search API / Manual info provision |
| Word Generation | Non-core | `docx` skill | python-docx script / MCP document server / Markdown output |
| File Read | Core | Built-in | Built-in on all platforms, note path convention differences |
| Knowledge Base Ref | Core | `[references/xxx.md](references/xxx.md)` | Platforms not supporting file refs need to inline references/ content |

### Compatibility Quick Reference

| Platform | Adaptation Difficulty | Notes |
|------|---------|------|
| Claude Code | Low | Skill format compatible, only need to replace search and document generation tools |
| Codex CLI | Medium | No Skill system, need to inline knowledge base, inject via AGENTS.md |
| Cursor / Windsurf | Medium | Inject via .cursorrules, need MCP to supplement search capability |