---
name: telegram-native-audio
description: Processar conversas por áudio no Telegram nativo do Picoclaw, sem webhook. Use quando o usuário quiser receber mensagem de voz, transcrever áudio recebido, gerar resposta falada, reutilizar scripts de STT/TTS, ou manter fluxo voice-to-voice no canal atual do Telegram usando polling nativo.
---

# Telegram Native Audio

**Criador:** Fabyano Titara

Use esta skill para operar **somente no Telegram nativo** do Picoclaw.

## Regras obrigatórias

- **Não usar webhook**.
- **Não usar cloudflared**.
- **Não criar bot paralelo**.
- Preservar o canal Telegram nativo já ativo.

## Objetivo

Permitir o fluxo de conversas por voz no Telegram nativo através de um modelo **semiautomático**:
1. O Picoclaw baixa o áudio recebido no Telegram.
2. O watcher detecta o arquivo e transcreve automaticamente para texto.
3. O assistente recebe a transcrição e decide a resposta.
4. O assistente gera e envia a resposta em áudio usando um script finalizador.

## Requisitos

- **Chave de API do GROQ**: É obrigatório configurar a variável de ambiente `GROQ_API_KEY` para o funcionamento da transcrição (modelo `whisper-large-v3-turbo`).
- **Edge TTS**: Utilizado para a geração de áudio (voz `pt-BR-FranciscaNeural`).

## Recursos incluídos (Scripts)

- `scripts/transcribe_audio.py`: transcreve áudio com GROQ Whisper.
- `scripts/generate_audio.py`: gera áudio com EDGE TTS.
- `scripts/semi_auto_watcher.py`: monitora a pasta de mídia do Picoclaw (`/tmp/picoclaw_media`), transcreve novos áudios automaticamente e cria uma pendência de resposta.
- `scripts/finalize_reply.py`: recebe a pendência e o texto final da resposta, gera o áudio e envia de volta ao usuário.
- `scripts/cleanup_old_files.py`: rotina de limpeza automática que remove arquivos de áudio (inbox, outbox, tmp) mais antigos que **15 dias**.

## Como usar

### 1. Iniciar o Watcher (Semiautomático)
O watcher roda em background para processar novos áudios:
```bash
nohup python3 /root/.picoclaw/workspace/skills/telegram-native-audio/scripts/semi_auto_watcher.py > /root/.picoclaw/workspace/skills/telegram-native-audio/scripts/semi_auto_watcher.log 2>&1 &
```

### 2. Responder a uma pendência de áudio
Quando um áudio é recebido, ele será transcrito e notificado ao assistente. Para responder com voz, o assistente deve executar:
```bash
python3 /root/.picoclaw/workspace/skills/telegram-native-audio/scripts/finalize_reply.py \
  "ID_DA_PENDENCIA" \
  "Texto da resposta que será falada"
```

### 3. Limpeza Automática (Auto-Cleanup)
A limpeza de áudios antigos (mais de 15 dias) é gerenciada automaticamente pelo `semi_auto_watcher.py`, que executa o script `cleanup_old_files.py` uma vez por dia.

## Observações

- Preferir `.ogg` ou `.mp3` conforme o canal aceitar melhor.
- Ao trabalhar nesta skill, manter o foco em integração com o runtime atual do Picoclaw, não em automação externa do Telegram.
