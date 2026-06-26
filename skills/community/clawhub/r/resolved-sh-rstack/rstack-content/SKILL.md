---
name: rstack-content
preamble-tier: 2
version: 1.0.0
description: |
  Plans and publishes monetized content on resolved.sh: blog post series, structured
  courses with modules, and paywalled page sections. Interviews the operator to determine
  the best content strategy for their specific agent or tool, then generates ready-to-run
  PUT commands for each piece. Covers free vs. paid split, pricing per post vs. bundle,
  and paywall marker placement. Use when asked to "publish a blog post", "create a course",
  "add a paywall", "sell my knowledge", "add content to my page", or after rstack-audit
  reports no content published.
allowed-tools:
  - Bash
  - AskUserQuestion
metadata:
  env:
    - name: RESOLVED_SH_API_KEY
      description: Your resolved.sh API key (aa_live_...)
      required: true
    - name: RESOLVED_SH_RESOURCE_ID
      description: Your resource UUID
      required: true
    - name: RESOLVED_SH_SUBDOMAIN
      description: Your subdomain slug
      required: true
---

# rstack-content

Turn what you know into revenue. resolved.sh supports three content monetization modes:
blog post series (pay per post), structured courses (pay per module or bundle), and
paywalled page sections (gate part of your main page). This skill finds the right mix
for your specific use case and generates every command needed to publish.

---

## Preamble (run first)

```bash
echo "API key set: $([ -n "$RESOLVED_SH_API_KEY" ] && echo yes || echo NO — required)"
echo "Resource ID: $RESOLVED_SH_RESOURCE_ID"
echo "Subdomain:   $RESOLVED_SH_SUBDOMAIN"
```

Fetch current content state:

```bash
# Existing posts
curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/posts" \
  -H "Accept: application/json" \
  -o /tmp/rstack_posts.json 2>/dev/null

# Existing courses
curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/courses" \
  -H "Accept: application/json" \
  -o /tmp/rstack_courses.json 2>/dev/null

# Current page content (check for paywall marker)
curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh?format=json" \
  -o /tmp/rstack_page.json 2>/dev/null

python3 -c "
import json

posts = json.load(open('/tmp/rstack_posts.json')).get('posts', []) if open('/tmp/rstack_posts.json').read().strip() else []
courses = json.load(open('/tmp/rstack_courses.json')).get('courses', []) if open('/tmp/rstack_courses.json').read().strip() else []
page = json.load(open('/tmp/rstack_page.json'))
md = page.get('md_content') or ''

print(f'Published posts:   {len([p for p in posts if p.get(\"price_usdc\", 0) == 0])} free, {len([p for p in posts if (p.get(\"price_usdc\") or 0) > 0])} paid')
print(f'Published courses: {len(courses)}')
has_paywall = '<!-- paywall' in md
print('Page paywall:     ', 'yes' if has_paywall else 'no')
print(f'md_content length: {len(md)} chars')
" 2>/dev/null || echo "(Could not parse content state)"
```

Show this summary. If the operator already has content, ask: "I can see you have {summary}. Would you like to (A) add more content, (B) improve existing content, or (C) set up a new content type you haven't tried yet?"

---

## Phase 1 — Choose a content strategy

AskUserQuestion: "What kind of content do you want to create? Choose what fits best:

**(A) Blog post series** — A sequence of posts your audience reads over time. Good for: weekly insights, release notes, tutorials, analysis reports, anything episodic. Each post has its own price (or is free).

**(B) Course with modules** — Structured educational content with an ordered progression. Good for: how-to guides, onboarding sequences, technical tutorials, anything with a clear beginning → end arc. Buyers can purchase individual modules or the full bundle at a discount.

**(C) Paywalled page section** — Gate part of your main page. Everything above the marker is free; everything below is paid. Good for: teaser + deep-dive format, a free intro + premium methodology, public overview + private API details.

**(D) Ask inbox** — A paid Q&A inbox. Buyers pay per question via x402 USDC and you receive an email with their question and optional attachment. Good for: consultants, domain experts, or any operator who wants async paid advisory without building a support system.

**(E) Multiple** — tell me which combination and we'll do them in order."

---

## Phase 2A — Blog post series (if A or D includes posts)

**Q1:** "What's the series about? One sentence — the topic and why someone would pay to read it."

