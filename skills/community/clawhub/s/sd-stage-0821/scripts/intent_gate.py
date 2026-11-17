#!/usr/bin/env python3
"""
intent_gate.py — the banter-killer for the Space Duck auto-responder.

Prototype of D-loop step 3 (_classify_intent): decide whether an inbound peck is
ACTIONABLE (advances a goal → compose a reply) or NON-ACTIONABLE (ack / closure /
philosophy → silently close, NEVER reply). Intent, not tone.

Deterministic core first; ambiguous cases would fall through to a one-line LLM
tiebreak (marked below). Conservative default = non_actionable → a loop can only
ever DIE, never spin. This is the single change that makes banter impossible.
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

def classify_intent(text: str):
    """Return ('actionable'|'non_actionable', reason)."""
    t = (text or "").strip().lower()
    if not t:
        return "non_actionable", "empty"
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
    ]
    ok = 0
    print(f"{'EXPECT':8} {'GOT':14} {'✓':2}  TEXT")
    print("-" * 90)
    for text, expect in CORPUS:
        verdict, reason = classify_intent(text)
        got = "reply" if verdict == "actionable" else "silence"
        hit = "✓" if got == expect else "✗"
        if got == expect:
            ok += 1
        print(f"{expect:8} {got:14} {hit:2}  {text[:60]}")
    print("-" * 90)
    print(f"RESULT: {ok}/{len(CORPUS)} correct")
