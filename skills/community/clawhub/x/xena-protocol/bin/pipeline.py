"""Three-stage detection pipeline orchestrator.

Consumed by the OpenClaw skill: called once per incoming email, returns a
JSON-serializable dict that tells the agent whether to alert/report and
whether a Stage-3 LLM classification is still needed.

Flow per email:

  1. Short-circuits: duplicate message-id? trusted sender? cached verdict?
  2. Stage 1 gates (deterministic, free): auth failure, display-name spoof,
     registry hit. Output is `gate_score` (0 or 75-95).
  3. Stage 2 heuristics (if no gate >= 90): URL red-flag score + Bayes score.
  4. Decide `needs_llm`:
     - `gate_score >= 90` → still send to LLM for category+reasoning only
     - `url_score < 20 AND bayes_score < 20 AND gate_score == 0` → safe, skip LLM
     - else → LLM classifies
  5. `combine_final(pre, llm_score, llm_category)` runs after LLM returns.
     Two branches:

     - `llm_category == "safe"`: LLM's confidence is its confidence IN its
       safe verdict, NOT a threat probability. Drop the LLM term entirely:
            confidence = max(gate_score, 0.15*url + 0.25*bayes)
       Hard gates still win (crypto truth > LLM opinion).

     - `llm_category != "safe"`:
            blended = 0.15*url + 0.25*bayes + 0.60*llm
            has_deterministic_signal = gate > 0 OR bayes >= 70
            llm_trust = llm if (llm >= 80 AND has_deterministic_signal) else 0
            confidence = max(gate, llm_trust, blended)

       The deterministic-signal requirement on llm_trust prevents the LLM
       alone from auto-reporting legit transactional emails (Google
       security alerts, bank/exchange notifications) that the LLM
       sometimes misclassifies as phishing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from bin.bayes_classify import classify, load_model
from bin.cache import Cache
from bin.check_auth import parse_authentication_results
from bin.parse_email import parse_eml
from bin.registry_client import RegistryClient, hash_identifier
from bin.url_features import score_urls

REPORT_THRESHOLD = 70
ALERT_THRESHOLD = 50
SAFE_LLM_SKIP_BOTH_BELOW = 20
GATE_SHORT_CIRCUIT = 90
DOMAIN_HIT_THRESHOLD = 5

# Stage-1 gate: a loud Bayes signal (typically strong phish tokens like
# "inheritance wire invoice urgent bitcoin") is enough on its own, even
# when auth passes and there are no URLs (classic BEC / Nigerian Prince
# pattern).
STRONG_BAYES_GATE_THRESHOLD = 85
STRONG_BAYES_GATE_SCORE = 80

# combine_final weights (must sum to 1.0)
W_URL = 0.15
W_BAYES = 0.25
W_LLM = 0.60

# LLM-trust floor: the LLM's threat confidence becomes the decision by itself
# IF it's at least this confident AND there is corroborating deterministic
# signal. Without the corroboration check, the LLM alone would auto-report
# any transactional email it happened to mis-classify as phishing.
LLM_TRUST_THRESHOLD = 80
# LLM-alone reports need STRONG corroboration now (was 70). Newsletters with
# moderately phish-leaning vocab were scoring bayes 70-80 and tripping
# auto-report when combined with an over-confident LLM.
LLM_TRUST_REQUIRES_BAYES = STRONG_BAYES_GATE_THRESHOLD   # 85

# Only these Stage-1 gates carry enough evidence to override an LLM
# "safe" verdict. Auth-fail (95) and registry identity hit (90) are
# cryptographic / network-corroborated. The strong-Bayes gate (80) is
# heuristic and can misfire on newsletters — LLM safe beats it.
HARD_GATE_FLOOR = 90


@dataclass
class Pipeline:
    model_path: Path
    brand_domains_path: Path
    registry: RegistryClient | None = None
    cache: Cache | None = None

    def __post_init__(self) -> None:
        self._model = load_model(self.model_path)
        self._brands = json.loads(Path(self.brand_domains_path).read_text())

    def process(self, raw_mime: bytes) -> dict:
        email = parse_eml(raw_mime)
        sender = email.from_address
        mid = email.message_id

        auth = parse_authentication_results(email.authentication_results)

        # Verified-legit shortcut: display-name brand matches the sender's own
        # domain AND all three auth methods pass = the real brand sent this.
        # Short-circuit to safe BEFORE any other gates / heuristics fire.
        if self._is_verified_legit_sender(email, auth):
            return _verified_response(email, reason="verified_brand_sender")

        # Stage 1 — hard gates
        gate_score, gate_reasons = self._stage1_gates(email, auth)

        # Stage 2 — heuristic features (always compute, cheap; skip LLM later if low)
        url_info = score_urls(email.urls)
        url_score = url_info["score"]
        bayes_prob, bayes_top = classify(
            f"{email.subject}\n{email.body_plain}", self._model
        )
        bayes_score = int(round(bayes_prob * 100))

        # Strong-Bayes gate (promoted back to Stage 1 conceptually).
        # Pure social engineering like Quanta BEC / Nigerian Prince has
        # clean auth and no URLs; the Bayes model is the only deterministic
        # signal and deserves to gate if it's loud enough.
        if bayes_score >= STRONG_BAYES_GATE_THRESHOLD:
            gate_reasons.append("strong_bayes")
            gate_score = max(gate_score, STRONG_BAYES_GATE_SCORE)

        # Decide LLM need
        needs_llm = True
        if (
            gate_score == 0
            and url_score < SAFE_LLM_SKIP_BOTH_BELOW
            and bayes_score < SAFE_LLM_SKIP_BOTH_BELOW
        ):
            needs_llm = False

        # Pre-LLM best guess
        if gate_score >= GATE_SHORT_CIRCUIT:
            verdict = "spoof"
        elif not needs_llm:
            verdict = "safe"
        else:
            verdict = "ambiguous"

        # Same formula shape as combine_final but without the LLM contribution,
        # so the agent can cite a consistent pre-LLM number.
        pre_llm_score = max(
            gate_score,
            int(round(W_URL * url_score + W_BAYES * bayes_score)),
        )

        return {
            "message_id": mid,
            "from_address": sender,
            "from_display": email.from_display,
            "from_domain": email.from_domain,
            "subject": email.subject,
            "urls": email.urls,
            "short_circuit": None,
            "gate_score": gate_score,
            "gate_reasons": gate_reasons,
            "url_score": url_score,
            "url_flags": url_info["per_url_flags"],
            "bayes_score": bayes_score,
            "bayes_top_tokens": [(t, round(p, 3)) for t, p in bayes_top],
            "pre_llm_score": pre_llm_score,
            "needs_llm": needs_llm,
            "verdict": verdict,
        }

    def _stage1_gates(self, email, auth) -> tuple[int, list[str]]:
        reasons: list[str] = []
        score = 0

        # Gate 1.1 — all three auth methods fail
        if auth.all_fail:
            reasons.append("auth_all_fail")
            score = max(score, 95)

        # Gate 1.2 — display-name brand vs sender-domain mismatch.
        # Only inspect the DISPLAY NAME for brand tokens (subject matching
        # caused false positives on newsletters that mentioned brands).
        # Legit brand subdomains are recognized via suffix match against
        # the brand's declared legit domains.
        brand = self._detect_brand(email.from_display)
        if brand and email.from_domain:
            legit = {d.lower() for d in self._brands.get(brand, [])}
            if not _domain_matches_any(email.from_domain, legit):
                reasons.append("display_name_spoof")
                score = max(score, 80)

        # Gate 1.3 + 1.4 — registry hits
        if self.registry is not None:
            try:
                h = hash_identifier(email.from_address)
                exists, count = self.registry.is_reported(h)
                if exists and count > 0:
                    reasons.append("registry_identity_hit")
                    score = max(score, 90)
            except Exception:
                pass

            try:
                dom_count = self.registry.domain_report_count(email.from_domain)
                if dom_count > DOMAIN_HIT_THRESHOLD:
                    reasons.append("registry_domain_hit")
                    score = max(score, 75)
            except Exception:
                pass

        return score, reasons

    def _detect_brand(self, display: str) -> str | None:
        if not display:
            return None
        needle = display.lower()
        for brand in self._brands:
            if brand in needle:
                return brand
        return None

    def _is_verified_legit_sender(self, email, auth) -> bool:
        """True when the sender passes BOTH of these gates:

        1. All three auth methods (SPF, DKIM, DMARC) pass.
        2. EITHER:
             a) Display-name brand is in our curated allowlist AND
                from_domain exact-matches or is a subdomain of that brand's
                declared legit domains, OR
             b) A significant word (>=4 chars) from the display name
                appears in from_domain — a self-consistent identity claim.
                Catches legitimate transactional senders outside the
                curated allowlist (Subito, IDA, Juno, Luma, TLDR, etc.).

        A phishing spoof typically uses a domain that does NOT contain the
        brand word it's impersonating, so (b) is a real trust signal.
        """
        if not (auth.spf == "pass" and auth.dkim == "pass" and auth.dmarc == "pass"):
            return False
        from_domain = (email.from_domain or "").lower()
        if not from_domain:
            return False

        # (a) curated brand match
        brand = self._detect_brand(email.from_display)
        if brand:
            legit = {d.lower() for d in self._brands.get(brand, [])}
            if _domain_matches_any(from_domain, legit):
                return True

        # (b) display-domain alignment: any significant word of the display
        # name appears inside from_domain.
        if _display_domain_aligned(email.from_display, from_domain):
            return True

        return False


# Words commonly present in display names that don't identify the sender.
# Used to filter display-domain alignment — "Support Team" against a random
# domain shouldn't count as aligned.
_DISPLAY_NOISE = frozenset({
    "the", "team", "support", "help", "info", "service", "services", "admin",
    "noreply", "no-reply", "notifications", "notification", "alerts", "alert",
    "newsletter", "news", "mail", "email", "staff", "inc", "llc", "ltd",
    "update", "updates", "account", "accounts", "billing", "customer",
    "group", "company", "customers", "welcome", "contact", "community",
})


def _word_matches_label(word: str, label: str) -> bool:
    """Match `word` against a single dot-separated domain `label`.

    - exact label == word                          → match
    - label starts with word and next char is alnum → match (brand + suffix
      compound like "tldrnewsletter" or "yostudios")
    - label starts with word and next char is '-' or other separator → NO
      (attacker compounds like "paypal-verify", "not-paypal")
    """
    if label == word:
        return True
    if not label.startswith(word):
        return False
    next_char = label[len(word)]
    return next_char.isalnum()


def _display_domain_aligned(display: str, from_domain: str) -> bool:
    """True if any significant display-name word matches a label of from_domain.

    Three rules, stacked from most to least strict (3-char bar relaxed only
    for exact-label matches):

    - Exact label match for 3+ char words (e.g. "IDA" == label "ida").
    - Prefix/compound match for 4+ char words via `_word_matches_label`.
    - Compound of all display words (2+) matching a label.

    - "Subito" + "email.subito.it"             → True
    - "YO Studios" + "e.yostudios.com"         → True  (compound "yostudios")
    - "TLDR" + "tldrnewsletter.com"            → True  (prefix, next alnum)
    - "IDA" + "nyt.ida.dk"                     → True  (exact label)
    - "PayPal" + "not-paypal.com"              → False
    - "PayPal" + "paypa1-secure.ru"            → False
    - "Quanta" + "quanta-computer-inc.xyz"     → False (label; next char '-')
    - "Support Team" + anything                → False (both in noise list)
    """
    if not display or not from_domain:
        return False
    import re
    all_words = [w.lower() for w in re.findall(r"[A-Za-z]+", display)]
    all_words = [w for w in all_words if w not in _DISPLAY_NOISE]
    if not all_words:
        return False

    labels = from_domain.lower().split(".")

    # Exact label match — relaxed to 3+ chars (must equal a whole label).
    if any(w in labels for w in all_words if len(w) >= 3):
        return True

    # Prefix/compound match — 4+ chars.
    long_words = [w for w in all_words if len(w) >= 4]
    for word in long_words:
        for label in labels:
            if _word_matches_label(word, label):
                return True

    if len(all_words) >= 2:
        compound = "".join(all_words)
        if len(compound) >= 6:
            for label in labels:
                if _word_matches_label(compound, label):
                    return True
    return False


def _domain_matches_any(domain: str, candidates: set[str]) -> bool:
    """Exact match OR strict subdomain suffix match against any candidate.

    `accounts.google.com` matches `google.com` (subdomain).
    `googleusercontent.com` does NOT match `google.com` (different registered name).
    `google.com.evil.ru` does NOT match `google.com` (suffix but not domain).
    """
    domain = domain.lower()
    for cand in candidates:
        cand = cand.lower()
        if domain == cand or domain.endswith("." + cand):
            return True
    return False


def _verified_response(email, *, reason: str) -> dict:
    """Short-circuit output for verified-legit senders — bypasses all scoring."""
    return {
        "message_id": email.message_id,
        "from_address": email.from_address,
        "from_display": email.from_display,
        "from_domain": email.from_domain,
        "subject": email.subject,
        "urls": email.urls,
        "short_circuit": reason,
        "verdict": "safe",
        "gate_score": 0,
        "gate_reasons": [],
        "url_score": 0,
        "url_flags": [],
        "bayes_score": 0,
        "bayes_top_tokens": [],
        "pre_llm_score": 0,
        "needs_llm": False,
        "confidence": 0,
        "should_alert": False,
        "should_report": False,
    }


def combine_final(pre: dict, *, llm_score: int, llm_category: str) -> dict:
    url = pre.get("url_score", 0)
    bayes = pre.get("bayes_score", 0)
    gate = pre.get("gate_score", 0)

    if llm_category == "safe":
        # LLM is context-aware; it reads the body. If it says safe, trust it
        # over heuristic-only gates (strong_bayes fires on newsletters that
        # happen to use phish-leaning vocabulary: "verify", "password",
        # "account", "urgent"). Only cryptographic / network-corroborated
        # gates — auth-fail (95) and registry identity hit (90) — override.
        if gate >= HARD_GATE_FLOOR:
            confidence = gate
        else:
            confidence = 0
        llm_trust = 0
    else:
        blended = int(round(W_URL * url + W_BAYES * bayes + W_LLM * llm_score))
        has_deterministic_signal = gate > 0 or bayes >= LLM_TRUST_REQUIRES_BAYES
        llm_trust = (
            llm_score
            if llm_score >= LLM_TRUST_THRESHOLD and has_deterministic_signal
            else 0
        )
        confidence = max(gate, llm_trust, blended)
        # When there's no deterministic corroboration, do not let the LLM
        # blend alone carry us past the report threshold. Alert, don't
        # auto-report. This stops LLM-over-confident classifications of
        # legit transactional mail (Subito, IDA, Substack) from reporting.
        if not has_deterministic_signal and confidence >= REPORT_THRESHOLD:
            confidence = REPORT_THRESHOLD - 1

    return {
        **pre,
        "llm_score": llm_score,
        "confidence": confidence,
        "category": llm_category,
        "should_report": confidence >= REPORT_THRESHOLD,
        "should_alert": confidence >= ALERT_THRESHOLD,
    }


def _short_circuit(
    email, reason: str, verdict: str | None, confidence: int | None = None
) -> dict:
    return {
        "message_id": email.message_id,
        "from_address": email.from_address,
        "from_display": email.from_display,
        "from_domain": email.from_domain,
        "subject": email.subject,
        "urls": email.urls,
        "short_circuit": reason,
        "verdict": verdict or "safe",
        "confidence": confidence,
        "needs_llm": False,
    }


# ----- CLI -----
def _cli() -> None:
    """`python -m bin.pipeline --poll` entry point used by HEARTBEAT.md.

    Loads skill config + deployed contract + bayes model, fetches unread
    Gmail via gog, runs the pipeline on each, prints a JSON array, and
    marks each message read.
    """
    import argparse
    import os

    from bin.cache import Cache
    from bin.gog_client import GogClient
    from bin.registry_client import RegistryClient

    parser = argparse.ArgumentParser()
    parser.add_argument("--poll", action="store_true", help="Poll inbox + run pipeline")
    parser.add_argument("--max", type=int, default=20, help="Max messages per poll")
    parser.add_argument(
        "--query",
        default="in:inbox",
        help='Gmail search query (default: "in:inbox" — most recent N, no dedup)',
    )
    parser.add_argument(
        "--combine",
        help="Combine pre-LLM JSON with LLM score/category (takes JSON on stdin)",
    )
    parser.add_argument("--llm-score", type=int)
    parser.add_argument("--llm-category", type=str)
    args = parser.parse_args()

    # --combine mode: read pre JSON from file, merge in LLM output, print final
    if args.combine:
        pre = json.loads(Path(args.combine).read_text())
        final = combine_final(pre, llm_score=args.llm_score, llm_category=args.llm_category)
        print(json.dumps(final))
        return

    if not args.poll:
        parser.print_help()
        return

    cfg_path = Path.home() / ".openclaw" / "phishing-detection" / "config.json"
    if not cfg_path.exists():
        print(json.dumps({"error": "setup_required", "path": str(cfg_path)}))
        raise SystemExit(1)
    cfg = json.loads(cfg_path.read_text())

    account = cfg.get("gmail_account")
    if not account:
        print(json.dumps({"error": "gmail_account missing from config"}))
        raise SystemExit(1)

    # Paths
    agent_root = Path(__file__).resolve().parent.parent
    model_path = agent_root / "data" / "bayes_model.json"
    brands_path = agent_root / "data" / "brand_domains.json"
    # Bundled with the skill, with monorepo fallback for dev
    bundled_deployed = agent_root / "data" / "deployed.json"
    sibling_deployed = agent_root.parent / "contracts" / "deployed.json"
    deployed_path = bundled_deployed if bundled_deployed.exists() else sibling_deployed
    cache_path = cfg_path.parent / "cache.db"

    # Optional registry (Watcher mode can skip if no RPC is set)
    registry = None
    rpc = os.environ.get("SEPOLIA_RPC")
    if rpc and deployed_path.exists():
        try:
            registry = RegistryClient(rpc_url=rpc, deployed_json=deployed_path)
        except Exception as exc:
            print(json.dumps({"warning": f"registry unavailable: {exc}"}), file=__import__("sys").stderr)

    cache = Cache(cache_path)
    pipe = Pipeline(
        model_path=model_path,
        brand_domains_path=brands_path,
        registry=registry,
        cache=cache,
    )
    gog = GogClient(account=account)

    results: list[dict] = []
    messages = gog.list_unread(query=args.query, max_results=args.max)
    for m in messages:
        msg_id = m.get("id")
        if not msg_id:
            continue
        try:
            raw = gog.fetch_mime(msg_id)
            record = pipe.process(raw)
            record["gmail_message_id"] = msg_id
            results.append(record)
        except Exception as exc:
            results.append({"gmail_message_id": msg_id, "error": str(exc)})

    print(json.dumps(results))


if __name__ == "__main__":
    _cli()
