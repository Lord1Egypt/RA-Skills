#!/usr/bin/env python3
"""Fingerprint repos for listable assets and route them to visibility platforms.

Usage:
  scan.py [root ...] [--have a,b] [--json]   one report per root on stdout
  scan.py --check                            catalog consistency

Assets a file can prove are detected here; the rest (a live remote MCP URL, a domain you
control, a test account) come from --have, which the plan skill fills after asking.
The catalog lives in ../catalog.json; every platform fact has its home there.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(os.path.dirname(HERE), "catalog.json")
RECIPES = os.path.join(os.path.dirname(os.path.dirname(HERE)), "build", "recipes")
SKIP = re.compile(r"(^|/)(node_modules|vendor|Pods|build|dist|\.build|DerivedData|\.dart_tool|\.next|target"
                  r"|\.venv|venv|__pycache__|\.git|\.audit|\.visibility|_archive|_worktrees"
                  r"|tests?|__tests__|fixtures?|__fixtures__|testdata)(/|$)")  # a fixture is not the product's asset
BUILD_OUTPUT = {"build", "dist", "target"}  # skipped as build output unless git tracks files in them (skills/build)
MAX_FILES = 20_000

# asset -> (how it is known, description). "ask" assets are never detected, only declared with --have.
ASSETS = {
    "github-public":  ("detect", "public GitHub repo (checked with gh)"),
    "skill-md":       ("detect", "an Agent Skill (SKILL.md)"),
    "claude-plugin":  ("detect", "a Claude Code plugin (.claude-plugin/plugin.json)"),
    "mcp-server":     ("detect", "MCP server code (MCP SDK dependency or server.json)"),
    "openapi":        ("detect", "an OpenAPI/Swagger file"),
    "npm-package":    ("detect", "a publishable npm package (package.json, not private)"),
    "npm-cli":        ("detect", "an npm CLI (package.json bin)"),
    "pypi-package":   ("detect", "a publishable Python package (pyproject [project])"),
    "browser-ext":    ("detect", "a browser extension (manifest.json with manifest_version)"),
    "vscode-ext":     ("detect", "a VS Code extension (package.json engines.vscode)"),
    "raycast-ext":    ("detect", "a Raycast extension (@raycast/api)"),
    "obsidian-plugin": ("detect", "an Obsidian plugin (manifest.json with minAppVersion)"),
    "github-action":  ("detect", "a GitHub Action (action.yml at the root)"),
    "llms-txt":       ("detect", "an llms.txt file"),
    "ios-app":        ("detect", "an iOS/macOS app (.xcodeproj)"),
    "dockerfile":     ("detect", "a Dockerfile"),
    "rust-crate":     ("detect", "a Rust crate (Cargo.toml [package])"),
    "jetbrains-plugin": ("detect", "a JetBrains plugin (META-INF/plugin.xml)"),
    "figma-plugin":   ("detect", "a Figma plugin (manifest.json with editorType)"),
    "wordpress-plugin": ("detect", "a WordPress plugin (PHP 'Plugin Name:' header)"),
    "cursor-plugin":   ("detect", "a Cursor plugin (.cursor-plugin/plugin.json)"),
    "zed-extension":   ("detect", "a Zed extension (extension.toml)"),
    "kiro-power":      ("detect", "a Kiro power (POWER.md; a plugin.json-format power is declared with --have)"),
    "teams-app":       ("detect", "a Microsoft Teams app (manifest.json with the MicrosoftTeams $schema)"),
    "power-connector":  ("detect", "a Power Platform custom connector (apiDefinition.swagger.json + apiProperties.json)"),
    "forge-app":       ("detect", "an Atlassian Forge app (manifest.yml with app.id / modules)"),
    "workspace-addon":  ("detect", "a Google Workspace add-on (appsscript.json with addOns)"),
    "canva-app":       ("detect", "a Canva app (@canva/app-ui-kit or @canva/platform dependency)"),
    "framer-plugin":   ("detect", "a Framer plugin (framer-plugin dependency)"),
    "webflow-app":     ("detect", "a Webflow Designer Extension (webflow.json / @webflow/designer-extension-typings)"),
    "apify-actor":     ("detect", "an Apify Actor (.actor/actor.json)"),
    "jsr-package":     ("detect", "a JSR package (jsr.json)"),
    "slack-app":      ("ask", "a Slack app with real installs (10+ workspaces or 20+ MAU)"),
    "discord-app":    ("ask", "a verified Discord app"),
    "shopify-app":    ("ask", "a Shopify app"),
    "alfred-workflow": ("ask", "an Alfred workflow with real users"),
    "mcp-remote":     ("ask", "a live remote (Streamable HTTP) MCP server URL"),
    "mcp-oauth":      ("ask", "that remote MCP server supports OAuth"),
    "public-api":     ("ask", "a public HTTP API customers call with their own API key"),
    "own-domain":     ("ask", "a domain whose DNS you control"),
    "docs-site":      ("ask", "docs published on your own domain"),
    "website":        ("ask", "a live product website"),
    "test-account":   ("ask", "a test account you can hand reviewers"),
    "demo-video":     ("ask", "a short uncut demo video"),
    "claude-paid":    ("ask", "a paid claude.ai plan (directory portal access)"),
    "apple-dev":      ("ask", "an Apple Developer Program membership"),
}
EFFORT = {"minutes": 1, "hours": 2, "days": 4, "weeks": 8}
# AGENTS.md: accounts, payment, credentials and form submission are always human: steps. Words after "/" are URL paths.
HUMAN_ONLY = re.compile(r"(?<![/\w-])(sign[ -]?in|log[ -]?in|submit|pay|token|password|credentials?|portal"
                        r"|partner center)(?![\w-])", re.I)
REQUIRED = ("id", "name", "category", "submit", "requires", "cost", "review", "link", "effort", "source", "verified")


def read(path, limit=200_000):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except OSError:
        return ""


def recipes():
    """Ids (asset or platform) that have a build recipe in ../../build/recipes/<id>.md."""
    try:
        return {f[:-3] for f in os.listdir(RECIPES) if f.endswith(".md")}
    except OSError:
        return set()


def load_catalog():
    with open(CATALOG, encoding="utf-8") as f:
        return json.load(f)["platforms"]


def tracked_dirs(root):
    """Folders (relative to root) that hold files git tracks; empty outside a repo."""
    try:
        out = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return set()
    return {f[:i] for f in out.split("\0") for i, c in enumerate(f) if c == "/"}


def walk(root):
    """(relative path, full path) per file, then ("", None) once if MAX_FILES cut the walk short."""
    n, tracked = 0, tracked_dirs(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        here = "" if rel == "." else rel + "/"
        dirnames[:] = [d for d in dirnames
                       if not SKIP.search(d) or (d in BUILD_OUTPUT and here + d in tracked)]
        for d in dirnames:
            if d.endswith(".xcodeproj"):
                yield ("" if rel == "." else rel + "/") + d, None
        for name in filenames:
            n += 1
            if n > MAX_FILES:  # shortcut: huge monorepos are sampled, not walked; raise MAX_FILES if a real one needs it
                yield "", None
                return
            yield ("" if rel == "." else rel + "/") + name, os.path.join(dirpath, name)


def detect(root):
    """Assets a file in root proves, each with the file that proved it."""
    found = {}

    def hit(asset, why):
        found.setdefault(asset, why)

    for rel, path in walk(root):
        base = rel.rsplit("/", 1)[-1]
        if not rel:
            found["truncated"] = f"stopped after {MAX_FILES} files; assets in the rest of the tree were not looked for"
        elif rel.endswith(".xcodeproj"):
            hit("ios-app", rel)
        elif base == "SKILL.md":
            if re.match(r"---\n(.*\n)*?name:.*\n(.*\n)*?---", read(path, 8192)):  # a skill has frontmatter with a name
                hit("skill-md", rel)
        elif rel.endswith(".claude-plugin/plugin.json"):
            hit("claude-plugin", rel)
        elif base == "server.json" and "modelcontextprotocol" in read(path):
            hit("mcp-server", rel)
        elif re.fullmatch(r"(openapi|swagger)[\w.-]*\.(json|ya?ml)", base, re.I):
            hit("openapi", rel)
        elif base == "Dockerfile":
            hit("dockerfile", rel)
        elif base == "Cargo.toml" and "[package]" in read(path):
            hit("rust-crate", rel)
        elif rel.endswith("META-INF/plugin.xml"):
            hit("jetbrains-plugin", rel)
        elif base.endswith(".php") and "/" not in rel and re.search(r"^\s*\*?\s*Plugin Name:", read(path, 8192), re.M):
            hit("wordpress-plugin", rel)
        elif rel.endswith(".cursor-plugin/plugin.json"):
            hit("cursor-plugin", rel)
        elif rel.endswith(".actor/actor.json"):
            hit("apify-actor", rel)
        elif base == "extension.toml":
            hit("zed-extension", rel)
        elif base == "POWER.md":
            hit("kiro-power", rel)
        elif base == "apiProperties.json":
            hit("power-connector", rel)
        elif base == "manifest.yml" and re.search(r"^app:", read(path), re.M) and re.search(r"^modules:", read(path), re.M):
            hit("forge-app", rel)
        elif base == "appsscript.json" and '"addOns"' in read(path):
            hit("workspace-addon", rel)
        elif base == "webflow.json":
            hit("webflow-app", rel)
        elif base == "jsr.json":
            hit("jsr-package", rel)
        elif base == "llms.txt":
            hit("llms-txt", rel)
        elif rel in ("action.yml", "action.yaml"):
            hit("github-action", rel)
        elif base == "manifest.json":
            text = read(path)
            if "MicrosoftTeams" in text:
                hit("teams-app", rel)
            elif '"manifest_version"' in text:
                hit("browser-ext", rel)
            elif '"minAppVersion"' in text:
                hit("obsidian-plugin", rel)
            elif '"editorType"' in text:
                hit("figma-plugin", rel)
        elif base == "package.json":
            try:
                pkg = json.loads(read(path))
            except ValueError:
                continue
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "@modelcontextprotocol/sdk" in deps or "fastmcp" in deps:
                hit("mcp-server", rel)
            if "@canva/app-ui-kit" in deps or "@canva/platform" in deps:
                hit("canva-app", rel)
            if "framer-plugin" in deps:
                hit("framer-plugin", rel)
            if "@webflow/designer-extension-typings" in deps:
                hit("webflow-app", rel)
            if "@raycast/api" in deps:
                hit("raycast-ext", rel)
            if "vscode" in pkg.get("engines", {}):
                hit("vscode-ext", rel)
            if not pkg.get("private") and pkg.get("name"):
                hit("npm-package", rel)
                if pkg.get("bin"):
                    hit("npm-cli", rel)
        elif base == "pyproject.toml":
            text = read(path)
            if re.search(r"^\[project\]", text, re.M):
                hit("pypi-package", rel)
            if re.search(r"""["'](mcp|fastmcp)[\[>=<~" ']""", text):
                hit("mcp-server", rel)
        elif base.startswith("requirements") and base.endswith(".txt"):
            if re.search(r"^(mcp|fastmcp)\b", read(path), re.M):
                hit("mcp-server", rel)
    try:
        origin = subprocess.run(["git", "-C", root, "remote", "get-url", "origin"],
                                capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        origin = ""
    if "github.com" in origin:
        try:  # a github.com remote may be private; only gh can tell
            private = subprocess.run(["gh", "repo", "view", origin, "--json", "isPrivate", "-q", ".isPrivate"],
                                     capture_output=True, text=True, timeout=10).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            private = ""
        if private == "false":
            hit("github-public", origin)
        else:
            found["github-remote"] = f"{origin} (private or unknown; not counted as public)"
    return found


def route(have, catalog):
    """Split the catalog into eligible rows, rows one asset away, and the rest."""
    eligible, near, far = [], [], []
    for p in catalog:
        missing = [a for a in p["requires"] if not set(a.split("|")) & have]  # "a|b" = either asset
        (eligible if not missing else near if len(missing) == 1 else far).append((p, missing))
    # rows with a claimed DR first, by DR over effort; rows with none after them, by effort: an unknown is not a 50
    effort = lambda p: EFFORT.get(p["effort"], 4)
    eligible.sort(key=lambda pm: (not pm[0].get("dr"), -(pm[0].get("dr") or 0) / effort(pm[0]), effort(pm[0])))
    unlocks = {}
    for p, missing in near:
        unlocks.setdefault(missing[0], []).append(p)
    ranked = sorted(unlocks.items(), key=lambda kv: (-sum(p.get("dr") or 0 for p in kv[1]), -len(kv[1])))
    return eligible, ranked, far


def report(root, have_extra, catalog):
    found = detect(root)
    have = set(found) | set(have_extra)
    eligible, unlocks, far = route(have, catalog)
    out = [f"# {os.path.basename(os.path.abspath(root))}", "", "## Assets", ""]
    truncated = found.pop("truncated", None)
    if truncated:
        out += [f"Incomplete scan: {truncated}.", ""]
    if "github-remote" in found:
        out.append(f"- [ ] `github-public`: {found.pop('github-remote')}")
    for a, (kind, desc) in ASSETS.items():
        if a in found:
            out.append(f"- [x] `{a}`: {desc} ({found[a]})")
        elif a in have_extra:
            out.append(f"- [x] `{a}`: {desc} (declared)")
        elif kind == "ask":
            out.append(f"- [ ] `{a}`: {desc} (ask)")
    listed = [(p, m) for p, m in eligible if p["category"] != "monetize"]
    earn = [(p, m) for p, m in eligible if p["category"] == "monetize"]
    out += ["", f"## Eligible now ({len(listed)})", "",
            "| Platform | DR (claimed) | Effort | Cost | Link | Verified |", "|---|---|---|---|---|---|"]
    for p, _ in listed:
        out.append(f"| `{p['id']}` {p['name']} | {p.get('dr') or 'unknown'} | {p['effort']} | {p['cost']} "
                   f"| {p['link']} | {p['verified']} |")
    out += ["", f"## Earn now ({len(earn)})", "", "| Channel | Revenue | Effort | Verified |", "|---|---|---|---|"]
    for p, _ in earn:
        out.append(f"| `{p['id']}` {p['name']} | {p['revenue']} | {p['effort']} | {p['verified']} |")
    have_recipe = recipes()
    out += ["", "## One asset away", ""]
    for asset, ps in unlocks:
        built = sorted(set(asset.split("|")) & have_recipe)
        hint = f" (recipe: `/visibility:build {built[0]}`)" if built else ""
        out.append(f"- `{asset}` unlocks {len(ps)}{hint}: " + ", ".join(f"`{p['id']}`" for p in ps))
    out += ["", f"## Two or more assets away: {len(far)}", ""]
    return "\n".join(out), {"root": root, "assets": {k: v for k, v in found.items() if k in ASSETS}, "declared": sorted(have_extra), "truncated": bool(truncated),
                            "eligible": [p["id"] for p, _ in listed], "earn": [p["id"] for p, _ in earn],
                            "unlocks": {a: [p["id"] for p in ps] for a, ps in unlocks}}


def check(catalog):
    errors, ids = [], set()
    for i, p in enumerate(catalog):
        where = p.get("id", f"row {i}")
        errors += [f"{where}: missing {k}" for k in REQUIRED if k not in p]
        if p.get("id") in ids:
            errors.append(f"{where}: duplicate id")
        ids.add(p.get("id"))
        errors += [f"{where}: unknown asset {a}" for r in p.get("requires", []) for a in r.split("|") if a not in ASSETS]
        if p.get("effort") not in EFFORT:
            errors.append(f"{where}: effort must be one of {', '.join(EFFORT)}")
        if p.get("verified") not in ("yes", "flow", "no"):
            errors.append(f"{where}: verified must be yes, flow or no")
        if p.get("verified") == "yes" and str(p.get("link", "")).startswith("unchecked"):
            errors.append(f"{where}: verified is yes but link is unchecked; use flow until the listing's link is observed")
        if p.get("category") == "monetize" and not p.get("revenue"):
            errors.append(f"{where}: monetize rows need revenue (fee, rev share, payout minimum)")
        if not (p.get("steps") or p.get("see")):
            errors.append(f"{where}: needs steps or a see pointer")
        for s in p.get("steps", []):
            if not re.match(r"^(claude|human|approve): ", s):
                errors.append(f"{where}: step must start with claude:/human:/approve: -> {s[:40]}")
            elif not s.startswith("human:") and HUMAN_ONLY.search(s):
                errors.append(f"{where}: '{HUMAN_ONLY.search(s).group(0)}' in a {s.split(':')[0]}: step; signing in, "
                              f"submitting, paying and handling credentials are human: steps -> {s[:60]}")
    ids |= set(ASSETS)
    errors += [f"recipes/{r}.md: not an asset or platform id" for r in sorted(recipes() - ids)]
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("roots", nargs="*", default=["."])
    ap.add_argument("--have", default="", help="comma-separated assets confirmed by asking")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    catalog = load_catalog()
    if a.check:
        errors = check(catalog)
        print("\n".join(errors) or f"ok: {len(catalog)} platforms, {len(recipes())} recipes")
        return 1 if errors else 0
    have = {x.strip() for x in a.have.split(",") if x.strip()}
    bad = have - set(ASSETS)
    if bad:
        sys.exit(f"unknown asset(s): {', '.join(sorted(bad))}; known: {', '.join(ASSETS)}")
    missing = [r for r in a.roots if not os.path.isdir(r)]
    if missing:
        ap.error(f"not a directory: {', '.join(missing)}")  # exits 2: a mistyped path is not a project with no assets
    results = [report(r, have, catalog) for r in a.roots]
    if a.json:
        print(json.dumps([j for _, j in results], indent=2))
    else:
        print("\n\n".join(md for md, _ in results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
