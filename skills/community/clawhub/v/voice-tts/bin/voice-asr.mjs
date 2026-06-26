#!/usr/bin/env node
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { loadConfig, getSkillRoot } from '../lib/config.mjs';
import { formatError } from '../lib/errors.mjs';
import { validateAudio } from '../lib/audio.mjs';

function parseArgs(argv) {
  const passthrough = [];
  let audioFile = null;
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (!token) continue;
    if ((token === '--model' || token === '-m' || token === '--language' || token === '-l' || token === '--initial-prompt' || token === '--temperature') && i + 1 < argv.length) {
      passthrough.push(token, argv[i + 1]);
      i += 1;
      continue;
    }
    if (token === '--timestamps' || token === '-t' || token === '--json' || token === '-j' || token === '--quiet' || token === '-q' || token === '--condition-on-previous-text' || token === '--no-condition-on-previous-text') {
      passthrough.push(token);
      continue;
    }
    if (token.startsWith('-')) {
      passthrough.push(token);
      continue;
    }
    if (!audioFile) {
      audioFile = token;
    } else {
      passthrough.push(token);
    }
  }
  return { audioFile, passthrough };
}

async function main() {
  const { audioFile, passthrough } = parseArgs(process.argv.slice(2));
  const config = loadConfig();
  const validation = validateAudio(audioFile, config);
  if (!validation.ok) {
    console.error(JSON.stringify(formatError(validation.error)));
    process.exit(1);
  }

  // Inject default ASR parameters from config if not overridden
  if (!passthrough.includes('--initial-prompt') && config.asr?.defaultInitialPrompt) {
    passthrough.push('--initial-prompt', config.asr.defaultInitialPrompt);
  }
  if (!passthrough.includes('--temperature') && config.asr?.defaultTemperature !== undefined && config.asr?.defaultTemperature !== null) {
    passthrough.push('--temperature', String(config.asr.defaultTemperature));
  }
  if (!passthrough.includes('--condition-on-previous-text') && !passthrough.includes('--no-condition-on-previous-text') && config.asr?.conditionOnPreviousText !== undefined) {
    passthrough.push(config.asr.conditionOnPreviousText ? '--condition-on-previous-text' : '--no-condition-on-previous-text');
  }

  // Run Whisper transcription
  const script = path.join(getSkillRoot(), 'scripts', 'whisper');
  const child = spawn('python3', [script, audioFile, ...passthrough], { stdio: ['ignore', 'pipe', 'pipe'] });
  let stdout = '';
  let stderr = '';
  child.stdout.on('data', (d) => { stdout += d.toString(); });
  child.stderr.on('data', (d) => { stderr += d.toString(); });

  const timeout = setTimeout(() => child.kill('SIGKILL'), config.limits.asrTimeoutMs);

  await new Promise((resolve, reject) => {
    child.on('close', (code, signal) => {
      clearTimeout(timeout);
      if (signal === 'SIGKILL') {
        console.error(JSON.stringify(formatError('timeout')));
        reject(new Error('timeout'));
        return;
      }
      if (code !== 0) {
        let details = stderr.trim() || stdout.trim();
        try {
          const parsed = JSON.parse(details);
          if (parsed?.error) {
            console.error(JSON.stringify(formatError(parsed.error, parsed.details || '')));
            reject(new Error(parsed.error));
            return;
          }
        } catch {}
        console.error(JSON.stringify(formatError('transcription_failed', details)));
        reject(new Error('transcription_failed'));
        return;
      }
      resolve();
    });
    child.on('error', reject);
  });

  // ── Transcription succeeded — archive the file ──────────────────────
  // After successful ASR, move the file from ~/.openclaw/media/inbound/
  // to the agent's workspace media/inbound/, then delete the original.
  const inboundDir = path.join(os.homedir(), '.openclaw', 'media', 'inbound');
  if (audioFile.startsWith(inboundDir + path.sep) || audioFile === inboundDir) {
    const agentWorkspace = process.env.OPENCLAW_WORKSPACE || path.join(os.homedir(), '.openclaw', 'workspace');
    const agentInboundDir = path.join(agentWorkspace, 'media', 'inbound');
    const destPath = path.join(agentInboundDir, path.basename(audioFile));

    try {
      fs.mkdirSync(agentInboundDir, { recursive: true });
      // Copy first (in case delete fails, we still have the file)
      fs.copyFileSync(audioFile, destPath);
      // Delete original only after copy succeeds
      fs.unlinkSync(audioFile);
    } catch (err) {
      // Non-fatal: ASR already succeeded, file still exists at original path
      // Just log and continue — don't fail the transcription result
      console.error(`[voice-asr] archive warning: ${err.message}`);
    }
  }

  // Output formatted voice message — agent reads this and calls send_voice_reply.mjs
  const voiceMessage = `【语音消息】
执行要求：必须按照 voice-tts skill 的规则执行，回复需调用 send_voice_reply.mjs 返回语音+文字双通道格式
语音内容：${stdout.trim()}`;
  process.stdout.write(voiceMessage);
}

main().catch((err) => {
  console.error(JSON.stringify(formatError('transcription_failed', String(err))));
  process.exit(1);
});
