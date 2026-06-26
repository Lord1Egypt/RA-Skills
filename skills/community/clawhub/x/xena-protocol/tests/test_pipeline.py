from pathlib import Path
from unittest.mock import MagicMock

import pytest

from bin.pipeline import Pipeline, combine_final

AGENT_ROOT = Path(__file__).parent.parent
FIXTURES = Path(__file__).parent / "fixtures"
MODEL_PATH = AGENT_ROOT / "data" / "bayes_model.json"
BRANDS_PATH = AGENT_ROOT / "data" / "brand_domains.json"


pytestmark = pytest.mark.skipif(
    not MODEL_PATH.exists(), reason="bayes_model.json missing — run trainer"
)


@pytest.fixture
def mock_registry():
    reg = MagicMock()
    reg.is_reported.return_value = (False, 0)
    reg.domain_report_count.return_value = 0
    return reg


@pytest.fixture
def pipe(mock_registry, tmp_path):
    from bin.cache import Cache
    return Pipeline(
        model_path=MODEL_PATH,
        brand_domains_path=BRANDS_PATH,
        registry=mock_registry,
        cache=Cache(tmp_path / "cache.db"),
    )


def _raw(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


# ---- benign email ----
def test_benign_scores_low_needs_no_llm_if_below_threshold(pipe):
    out = pipe.process(_raw("benign.eml"))
    assert out["from_domain"] == "github.com"
    assert out["gate_score"] == 0
    assert out["bayes_score"] < 50
    # small corpus can still push bayes above 20, so not always safe-fast-path
    # but must not fire a gate or trigger >= 70 pre-LLM
    assert out["pre_llm_score"] < 70


# ---- hard-spoof phish ----
def test_phish_spoof_triggers_auth_fail_gate(pipe):
    out = pipe.process(_raw("phish_spoof.eml"))
    # auth failure gate hits 95
    assert out["gate_score"] == 95
    assert "auth_all_fail" in out["gate_reasons"]
    # URL features also high
    assert out["url_score"] > 30
    assert out["needs_llm"] is True  # still want LLM for category
    assert out["verdict"] == "spoof"


def test_phish_spoof_has_bayes_signal(pipe):
    out = pipe.process(_raw("phish_spoof.eml"))
    assert out["bayes_score"] >= 70
    top = [t for t, _ in out["bayes_top_tokens"]]
    assert any(t in top for t in ("urgent", "verify", "limited"))


# ---- BEC (auth passes, social engineering) ----
def test_bec_quanta_no_auth_gate_but_strong_bayes_gate(pipe):
    out = pipe.process(_raw("bec_quanta.eml"))
    # auth all pass → no auth/display/registry gate…
    assert "auth_all_fail" not in out["gate_reasons"]
    assert "display_name_spoof" not in out["gate_reasons"]
    # …but Bayes is loud enough to trigger the strong_bayes gate
    assert out["bayes_score"] >= 85
    assert "strong_bayes" in out["gate_reasons"]
    assert out["gate_score"] >= 80
    top = [t for t, _ in out["bayes_top_tokens"]]
    assert any(t in top for t in ("quanta", "wire", "invoice", "urgent"))
    assert out["needs_llm"] is True


# ---- display-name spoof gate ----
def test_display_name_lookalike_triggers_gate_1_2():
    # Craft a synthetic email: display says "PayPal" but domain isn't paypal's
    import textwrap
    eml = textwrap.dedent("""
        From: "PayPal Security" <security@not-paypal.com>
        To: victim@example.com
        Subject: Account verification
        Message-ID: <lookalike@not-paypal.com>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Please verify your account.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert "display_name_spoof" in out["gate_reasons"]
    assert out["gate_score"] >= 80


# ---- verified-legit short-circuit ----
def test_legit_linkedin_subdomain_short_circuits_safe():
    # Real LinkedIn newsletter from e.linkedin.com — previously flagged
    # as display_name_spoof because domain didn't exact-match linkedin.com.
    import textwrap
    eml = textwrap.dedent("""
        From: "LinkedIn" <invitations@e.linkedin.com>
        To: me@example.com
        Subject: Jane has accepted your invitation
        Message-ID: <li-notif@e.linkedin.com>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Your invitation to connect has been accepted.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert out["short_circuit"] == "verified_brand_sender"
    assert out["verdict"] == "safe"
    assert out["should_alert"] is False
    assert out["should_report"] is False


def test_legit_google_security_alert_short_circuits_safe():
    import textwrap
    eml = textwrap.dedent("""
        From: "Google" <no-reply@accounts.google.com>
        To: me@gmail.com
        Subject: Security alert
        Message-ID: <g-alert@accounts.google.com>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        A new sign-in was detected on your account.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert out["short_circuit"] == "verified_brand_sender"
    assert out["verdict"] == "safe"


def test_legit_etherscan_short_circuits_safe():
    import textwrap
    eml = textwrap.dedent("""
        From: "Etherscan" <noreply@etherscan.io>
        To: me@example.com
        Subject: Welcome back
        Message-ID: <es@etherscan.io>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Welcome back to Etherscan.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert out["short_circuit"] == "verified_brand_sender"


def test_display_domain_aligned_subito_short_circuits():
    # "Subito" isn't in brand_domains — but display-domain alignment rule
    # catches it: "subito" is a word in from_domain "email.subito.it".
    import textwrap
    eml = textwrap.dedent("""
        From: "Subito" <noreply@email.subito.it>
        To: me@example.com
        Subject: Ecco come vanno i tuoi annunci
        Message-ID: <sub@email.subito.it>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Dai un occhio ai tuoi annunci attivi.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert out["short_circuit"] == "verified_brand_sender"


def test_display_domain_aligned_compound_word():
    # "YO Studios" → "yostudios" → matches from_domain "e.yostudios.com".
    import textwrap
    eml = textwrap.dedent("""
        From: "YO Studios" <hi@e.yostudios.com>
        To: me@example.com
        Subject: Monthly update from YO Studios
        Message-ID: <yo@e.yostudios.com>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        We shipped two features this month.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert out["short_circuit"] == "verified_brand_sender"


def test_display_domain_alignment_rejects_misspelled_spoof():
    # "PayPal" display vs "paypa1-secure.ru" domain — the misspelled
    # "paypa1" is not the same string as "paypal". No alignment.
    import textwrap
    eml = textwrap.dedent("""
        From: "PayPal" <verify@paypa1-secure.ru>
        To: victim@example.com
        Subject: Verify your account
        Message-ID: <fake@paypa1-secure.ru>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Click to verify.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    # Verified-legit does NOT fire (paypal not in paypa1-secure.ru).
    assert out["short_circuit"] is None
    # And the spoof gate still does.
    assert "display_name_spoof" in out["gate_reasons"]


def test_display_domain_alignment_ignores_noise_words():
    # "Notifications" / "Support" alone shouldn't count as alignment.
    import textwrap
    eml = textwrap.dedent("""
        From: "Support Team" <help@evil.ru>
        To: me@example.com
        Subject: Action required
        Message-ID: <s@evil.ru>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Please verify your account.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert out["short_circuit"] is None


def test_newsletter_mentioning_brand_in_subject_does_not_false_trigger():
    # TLDR-style newsletter with "LinkedIn" in subject. Old code matched
    # the brand token in subject → flagged as spoof. New code only looks
    # at display name.
    import textwrap
    eml = textwrap.dedent("""
        From: "TLDR" <newsletter@tldrnewsletter.com>
        To: me@example.com
        Subject: LinkedIn's layoffs, Apple's new chip, and more
        Message-ID: <tldr@tldrnewsletter.com>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Today in tech news.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    assert "display_name_spoof" not in out["gate_reasons"]


def test_paypal_lookalike_still_triggers_spoof_gate():
    # Ensure the verified-legit shortcut doesn't accidentally open the door
    # to spoofers. Display says PayPal, domain is attacker-controlled.
    import textwrap
    eml = textwrap.dedent("""
        From: "PayPal" <verify@paypa1-secure.ru>
        To: victim@example.com
        Subject: Verify your account
        Message-ID: <fake@paypa1-secure.ru>
        Authentication-Results: mx.example.com; spf=pass; dkim=pass; dmarc=pass
        Content-Type: text/plain

        Click to verify.
    """).strip().encode()
    pipe = _fresh_pipeline()
    out = pipe.process(eml)
    # Auth passes (attacker set up their own domain) but display says PayPal
    # and domain isn't paypal.com / *.paypal.com → gate fires
    assert "display_name_spoof" in out["gate_reasons"]
    assert out["gate_score"] >= 80
    assert out["short_circuit"] is None


# ---- registry hit gates ----
def test_registry_identity_hit_triggers_gate(mock_registry):
    mock_registry.is_reported.return_value = (True, 5)
    pipe = _fresh_pipeline(registry=mock_registry)
    out = pipe.process(_raw("bec_quanta.eml"))
    assert out["gate_score"] == 90
    assert "registry_identity_hit" in out["gate_reasons"]


def test_registry_domain_hit_triggers_gate(mock_registry):
    # Use bec_quanta fixture: display "Mark Anderson | Quanta" is not a
    # brand token in brand_domains, so the verified-legit shortcut doesn't
    # fire and the registry gate can be exercised.
    mock_registry.is_reported.return_value = (False, 0)
    mock_registry.domain_report_count.return_value = 10
    pipe = _fresh_pipeline(registry=mock_registry)
    out = pipe.process(_raw("bec_quanta.eml"))
    assert out["short_circuit"] is None
    assert "registry_domain_hit" in out["gate_reasons"]
    assert out["gate_score"] >= 75


# ---- reprocessing is allowed ----
def test_same_message_processed_repeatedly(pipe):
    # No caching — calling process twice returns the same (non-cache) output.
    # bec_quanta doesn't match the verified-legit shortcut; use it here.
    out1 = pipe.process(_raw("bec_quanta.eml"))
    out2 = pipe.process(_raw("bec_quanta.eml"))
    # Both runs return the same record; whether short_circuit is None
    # depends on the pipeline path, but the two runs must match.
    assert out1["from_domain"] == out2["from_domain"]
    assert out1.get("gate_score") == out2.get("gate_score")


# ---- combine_final formula ----
def test_combine_final_max_of_gate_and_blend():
    pre = {"gate_score": 95, "url_score": 50, "bayes_score": 80}
    out = combine_final(pre, llm_score=50, llm_category="phishing")
    assert out["confidence"] == 95
    assert out["category"] == "phishing"
    assert out["should_report"] is True


def test_combine_final_weighted_blend_when_gates_cold():
    # bayes 90 >= STRONG_BAYES_GATE_THRESHOLD so llm_trust fires.
    pre = {"gate_score": 0, "url_score": 60, "bayes_score": 90, "needs_llm": True}
    out = combine_final(pre, llm_score=90, llm_category="bec")
    # blended = 0.15*60 + 0.25*90 + 0.60*90 = 9 + 22.5 + 54 = 86
    # llm_trust = 90 (>= 80 threshold and bayes >= 85 corroborates)
    # confidence = max(0, 90, 86) = 90
    assert out["confidence"] == 90
    assert out["category"] == "bec"
    assert out["should_report"] is True


def test_combine_final_llm_trust_floor_with_strong_bayes_corroboration():
    # Real phish: strong Bayes ≥ 85 corroborates, LLM ≥ 80 threat.
    # Classic Nigerian Prince / Quanta BEC scenario.
    pre = {"gate_score": 0, "url_score": 0, "bayes_score": 90, "needs_llm": True}
    out = combine_final(pre, llm_score=92, llm_category="bec")
    # blended = 0.15*0 + 0.25*90 + 0.60*92 = 0 + 22.5 + 55.2 = 78
    # has_det_signal = True (bayes 90 >= 85 threshold)
    # llm_trust = 92
    # confidence = max(0, 92, 78) = 92
    assert out["confidence"] == 92
    assert out["should_report"] is True


def test_combine_final_llm_trust_does_NOT_fire_without_deterministic_signal():
    # LLM calls phishing at 90 but nothing else corroborates — classic
    # legit-transactional false positive (Subito newsletter, IDA newsletter).
    # Must NOT auto-report. Bayes 70 is below the 85 threshold now.
    pre = {"gate_score": 0, "url_score": 0, "bayes_score": 70, "needs_llm": True}
    out = combine_final(pre, llm_score=92, llm_category="phishing")
    # blended = 0.15*0 + 0.25*70 + 0.60*92 = 0 + 17.5 + 55.2 = 73
    # has_det_signal = False (bayes 70 < 85, no gate)
    # llm_trust = 0
    # confidence = max(0, 0, 73) = 73
    # 73 is above REPORT_THRESHOLD=70 but we want this to NOT auto-report.
    # Cap at REPORT_THRESHOLD - 1 when no deterministic signal.
    assert out["confidence"] < REPORT_THRESHOLD
    assert out["should_report"] is False
    assert out["should_alert"] is True   # still alert the user


def test_combine_final_llm_trust_does_not_fire_below_80():
    pre = {"gate_score": 0, "url_score": 10, "bayes_score": 30, "needs_llm": True}
    out = combine_final(pre, llm_score=75, llm_category="other")
    # blended = 0.15*10 + 0.25*30 + 0.60*75 = 1.5 + 7.5 + 45 = 54
    # llm_trust = 0 (< 80 threshold)
    # confidence = max(0, 0, 54) = 54
    assert out["confidence"] == 54
    assert out["should_report"] is False
    assert out["should_alert"] is True


def test_combine_final_safe_verdict_ignores_llm_score():
    # CRITICAL: LLM's 95% confidence in a "safe" verdict must NOT drive
    # the threat score. Newsletters were being auto-reported.
    pre = {"gate_score": 0, "url_score": 0, "bayes_score": 10, "needs_llm": True}
    out = combine_final(pre, llm_score=95, llm_category="safe")
    assert out["confidence"] == 0
    assert out["should_report"] is False
    assert out["should_alert"] is False


def test_combine_final_safe_verdict_beats_heuristic_gate():
    # Newsletter with phish-leaning tokens: strong_bayes gate fires at 80,
    # but LLM reads the content and says safe. LLM wins — heuristic gate
    # alone is not enough to override a safe verdict.
    pre = {"gate_score": 80, "url_score": 0, "bayes_score": 90, "needs_llm": True}
    out = combine_final(pre, llm_score=95, llm_category="safe")
    assert out["confidence"] == 0
    assert out["should_report"] is False
    assert out["should_alert"] is False


def test_combine_final_safe_verdict_loses_to_auth_fail_gate():
    # Auth-fail (95) is cryptographic evidence — trumps an LLM safe verdict.
    pre = {"gate_score": 95, "url_score": 0, "bayes_score": 50, "needs_llm": True}
    out = combine_final(pre, llm_score=95, llm_category="safe")
    assert out["confidence"] == 95
    assert out["should_report"] is True


def test_combine_final_safe_verdict_loses_to_registry_hit_gate():
    # Registry identity hit (90) means other agents flagged this sender.
    # Network corroboration beats a single LLM's safe opinion.
    pre = {"gate_score": 90, "url_score": 0, "bayes_score": 30, "needs_llm": True}
    out = combine_final(pre, llm_score=95, llm_category="safe")
    assert out["confidence"] == 90
    assert out["should_report"] is True


from bin.pipeline import ALERT_THRESHOLD, REPORT_THRESHOLD  # noqa: E402


def test_combine_final_below_report_threshold():
    pre = {"gate_score": 0, "url_score": 10, "bayes_score": 20, "needs_llm": True}
    out = combine_final(pre, llm_score=30, llm_category="other")
    # 0.25*10 + 0.25*20 + 0.5*30 = 2.5 + 5 + 15 = 22.5 → 22 or 23
    assert out["confidence"] < 70
    assert out["should_report"] is False


# ---- helpers ----
def _fresh_pipeline(*, registry=None):
    import tempfile

    from bin.cache import Cache
    if registry is None:
        registry = MagicMock()
        registry.is_reported.return_value = (False, 0)
        registry.domain_report_count.return_value = 0

    return Pipeline(
        model_path=MODEL_PATH,
        brand_domains_path=BRANDS_PATH,
        registry=registry,
        cache=Cache(tempfile.mkstemp()[1]),
    )
