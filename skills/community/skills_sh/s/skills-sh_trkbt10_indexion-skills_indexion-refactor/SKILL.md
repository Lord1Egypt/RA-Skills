---
name: indexion-refactor
description: After writing code, detect and clean up duplication at three levels — copy-paste blocks, cross-package shared code, unnecessary wrappers, and concept-level SoT violations. Detect with indexion, fix, and verify.
---

# indexion refactor — Codebase Refactoring

Detect and eliminate duplication at three levels — textual, structural, and conceptual —
using indexion's analysis commands, then verify SoT is enforced.

## When to Use

- After adding a new abstraction (type, module, API layer)
- After introducing a new file format or I/O boundary
- When a fix required touching 3+ files for the same reason
- When a "guard" or "skip" was added to work around a structural problem
- When `opendir`, `ENOENT`, or similar filesystem errors appear from unexpected paths
- When extracting shared code across packages
- When cleaning up after a refactor (removing trivial wrapper functions)
- Periodic SoT health check on a codebase

## Three Levels of Duplication

| Level | What it is | Tool | Example |
|-------|-----------|------|---------|
| **Textual** | Copy-pasted code blocks, identical functions | `plan refactor` | `is_whitespace` copied across 5 modules |
| **Structural** | Same logic structure with different names | `plan solid`, `plan unwrap` | cross-package extraction candidates, trivial wrappers |
| **Conceptual** | Same domain concept implemented independently | `explore` + manual analysis | Three modules each deciding "is this file an archive?" |

Textual duplication is easy to find and fix. Conceptual duplication is the hardest and
most dangerous — it produces no copy-paste matches but means changing one concept requires
updating every scattered implementation.

## Workflow

### Phase 1: Clear textual duplication (`plan refactor`)

Start with high-confidence matches and work down.

```bash
# Step 1: Find 90%+ duplicates (high confidence)
indexion plan refactor --threshold=0.9 \
  --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' \
  cmd/indexion/

indexion plan refactor --threshold=0.9 \
  --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' \
  src/
```

**Read the output in three sections:**

| Section | What it finds | Action |
|---------|--------------|--------|
| Similar Files | Files with high overall similarity | Investigate for structural consolidation |
| Duplicate Code Blocks | Line-level identical code between files | Extract to `@common` or shared module |
| Function-Level Duplicates | Structurally similar functions (TF-IDF on bodies) | Unify into single SoT function |

**Same-file duplicates** (functions within one file at 90%+) are the highest-value
targets — easiest to fix, clearest wins. Example: `get_global_data_dir` and
`get_global_cache_dir` share 95% structure, extracted into `resolve_os_dir`.

```bash
# Step 2: Use grep to trace references before consolidating
indexion grep "TypeIdent:TfidfEmbeddingProvider" src/
indexion grep --semantic=name:is_whitespace src/

# Step 3: Fix, then re-run to confirm duplicates are gone
indexion plan refactor --threshold=0.9 --include='*.mbt' ...

# Step 4: Lower threshold and iterate
indexion plan refactor --threshold=0.85 --include='*.mbt' ...
```

**`plan refactor` options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--threshold=FLOAT` | 0.7 | Minimum similarity threshold |
| `--strategy=NAME` | hybrid | Similarity: hybrid, tfidf, bm25, jsd, ncd |
| `--fdr=FLOAT` | 0 | FDR correction (0=disabled) |
| `--style=STYLE` | raw | Output: raw, structured |
| `--format=FORMAT` | md | Output: md, json, text, github-issue |
| `--name=NAME` | -- | Project name (for structured style) |
| `--include=PATTERN` | -- | Include pattern (repeatable) |
| `--exclude=PATTERN` | -- | Exclude pattern (repeatable) |
| `-o, --output=FILE` | stdout | Output file path |
| `--specs-dir=DIR` | kgfs | KGF specs directory |

**What remains after cleanup (stop signals):**

- **Platform stubs** (`native.mbt` / `stub.mbt`) — intentional platform branching
- **Type method similarity** (`to_string` on different types) — different types, same pattern
- **CLI command boilerplate** (`command()` functions) — @argparse API pattern, not duplication
- **Semantic-but-different** functions (`is_disqualifying_keyword` vs `is_skip_token`) — different purpose

### Phase 2: Extract cross-package shared code (`plan solid`)

After cleaning within each directory, find code that should be shared across packages.

```bash
# Find overlap between two packages
indexion plan solid --from=src/a,src/b

