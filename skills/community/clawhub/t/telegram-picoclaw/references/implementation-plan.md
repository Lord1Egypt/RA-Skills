# Plano de implementação

## Meta

Adicionar suporte a voice-to-voice no Telegram nativo do Picoclaw sem webhook.

## Premissas

- O canal Telegram nativo já está ativo.
- O usuário quer manter polling nativo.
- Já existem scripts funcionais para STT e TTS.

## Etapas

1. Descobrir como o gateway Picoclaw expõe mensagens de áudio recebidas.
2. Descobrir como responder com arquivo de áudio no mesmo canal.
3. Criar rotina local para:
   - salvar mídia temporária;
   - transcrever;
   - obter resposta do assistente;
   - sintetizar áudio;
   - enviar áudio;
   - apagar temporários.
4. Testar com áudio curto em pt-BR.
5. Ajustar formato final do arquivo para compatibilidade com Telegram.

## Pontos de integração a investigar

- Onde o runtime atual guarda anexos recebidos.
- Se existe marcação especial para enviar voice note em vez de arquivo genérico.
- Se `send_file` no canal Telegram preserva comportamento de áudio reproduzível no app.
- Se é necessário ffmpeg para converter para `.ogg/.opus`.

## Critérios de sucesso

- Usuário envia áudio no chat atual.
- O conteúdo é transcrito corretamente.
- A resposta do assistente é enviada em áudio de volta no mesmo chat.
- Nenhum webhook é usado.
