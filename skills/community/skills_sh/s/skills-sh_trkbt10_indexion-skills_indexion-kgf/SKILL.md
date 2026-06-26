---
name: indexion-kgf
description: Debug and inspect KGF specs — view tokenization results, parse trees, and extracted edges from source files. Use when adding/fixing language support or when indexion's analysis output looks wrong.
---

# indexion kgf

Inspect and debug KGF language specs by viewing tokens, parse events, and extracted edges.

## When to Use

- User wants to debug how indexion processes a specific file
- User is developing or modifying a KGF spec
- User asks "how does indexion parse this file?"
- Verifying that tokenization/parsing works correctly for a language
- **Debugging grep patterns**: when a grep pattern doesn't match, use
  `kgf tokens` to see the actual token kinds

## Subcommands

### `indexion kgf list` — List Installed Specs

```bash
indexion kgf list
```

### `indexion kgf update` — Update All Specs

Download the latest specs from GitHub.

```bash
indexion kgf update
```

### `indexion kgf add` — Install a Single Spec

```bash
indexion kgf add <spec-name>
```

### `indexion kgf inspect` — Full Inspection

Show tokens, events, and edges all at once.

```bash
indexion kgf inspect <file>
indexion kgf inspect --spec=typescript src/app.ts
```

### `indexion kgf tokens` — Tokenization Only

Show how a file is tokenized.

```bash
indexion kgf tokens <file>
indexion kgf tokens --spec=go-mod go.mod
```

### `indexion kgf events` — Parse Events Only

Show parse events generated from tokens.

```bash
indexion kgf events <file>
```

### `indexion kgf edges` — Extracted Edges Only

Show the dependency edges extracted from a file.

```bash
indexion kgf edges <file>
indexion kgf edges fixtures/project/npm/package.json
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--spec=NAME` | auto-detect | KGF spec name to use |
| `--kgf-dir=PATH` | kgfs | KGF specs directory |

## Relationship to grep

`indexion grep` uses KGF tokenization under the hood. Pattern aliases
(`pub` → `KW_pub`) are derived from the `=== lex` section of KGF specs.

When a grep pattern doesn't match as expected:

```bash
# 1. See the actual tokens for a file
indexion kgf tokens src/config/paths.mbt

# 2. Check which token kinds exist
indexion kgf tokens src/config/paths.mbt | head -20

# 3. Then adjust your grep pattern to match the actual token kinds
indexion grep "KW_pub KW_fn Ident" src/config/paths.mbt
```

Common token kinds (MoonBit):
- `KW_pub`, `KW_fn`, `KW_struct`, `KW_enum`, `KW_type`, `KW_trait`, `KW_let`, `KW_for`
- `Ident` (lowercase identifiers), `TypeIdent` (PascalCase type names)
- `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`, `LBRACKET`, `RBRACKET`
- `NL` (newline), `SKIP` (whitespace — filtered from grep patterns)
- `DocComment`, `DocLine`, `DocSection`, `LineComment`, `BlockComment`
- `String`, `Number`, `Char`

## Workflow

1. Run `indexion kgf inspect <file>` to see the full processing pipeline
2. If something looks wrong, drill down with `tokens`, `events`, or `edges`
3. Compare with the KGF spec file (`kgfs/<lang>.kgf`) to diagnose issues

## KGF Development Pitfalls

Common bugs found when writing or modifying KGF specs:

### PEG Item Ordering (first-match-wins)

KGF uses PEG parsing. In `Item -> A / B / C`, if A matches, B and C are
never tried. DocComment as a standalone alternative **before** declaration
rules will consume doc comments that should be attached to declarations.

```
# BAD: DocComment before FuncDecl — doc is consumed as standalone item
Item -> NL / DocComment / FuncDecl / Other

# GOOD: DocComment after declarations — FuncDecl's doc:DocComment? gets it
Item -> NL / FuncDecl / DocComment / Other
```

### NL Between Doc and Keyword

Source code has newlines between doc comments and declarations. Without
`NL?` or `NL*`, the optional doc capture fails silently:

```
# BAD: DocComment immediately followed by keyword — NL breaks the match
FuncDecl -> doc:DocComment? KW_fn id:Ident ...

# GOOD: NL? allows the typical newline between doc and keyword
FuncDecl -> doc:DocComment? NL? KW_fn id:Ident ...
```

### Bottom-Up Event Order (bind/scope)

Events fire bottom-up: child rules before parent rules. If ExportDecl
wraps FunctionDecl, FunctionDecl fires first. Use `bind`/`$scope` to
pass data from child to parent:

```
on FunctionDecl {
  bind ns "value" name "child_decl_id" to $id
  edge declares from $file to sym_id attrs obj(...)
}
on ExportDecl when $doc {
  let id = $scope("value", "child_decl_id")
  edge declares from $file to sym_id attrs obj("doc", $doc, ...)
}
```

### Token Priority Conflicts

Tokens defined earlier take priority. A generic `Operator /[=+\-*]+/`
before `EQ /=/` will consume `=` as Operator. Define specific tokens first:

```
# BAD: Operator matches = before EQ can
TOKEN Operator /[!$%&*+\-.\/:<=>?@^|~]+/
TOKEN EQ       /=/

# GOOD: EQ defined first, takes priority
TOKEN EQ       /=/
TOKEN Operator /[!$%&*+\-.\/:<=>?@^|~]+/
```

### Verifying Doc Extraction

After modifying a KGF, always verify doc appears in declares edges:

```bash
# Must show doc="..." in the declares edge
indexion kgf edges test_file.ts --spec=typescript | grep declares

# If doc is missing, check events to see where the DocComment went
indexion kgf events test_file.ts --spec=typescript | grep DocComment
```
