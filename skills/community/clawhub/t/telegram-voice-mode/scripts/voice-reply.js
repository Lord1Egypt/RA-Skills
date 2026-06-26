#!/usr/bin/env node

/**
 * Voice Reply Tool
 * 自动将回复内容转换为语音并发送到用户渠道
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// 临时文件目录
const TMP_DIR = '/tmp';
const VOICE_REPLY_DIR = path.join(TMP_DIR, 'voice-reply');

// 确保临时目录存在
if (!fs.existsSync(VOICE_REPLY_DIR)) {
  fs.mkdirSync(VOICE_REPLY_DIR, { recursive: true });
}

/**
 * 生成唯一文件名
 */
function generateFileName(ext = 'mp3') {
  return `voice_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.${ext}`;
}

/**
 * 使用 edge-tts 生成语音
 * @param {string} text - 要转换的文本
 * @param {string} voice - 语音名称（默认中文女声）
 * @returns {Promise<string>} - 返回生成的音频文件路径
 */
async function generateVoice(text, voice = 'zh-CN-XiaoxiaoNeural') {
  return new Promise((resolve, reject) => {
    const outputFile = path.join(VOICE_REPLY_DIR, generateFileName());
    
    // 获取 edge-tts 脚本路径
    const edgeTtsDir = path.join(os.homedir(), '.openclaw/workspace/skills/edge-tts/scripts');
    const ttsScript = path.join(edgeTtsDir, 'tts-converter.js');
    
    // 检查脚本是否存在
    if (!fs.existsSync(ttsScript)) {
      reject(new Error(`edge-tts 脚本不存在: ${ttsScript}`));
      return;
    }
    
    const args = [
      ttsScript,
      text,
      '--voice', voice,
      '--output', outputFile
    ];
    
    console.log(`[voice-reply] 生成语音: ${text.substring(0, 20)}...`);
    console.log(`[voice-reply] 输出文件: ${outputFile}`);
    
    const process = spawn('node', args, {
      cwd: edgeTtsDir,
      stdio: 'pipe'
    });
    
    let stderr = '';
    
    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    process.on('close', (code) => {
      if (code === 0 && fs.existsSync(outputFile)) {
        console.log(`[voice-reply] 语音生成成功: ${outputFile}`);
        resolve(outputFile);
      } else {
        console.error(`[voice-reply] 语音生成失败: ${stderr}`);
        reject(new Error(`语音生成失败: ${stderr}`));
      }
    });
  });
}

/**
 * 主函数 - 当作为命令行工具运行时
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage: node voice-reply.js "要转换的文本" [--voice voice_name]');
    console.log('Example: node voice-reply.js "你好，我是小坚果" --voice zh-CN-XiaoxiaoNeural');
    process.exit(1);
  }
  
  const text = args[0];
  let voice = 'zh-CN-XiaoxiaoNeural';
  
  // 解析参数
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--voice' && args[i + 1]) {
      voice = args[i + 1];
      i++;
    }
  }
  
  try {
    const outputFile = await generateVoice(text, voice);
    console.log(`SUCCESS: ${outputFile}`);
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

// 导出函数供外部调用
module.exports = {
  generateVoice,
  generateFileName
};

// 如果直接运行
if (require.main === module) {
  main();
}
