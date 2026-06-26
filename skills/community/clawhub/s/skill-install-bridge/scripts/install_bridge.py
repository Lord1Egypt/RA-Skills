#!/usr/bin/env python3
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import quote


def main():
    parser = argparse.ArgumentParser(description="Generate install snippets for a published skill.")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--name")
    parser.add_argument("--owner", default="zack-dev-cm")
    parser.add_argument("--version")
    parser.add_argument("--description")
    parser.add_argument("--url")
    parser.add_argument("--out-dir", default="install-bridge")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output files")
    args = parser.parse_args()

    bridge = build_bridge(args)
    out_dir = Path(args.out_dir).resolve()
    write(out_dir / "install-bridge.json", json.dumps(bridge, indent=2) + "\n", force=args.force)
    write(out_dir / "README-snippet.md", render_markdown(bridge), force=args.force)
    write(out_dir / "landing-card.html", render_html(bridge), force=args.force)
    write(out_dir / "social-post.txt", render_social(bridge), force=args.force)
    print(json.dumps(bridge, indent=2))


def build_bridge(args):
    slug = str(args.slug).strip()
    if not re.match(r"^[a-z0-9][a-z0-9-]{1,78}[a-z0-9]$", slug):
        raise SystemExit("Slug must be lower-case letters, numbers, and hyphens.")
    owner = safe_handle(args.owner)
    name = safe_text(args.name or title_from_slug(slug), 80)
    version = safe_text(args.version or "latest", 32)
    url = safe_url(args.url or f"https://clawhub.ai/{owner}/{slug}")
    command = f"npx --yes clawhub@0.9.0 install {slug}"
    return {
        "slug": slug,
        "name": name,
        "owner": owner,
        "version": version,
        "url": url,
        "description": safe_text(args.description or "Install this skill from ClawHub and use it in your agent workflow.", 180),
        "installCommand": command,
        "usagePrompt": f"Use ${slug} for this task.",
    }


def render_markdown(bridge):
    name = markdown_text(bridge["name"])
    url = markdown_destination(bridge["url"])
    return f'''## Install {name}

```bash
{bridge["installCommand"]}
```

Open: [{name}]({url})

After install, ask your agent:

```text
{bridge["usagePrompt"]}
```
'''


def render_html(bridge):
    name = escape(bridge["name"])
    description = escape(bridge["description"])
    command = escape(bridge["installCommand"])
    url = escape(bridge["url"])
    return f'''<section class="skill-install-card" style="border:1px solid #d7ded2;border-radius:8px;padding:18px;max-width:560px;font-family:Inter,system-ui,sans-serif;background:#f8faf6;color:#121417">
  <p style="margin:0 0 6px;font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:#4d35a3">ClawHub Skill</p>
  <h2 style="margin:0 0 8px;font-size:24px;line-height:1.15">{name}</h2>
  <p style="margin:0 0 14px;font-size:15px;line-height:1.45">{description}</p>
  <pre style="white-space:pre-wrap;margin:0 0 14px;padding:12px;border-radius:6px;background:#121417;color:#f8faf6;font-size:13px;overflow:auto"><code>{command}</code></pre>
  <a href="{url}" style="display:inline-block;color:#121417;font-weight:800;text-decoration:underline">View skill</a>
</section>
'''


def render_social(bridge):
    return f'''I shipped {bridge["name"]}.

Install:
{bridge["installCommand"]}

Use it with:
{bridge["usagePrompt"]}

{bridge["url"]}
'''


def title_from_slug(slug):
    return " ".join(part.capitalize() for part in slug.split("-"))


def safe_text(value, limit):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def safe_handle(value):
    text = str(value or "").strip()
    if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,48}$", text):
        raise SystemExit("Owner handle is invalid.")
    return text


def safe_url(value):
    text = str(value or "").strip()
    if not re.match(r"^https://[^\s<>]+$", text):
        raise SystemExit("URL must be HTTPS.")
    return text


def markdown_text(value):
    text = html.escape(str(value), quote=False)
    return re.sub(r"([\\\[\]`*_{}()#+.!|>\-])", r"\\\1", text)


def markdown_destination(value):
    text = str(value or "").strip()
    if not text:
        return ""
    return quote(text, safe="/:#?&=%@+.,;~_-")


def escape(value):
    return html.escape(str(value), quote=True)


def write(path, text, force=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
