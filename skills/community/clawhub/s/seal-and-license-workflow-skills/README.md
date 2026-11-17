# Seal and License Workflows or Skill Packages

> **Version 1.3.0** · For script sales and local delivery — turn a Python workflow into a source-bound local package. The authorized node runs it, the source stays encrypted end to end. Zero cloud, zero code rewrite.

---

## What this skill solves

| Your situation | The problem with the usual approach | What this skill does |
|----------------|-----------------------------------|------------------------|
| You sell scripts and customers forward them | One copy sold = one copy given away | One key per recipient, bound to the named node |
| You deliver a small system to a client | The client edits the code, or resells it to a peer | You deliver a sealed package — the source never lands in plaintext |
| You publish a universal tool pack on a marketplace | Publishing the source means giving up ownership | A free-mode package: installable and runnable anywhere, source still stays sealed |
| Teams share scripts internally but fear leaks | Approval workflows kill throughput | Sealed package + link authorization — provenance is traceable, tampering invalidates |

---

## Core capabilities

### Double-layer encryption + link authorization (MGC 1.5.4)

Sealing encrypts the content with AES-256-GCM, wraps the AES key with the target node's RSA-2048 public key, then wraps that result again with an AES-GCM key derived from the **author's source_node_pub** (AAD = seal mode).

- `ext03` — the doubly-wrapped ciphertext
- `ext07` — the author's node_pub (plaintext identifier, participates in encryption)
- `ext09` — seal mode (`p2p mode` / `free mode`)

**Changing `ext07` or `ext09` — even one space — makes the whole package unrestorable.** The source identity is the integrity anchor.

### Two seal modes

| | p2p mode | Free mode |
|---|---|---|
| How to seal | Pass `ext04=target node PEM` | **Omit** `ext04` |
| Who can unseal and run it | Only the node holding the matching private key | **Any MGC 1.5.4+ node** |
| The source | Never lands in plaintext | Never lands in plaintext |
| Best for | Single-customer licensing, private delivery | **Skill marketplace, public demos, universal installers** |

### Zero-rewrite sealing

Scripts stay exactly as written, and MGC recognizes the cross-script relationships at save time:

- `from helpers.fetch import get_weather` ✅
- `import config` ✅
- `Path(__file__).parent / "settings.json"` ✅
- `subprocess.run([sys.executable, "helper.py"])` ✅
- **Same-package cross-subdirectory** `Path(__file__).resolve().parent.parent / "y.py"` ✅ (new in 1.5.4)
- **Subprocess with a computed absolute path** `subprocess.run([sys.executable, str(base_dir / "y.py")])` ✅ (new in 1.5.4)

Execution is routed through sealed execution — **no files on disk, no plaintext, no rewrites**.

---

## Quick start

### 1 · Store (author side)

```python
mgc_save_file(path="./my_workflow", info_owner="my_workflow", diff_2="my_workflow")
```

### 2 · Get the target node's public key

```python
node_pub = mgc_get(info_type="__NODE_PUB__", info_owner="__NODE_PUB__")
```

### 3 · Seal

```python
mgc_seal_package(
    info_owner="my_workflow",
    diff_2="my_workflow",
    ext04=node_pub,           # omit this line for free mode
    output_dir="./delivery",  # required from 1.5.4
)
# → delivery/my_workflow_delivery/{ my_workflow.mgc_file, README.md }
```

### 4 · Import (receiving side)

```python
mgc_save_file(
    path="./my_workflow_delivery/my_workflow.mgc_file",
    info_owner="my_workflow",
    diff_2="my_workflow",
)
```

### 5 · Run

```python
mgc_run(info_type="script", info_owner="my_workflow", diff_2="my_workflow")
# → {"pid": 12345, "status": "started"}
```

> 💡 `diff_1` is optional from 1.5.4; `diff_3` (the script's path inside the package) is the most reliable way to target a single script.

---

## Environment requirements

- **Python 3.10+** (macOS 14+ Apple Silicon does NOT support Python 3.12)
- **MGC Blackbox ≥ 1.5.4**
- `pip install mgc-blackbox>=1.5.4` → run `mgc` (API `127.0.0.1:57219` / WebUI `127.0.0.1:57218`)

> ⚠️ From 1.5.4, `mgc_seal` / `mgc_seal_package` / `mgc_package` **require `output_dir`** (absolute path) — there is no desktop fallback.

---

## Example

`example/` provides 4 zero-dependency scripts covering every recognizable call pattern:

```
example/
├── config_a.py     # config script
├── script_b.py     # gets values from A via import
├── script_c.py     # calls A via subprocess
└── script_d.py     # driver, drives B + C
```

### Try it: seal example/ in free mode

No second node, no key exchange — four steps to the full chain:

```python
# 1 · Store into MGC
mgc_save_file(path="./example", info_owner="demo_free", diff_2="example")

# 2 · Free-mode seal (no ext04)
mgc_seal_package(
    info_owner="demo_free",
    diff_2="example",
    output_dir="./_demo_out",
)

# 3 · Import the package you just generated
mgc_save_file(
    path="./_demo_out/example_delivery/example.mgc_file",
    info_owner="demo_free",
    diff_2="example",
)

# 4 · Run the driver
mgc_run(info_type="script", info_owner="demo_free", diff_2="example", diff_3="script_d.py")
```

Four files appear on the Desktop — `txt1.txt` / `txt2.txt` / `txt2_via_a.txt` / `combined.txt` — and the whole chain works. Fetching a script with `mgc_get` then returns a long Base64 ciphertext — **it runs, but the source cannot be read**.

> ⚠️ Package records carry their own `info_owner`; the value passed at import only satisfies the required-field check. Same node + same `info_owner` overwrites the source records.

Full walkthrough in [example/README.md](example/README.md).

---

## Security boundary

MGC protects **content confidentiality**, not runtime behavior:

- Data is encrypted at rest; sealed source is decrypted only in memory, at execution time
- Runtime behavior belongs to the script's author — MGC cannot guarantee the trustworthiness of the author, and what the script does at run time is the author's responsibility
- Before importing, verify the source node's public key against a trusted channel; link authorization detects any modification of the source identity

---

## Related skills

- **MGC Blackbox (Cross-Device Script Authorization)** — single-script sealing (lighter weight)
- **MGC Blackbox Meta Skill** — full reference for all MGC capabilities

---

## Links

- **Main repo**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com
