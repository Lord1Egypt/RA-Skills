# Speech-to-Text (STT) Skill

Transcreve arquivos de áudio para texto usando OpenAI Whisper, otimizado para
 português (Brasil).

## When to use

- Converter mensagens de voz ou áudios para texto
- Transcrever áudios do WhatsApp, Telegram, etc.
- Processar formatos: OGG, WAV, MP3, M4A, FLAC, AAC, OPUS
- Obter transcrições com timestamps
- Processar conteúdo em português brasileiro

## Tools

- stt_transcribe: Transcreve um arquivo de áudio específico
- stt_watch: Inicia monitoramento contínuo da pasta inbound
- stt_batch: Processa todos os áudios pendentes de uma vez

## Setup

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
 ```

 2. Instalar FFmpeg (necessário pelo Whisper):
  - Windows: execute install_ffmpeg.cmd ou winget install "Gyan.FFmpeg"
  - macOS: brew install ffmpeg
  - Linux: sudo apt install ffmpeg
 3. Criar pasta de entrada:
```bash
  mkdir -p ../../../media/inbound
```

## Usage

### Transcrever arquivo específico

 ```bash
python stt_processor.py --file /caminho/para/audio.ogg
 ```

### Transcrever todos os áudios pendentes

 ```bash
python stt_processor.py