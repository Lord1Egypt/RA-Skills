#!/usr/bin/env bash
# slide/scripts/script.sh — Presentation slide deck builder
# Data: ~/.slide/data.jsonl
set -euo pipefail

VERSION="1.0.0"
DATA_DIR="$HOME/.slide"
DATA_FILE="$DATA_DIR/data.jsonl"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

CMD="${1:-help}"
shift 2>/dev/null || true

show_help() {
cat << 'HELPEOF'
Slide Skill v1.0.0 — Presentation slide deck builder

Commands:
  create       Create a new slide deck
  add          Add a new slide to a deck
  edit         Edit a slide's title, content, or layout
  reorder      Move a slide to a new position
  theme        Apply or view a theme for a deck
  outline      Show a text outline of all slides
  export       Export a deck to HTML or JSON
  preview      Generate a quick text preview of a slide
  list         List all decks or slides within a deck
  template     List built-in templates or apply one
  notes        Add or view speaker notes for a slide
  help         Show this help
  version      Show version

Examples:
  script.sh create "Quarterly Review" --author "Kelly"
  script.sh add deck_abc --title "Welcome" --content "Q1 Results" --layout title
  script.sh edit slide_xyz --content "Updated figures"
  script.sh theme deck_abc --set dark
  script.sh export deck_abc --format html --output out.html
HELPEOF
}

case "$CMD" in

create|add|edit|reorder|theme|outline|export|preview|list|template|notes)
__SKILL_ARGS_JSON=$(python3 -c "import sys,json; print(json.dumps(sys.argv[1:]))" "$@")
export __SKILL_CMD="$CMD" __SKILL_ARGS="$__SKILL_ARGS_JSON"
python3 << 'PYEOF' 
import sys, json, os, uuid, datetime

DATA_FILE = os.path.expanduser("~/.slide/data.jsonl")

def load_all():
    records = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    return records

def save_all(records):
    with open(DATA_FILE, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

def append_record(record):
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def now_iso():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_args(args):
    parsed = {}
    positional = []
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i+1].startswith("--"):
                parsed[key] = args[i+1]
                i += 2
            else:
                parsed[key] = True
                i += 1
        else:
            positional.append(args[i])
            i += 1
    return parsed, positional

def find_decks(records, deck_id=None):
    return [r for r in records if r.get("type") == "deck" and (deck_id is None or r.get("id") == deck_id)]

def find_slides(records, deck_id=None, slide_id=None):
    results = []
    for r in records:
        if r.get("type") != "slide":
            continue
        if deck_id and r.get("deck_id") != deck_id:
            continue
        if slide_id and r.get("id") != slide_id:
            continue
        results.append(r)
    return sorted(results, key=lambda x: x.get("order", 0))

VALID_LAYOUTS = ["title", "content", "two-column", "image", "blank", "section-header"]
VALID_THEMES = ["default", "dark", "light", "corporate", "creative", "minimal"]
TEMPLATES = {
    "blank": {"name": "blank", "slides": []},
    "pitch-deck": {"name": "pitch-deck", "slides": ["Title", "Problem", "Solution", "Market Size", "Business Model", "Traction", "Team", "Ask"]},
    "quarterly-review": {"name": "quarterly-review", "slides": ["Title", "Agenda", "Q Summary", "Revenue", "Growth", "Challenges", "Next Quarter", "Q&A"]},
    "project-proposal": {"name": "project-proposal", "slides": ["Title", "Background", "Objectives", "Approach", "Timeline", "Budget", "Risks", "Next Steps"]},
    "workshop": {"name": "workshop", "slides": ["Title", "Overview", "Section 1", "Exercise 1", "Section 2", "Exercise 2", "Summary", "Resources"]},
}

