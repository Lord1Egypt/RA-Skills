# Packaging — Environments, Dependencies, and Shipping

Two separate jobs get confused here: reproducing an environment (venv + lock) and publishing an artifact (pyproject + wheel). Diagnose which one you are in first.

## The Environment Rules

- One venv per project, inside the project: `python3.12 -m venv .venv` names the interpreter explicitly, so an upgrade of "python3" cannot silently move you.
- `python -m pip install …`, never bare `pip`. Bare `pip` is whatever shim is first on PATH; `python -m pip` installs into the interpreter you are about to run. Every "installed but ModuleNotFoundError" is this.
- Never install into the system interpreter. Distros mark it externally managed (PEP 668) and pip refuses with `error: externally-managed-environment` — that error is correct, and `--break-system-packages` earns its name.
- A venv is not relocatable: its scripts hard-code the absolute interpreter path. Moving or renaming the project directory, or upgrading a Homebrew/pyenv Python underneath it, produces `No module named encodings` or a shim pointing at a deleted binary. Delete and recreate; never hand-edit `pyvenv.cfg`.
- `.venv/` in `.gitignore`, always. The lockfile is the artifact you commit, not the tree.

## Which Tool

| Situation | Use | Why |
|---|---|---|
| Any project, zero extra tooling | `venv` + `pip` + a compiled lock (`pip-tools`) | Present on every machine; the fallback everyone can run |
| Speed matters, or you juggle Python versions | `uv` (`uv venv`, `uv sync`, `uv run`, `uv python install 3.12`) | Resolves and installs an order of magnitude faster than pip on cold caches (vendor benchmark — verify on your own tree); also manages interpreters |
| Library with a lot of release ceremony | `poetry` or `hatch` | Version bumps, build, publish in one tool |
| Scientific stack with non-Python deps (CUDA, MKL, GDAL) | `conda`/`mamba` for those, pip only for the rest | Conda ships the C libraries wheels cannot |
| Anything else | `venv` + `pip` | Do not add a tool to a project that has no dependency problem |

Mixing conda and pip: create the conda env, install everything conda-provided FIRST, then pip last, and never re-run `conda install` afterwards — it rewrites files pip owns and the env becomes unexplainable.

## pyproject.toml, The Only File You Need

```toml
[project]
name = "myapp"
version = "0.3.1"
requires-python = ">=3.11"
dependencies = ["httpx>=0.27,<1", "pydantic>=2.6"]

[project.optional-dependencies]
dev = ["pytest>=8", "mypy>=1.10"]

[project.scripts]
myapp = "myapp.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- `requires-python` is load-bearing: without it pip happily installs your package on an interpreter it cannot import on, and the failure surfaces as a runtime `SyntaxError` in someone else's project.
- `setup.py` is not deprecated as a config file, but `python setup.py install` is removed — build with `python -m build`, install with pip.
- `[project.scripts]` generates the console entry point; `python -m myapp` (a `__main__.py`) works without installation and is the debug-friendly twin.

## Pinning: Applications vs Libraries

- **Application** (you deploy it): declare ranges in `pyproject`, then compile a fully pinned lock of the whole transitive tree with hashes and commit it. `pip-compile --generate-hashes` or `uv lock`. Deploy with `pip install --require-hashes -r requirements.lock` — hashes are what turn a lock into a supply-chain control.
- **Library** (someone else depends on it): ranges only, never `==`. An exact pin in a library is a conflict you inflict on every consumer. Upper bounds only where you know a breakage exists (`<2` on a package that breaks majors), because a speculative cap ages into an unsolvable resolution.
- `pip freeze > requirements.txt` is not a lock: it snapshots whatever is in the env (including your editor's plugins), carries no hashes, and records nothing about which packages you actually asked for. Use it to inspect, not to pin.

## Why The Install Failed

| Symptom | Cause | Fix |
|---|---|---|
| Compiler errors, "building wheel for X" | No wheel for your Python/OS/arch, so pip fell back to the sdist | Wait for the wheel, drop to the previous minor Python, or install the system build deps |
| `incompatible architecture` at import | x86_64 wheel on arm64 (or a Rosetta shell) | `python -c "import platform; print(platform.machine())"`; recreate the venv with the native interpreter |
| Resolution runs for minutes then backtracks | Unbounded ranges across many packages | Constrain the two or three packages that pin hardest, or switch resolver (`uv`) |
| `pip check` reports conflicts after a series of installs | pip only solves what it is given in ONE command | Reinstall from one requirements file so the resolver sees everything at once |
| Package installs but `import` fails | Distribution name ≠ import name (`pillow`→`PIL`, `beautifulsoup4`→`bs4`, `python-dateutil`→`dateutil`) | `python -m pip show -f <dist>` lists the modules it actually ships |
| Works after `pip install -e .`, breaks in the built wheel | Data files or subpackages not declared | Inspect the artifact: `python -m zipfile -l dist/*.whl` — what is not in the list does not ship |
| Anything else | Reproduce in a fresh venv (`python -m venv /tmp/x && /tmp/x/bin/python -m pip install …`) | Half of install bugs are the state of the current env |

## Editable Installs and Layout

- `pip install -e .` (PEP 660) makes your source tree importable without reinstalling on every edit. Requires a modern backend; setuptools supports it from 64.
- Use the `src/` layout: `src/myapp/__init__.py`. With a flat layout, `import myapp` resolves to the directory you happen to be standing in, so tests pass against the source tree even when the package is broken or not installed at all — the failure only appears for your users.
- Package data (templates, JSON, model files) is read with `importlib.resources.files("myapp") / "data.json"`, never `open(os.path.dirname(__file__) + …)` — the latter breaks in zipped installs and in any environment where the package is not a plain directory. Declare the files in the build config or they are silently omitted.

## Publishing

1. `python -m build` → an sdist and a wheel in `dist/`.
2. `twine check dist/*` catches a broken README before PyPI rejects it.
3. Upload to TestPyPI first; install from it into a scratch venv and import.
4. Real upload: trusted publishing (OIDC from CI) over a long-lived API token. A token in CI secrets is a credential that can publish any of your packages forever.
5. A version number can never be reused, even after deletion — yanking hides a release from resolution but does not free the number. Ship `0.3.2`, not "the fixed 0.3.1".

## Private Indexes

`--extra-index-url` tells pip to consider BOTH indexes and take the highest version — so anyone who publishes `yourinternalpkg 99.0` to public PyPI wins the resolution. That is the dependency-confusion attack. Use `--index-url` pointed at a proxy that mirrors PyPI, or pin your internal packages by hash. Configure it in `pip.conf`/`uv.toml` so no one has to remember the flag.
