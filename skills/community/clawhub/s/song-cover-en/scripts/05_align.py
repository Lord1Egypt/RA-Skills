"""Stage 5 (v2) - lay the singable English onto the real melody.

Why this was rewritten: the first version gave every LRC line a *time window* and
grabbed whatever notes fell inside it. The LRC timestamps do not match the actual
singing, so one line received a single note while the next received seventeen.
The singer then had to cram several syllables onto one note (audible sudden speed
up) and hold others absurdly long (audible dragging). Two changes fix it:

  1. Notes are allocated per *section* with a monotonic sequence alignment, so each
     line gets a contiguous run of notes about as long as the original Chinese line
     was. Every line gets a fair share of the melody, and no line can absorb the
     opening of the next one -- which is what the earlier clock-proportional split
     did whenever note density was uneven.
  2. The English is written to fit inside that budget (syllables <= characters),
     so no note ever has to be split to make room for an extra syllable.

Only when a line genuinely has more syllables than its note budget do we split a
note, and we report how often that happens so it stays visible.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _env import LIBS

here = Path(__file__).resolve().parent
for p in (str(LIBS), str(here)):
    if p not in sys.path:
        sys.path.insert(0, p)

import singlib as S  # noqa: E402

GROUP_GAP_S = 12.0      # a longer silence than this starts a new sung section


def split_sections(lines: list[dict]) -> list[list[dict]]:
    groups: list[list[dict]] = []
    cur = [lines[0]]
    for prev, ln in zip(lines, lines[1:]):
        if ln["t"] - prev["t"] > GROUP_GAP_S:
            groups.append(cur)
            cur = [ln]
        else:
            cur.append(ln)
    groups.append(cur)
    return groups


def allocate(notes: list[dict], chars: list[int], needs: list[int] | None = None) -> list[list[dict]]:
    """Give each line a contiguous, monotonically ordered run of notes.

    This used to cut the section's *clock* in proportion to each line's character
    count. That assumes note density is uniform, and it is not: one line lands on a
    cluster of short notes, finishes early, and the next line's opening slides into
    its melody -- which is precisely the reported "the English line plus the start of
    the next one makes up one Chinese line's tune".

    Now we solve a monotonic sequence alignment (S.align_lines_to_notes) whose cost is
    how far each line's note count is from the number of notes the original Chinese
    line occupied (its character count). Boundaries then cannot drift, because group i
    starts exactly where group i-1 ended.

    `chars[i]` is used as the note budget, with `needs[i]` (the English syllable
    count) as a floor so no syllable ever has to share a note.
    """
    if not notes:
        return [[] for _ in chars]
    if len(notes) < len(chars):
        notes = S.pad_notes_for_lines(notes, len(chars))

    budget = list(chars)
    if needs:
        budget = [max(c, n) for c, n in zip(chars, needs)] if len(needs) == len(chars) else budget

    groups = S.align_lines_to_notes(notes, budget)
    return [notes[lo:hi] for lo, hi in groups]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--lyrics",
                    default=str(Path(__file__).resolve().parents[1] / "assets" / "lyrics_en.json"))
    ap.add_argument("--min-note", type=float, default=0.07)
    a = ap.parse_args()

    run = Path(a.run_dir)
    out = run / "05"
    out.mkdir(parents=True, exist_ok=True)

    lst = json.loads((run / "01_lyrics.json").read_text(encoding="utf-8"))
    mel = json.loads((run / "04" / "melody.json").read_text(encoding="utf-8"))
    words = json.loads(Path(a.lyrics).read_text(encoding="utf-8"))
    en_by_zh = {d["zh"]: d["en"] for d in words["lines"]}

    notes = S.clean_notes(mel["notes"], min_dur=a.min_note)

    sections = split_sections(lst["lines"])
    report, segments, splits = [], [], 0
    for gi, grp in enumerate(sections):
        sec_start = grp[0]["t"] - 0.3
        sec_end = grp[-1]["next_t"] if grp[-1]["next_t"] - grp[-1]["t"] < 14 else grp[-1]["t"] + 8
        pool = [n for n in notes if sec_start <= n["start_s"] < sec_end]
        pool = S.first_vocal_run(pool, max_gap=2.5)
        if not pool:
            print(f"  !! section {gi}: no notes", flush=True)
            continue

        chars = [len(g["zh"]) for g in grp]
        # how many notes each line would need so that no syllable ever shares one
        needs = [len(S.syllables_of_line(en_by_zh.get(g["zh"], ""))) for g in grp]
        share = allocate(pool, chars, needs)
        events: list[dict] = []
        g_start, g_end = None, 0.0
        for ln, my_notes in zip(grp, share):
            en = en_by_zh.get(ln["zh"])
            if en is None:
                print(f"  !! no translation for {ln['zh']}", flush=True)
                continue
            syls = S.syllables_of_line(en)
            if len(syls) > len(my_notes):
                splits += 1
            fitted = S.fit_syllables_to_notes(syls, my_notes)
            if not fitted:
                print(f"  !! no notes for {ln['zh']}", flush=True)
                continue

            syll_to_word: list[int] = []
            wl = S.words_with_syllables(en)
            for wi, (_w, k) in enumerate(wl):
                syll_to_word.extend([wi] * k)
            # carry the word id instead of a "starts a word" flag: build_segment may
            # drop overlapping notes, and a dropped flag would silently lose the
            # boundary, while a word id can always be compared to its predecessor
            for e in fitted:
                si = e["syllable_index"]
                e["word_id"] = syll_to_word[si] if si < len(syll_to_word) else len(wl) - 1
            events.extend(fitted)

            wstart: dict[int, float] = {}
            wend: dict[int, float] = {}
            for e in fitted:
                wi = syll_to_word[e["syllable_index"]] if e["syllable_index"] < len(syll_to_word) else 0
                wstart.setdefault(wi, e["start_s"])
                wend[wi] = max(wend.get(wi, 0.0), e["start_s"] + e["dur_s"])
            word_times = [{"w": wl[wi][0] if wi < len(wl) else "",
                           "t0": round(wstart[wi], 3), "t1": round(wend[wi], 3)}
                          for wi in sorted(wstart)]

            dur = fitted[-1]["start_s"] + fitted[-1]["dur_s"] - fitted[0]["start_s"]
            report.append({
                "line": ln["i"], "zh": ln["zh"], "en": en,
                "chars": len(ln["zh"]), "syllables": len(syls),
                "notes": len(my_notes), "placed": len(fitted),
                "t": ln["t"], "sung_s": round(dur, 2),
                "syl_per_s": round(len(syls) / max(dur, 1e-3), 2),
                "phonemes": [e["phoneme"] for e in fitted],
                "words": word_times,
            })
            if g_start is None:
                g_start = fitted[0]["start_s"]
            g_end = max(g_end, fitted[-1]["start_s"] + fitted[-1]["dur_s"])

        if not events:
            continue
        seg = S.build_segment(events, g_start - 0.3, g_end + 0.35)
        if seg:
            seg["_group"] = gi
            # Mark which note index starts a new word: the renderer cuts long
            # sections into chunks, and it must not cut inside a word or the word
            # gets split across two model passes and comes out garbled.
            seg_events = [e for e in events]
            starts = [i for i, e in enumerate(seg_events) if i == 0 or
                      e["syllable_index"] != seg_events[i - 1]["syllable_index"]]
            seg["_syll_starts"] = [e["syllable_index"] for e in seg_events]
            segments.append(seg)
            print(f"section {gi}: {len(grp)} lines, {len(events)} notes, "
                  f"{seg['time'][0]/1000:.2f}-{seg['time'][1]/1000:.2f}s "
                  f"({(seg['time'][1]-seg['time'][0])/1000:.1f}s)", flush=True)

    # ---- reference prompt: the original singer's own timbre.
    #
    # Getting this wrong transposes the whole cover. SoulX's auto_shift computes
    # f0_shift = median(prompt notes) - median(target notes) and then shifts every
    # target note by it, which pulls the vocal into the *prompt's* register no
    # matter what notes we ask for. So the prompt has to sit in the same register
    # as the song, otherwise the cover comes out a semitone (or worse) off and
    # clashes with the backing track, which is in the original key.
    #
    # We therefore pick the Chinese phrase whose median pitch is closest to the
    # song's overall median, which makes f0_shift ~ 0.
    all_pitch = sorted(n["midi"] for n in notes)
    global_median = all_pitch[len(all_pitch) // 2]

    best_prompt, best_gap = None, 1e9
    for ln in lst["lines"]:
        cand = S.first_vocal_run(
            [n for n in notes if ln["t"] - 0.3 <= n["start_s"] < ln["next_t"]], max_gap=0.6)
        if len(cand) < 4:
            continue
        med = sorted(n["midi"] for n in cand)[len(cand) // 2]
        gap = abs(med - global_median)
        if gap < best_gap:
            best_gap, best_prompt = gap, (ln, cand, med)

    prompt_seg = None
    if best_prompt:
        ln_p, p_notes, p_med = best_prompt
        p_tok = [S.chr_token(c) for c in ln_p["zh"]]
        p_fit = S.fit_syllables_to_notes(p_tok, p_notes, tokens=p_tok,
                                         weights=[1.0] * len(p_tok))
        if p_fit:
            p0 = p_fit[0]["start_s"] - 0.15
            p1 = p_fit[-1]["start_s"] + p_fit[-1]["dur_s"] + 0.15
            prompt_seg = S.build_segment(p_fit, p0, p1)
            if prompt_seg:
                prompt_seg["_wav_span"] = [round(p0, 3), round(p1, 3)]
                prompt_seg["_median_note"] = round(p_med, 1)
                prompt_seg["_song_median_note"] = round(global_median, 1)
            print(f"prompt: '{ln_p['zh']}' {len(p_fit)} notes, {p0:.2f}-{p1:.2f}s, "
                  f"median pitch {p_med:.1f} vs song {global_median:.1f} "
                  f"(gap {p_med-global_median:+.1f} st -> auto_shift will apply "
                  f"{round(global_median - p_med)} st)", flush=True)

    (out / "target.json").write_text(json.dumps(segments, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
    (out / "prompt.json").write_text(json.dumps([prompt_seg] if prompt_seg else [],
                                                ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "align.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                    encoding="utf-8")

    tot = sum(r["sung_s"] for r in report)
    rates = [r["syl_per_s"] for r in report]
    print(f"\nlines placed {len(report)}   total sung {tot:.1f}s", flush=True)
    print(f"lines needing note splits: {splits}", flush=True)
    # a steady pace is the whole point: report the spread, not just the mean
    import statistics as st
    print(f"syllables/s: mean {st.mean(rates):.2f}  median {st.median(rates):.2f}  "
          f"min {min(rates):.2f}  max {max(rates):.2f}", flush=True)
    over = [r for r in report if r["syllables"] > r["chars"]]
    print(f"lines where english syllables exceed chinese characters: {len(over)}", flush=True)
    for r in over:
        print(f"   {r['zh']} ({r['chars']}) -> {r['syllables']}: {r['en']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
