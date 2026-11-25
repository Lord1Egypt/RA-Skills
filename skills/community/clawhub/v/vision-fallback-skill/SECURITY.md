# Security

## Overview

This document addresses security considerations for the vision-fallback skill,
including responses to automated audit findings (Snyk, Agent Trust Hub).

## Volcengine Ark endpoint (`ark.cn-beijing.volces.com`)

**Snyk flags this as a "suspicious download URL" / typosquat. This is a false positive.**

`ark.cn-beijing.volces.com` is the **official API endpoint** for Volcengine Ark
(火山方舟), ByteDance's cloud AI platform. The domain:

- `volces.com` is the registered domain of Volcengine (火山引擎), a major
  Chinese cloud provider and subsidiary of ByteDance.
- `ark.cn-beijing` is the Ark (model serving) service in the Beijing region.
- Documentation: https://www.volcengine.com/docs/82379
- The endpoint is only a default — users override it with `VISION_BASE_URL`.

**This is not a download URL.** No executable is fetched from this host. The
skill sends an authenticated POST request to a chat completions API, identical
in nature to calling `api.openai.com`.

## Security design

### JSON injection prevention (RCE mitigation)

**Previous design (vulnerable):** The payload was built by `jq gsub` string
substitution on a JSON template, then parsed with `fromjson`. User-supplied
text containing double quotes or control characters could break the JSON
structure and inject unauthorized keys.

**Current design (safe):** The payload is constructed natively with
`jq -n --arg`, which handles all JSON escaping internally. No string
substitution or template parsing occurs. This eliminates the injection surface
entirely.

### Prompt injection mitigation

Untrusted data (`ocr_text`, `failure_reason`, `primary_model_output`) is
wrapped in `<UNTRUSTED_INPUT>` boundary markers within the user message. The
system prompt explicitly instructs the model to treat content inside these tags
as data, not instructions.

### Credential handling

**Previous design (unsafe):** Dotenv files were sourced with `. "$f"`, which
executes their content as shell commands — a risk if the file is writable by
another process/user.

**Current design (safe):** Dotenv files are parsed with `grep` + `sed` to
extract `KEY=VALUE` lines. No execution occurs. Only the specific keys
(`VISION_API_KEY`, `ARK_API_KEY`, `OPENAI_API_KEY`) are extracted.

### Data exfiltration (inherent, accepted)

The skill's core function is sending images to a vision API for interpretation.
This is documented behavior, not a vulnerability. Users choose their provider
(`ark` or `openai` or any custom endpoint via `VISION_BASE_URL`) and provide
their own API key. No data is sent to any endpoint other than the configured
vision API.

### Command execution (inherent, accepted)

The skill uses standard system utilities (`curl`, `jq`, `base64`, `file`) to
process images and make network requests. These are necessary for the skill's
functionality and are clearly documented in the compatibility requirements.
