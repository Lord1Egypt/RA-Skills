#!/usr/bin/env python3
"""
intent_gate.py — the banter-killer for the Space Duck auto-responder.

Prototype of D-loop step 3 (_classify_intent): decide whether an inbound peck is
ACTIONABLE (advances a goal → compose a reply) or NON-ACTIONABLE (ack / closure /
philosophy → silently close, NEVER reply). Intent, not tone.

Deterministic core first; ambiguous cases would fall through to a one-line LLM
tiebreak (marked below). Conservative default = non_actionable → a loop can only
ever DIE, never spin. This is the single change that makes banter impossible.

0.9.0 [P4] — third class `security_decline`. A security-correct refusal ("I
won't attest that version / grant ID") is neither banter nor a normal action:
it must NOT be re-asked (it matched verify/confirm patterns → the binary gate
called it actionable → the composer re-asked → refusal loop) and it must NOT be
silently closed (falling to non_actionable dropped the signal). Decline is
detected BEFORE the action scan and handed to the caller so peck_responder can
notify the owner exactly once and close — never reply, never loop.
"""
import re

# --- non-actionable: acknowledgements, closures, agreement, fortune-cookie filler ---
_ACK = [
    r"\bthanks?\b", r"\bthank you\b", r"\bagreed?\b", r"\bexactly\b", r"\bship it\b",
    r"\bnice work\b", r"\bgood (work|call|point|stuff|omen|sign|foundation)\b",
    r"\bglad (it|that|to)\b", r"\bsounds? (good|right|correct)\b", r"\blgtm\b",
    r"\b\+1\b", r"\bwell said\b", r"\bcouldn'?t agree\b", r"\bfair enough\b",
    r"\bthat'?s (a )?(keeper|fair|right)\b", r"\bhappy (it|to)\b", r"\bcheers\b",
    r"\bmakes sense\b", r"\bnoted\b", r"\bwill do\b", r"\bgot it\b", r"\bperfect\b",
    r"\byou'?re right\b", r"\bright —", r"\bgood rule of thumb\b",
]
# --- actionable: questions, requests, decisions-needed, new data, blockers ---
_ACTION = [
    r"\?",                                   # a question
    r"\b(can|could|would|will) you\b", r"\bplease\b", r"\bneed (you|to|the|a)\b",
    r"\bshould (we|i|you)\b", r"\b(what|how|why|when|where|which|who)\b.*\?",
    r"\bsend (me|the|over)\b", r"\bconfirm\b", r"\bverif(y|ied|ication)\b",
    r"\bseed\b", r"\bprovide\b", r"\bapprove\b", r"\bdeploy\b", r"\bmerge\b",
    r"\bblocked?\b", r"\berror\b", r"\bfailed?\b", r"\bbug\b", r"\bbroken\b",
    r"\bjob[_ ]?id\b", r"\bcreds?\b", r"\bruling\b", r"\breconcile\b",
    r"\bdecide\b", r"\bdecision\b", r"\bnext step\b", r"\baction\b",
    r"\bwait(ing)? on\b", r"\bcan'?t\b.*\bwithout\b",
]

# --- security_decline: a refusal to attest / vouch / confirm identity, a
#     version, a grant, an ID, or a credential. TWO signals are required — a
#     refusal VERB and an attestation CONTEXT — so a plain request ("can you
#     verify the grant ID?") is never mistaken for a refusal. The context is
#     deliberately narrow (attest/vouch/sign-off, or verify/confirm OF a
#     version|grant|id|identity|claim) so "can't proceed without creds" (a
#     request FOR something, not a refusal to PROVIDE it) stays actionable.
_DECLINE_VERB = [
    r"\bwo?n'?t\b", r"\bwill not\b", r"\bcan'?t\b", r"\bcannot\b",
    r"\bunable to\b", r"\bnot able to\b", r"\brefus(e|es|ing|ed|al)\b",
    r"\bdeclin(e|es|ing|ed)\b", r"\bnot going to\b", r"\bnot comfortable\b",
    r"\bnot willing\b", r"\bno way (i|we)\b",
]
_DECLINE_CONTEXT = [
    r"\battest", r"\bvouch\b", r"\bsign off\b", r"\bstand behind\b",
    r"\b(verify|verifying|confirm|confirming|validate|validating|certify)\b"
    r"[^.?!]*\b(version|grant|id|identity|claim|credential|key|attestation)\b",
    r"\b(version|grant|id|identity|claim|credential|key)\b"
    r"[^.?!]*\b(is|are)?\s*(genuine|authentic|legitimate|real|valid)\b",
    r"\bgrant[_ ]?id\b", r"\bversion (id|number|string|hash)\b",
    r"\bthat (version|grant|id|identity|claim)\b",
]


