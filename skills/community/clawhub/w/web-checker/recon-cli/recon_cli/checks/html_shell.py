"""HTML shell check - static vs framework, forms, mailto, comments, 3rd-party."""
from __future__ import annotations

import re
from typing import List

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..http import get
from .base import Check

FRAMEWORK_SIGNALS = {
    "react": [r'\bReact\b', r'\b__REACT', r"id=\"root\"", r'id="app"'],
    "next.js": [r"__NEXT_DATA__", r"_next/static"],
    "vue": [r"vue\.(dev\.)?js", r"data-v-[0-9a-f]{8}"],
    "angular": [r"ng-version=", r"angular[\s./-]\d"],
    "svelte": [r"svelte-"],
    "nuxt": [r"__NUXT__", r"_nuxt/"],
    "vite": [r"/assets/index-[A-Za-z0-9_-]+\.js"],
}


class HtmlShellCheck(Check):
    name = "html_shell"
    description = "Detect framework, forms/mailto (data paths), comments, 3rd-party scripts"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        url = target if target.startswith("http") else f"https://{target}"
        ok, body = get(url, cfg, follow=True)
        if not ok:
            return CheckResult(self.name, "error", error=body[:400])

        size = len(body)
        findings.append(Finding(self.name, f"HTML shell {size:,} bytes", Severity.INFO))

        # framework detection
        detected = [k for k, pats in FRAMEWORK_SIGNALS.items()
                    if any(re.search(p, body, re.I) for p in pats)]
        if detected:
            evidence = ""
            idx = body.lower().find(detected[0])
            if idx >= 0:
                evidence = body[max(0, idx - 20): idx + 80]
            findings.append(Finding(self.name, "Likely stack: " + ", ".join(detected),
                                   Severity.INFO, evidence))
        else:
            findings.append(Finding(self.name, "No known framework signals (likely static HTML)", Severity.INFO))

        # data paths: forms + mailto + external form endpoints
        forms = re.findall(r'<form\b[^>]*>', body, re.I)
        if forms:
            for f in forms[:5]:
                findings.append(Finding(self.name, f"Form: {f}", Severity.LOW, f,
                                       "Confirm where form data is sent (3rd-party = data path)."))
        else:
            findings.append(Finding(self.name, "No <form> in shell", Severity.INFO))

        mailtos = re.findall(r'mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+', body, re.I)
        if mailtos:
            findings.append(Finding(self.name, "mailto: link(s) found", Severity.INFO,
                                   "; ".join(sorted(set(mailtos))[:5]),
                                   "Email address disclosed (informational)."))

        # 3rd-party scripts / iframes
        ext = set(re.findall(r'<script\b[^>]*\bsrc=["\'](https?://[^"\']+)', body, re.I))
        ext |= set(re.findall(r'<iframe\b[^>]*\bsrc=["\'](https?://[^"\']+)', body, re.I))
        if ext:
            for e in sorted(ext)[:8]:
                findings.append(Finding(self.name, f"3rd-party: {e}", Severity.LOW, e,
                                       "Supply-chain / exfil surface - confirm trust."))
        else:
            findings.append(Finding(self.name, "No external <script src> in shell", Severity.INFO))

        # comments
        comments = re.findall(r'<!--(?!\[).*?-->', body, re.S)
        if comments:
            for c in comments[:5]:
                findings.append(Finding(self.name, f"HTML comment: {c.strip()[:80]}",
                                       Severity.INFO, c.strip()[:200]))

        # robots / security.txt hints
        if "robots.txt" in body:
            findings.append(Finding(self.name, "robots.txt referenced", Severity.INFO))

        summary = f"shell {size:,}B; forms={len(forms)}; ext-scripts={len(ext)}"
        return CheckResult(self.name, "ok", findings, summary)
