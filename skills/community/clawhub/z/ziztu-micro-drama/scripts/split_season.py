#!/usr/bin/env python3
"""Split a season Fountain file into one file per episode, ready to import into Ziztu (one project per episode).

Usage:
  python3 split_season.py season.fountain --out episodes/ [--strip-notes]

The season file has an optional title page, then a section line per episode, then that episode's scenes:

  Title: Marry Me by Friday
  Format: Live-action vertical micro drama, 9:16

  # Episode 1: The Hundred-Dollar Bill

  INT. BLAKE TOWER - CEO OFFICE - DAY

  ...

  # Episode 2: Majority Owner

  ...

(Keep a blank line before and after every section line and scene heading: Fountain needs it to read a heading.)

Each episode file gets its own title page ("Title: <series>", "Episode: <n> - <title>" and the season's other keys) and
is named ep01-the-hundred-dollar-bill.fountain. --strip-notes leaves out [[notes]] for a clean reading copy (keep them
for Ziztu: its shot planner reads notes inside scenes as writer notes). Existing files are never overwritten unless
--force is given. Standard library only.
"""
import argparse
import os
import re
import sys

EP_RE = re.compile(r"^\s*#{1,6}\s*(?:episode|ep\.?)\s*(\d+)\s*[:.\-–—]?\s*(.*)$", re.I)
TITLE_LINE = re.compile(r"^([A-Za-z][A-Za-z ]{0,30}):\s*(.*)$")


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:48] or "episode"


def read_title_page(lines):
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    keys = []
    if i < len(lines) and TITLE_LINE.match(lines[i].strip()):
        while i < len(lines) and lines[i].strip():
            m = TITLE_LINE.match(lines[i].strip())
            if m:
                keys.append([m.group(1).strip(), m.group(2).strip()])
            elif keys:
                keys[-1][1] = (keys[-1][1] + "\n   " + lines[i].strip()).strip()
            i += 1
    return keys, i


def strip_notes(text):
    return re.sub(r"\n?[ \t]*\[\[[\s\S]*?\]\][ \t]*\n?", "\n", text)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Split a season Fountain file into episode files.")
    ap.add_argument("season", help="the season .fountain file")
    ap.add_argument("--out", required=True, help="folder for the episode files")
    ap.add_argument("--strip-notes", action="store_true", help="leave out [[notes]]")
    ap.add_argument("--force", action="store_true", help="overwrite existing episode files")
    args = ap.parse_args(argv)
    with open(args.season, encoding="utf-8") as fh:
        text = fh.read().replace("\r\n", "\n")
    lines = text.split("\n")
    keys, start = read_title_page(lines)
    series = next((v for k, v in keys if k.lower() in ("title", "series")), "")
    other = [(k, v) for k, v in keys if k.lower() not in ("title", "series", "episode")]
    marks = [i for i in range(start, len(lines)) if EP_RE.match(lines[i])]
    if not marks:
        print("No '# Episode N' section lines found in %s." % args.season, file=sys.stderr)
        return 2
    os.makedirs(args.out, exist_ok=True)
    written = []
    for a, i in enumerate(marks):
        end = marks[a + 1] if a + 1 < len(marks) else len(lines)
        m = EP_RE.match(lines[i])
        num, name = int(m.group(1)), m.group(2).strip()
        body = "\n".join(lines[i + 1:end]).strip("\n")
        if args.strip_notes:
            body = strip_notes(body)
        head = []
        if series:
            head.append("Title: %s" % series)
        head.append("Episode: %d%s" % (num, (" - " + name) if name else ""))
        head += ["%s: %s" % (k, v) for k, v in other]
        content = "\n".join(head) + "\n\n" + re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
        path = os.path.join(args.out, "ep%02d-%s.fountain" % (num, slug(name or "episode-%d" % num)))
        if os.path.exists(path) and not args.force:
            print("Exists, not overwritten (use --force): %s" % path, file=sys.stderr)
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(path)
    for p in written:
        print(p)
    print("%d episode file(s) written to %s" % (len(written), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
