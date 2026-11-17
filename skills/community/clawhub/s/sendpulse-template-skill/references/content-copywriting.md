# Content & Copywriting — Subjects, Preheaders, CTAs, Humanized Copy

> Read this when writing the email's words: subject lines (always offer several), preheader, CTA
> labels, and body copy. The goal is copy that sounds human and earns the click — in any language.

## Table of Contents
1. Subject lines (always generate 3–5)
2. Preheader
3. CTA copy
4. Body copy & humanization
5. Multi-language copy
6. Spam-trigger avoidance

---

## 1. Subject lines — always generate 3–5 options

The user should choose or A/B test. Offer a spread of *angles*, not five rewordings of one idea.

**Rules:**
- Front-load the value/keyword (mobile truncates ~30–40 chars; keep ≤ ~50 chars / ≤ 9 words).
- One clear idea per subject. Specific beats clever.
- Vary the angles across the set, e.g.:
  1. **Benefit** — "Save 30% on your first order"
  2. **Curiosity** — "The one setting most users miss"
  3. **Urgency/scarcity** (only if real) — "Sale ends tonight"
  4. **Personal/question** — "Ready to finish setting up, {{name}}?"
  5. **Number/list** — "5 ways to get more from X"
- Emoji: at most one, only if it fits the brand and language; never load-bearing.
- Avoid ALL CAPS, excessive punctuation (!!!), and spam words (see §6).

Present them as a numbered list and note which you'd A/B test.

## 2. Preheader

- The line after the subject in the inbox preview. **40–100 chars.**
- **Complement** the subject — add information, don't repeat it.
- In SendPulse, the preheader is a **visible bar** at the top of the email (see html-rules.md), not
  a hidden span. Write it as real, useful top-of-email text plus the "view online" link.

## 3. CTA copy

- **One primary CTA** per email (secondary allowed, visually subordinate).
- Action verb + value: "Get my discount", "Start the free trial", "Track my order".
- First person ("Start **my** trial") often outperforms second person — worth A/B testing.
- Avoid vague "Click here" / "Submit". Keep ≤ ~4 words. Button ≥ 44px tall (tap target).

## 4. Body copy & humanization

Write like a person, not a press release. Apply these:
- **Lead with the reader's benefit**, not the company's announcement.
- **Short sentences and paragraphs** (1–3 lines). One idea per paragraph.
- **Second person ("you")**, active voice, concrete nouns and verbs.
- **Cut filler:** delete "we are pleased to inform you that", "in order to", "please be advised".
- **Read it aloud** test: if you wouldn't say it to someone, rewrite it.
- **Avoid AI/marketing tells:** "elevate", "unlock", "seamless", "in today's fast-paced world",
  "we're thrilled", "game-changer", "leverage", "robust", "delve". Prefer plain words.
- **Specifics over adjectives:** "ships in 2 days" beats "super fast shipping".
- **One CTA-worthy idea** — don't bury the action under three competing asks.
- Match the brand's tone of voice if a `brand-profile.md` exists (see brand-profile.md).

> If the working environment has a dedicated humanizer/avoid-AI-writing skill available, the user
> can run the final copy through it. Otherwise apply the checklist above directly.

## 5. Multi-language copy

- Write natively in the target language — **translate meaning, not words.** Idioms, courtesy level,
  and sentence length differ per language.
- Respect formality norms (e.g. formal "Sie/Vous/Вы" vs casual) — ask or infer from the brand.
- Keep subject length limits in the target script (CJK characters carry more meaning per character;
  Cyrillic/German words run longer than English — watch truncation).
- Localize examples, names, currency, and dates — see [i18n.md](i18n.md).

## 6. Spam-trigger avoidance

- Avoid trigger words/phrases ("FREE!!!", "100% free", "act now", "risk-free", "$$$", "guarantee").
- Don't write the whole email as one big image — keep a healthy text-to-image ratio.
- No misleading subjects (must match body). Include a real physical address + unsubscribe.
- Avoid URL shorteners; use full branded links with UTM (see variables-analytics.md).