def _is_security_decline(t: str):
    verb = next((p for p in _DECLINE_VERB if re.search(p, t)), None)
    if not verb:
        return None
    ctx = next((p for p in _DECLINE_CONTEXT if re.search(p, t)), None)
    if not ctx:
        return None
    return f"refusal /{verb}/ + attest-context /{ctx}/"


def classify_intent(text: str):
    """Return ('actionable'|'non_actionable'|'security_decline', reason)."""
    t = (text or "").strip().lower()
    if not t:
        return "non_actionable", "empty"
    # Decline is scanned FIRST: a refusal to attest often also contains
    # verify/confirm (action) words, so the binary gate used to call it
    # actionable and re-ask. Catch it before the action scan.
    dec = _is_security_decline(t)
    if dec:
        return "security_decline", dec
    for pat in _ACTION:
        if re.search(pat, t):
            return "actionable", f"matched action signal /{pat}/"
    for pat in _ACK:
        if re.search(pat, t):
            return "non_actionable", f"ack/closure /{pat}/"
    # No actionable signal AND no explicit ack → ambiguous.
    # PRODUCTION: one-line LLM tiebreak ("requires an action or answer? YES/NO").
    # PROTOTYPE: conservative default — no ask detected → do not reply (loops can only die).
    return "non_actionable", "no action signal (LLM-tiebreak in prod; conservative default)"

def should_reply(text: str) -> bool:
    return classify_intent(text)[0] == "actionable"

if __name__ == "__main__":
    # Real corpus: the actual filler pecks from Josh's JP + Cash transcripts (must SILENCE),
    # plus genuinely actionable pecks (must REPLY).
    CORPUS = [
        # --- REAL banter that looped forever (expect NON_ACTIONABLE / silent) ---
        ("Agreed — TTL plus grace window closes the loop cleanly. Ship it.", "silence"),
        ("Shipping it — nice work getting the grace window right on the first pass.", "silence"),
        ("Thanks — glad the grace window logic landed cleanly. Timing edge cases can be fiddly.", "silence"),
        ("Exactly right — the number is almost never the real problem.", "silence"),
        ("That five-minute heuristic is a keeper — simple enough to remember.", "silence"),
        ("Good foundation to build on.", "silence"),
        ("the scenic route has a way of teaching things the shortcut never could", "silence"),
        ("disorientation is the tuition fee for spatial reasoning", "silence"),
        ("dead ends are where you learn the terrain", "silence"),
        # --- genuinely actionable (expect ACTIONABLE / reply) ---
        ("Can you seed a test job and peck me the job ID?", "reply"),
        ("D1: the Dry Run job shows Confirmed on fabricated context — needs a ruling.", "reply"),
        ("Doc-gen run cmr1q6exd80 failed 0/3 — reconcile with your 3-confirmed claim?", "reply"),
        ("Still blocked on test-login creds for app.builditproof.com — can you send them?", "reply"),
        ("Should we set the grace window to 30s or 60s?", "reply"),
        # actionable requests that MENTION verify/grant/id but are NOT refusals —
        # guard against the decline detector over-matching a plain ask.
        ("Can you verify the grant ID and confirm it's live before I retry?", "reply"),
        ("I can't proceed without the test-login creds — can you send them?", "reply"),
        # --- security_decline (expect SECURITY_DECLINE / decline) ---
        # Real refusals that MUST notify the owner once and close, never re-ask.
        ("I won't attest that version — I can't confirm the grant ID is genuine.", "decline"),
        ("Refusing to vouch for that grant ID without provenance.", "decline"),
        ("I cannot confirm that identity claim; declining to attest.", "decline"),
        ("No way I sign off on that version string — it's unverified.", "decline"),
        ("I'm not comfortable certifying that the credential is authentic.", "decline"),
    ]
    ok = 0
    print(f"{'EXPECT':8} {'GOT':14} {'✓':2}  TEXT")
    print("-" * 90)
    for text, expect in CORPUS:
        verdict, reason = classify_intent(text)
        got = {"actionable": "reply",
               "security_decline": "decline"}.get(verdict, "silence")
        hit = "✓" if got == expect else "✗"
        if got == expect:
            ok += 1
        print(f"{expect:8} {got:14} {hit:2}  {text[:60]}")
    print("-" * 90)
    print(f"RESULT: {ok}/{len(CORPUS)} correct")
    raise SystemExit(0 if ok == len(CORPUS) else 1)
