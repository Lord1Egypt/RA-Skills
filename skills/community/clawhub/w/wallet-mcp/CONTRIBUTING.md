# Contributing to wallet-mcp

Thank you for your interest in contributing! This guide covers everything you need to get started.

---

## Getting Started

### 1. Fork & clone

```bash
git clone https://github.com/genoshide/wallet-mcp
cd wallet-mcp
```

### 2. Set up development environment

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies
uv sync

# Copy env template
cp .env.example .env
```

### 3. Run the test suite

```bash
python -X utf8 test_local.py
```

All 36 tests must pass before submitting a PR.

---

## Project Structure

```
src/wallet_mcp/
├── server.py       ← FastMCP tool definitions — add new tools here
└── core/
    ├── evm.py      ← EVM blockchain operations
    ├── solana.py   ← Solana blockchain operations
    ├── generator.py
    ├── distributor.py
    ├── manager.py
    ├── storage.py
    └── utils.py
```

---

## Adding a New Tool

### Step 1 — Add the logic to a core module

```python
# src/wallet_mcp/core/manager.py
def my_new_feature(param: str) -> dict:
    ...
    return {"result": ...}
```

### Step 2 — Expose it in server.py

```python
# src/wallet_mcp/server.py
@mcp.tool()
def my_new_tool(param: str) -> dict:
    """
    One-line description shown to the AI agent.

    Args:
        param: description of the parameter

    Returns:
        {status, result}
    """
    try:
        from wallet_mcp.core.manager import my_new_feature
        return {"status": "success", **my_new_feature(param)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Step 3 — Document it in openclaw/SKILL.md

Add the tool definition to `openclaw/SKILL.md`.

### Step 4 — Add a test

Add a test case to `test_local.py` under the appropriate section.

---

## Code Standards

- **Python 3.11+** — use modern type hints (`list[dict]` not `List[Dict]`)
- **No bare `except`** — always catch specific exceptions or use `except Exception as e`
- **All tools return `{status: "success"|"error", ...}`** — never raise from a tool function
- **rpc_url guard** — all RPC functions must have `rpc_url = rpc_url or DEFAULT_RPC`
- **Lazy imports inside functions** — keep server startup fast, import heavy libs inside tool functions
- **No print() in core modules** — use `setup_logging()` logger only

---

## Pull Request Checklist

- [ ] `python -X utf8 test_local.py` → all tests pass
- [ ] New feature has at least one test in `test_local.py`
- [ ] `openclaw/SKILL.md` updated if new tool added
- [ ] CHANGELOG.md entry added under `[Unreleased]`
- [ ] No `.env` or `wallets.csv` committed

---

## Reporting Bugs

Open an issue with:
- Python version (`python --version`)
- OS + wallet-mcp version
- Steps to reproduce
- Actual vs expected output (JSON)

---

## Questions

Open a GitHub Discussion or issue — happy to help!
