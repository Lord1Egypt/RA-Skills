---
spec: usk/3.0
id: seal-workflow-licensing-en
version: 1.3.0
name: Seal and License Workflows or Skill Packages (Anti-Piracy, Node-Authorized Delivery)
description: "For script sales and local delivery scenarios — seal Python script collections into source-bound local packages. Scripts keep their original code (import / relative paths / subprocess all supported); MGC 1.5.4 auto-routes through sealed execution. Double-layer encryption plus link authorization binds the source node, supporting single-node licensing and free-mode public distribution. Zero cloud, zero exposure."
author: MirginCipher Team
license: MIT
tags: anti-piracy, encrypted-delivery, zero-exposure, workflow-licensing, local-delivery, node-authorized, free-mode-distribution, link-authorization, sealed-cross-script, auto-recognized-workflow, script-sales, small-system-delivery, knowledge-products, mgc, blackbox
platform_compatibility: windows, macos, linux
mcp_tools: mgc_save, mgc_save_file, mgc_get, mgc_run, mgc_find, mgc_list, mgc_seal, mgc_seal_package, mgc_package, mgc_delete, mgc_open_webui, mgc_skill
requirements:
  mgc_version: ">=1.5.4"
install: pip install mgc-blackbox>=1.5.4
runtime: mgc
port: 57219
files:
  example_dir: example/
changelog:
  - version: 1.3.0
    changes:
      - Upgraded to MGC 1.5.4: sealing mechanism switched to double-layer encryption (ext09 mode field + ext07 source binding)
      - Rewrote Selling point 2: from single-layer RSA binding to double-layer encryption + link authorization, and documented free mode (omit ext04)
      - Added free-mode public distribution scenario (skill marketplace / public demo)
      - Added output_dir to every sealing example (required from 1.5.4, no desktop fallback) and documented the artifact directory layout
      - Corrected recognizable cross-script scope: same-package cross-subdirectory references supported from 1.5.4; added computed absolute-path subprocess
      - Added ext10 runtime compatibility badge and fatal path check guidance
      - Added error codes AMBIGUOUS_SCRIPT / NO_SCRIPT_TO_SEAL / MULTIPLE_MATCHES / MISSING_REQUIRED_FIELDS
      - Corrected mgc_run params: diff_1 optional, diff_3 is the most reliable way to target a single script
      - Added single-script capsule export and dual-path import (with the same-info_owner overwrite warning)
      - Added a verified 'try free mode with example/' walkthrough (no second node or key exchange needed)
      - Corrected import identity semantics: package records carry their own info_owner; the value passed at import only satisfies the required-field check
      - Normalized wording: de-AI-ified phrasing, security boundary restated as source binding and responsibility attribution
      - mcp_tools extended with mgc_delete and mgc_skill
      - Added tags/keywords: free-mode-distribution, link-authorization, public-distribution
  - version: 1.2.0
    changes:
      - Upgraded to MGC 1.5.2: included ext08 auto-recognition and sealed cross-script import
      - Added market scenario opener (script sales / small system delivery / workflow licensing / knowledge products)
      - Added problem-to-solution map (hardcoded paths, config dependencies, missing libraries, platform incompatibility)
      - Added error code handling (DIFF2_MISMATCH / DEP_MISSING / PLATFORM_INCOMPAT)
      - Rewrote Rule 1: changed from 'forbidden paths' to 'same-package paths auto-sealed'
      - Added tags/keywords: sealed-cross-script, auto-recognized-workflow, script-sales, small-system-delivery, local-delivery, one-key-per-node
  - version: 1.0.0
    changes:
      - Initial release. Based on MGC 1.5.0, introduces sealing & licensing of skill packages / workflow folders
---

# One-liner

**Selling scripts and worrying about forwarding? Seal your Python workflow into a source-bound local package — the authorized node can run it, the source stays encrypted end to end, and the source public key cannot be modified: change one byte and the package is unrestorable. Zero cloud, zero code rewrite.**

---

# Who is this for?

