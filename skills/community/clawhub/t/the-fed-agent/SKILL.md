---
name: the-fed-agent
description: Macroeconomics and central bank policy analysis. Use when analyzing Fed decisions, Treasury yields, inflation data, monetary policy statements, and central bank actions. Triggered by news articles about interest rates, inflation, economic data, or monetary policy.
---

# The Fed Agent

Analyzes central bank policy decisions and macroeconomic data through integrated frameworks to assess policy stance, inflation outlook, and market implications.

## Usage

```
the-fed-agent <news_url>
```

The skill fetches the news URL and produces a structured analysis with four outputs.

## Workflow

### Step 1: Fetch and Parse News Content

Use `web_fetch` to extract article content from the provided URL.

### Step 2: Apply Analytical Frameworks

Analyze the macroeconomic situation using these integrated frameworks (stored in `references/`):

1. **Fed Policy Framework** — dual mandate balance (employment vs. inflation)
2. **Inflation Transmission** — oil/commodity passthrough to CPI/PCE
3. **Stagflationary Dynamics** — growth slowdown + inflation rise scenarios
4. **Central Bank Credibility** — forecast revision patterns, forward guidance
5. **Great Power Entrapment** — geopolitical conflict impact on policy path

### Step 3: Generate Structured Output

Produce analysis in this exact format:

```
## 1. Conclusion
[Clear thesis statement about central bank policy stance, inflation outlook, and policy bind. Include key decision metrics.]

## 2. Economic/Commodity Impact
| Factor | Current Status | Policy Implication |
|--------|---------------|-------------------|
| [Rate decision] | [Value] | [Implication for policy path] |
| [Inflation] | [Value] | [Implication for policy path] |
| [Growth] | [Value] | [Implication for policy path] |
| [Oil price] | [Value] | [Implication for policy path] |

## 3. Commodity Trading Odds
| Position | Recommendation | Rationale | Risk Factor |
|----------|---------------|-----------|-------------|
| [Asset 1] | [Overweight/Underweight/Neutral] | [1-sentence rationale] | [Key risk] |
| [Asset 2] | [Overweight/Underweight/Neutral] | [1-sentence rationale] | [Key risk] |
| [Asset 3] | [Overweight/Underweight/Neutral] | [1-sentence rationale] | [Key risk] |

**Key Risk:** [Single most important risk factor]

## 4. What's Next Can Be Happened?
**Ranked by likelihood:**

1. **[Scenario Name]** — X%  
   [2-3 sentence description including policy path and timeline]

2. **[Scenario Name]** — X%  
   [2-3 sentence description including policy path and timeline]

3. **[Scenario Name]** — X%  
   [2-3 sentence description including policy path and timeline]

4. **[Scenario Name]** — X%  
   [2-3 sentence description including policy path and timeline]

---

**Analysis anchors:** [Framework names: Fed policy framework, inflation transmission, stagflationary dynamics, etc.]
```

## Framework Reference

Read `references/frameworks.md` for detailed analytical models when complex macroeconomic situations require deeper assessment.

## Output Guidelines

- **Be decisive** — provide clear probabilities, not vague ranges
- **Anchor to frameworks** — cite specific indicators from the loaded models
- **Market focus** — always tie back to trading implications (bonds, currencies, commodities)
- **Scenario-ranked** — order policy scenarios by probability, not alphabetically
- **4-section format** — Conclusion, Economic/Commodity Impact, Commodity Trading Odds, What's Next Can Be Happened
