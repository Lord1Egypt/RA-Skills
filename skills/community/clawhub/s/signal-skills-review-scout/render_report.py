#!/usr/bin/env python3
"""Render a findings payload into the signal-report template.

Owns the mechanical part of report generation: HTML/CSS boilerplate,
per-tier and per-item markup repetition, escaping, and the hard style
rules (no em dashes, valid confidence classes). Callers (this skill,
`podcast`, or any future one) supply only content: headline, tiers,
items, reasoning. The template's CSS/token structure is never touched
here beyond a single title substitution, so a bad payload cannot corrupt
the light/dark theme blocks.

Usage:
    python3 render_report.py payload.json output.html
    python3 render_report.py payload.json output.md      # plain-text/markdown
        # instead of HTML, picked by the output file's extension (.md/.txt ->
        # text, anything else -> HTML). Same payload, same validation, no
        # separate schema. This is the actionable-copy-paste form: headline,
        # tiers, and every item's claim/tag/reasoning/source as Markdown you
        # can paste into a prompt, ticket, or chat message, not just view as
        # a rendered report.
    python3 render_report.py payload.json output.html output.md   # both at once
    cat payload.json | python3 render_report.py - output.html
    python3 render_report.py payload.json output.html --open   # also opens
        # the result in the local default browser (webbrowser stdlib module,
        # cross-platform). Use this on any harness without an Artifact-style
        # publish tool (OpenCode, Codex CLI, plain terminal). Only applies to
        # an .html output target; ignored for .md/.txt targets.

Payload schema (JSON):
{
  "title": "<title>",
  "eyebrow": "<source scope + date>",
  "headline": "<answer-framed headline>",
  "query": "<one-sentence restatement of the query>",
  "tiers": [
    {
      "label": "<short tier meaning, e.g. 'Ship before the deadline'>",
      "name": "<tier display name>",
      "rank": 5,       // filled bars, 1-5
      "of": 5,          // total bars, usually 5
      "color": "sig",   // sig | mid | alert | off
      "items": [
        {
          "claim": "<the finding, stated plainly>",
          "tag": "confirmed twice",     // display text
          "tag_class": "sig",           // sig | mid | alert | off
          "reasoning": "<why it matters here>",
          "source": "<episode/doc + date>"
        }
      ]
    }
  ],
  "footer_left": "<source manifest / transcript path>",
  "footer_right": "<ledger / state path>"
}
"""
import html
import json
import re
import sys
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "template.html"
VALID_COLORS = {"sig", "mid", "alert", "off"}
CONFIDENCE_RANK = {"sig": 0, "mid": 1, "alert": 2, "off": 2}
EM_DASH_FIELDS_ERROR = (
    "Em dash found in field '{field}': {value!r}. "
    "Use a period, colon, comma, or parentheses instead."
)

