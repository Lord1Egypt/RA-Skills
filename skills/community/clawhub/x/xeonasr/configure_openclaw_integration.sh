#!/usr/bin/env bash
set -euo pipefail

log() {
  printf '[xeontts-config] %s\n' "$*"
}

fail() {
  printf '[xeontts-config] ERROR: %s\n' "$*" >&2
  exit 1
}

timestamp() {
  date +%Y%m%d-%H%M%S
}

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
CONFIG_FILE="${CONFIG_FILE:-$OPENCLAW_HOME/openclaw.json}"
RUN_ID="$(timestamp)"
QQBOT_TTS_BASE_URL="${QQBOT_TTS_BASE_URL:-http://127.0.0.1:9002}"
QQBOT_TTS_HEALTH_URL="${QQBOT_TTS_HEALTH_URL:-http://127.0.0.1:9002/health}"
OUTPUT_DIR="${OUTPUT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/outputs}"

command -v node >/dev/null 2>&1 || fail "missing required command: node"
[[ -f "$CONFIG_FILE" ]] || fail "OpenClaw config not found: $CONFIG_FILE"

export CONFIG_FILE RUN_ID QQBOT_TTS_BASE_URL QQBOT_TTS_HEALTH_URL OUTPUT_DIR

node <<'NODE'
const fs = require('node:fs');

const {
  CONFIG_FILE,
  RUN_ID,
  QQBOT_TTS_BASE_URL,
  QQBOT_TTS_HEALTH_URL,
  OUTPUT_DIR,
} = process.env;

const backupPath = `${CONFIG_FILE}.bak.${RUN_ID}`;
if (!fs.existsSync(backupPath)) {
  fs.copyFileSync(CONFIG_FILE, backupPath);
}

const raw = fs.readFileSync(CONFIG_FILE, 'utf8');
const config = JSON.parse(raw);

config.channels = config.channels || {};
config.channels.qqbot = config.channels.qqbot || {};
config.channels.qqbot.xeonTts = {
  ...(config.channels.qqbot.xeonTts || {}),
  enabled: true,
  baseUrl: QQBOT_TTS_BASE_URL,
  healthUrl: QQBOT_TTS_HEALTH_URL,
  outputDir: OUTPUT_DIR,
  cloneModel: 'qwen3_tts_0.6b_base_openvino',
  customModel: 'qwen3_tts_0.6b_custom_openvino',
  minReferenceDurationSec: 3,
  maxReferenceDurationSec: 5,
  maxCloneOutputSeconds: 20,
  maxCustomOutputSeconds: 30,
  modeRouting: {
    cloneIntentKeywords: ['克隆音色', '克隆声音', 'voice clone'],
    customIntentKeywords: ['生成语音', '朗读', '播报', 'tts'],
    asrGuardKeywords: ['转写', '识别语音', 'speech to text', 'asr'],
  },
};

if (config.skills && typeof config.skills === 'object' && 'xeontts' in config.skills) {
  delete config.skills.xeontts;
  if (Object.keys(config.skills).length === 0) {
    delete config.skills;
  }
}

fs.writeFileSync(CONFIG_FILE, `${JSON.stringify(config, null, 2)}\n`);
console.log('updated openclaw config with xeonTts block');
NODE

log "已写入 OpenClaw QQBOT TTS 配置: $CONFIG_FILE"
log "注意：xeontts 不会修改 tools.media.audio 或 channels.qqbot.stt，因此不会和 xeonasr 产生端口/配置冲突"
