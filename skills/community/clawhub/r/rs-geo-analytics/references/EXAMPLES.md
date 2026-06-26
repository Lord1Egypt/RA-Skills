# RS-Skill — Real Usage Examples

> Real-world scenarios with commands, outputs, and what to do next.
> All outputs from live testing (ROA-40, 2026-02-26) or validated mock data.

---

## Example 1: Monday Morning Brand Health Check

**Scenario:** You want a quick snapshot of your brand's AI visibility before the week starts.

**Command:**
```
node rankscale-skill.js
```

**Output (healthy brand):**
```
=======================================================
                 RANKSCALE GEO REPORT
             Brand: AcmeCorp | 2026-02-26
=======================================================
  GEO SCORE:      72 / 100   [+5 vs last week]
  CITATION RATE: 55.5%     [Industry avg: 45%]
  SENTIMENT:     Pos 61% | Neu 29% | Neg 10%
-------------------------------------------------------
  TOP AI SEARCH TERMS
  1. "best crm software"                  (500 mentions)
  2. "crm comparison"                     (300 mentions)
  3. "crm pricing"                        (200 mentions)
-------------------------------------------------------
  GEO INSIGHTS  [1 action]
  [INFO] Strong positive momentum detected.
  Action: Maintain current content cadence.
  Double down on formats producing citations.
  Consider expanding to adjacent topics.
-------------------------------------------------------
  Full report: https://rankscale.ai/dashboard/brands/acmecorp
=======================================================
```

**What this tells you:**
- Score 72/100, up +5 from last week → on a positive trajectory
- Citation rate (55.5%) is above industry average (45%) → good citation health
- Top term "best crm software" driving 500 mentions → your strongest query

**Next steps:**
- Visit the full dashboard for deep-dive
- Schedule `--engine-profile` to see which engines need attention

---

## Example 2: Identifying Your Weakest AI Engines

**Scenario:** You're planning a content sprint. You want to know which AI engines to optimize for.

**Command:**
```
node rankscale-skill.js --engine-profile
```

**Output (live API — ROA-40, 2026-02-26):**
```
-------------------------------------------------------
                ENGINE STRENGTH PROFILE
-------------------------------------------------------
  Engine       Visibility            Score
  Average      ──────────────────     69.3
-------------------------------------------------------
  mistral_larg ██████████████████████ 83.2 ✦
  deepseek_cha █████████████████████  79.5 ✦
  chatgpt_gui  ████████████████████   77.5 ✦
  perplexity_s ████████████████████   73.9
  google_ai_ov ███████████████████      73
  google_ai_mo ███████████████████    70.8
  google_gemin ██████████████████     66.2
  openai_gpt-5 ████████████████       60.1 ▼
  anthropic_cl ███████████████        57.7 ▼
  perplexity_g █████████████          50.7 ▼
-------------------------------------------------------
  ✦ Top-3 engines  ▼ Bottom-3 engines
```

**What this tells you:**
- Strong on Mistral (83.2), DeepSeek (79.5), ChatGPT (77.5)
- Weak on Perplexity Pro (50.7), Claude (57.7), GPT-5 preview (60.1)
- Average is 69.3 — Claude is 11.6 pts below average

**Next steps:**
- Create content that cites sources Claude tends to index (research papers, official docs)
- Build Perplexity-indexed citations (news sites, Stack Overflow, Wikipedia)
- Investigate why GPT-5 preview scores lower than ChatGPT standard

---

## Example 3: Content Calendar Planning with Gap Analysis

**Scenario:** You're building next quarter's content plan. You want to know what topics to target.

**Command:**
```
node rankscale-skill.js --gap-analysis
```

**Output (live test data):**
```
-------------------------------------------------------
                 CONTENT GAP ANALYSIS
-------------------------------------------------------
  ENGINE GAPS (vs avg 44.5):
  ▼ grok           score:   15  gap:-29.5
  ▼ gemini         score:   20  gap:-24.5

  LOW-VISIBILITY TERMS (<50%) — 3 found:
  email campaigns        ░                      5%
  sales pipeline         ░░░░                  18%
  marketing automation   ░░░░░░░░              42%

  RECOMMENDATIONS:
  1. Create content targeting top 3 gap terms:
     • "email campaigns"
     • "sales pipeline"
     • "marketing automation"
  2. Optimise for grok: score 15 vs avg 44.5
-------------------------------------------------------
```