def cmd_create(args):
    p, pos = parse_args(args)
    title = pos[0] if pos else p.get("title")
    if not title:
        print("ERROR: Title is required (first positional argument)", file=sys.stderr)
        sys.exit(1)
    deck_id = "deck_" + uuid.uuid4().hex[:8]
    rec = {
        "type": "deck",
        "id": deck_id,
        "title": title,
        "author": p.get("author", ""),
        "description": p.get("description", ""),
        "theme": "default",
        "slide_count": 0,
        "created_at": now_iso(),
        "updated_at": now_iso()
    }
    append_record(rec)
    print(json.dumps({"ok": True, "id": deck_id, "title": title}, indent=2))

def cmd_add(args):
    p, pos = parse_args(args)
    deck_id = pos[0] if pos else p.get("deck")
    if not deck_id:
        print("ERROR: Deck ID is required (first positional argument)", file=sys.stderr)
        sys.exit(1)
    records = load_all()
    decks = find_decks(records, deck_id=deck_id)
    if not decks:
        print(f"ERROR: Deck '{deck_id}' not found", file=sys.stderr)
        sys.exit(1)
    title = p.get("title", "Untitled Slide")
    content = p.get("content", "")
    layout = p.get("layout", "content")
    if layout not in VALID_LAYOUTS:
        print(f"ERROR: Invalid layout. Choose from: {VALID_LAYOUTS}", file=sys.stderr)
        sys.exit(1)
    existing_slides = find_slides(records, deck_id=deck_id)
    order = len(existing_slides) + 1
    slide_id = "slide_" + uuid.uuid4().hex[:8]
    rec = {
        "type": "slide",
        "id": slide_id,
        "deck_id": deck_id,
        "title": title,
        "content": content,
        "layout": layout,
        "order": order,
        "notes": "",
        "created_at": now_iso(),
        "updated_at": now_iso()
    }
    append_record(rec)
    # Update deck slide count
    for r in records:
        if r.get("id") == deck_id and r.get("type") == "deck":
            r["slide_count"] = order
            r["updated_at"] = now_iso()
            break
    save_all(records)
    # Re-append the new slide since save_all overwrote
    append_record(rec)
    # Actually, let's do it properly
    records2 = load_all()
    # Check if slide already added
    if not any(r.get("id") == slide_id for r in records2):
        append_record(rec)
    print(json.dumps({"ok": True, "id": slide_id, "deck_id": deck_id, "order": order}, indent=2))

def cmd_edit(args):
    p, pos = parse_args(args)
    slide_id = pos[0] if pos else p.get("slide")
    if not slide_id:
        print("ERROR: Slide ID is required (first positional argument)", file=sys.stderr)
        sys.exit(1)
    records = load_all()
    found = False
    for r in records:
        if r.get("type") == "slide" and r.get("id") == slide_id:
            found = True
            if p.get("title"):
                r["title"] = p["title"]
            if p.get("content"):
                r["content"] = p["content"]
            if p.get("layout"):
                if p["layout"] not in VALID_LAYOUTS:
                    print(f"ERROR: Invalid layout. Choose from: {VALID_LAYOUTS}", file=sys.stderr)
                    sys.exit(1)
                r["layout"] = p["layout"]
            r["updated_at"] = now_iso()
            break
    if not found:
        print(f"ERROR: Slide '{slide_id}' not found", file=sys.stderr)
        sys.exit(1)
    save_all(records)
    print(json.dumps({"ok": True, "message": f"Slide '{slide_id}' updated"}, indent=2))

def cmd_reorder(args):
    p, pos = parse_args(args)
    slide_id = pos[0] if pos else p.get("slide")
    position = p.get("position")
    if not slide_id or not position:
        print("ERROR: Slide ID and --position are required", file=sys.stderr)
        sys.exit(1)
    position = int(position)
    records = load_all()
    target = None
    for r in records:
        if r.get("type") == "slide" and r.get("id") == slide_id:
            target = r
            break
    if not target:
        print(f"ERROR: Slide '{slide_id}' not found", file=sys.stderr)
        sys.exit(1)
    deck_id = target["deck_id"]
    slides = find_slides(records, deck_id=deck_id)
    slides = [s for s in slides if s["id"] != slide_id]
    slides.insert(position - 1, target)
    for i, s in enumerate(slides, 1):
        for r in records:
            if r.get("id") == s["id"] and r.get("type") == "slide":
                r["order"] = i
                r["updated_at"] = now_iso()
                break
    save_all(records)
    print(json.dumps({"ok": True, "message": f"Slide '{slide_id}' moved to position {position}"}, indent=2))

