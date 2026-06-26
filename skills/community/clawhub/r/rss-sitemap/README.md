# rss-sitemap

Este skill descobre URLs de um site usando `sitemap.xml`, `sitemaps.xml`,
`atom.xml`, `rss.xml` e diretivas `Sitemap:` em `robots.txt` antes de cair para
crawl normal.

O script local fica em:

```bash
node skills/rss-sitemap/scripts/preprocess-rss-sitemap.js --site https://example.com --output /tmp/rss-sitemap.json
```

## Requisitos do skill

No `SKILL.md`, declare o binario usado pelo script:

```yaml
metadata: '{"openclaw":{"requires":{"bins":["node"]}}}'
```

O agente deve executar o script pela ferramenta OpenClaw `exec`. Nao existe uma
ferramenta separada chamada `bash`; em OpenClaw, `bash` eh apenas alias de
politica para `exec`.

## Politica global de exec

Para execucao local no host, sem Docker, use:

```bash
openclaw config set tools.exec.host gateway
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.ask on-miss
openclaw config set tools.exec.strictInlineEval true --strict-json
openclaw gateway restart
```

## WhatsApp

Para permitir este tipo de skill em grupos WhatsApp, o grupo precisa enxergar a
ferramenta `exec`. Nao libere `group:runtime` inteiro se voce so precisa rodar
scripts aprovados; deixe `process` e `code_execution` bloqueados.

Exemplo de patch para o wildcard de grupos WhatsApp:

```bash
openclaw config patch --stdin <<'JSON5'
{
  channels: {
    whatsapp: {
      groups: {
        "*": {
          tools: {
            deny: [
              "group:automation",
              "group:fs",
              "process",
              "code_execution",
              "shell",
              "apply_patch",
              "edit",
              "write",
              "delete",
              "gateway",
              "nodes",
              "sessions_spawn",
              "sessions_send",
            ],
          },
        },
      },
    },
  },
}
JSON5

openclaw gateway restart
```

Se voce usa `channels.whatsapp.accounts.<conta>.groups`, aplique o mesmo bloco
nesse caminho tambem. Politicas por conta podem sobrescrever a politica raiz.

## Autorizar o script corretamente

Metodo mais simples: peca pelo WhatsApp para o agente usar `$rss-sitemap`. Se o
OpenClaw pedir aprovacao, responda no chat:

```text
/approve <id> allow-always
```

Use `allow-once` para uma execucao unica. Use `allow-always` para persistir a
autorizacao daquele comando/padrao.

Metodo CLI restrito para preautorizar este script sem liberar `node` inteiro:

```bash
openclaw approvals get --gateway --json \
| node -e 'let input=""; process.stdin.on("data", c => input += c); process.stdin.on("end", () => { const snapshot = JSON.parse(input); const file = snapshot.file || snapshot; file.version = file.version || 1; file.defaults = file.defaults || {}; file.agents = file.agents || {}; const agent = file.agents["*"] || {}; const allowlist = Array.isArray(agent.allowlist) ? agent.allowlist : []; const entry = { pattern: "node", argPattern: "^(?:skills\\/rss-sitemap\\/scripts\\/preprocess-rss-sitemap\\.js|\\/home\\/carlosdelfino\\/workspace\\/openclaw-workspace\\/skills\\/rss-sitemap\\/scripts\\/preprocess-rss-sitemap\\.js)(?:\\s+.*)?$", source: "allow-always" }; if (!allowlist.some(item => item && item.pattern === entry.pattern && item.argPattern === entry.argPattern)) allowlist.push(entry); agent.allowlist = allowlist; file.agents["*"] = agent; process.stdout.write(JSON.stringify(file, null, 2)); });' \
| openclaw approvals set --gateway --stdin
```

Esse padrao permite somente comandos `node` cujo primeiro argumento seja o
script `skills/rss-sitemap/scripts/preprocess-rss-sitemap.js` ou o mesmo caminho
absoluto neste workspace.

Verifique:

```bash
openclaw approvals get --gateway
openclaw exec-policy show
openclaw skills check --agent main --json
```

## Modelo para outros skills com scripts

1. Coloque o script dentro do diretorio do skill, por exemplo
   `skills/meu-skill/scripts/run.js`.
2. Declare os binarios em `metadata.openclaw.requires.bins`.
3. Instrua o agente a usar `exec`, nao `bash`.
4. Mantenha `tools.exec.security=allowlist` e `tools.exec.ask=on-miss`.
5. Para WhatsApp, permita `exec` no grupo, mas mantenha `process`,
   `code_execution`, `gateway`, `nodes` e ferramentas de escrita bloqueadas.
6. Autorize o runtime com `argPattern` preso ao script do skill. Evite allowlist
   ampla como apenas `node` ou `python3` sem restringir argumentos.
