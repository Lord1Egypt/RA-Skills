---
name: monitor-tom-doerr
description: Monitor Tom Doerr's X.com profile for new posts and share on Telegram/Twitter. Use when: (1) User asks to monitor Tom Doerr, (2) Cron job runs for periodic checks, (3) Checking for new GitHub repos shared by Tom Doerr. Includes workflow for posting to Twitter with proper GitHub link verification.
---

# Monitor Tom Doerr

Workflow para monitorar posts do Tom Doerr no X.com e compartilhar repositórios interesantes.

## Processo Completo

### 1. Verificar novos posts
1. Abrir browser (se não estiver aberto): `openclaw browser --browser-profile openclaw start`
2. Navegar para `https://x.com/tom_doerr`
3. Verificar o primeiro post (mais recente)
4. Comparar ID com último post salvo em `memory/rotinas.md`

### 2. Verificar link do GitHub (CRÍTICO!)

**Dois métodos para descobrir o link real:**

**Método 1 (recomendado): Usar o link t.co do post**
1. No browser, clicar no link do post (o link encurtado t.co)
2. Ver para onde redireciona no URL do navegador
3. Exemplo: `t.co/nDOuPnyZXv` → `github.com/afterxleep/agents`

**Método 2: Buscar no GitHub**
1. Acessar o usuário/organização no GitHub (ex: github.com/afterxleep)
2. Buscar o repo correto pelo nome ou descrição
3. Confirmar o nome exato do repo

**Por que isso é importante:**
- O X mostra links truncados/encurtados no texto do post
- O link real pode ser diferente do mostrado!
- Exemplos de erros passados:
  - ❌ Errado: `github.com/afterxleep/age` (não existe)
  - ✅ Certo: `github.com/afterxleep/agents` (existe!)
  - ❌ Errado: `github.com/Yqnn/svg-path-` (truncado)
  - ✅ Certo: `github.com/Yqnn/svg-path-editor` (existe!)

### 3. Traduzir e reescrever para alcance
- Traduzir para português brasileiro
- Usar emojis relevanetes
- Adicionar hashtags: #IA #GitHub #Tech #OpenSource
- Descrição chamativa

### 4. Enviar para aprovação (Telegram)
- Primeiro enviar para o Telegram do Gabriel
- Esperar aprovação antes de postar no X

### 5. Postar no X (se aprovado)

**⚠️ PASSO A PASSO CORRETO (testado em 2026-03-06):**

1. Acessar `https://x.com/compose/post`
2. **Esperar a página carregar completamente** (dialog precisa aparecer)
3. No dialog que abre:
   - Textbox do post: `ref=e93` (dentro do dialog)
   - Botão Post: `ref=e170` (dentro do dialog, não o da timeline principal!)
4. Digitar o texto usando `kind: "type"` no textbox ref=e93
5. **AGUARDAR** o botão Post ficar habilitado (cursor=pointer, não disabled)
6. **FECHAR qualquer listbox/overlay** com `Escape` antes de clicar
7. Clicar no botão Post (ref=e170) com `kind: "click"`
8. **VERIFICAR** se o post apareceu na timeline (confirma sucesso)

**Estrutura da página (importante!):**
```
- dialog (ref=e20)
  - textbox "Post text" (ref=e93) ← DIGITAR AQUI
  - button "Post" (ref=e170) ← CLI AQUI (dentro do dialog!)
```

**🔑 Pontos críticos aprendidos (2026-03-06):**
- O dialog tem sua própria textbox (ref=e93) e botão Post (ref=e170)
- NÃO usar os elementos da timeline principal (outro textbox e botão)
- Sempre fechar listboxes de hashtags com Escape antes de clicar Post
- Se o click não funcionar, tentar pressionar Enter apósdigitar
- Snapshot mostra a estrutura completa - usar refs corretos do dialog

**Se automação falhar:**
- Enviar msg no Telegram pedindo para postar manualmente
- O texto já está pronto para colar

## Arquivos de referência

- **Último post enviado:** `memory/rotinas.md`
- **Instruções detalhadas:** `memory/instrucoes-tom-doerr.md`

## Cron Job

O monitoramento automático roda a cada 1 hora via:
```
openclaw cron add --name "monitor-tom-doerr" --every 1h --message "..." --channel telegram --to 1225303431 --announce
```