def cmd_theme(args):
    p, pos = parse_args(args)
    deck_id = pos[0] if pos else p.get("deck")
    if not deck_id:
        print("ERROR: Deck ID is required", file=sys.stderr)
        sys.exit(1)
    if p.get("list"):
        print("Available themes:")
        for t in VALID_THEMES:
            print(f"  - {t}")
        return
    theme_name = p.get("set")
    if not theme_name:
        records = load_all()
        decks = find_decks(records, deck_id=deck_id)
        if not decks:
            print(f"ERROR: Deck '{deck_id}' not found", file=sys.stderr)
            sys.exit(1)
        print(json.dumps({"deck": deck_id, "theme": decks[0].get("theme", "default")}, indent=2))
        return
    if theme_name not in VALID_THEMES:
        print(f"ERROR: Invalid theme. Choose from: {VALID_THEMES}", file=sys.stderr)
        sys.exit(1)
    records = load_all()
    found = False
    for r in records:
        if r.get("type") == "deck" and r.get("id") == deck_id:
            r["theme"] = theme_name
            r["updated_at"] = now_iso()
            found = True
            break
    if not found:
        print(f"ERROR: Deck '{deck_id}' not found", file=sys.stderr)
        sys.exit(1)
    save_all(records)
    print(json.dumps({"ok": True, "message": f"Theme '{theme_name}' applied to '{deck_id}'"}, indent=2))

def cmd_outline(args):
    p, pos = parse_args(args)
    deck_id = pos[0] if pos else p.get("deck")
    if not deck_id:
        print("ERROR: Deck ID is required", file=sys.stderr)
        sys.exit(1)
    records = load_all()
    decks = find_decks(records, deck_id=deck_id)
    if not decks:
        print(f"ERROR: Deck '{deck_id}' not found", file=sys.stderr)
        sys.exit(1)
    deck = decks[0]
    slides = find_slides(records, deck_id=deck_id)
    print(f"Outline: {deck.get('title','')}")
    print(f"Author: {deck.get('author','')}")
    print(f"Theme: {deck.get('theme','default')}")
    print("-" * 40)
    for s in slides:
        print(f"  {s.get('order',0):>3}. [{s.get('layout','content')}] {s.get('title','')}")
        if s.get("content"):
            preview = s["content"][:60] + ("..." if len(s.get("content","")) > 60 else "")
            print(f"       {preview}")

def cmd_export(args):
    p, pos = parse_args(args)
    deck_id = pos[0] if pos else p.get("deck")
    if not deck_id:
        print("ERROR: Deck ID is required", file=sys.stderr)
        sys.exit(1)
    fmt = p.get("format", "html")
    output_file = p.get("output")
    records = load_all()
    decks = find_decks(records, deck_id=deck_id)
    if not decks:
        print(f"ERROR: Deck '{deck_id}' not found", file=sys.stderr)
        sys.exit(1)
    deck = decks[0]
    slides = find_slides(records, deck_id=deck_id)
    if fmt == "json":
        data = {"deck": deck, "slides": slides}
        content = json.dumps(data, indent=2)
    else:
        theme = deck.get("theme", "default")
        theme_colors = {
            "default": ("bg:#fff;color:#333", "#2c3e50"),
            "dark": ("bg:#1a1a2e;color:#eee", "#e94560"),
            "light": ("bg:#f8f9fa;color:#212529", "#0d6efd"),
            "corporate": ("bg:#fff;color:#2c3e50", "#2980b9"),
            "creative": ("bg:#fdf6e3;color:#657b83", "#dc322f"),
            "minimal": ("bg:#fff;color:#000", "#000"),
        }
        bg, accent = theme_colors.get(theme, theme_colors["default"])
        slide_html = []
        for s in slides:
            slide_html.append(f"""
<div class="slide" style="{bg}">
  <h2 style="color:{accent}">{s.get('title','')}</h2>
  <div class="content">{s.get('content','')}</div>
  <div class="slide-num">{s.get('order',0)}</div>
</div>""")
        content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{deck.get('title','Presentation')}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
