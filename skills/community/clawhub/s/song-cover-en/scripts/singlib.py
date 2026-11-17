"""Shared singing-metadata helpers for the v2 pipeline.

SoulX-Singer does not want text, it wants four whitespace-separated strings plus a
millisecond time window:

  duration   seconds per note
  phoneme    one token per note: en_<ARPAbet syllables joined by -> or zh_<pinyin>
  note_pitch MIDI integer per note (0 = rest)
  note_type  1 = rest, 2 = new syllable, 3 = continuation of the previous syllable

Getting this right is what makes the output *sing* rather than speak: the phonemes
are placed on real notes of the original melody.
"""
from __future__ import annotations

import re
from typing import Iterable

import numpy as np

VOWELS = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY",
          "IH", "IY", "OW", "OY", "UH", "UW"}

# onsets English permits at the start of a syllable, longest first
ONSETS = ["STR", "SPR", "SKR", "SPL", "SKW", "THR", "SHR", "KWR",
          "PL", "PR", "BL", "BR", "TR", "DR", "KL", "KR", "GL", "GR",
          "FL", "FR", "TH", "SH", "CH", "SL", "SW", "TW", "DW", "KW", "GW",
          "SP", "ST", "SK", "SM", "SN", "S",
          "P", "B", "T", "D", "K", "G", "F", "V", "M", "N", "L", "R",
          "W", "Y", "HH", "JH", "Z", "DH", "ZH", "NG"]

_cmudict = None


def cmu() -> dict:
    global _cmudict
    if _cmudict is None:
        import cmudict as _c
        _cmudict = _c.dict()
    return _cmudict


def word_phones(word: str) -> list[str] | None:
    """ARPAbet phonemes (stress kept) for one word, or None if unknown."""
    d = cmu()
    w = re.sub(r"[^a-z']", "", word.lower())
    if not w:
        return None
    if w in d:
        return list(d[w][0])
    # crude fallback so an unusual name does not break the whole line
    if w.endswith("'s") and w[:-2] in d:
        return list(d[w[:-2]][0]) + ["Z"]
    return None


def syllabify(phones: list[str]) -> list[list[str]]:
    """Split a word's phonemes into syllables, maximal-onset style.

    English allows a consonant cluster after a vowel to belong to the next
    syllable's onset ("a-strin-gent"), which is exactly how a singer places them,
    so we hand as many consonants as form a legal onset to the following syllable.
    """
    vidx = [i for i, p in enumerate(phones) if p.rstrip("012") in VOWELS]
    if not vidx:
        return [phones] if phones else []
    if len(vidx) == 1:
        return [phones]
    cuts = []
    for a, b in zip(vidx, vidx[1:]):
        cluster = phones[a + 1:b]
        take = len(cluster)
        # shrink the onset until it is a legal English initial cluster
        while take > 0:
            if len(cluster[-take:]) == 1 or "".join(x.rstrip("012") for x in cluster[-take:]) in ONSETS:
                break
            take -= 1
        if take == 0 and cluster:
            take = 0
        cuts.append(b - take)
    out, prev = [], 0
    for c in cuts:
        out.append(phones[prev:c])
        prev = c
    out.append(phones[prev:])
    return [s for s in out if s]


def syllables_of_line(text: str) -> list[list[str]]:
    """Every syllable of a line, each as a phoneme list."""
    out: list[list[str]] = []
    for word in re.findall(r"[A-Za-z']+", text):
        ph = word_phones(word)
        if not ph:
            # unknown word: fake one open vowel per vowel group of the spelling
            groups = re.findall(r"[aeiouy]+", word.lower()) or ["ah"]
            for _ in groups:
                out.append(["AH1"])
            continue
        out.extend(syllabify(ph))
    return out


def words_with_syllables(text: str) -> list[tuple[str, int]]:
    """(word, syllable count) in order, so syllable indices map back to words."""
    out: list[tuple[str, int]] = []
    for word in re.findall(r"[A-Za-z']+", text):
        ph = word_phones(word)
        if not ph:
            n = len(re.findall(r"[aeiouy]+", word.lower())) or 1
        else:
            n = len(syllabify(ph))
        out.append((word, n))
    return out


def phoneme_token(syl: list[str]) -> str:
    return "en_" + "-".join(syl)


def chr_token(ch: str) -> str:
    """SoulX wants whole Mandarin syllables: `zh_xiang3`, `zh_ni3`, `zh_le5`.

    Only needed for the *reference* vocal; the English target uses en_ tokens.
    """
    from pypinyin import Style, pinyin
    got = pinyin(ch, style=Style.TONE3, neutral_tone_with_five=True, errors="ignore")
    if not got or not got[0]:
        return "<SP>"
    return "zh_" + got[0][0].lower()


