"""Stage 1 - fetch the original Chinese lyrics (LRC) and build the syllable budget.

Output: <run-dir>/01_lyrics.json
  {source, song_id, lines:[{i, t, zh, chars, next_t, slot}], sentences:[...]}
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from common import load_json, save_json

LRC_API = "https://music.163.com/api/song/lyric"
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://music.163.com/"}
TAG = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")

# slot tail pads: a line may breathe this long past its syllable budget
TAIL = 1.2
PER_SYL = 0.62


def fetch(song_id: int) -> str:
    import requests
    r = requests.get(LRC_API, params={"id": song_id, "lv": 1, "kv": 1, "tv": -1},
                     headers=HEADERS, timeout=25)
    r.raise_for_status()
    j = r.json()
    if "lrc" not in j or not j["lrc"].get("lyric"):
        raise SystemExit(f"no lyric in response: {list(j)}")
    return j["lrc"]["lyric"]


def parse(lrc: str):
    rows = []
    for raw in lrc.splitlines():
        m = TAG.match(raw.strip())
        if not m:
            continue
        t = int(m.group(1)) * 60 + float(m.group(2))
        zh = m.group(3).strip()
        if not zh:
            continue
        # drop credit lines such as "作词 : 许嵩"
        if "：" in zh or (":" in zh and len(zh) < 20):
            continue
        rows.append((t, zh))
    rows.sort(key=lambda x: x[0])
    return rows


def build(rows):
    lines = []
    for i, (t, zh) in enumerate(rows):
        nxt = rows[i + 1][0] if i + 1 < len(rows) else t + 4.0
        chars = len(re.sub(r"[^\u4e00-\u9fff]", "", zh)) or len(zh)
        slot = min(nxt - t, PER_SYL * chars + TAIL)
        lines.append({"i": i, "t": round(t, 3), "zh": zh, "chars": chars,
                      "next_t": round(nxt, 3), "slot": round(max(slot, 0.8), 3)})
    # distinct consecutive sentences, for the translation budget
    sentences, seen_last = [], None
    for ln in lines:
        if ln["zh"] != seen_last:
            sentences.append({"zh": ln["zh"], "chars": ln["chars"],
                              "occurrences": [ln["t"]]})
            seen_last = ln["zh"]
        else:
            sentences[-1]["occurrences"].append(ln["t"])
    # merge repeats that are not adjacent (choruses repeat non-consecutively)
    by_text: dict[str, dict] = {}
    for s in sentences:
        if s["zh"] in by_text:
            by_text[s["zh"]]["occurrences"] += s["occurrences"]
        else:
            by_text[s["zh"]] = s
    uniq = list(by_text.values())
    return lines, uniq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--song-id", type=int, default=167691)
    ap.add_argument("--lrc-file", help="use a local .lrc instead of the API")
    a = ap.parse_args()

    run = Path(a.run_dir)
    run.mkdir(parents=True, exist_ok=True)

    lrc = Path(a.lrc_file).read_text(encoding="utf-8") if a.lrc_file else fetch(a.song_id)
    (run / "01_source.lrc").write_text(lrc, encoding="utf-8")

    rows = parse(lrc)
    if not rows:
        raise SystemExit("no lyric lines parsed")
    lines, uniq = build(rows)

    save_json(run / "01_lyrics.json", {
        "song_id": a.song_id,
        "span": [lines[0]["t"], lines[-1]["t"]],
        "n_lines": len(lines),
        "n_unique": len(uniq),
        "total_chars": sum(u["chars"] for u in uniq),
        "lines": lines,
        "sentences": uniq,
    })
    print(f"{len(lines)} lines, {len(uniq)} unique, "
          f"{lines[0]['t']:.2f}s -> {lines[-1]['t']:.2f}s, "
          f"{sum(u['chars'] for u in uniq)} chars to translate")


if __name__ == "__main__":
    main()
