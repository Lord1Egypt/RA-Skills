# example/ — Demo Script Set

> 4 scripts demonstrating MGC 1.5.4's `ext08` auto-recognition and runtime sealed routing for all cross-script call patterns.
> Uses Python standard library only. Cross-platform: macOS / Linux / Windows.

## File structure

```
example/
├── config_a.py        # A · config script (callable via both import and subprocess)
├── script_b.py        # B · gets values from A via import → writes txt1.txt to Desktop
├── script_c.py        # C · calls A via subprocess → writes txt2.txt to Desktop
├── script_d.py        # D · imports B + subprocess C → writes combined.txt to Desktop
└── README.md          # this file
```

## ext08 pattern demo matrix (verified on MGC 1.5.2, carried forward by 1.5.4)

| Call relation | Code pattern | ext08 edge type | Recognized |
|--------------|---------------|-----------------|------------|
| B → A | `from config_a import get_greeting, DEFAULT_USER` | `from_import` | ✅ |
| B → A | `import config_a` | `import` | ✅ |
| C → A | `subprocess.run([sys.executable, "config_a.py", ...])` | `subprocess` | ✅ |
| D → B | `import script_b; script_b.run(...)` | `import` | ✅ |
| D → C | `subprocess.run([sys.executable, "script_c.py", ...])` | `subprocess` | ✅ |

> Before 1.5.2, `subprocess.run([sys.executable, "x.py"])` literal list runtime routing was **not supported**; from 1.5.2 it is fully supported.

## Output files (explicit disk artifacts — black-box execution does not rely on `print`)

| File | Written by | Content |
|------|-----------|---------|
| `~/Desktop/txt1.txt` | B | Greeting from A via `import`, plus DEFAULT_USER |
| `~/Desktop/txt2.txt` | C | Summary written by C (calls A via subprocess) |
| `~/Desktop/txt2_via_a.txt` | A (spawned by C) | Greeting written by A's subprocess |
| `~/Desktop/combined.txt` | D | Rollup of B and C outputs |

> On Linux, if `~/Desktop` does not exist, falls back to `~`.

## Recommended try-it-yourself flow (MGC MCP tools)

### Method A · Free mode (try this first)

No second node and no key exchange — just **omit `ext04`** when sealing.

```python
# 1. Store
mgc_save_file(
    path="./example",
    info_owner="demo_workflow",
    diff_2="example",
)
# Auto-builds ext08 call graph (verified 5 edges)

# 2. Free-mode seal — note: no ext04
mgc_seal_package(
    info_owner="demo_workflow",
    diff_2="example",
    output_dir="./_demo_out",                   # required from 1.5.4
)
# → generates _demo_out/example_delivery/example.mgc_file + README.md
#   artifact ext09 = "free mode"

# 3. Import the package you just generated
mgc_save_file(
    path="./_demo_out/example_delivery/example.mgc_file",
    info_owner="demo_workflow",                 # required; stored identity comes from the package
    diff_2="example",
)
# Splits into 5 ciphertext records (including README.md)

# 4. Run
mgc_run(
    info_type="script",
    info_owner="demo_workflow",
    diff_2="example",
    diff_3="script_d.py",
)
# → {"status": "started"}
```

### Method B · p2p mode (targeted at one node)

```python
# 1. Store (same as above)

# 2. Get the target node's node_pub
my_pub = mgc_get(info_type="__NODE_PUB__", info_owner="__NODE_PUB__")
# Returns multi-line PEM public key

# 3. Seal to that node
mgc_seal_package(
    info_owner="demo_workflow",
    diff_2="example",
    ext04=str(my_pub),                          # required for p2p mode
    output_dir="./_demo_out",                   # required from 1.5.4
)

# 4. Import + 5. Run (same as Method A)
```

### Verify the results

After 5 seconds, check that all 4 files exist on the Desktop — `txt1.txt`, `txt2.txt`, `txt2_via_a.txt`, `combined.txt`. All 4 present = end-to-end success.

Then verify "the source cannot be read":

```python
mgc_get(info_type="script", info_owner="demo_workflow", diff_2="example", diff_3="config_a.py")
# → a long Base64 ciphertext string — no Python source visible; mgc_run still executes it
```

> ⚠️ **Two notes confirmed by testing**
> 1. **Package records carry their own `info_owner`** — the value passed at import only satisfies the required-field check; the stored identity comes from the package, and later queries must use it.
> 2. **Same node + same `info_owner` overwrites the source records** — re-importing the package on your own machine replaces the plaintext with ciphertext (irreversible). To keep both versions, store the folder under a different `info_owner`.

> ⚠️ Known warning: MGC may misreport same-package `script_b` as an external dependency (`DEP_MISSING`) — ignore it; the scripts themselves run normally.

## Design principles

1. **Zero non-standard dependencies**: only `os` / `sys` / `subprocess` / `argparse` / `pathlib` / `time`
2. **Cross-platform**: `Path.home() / "Desktop"`, falls back to `~` on Linux
3. **Black-box friendly**: every result is explicitly written to a Desktop file, no `print` capture dependency
4. **Complete argparse**: each script has a literal `default=`, so `ext02` is auto-recognized
5. **UTF-8 throughout**: avoids Windows CJK garbling

## Patterns NOT demonstrated (see SKILL.md for the full list)

- Dynamic module name: `importlib.import_module(x)`
- Absolute path: `open("/Users/.../config.py")`
- Subprocess literal containing `..`: `subprocess.run([..., "../y.py"])` — from 1.5.4, use the computed absolute path form `Path(__file__).resolve().parent.parent / "y.py"` instead
- Function-level reference: `import helpers; helpers.some_func()` without a literal `Path`

> 💡 **Same-package cross-subdirectory references are recognized from 1.5.4** (e.g. `from helpers.fetch import get_weather`, `Path(__file__).resolve().parent.parent / "y.py"`). This example keeps the simplest same-directory shape; see SKILL.md §"Recognizable cross-script patterns" for the cross-subdirectory forms.

Details in SKILL.md "Recognizable cross-script patterns".
