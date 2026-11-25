#!/usr/bin/env python3
"""
anti_echo.py — D5 convergence guard for the Space Duck auto-responder.

Belt-and-suspenders behind the D3 intent gate: even if two messages both read as
"actionable", a reply that is ~a paraphrase of something we already said to this
peer (or the Nth near-identical turn) is the banter tail. Suppress it.

Per-PEER (not per-chain) ring buffer of recent reply fingerprints; a pending reply
that is >= SIM_THRESHOLD similar to any recent one → ECHO → do not send.
Purely local, no network. File-backed store at ~/.space-duck/reply_history.json.
"""
import json, re, os
from pathlib import Path

SD_DIR = Path(os.environ.get('SPACEDUCK_DIR', str(Path.home() / '.space-duck')))
STORE = SD_DIR / 'reply_history.json'
KEEP = 6              # recent replies remembered per peer
SIM_THRESHOLD = 0.5   # containment ratio above which a reply counts as an echo.
# 0.5 = half the content words repeat a recent reply → restatement/paraphrase of a
# settled point. Biased toward suppression on purpose: this is a safety net BEHIND the
# D3 intent gate, so the cost of a false-suppress is just one un-sent reply (peer re-asks),
# while the benefit is killing the paraphrase tail D3's tone-blind pass can miss.

# Two guards keep that suppression bias off SHORT status replies. Containment puts the
# smaller token set in the denominator, so a terse reply that merely reuses the subject
# nouns of a longer earlier reply scores high on word overlap while carrying entirely new
# information. Unguarded, the promised follow-up to "I'll peck you the job ID in ~2 min"
# — "Job ID is 4471 — running now." — scores 60% and gets eaten.
MIN_TOKENS = 5        # below this, containment is too noisy to act on → never suppress.
_DIGIT = re.compile(r"\d")
# A novel token carrying a digit (id, count, version, duration: 4471, 3/3, v1056, 45s) is
# new information by definition — a restatement cannot introduce one. Always send.

_WORD = re.compile(r"[a-z0-9]+")

def _tokens(text: str):
    # normalize: lowercase, words only, drop trivial stopwords that inflate overlap
    stop = {'the','a','an','and','or','but','is','it','that','this','to','of','in',
            'on','for','with','as','at','be','so','i','you','we','its','not','—'}
    return [w for w in _WORD.findall((text or '').lower()) if w not in stop]

def _similarity(a: str, b: str) -> float:
    ta, tb = set(_tokens(a)), set(_tokens(b))
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    return inter / min(len(ta), len(tb))   # containment ratio — catches paraphrase/restatement

def _load():
    try:
        return json.loads(STORE.read_text())
    except Exception:
        return {}

def _save(d):
    try:
        STORE.parent.mkdir(parents=True, exist_ok=True)
        STORE.write_text(json.dumps(d)[:200000])
    except Exception:
        pass

def is_echo(peer_sd: str, reply_text: str) -> tuple:
    """Return (echo: bool, reason). Does NOT record — call record() after a real send."""
    hist = _load().get(peer_sd, [])
    reply_tokens = set(_tokens(reply_text))
    if len(reply_tokens) < MIN_TOKENS:
        return False, f'too short to score ({len(reply_tokens)} content words)'
    for prev in hist:
        s = _similarity(reply_text, prev)
        if s < SIM_THRESHOLD:
            continue
        novel = reply_tokens - set(_tokens(prev))
        carried = sorted(t for t in novel if _DIGIT.search(t))
        if carried:
            return False, f'new identifier vs recent reply ({", ".join(carried[:3])})'
        return True, f'{int(s*100)}% overlap with a recent reply to {peer_sd[:8]}'
    return False, 'novel'

def record(peer_sd: str, reply_text: str):
    d = _load()
    lst = d.get(peer_sd, [])
    lst.append(reply_text[:500])
    d[peer_sd] = lst[-KEEP:]
    _save(d)

if __name__ == '__main__':
    # Simulate a converging thread: distinct real replies pass; paraphrased restatements
    # of what we already said get suppressed as echo.
    import tempfile
    SD_DIR = Path(tempfile.mkdtemp()); STORE = SD_DIR / 'reply_history.json'
    PEER = 'A2471364EA154B2A'
    stream = [
        ("Seeding the test job now — I'll peck you the job ID in ~2 min.",        'send'),
        ("Clock skew: going with a 45s grace window, rationale in the ADR.",       'send'),
        # now the tail starts — paraphrases of things already said:
        ("Agreed, clock skew handling is the tricky part; grace window it is.",    'suppress'),
        ("Right, the grace window handles the clock skew — good call.",            'suppress'),
        # a genuinely new actionable reply should still pass:
        ("Doc-gen run failed 0/3 — I need the missing inputs to reproduce.",       'send'),
        # the promised follow-up: reuses the subject nouns of turn 1, but carries the
        # identifier that was the whole point of the promise. Must NOT be eaten.
        ("Job ID is 4471 — running now.",                                          'send'),
        # terse status, below the scoring floor — containment is meaningless here.
        ("Grace window shipped.",                                                  'send'),
    ]
    ok = 0
    print(f"{'EXPECT':9} {'GOT':9} {'✓':2}  REPLY")
    print('-'*88)
    for text, expect in stream:
        echo, reason = is_echo(PEER, text)
        got = 'suppress' if echo else 'send'
        hit = '✓' if got == expect else '✗'
        ok += (got == expect)
        if not echo:
            record(PEER, text)   # only real sends enter history
        print(f"{expect:9} {got:9} {hit:2}  {text[:58]}")
    print('-'*88)
    print(f"RESULT: {ok}/{len(stream)} correct")
