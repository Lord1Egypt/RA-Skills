#!/usr/bin/env node
const path = require('path');

function loadEdgeTTS() {
  const candidates = [
    'node-edge-tts',
    '/usr/lib/node_modules/openclaw/node_modules/node-edge-tts',
  ];
  for (const mod of candidates) {
    try {
      return require(mod);
    } catch (_) {}
  }
  console.error('Missing dependency: node-edge-tts');
  console.error('The skill will not be able to generate audio until it is installed.');
  console.error('Install it with: npm i -g node-edge-tts');
  process.exit(1);
}

const { EdgeTTS } = loadEdgeTTS();

async function main() {
  const args = process.argv.slice(2);
  let voice = 'ru-RU-DmitryNeural';
  let out = '';
  let text = '';
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--voice') voice = args[++i];
    else if (a === '--out') out = args[++i];
    else text += (text ? ' ' : '') + a;
  }
  if (!text) {
    console.error('Usage: node edge_tts.js [--voice VOICE] [--out FILE] "Text"');
    process.exit(1);
  }
  if (!out) out = path.join(process.cwd(), `tts-${Date.now()}.mp3`);
  const tts = new EdgeTTS({ voice, timeout: 60000 });
  await tts.ttsPromise(text, out);
  console.log(out);
}

main().catch(err => {
  console.error(String(err));
  process.exit(1);
});