# Filter/sort toolbar: control-bar markup + the script that drives it, both
# generic across any report this template produces. Ported from the
# 2026-07-23 podcast-mining artifact where this was first built and proven
# out by hand before being folded back in here so future reports get it by
# default instead of needing to be hand-built per report.
FILTER_SCRIPT = """<script>
(function() {
  var itemSelector = '.item[data-tier], .skip-line[data-tier]';
  var allNodes = Array.prototype.slice.call(document.querySelectorAll(itemSelector));
  if (!allNodes.length) return;

  document.querySelectorAll('.item-list, .skip-block').forEach(function(container) {
    Array.prototype.slice.call(container.children).forEach(function(kid, i) {
      if (kid.hasAttribute('data-tier')) kid.setAttribute('data-idx', i);
    });
  });

  allNodes.forEach(function(node) {
    var topic = node.getAttribute('data-topic');
    var show = node.getAttribute('data-show');
    if (topic) {
      var pill = document.createElement('button');
      pill.type = 'button';
      pill.className = 'topic-pill';
      pill.textContent = topic;
      pill.setAttribute('data-pill-topic', topic);
      if (node.classList.contains('item')) {
        var top = node.querySelector('.item-top');
        if (top) top.appendChild(pill);
      } else {
        var srcInline = node.querySelector('.src-inline');
        if (srcInline) srcInline.insertAdjacentElement('afterend', pill);
        else node.appendChild(pill);
      }
    }
    if (show && node.classList.contains('item')) {
      var srcB = node.querySelector('.src b');
      if (srcB) {
        srcB.classList.add('show-link');
        srcB.setAttribute('data-link-show', show);
      }
    }
  });

  document.addEventListener('click', function(e) {
    var pill = e.target.closest && e.target.closest('.topic-pill');
    if (pill) {
      topicSel.value = pill.getAttribute('data-pill-topic');
      applyFilters();
      return;
    }
    var showLink = e.target.closest && e.target.closest('.show-link');
    if (showLink) {
      showSel.value = showLink.getAttribute('data-link-show');
      applyFilters();
    }
  });

  var shows = Array.from(new Set(allNodes.map(function(n){ return n.getAttribute('data-show'); }).filter(Boolean))).sort();
  var topics = Array.from(new Set(allNodes.map(function(n){ return n.getAttribute('data-topic'); }).filter(Boolean))).sort();
  var showSel = document.getElementById('show-filter');
  var topicSel = document.getElementById('topic-filter');
  shows.forEach(function(s) {
    var o = document.createElement('option'); o.value = s; o.textContent = s; showSel.appendChild(o);
  });
  topics.forEach(function(t) {
    var o = document.createElement('option'); o.value = t; o.textContent = t; topicSel.appendChild(o);
  });

  var activeTiers = {};
  document.querySelectorAll('#tier-chips .chip').forEach(function(c) {
    activeTiers[c.getAttribute('data-chip-tier')] = true;
  });
  var sortSel = document.getElementById('sort-mode');
  var counter = document.getElementById('result-count');

  function applyFilters() {
    var showVal = showSel.value;
    var topicVal = topicSel.value;
    var visibleCount = 0;
    allNodes.forEach(function(node) {
      var match = activeTiers[node.getAttribute('data-tier')] &&
                  (!showVal || node.getAttribute('data-show') === showVal) &&
                  (!topicVal || node.getAttribute('data-topic') === topicVal);
      node.classList.toggle('is-hidden', !match);
      if (match) visibleCount++;
    });

    document.querySelectorAll('details.show-group').forEach(function(grp) {
      var visible = grp.querySelectorAll('.item:not(.is-hidden), .skip-line:not(.is-hidden)').length;
      grp.classList.toggle('is-hidden', visible === 0);
    });

    document.querySelectorAll('.tier-head[data-tier-key]').forEach(function(head) {
      var key = head.getAttribute('data-tier-key');
      var anyVisible = false;
      var el = head.nextElementSibling;
      while (el && !(el.classList.contains('tier-head') && el.hasAttribute('data-tier-key'))) {
        if (el.querySelectorAll && el.querySelectorAll('.item:not(.is-hidden), .skip-line:not(.is-hidden)').length > 0) anyVisible = true;
        el = el.nextElementSibling;
      }
      head.classList.toggle('is-hidden', !activeTiers[key] || !anyVisible);
    });

    if (counter) counter.textContent = 'Showing ' + visibleCount + ' of ' + allNodes.length;
  }

  function applySort() {
    var mode = sortSel.value;
    document.querySelectorAll('.item-list, .skip-block').forEach(function(container) {
      var kids = Array.prototype.slice.call(container.children).filter(function(k){ return k.hasAttribute('data-tier'); });
      if (!kids.length) return;
      kids.sort(function(a, b) {
        if (mode === 'confidence') return (+a.getAttribute('data-confidence')) - (+b.getAttribute('data-confidence'));
        if (mode === 'date-desc') return (b.getAttribute('data-date') || '').localeCompare(a.getAttribute('data-date') || '');
        if (mode === 'date-asc') return (a.getAttribute('data-date') || '').localeCompare(b.getAttribute('data-date') || '');
        return (+a.getAttribute('data-idx')) - (+b.getAttribute('data-idx'));
      });
      kids.forEach(function(k){ container.appendChild(k); });
    });
    applyFilters();
  }

  document.getElementById('tier-chips').addEventListener('click', function(e) {
    var chip = e.target.closest('.chip');
    if (!chip) return;
    var key = chip.getAttribute('data-chip-tier');
    activeTiers[key] = !activeTiers[key];
    chip.classList.toggle('active', activeTiers[key]);
    applyFilters();
  });
  showSel.addEventListener('change', applyFilters);
  topicSel.addEventListener('change', applyFilters);
  sortSel.addEventListener('change', applySort);
  document.getElementById('reset-filters').addEventListener('click', function() {
    Object.keys(activeTiers).forEach(function(k){ activeTiers[k] = true; });
    document.querySelectorAll('#tier-chips .chip').forEach(function(c){ c.classList.add('active'); });
    showSel.value = '';
    topicSel.value = '';
    sortSel.value = 'default';
    applySort();
  });

  applyFilters();
})();
</script>
"""