**Q2:** "Who is the reader? (A) Developers/builders, (B) Autonomous agents consuming the content programmatically, (C) Both, (D) Other"

**Q3:** "How many posts are you launching with? Give me titles for 1–5 posts to start. One title per line."

**Q4:** "What's your pricing model?
(A) All free — build audience first
(B) First post free, rest paid (give the price per post in USDC)
(C) All paid (give the price per post in USDC)
(D) Mixed — tell me which posts are free"

**Q5:** "For each post that's paid: do you have the content now, or should I generate a placeholder structure you can fill in?"

For each post, generate the PUT command:

```bash
# Post: "{title}"
curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/posts/{slug}" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "title": "{title}",
  "md_content": "{content or placeholder structure}",
  "price_usdc": {0 for free, or price},
  "published_at": null
}
EOF
```

**Slug generation rule:** lowercase, spaces → hyphens, remove special chars. Example: "How to Query DeFi Data" → `how-to-query-defi-data`

**Note on `published_at`:**
- Omit `published_at` (or set to current ISO datetime) → publishes immediately
- Set to a future ISO datetime → schedules for that time
- Set explicitly to `null` → saves as draft (not public)

For placeholder content, use this structure:

```markdown
# {title}

{2-sentence hook — what the reader will learn and why it matters now}

## {Section 1 title}

{Placeholder: write 2–3 paragraphs here}

## {Section 2 title}

{Placeholder: write 2–3 paragraphs here}

## {Section 3 title}

{Placeholder: write 2–3 paragraphs here}

---

*Published on [{subdomain}.resolved.sh]({subdomain}.resolved.sh)*
```

Generate all PUT commands in sequence. Show them together so the operator can run them in order.

After generating commands: "Posts at `GET https://{subdomain}.resolved.sh/posts`. Buyers pay per post via x402 USDC on Base and receive a 30-day access token for re-reads."

---

## Phase 2B — Course with modules (if B or D includes a course)

**Q1:** "What is this course about? One sentence — the transformation a student gets from start to finish."

**Q2:** "What are the modules, in order? Give me 3–8 module titles. Each module should be a concrete step in the progression."

**Q3:** "Pricing strategy — choose one:
(A) All modules free (the course is a marketing asset / onboarding guide)
(B) First module free, rest paid — price per module in USDC?
(C) All paid per module — price per module in USDC?
(D) Bundle discount — what's the per-module price? What's the bundle price (for all modules at once)?

Bundle tip: set bundle_price_usdc to ~70% of (module count × per-module price). Buyers who want everything pay less; buyers who want one module pay per module. Both are valid purchase paths."

**Q4:** "Is there a course description beyond the title? 1–2 sentences for the course overview page."

**Step 1 — Register the course:**

```bash
COURSE_SLUG="{slug-from-title}"  # e.g., "defi-data-mastery"

curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/courses/$COURSE_SLUG" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "title": "{course title}",
  "description": "{course description from Q4}",
  "bundle_price_usdc": {bundle price or null if no bundle pricing}
}
EOF
```

**Step 2 — Register each module (one PUT per module):**

```bash
# Module {N}: "{module title}"
MODULE_SLUG="{module-slug}"  # e.g., "01-setting-up-your-wallet"

curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/courses/$COURSE_SLUG/modules/$MODULE_SLUG" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "title": "{module title}",
  "md_content": "{content or placeholder}",
  "price_usdc": {0 for free, or price — null also means free},
  "order_index": {N starting from 0}
}
EOF
```

Generate all module commands in order. Number the slugs for clarity: `01-intro`, `02-setup`, `03-first-query`, etc.

After generating commands: "Course at `GET https://{subdomain}.resolved.sh/courses/{course-slug}`. Modules unlock via x402 payment (per-module) or bundle purchase (all at once). Bundle buyers also get access to any modules added later — a strong reason to offer bundle pricing."

---

## Phase 2C — Paywalled page section (if C or D includes paywall)

**Q1:** "What's the free part of your page — what do you want everyone to see?"

**Q2:** "What's the paid part — what's behind the paywall? Describe it in one sentence."

**Q3:** "What should the paywall price be in USDC?
Guidance:
- `$0.50–$2.00` — a piece of useful context (API details, private docs, config reference)
- `$2.00–$10.00` — a substantial methodology, proprietary process, or research findings
- `$10.00+` — a high-value resource that would take real time to produce independently"

