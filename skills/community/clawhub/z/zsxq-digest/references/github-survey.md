# GitHub survey

## Purpose

Summarize nearby open-source approaches that are relevant to `zsxq-digest` so the project can borrow good ideas and avoid bad defaults.

## What was found

No obvious public OpenClaw-native skill for Knowledge Planet was found in the GitHub search pass.

Relevant adjacent projects did appear in four buckets:

1. **RSS / feed route implementations**
   - `DIYgod/RSSHub`
   - `samuelye/RSS-Hub`
2. **Backup / export crawlers**
   - `lxzmads/zsxqbackup`
   - `wbsabc/zsxq-spider`
   - `chanwoood/crawl-zsxq`
3. **Notification-style tool**
   - `tangxiaofeng7/zsxq_notice`
4. **SDK / auth guide**
   - `yiancode/zsxq-sdk`

## Useful findings

### 1. `zsxq_access_token` is the common auth anchor
Multiple repos and code search hits consistently use the cookie name `zsxq_access_token`.

Examples observed:
- RSSHub route config expects `ZSXQ_ACCESS_TOKEN`
- `zsxqbackup` and older spiders read the cookie/token directly
- `yiancode/zsxq-sdk` documents how to extract it from browser devtools

**Takeaway for this skill:**
- The local private session schema should explicitly center on `zsxq_access_token`.
- The README can safely teach users how to extract this cookie into a local gitignored file.

### 2. User-Agent consistency matters in API-oriented projects
Several crawler repos require both:
- `ZSXQ_ACCESS_TOKEN`
- `USER_AGENT`

This is a strong signal that direct HTTP/API routes may be sensitive to request headers and anti-bot checks.

**Takeaway for this skill:**
- Browser relay mode remains the safest primary path.
- Session-token mode should be marked advanced/experimental.
- If token mode is later expanded, document optional `user_agent` storage alongside the token.

### 3. Existing backup/export projects are heavier than needed
Examples like `zsxqbackup` rely on:
- chromedriver / selenium
- scrapy
- broader backup goals (topics, comments, files, images)

`zsxq_notice` uses:
- MySQL
- notification integration
- a more service-like deployment model

**Takeaway for this skill:**
- Do not copy their stack directly.
- Keep `zsxq-digest` focused on lightweight summarization, bounded state, and public-friendly distribution.

### 4. RSSHub proves a narrow route can work, but it is API-coupled
RSSHub's ZSXQ route uses a token and fetches group topics through API paths under `https://api.zsxq.com/v2`.
It is elegant, but tightly tied to the platform's API behavior.

**Takeaway for this skill:**
- Borrow the narrow-scope mentality: fetch only what is needed.
- Do not let MVP depend on private API stability.
- Keep fetch/token/API routes as optional and secondary.

## What not to copy

1. **Do not hardcode tokens or cookies in source files**
   Many public repos and code search hits expose real or example auth material inline. This is unacceptable for a public-friendly skill.

2. **Do not require heavy drivers or databases for MVP**
   Selenium/chromedriver, Scrapy, or MySQL are valid for full crawlers, but they hurt compatibility.

3. **Do not overpromise fetch fallback**
   None of the relevant references proved that plain HTML fetch is a reliable main path for a modern authenticated SPA.

## Final takeaway

The external ecosystem supports the updated direction:
- **Primary:** local private session using `zsxq_access_token`
- **Secondary:** browser relay for recovery and verification
- **Experimental only:** fetch/API fallback

The survey also reinforces two documentation tasks:
1. a beginner-friendly token extraction guide
2. a strong warning against high-frequency polling and public secret leakage