def clean_notes(notes: list[dict], min_dur: float = 0.07) -> list[dict]:
    """Drop tracker blips and fold same-pitch neighbours together."""
    if not notes:
        return []
    out = []
    for n in notes:
        if n["dur_s"] < min_dur:
            continue
        if out and abs(n["midi"] - out[-1]["midi"]) < 0.75 and n["start_s"] - out[-1]["end_s"] < 0.06:
            prev = out[-1]
            prev["end_s"] = n["end_s"]
            prev["dur_s"] = prev["end_s"] - prev["start_s"]
            prev["midi"] = (prev["midi"] + n["midi"]) / 2
        else:
            out.append(dict(n))
    return out


def first_vocal_run(notes: list[dict], max_gap: float = 1.0) -> list[dict]:
    """Keep the longest continuous stretch of singing inside a window.

    LRC line windows are unreliable: an instrumental break can sit inside one, and
    without this a line would drag in notes from a later chorus. We take the
    *longest* run rather than the first, because a line sometimes begins with one
    stray note from the previous phrase.
    """
    if not notes:
        return []
    runs: list[list[dict]] = []
    cur = [notes[0]]
    for n in notes[1:]:
        if n["start_s"] - cur[-1]["end_s"] > max_gap:
            runs.append(cur)
            cur = [n]
        else:
            cur.append(n)
    runs.append(cur)
    if len(runs) == 1:
        return runs[0]
    return max(runs, key=lambda r: r[-1]["end_s"] - r[0]["start_s"])


def pad_notes_for_lines(notes: list[dict], k: int) -> list[dict]:
    """Split the longest notes in halves until there are at least `k` of them.

    Last resort when a section has fewer tracker notes than lyric lines: a line with
    no note at all cannot be sung, and handing it a *sibling's* note would make two
    lines share one melody slot -- the exact drift we are fixing. Splitting keeps the
    pitch and the note order intact, so callers must use the returned list.
    """
    notes = [dict(n) for n in notes]
    while len(notes) < k:
        i = max(range(len(notes)), key=lambda j: notes[j]["dur_s"])
        n = notes[i]
        if n["dur_s"] < 0.12:
            break
        mid = n["start_s"] + n["dur_s"] / 2
        a = dict(n, end_s=round(mid, 3), dur_s=round(mid - n["start_s"], 3))
        b = dict(n, start_s=round(mid, 3), dur_s=round(n["end_s"] - mid, 3))
        notes[i:i + 1] = [a, b]
    return notes


def align_lines_to_notes(notes: list[dict], need: list[int],
                         dur_weight: float = 0.0,
                         floor: list[int] | None = None) -> list[tuple[int, int]]:
    """Split `notes` into len(need) contiguous groups; return (start, end) per line.

    Why not allocate by the clock: cutting a section's elapsed time in proportion to
    each line's character count assumes note density is uniform, which it is not. One
    line lands on a cluster of short notes and finishes early, so the *next* line's
    opening slides into its melody -- the listener hears "this English line plus the
    start of the next one" as one Chinese line's tune.

    The fix is a proper monotonic sequence alignment: choose cut points so that line
    i receives a contiguous run of notes whose length k is as close as possible to
    need[i] (the line's Chinese character count = how many notes the original line
    occupied). Cost is (k - need[i])^2, so being one note short costs the same as one
    too many and no line can be starved to feed another. Because every group starts
    where the previous one ended, boundaries can never drift backwards.

    `floor[i]`, when given, is a hard minimum note count for line i (use the English
    syllable count: two syllables can never share a note without splitting it).
    `dur_weight` optionally adds a term matching each group's time span to its
    proportional share of the section, which keeps syllables/second uniform; 0
    disables it.

    The returned indices always refer to the `notes` list passed in. If there are
    fewer notes than lines, call `pad_notes_for_lines` first and pass its result --
    this function will not invent notes, it just degrades monotonically.
    """
    n_lines, n_notes = len(need), len(notes)
    if n_lines == 0:
        return []
    if n_notes == 0:
        return [(0, 0) for _ in range(n_lines)]
    if n_notes < n_lines:
        # not enough notes to give everyone one; hand out what exists, monotonically
        return [(min(i, n_notes), min(i + 1, n_notes)) for i in range(n_lines)]

    INF = float("inf")
    # dp[i][j] = best cost after assigning lines 0..i-1 to notes 0..j-1
    dp = np.full((n_lines + 1, n_notes + 1), INF)
    back = np.zeros((n_lines + 1, n_notes + 1), dtype=np.int32)
    dp[0, 0] = 0.0

    starts = np.array([n["start_s"] for n in notes])
    ends = np.array([n["end_s"] for n in notes])
    span_total = float(ends[-1] - starts[0])
    need_total = sum(need) or 1

    for i in range(1, n_lines + 1):
        w = need[i - 1]
        f = max(1, floor[i - 1]) if floor else 1
        # with a floor, a line can be allowed to run longer than 2.5x its budget
        lo = max(1, min(int(w * 0.25), f))
        hi = max(lo + 1, int(w * 2.5) + 2, f + 1)
        exp = span_total * w / need_total
        for j in range(i, n_notes - (n_lines - i) + 1):
            best, arg = INF, -1
            # k = notes given to line i-1; look back over a sane window only
            for k in range(lo, min(hi, j) + 1):
                prev = dp[i - 1, j - k]
                if prev == INF:
                    continue
                c = prev + (k - w) ** 2
                if dur_weight:
                    span = ends[j - 1] - starts[j - k]
                    c += dur_weight * (span - exp) ** 2
                if c < best:
                    best, arg = c, k
            dp[i, j] = best
            back[i, j] = arg

    groups: list[tuple[int, int]] = []
    j = n_notes
    for i in range(n_lines, 0, -1):
        k = int(back[i, j])
        if k <= 0:
            k = 1
        groups.append((j - k, j))
        j -= k
    groups.reverse()
    return groups