**Q4:** "Do you have the paid content ready to add, or should I create a placeholder structure?"

**Paywall marker format — exact syntax required:**

```
<!-- paywall $X.00 -->
```

The parser is strict: dollar sign required, two decimal places required. Examples:
- `<!-- paywall $2.00 -->` ✓
- `<!-- paywall $0.50 -->` ✓
- `<!-- paywall $10.00 -->` ✓
- `<!-- paywall 2 -->` ✗ (missing $ and decimals)

**Generate the updated md_content:**

Fetch the current content, then restructure it with the paywall marker in the right place:

```bash
curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh?format=json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('md_content') or '')"
```

Place the free content above the marker and the paid content below it. The paid content should be substantial enough to justify the price — if the operator says "placeholder", generate a concrete structure they can fill in.

**Generate the PUT command:**

```bash
curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "md_content": "{full content with paywall marker at the right position}"
}
EOF
```

After applying: "Visitors see the free section at `https://{subdomain}.resolved.sh`. The locked section shows a paywall prompt. Buyers unlock via x402 USDC on Base and receive a `?section_token=<jwt>` link for re-access."

---

## Phase 2D — Ask inbox (if D or E includes ask inbox)

**Q1:** "What email address should buyer questions be sent to? This is private — it's never shown to buyers."

**Q2:** "What's your price per question in USDC? Minimum $0.50.
Guidance:
- `$1–$5` — general questions, short answers, quick lookups
- `$5–$20` — expert advice, research, detailed explanations
- `$20–$50` — specialized consulting, code review, strategy questions
- `$50+` — high-stakes advisory, rare domain expertise"

Generate the configuration command:

```bash
curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/ask" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ask_email": "{email from Q1}", "ask_price_usdc": {price from Q2}}'
```

After applying, show the buyer-facing endpoint and usage:

```
  Buyers call:  POST https://{subdomain}.resolved.sh/ask
  Format:       multipart/form-data
  Fields:
    question    (required) — the question text
    email       (required) — buyer's reply-to email
    attachment  (optional) — any file type, max 10 MB
  Payment:      x402 USDC on Base (PAYMENT-SIGNATURE header)
```

Note: To read the current configuration at any time: `GET https://resolved.sh/listing/{resource_id}/ask` (requires API key). Returns `{ask_email, ask_price_usdc}` or 404 if not configured.

---

## Phase 3 — Pricing summary

After all commands are generated, produce a summary of the revenue streams now configured:

```
══════════════════════════════════════════════
  rstack content: {subdomain}.resolved.sh
══════════════════════════════════════════════
  {if posts:}
  Blog posts      {N} posts at {price range}
  URL:            https://{subdomain}.resolved.sh/posts

  {if course:}
  Course          "{title}" — {module_count} modules
  Per module:     ${price_usdc} USDC
  Bundle:         ${bundle_price_usdc} USDC (all modules)
  URL:            https://{subdomain}.resolved.sh/courses/{slug}

  {if paywall:}
  Page paywall    ${price_usdc} USDC to unlock
  URL:            https://{subdomain}.resolved.sh

  {if ask inbox:}
  Ask inbox       ${ask_price_usdc} USDC/question → {ask_email}
  URL:            POST https://{subdomain}.resolved.sh/ask

  All purchases:  x402 USDC on Base · 10% protocol fee
  Your cut:       90% swept daily to your payout wallet

  Contact form is off by default. Enable with:
    PUT https://resolved.sh/listing/{resource_id} → {"contact_form_enabled": true}
══════════════════════════════════════════════
```

If no payout wallet is registered, add: "⚠ No payout wallet set. Register one at `POST https://resolved.sh/account/payout-address` to receive earnings. Earnings accumulate until a wallet is registered."

---

## Completion Status

**DONE** — Commands generated and/or run. Close with: "Run `/rstack-audit` to see your updated Content score, or `/rstack-services` if you also want to sell per-call API access."

**DONE_WITH_CONCERNS** — If the operator chose placeholder content: "Your posts/modules are live but need real content to convert. Fill in the placeholders and re-run the PUT commands with the final text. Draft tip: set `published_at: null` to save as draft until the content is ready."

**BLOCKED** — If env vars are missing, or the registration is not active. Free registrations support content publishing — if they're on the free tier, they can still use this skill.
