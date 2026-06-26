# React Modernization

Upgrade React applications from class components to hooks, adopt concurrent features, and migrate between major versions.

## What's Inside

- Version upgrade paths (React 17→18, 18→19 breaking changes)
- Class-to-hooks migration with lifecycle method mappings
- State migration patterns (class state to useState/useEffect)
- HOC to custom hook migration
- React 18+ concurrent features (createRoot, useTransition, Suspense)
- React 19 features (use() hook, actions, ref as prop, Context as provider)
- Automated codemods for bulk refactoring
- TypeScript migration for React components
- Pre/post migration checklists

## When to Use

- Migrating class components to functional components with hooks
- Upgrading React 16/17 apps to React 18/19
- Adopting concurrent features (Suspense, transitions, use)
- Converting HOCs and render props to custom hooks
- Adding TypeScript to React projects

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/frontend/react-modernization
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-modernization
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/frontend/react-modernization .cursor/skills/react-modernization
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/frontend/react-modernization ~/.cursor/skills/react-modernization
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/frontend/react-modernization .claude/skills/react-modernization
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/frontend/react-modernization ~/.claude/skills/react-modernization
```

---

Part of the [Frontend](..) skill category.