# Specify extraction target
indexion plan solid --from=src/a,src/b --to=src/common

# Use tree edit distance for precise function-level matching
indexion plan solid --from=src/a,src/b --strategy=apted

# Higher threshold for stricter matching
indexion plan solid --from=src/a,src/b --threshold=0.95

# Filter files
indexion plan solid --from=src/a,src/b --include='*.mbt' --exclude='*_test.mbt'
```

`plan solid` differs from `plan refactor`:

| | `plan refactor` | `plan solid` |
|---|-----------------|-------------|
| Scope | Internal duplication within directories | Cross-directory overlap |
| Goal | Consolidate within a codebase | Extract shared code into a new package |
| Input | `<path>` | `--from=dirA,dirB` |

**`plan solid` options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--from=DIRS` | (required) | Source directories (comma-separated or repeatable) |
| `--to=DIR` | -- | Target directory for extraction |
| `--rules=FILE` | -- | Rules file (.solidrc) |
| `--rule=RULE` | -- | Inline rule (repeatable) |
| `--threshold=FLOAT` | 0.9 | Minimum similarity threshold |
| `--strategy=NAME` | tfidf | Similarity: tfidf, apted, tsed |
| `--include=PATTERN` | -- | Include pattern (repeatable) |
| `--exclude=PATTERN` | -- | Exclude pattern (repeatable) |
| `--format=FORMAT` | md | Output: md, json, github-issue |
| `-o, --output=FILE` | stdout | Output file path |
| `--specs-dir=DIR` | kgfs | KGF specs directory |

**Workflow:**

1. Run `plan refactor` on each directory individually first to clean internal duplication
2. Run `plan solid --from=dirA,dirB` to find cross-directory extraction candidates
3. Extract shared code following the plan's recommendations
4. Use `indexion grep "TypeIdent:SharedType"` to verify all references are updated

### Phase 3: Remove unnecessary wrappers (`plan unwrap`)

After consolidation, clean up trivial delegation functions that add indirection without value.

```bash
# Step 1: Quick check
indexion grep --semantic=proxy src/

# Step 2: Detailed report
indexion plan unwrap --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' src/

# Step 3: Preview changes (safe — no files modified)
indexion plan unwrap --dry-run --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' src/

# Step 4: Apply fixes
indexion plan unwrap --fix --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' src/

# Step 5: Run tests
moon test --target native
```

**What gets detected:** Functions whose body is a single function call with
all arguments forwarded as simple identifiers — no control flow, no transforms.

```moonbit
// Detected (default) — trivial delegation
fn matches_pattern(text : String, pat : String) -> Bool {
  @glob.glob_match(text, pat)
}

// Excluded by default (use --all to include)
fn length(self : MyList) -> Int {
  self.items.length()    // self-delegation (encapsulation)
}
fn emit(value : String) -> Action {
  Emit(value)            // bare constructor
}
```

**`plan unwrap` modes:**

| Mode | Flag | Description |
|------|------|-------------|
| Report | (default) | List wrappers found |
| Preview | `--dry-run` | Show all edits without modifying files |
| Fix | `--fix` | Apply edits to files |

**`plan unwrap` options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--dry-run` | -- | Preview edits |
| `--fix` | -- | Apply edits |
| `--all` | -- | Include self-delegation and bare constructor wrappers |
| `--include-self` | -- | Include `self.field.method` patterns |
| `--include-bare` | -- | Include bare constructor wrappers |
| `--include=PATTERN` | -- | Include pattern (repeatable) |
| `--exclude=PATTERN` | -- | Exclude pattern (repeatable) |
| `--format=FORMAT` | md | Output: md, json, text |
| `-o, --output=FILE` | stdout | Output file path |
| `--specs-dir=DIR` | kgfs | KGF specs directory |

**Review before removing:**

- **Platform wrappers** (FFI, `@osenv_path`) are abstraction layers, not accidental indirection
- **Public API wrappers** used by external packages — removing them is a breaking change
- **Always `--dry-run` first**

### Phase 4: Detect concept-level duplication (`explore` + analysis)

This is the hardest level. Textual and structural tools won't find it because the
code is different — but the *concept* is the same.

```bash
# Find which files share vocabulary (= work in the same concept domain)
indexion explore --threshold=0.4 \
  --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' \
  src/ cmd/
