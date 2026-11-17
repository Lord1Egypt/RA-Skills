# `rwlib` Public API Reference

`rwlib` is the shared engine behind `rabbit-writes`, `rabbit-readme-improver`, and companion scripts. It requires only the Python standard library (Python 3.9+) and zero external dependencies.

## Integration Patterns

External tools and sibling skills interact with the engine in two supported ways:

### 1. Loose Coupling (Recommended): Subprocess + `--json`
Invoke `scan.py` directly and parse structured JSON. The output carries `schema_version`, `lexicon_version`, `registers_version`, and `ste_version` to guarantee deterministic parsing.

```bash
python3 <path-to-rabbit-writes>/scripts/scan.py document.md --json
```

Top-level JSON contract:
- `schema_version`: Findings schema version (currently `1`).
- `lexicon_version`: Lexicon catalogue version (e.g. `5`).
- `registers_version`: Tolerance matrix version (e.g. `4`).
- `ste_version`: ASD-STE100 lexicon version (e.g. `3`).
- `findings`: List of findings matching the findings schema.
- `counts`: Aggregated findings counts by priority and band.
- `stats`: Document statistics (word count, sentence length SD/mean, etc.).

### 2. Direct Python Import: Path Bootstrap
Add the engine directory to `sys.path` and import desired modules:

```python
import os, sys
ENGINE_DIR = "<path-to-rabbit-writes>/scripts"
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from rwlib import findings, markdown, sections, lexicon, registers, ste, stylometry, voices
```

Alternatively, dynamically load `scan.py` via `rwlib.load_scan()`:

```python
from rwlib import load_scan
scan_mod = load_scan()
findings, stats = scan_mod.scan("Your text here")
```

---

## Stable Public Modules

The following modules maintain strict backward-compatible contracts and versioned schemas:

### `rwlib.findings`
Standardized finding data structures and validators.
- `SCHEMA_VERSION`: Integer schema version (`1`).
- `make(finding_id, label, band, priority, line, match, excerpt, ...)`: Construct a valid finding dictionary.
- `counts(findings)`: Calculate priority and band totals (`total`, `p0`, `p1`, `p2`, `craft`, `fingerprint`, etc.).
- `validate(findings)`: Generator yielding `(index, error_message)` for any malformed finding.

### `rwlib.markdown`
Markdown parsing, span locator utilities, and exemption handling.
- `word_count(text)`: Measure word count excluding markdown markup and code spans.
- `is_prose_block(block_text)`: Determine whether a block is running prose vs. list/table/code.
- `strip_fences(text)`: Remove fenced code blocks.
- `blank_entities(text)`: Blank HTML entities preserving string offsets.
- `apply_exemptions(text)`: Blank code spans, fences, and quoted examples for safe scanning.
- `line_of(text, char_offset)`: 1-indexed line number for a character offset.

### `rwlib.sections`
Heading classification and structural standards for documentation and README analysis.
- `classify_heading(heading_text)`: Returns a canonical section category from `SECTION_NAMES` (`toc`, `features`, `demo`, `installation`, `usage`, `examples`, `configuration`, `api`, `architecture`, `contributing`, `testing`, `roadmap`, `faq`, `license`, `credits`, `support`, `sponsors`, `changelog`, `security`, `related`, `performance`), or `other` when nothing matches.
- `SECTION_KEYWORDS`: `[(category, [keyword, ...]), ...]`, the ordered table `classify_heading` matches against. `SECTION_NAMES`: the category names alone, in the same order.

### `rwlib.lexicon`
Pattern and tier catalogue loader.
- `version(path=None)`: Current lexicon version integer (`6`).
- `load(path=None)`: Load `lexicon.json` dictionary.
- `SYNTHETIC_FINDING_IDS`: Set of findings raised synthetically by code rather than by direct regex.
- `word_regex(entries)` / `phrase_regex(entries)`: Helper compilers with whole-word/phrase boundaries.

### `rwlib.registers`
Tolerance matrix and register detection.
- `version(path=None)`: Registers version integer (`4`).
- `registers()`: List of known register names (`blog`, `chat`, `technical`, `academic`, etc.).
- `detect_register(text)`: Auto-detect register from structural prose characteristics.
- `skip_table()` / `relax_table()`: Tolerance thresholds per register.
- `default_register()`: Strict baseline register (`blog`).

### `rwlib.stylometry`
Stylometric fingerprinting and voice distance calculations.
- `SCHEMA_VERSION`: Fingerprint schema version (`2`).
- `fingerprint(text, sample_measures=...)`: Measure 10 stylometric dimensions across a document.
- `distance(fp_a, fp_b)`: Manhattan distance between two fingerprints.
- `bands(dimension)`: Human reference ranges for stylometric markers.

### `rwlib.ste`
ASD-STE100 Issue 9 Simplified Technical English structural and vocabulary checks.
- `version(path=None)`: STE lexicon version integer (`4`).
- `check(text, mode=None, scope="all", word_cap=None)`: Run STE checks. `scope="mechanical"` runs the default counted band; `scope="all"` includes advisory vocabulary.
- `check_for_scan(text, ...)`: Run STE checks and attach `ste_version` to each finding.
- `MECHANICAL_IDS`: Counted, default-on finding IDs (`ste-sentence-procedural`, `ste-sentence-descriptive`, `ste-paragraph-sentences`, `ste-condition-order`, `ste-no-punctuation`).
- `ADVISORY_IDS`: Word-list advisory finding IDs (`ste-modal`, `ste-ing-verb`, `ste-banned-verb`, `ste-phrasal-verb`, `ste-passive`, `ste-vocab`).

### `rwlib.rewrite`
Model-assisted rewrite generation, candidate gating, and replacement palette loader.
- `load_alternatives(path=None)`: Load replacement palette from `thesaurus_alternatives.json`.
- `plan(text, findings, ...)`: Group actionable findings into rewrite units.
- `gate(unit, candidate, scan_fn, validate_fn, ...)`: Multi-gate validation for proposed rewrites.
- `run(text, findings, endpoint, scan_fn, validate_fn, ...)`: Orchestrate end-to-end rewrite workflow.

### `rwlib.voices`
Voice profile loading, inheritance (`extends`), and resolution.
- `resolve(name_or_path, voices_dir=None)`: Resolve voice configuration dictionary.
- `load_scan(caller_name="engine")`: Dynamic loader for `scan.py`.

---

## Internal & Volatile Modules

The following modules are internal to `rabbit-writes` implementation and subject to refactoring:
- `rwlib.fixes`: Rule-specific mechanical replacements for `--apply-safe`.
- `rwlib.suppress`: In-document comment suppression parsing (`rabbit-allow`).
- `rwlib.language`: Scope validation for English prose.
- `rwlib.corpus`: Repository-internal README research dataset loader (layout-aware).