.slide{{width:100vw;height:100vh;display:none;flex-direction:column;justify-content:center;align-items:center;padding:60px;position:relative}}
.slide.active{{display:flex}}
.slide h2{{font-size:2.5em;margin-bottom:30px}}
.slide .content{{font-size:1.4em;max-width:80%;text-align:center}}
.slide-num{{position:absolute;bottom:20px;right:30px;font-size:0.9em;opacity:0.5}}
body{{overflow:hidden;font-family:system-ui,sans-serif}}
</style></head><body>
{''.join(slide_html)}
<script>
let cur=0;const slides=document.querySelectorAll('.slide');
function show(n){{slides.forEach(s=>s.classList.remove('active'));if(slides[n])slides[n].classList.add('active')}}
document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key===' '){{cur=Math.min(cur+1,slides.length-1);show(cur)}}
  else if(e.key==='ArrowLeft'){{cur=Math.max(cur-1,0);show(cur)}}
  else if(e.key==='f'){{document.documentElement.requestFullscreen?.()}}
}});
show(0);
</script></body></html>"""
    if output_file:
        with open(output_file, "w") as f:
            f.write(content)
        print(json.dumps({"ok": True, "message": f"Exported to {output_file}", "format": fmt}))
    else:
        print(content)

def cmd_preview(args):
    p, pos = parse_args(args)
    slide_id = pos[0] if pos else p.get("slide")
    if not slide_id:
        print("ERROR: Slide ID is required", file=sys.stderr)
        sys.exit(1)
    records = load_all()
    slides = find_slides(records, slide_id=slide_id)
    if not slides:
        print(f"ERROR: Slide '{slide_id}' not found", file=sys.stderr)
        sys.exit(1)
    s = slides[0]
    print(f"┌{'─'*50}┐")
    print(f"│ Slide #{s.get('order',0):<5} [{s.get('layout','content')}]{' '*(50-18-len(str(s.get('order',0)))-len(s.get('layout','content')))}│")
    print(f"├{'─'*50}┤")
    title = s.get("title","")
    print(f"│ {title:<49}│")
    print(f"│{' '*50}│")
    content = s.get("content","")
    for line in content.split("\\n")[:5]:
        line = line[:48]
        print(f"│ {line:<49}│")
    print(f"│{' '*50}│")
    if s.get("notes"):
        print(f"│ Notes: {s['notes'][:41]:<42}│")
    print(f"└{'─'*50}┘")

def cmd_list(args):
    p, pos = parse_args(args)
    records = load_all()
    deck_id = p.get("deck")
    limit = int(p.get("limit", 100))
    if deck_id:
        slides = find_slides(records, deck_id=deck_id)[:limit]
        if not slides:
            print(f"No slides found in deck '{deck_id}'.")
            return
        header = f"{'#':<5} {'ID':<16} {'Title':<30} {'Layout':<15}"
        print(header)
        print("-" * len(header))
        for s in slides:
            print(f"{s.get('order',0):<5} {s.get('id',''):<16} {s.get('title',''):<30} {s.get('layout',''):<15}")
    else:
        decks = find_decks(records)[:limit]
        if not decks:
            print("No decks found.")
            return
        header = f"{'ID':<16} {'Title':<30} {'Author':<15} {'Theme':<10} {'Slides':<8}"
        print(header)
        print("-" * len(header))
        for d in decks:
            print(f"{d.get('id',''):<16} {d.get('title',''):<30} {d.get('author',''):<15} {d.get('theme',''):<10} {d.get('slide_count',0):<8}")

def cmd_template(args):
    p, pos = parse_args(args)
    if p.get("list"):
        print("Available templates:")
        for name, tpl in TEMPLATES.items():
            slides = tpl.get("slides", [])
            print(f"  {name:<20} ({len(slides)} slides)")
            if slides:
                print(f"    Slides: {', '.join(slides)}")
        return
    apply_name = p.get("apply")
    if not apply_name:
        print("ERROR: Use --list to list templates or --apply NAME to apply one", file=sys.stderr)
        sys.exit(1)
    if apply_name not in TEMPLATES:
        print(f"ERROR: Template '{apply_name}' not found. Use --list.", file=sys.stderr)
        sys.exit(1)
    tpl = TEMPLATES[apply_name]
    deck_id = "deck_" + uuid.uuid4().hex[:8]
    deck_rec = {
        "type": "deck",
        "id": deck_id,
        "title": apply_name.replace("-", " ").title(),
        "author": "",
        "description": f"Created from template: {apply_name}",
        "theme": "default",
        "slide_count": len(tpl["slides"]),
        "created_at": now_iso(),
        "updated_at": now_iso()
    }
    records = [deck_rec]
    for i, slide_title in enumerate(tpl["slides"], 1):
        slide_rec = {
            "type": "slide",
            "id": "slide_" + uuid.uuid4().hex[:8],
            "deck_id": deck_id,
            "title": slide_title,
            "content": "",
            "layout": "title" if i == 1 else "content",
            "order": i,
            "notes": "",
            "created_at": now_iso(),
            "updated_at": now_iso()
        }
        records.append(slide_rec)
    existing = load_all()
    existing.extend(records)
    save_all(existing)
    print(json.dumps({"ok": True, "deck_id": deck_id, "template": apply_name, "slides": len(tpl["slides"])}, indent=2))

def cmd_notes(args):
    p, pos = parse_args(args)
    slide_id = pos[0] if pos else p.get("slide")
    if not slide_id:
        print("ERROR: Slide ID is required", file=sys.stderr)
        sys.exit(1)
    records = load_all()
    text = p.get("set")
    if text:
        found = False
        for r in records:
            if r.get("type") == "slide" and r.get("id") == slide_id:
                r["notes"] = text
                r["updated_at"] = now_iso()
                found = True
                break
        if not found:
            print(f"ERROR: Slide '{slide_id}' not found", file=sys.stderr)
            sys.exit(1)
        save_all(records)
        print(json.dumps({"ok": True, "message": f"Notes set for '{slide_id}'"}, indent=2))
    else:
        slides = find_slides(records, slide_id=slide_id)
        if not slides:
            print(f"ERROR: Slide '{slide_id}' not found", file=sys.stderr)
            sys.exit(1)
        notes = slides[0].get("notes", "")
        if notes:
            print(f"Notes for {slide_id}: {notes}")
        else:
            print(f"No notes for {slide_id}")

cmd = os.environ['__SKILL_CMD']
args = json.loads(os.environ.get('__SKILL_ARGS', '[]'))
fn = {
    "create": cmd_create,
    "add": cmd_add,
    "edit": cmd_edit,
    "reorder": cmd_reorder,
    "theme": cmd_theme,
    "outline": cmd_outline,
    "export": cmd_export,
    "preview": cmd_preview,
    "list": cmd_list,
    "template": cmd_template,
    "notes": cmd_notes,
}
fn[cmd](args)
PYEOF
;;

help)
  show_help
;;

version)
  echo "slide v${VERSION}"
;;

*)
  echo "ERROR: Unknown command '$CMD'. Run 'script.sh help' for usage." >&2
  exit 1
;;

esac
