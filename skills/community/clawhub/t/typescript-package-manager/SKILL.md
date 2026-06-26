---
name: typescript-package-manager
description: 'Expert 10x Software engineer specializing in TypeScript with deep knowledge of all popular package management tools including npm, yarn, pnpm, bun, and deno. Use when asked to configure package managers, manage dependencies, set up workspaces, resolve package conflicts, optimize package.json files, troubleshoot installation issues, or work with monorepos. Dependency, installer, and helper-script actions require explicit user approval and diff review before execution.'
---

# TypeScript Package Manager Skill

An expert skill for managing TypeScript projects with comprehensive knowledge of modern package management tools and ecosystem best practices. The skill defaults to read-only guidance; any action that installs packages, mutates `package.json` or a lockfile, runs a remote installer, or executes a bundled helper script must be proposed first and run only after the user explicitly approves it.

## Safety and Trust Model

- **Inspect before executing.** The bundled helpers under `scripts/` (notably `bun-workflow.js.txt` and `health-check.js.txt`) shell out to local tools via `child_process.execSync`. They ship with a `.js.txt` extension so they are not directly executable; open and read each one, rename it back to `.js` only inside a trusted project working directory you control, and run it only after confirming the exact command.
- **Verify remote installers.** Any documented one-liner that fetches code from the network (for example `curl -fsSL https://bun.sh/install | bash` or `powershell -c "irm bun.sh/install.ps1 | iex"`) executes whatever the upstream serves at that moment. Confirm the URL, prefer the official downloaded installer or your OS package manager, and pin to a known version when stricter review is required.
- **Approve dependency changes explicitly.** Treat installs, updates, removals, audits with `--fix`, and lockfile regenerations as mutating actions. Surface the exact command and the expected `package.json` / lockfile diff first, then proceed only after the user confirms.
- **Provenance disclosure.** The helper scripts in this skill are local to this repository and are not currently published with an upstream source or homepage in the registry metadata. Treat them as untrusted code until you have read them, and prefer skills with clear provenance when execution is involved.

## When to Use This Skill

- Setting up or configuring package managers (npm, yarn, pnpm, bun, deno)
- Managing project dependencies and resolving conflicts
- Optimizing package.json configuration
- Working with monorepos and workspaces
- Troubleshooting installation or dependency issues
- Configuring package scripts and build pipelines
- Understanding lock files and version constraints
- Integrating package managers with build tools
- Migrating between package managers
- Performance optimization of package operations

## Prerequisites

- Node.js environment (for npm, yarn, pnpm, bun)
- Basic understanding of TypeScript/JavaScript projects
- Terminal/command line access
- Understanding of semantic versioning (semver)

## Shorthand Keywords

Keywords to trigger this skill quickly:

```javascript
openPrompt = ["typescript-package-manager", "ts-pkg", "pkg-manager"]
```

Use these shorthand commands for quick invocation:

- `ts-pkg --install <package>`
- `pkg-manager --compare-tools`
- `ts-pkg migrate to pnpm`
- `pkg-manager --optimize workspace`

## Core Capabilities

### Package Manager Expertise

This skill provides deep knowledge across all major JavaScript/TypeScript package managers:

- **npm**: The default Node.js package manager, widely used and battle-tested
- **yarn**: Fast, reliable package manager with enhanced features
- **pnpm**: Disk-space efficient with strict dependency isolation
- **bun**: Ultra-fast all-in-one toolkit with native package management
- **deno**: Secure-by-default runtime with built-in tooling

### Dependency Management

All of the following are mutating operations: propose the exact command, show the expected `package.json` and lockfile diff, and execute only after explicit user approval.

- Installing, updating, and removing dependencies (requires approval and diff review)
- Managing dev dependencies vs production dependencies
- Understanding peer dependencies and optional dependencies
- Resolving version conflicts and compatibility issues
- Audit and security vulnerability management (read-only by default; `--fix` flags require approval)
- Dependency deduplication and optimization

### Configuration and Optimization