def slugify_key(text, fallback):
    slug = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return slug or fallback


class PayloadError(ValueError):
    pass


def check_no_em_dash(value, field):
    if isinstance(value, str) and "—" in value:
        raise PayloadError(EM_DASH_FIELDS_ERROR.format(field=field, value=value))


def esc(value):
    return html.escape(str(value), quote=True)


def render_bars(rank, of, color):
    if not (1 <= rank <= of):
        raise PayloadError(f"tier bar rank {rank} out of range for 'of' {of}")
    filled = "".join('<i class="on"></i>' for _ in range(rank))
    empty = "".join("<i></i>" for _ in range(of - rank))
    return (
        f'<div class="bars" style="--bar-color: var(--{esc(color)})">'
        f"{filled}{empty}</div>"
    )


def validate_item(item, tier_index, item_index):
    for field in ("claim", "tag", "reasoning", "source"):
        if field not in item:
            raise PayloadError(f"tier {tier_index} item {item_index} missing '{field}'")
        check_no_em_dash(item[field], f"tiers[{tier_index}].items[{item_index}].{field}")
    tag_class = item.get("tag_class", "sig")
    if tag_class not in VALID_COLORS:
        raise PayloadError(
            f"tier {tier_index} item {item_index} invalid tag_class {tag_class!r}"
        )
    border_color = item.get("border_color", tag_class)
    if border_color not in VALID_COLORS:
        raise PayloadError(
            f"tier {tier_index} item {item_index} invalid border_color {border_color!r}"
        )


def validate_tier(tier, tier_index):
    for field in ("label", "name", "items"):
        if field not in tier:
            raise PayloadError(f"tier {tier_index} missing '{field}'")
    check_no_em_dash(tier["label"], f"tiers[{tier_index}].label")
    check_no_em_dash(tier["name"], f"tiers[{tier_index}].name")
    if not tier["items"]:
        raise PayloadError(
            f"tier {tier_index} ({tier['name']!r}) has zero items; "
            "drop the tier from the payload instead of rendering it empty"
        )
    color = tier.get("color", "sig")
    if color not in VALID_COLORS:
        raise PayloadError(f"tier {tier_index} invalid color {color!r}")
    for i, item in enumerate(tier["items"]):
        validate_item(item, tier_index, i)


def validate_payload(payload):
    for field in ("title", "eyebrow", "headline", "query", "tiers"):
        if field not in payload:
            raise PayloadError(f"payload missing required field '{field}'")
    for field in ("title", "eyebrow", "headline", "query"):
        check_no_em_dash(payload[field], field)
    if not payload["tiers"]:
        raise PayloadError("payload has zero tiers")
    for i, tier in enumerate(payload["tiers"]):
        validate_tier(tier, i)


def render_item(item):
    tag_class = item.get("tag_class", "sig")
    border_color = item.get("border_color", tag_class)
    return f"""    <div class="item" style="border-left-color: var(--{border_color})">
      <div class="item-top">
        <h3>{esc(item['claim'])}</h3>
        <span class="tag {tag_class}">{esc(item['tag'])}</span>
      </div>
      <p>{esc(item['reasoning'])}</p>
      <div class="src">{esc(item['source'])}</div>
    </div>"""


