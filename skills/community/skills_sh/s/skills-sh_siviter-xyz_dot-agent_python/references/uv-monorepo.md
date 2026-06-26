# Python Monorepo Guidelines

Guidelines for Python monorepos managed by `uv` with Hatch as the build system.

## Project Structure

### Layout

- Root workspace at repository root
- Packages under `packages/` directory
- Shared config in root `pyproject.toml`
- Workspace tasks in root `justfile`
- Package tasks in individual `justfiles`

### Package Structure

Required structure for each package:

```
packages/<package-name-kebab-case>/
├── pyproject.toml         # Config and dependencies
├── justfile               # Package-specific tasks
├── src/
│   └── <package_name_snake_case>/  # Python module
│       ├── main.py
│       └── <submodule>/   # Submodules in snake_case
└── tests/                 # Mirrors src structure
    └── _integration/      # Integration tests (if package exposes API/CLI/interface etc)
```

**Naming**: Directories use kebab-case; Python modules and submodules use snake_case

## Build System

- **Build backend**: Hatch (pypa/hatch)
- **Versioning**: hatch-vcs (ofek/hatch-vcs) from git tags
- Package versions auto-derived from git tags

## Dependency Management

- **Tool**: ALWAYS use `uv`. NEVER use pip or other tools directly
- **Root dependencies**: Available to all packages
- **Sync**: Use `uv sync` to install/sync
- **Package dependencies**: Specify in individual `pyproject.toml`
- **Dev dependencies**: Use `[dependency-groups]` in `pyproject.toml`

## Package Organization

### Cross-Package Dependencies

- Reference workspace packages in `pyproject.toml`
- Extract common functionality into a shared core package
- Establish clear dependency hierarchy; avoid circular dependencies

### Package Boundaries

- Each package is independently buildable and testable
- Expose only necessary APIs or CLIs through public interfaces
- Keep implementation details private within modules
- Place shared utilities in dedicated packages

## Testing

### Integration Tests

- Packages exposing APIs or CLIs should include integration tests
- Place integration tests in `tests/_integration/` directory
- Integration tests verify end-to-end behavior of public interfaces
- Keep integration tests in the package that exposes the functionality
- Integration tests with costs, or involved setup, should be enabled through an environment variable
