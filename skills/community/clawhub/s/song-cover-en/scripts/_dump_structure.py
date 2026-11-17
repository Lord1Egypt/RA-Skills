import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import load_json

run = Path(sys.argv[1])
mel = load_json(run / "04" / "melody.json")
seen, out = set(), []
for l in mel["lines"]:
    if l["zh"] in seen:
        continue
    seen.add(l["zh"])
    out.append({"zh": l["zh"], "n": len(l["notes"]), "notes": l["notes"],
                "slot": l["slot"], "t0": l["t0"]})
print(len(out), "unique lines")
for o in out:
    print(f"{o['zh']:<9} n={o['n']} slot={o['slot']:.2f}s "
          f"dur/syl={o['slot']/o['n']:.2f} {o['notes']}")
Path(run / "05").mkdir(parents=True, exist_ok=True)
(run / "05" / "structure.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