def render_tier(tier):
    color = tier.get("color", "sig")
    rank = tier.get("rank", len(tier["items"]))
    of = tier.get("of", 5)
    bars = render_bars(rank, of, color)
    items_html = "\n".join(render_item(item) for item in tier["items"])
    return f"""  <div class="tier-head">
    {bars}
    <div class="titles">
      <div class="label">{esc(tier['label'])}</div>
      <h2 class="name">{esc(tier['name'])}</h2>
    </div>
  </div>
  <div class="item-list">
{items_html}
  </div>"""


def render(payload):
    validate_payload(payload)

    template = TEMPLATE_PATH.read_text()
    head, _, _ = template.partition('<div class="wrap">')
    head = head.replace("REPLACE_TITLE", esc(payload["title"]), 1)

    tiers_html = "\n\n".join(render_tier(tier) for tier in payload["tiers"])

    footer_left = esc(payload.get("footer_left", ""))
    footer_right = esc(payload.get("footer_right", ""))

    wrap = f"""<div class="wrap">
  <p class="eyebrow">{esc(payload['eyebrow'])}</p>
  <h1>{esc(payload['headline'])}</h1>
  <p class="query">{esc(payload['query'])}</p>

{tiers_html}

  <footer>
    <span>{footer_left}</span>
    <span>{footer_right}</span>
  </footer>
</div>
"""
    return head + wrap


TEXT_EXTENSIONS = {".md", ".markdown", ".txt"}


def render_item_text(item):
    lines = [f"- **{item['claim']}** _{item['tag']}_", f"  {item['reasoning']}"]
    lines.append(f"  Source: {item['source']}")
    return "\n".join(lines)


def render_tier_text(tier):
    lines = [f"## {tier['name']}", f"*{tier['label']}*", ""]
    lines.extend(render_item_text(item) for item in tier["items"])
    return "\n".join(lines)


def render_text(payload):
    """Actionable plain-text/Markdown form of the same payload rendered by
    `render()` — for pasting into a prompt, a ticket, a chat message, or
    feeding to another agent, where an HTML Artifact isn't the right shape.
    Same validation, same content, just no HTML/CSS."""
    validate_payload(payload)

    lines = [
        f"# {payload['headline']}",
        "",
        f"_{payload['eyebrow']}_",
        "",
        payload["query"],
        "",
    ]
    for tier in payload["tiers"]:
        lines.append(render_tier_text(tier))
        lines.append("")

    footer_left = payload.get("footer_left", "")
    footer_right = payload.get("footer_right", "")
    if footer_left or footer_right:
        lines.append("---")
        lines.append(" | ".join(p for p in (footer_left, footer_right) if p))

    return "\n".join(lines).rstrip() + "\n"


def render_to(payload, dst: Path):
    if dst.suffix.lower() in TEXT_EXTENSIONS:
        return render_text(payload)
    return render(payload)


def main():
    args = [a for a in sys.argv[1:] if a != "--open"]
    should_open = "--open" in sys.argv[1:]
    if len(args) < 2:
        print(
            f"usage: {sys.argv[0]} <payload.json|-> <output.html> [output.md ...] [--open]",
            file=sys.stderr,
        )
        sys.exit(2)

    src, *dests = args
    raw = sys.stdin.read() if src == "-" else Path(src).read_text()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"invalid JSON payload: {e}", file=sys.stderr)
        sys.exit(1)

    opened = False
    for dest in dests:
        dst = Path(dest)
        try:
            output = render_to(payload, dst)
        except PayloadError as e:
            print(f"payload error: {e}", file=sys.stderr)
            sys.exit(1)

        dst.write_text(output)
        print(f"wrote {dst} ({len(output)} bytes, {len(payload['tiers'])} tiers)")

        if should_open and not opened and dst.suffix.lower() not in TEXT_EXTENSIONS:
            # Platform-agnostic local preview: no Artifact tool required,
            # works under any harness (OpenCode, Codex CLI, plain terminal)
            # as long as a default browser exists on the machine.
            import webbrowser

            webbrowser.open(dst.resolve().as_uri())
            opened = True


if __name__ == "__main__":
    main()
