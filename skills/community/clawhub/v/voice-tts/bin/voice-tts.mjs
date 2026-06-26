#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { loadConfig, resolveVoice, getSkillRoot } from '../lib/config.mjs';
import { formatError } from '../lib/errors.mjs';

function parseArgs(argv) {
  const args = { text: '', output: '/tmp/voice.mp3', rate: null, pitch: null, voice: null, agent: null };
  const rest = [...argv];
  while (rest.length) {
    const token = rest.shift();
    if (!token) continue;
    if (!args.text && !token.startsWith('-')) {
      args.text = token;
      continue;
    }
    if (token === '-f' || token === '--output') args.output = rest.shift();
    else if (token === '-v' || token === '--voice') args.voice = rest.shift();
    else if (token === '-r' || token === '--rate') args.rate = rest.shift();
    else if (token === '-p' || token === '--pitch') args.pitch = rest.shift();
    else if (token === '--agent') args.agent = rest.shift();
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.text) {
    console.error(JSON.stringify(formatError('synthesis_failed', 'missing_text')));
    process.exit(1);
  }

  const config = loadConfig();
  const voice = resolveVoice({ agentId: args.agent || process.env.OPENCLAW_AGENT_ID, explicitVoice: args.voice, config });
  const rate = args.rate || config.defaultRate;
  const pitch = args.pitch || config.defaultPitch;
  const output = path.resolve(args.output);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  const tempOutput = `${output}.tmp`;

  const script = path.join(getSkillRoot(), 'scripts', 'edge_tts');
  const child = spawn('python3', [script, args.text, '-v', voice, '-f', tempOutput, '-r', rate, '-p', pitch], {
    stdio: ['ignore', 'pipe', 'pipe']
  });

  let stderr = '';
  child.stderr.on('data', (d) => { stderr += d.toString(); });

  const timeout = setTimeout(() => {
    child.kill('SIGKILL');
  }, config.limits.ttsTimeoutMs);

  child.on('close', (code) => {
    clearTimeout(timeout);
    if (code !== 0 || !fs.existsSync(tempOutput)) {
      console.error(JSON.stringify(formatError('synthesis_failed', stderr.trim())));
      process.exit(1);
    }
    fs.renameSync(tempOutput, output);
    process.stdout.write(`${output}\n`);
  });
}

main().catch((err) => {
  console.error(JSON.stringify(formatError('synthesis_failed', String(err))));
  process.exit(1);
});
