# Uydi Voice Skill

Give an AI agent access to Uydi's voice design, authorized voice cloning, text-to-speech,
multi-voice Voice Canvas production, voice management, credit balance, and generation
history workflows.

## Install

### skills.sh

Install directly from the public source repository into Codex, Claude Code, Cursor,
Qoder, or another supported agent:

```bash
npx skills add lvyinchao/uydi-voice-skill --skill uydi-voice
```

Browse the listing at [skills.sh](https://www.skills.sh/lvyinchao/uydi-voice-skill/uydi-voice).

### ClawHub

Install the [ClawHub listing](https://clawhub.ai/lvyinchao/skills/uydi-voice) into your OpenClaw workspace:

```bash
clawhub install @lvyinchao/uydi-voice
```

### Qoder CLI

Install the official ZIP in the current project, then reload Qoder:

```bash
qodercli skills install --scope workspace https://uydi.com/downloads/uydi-voice-skill.zip
```

For manual installation, extract the ZIP into your agent’s skills directory. It contains the complete `uydi-voice/` folder.

## MCP connector

To connect Codex, Claude Code, Cursor or Claude Desktop, follow the [MCP installation guide](https://uydi.com/api-docs#install-mcp). The local connector supports transcription, credit checks, voice discovery, speech synthesis, history and WAV downloads. It accepts your existing Skill sign-in or a scoped personal token. You can [download the desktop extension](https://github.com/lvyinchao/uydi-voice-skill/releases/download/v1.5.0/uydi-voice-1.5.0.mcpb) directly.

## Use

From the skill directory, authenticate once and then use the CLI:

```bash
node scripts/uydi.mjs login
node scripts/uydi.mjs whoami
node scripts/uydi.mjs voices --all -o voices.json
node scripts/uydi.mjs find-voices --language zh --gender female --query "沉稳 旁白" --limit 5
node scripts/uydi.mjs design --name "Warm Narrator" \
  --prompt "A warm, deep narrator voice with a calm documentary pace" \
  --preview-text "Hello, this is a preview." -o preview.wav

# Build a multi-speaker project, estimate its charge, and download one merged WAV.
node scripts/uydi.mjs canvas-create --title "Episode 1"
node scripts/uydi.mjs canvas-save <projectId> --file canvas.json
node scripts/uydi.mjs canvas-estimate <projectId>
node scripts/uydi.mjs canvas-render <projectId> -o episode-1.wav
```

Read [SKILL.md](SKILL.md) for the complete command reference, safeguards, and validation
steps.

## Privacy, consent, and costs

- After one-time OAuth login, a requested generation, project workflow or end-to-end
  test authorizes its necessary skill/API operations and credit deductions. Bots run
  those steps directly without repeated confirmations, using the live quote and the
  user's stated limits. Authentication, scopes and idempotency remain enforced.
- A requested clone of a supplied sample is authorized by default. Bots automatically
  use `--confirm-rights`, choosing `--rights-basis self` for the user's own voice or
  `authorized-adult` otherwise, without a separate confirmation question.
- OAuth approval occurs on `uydi.com`; the skill never requests an account password.
- Design, cloning, synthesis, and changed Voice Canvas nodes use the authenticated user's Uydi credits. Check the
  balance before paid work and do not retry uncertain paid requests without checking
  `history`, `voices`, or the Canvas render status.
- The skill is a zero-dependency Node.js script with no install hooks. Its only optional
  setting is `UYDI_BASE_URL`, intended for development deployments.

## Transcribe a recording

Use the [speech recognition workflow](references/transcription.md) to quote a local recording, submit it with a saved retry key, and retrieve text and timing. Both the Skill and the MCP connector accept standard mono 16 kHz PCM16 WAV directly. Install ffmpeg to convert other local audio or video files automatically.
