# Telegram Native Audio - modo automático local

## Objetivo

Implementar a etapa C sem webhook: um watcher local que processa áudios recebidos via pasta de entrada.

## Pastas

- Inbox: `/root/.picoclaw/workspace/state/telegram-native-audio/inbox`
- Outbox: `/root/.picoclaw/workspace/state/telegram-native-audio/outbox`
- Processados: `/root/.picoclaw/workspace/state/telegram-native-audio/processed`
- Estado: `/root/.picoclaw/workspace/state/telegram-native-audio/state.json`

## Como funciona

1. Um arquivo de áudio é colocado em `inbox/`.
2. `auto_runner.py` detecta o arquivo.
3. Chama `runner.py process <arquivo>`.
4. Gera:
   - transcrição;
   - resposta textual;
   - mp3 de resposta.
5. Move o áudio original para `processed/`.
6. Salva na `outbox/`:
   - um `.mp3` com a resposta;
   - um `.json` com metadados.

## Executar manualmente

```bash
python3 /root/.picoclaw/workspace/skills/telegram-native-audio/scripts/auto_runner.py
```

## Integração com Telegram nativo

Próxima conexão prática no runtime:
- quando o canal Telegram nativo salvar/baixar um áudio recebido, copiar o arquivo para `inbox/`;
- quando sair um `.mp3` em `outbox/`, usar `send_file` no mesmo chat.

## Observação

Esta implementação evita webhook e preserva o canal nativo. Falta apenas ligar os pontos de entrada/saída do runtime atual do Picoclaw.


## Limpeza automática de arquivos antigos

Foi adicionado o script `scripts/cleanup_old_files.py`.

### Política atual
- Retenção configurada: **15 dias**
- Remove arquivos com idade **maior ou igual a 15 dias**
- Escopo de limpeza:
  - `inbox/`
  - `outbox/`
  - `done/`
  - `tmp/`
  - `processed/`
  - `sent/`
- Extensões alvo:
  - `.mp3`, `.ogg`, `.oga`, `.wav`, `.m4a`, `.opus`, `.json`
- Não atua sobre arquivos de configuração da skill
- Log em: `/root/.picoclaw/workspace/state/telegram-native-audio/cleanup.log`

### Execução manual
```bash
python3 /root/.picoclaw/workspace/skills/telegram-native-audio/scripts/cleanup_old_files.py
```

### Execução automática dentro da skill
- O watcher semiautomático `scripts/semi_auto_watcher.py` executa a limpeza automaticamente
- Frequência: no máximo **1 vez por dia**
- Controle de estado: `/root/.picoclaw/workspace/state/telegram-native-audio/semi-auto-state.json`
- A limpeza automática usa a mesma política de retenção de **15 dias**
- Não depende de cron externo nem de webhook
