---
name: indexion-documentation
description: Documentation analysis — assess coverage, detect code-to-doc drift with plan reconcile, visualize dependencies with doc graph. Answers "what needs docs?" and "are docs still accurate?"
---

# indexion documentation — Documentation Analysis

Assess documentation state and detect drift. This skill covers the
**evaluation side** of the documentation lifecycle: what exists, what's
missing, what's stale. For building READMEs, see `indexion-readme`.

## "What needs documentation?"

```bash
# Quick coverage overview — how much of the public API is documented?
indexion plan documentation --style=coverage .
```

Reports:
- Overall coverage percentage (documented / total pub items)
- Per-package breakdown with README presence
- Functions vs types coverage split

Output example:
```
Overall Coverage: 81% (2285/2806)
Functions: 89%, Types: 75%
```

For a detailed plan with prioritized action items:

```bash
# Full plan with priorities and package inventory
indexion plan documentation .

# As a GitHub Issue for tracking
indexion plan documentation --format=github-issue .

# JSON for scripting
indexion plan documentation --format=json .
```

For a quick per-file listing of undocumented items:

```bash
# Which pub declarations lack doc comments?
indexion grep --undocumented src/
```

**How detection works:** Uses KGF tokenization to find visibility keywords
(`pub`, `public`, `export`) paired with declaration keywords (`fn`, `struct`,
`enum`, `type`, `trait`). Associates `///` doc comments with declarations.
Language-agnostic — works for any KGF-supported language.

**Caveat:** `///|` marker-only comments count as "documented" even without
descriptive text. Check `doc_preview` in the output for quality, not just coverage.

## "Are my docs up to date?"

Detect drift between implementation code and documentation.

```bash
# Full reconcile report in markdown
indexion plan reconcile --format=md .
```

This compares code symbols against documentation and reports:
- **Vocabulary divergence**: source code terms missing from co-located docs
- **Stale docs**: code changed after docs were last updated
- **Missing docs**: code modules with no documentation coverage

**Read the report:**

The Vocabulary Divergence table shows distance (0-100%) between code vocabulary
and documentation. 90%+ distance means the README is essentially unrelated to
the current code. Check the Gap Terms column for specific missing vocabulary.

**Scoped checks:**

```bash
# Check only package-level docs
indexion plan reconcile --scope=package-docs .

# Check only tree-level docs
indexion plan reconcile --scope=tree-docs .

# Check specific documents
indexion plan reconcile --doc='docs/**/*.md' .
indexion plan reconcile --doc-spec=markdown .
```

**Timestamp strategies:**

```bash
# Use git commit timestamps (more accurate for collaborative projects)
indexion plan reconcile --git .

# Use file mtimes only (faster, no git dependency)
indexion plan reconcile --mtime-only .
```

**Cache and drift:**

`plan reconcile` maintains a cache at `.indexion/cache/reconcile/`. After schema
changes or indexion upgrades, the cache can become stale and cause deserialization
errors. Clear it:

```bash
rm -rf .indexion/cache/reconcile
```

## "Show me the dependency structure"

Generate dependency diagrams for understanding module relationships.

```bash
# Mermaid diagram (default — embeddable in GitHub README)
indexion doc graph src/config/

# Other formats
indexion doc graph --format=dot src/     # Graphviz DOT
indexion doc graph --format=d2 src/      # D2
indexion doc graph --format=text src/    # ASCII text
indexion doc graph --format=json src/    # Machine-readable

# Custom title and output file
indexion doc graph --title="KGF Dependencies" --output=deps.mmd src/kgf/
```

## Analysis Workflow

```bash
# 1. What's the current state?
indexion plan documentation --style=coverage .

# 2. What specific items lack docs?
indexion grep --undocumented src/

# 3. Has code drifted from existing docs?
indexion plan reconcile --format=md .

# 4. What does the dependency structure look like?
indexion doc graph --output=deps.mmd src/

# 5. Fix flagged docs, re-verify
indexion plan reconcile --format=md .
```

## Common Pitfalls

**"plan reconcile shows 90%+ divergence everywhere"**
- Auto-generated skeleton READMEs (API listing only) have high divergence because
  they lack the vocabulary of the actual implementation. Enrich them with
  descriptions of what the code does, not just what it exports.

**"plan documentation says 100% coverage but docs are wrong"**
- Coverage measures presence of doc comments, not accuracy. A `///|` marker
  counts as documented. Use `plan reconcile` to check content accuracy.

**"plan reconcile crashes on startup"**
- Cache deserialization error after schema changes. Clear it:
  `rm -rf .indexion/cache/reconcile`

**"plan reconcile detects drift I already fixed"**
- The `--git` flag uses commit timestamps. If you fixed docs but haven't committed,
  mtime-based detection (`--mtime-only`) will see the fix, but git-based won't.

**Reconcile only checks implementation -> docs direction.** It detects code terms
missing from docs, but does NOT detect docs referencing nonexistent CLI options.
For that direction, compare each README against `indexion <command> --help` manually.