| # | Scenario | Pain point |
|---|----------|------------|
| 1 | **Selling scripts / small tools** — Independent developer writes a data-processing / report / scraper script, wants to sell 100 copies | Fear of unlimited copying and reselling; a regular zip means gifting source |
| 2 | **Delivering internal small systems** — Vendor hands a small system built from scripts to a client | Client gets the source and may modify it or hand it to a third party |
| 3 | **Delivering enterprise automation** — Automation consultant packages a workflow for an enterprise | Each enterprise needs its own license; keys cannot be shared |
| 4 | **Paid knowledge products** — Selling an automation method as a content product | Let users run it, but cannot leak the core method |
| 5 | **Public distribution / skill marketplace** — You want any MGC node to be able to install and run it | You need a universal installer package that names no specific node, while the source stays inside the package |

> Common requirement: **delivery = authorization — one key per authorized recipient, with the source locked inside the package as well.**

---

# Why not a GitHub private repo / SaaS encryption / a license server?

| Have you hit this? | GitHub private repo | SaaS encryption service | License server | **MGC sealed delivery** |
|---|---|---|---|---|
| Customer says "I'll just share it with a colleague", then it spreads | ❌ Fully out of your control | ⚠️ Service-dependent | ⚠️ Service-dependent | ✅ **Node-bound — one extra person cannot run it** |
| Do you need to run and maintain a server, worry about DDoS? | — | — | ❌ Ops cost | ✅ **Fully local, zero ops** |
| Can a third party see the source? | ⚠️ Visible to the platform | ❌ Visible server-side | ⚠️ Implementation-dependent | ✅ **Nobody but you can see it** |
| Does it work offline / on an intranet client? | ❌ | ❌ | ❌ | ✅ **USB / email / intranet, any way** |
| Monthly fee / revenue share | Medium (per seat) | High (per call) | Medium (per server) | ✅ **MGC itself is free — no subscription, no cut** |

---

# Three core selling points

## Selling point 1 — Zero rewrite

Write your workflow as you would normally:

- `from helpers.fetch import get_weather`
- `import config`
- `Path(__file__).parent / "settings.json"`
- `subprocess.run([sys.executable, "helper.py"])`

**MGC 1.5.4 automatically recognizes** these `import` / `relative-path` / `subprocess` relationships. At runtime, execution is routed through sealed execution:

- ✅ Files **never land on the customer's disk**
- ✅ **No path on the customer's machine** can `cat` the source directly
- ✅ **No need to rewrite scripts as API-call patterns**
- ✅ **From 1.5.4, same-package cross-subdirectory references are recognized too** (`from helpers.fetch import ...`, `Path(__file__).resolve().parent.parent / "y.py"`)

> Compared with traditional approaches: traditional schemes require you to rewrite scripts as "call by info_owner", turning 5 lines of calls into 50 lines. MGC 1.5.4 takes over for you.

> 📦 **Bundled example**: this skill ships an `example/` folder with 4 scripts (A/B/C/D) covering every recognizable pattern. Run the example first, then swap in your own workflow.

## Selling point 2 — One key per recipient

**MGC 1.5.4 sealing is double-layer encrypted**: the source public key joins the encrypt/decrypt path.

```
Layer 1: content encrypted with a one-time AES-256-GCM key
Layer 2: the AES key is wrapped with the target node's RSA-2048 public key
Layer 3: the wrapped result is wrapped again with an AES-GCM key derived
         from the author's source_node_pub (AAD = seal mode, ext09)
```

Three fields, three jobs:

| Field | Meaning | Role |
|-------|---------|------|
| `ext03` | The doubly-wrapped ciphertext | Protects both content and key material |
| `ext07` | The **author's** node_pub (plaintext identifier) | Binds the source and derives the outer encryption key |
| `ext09` | Seal mode (`p2p mode` / `free mode`) | Decides whose private key unseals the package |

The direct results:

- In p2p mode, the target node has no matching private key → cannot get the content
- **Modifying `ext07` or `ext09` (even a single space) makes the whole package unrestorable** (link authorization — applies to both p2p and free mode)
- A p2p recipient holds no source key that would let them re-seal onward → cannot hand the original package to a third party

```
Author node                              Customer node
───────────                              ────────────
mgc_save_file(path="./workflow")
mgc_seal_package(ext04=customer_pub,
                 output_dir=...)
        │
        ▼
   encrypted package (.mgc_file)
        │
        └──── any channel ─────►        mgc_save_file(path="./received.mgc_file")
                                     mgc_run(...)
```