- package.json structure and best practices
- Lock file management (package-lock.json, yarn.lock, pnpm-lock.yaml)
- Workspace and monorepo configuration
- Scripts and lifecycle hooks
- Registry configuration and private packages
- CI/CD integration

### Ecosystem Integration

- TypeScript compiler (tsc) integration with package managers
- Build tool configuration (Vite, webpack, esbuild, Rollup, Turbopack)
- Testing framework setup (Vitest, Jest, Mocha)
- Linting and formatting tools (ESLint, Prettier)
- Development server configuration and hot reload
- CI/CD pipeline optimization

## Key Concepts

### Semantic Versioning (semver)

Understanding version constraints in package.json:

- **^1.2.3** (caret): >=1.2.3 <2.0.0 - Allows minor and patch updates (recommended)
- **~1.2.3** (tilde): >=1.2.3 <1.3.0 - Allows only patch updates
- **1.2.3** (exact): Exact version only
- **>=1.2.3 <2.0.0** (range): Custom version range
- **latest**: Always use latest version (dangerous, not recommended)

### Lock Files

Lock files ensure reproducible installations across environments:

- **package-lock.json** (npm): JSON format, exact dependency tree
- **yarn.lock** (yarn): YAML-like format, deterministic resolution
- **pnpm-lock.yaml** (pnpm): YAML format with content-addressable storage
- **bun.lockb** (bun): Binary format for fast parsing

**Best Practice:** Always commit lock files to version control.

### Workspaces (Monorepos)

Manage multiple packages in a single repository:

```json
{
  "workspaces": ["packages/*", "apps/*"]
}
```

**Benefits:**
- Shared dependencies across packages
- Cross-package development and testing
- Unified versioning and release coordination
- Simplified dependency management

## Best Practices

1. **Choose the Right Tool**: Understand trade-offs between package managers for your project needs
   - npm: Maximum compatibility, widest ecosystem support
   - yarn: Enhanced features, good monorepo support
   - pnpm: Best disk space efficiency, strict dependencies
   - bun: Maximum speed, all-in-one tooling
   - deno: Security-first, URL-based imports

2. **Lock File Discipline**: Always commit lock files to ensure reproducible builds across environments

3. **Semantic Versioning**: Use appropriate version constraints
   - Use `^` (caret) for most dependencies (recommended)
   - Use `~` (tilde) for conservative updates
   - Use exact versions only when necessary

4. **Security First**: Regularly audit dependencies for vulnerabilities
   ```bash
   npm audit      # npm
   yarn audit     # yarn
   pnpm audit     # pnpm
   bun pm audit   # bun
   ```

5. **Workspace Optimization**: Leverage workspaces for monorepo efficiency and shared dependencies

6. **Script Consistency**: Use cross-platform compatible scripts (avoid shell-specific commands)

7. **Minimal Dependencies**: Avoid unnecessary packages to reduce complexity, security surface, and bundle size

8. **Documentation**: Document package manager choice, special configurations, and setup instructions in README.md

9. **CI/CD Optimization**: Use frozen lockfiles in CI for deterministic builds
   ```bash
   npm ci                                    # npm
   yarn install --frozen-lockfile            # yarn
   pnpm install --frozen-lockfile            # pnpm
   bun install --frozen-lockfile             # bun
   ```

10. **Version Management**: Use `packageManager` field in package.json to enforce consistency
    ```json
    {
      "packageManager": "pnpm@8.15.0"
    }
    ```

## Choosing the Right Package Manager

### Decision Factors

**npm (Default Choice)**
- ✅ Maximum compatibility and ecosystem support
- ✅ Default with Node.js, no additional setup
- ✅ Well-tested and mature
- ❌ Slower than alternatives
- ❌ Less disk-efficient

**yarn (Enhanced Features)**
- ✅ Good performance and caching
- ✅ Excellent monorepo/workspace support
- ✅ Plug'n'Play mode (Berry) for zero-installs
- ❌ Classic vs Berry version confusion
- ❌ Plug'n'Play requires IDE setup

