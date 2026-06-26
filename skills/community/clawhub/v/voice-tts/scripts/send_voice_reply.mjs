#!/usr/bin/env node
/**
 * send_voice_reply.mjs
 *
 * 接收文字回复内容，自动选择发送方式：
 * --channel telegram  → 直连 Telegram Bot API
 * --channel 其他       → 生成音频文件路径，agent 自行用 message 工具发送
 *
 * 用法：
 *   node send_voice_reply.mjs --text "回复内容" --chat-id "8317347201" --agent "main" --channel telegram
 *
 * Token 优先级（从上到下）：
 *   1. --token 参数
 *   2. openclaw.json 中当前 agent 的 botToken
 *   3. openclaw.json 中 default 账户的 botToken
 *   4. TELEGRAM_BOT_TOKEN 环境变量（兜底）
 */

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import { loadConfig, getSkillRoot, resolveVoice } from '../lib/config.mjs';

function parseArgs(argv) {
  const args = { text: '', chatId: '', agentId: 'main', voice: null, rate: null, token: null, channel: 'telegram' };
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (!token) continue;
    if (token === '--text' || token === '-t') args.text = argv[++i];
    else if (token === '--chat-id' || token === '-c') args.chatId = argv[++i];
    else if (token === '--agent' || token === '-a') args.agentId = argv[++i];
    else if (token === '--voice' || token === '-v') args.voice = argv[++i];
    else if (token === '--rate' || token === '-r') args.rate = argv[++i];
    else if (token === '--token') args.token = argv[++i];
    else if (token === '--channel') args.channel = argv[++i];
  }
  return args;
}

function runCommand(cmd, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '';
    child.stdout.on('data', d => { stdout += d.toString(); });
    child.stderr.on('data', d => { stderr += d.toString(); });
    child.on('close', (code) => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(new Error(stderr || `exit ${code}`));
    });
    child.on('error', reject);
  });
}

function getBotToken(agentId) {
  try {
    const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    if (!fs.existsSync(configPath)) return null;
    const raw = fs.readFileSync(configPath, 'utf8');
    const cfg = vm.runInNewContext(`(${raw})`, {});
    const accounts = cfg?.channels?.telegram?.accounts;
    if (!accounts) return null;
    return accounts[agentId]?.botToken || accounts['default']?.botToken || null;
  } catch {
    return null;
  }
}

async function synthesize(text, voice, rate) {
  const tempFile = `/tmp/voice-reply-${Date.now()}.mp3`;
  await runCommand('node', [
    path.join(getSkillRoot(), 'bin', 'voice-tts.mjs'),
    text, '-f', tempFile, '-v', voice, '-r', rate,
  ]);
  return tempFile;
}

async function sendTelegram(botToken, chatId, voiceFile, caption) {
  const apiUrl = `https://api.telegram.org/bot${botToken}/sendVoice`;
  const { stdout: httpCode } = await runCommand('curl', [
    '-s', '-o', '/dev/null', '-w', '%{http_code}',
    '-F', `chat_id=${chatId}`,
    '-F', `voice=@${voiceFile}`,
    '-F', `caption=${caption.slice(0, 1024)}`,
    apiUrl
  ]);
  return httpCode;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.text) {
    console.error(JSON.stringify({ error: 'missing_text', message: '必须提供 --text 参数' }));
    process.exit(1);
  }
  if (!args.chatId && args.channel === 'telegram') {
    console.error(JSON.stringify({ error: 'missing_chat_id', message: 'Telegram 发送需要 --chat-id' }));
    process.exit(1);
  }

  const config = loadConfig();
  const voice = args.voice || resolveVoice({ agentId: args.agentId, explicitVoice: null, config });
  const rate = args.rate || config.tts?.defaultRate || '+0%';
  const channel = args.channel || 'telegram';

  console.error(`[send_voice_reply] channel=${channel}, voice=${voice}, rate=${rate}, agent=${args.agentId}, text="${args.text.slice(0, 50)}..."`);

  // Step 1: 生成 TTS
  let voiceFile;
  try {
    voiceFile = await synthesize(args.text, voice, rate);
  } catch (err) {
    console.error(JSON.stringify({ error: 'tts_failed', details: err.message }));
    process.exit(1);
  }

  if (!fs.existsSync(voiceFile) || fs.statSync(voiceFile).size === 0) {
    console.error(JSON.stringify({ error: 'tts_empty_file', message: 'TTS 生成空文件' }));
    process.exit(1);
  }

  // Step 2: 根据 channel 发送
  if (channel === 'telegram') {
    const explicitToken = args.token || process.env.TELEGRAM_BOT_TOKEN || null;
    const openclawToken = getBotToken(args.agentId);
    const botToken = explicitToken || openclawToken;
    if (!botToken) {
      console.error(JSON.stringify({
        error: 'missing_token',
        message: `未找到 Telegram Bot Token。请检查：\n` +
          `1. openclaw.json 中 channels.telegram.accounts.${args.agentId}.botToken\n` +
          `2. openclaw.json 中 channels.telegram.accounts.default.botToken\n` +
          `3. 或设置环境变量 TELEGRAM_BOT_TOKEN`
      }));
      process.exit(1);
    }
    const httpCode = await sendTelegram(botToken, args.chatId, voiceFile, args.text);
    fs.unlinkSync(voiceFile);
    if (httpCode !== '200') {
      console.error(JSON.stringify({ error: 'telegram_send_failed', httpCode }));
      process.exit(1);
    }
    console.error(`[send_voice_reply] Telegram 发送成功 → chat_id=${args.chatId}`);
    process.stdout.write(JSON.stringify({ ok: true, channel, chatId: args.chatId, voice, agent: args.agentId }));
  } else {
    // 非 Telegram：输出文件路径，由 agent 自行用 message 工具发送
    fs.unlinkSync(voiceFile);
    // 重新生成到 workspace 目录（message 工具允许的路径）
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(os.homedir(), '.openclaw', 'workspace');
    const mediaOut = path.join(workspace, 'media', 'outbound');
    fs.mkdirSync(mediaOut, { recursive: true });
    const outFile = path.join(mediaOut, `voice-${Date.now()}.mp3`);
    await runCommand('node', [
      path.join(getSkillRoot(), 'bin', 'voice-tts.mjs'),
      args.text, '-f', outFile, '-v', voice, '-r', rate,
    ]);

    const messageHint = channel === 'discord'
      ? `message(action="send", channel="discord", media="${outFile}", message="${args.text}")`
      : channel === 'whatsapp'
      ? `message(action="send", channel="whatsapp", media="${outFile}", message="${args.text}")`
      : `message(action="send", channel="${channel}", media="${outFile}", message="${args.text}")`;

    console.error(`[send_voice_reply] ${channel} 模式：音频已生成，请 agent 自行调用：\n${messageHint}`);
    process.stdout.write(JSON.stringify({
      ok: true,
      channel,
      file: outFile,
      agentHint: messageHint,
      voice,
      agent: args.agentId,
    }));
  }
}

main().catch(err => {
  console.error(JSON.stringify({ error: 'unexpected', details: String(err) }));
  process.exit(1);
});
