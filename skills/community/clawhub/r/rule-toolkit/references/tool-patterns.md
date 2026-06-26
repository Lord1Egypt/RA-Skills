# Tool Generation Patterns

Detailed patterns for converting constraint rules into automated tooling.

## ESLint Rules

### Code Style Rules

```javascript
// .eslintrc.cjs
module.exports = {
  rules: {
    // "No semicolons"
    semi: ["error", "never"],
    // "Single quotes"
    quotes: ["error", "single"],
    // "2 space indentation"
    indent: ["error", 2],
  }
};
```

### Naming Convention Rules

```javascript
// Custom rule for file naming (via eslint-plugin-filenames or no-restricted-syntax)
module.exports = {
  rules: {
    // "Files must be kebab-case"
    "filenames/match-regex": ["error", "^[a-z0-9\\-]+$"],
    // "Constants must be UPPER_SNAKE_CASE"
    "no-restricted-syntax": ["error", {
      selector: "VariableDeclaration[kind='const'] > VariableDeclarator > Identifier[name=/[a-z]/]",
      message: "Constants must use UPPER_SNAKE_CASE naming"
    }],
  }
};
```

### Import Rules

```javascript
module.exports = {
  rules: {
    // "No default exports"
    "import/no-default-export": "error",
    // "Always use @/ alias for src imports"
    "no-restricted-imports": ["error", {
      patterns: [{
        group: ["../*", "./*"],
        message: "Use @/ alias instead of relative imports"
      }]
    }],
    // "No imports from lodash, use lodash-es"
    "no-restricted-imports": ["error", {
      paths: [{
        name: "lodash",
        message: "Use lodash-es instead of lodash"
      }]
    }],
  }
};
```

### Security Rules

```javascript
module.exports = {
  rules: {
    // "No innerHTML"
    "no-restricted-properties": ["error", {
      object: "document",
      property: "innerHTML",
      message: "Use textContent or DOMPurify.sanitize() instead"
    }],
    // "No eval"
    "no-eval": "error",
    "no-implied-eval": "error",
  }
};
```

### Error Handling Rules

```javascript
module.exports = {
  rules: {
    // "No bare throw strings"
    "no-throw-literal": "error",
    // "Must handle promise rejections"
    "promise/no-return-wrap": "error",
  }
};
```

## Prettier Config

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

## TypeScript Strict Config

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Git Hooks

### Husky + lint-staged

```bash
# .husky/pre-commit
npx lint-staged
```

```bash
# .husky/commit-msg
npx commitlint --edit "$1"
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml}": ["prettier --write"]
  }
}
```

### Commitlint Config

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
};
```

## Wrapper Functions

### API Response Wrapper

```typescript
// src/utils/response.ts
export interface ApiResponse<T> {
  code: number;
  data: T | null;
  msg: string;
}

export function ok<T>(data: T): ApiResponse<T> {
  return { code: 0, data, msg: "success" };
}

export function fail(msg: string, code = -1): ApiResponse<null> {
  return { code, data: null, msg };
}
```

### Result Type (for error handling rules)

```typescript
// src/utils/result.ts
export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export function tryResult<T>(fn: () => T): Result<T> {
  try {
    return { ok: true, value: fn() };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e : new Error(String(e)) };
  }
}
```

## Validation Scripts

### Test Coverage Checker

```javascript
// scripts/check-test-coverage.js
const fs = require("fs");
const path = require("path");

function findFiles(dir, ext) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory() && entry.name !== "node_modules") {
      results.push(...findFiles(full, ext));
    } else if (entry.name.endsWith(ext)) {
      results.push(full);
    }
  }
  return results;
}

const srcFiles = findFiles("src", ".ts").filter(f => !f.includes(".test.") && !f.includes(".spec."));
const testFiles = findFiles("src", ".test.ts").concat(findFiles("src", ".spec.ts"));

const missing = srcFiles.filter(src => {
  const base = src.replace(/\.ts$/, "");
  return !testFiles.some(t => t.includes(base));
});

if (missing.length > 0) {
  console.error("Missing test files for:");
  missing.forEach(f => console.error(`  ${f}`));
  process.exit(1);
}
```

### File Length Checker

```javascript
// scripts/check-file-length.js
const fs = require("fs");
const MAX_LINES = 300;

const file = process.argv[2];
if (!file) { console.error("Usage: node check-file-length.js <file>"); process.exit(1); }

const lines = fs.readFileSync(file, "utf-8").split("\n").length;
if (lines > MAX_LINES) {
  console.error(`${file}: ${lines} lines (max ${MAX_LINES})`);
  process.exit(1);
}
```

## Python Tooling

### Ruff Config

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "SIM"]
# E=pycodestyle, F=pyflakes, I=isort, N=naming, UP=upgrade, B=bugbear, A=builtins, SIM=simplify

[tool.ruff.lint.isort]
known-first-party = ["myapp"]
```

### MyPy Strict Config

```toml
# pyproject.toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
```

## Rust Tooling

### Clippy Config

```toml
# Cargo.toml
[lints.clippy]
all = "warn"
pedantic = "warn"
nursery = "warn"
```

## Go Tooling

### golangci-lint Config

```yaml
# .golangci.yml
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gocritic
    - gofmt
    - goimports
```
