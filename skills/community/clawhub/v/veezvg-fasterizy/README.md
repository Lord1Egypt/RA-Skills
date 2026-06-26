<p align="center">
  <img src="img/fasterizy-img-0.svg" alt="fasterizy" height="120" />
</p>

<h1 align="center">fasterizy</h1>

<p align="center">
  <a href="https://www.npmjs.com/package/fasterizy"><img src="https://img.shields.io/npm/v/fasterizy.svg?color=blue" alt="npm"></a>
  <a href="https://github.com/felipeinf/fasterizy"><img src="https://img.shields.io/github/stars/felipeinf/fasterizy?style=social" alt="GitHub stars"></a>
</p>

**Fasterizy** is a **multi-agent skill** (one `SKILL.md`). It speeds up **work** in agent-assisted **workflows** by shortening the **time between turns**. Tuned for **Q&A, planning, and technical documentation** with technical accuracy and exact terminology.

## Install via skills.sh

Use [vercel-labs/skills](https://github.com/vercel-labs/skills) and `npx skills add`. The same skill ships to many agents (for example Claude Code, Codex, Cursor, OpenCode, Windsurf, Copilot, Antigravity, Cline, and others the toolchain supports).

```bash
npx skills add felipeinf/fasterizy -a opencode
```

Replace `opencode` with your agent flag.

## Native plugins

**Claude Code**

```
/plugin marketplace add felipeinf/fasterizy
/plugin install fasterizy@fasterizy
```

**Codex**

```
/plugin marketplace add felipeinf/fasterizy
/plugin install fasterizy@fasterizy
```

## Install via CLI

```bash
npx fasterizy install
```

Also: `update`, `start`, `stop`, `status`, `-h`.

## Chat

`/fasterizy` toggles on · `/fasterizy on` · `/fasterizy off`

## License

MIT. See [LICENSE](LICENSE).
