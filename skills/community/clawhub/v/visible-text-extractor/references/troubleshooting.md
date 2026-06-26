# troubleshooting

## Purpose
Help users understand whether a bad result came from the source, the environment, or OCR quality.

## Common failure modes

### 1) WeChat article returns blocked / validation page
Symptoms:
- `blocked: true`
- body text looks like validation copy instead of the article

Meaning:
- the page is public in principle, but current environment access is limited

Recommended response:
- keep `blocked: true`
- try browser fallback
- try screenshot OCR only as a supplement, not as a fake replacement for the article
- tell the user when content quality is degraded

### 2) Body text is fine but images are noisy
Meaning:
- OCR quality is the bottleneck, not URL extraction

Recommended response:
- keep正文 as the primary truth source
- absorb only high-value image facts into the final deliverable
- do not paste raw noisy OCR into the main body

### 3) Page is JS-heavy and plain HTTP is incomplete
Meaning:
- the page likely requires browser rendering

Recommended response:
- enable browser fallback
- if browser tooling is unavailable, say so clearly

### 4) Local screenshots are low quality
Meaning:
- OCR may miss text or hallucinate fragments

Recommended response:
- mark uncertain areas explicitly
- keep low-confidence fragments separate from the main clean output

## Quality rule
If the source is only partially readable, prefer:
- accurate partial result + clear uncertainty
instead of
- seemingly complete result polluted by garbage