## Selling point 3 — Local delivery

- All encryption, decryption, and execution happen **locally**
- MGC connects to no cloud, has no external endpoints
- The encrypted package can be delivered by email, USB, IM, GitHub Releases, private cloud drive — **any way you like**
- Even if the package is intercepted, without the corresponding node's private key it cannot be decrypted
- Scripts and their `print` output never land in plaintext — specify explicit output artifacts

---

# Free mode — a new option for public distribution

MGC 1.5.4 adds **free mode** — just **omit `ext04`** when sealing:

| | p2p mode (default) | Free mode |
|---|---|---|
| How to seal | Pass `ext04=target node PEM` | **Omit** `ext04` |
| Who can unseal and run it | Only the node holding the matching private key | **Any MGC 1.5.4+ node** |
| Is the source visible? | No | No (same in-memory-only decryption) |
| Best for | Single-customer licensing, private delivery | **Skill marketplace, public demos, universal installer packages** |

Free mode wraps the content with MGC's shared default public key, so **any machine with MGC 1.5.4+ can install and run it**, while the source still never decrypts to disk on the receiving side.

> ⚠️ A free-mode package can be run by any node — perfect for "one runnable trial copy for everyone", **not** suitable when you need per-customer restrictions.

## Try it: seal example/ in free mode

This skill ships `example/` — 4 scripts plus a README, ready to use as a workflow. You can run the entire free-mode chain with it. **No second node, no key exchange.**

```python
# 1 · Store into MGC (workflow folder)
mgc_save_file(path="./example", info_owner="demo_free", diff_2="example")
# → 5 records (4 scripts + README), ext08 call graph built automatically

# 2 · Free-mode seal — note: no ext04
mgc_seal_package(
    info_owner="demo_free",
    diff_2="example",
    output_dir="./_demo_out",   # required from 1.5.4
)
# → _demo_out/example_delivery/{ example.mgc_file, README.md }

# 3 · Import the package you just generated
mgc_save_file(
    path="./_demo_out/example_delivery/example.mgc_file",
    info_owner="demo_free",
    diff_2="example",
)
# → 5 ciphertext records (ext03 populated, ext09="free mode")

# 4 · Run the driver (which drives B + C)
mgc_run(
    info_type="script",
    info_owner="demo_free",
    diff_2="example",
    diff_3="script_d.py",
)
# → {"status": "started"}
```

**Verification** — 4 files on the Desktop means the whole chain works:

| File | Written by | Content |
|------|-----------|---------|
| `~/Desktop/txt1.txt` | B | Greeting obtained from A via import |
| `~/Desktop/txt2.txt` | C | C's own summary |
| `~/Desktop/txt2_via_a.txt` | C → A | Greeting written by A's subprocess |
| `~/Desktop/combined.txt` | D | Rollup of B and C |

> On Linux, if `~/Desktop` does not exist, it falls back to `~`.

**Then verify "the source cannot be read"** — fetch a script after importing:

```python
mgc_get(info_type="script", info_owner="demo_free", diff_2="example", diff_3="config_a.py")
# → a long Base64 ciphertext string — no Python source visible
```

`mgc_run` still works at that point — **it runs, but the source cannot be read**. That is the core of free mode.

> ⚠️ **Two notes confirmed by testing**
> 1. **Step 3's `info_owner` matches the sealing-time value** (`demo_free` here). Records inside the package carry their own `info_owner` — the value passed at import does not override it. Even if you pass a different name, queries still use the package's `demo_free`.
> 2. **Same node + same `info_owner` overwrites the source records.** To keep both the plaintext and the ciphertext versions, store the folder under a different `info_owner`, or import on a different machine.

---

# Verified real-world scenarios

> MGC sealed delivery has been validated in enterprise workflow delivery practice — it is not a lab toy.

- ✅ A vendor delivers a data-automation workflow to a client — the code never lands in plaintext
- ✅ An independent developer seals and sells tool scripts — each license is managed independently
- ✅ Internal cross-team script licensing — prevents sensitive config and core logic from leaking
- ✅ A free-mode package distributed through a public channel — the receiving side imports and runs it

---