def fit_syllables_to_notes(syls: list, notes: list[dict],
                          tokens: list[str] | None = None,
                          weights: list[float] | None = None) -> list[dict]:
    """Lay syllables onto notes, one syllable per note where possible.

    `syls` may be phoneme lists (English) or plain strings; `tokens` overrides the
    emitted phoneme token, which is how the Chinese reference prompt reuses the
    same layout code with `zh_` tokens.

    Two cases the old pipeline could not handle (it hard-failed unless the counts
    matched exactly):
      * more notes than syllables -> extra notes become melisma (note_type 3),
        which is how a singer holds a vowel across several notes;
      * fewer notes than syllables -> the longest notes are split, because a
        syllable simply cannot share a note with another syllable.

    The DP keeps each syllable on a *contiguous* run of notes and penalises
    allocation that drifts from the natural speech rhythm, so the result follows
    the melody instead of dumping syllables on bar lines.
    """
    n_note, n_syl = len(notes), len(syls)
    if n_note == 0 or n_syl == 0:
        return []

    if tokens is None:
        tokens = [phoneme_token(s) if isinstance(s, list) else str(s) for s in syls]
    if weights is None:
        weights = [max(len(s), 1) if isinstance(s, list) else 1 for s in syls]

    # split notes if we are short of them
    notes = [dict(n) for n in notes]
    while len(notes) < n_syl:
        i = max(range(len(notes)), key=lambda k: notes[k]["dur_s"])
        n = notes[i]
        if n["dur_s"] < 0.12:
            break
        mid = n["start_s"] + n["dur_s"] / 2
        a = dict(n, end_s=round(mid, 3), dur_s=round(mid - n["start_s"], 3))
        b = dict(n, start_s=round(mid, 3), dur_s=round(n["end_s"] - mid, 3))
        notes[i:i + 1] = [a, b]
    n_note = len(notes)
    if n_syl > n_note:
        # still short: give the tail syllables to the last note rather than crash
        n_syl = n_note
        tokens = tokens[:n_syl]
        weights = weights[:n_syl]

    total_dur = sum(n["dur_s"] for n in notes)
    weight = np.array(weights[:n_syl], dtype=float)
    want = weight / weight.sum() * total_dur

    INF = 1e18
    # dp[j][i]: best cost placing first i notes into first j syllables
    dp = np.full((n_syl + 1, n_note + 1), INF)
    back = np.zeros((n_syl + 1, n_note + 1), dtype=int)
    dp[0][0] = 0.0
    for j in range(1, n_syl + 1):
        for i in range(1, n_note + 1):
            best, arg = INF, -1
            spent = 0.0
            for k in range(i - 1, -1, -1):
                spent += notes[k]["dur_s"]
                if dp[j - 1][k] >= INF:
                    continue
                cost = dp[j - 1][k] + (spent - want[j - 1]) ** 2 / max(want[j - 1], 1e-3)
                if cost < best:
                    best, arg = cost, k
            dp[j][i] = best
            back[j][i] = arg
    if dp[n_syl][n_note] >= INF:
        # fall back to a straight proportional split
        spans, acc = [], 0
        for j in range(n_syl):
            take = max(1, int(round(want[j] / total_dur * n_note)))
            spans.append((acc, min(acc + take, n_note)))
            acc = spans[-1][1]
        spans[-1] = (spans[-1][0], n_note)
    else:
        spans, i = [], n_note
        for j in range(n_syl, 0, -1):
            k = back[j][i]
            spans.append((k, i))
            i = k
        spans.reverse()

    out = []
    for j, (a, b) in enumerate(spans):
        for t in range(a, b):
            n = notes[t]
            out.append({
                "start_s": n["start_s"],
                "dur_s": n["dur_s"],
                "midi": n["midi"],
                "phoneme": tokens[j],
                "note_type": 2 if t == a else 3,
                "syllable_index": j,
            })
    return out