**pnpm (Recommended for Most Projects)**
- ✅ 60-70% disk space savings
- ✅ 2-3x faster than npm
- ✅ Strict dependency isolation prevents phantom dependencies
- ✅ Excellent monorepo support
- ❌ May expose hidden dependency issues

**bun (Cutting Edge)**
- ✅ Blazing fast (5-10x faster than npm)
- ✅ All-in-one: runtime, bundler, test runner
- ✅ Native TypeScript support
- ❌ Newer and less mature
- ❌ Some npm package incompatibilities

**deno (Security-First)**
- ✅ Secure by default with explicit permissions
- ✅ Native TypeScript support
- ✅ No package.json or node_modules
- ❌ Different paradigm (URL-based imports)
- ❌ Smaller ecosystem than npm

### Quick Recommendation

- **New TypeScript project**: pnpm or bun
- **Existing project**: Keep current manager unless migrating for specific benefits
- **Monorepo**: pnpm or yarn (berry)
- **Maximum compatibility**: npm
- **Security-critical**: deno or pnpm

## Common Tasks

### Installing Dependencies

```bash
# npm
npm install

# yarn
yarn install

# pnpm
pnpm install

# bun
bun install
```

### Adding New Dependencies

```bash
# Production dependency
npm install package-name
yarn add package-name
pnpm add package-name
bun add package-name

# Development dependency
npm install --save-dev package-name
yarn add --dev package-name
pnpm add --save-dev package-name
bun add --dev package-name
```

### Running Scripts

```bash
# All package managers support npm scripts
npm run script-name
yarn script-name
pnpm script-name
bun run script-name
```

## Troubleshooting

### Common Issues

**Installation Failures**:
- Clear cache and retry
- Delete node_modules and lock file, reinstall
- Check for incompatible peer dependencies
- Verify Node.js version compatibility

**Version Conflicts**:
- Use resolutions/overrides in package.json
- Upgrade conflicting dependencies
- Consider using pnpm for better isolation

**Performance Issues**:
- Use pnpm or bun for faster operations
- Enable caching mechanisms
- Optimize workspace configuration

**Lock File Conflicts**:
- Resolve merge conflicts carefully
- Regenerate lock file if corrupted
- Ensure team uses same package manager

## References

See the `references/` folder for detailed documentation:

- **package-management.md** - Comprehensive guide to JavaScript/TypeScript package managers including npm, yarn, pnpm, bun, deno, with concepts, version management, security, and best practices
- **integration-with-build-tools.md** - Complete guide to integrating package managers with Vite, webpack, esbuild, Rollup, TypeScript compiler (tsc), and CI/CD pipelines

## Scripts

See the `scripts/` folder for workflow guides and automation. The helper sources ship with a `.js.txt` extension so they are inert until a user explicitly renames them to `.js`; they execute local shell commands through `child_process.execSync` (for example `bun-workflow.js.txt` line 45 and `health-check.js.txt` line 47 to detect tool versions). Read each helper before renaming, run it only inside a trusted project directory, and prefer the `.md` walkthroughs when you only need reference material.

- **npm-workflow.md** / **npm-workflow.js.txt** - Complete npm workflow from initialization to publishing (rename to `.js` before running with Node)
- **yarn-workflow.md** - Complete yarn workflow covering Classic (1.x) and Berry (3.x+) versions
- **pnpm-workflow.md** - Complete pnpm workflow with monorepo and workspace features
- **bun-workflow.md** / **bun-workflow.js.txt** - Complete bun workflow for ultra-fast package management (rename to `.js` before running). The documented Bun installer one-liners (`curl … | bash`, `irm … | iex`) fetch and execute remote code; verify the source URL and prefer a pinned, downloaded installer when stricter review is required.
- **health-check.md** / **health-check.js.txt** - Package manager health check and diagnostics scripts (rename to `.js` before running)

## Assets

See the `assets/` folder for templates and reference materials:

- **package-manager-comparison.md** - Detailed comparison matrix, benchmarks, and decision tree for choosing package managers
- **package-json-template.md** - Production-ready package.json template with field-by-field explanations and best practices
