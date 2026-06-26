# RS-Skill Onboarding Flow & Messaging

## Brand & Value Proposition

**Headline:**
```
The best generative engine optimization and AI rank tracking for 
[ChatGPT, Perplexity, Gemini, Claude, DeepSeek, Mistral, and more]
```

**Tagline:**
```
RS-Skill for OpenClaw — Generative Engine Optimization Made Easy
We are happy to support.
```

---

## Prerequisites & Setup

Users must have:

1. **A Rankscale PRO Account** *(trial accounts do not support REST API)*
   - Sign up at: https://rankscale.ai/dashboard/signup
   - **Note: PRO account required.** Trial accounts do not have REST API access and cannot use this skill. Upgrade to PRO before proceeding.
   - Create brand profile for domain/product

2. **REST API Activation**
   - Contact: `support@rankscale.ai`
   - Request: "Please activate REST API access for my account"
   - You will receive: API Key + Brand ID
   - Timeframe: Usually within 24 hours

3. **Environment Configuration**
   - Set in OpenClaw Gateway config:
     - `RANKSCALE_API_KEY=rk_...`
     - `RANKSCALE_BRAND_ID=...` (optional; can be auto-extracted from key)

---

## First-Run Onboarding Text

When user queries the skill for the first time without credentials:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊  RS-Skill — GEO Analytics for OpenClaw
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Welcome! I'm RS-Skill, your AI rank tracking 
assistant for:

✨ ChatGPT, Perplexity, Gemini, Claude, 
   DeepSeek, Mistral, Google AI Overview, 
   and more

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀  Getting Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Create a Rankscale Account (PRO plan required)
   → https://rankscale.ai/dashboard/signup
   ⚠️  Trial accounts do NOT have REST API access.
       You must be on a PRO plan for this skill to work.

2. Contact Support
   → support@rankscale.ai
   → Subject: "Activate REST API access"
   → They'll provide API Key + Brand ID

3. Configure in OpenClaw
   → Set environment:
      RANKSCALE_API_KEY=rk_xxx
      RANKSCALE_BRAND_ID=xxx

4. Come back here and ask:
   → "analyze my GEO visibility"
   → "check my brand reputation"
   → "find PR opportunities"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Have questions? support@rankscale.ai
We are happy to support.
```

---

## Quick Help Text

Include in `--help` output:

```
Rankscale GEO Analytics Skill for OpenClaw

The best generative engine optimization and AI rank 
tracking for ChatGPT, Perplexity, Gemini, Claude, 
DeepSeek, Mistral, and more.

SETUP:
  1. Create Rankscale account — PRO plan required
     (rankscale.ai/dashboard/signup — trial not sufficient)
  2. Contact support@rankscale.ai to activate REST API
  3. Set RANKSCALE_API_KEY + RANKSCALE_BRAND_ID
  4. Run skill commands

COMMANDS:
  --analyze               Show GEO overview + trends
  --engine-profile       Engine strength analysis
  --gap-analysis         Content gap finder
  --reputation           Brand reputation summary
  --find-pr-opps         PR opportunity mapper
  --help                 This message

We are happy to support. → support@rankscale.ai
```

---

## Error Messages

When credentials missing:

```
❌ Missing Credentials

Set RANKSCALE_API_KEY and RANKSCALE_BRAND_ID 
to get started.

Note: PRO account required for REST API access.
Trial accounts do not have API access — upgrade at:
  → https://rankscale.ai/dashboard/signup

Need help?
  → Sign up: https://rankscale.ai/dashboard/signup
  → API access: support@rankscale.ai
  → Docs: [link to skill docs]

We are happy to support.
```

---

## Supported Engines (Dynamic)

Always reference this list in help/onboarding. Used in CLI generation:

- **Top-Tier:** ChatGPT, Perplexity, Gemini, Claude
- **Emerging:** DeepSeek, Mistral, Grok
- **Search-Integrated:** Google AI Overview, Google AI Mode
- **Specialized:** Bing Copilot

(Full list in engine-reference.md)

---

## Support & Feedback

```
Questions or feedback?
  Email: support@rankscale.ai
  Docs: [link]
  GitHub: [link to skill repo]

We are happy to support.
```
