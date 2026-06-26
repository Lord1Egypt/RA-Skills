#!/usr/bin/env node

/**
 * Voice Reply - 一键生成语音并发送到 Telegram
 * 
 * 用法: node voice-send.js "要发送的文字" [telegram_id]
 * 
 * 示例: node voice-send.js "你好呀！" 5500262186
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// 配置
const VOICE_REPLY_DIR = '/tmp/voice-reply';
const WORKSPACE_DIR = os.homedir() + '/.openclaw/workspace';
const DEFAULT_VOICE = 'zh-CN-XiaoxiaoNeural';
const DEFAULT_CHANNEL = 'telegram';
const DEFAULT_TARGET = '5500262186'; // 坚果爸爸的 Telegram ID

// 确保目录存在
if (!fs.existsSync(VOICE_REPLY_DIR)) {
  fs.mkdirSync(VOICE_REPLY_DIR, { recursive: true });
}

/**
 * 生成唯一文件名
 */
function generateFileName() {
  return `voice_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.mp3`;
}

/**
 * 使用 edge-tts 生成语音
 */
function generateVoice(text, voice = DEFAULT_VOICE) {
  return new Promise((resolve, reject) => {
    const outputFile = path.join(VOICE_REPLY_DIR, generateFileName());
    const edgeTtsScript = path.join(os.homedir(), '.openclaw/workspace/skills/edge-tts/scripts/tts-converter.js');
    
    console.log(`[1/3] 生成语音: "${text.substring(0, 20)}..."`);
    
    const args = [edgeTtsScript, text, '--voice', voice, '--output', outputFile];
    
    const proc = spawn('node', args, {
      cwd: path.dirname(edgeTtsScript),
      stdio: 'pipe'
    });
    
    let stderr = '';
    proc.stderr.on('data', d => stderr += d);
    
    proc.on('close', code => {
      if (code === 0 && fs.existsSync(outputFile)) {
        console.log(`[1/3] ✅ 语音生成成功: ${outputFile}`);
        resolve(outputFile);
      } else {
        reject(new Error(`语音生成失败: ${stderr}`));
      }
    });
  });
}

/**
 * 复制到 workspace
 */
function copyToWorkspace(sourceFile) {
  const destFile = path.join(WORKSPACE_DIR, 'voice.mp3');
  fs.copyFileSync(sourceFile, destFile);
  console.log(`[2/3] ✅ 已复制到: ${destFile}`);
  return destFile;
}

/**
 * 发送语音消息
 */
function sendVoice(channel, target, mediaPath) {
  return new Promise((resolve, reject) => {
    console.log(`[3/3] 发送语音到 ${channel}...`);
    
    const args = [
      'message', 'send',
      '--channel', channel,
      '--target', target,
      '--media', mediaPath
    ];
    
    const proc = spawn('openclaw', args, { stdio: 'pipe' });
    
    let stdout = '', stderr = '';
    proc.stdout.on('data', d => stdout += d);
    proc.stderr.on('data', d => stderr += d);
    
    proc.on('close', code => {
      if (stdout.includes('✅') || stdout.includes('ok')) {
        console.log(`[3/3] ✅ 发送成功!`);
        resolve();
      } else {
        reject(new Error(`发送失败: ${stderr || stdout}`));
      }
    });
  });
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法: node voice-send.js "文字内容" [telegram_id]');
    console.log('示例: node voice-send.js "你好呀！" 5500262186');
    process.exit(1);
  }
  
  const text = args[0];
  const target = args[1] || DEFAULT_TARGET;
  const channel = DEFAULT_CHANNEL;
  
  console.log('========================================');
  console.log(`文字内容: ${text}`);
  console.log(`目标: ${channel} -> ${target}`);
  console.log('========================================\n');
  
  try {
    // 1. 生成语音
    const voiceFile = await generateVoice(text);
    
    // 2. 复制到 workspace
    const workspaceFile = copyToWorkspace(voiceFile);
    
    // 3. 发送
    await sendVoice(channel, target, workspaceFile);
    
    console.log('\n🎉 完成!');
  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
