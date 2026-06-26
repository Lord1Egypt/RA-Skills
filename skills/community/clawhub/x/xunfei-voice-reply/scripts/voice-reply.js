#!/usr/bin/env node
/**
 * 语音回复脚本 - 使用讯飞 TTS 生成语音
 * 用法: node voice-reply.js "要说的文本"
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 动态确定 skill 目录位置
const skillDir = path.dirname(__dirname);
const libDir = path.join(skillDir, 'lib');
const { XunfeiTTS } = require(path.join(libDir, 'tts-core'));
const config = require(path.join(libDir, 'tts-config'));

const text = process.argv[2];
if (!text) {
  console.error('Usage: node voice-reply.js "text"');
  process.exit(1);
}

// 使用配置中的输出目录
const tmpDir = config.outputDir;
if (!fs.existsSync(tmpDir)) {
  fs.mkdirSync(tmpDir, { recursive: true });
}

const mp3Path = path.join(tmpDir, 'voice-reply-temp.mp3');
const opusPath = path.join(tmpDir, 'voice-reply.opus');

async function main() {
  try {
    // 1. 使用讯飞 TTS 生成 MP3
    const tts = new XunfeiTTS();
    await tts.synthesize(text, mp3Path);

    // 2. 转换为 Opus（飞书要求）
    execSync(`ffmpeg -y -i ${mp3Path} -c:a libopus -b:a ${config.xunfei.audio.outputBitrate} -ar ${config.xunfei.audio.outputSampleRate} -ac 1 ${opusPath} 2>/dev/null`, {
      stdio: 'pipe'
    });

    // 3. 输出路径供调用方使用
    console.log(`VOICE_READY:${opusPath}`);

    // 清理临时文件
    if (fs.existsSync(mp3Path)) {
      fs.unlinkSync(mp3Path);
    }

  } catch (err) {
    console.error('VOICE_ERROR:', err.message);
    process.exit(1);
  }
}

main();
