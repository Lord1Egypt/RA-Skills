"""Screenshot a rendered report in headless Chrome: the flowchart (desktop, dark, a selected file), the overview tab, and a true 390 px phone width (macOS headless Chrome will not go narrower than 500 px, so the phone view is a 390 px iframe inside a 500 px window)."""
from __future__ import annotations

import os
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

CANDIDATES = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium")
NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")
GRAPH_W, GRAPH_H = 1400, 900  # the flowchart fills the window, so it is shot at a normal screen size
PHONE_H = 1400  # tall enough to show the stacked graph (55 vh) and the top of the panel


def find_chrome() -> str | None:
    env = os.environ.get("VIBE_LEDGER_CHROME")
    if env and Path(env).exists():
        return env
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    for n in NAMES:
        found = shutil.which(n)
        if found:
            return found
    return None


def _shoot(chrome: str, url: str, out: Path, width: int, height: int) -> bool:
    try:
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={width},{height}", f"--screenshot={out}", url],
                       capture_output=True, timeout=90)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return out.exists() and out.stat().st_size > 0


def take_shots(report: Path, out_dir: Path, chrome: str, select: str | None = None, journey: str | None = None,
               height: int = 6000, requirements: bool = False, dataflow: bool = False) -> list[Path]:
    report = Path(report).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    url = report.as_uri()
    sel = f"?select={quote(select, safe='/')}" if select else ""
    phone_page = out_dir / "phone.html"
    phone_page.write_text(
        '<!doctype html><meta charset="utf-8"><body style="margin:0">'
        f'<iframe src="{url}{sel}" style="width:390px;height:{PHONE_H}px;border:0"></iframe>',
        encoding="utf-8")
    jobs = [(url, "desktop.png", GRAPH_W, GRAPH_H),
            (url + "?theme=dark", "desktop-dark.png", GRAPH_W, GRAPH_H),
            (phone_page.as_uri(), "phone-390.png", 500, PHONE_H)]
    if select:
        jobs.append((url + sel, "selected.png", GRAPH_W, GRAPH_H))
    if journey:
        jobs.append((url + f"?journey={quote(journey)}", "journey.png", GRAPH_W, GRAPH_H))
    jobs.append((url + "?tab=overview", "overview.png", 1280, height))
    if dataflow:
        jobs.append((url + "?mode=data", "dataflow.png", GRAPH_W, GRAPH_H))
    if requirements:
        jobs.append((url + "?tab=requirements", "requirements.png", 1280, height))
    return [out_dir / name for u, name, w, h in jobs if _shoot(chrome, u, out_dir / name, w, h)]


class _NodeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes: list[dict] = []
        self.done = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "body" and a.get("data-layout") == "done":
            self.done = True
        if tag == "g" and "vlg-node" in (a.get("class") or "").split():
            self.nodes.append({"id": a.get("data-id"), "x": float(a.get("data-x") or 0), "y": float(a.get("data-y") or 0),
                               "w": float(a.get("data-w") or 0), "h": float(a.get("data-h") or 0),
                               "cls": a.get("class") or "", "dim": a.get("data-dim") or "0"})


def dump_dom(chrome: str, url: str, timeout: int = 90) -> str:
    """The page's DOM after its scripts ran (headless Chrome)."""
    try:
        res = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--window-size=1400,900",
                              "--virtual-time-budget=5000", "--dump-dom", url],
                             capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return res.stdout


def layout_report(dom: str) -> dict:
    p = _NodeParser()
    p.feed(dom or "")
    nodes, overlaps = p.nodes, []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            if (a["x"] < b["x"] + b["w"] - 1 and b["x"] < a["x"] + a["w"] - 1
                    and a["y"] < b["y"] + b["h"] - 1 and b["y"] < a["y"] + a["h"] - 1):
                overlaps.append([a["id"], b["id"]])
    return {"done": p.done, "nodes": nodes, "overlaps": overlaps,
            "selected": [n["id"] for n in nodes if "sel" in n["cls"].split()]}
