# Code to Documentation Mapping

Strategies for discovering which documentation files correspond to changed source code in any project.

## Discovery Strategies

### Strategy 1: Search by Symbol Name

The most reliable approach — grep for the name of the changed function, class, component, or config option in the documentation directory.

```
# Using the Grep tool:
# Pattern: the exported symbol name (e.g., "createServer", "useRouter", "Config")
# Path: the project's documentation directory
# Glob: *.md, *.mdx, *.rst, *.adoc (match the project's doc format)
```

This catches docs that reference the symbol regardless of how the doc directory is organized.

### Strategy 2: Search by File/Module Path

Docs often reference source file paths or import paths. Search for the changed file's path or module name in docs.

```
# Using the Grep tool:
# Pattern: the module path (e.g., "from mylib.utils", "require('mylib/utils')")
# Path: the project's documentation directory
```

### Strategy 3: Co-located Documentation

Many projects keep documentation alongside source code:

| Pattern                  | Description                          |
| ------------------------ | ------------------------------------ |
| `src/feature/README.md`  | Feature-level documentation          |
| `src/feature/docs/`      | Dedicated docs folder per feature    |
| Inline doc comments       | JSDoc, docstrings, rustdoc, godoc   |
| `CHANGELOG.md` at root    | Project-level change log            |

Check for README or doc files in the same directory (or parent directory) as the changed source files.

### Strategy 4: Directory Convention Mapping

Many projects have a parallel structure between source and docs. Look for patterns like:

| Source Directory       | Potential Doc Directory              |
| ---------------------- | ------------------------------------ |
| `src/components/`      | `docs/components/` or `docs/api/components/` |
| `src/api/`             | `docs/api-reference/`                |
| `src/cli/`             | `docs/cli/` or `docs/commands/`      |
| `lib/`                 | `docs/api/` or `docs/reference/`     |
| `packages/<name>/`     | `docs/<name>/` or `docs/packages/<name>/` |
| `src/config/`          | `docs/configuration/`                |

These are heuristics — verify by checking the actual project structure.

### Strategy 5: Git History Correlation

Files that are frequently changed together often have a code-to-docs relationship.

```bash
# Find files commonly changed alongside a source file
git log --pretty=format: --name-only --follow -- path/to/source/file.ts | sort | uniq -c | sort -rn | head -20
```

Look for documentation files that appear in the same commits as the source file.

### Strategy 6: Documentation Build Configuration

Some documentation systems explicitly declare which source files to document:

- **Sphinx autodoc**: `conf.py` lists modules to document
- **TypeDoc/JSDoc**: Config files specify source entry points
- **Swagger/OpenAPI**: Specs map to API endpoints in source
- **Storybook**: Story files map directly to component source

Check these configs to find explicit source-to-doc mappings.

## Finding Documentation Directories

### Common Locations

Search for documentation in these standard locations:

| Directory            | Typical Use                            |
| -------------------- | -------------------------------------- |
| `docs/`              | Most common documentation root         |
| `documentation/`     | Alternative name                       |
| `doc/`               | Common in Ruby, C/C++ projects         |
| `site/`              | Built documentation output             |
| `website/`           | Separate documentation site source     |
| `content/`           | Hugo, some static site generators      |
| `pages/`             | Some documentation frameworks          |
| `wiki/`              | GitHub wiki-style docs                 |
| `man/`               | Unix manual pages                      |
| `guides/`            | Tutorial-style documentation           |

### Monorepo Patterns

In monorepos, documentation may be:

- **Centralized**: One `docs/` at the repo root covering all packages
- **Distributed**: Each package has its own `docs/` or `README.md`
- **Hybrid**: Root `docs/` for guides, per-package READMEs for API reference

Check `packages/*/README.md`, `packages/*/docs/`, and the root `docs/` directory.

## Building a Project-Specific Mapping

When working with a new project, build a mental mapping by:

1. **List the docs directory structure**: Use Glob to see how docs are organized
2. **Read a few representative docs**: Understand how they reference source code
3. **Check for auto-generated docs**: Look for "generated" markers — if present, find the source template/config instead
4. **Identify the naming pattern**: Do doc filenames match source filenames? Module names? Feature names?
5. **Check for a docs contribution guide**: Many projects have `CONTRIBUTING.md` or similar that explains doc structure

## Common Patterns by Ecosystem

### JavaScript/TypeScript
- API docs often generated from JSDoc/TSDoc comments in source
- Framework docs in `docs/` with MDX format
- README-driven documentation for smaller packages

### Python
- Sphinx docs in `docs/` with `.rst` files and `conf.py`
- Docstrings in source code auto-extracted by Sphinx autodoc
- `mkdocs.yml` with Markdown for newer projects

### Go
- Godoc comments in source are the primary documentation
- Additional docs in `docs/` or project wiki
- `README.md` per package

### Rust
- Rustdoc comments (`///`) in source are primary
- Book-style docs using mdBook in `docs/` or `book/`
- `README.md` per crate

### Java/Kotlin
- Javadoc/KDoc comments in source
- Additional docs in `docs/` or wiki
- AsciiDoc format common in Spring ecosystem

## Quick Search Commands

Use Claude's built-in tools for efficient discovery:

- **Find all documentation files**: Use Glob with patterns like `docs/**/*.md`, `**/*.rst`
- **Find docs mentioning a symbol**: Use Grep with the symbol name, scoped to the docs directory
- **Find auto-generated markers**: Use Grep with patterns like `generated`, `do not edit`, `auto-generated`
- **Find documentation config**: Use Glob with patterns like `**/mkdocs.yml`, `**/docusaurus.config.*`, `**/conf.py`
- **List docs directory structure**: Use Glob with `docs/**/*` to see the full tree