```

Files at 40-60% similarity without structural duplication are **concept neighbors** —
they use the same terms because they deal with the same domain.

For each high-similarity pair, ask: **"What concept do they share, and who owns it?"**

```bash
# Inspect shared vocabulary with tree structure comparison
indexion explore file_a.mbt file_b.mbt --threshold=0 --strategy=apted
```

**Common patterns of concept leakage:**

| Symptom | Concept leaked | Fix |
|---------|---------------|-----|
| Both files call `is_X(spec)` then `Y::from_spec(spec)` | "Determine if X and configure Y" | Extract `try_do_X(path, spec)` into the module that owns X |
| Both files `@fs.read_file_to_string(path)` when content is already loaded | "Read file content" | Pass content as argument, don't re-read |
| Both files `parent_dir(path)` then `@fs.read_dir(dir)` | "List sibling files" | Centralize directory walking into pipeline |
| Multiple `if is_virtual_path(x) { skip }` guards | "Real vs virtual path" | Make the type system prevent virtual paths from reaching here |
| Both files `buf.write_string("\n"); buf.write_string(x)` | "Join text entries" | Extract `join_text_entries()` into the owning module |

### Phase 5: Consolidate into SoT

The module that **defines the concept** should be the only one that **implements the logic**.

Rules:
1. **One concept, one module, one function.** If "extract text from archive" appears in `vfs.mbt`, `discover.mbt`, and `args.mbt`, it belongs in `vfs.mbt` only.
2. **Callers receive results, not ingredients.** Don't export `is_archive_spec` + `ArchiveSpec::from_spec` + `expand_archive` separately. Export `try_extract_archive_text(path, spec) -> String?`.
3. **Guards are symptoms, not fixes.** `if is_virtual_path(x) { skip }` means virtual paths shouldn't reach here at all. Fix the source, not the sink.
4. **Re-reading from disk what's already in memory is a concept leak.** If `SupportedFile.content` holds the text, no downstream code should call `@fs.read_file_to_string(file.path)`.

### Phase 6: Verify

```bash
# Confirm textual duplication is gone
indexion plan refactor --threshold=0.9 \
  --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' \
  src/ cmd/indexion/

# Confirm concept similarity is reduced
indexion explore file_a.mbt file_b.mbt --threshold=0

# Confirm wrappers are cleaned up
indexion plan unwrap --include='*.mbt' --exclude='*_wbtest.mbt' \
  --exclude='*moon.pkg*' --exclude='*pkg.generated*' src/

# Run tests
moon test --target native
```

After SoT consolidation:
- Textual similarity between the concept owner and its callers drops
- Callers become shorter (one API call instead of multi-step logic)
- The concept owner may grow, but it's the **single place to change**

### Phase 7: Prove non-recurrence with tests

Write a test that **structurally prevents** the old pattern from recurring:

```moonbit
test "SoT: SupportedFile.path is always a real filesystem path" {
  // Create an archive, run load_supported_file_info
  // Assert: no path contains "!/"
  // Assert: every path passes @fs.path_exists
}
```

The test doesn't check behavior — it checks the **SoT invariant**.

## Red Flags

### "I need to add a guard here"

If you're adding `if is_special_case(x) { skip }` to a function that shouldn't receive
special cases, **the problem is upstream**. The function's caller should never pass that value.

### "It works but prints errors to stderr"

Stderr messages from C runtime (`opendir: No such file or directory`) mean invalid data
reached a system call. `catch` absorbs the error, but `perror()` already printed.
The only fix is preventing invalid data from reaching the call.

### "I'll fix it in each command separately"

If the same fix is needed in explore, search, grep, reconcile, plan documentation...
the fix belongs in the shared pipeline, not in each command.

### "The similarity is just shared vocabulary, not real duplication"

40-60% TF-IDF similarity between modules that aren't supposed to share concepts is a
warning. The vocabulary match IS the signal.

## Quick Reference: Which Command When

| Question | Command |
|----------|---------|
| "What files are similar?" | `explore --format=list` |
| "What exactly is duplicated?" | `plan refactor --threshold=0.9` |
| "What code overlaps between packages A and B?" | `plan solid --from=A,B` |
| "Which functions are trivial wrappers?" | `plan unwrap` or `grep --semantic=proxy` |
| "What concept do these files share?" | `explore file_a file_b --threshold=0 --strategy=apted` |
| "Has the duplication been fixed?" | Re-run `plan refactor` with same threshold |