# ⚡ 30-second quick experience (run the full loop on your own node)

Before handing anything to a customer, run the seal → import → execute loop on your own machine.

> 💡 **Want to skip the key exchange?** Jump straight to "Try it: seal example/ in free mode" above — free mode needs no `ext04`, so it works in one step.

```python
# 1. Store the workflow folder into MGC
mgc_save_file(path="./example", info_owner="demo", diff_2="demo")

# 2. Seal with your own node_pub (simulates "self" authorization)
my_pub = mgc_get(info_type="__NODE_PUB__", info_owner="__NODE_PUB__")
mgc_seal_package(
    info_owner="demo",
    diff_2="demo",
    ext04=my_pub,
    output_dir="./_demo_out",      # required from 1.5.4
)

# 3. Re-import the generated .mgc_file (simulates the customer importing it)
mgc_save_file(
    path="./_demo_out/demo_delivery/demo.mgc_file",
    info_owner="demo",             # required; the stored identity comes from the package
    diff_2="demo",
)

# 4. Run the driver D (which drives B + C)
mgc_run(
    info_type="script", info_owner="demo",
    diff_2="demo", diff_3="script_d.py",
)
# → {"pid": 12345, "status": "started"}
```

> 💡 `diff_1` is optional from 1.5.4; `diff_3` (the script's path inside the package) is the most reliable way to target a single script.

After the run, the Desktop should show:

- ✅ `~/Desktop/txt1.txt` (written by B)
- ✅ `~/Desktop/txt2.txt` (written by C)
- ✅ `~/Desktop/txt2_via_a.txt` (written by C via A)
- ✅ `~/Desktop/combined.txt` (written by D)

> On Linux, if `~/Desktop` does not exist, it falls back to `~`.

**Working?** You now have the core sealed-delivery flow. Swapping in your customer's public key is all that is left to produce a licensed package.

---

# About cost

- **MGC Blackbox itself is free** to use. The encryption layer intentionally does not ship its source, for user safety — no monthly fee, no revenue share, no usage limits
- **This skill is free** — it packages the sealed-delivery best practices and detailed guidance
- **What you earn from selling scripts is entirely yours** — MGC takes no cut

> Why free? We believe a foundational security tool should be a free public good.

---

# Problem-to-solution map (market perspective)

| # | User pain | MGC 1.5.4 solution |
|---|-----------|---------------------|
| P1 | Customer can directly `cat` my `.py` files | Full AES-256 encryption, **no plaintext on disk** |
| P2 | Customer copies scripts to a colleague | AES key wrapped by the recipient's node RSA — **a different node cannot decrypt** |
| P3 | Multiple scripts use `import`; customer's machine changes paths | `ext08` auto-recognizes `import / Path / subprocess`, **runtime sealed routing**, no path dependency |
| P4 | Customer modifies my code and stops paying | Link authorization — **any change to `ext07` / `ext09` makes it unrestorable** |
| P5 | I have to maintain a "runbook"; customers can't set up dependencies | `ext05` auto-infers dependency list from imports, `ext06` infers platforms, `ext10` flags runtime compatibility |
| P6 | Re-sealing for each customer is tedious | `mgc_seal_package` handles folder-level sealing + node binding in one call |
| P7 | I want to publish a universal package for the marketplace | **Free mode** — no `ext04`, runnable on any MGC 1.5.4+ node |

---

# Prerequisites

- **Python 3.10+** (macOS 14+ Apple Silicon does NOT support Python 3.12)
- **MGC Blackbox ≥ 1.5.4** (double-layer encryption + link authorization + free mode + same-package cross-subdirectory recognition are all 1.5.4 capabilities)
- Install: `pip install mgc-blackbox`
- Run: `mgc` (API at `http://127.0.0.1:57219`, WebUI at `http://127.0.0.1:57218`)

> ⚠️ From 1.5.4, `mgc_seal` / `mgc_seal_package` / `mgc_package` **require `output_dir`** (absolute path). There is no desktop fallback — the desktop location differs across platforms, so MGC no longer guesses for you.

---

# Three-step delivery (author side)

## Step 1 — Store the workflow folder into MGC

```
my_workflow/
├── manifest.json
├── SKILL.md
├── run.py
├── helpers/
│   ├── fetch.py
│   └── parse.py
└── config/
    └── settings.json
```

```python
mgc_save_file(
    path="./my_workflow",
    info_owner="my_workflow",
    diff_2="my_workflow",
)
```

This step automatically:
- Parses each script's `argparse` and writes `ext02`
- Scans imports and writes `ext05` (dependency list)
- Infers `ext06` (platform list)
- Builds `ext08` (cross-script call graph)
- Runs a static runtime-compatibility check and writes `ext10` (`supported` / `unsupported` badge)

## Step 2 — Get the customer's RSA public key

```python
# Customer runs this on their own machine (WebUI or MCP)
node_pub = mgc_get(
    info_type="__NODE_PUB__",
    info_owner="__NODE_PUB__",
)
# Customer sends you the multi-line PEM (public key is not secret; any channel works)
```

> **WebUI path (1.4.7+ recommended)**: WebUI → Skill page → Settings dropdown → Node Public Key → copy multi-line PEM.
>
> ⚠️ `ext04` must contain real `\n` newlines; do not concatenate into a single line.

> 💡 **Free mode skips this step** — omit `ext04` to produce a package runnable on any MGC 1.5.4+ node.

## Step 3 — One-click seal

```python
mgc_seal_package(
    info_owner="my_workflow",
    diff_2="my_workflow",
    ext04=node_pub,          # customer's PEM; omit this line for free mode
    output_dir="./delivery", # required from 1.5.4
)
```

**Artifact directory layout:**

```
delivery/
└── my_workflow_delivery/
    ├── my_workflow.mgc_file   # zip: sealed scripts + MGCFILE.json manifest
    └── README.md               # usk/3.0 yaml + import instructions
```

Send the whole `my_workflow_delivery/` directory to the customer through any channel.

> 🔒 **Self-sealing warning**: if `ext04` is **your own** node_pub, MGC reports "sealing to this machine" — re-importing that package back into MGC overwrites the plaintext records irreversibly. For demos, prepare a separate test node.

---

# Three-step receive (customer side)

## Step 1 — Import the encrypted package

```python
mgc_save_file(
    path="./my_workflow_delivery/my_workflow.mgc_file",
    info_owner="my_workflow",
    diff_2="my_workflow",
)
# MGC splits the encrypted package into local records
```

> 💡 **Records inside the package carry their own `info_owner`** — the value passed at import only satisfies the required-field check; it does not change the stored identity. Later `mgc_get` / `mgc_run` calls must use the **package's** `info_owner` (`my_workflow` here).
> ⚠️ **Same node + same `info_owner` overwrites the source records** — re-importing the package on the author's own machine replaces the plaintext with ciphertext (irreversible). To keep both on one machine, store the folder under a different `info_owner` or import on a different machine.

## Step 2 — Browse the structure

```python
# List package entries (metadata only, no plaintext)
mgc_find(info_owner="my_workflow", diff_2="my_workflow")

# Read manifest (plaintext, explains the workflow structure)
mgc_get(info_type="file", info_owner="my_workflow", diff_2="my_workflow")

# Read SKILL.md (plaintext, follow the instructions to call scripts)
mgc_get(info_type="file", info_owner="my_workflow", diff_2="my_workflow", diff_3="SKILL.md")
```

## Step 3 — Black-box run

```python
mgc_run(info_owner="my_workflow", diff_2="my_workflow")
# → {"pid": 12345, "status": "started"}
# The caller only gets the launch status; the source stays encrypted
```

> 💡 To target a single script, `diff_3` (the script's path inside the package) is the most reliable: `mgc_run(info_owner=..., diff_2=..., diff_3="script/main.py")`.

---

# Single-script delivery: capsule export and dual-path import

When you only need to deliver **one script**, `mgc_seal` is lighter.

## Export the capsule

```python
mgc_seal(
    info_owner="my_script",
    ext04=node_pub,           # omit for free mode
    output_dir="./delivery",  # required from 1.5.4
)
# → delivery/my_script_20260929_120000/sealed_capsule.json
```

`sealed_capsule.json` is **self-describing** JSON — it carries `info_type` / `info_owner` / `diff_*` / `ext03` / `ext07` / `ext09` / the ciphertext, so the receiving side doesn't have to pick fields by hand.

## Import (two paths, pick either)

| Path | How | `info_type` needed? |
|------|-----|-------------------|
| **A · Handover file (recommended)** | `mgc_save_file(path='<capsule.json>', info_owner='<your owner>')` | **No** — inferred from the capsule |
| **B · Pass the JSON content** | `mgc_save(content=<whole capsule JSON>, info_type='script', info_owner='<your owner>')` | **Yes** — must state `info_type="script"` explicitly |

> ⚠️ On path B, **do not** pass `ext03` / `ext07` / `ext09` separately — when you pass the whole JSON, MGC extracts all ext fields automatically.
> 💡 **The capsule carries its own `info_owner`** — on path A the value you pass only satisfies the required-field check, while the stored identity comes from the capsule; on path B your `info_owner` is used (falling back to the capsule's if empty).
> ⚠️ **Same node + same `info_owner` overwrites the source records** — an `info_owner` identical to the source replaces the original plaintext records on the target node (irreversible). Use a different `info_owner` to keep both.

---

# Three critical rules

## Rule 1 — Same-package paths are OK; cross-package calls use the MGC API

Scripts inside the **same folder package** can freely use `import / relative paths / subprocess`** — MGC 1.5.4's `ext08` automatically recognizes and routes them through sealed execution at runtime. **No need to rewrite as API calls** (this includes same-package cross-subdirectory references, supported from 1.5.4).

Only **cross-folder-package calls** (different `info_owner + diff_2`) require the MGC API:

```python
import os, requests

with open(os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")) as f:
    MGC_TOKEN = f.read().strip()

def call_remote_script(info_owner, ext02=None):
    return requests.post(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        headers={"X-MGC-Token": MGC_TOKEN},
        json={
            "info_type": "script",
            "info_owner": info_owner,
            "diff_1": info_owner,
            "action": "run",
            "ext01": "python",
            "ext02": ext02,
        },
    ).json()
```

## Rule 2 — Author's SKILL.md is plaintext (by design)

The author's SKILL.md must be plaintext — it is the **routing instruction** for the customer: which script to call in which scenario, in what order, with what parameters. Without it, the customer cannot use the package at all.

> This is the public API contract, not implementation detail. **Core logic must go in the scripts** — see the next rule.

## Rule 3 — Put core algorithm in scripts, not in prompts

Both SKILL.md and prompts are **plaintext** — the customer can read them. Therefore:

| ✅ Do this | ❌ Don't do this |
|-----------|------------------|
| Put core algorithm in `run.py` | Put core algorithm in SKILL.md |
| SKILL.md says "when to call run.py, what args to pass" | SKILL.md says "the full business flow is…" (with details) |
| Business rules, thresholds, formulas → in scripts | Business rules written in prompts |

> The prompt is the customer-visible "manual". **The algorithm is what you're selling** — it must be locked inside the scripts.

---

# Recognizable cross-script patterns (MGC 1.5.4 complete table)

> Source: MGC skill_spec §2.4. When you save a folder via `mgc_save_file`, MGC statically parses every script to build the cross-script call graph (`ext08`). At runtime, MGC intercepts these patterns and routes them through sealed execution — **no files on disk, no plaintext, no rewrites**.

| Pattern | Code example | ext08 edge kind | Recognized? |
|---------|-------------|-----------------|-------------|
| `from` import | `from config import DEFAULT_CITY` | `from_import` | Yes |
| `from` import with alias | `from helpers.fetch import get_weather as gw` | `from_import` (asname preserved) | Yes |
| Plain `import` | `import helpers.parse` | `import` | Yes |
| Relative path via `Path` | `Path(__file__).parent / "config.py"` | `path` | Yes |
| Relative path via `open()` | `open("config.json")` against sibling file | `path` | Yes (recognition only in the current version; runtime routing is not yet supported) |
| Subprocess with relative path | `subprocess.run([sys.executable, str(Path(__file__).parent / "config.py"), ...])` | `path` (recognized via the `Path(...)` literal above; runtime also intercepts the subprocess call) | Yes — only when the caller and target were saved into MGC together as one workflow package. |
| Subprocess with literal list | `subprocess.run(['helper.py', '--x'])` (or `from subprocess import run; run([...])`) | `subprocess` (`callee` field records which subprocess function: `run` / `Popen` / `call` / `check_call` / `check_output`) | Yes — same package rule as above. Runtime interception runs the helper as sealed subprocess. |
| **Same-package cross-subdirectory import** | `from helpers.fetch import get_weather` (`helpers/` is a subdirectory) | `from_import` | Yes — **new in 1.5.4** |
| **Same-package cross-subdirectory `Path`** | `Path(__file__).resolve().parent.parent / "y.py"` | `path` | Yes — **new in 1.5.4** |
| **Subprocess with computed absolute path** | `subprocess.run([sys.executable, str(base_dir / "y.py")])` | `subprocess` | Yes — **new in 1.5.4**; the target script name must be unique within the package |
| Dynamic import | `importlib.import_module(module_name)` | — | No — MGC statically parses only string literals; dynamic names are not recognized. At runtime, Python's standard import will attempt to resolve the name (typically fails with `ModuleNotFoundError`). |
| Absolute path | `open("/Users/alice/scripts/config.py")` | — | No — absolute paths are not portable and cannot be sealed. Use MGC location addressing instead. |
| Subprocess literal with `..` | `subprocess.run([..., "../y.py"])` where `..` escapes the caller's directory | — | No — use the computed absolute path form `Path(__file__).resolve().parent.parent / "y.py"` instead |
| Function-level call without import | A function defined in another file called only by reference (no `import` / `from-import` / literal `Path` referencing it) | — | No — the parser only inspects string literals reachable via the conventional forms above. |

**Scope (1.5.4):**

- ✅ Cross-script calls are recognized **within the same folder** (`info_owner + diff_2` of the caller and the callee must be identical).
- ✅ **From 1.5.4, same-package cross-subdirectory references are recognized** — including `from helpers.x import y` and `Path(__file__).resolve().parent.parent / "y.py"`.
- ✅ **From 1.5.4, literal calls across different saved folders are also recognized** (the callee's script filename must be globally unique). ⚠️ In that case the caller must be **re-saved after the callee is stored**, so the dependency graph is rebuilt.
- ❌ **Function-level calls** that don't appear as `import` / `from-import` / `Path` literals in source — not recognized.

**Key invariants:**

- The `argparse` on each script is independent — the driver's args go to the driver's `ext02`, each helper's args go to the helper's own `ext02`.
- `Path(__file__).parent / "x.py"` resolves correctly on macOS, Linux (POSIX), and Windows (`\` separator) — MGC normalizes via `_normalize_path` in `subprocess_adapter`.
- Subprocess output flows through normally — `capture_output=True, text=True` works because the launched helper is a real Python interpreter with UTF-8 decoding.

**Runtime compatibility badge (`ext10`):**

Each script is statically checked at save time for whether it can run inside MGC. The result shows up as an `mgc_run` badge (`supported` / `unsupported`) in list and detail views.

- `unsupported` means the script contains a **fatal path check** (for example `if not Path(...).exists(): sys.exit(1)`) that exits **before** MGC's interception routing takes effect.
- How to fix: turn the path check into "warn when the path is missing and take a fallback branch" instead of `sys.exit(1)`.

**Limits.** The cross-script call only works when both scripts are saved together. To orchestrate scripts across different packages, use the REST API pattern — pass the MGC location (`info_owner`) of the target script.

---

# Error codes and troubleshooting

| Code | Meaning | Resolution |
|------|---------|------------|
| `MISSING_REQUIRED_FIELDS` | `mgc_seal` / `mgc_seal_package` is missing a required parameter | From 1.5.4, `output_dir` is **required**; p2p mode also needs `ext04` (free mode omits `ext04`) |
| `DIFF2_MISMATCH` | Script used `from-import` but **target script is not in the same folder package** | Put both scripts into the same `mgc_save_file` package; or use MGC API |
| `DEP_MISSING` | A dependency in `ext05` is not installed on the customer's machine | `pip install <missing dep>` (MGC does NOT auto-install) |
| `PLATFORM_INCOMPAT` | The `ext06` platform list doesn't include the current OS | Re-save on a supported platform, or extend platform branches in code |
| `AMBIGUOUS_SCRIPT` | `mgc_run`'s `diff_3` matched more than one script | Use a more complete `diff_3` (including subdirectory, e.g. `script/main.py`) |
| `NO_SCRIPT_TO_SEAL` | No sealable script was found during sealing | Confirm the script is stored in MGC and that `info_owner` / `diff_2` match the values used at save time |
| `MULTIPLE_MATCHES` | The query matched multiple records | Narrow it down with `diff_2` / `diff_3` |
| `args_not_recognized` | `argparse` parsing failed | Check `add_argument` usage; ensure literal `default=` |
| `dynamic_args_detected` | Default value uses dynamic computation (e.g. `datetime.now()`) | Use literal defaults, or pass via `ext02` explicitly |
| `Invalid PEM format` | `ext04` is not multi-line PEM | Copy from `mgc_get(info_type='__NODE_PUB__')` verbatim, preserving `\n` |

---

# When to use vs. when not to use (boundaries)

| ✅ Good fit | ❌ Not a good fit |
|-----------|------------------|
| Selling or licensing Python small tools | Open-source scripts (use GitHub) |
| Delivering internal small systems to clients | Large SaaS products (use cloud solutions) |
| Cross-node execution of automation workflows | Single-machine personal scripts (no need to seal) |
| "Tool packs" in paid knowledge products | Customer machines with full source environment for re-development |
| **Skill marketplace / universal installer packages (free mode)** | **Scenarios needing per-customer restrictions** (free mode runs on any node) |

---

# Comparison with alternatives

| Dimension | GitHub private repo | SaaS encryption service | License server | **MGC Sealed Delivery** |
|-----------|------------------------|-------------------------|-----------------|------------------------|
| Requires cloud | Yes | Yes | Yes | **No** |
| Monthly cost | Medium | High | Medium | **None** |
| Prevents source leak | ❌ Private but visible | ⚠️ Service-dependent | ❌ Server-side visible | ✅ **Completely invisible** |
| Prevents resell | ❌ | ⚠️ Service-dependent | ⚠️ Service-dependent | ✅ **Node-locked, cannot resell** |
| Offline delivery | ❌ | ❌ | ❌ | ✅ **Any channel** |
| Good for small systems | ⚠️ | ❌ Heavy | ⚠️ Heavy | ✅ **Light** |

---

# Security boundary

MGC protects **content confidentiality**, not runtime behavior:

- Data is encrypted at rest; sealed source is decrypted only in memory, at execution time
- Runtime behavior belongs to the script's author — once a package is unsealed on a node, MGC cannot guarantee the trustworthiness of its author, and what the script does at run time is the author's responsibility
- Before importing, verify the source node's public key against a trusted channel; link authorization (`ext07` / `ext09`) detects any modification of the artifact

---

# MCP tools quick reference

| Tool | Purpose | Required params |
|------|---------|-----------------|
| `mgc_save_file` | Store a local folder (auto-recognizes workflow) / import a `.mgc_file` / import a capsule | path, info_owner |
| `mgc_seal_package` | Seal a package for the target node | info_owner, diff_2, **output_dir** (p2p also needs ext04) |
| `mgc_save` | Store a single script (not in a package) / pass a capsule JSON | info_type, info_owner, content |
| `mgc_seal` | Seal a single script (exports a capsule) | info_owner, **output_dir** (p2p also needs ext04) |
| `mgc_run` | Black-box execution | info_type="script", info_owner (`diff_3` is the most reliable way to target one script) |
| `mgc_get` | Retrieve value / retrieve node_pub | info_type, info_owner |
| `mgc_find` | Fuzzy search | info_owner, match_mode |
| `mgc_list` | List all metadata | — |
| `mgc_package` | Plaintext packaging within same trust zone | info_owner, **output_dir** |
| `mgc_delete` | Delete stored records (has a confirmation flow) | info_type, info_owner |
| `mgc_open_webui` | Open WebUI | — |
| `mgc_skill` | Read MGC skill documentation | — |

---

# Related skills

- **MGC Blackbox (Cross-Device Script Authorization)** — Single-script sealing (lighter weight)
- **MGC Blackbox Meta Skill** — Full reference for all MGC capabilities

---

# Contact

- **Main repo**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com