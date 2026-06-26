# Contributing Generator

Analyze project structure and settings to auto-generate a CONTRIBUTING.md file.

## Trigger

- "CONTRIBUTING generate", "CONTRIBUTING.md create"
- "contributing guide", "contribution guide"
- After initial project setup

## Analysis Targets

| File/Directory | Extracted Info |
|---------------|---------------|
| package.json | Scripts, package manager, lint config |
| pnpm-workspace.yaml | Monorepo structure |
| .editorconfig | Code style |
| eslint.config.js | Lint rules |
| .husky/ | Pre-commit hooks |
| tsconfig.json | TypeScript config |

## Workflow

### Step 1: Detect Project Type

```bash
# Monorepo check
ls pnpm-workspace.yaml 2>/dev/null && echo "monorepo"

# Package manager
cat package.json | grep packageManager
```

Project types:
- Single package
- pnpm monorepo
- npm workspaces

### Step 2: Analyze Config Files

```bash
# package.json scripts
cat package.json | jq '.scripts'

# EditorConfig settings
cat .editorconfig

# Prettier settings
cat package.json | jq '.prettier'
```

### Step 3: Detect Directory Structure

```bash
# Source structure
ls -la src/ packages/

# Monorepo package list
ls packages/
```

### Step 4: Generate CONTRIBUTING.md

## Template Structure

```markdown
# Contributing to {project-name}

Thank you for contributing!

## Development Setup

### Requirements
{detected-requirements}

### Installation
{installation-commands}

## {Project Structure / Monorepo Structure}
{directory-tree}

## Code Style

### EditorConfig
{editorconfig-summary}

### ESLint & Prettier
{lint-config-summary}

### Running Lint
{lint-commands}

## Commit Convention
{commit-convention}

## Pre-commit Hook
{husky-config}

## Build & Development
{build-commands}

## Pull Request Guide
{pr-guide}

## License
{license-info}
```

## Detection Patterns

### Requirements Section

```javascript
// package.json engines field
{
  "engines": {
    "node": ">=22"
  },
  "packageManager": "pnpm@9.15.9"
}
```

Output:
```markdown
### Requirements

- Node.js 22+
- pnpm 9.15.0+ (managed via corepack)
```

### Code Style Section

EditorConfig detection:
```ini
indent_style = space
indent_size = 2
end_of_line = lf
```

Output:
```markdown
### EditorConfig

- **Indent:** 2 spaces
- **End of Line:** LF
- **Charset:** UTF-8
```

### Build Commands Section

package.json scripts detection:
```json
{
  "scripts": {
    "build": "pnpm -r build",
    "dev": "pnpm --filter @scope/web dev"
  }
}
```

Output:
```markdown
### Full Build

\`\`\`bash
pnpm build
\`\`\`

### Development

\`\`\`bash
pnpm dev
\`\`\`
```

## Monorepo-Specific Sections

### Package Dependencies Diagram

```
@scope/core (no dependencies)
        |
@scope/web (depends on core)
        |
package-mcp (depends on core)
```

### Build Order

```bash
# Build in dependency order
pnpm --filter @scope/core build
pnpm --filter @scope/web build
pnpm --filter package-mcp build
```

## Commit Convention Template

```markdown
## Commit Convention

Follow **Conventional Commits** format:

\`\`\`
<type>(<scope>): <subject>
\`\`\`

### Types

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Add/update tests
- `chore:` Build process, tooling

### Scope Examples

{detected-scopes}
```

## Output

Save generated CONTRIBUTING.md to project root:

```bash
# Create file
Write tool -> ./CONTRIBUTING.md

# If existing file, confirm with user
AskUserQuestion: "Overwrite existing CONTRIBUTING.md?"
```

## Notes

1. **Check existing file**: Confirm before overwriting
2. **Reflect project specifics**: Only include detected settings
3. **Language setting**: Match project language (Korean/English)
4. **License check**: Verify LICENSE file existence
