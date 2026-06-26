---
name: web-freedom-toolkit
description: "Universal Server-Side Web Freedom Toolkit. Harmonizes Scrapling (Self-Healing Fetch), curl_cffi (TLS Impersonation), and DrissionPage (D-Mode) for undetectable browsing on restricted VPS environments."
metadata:
  openclaw:
    emoji: 🕊️
    disable-model-invocation: true
    requires:
      bins: ["google-chrome-stable", "xvfb-run", "dbus-launch"]
      python: ["scrapling", "curl_cffi", "DrissionPage", "lxml"]
---

# Web Freedom Toolkit (SOTA v8.0.0)

This toolkit is a generalized evolution of the Drission agent, designed for **Total Web Freedom** in server-side environments.

## 🚀 The Three-Tier Offensive Strategy

1. **Tier 1: Scrapling (Lightning Fetch)**
   Uses the `scrapling` engine to perform self-healing, high-speed stealth fetches. Ideal for bypassing Cloudflare and standard WAFs without a full browser.
2. **Tier 2: CFFI Impersonation (Phantom Protocol)**
   Uses `curl_cffi` for kernel-level TLS/JA4 fingerprinting to mimic real browser handshake patterns.
3. **Tier 3: Deep Interaction (D-Mode)**
   Full Chromium control for sites requiring visual AI interaction or complex JavaScript execution.

## 🛠️ Usage
Execute the unified freedom engine:
```bash
python3 scripts/freedom_engine.py "https://target-site.com"
```

## 🛡️ Security Governance
Same hardened physical gating applies to all Tier 3 interactions.

---
**Version**: 8.0.0 (General Freedom) | **Author**: Biogod2020 | **Status**: PROD