def build_segment(events: list[dict], t0: float, t1: float,
                  sample_rate: int = 24000, hop_size: int = 480) -> dict | None:
    """Turn note events into one SoulX target segment covering [t0, t1] seconds.

    Notes coming from adjacent LRC lines can overlap slightly in time. SoulX lays
    notes end to end, so an overlap would silently stretch the segment past its
    window and make the audio drift out of sync -- clamp each note to the next
    note's onset.
    """
    if not events:
        return None
    events = sorted((dict(e) for e in events), key=lambda e: e["start_s"])
    # Drop notes that a later note tramples almost entirely, then clamp the rest.
    # Both matter: LRC lines overlap, and a negative-length note would make the
    # final duration correction below go negative.
    kept: list[dict] = []
    for e in events:
        if kept and e["start_s"] - kept[-1]["start_s"] < 0.02:
            if e["dur_s"] > kept[-1]["dur_s"]:
                kept[-1] = e
            continue
        kept.append(e)
    events = kept
    for i in range(len(events) - 1):
        limit = events[i + 1]["start_s"] - events[i]["start_s"]
        if limit > 0.02 and events[i]["dur_s"] > limit:
            events[i]["dur_s"] = limit
    events = [e for e in events if e["dur_s"] > 0.02]
    if not events:
        return None
    t0 = min(t0, events[0]["start_s"])
    t1 = max(t1, events[-1]["start_s"] + events[-1]["dur_s"])

    dur, ph, pitch, ntype, wid = [], [], [], [], []
    # lead-in rest, so the model starts from silence like the record does
    if events[0]["start_s"] - t0 > 0.02:
        dur.append(round(events[0]["start_s"] - t0, 4))
        ph.append("<SP>")
        pitch.append(0)
        ntype.append(1)
        wid.append(-1)
    for idx, e in enumerate(events):
        if idx:
            gap = e["start_s"] - (events[idx - 1]["start_s"] + events[idx - 1]["dur_s"])
            if gap > 0.02:
                dur.append(round(gap, 4))
                ph.append("<SP>")
                pitch.append(0)
                ntype.append(1)
                wid.append(-1)
        dur.append(round(e["dur_s"], 4))
        ph.append(e["phoneme"])
        pitch.append(int(round(e["midi"])))
        ntype.append(e["note_type"])
        wid.append(int(e.get("word_id", -1)))
    last = events[-1]["start_s"] + events[-1]["dur_s"]
    if t1 - last > 0.02:
        dur.append(round(t1 - last, 4))
        ph.append("<SP>")
        pitch.append(0)
        ntype.append(1)
        wid.append(-1)
    # Derive "this note begins a word" from the word ids rather than trusting a
    # precomputed flag: notes get dropped as overlapping above, and a dropped flag
    # would silently erase a word boundary the renderer needs for chunking.
    word_start = []
    prev = None
    for w in wid:
        is_start = 0 if w < 0 else int(w != prev)
        word_start.append(is_start)
        if w >= 0:
            prev = w
    # SoulX derives its frame count from sum(duration); make it land exactly on t1-t0
    fix = (t1 - t0) - sum(dur)
    if abs(fix) > 1e-6 and dur:
        dur[-1] = round(dur[-1] + fix, 4)
    if dur[-1] <= 0.01 or sum(dur) <= 0:
        return None
    return {
        "time": [int(round(t0 * 1000)), int(round(t1 * 1000))],
        "duration": " ".join(f"{d:.4f}" for d in dur),
        "phoneme": " ".join(ph),
        "note_pitch": " ".join(str(p) for p in pitch),
        "note_type": " ".join(str(t) for t in ntype),
        "word_start": " ".join(str(w) for w in word_start),
    }