**What this tells you:**
- "Email campaigns" at 5% → a near-complete blind spot, highest priority content topic
- "Sales pipeline" at 18% → strong opportunity, likely covered by competitors
- Grok score (15) is 29.5 pts below average → engine-specific strategy needed

**Next steps:**
- Assign a writer to produce 3 pieces on "email campaigns", "sales pipeline", "marketing automation"
- Research what Grok indexes — typically Twitter/X-native content, real-time data
- Re-run gap analysis in 2 weeks to measure impact

---

## Example 4: Reputation Check Before a Product Launch

**Scenario:** Your team is shipping a major update next week. You want to check current brand sentiment before the launch.

**Command:**
```
node rankscale-skill.js --reputation
```

**Output (brand with mixed sentiment):**
```
-------------------------------------------------------
              REPUTATION SCORE & SUMMARY
-------------------------------------------------------
  Score:  ██████████████████░░░░░░░░░░░░ 61/100
  Status: Good   Trend: ↑ improving

  Sentiment breakdown:
    Positive: 56.2%  Negative: 15.7%  Neutral: 28.1%

  Top positive signals:
    easy to use, great support, powerful

  Risk areas:
    expensive, slow

  Summary: Brand health is good (61/100) and improving.
           Monitor: expensive, slow.
-------------------------------------------------------
```

**What this tells you:**
- Score 61/100, trending upward → launch timing is good
- Negative signals "expensive" and "slow" → address in launch messaging
- "Great support" is a positive signal → lean into it in launch copy

**Next steps:**
- Adjust launch messaging to pre-empt "expensive" concerns (pricing transparency, ROI data)
- Prepare support team for volume spike (the "slow" signal may be support wait times)
- Re-run `--sentiment-alerts` post-launch to catch any narrative shift quickly

---

## Example 5: PR Campaign Targeting with Citation Intelligence

**Scenario:** You're planning a link-building and PR campaign. You want to know which publications to target and where competitors have an edge.

**Command:**
```
node rankscale-skill.js --citations full
```

**Output:**
```
🔗 Citation Intelligence
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top Sources:
  1. techcrunch.com      42 citations   🟢 High authority
  2. forbes.com          38 citations   🟢 High authority
  3. g2.com              21 citations   🟡 Mid authority

Gap vs Competitors:
  Competitor A leads +31 citations on Perplexity
  Competitor B leads +18 citations on Gemini

PR Targets:
  → wired.com (competitor coverage, not yours)
  → venturebeat.com (high Gemini indexing)

Citation↔Visibility Correlation:
  +1 TechCrunch citation ≈ +0.8 Perplexity visibility
  +1 Forbes citation     ≈ +0.5 ChatGPT visibility
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**What this tells you:**
- Competitors lead on Perplexity via 31 more citations → Perplexity is a key battleground
- Wired.com covers competitors but not you → direct outreach target
- VentureBeat has strong Gemini indexing → one article there = Gemini visibility boost

**Next steps:**
- Pitch Wired.com with a story angle competitors haven't covered
- Brief VentureBeat on your product launch (Gemini lift)
- Use TechCrunch/Forbes as anchor citations in new content (they correlate directly to visibility)

---

## Combining Commands: Weekly GEO Workflow

A recommended weekly workflow using RS-Skill:

```bash
# 1. Monday: Full overview
node rankscale-skill.js

# 2. Check engine-level shifts
node rankscale-skill.js --engine-movers

# 3. Sentiment pulse
node rankscale-skill.js --sentiment-alerts

# 4. Monthly: Content planning
node rankscale-skill.js --gap-analysis

# 5. Monthly: PR planning
node rankscale-skill.js --citations full
```

---

## Questions?

We are happy to support.

📧 `support@rankscale.ai`
🌐 [rankscale.ai](https://rankscale.ai)

Back to [SKILL.md](../SKILL.md) | Feature reference: [FEATURES.md](FEATURES.md) | Troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
