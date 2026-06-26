/**
 * TTS 配置模块
 * 优先级：环境变量 > config.json > 默认值
 */
const fs = require('fs');
const path = require('path');

const skillDir = path.dirname(__dirname);
const configPath = path.join(skillDir, 'config.json');

// 默认配置
const defaultConfig = {
  voice: 'x4_xiaoyan',
  audio: {
    aue: 'raw',
    auf: 'audio/L16;rate=16000',
    tte: 'UTF8',
    outputBitrate: '24k',
    outputSampleRate: 24000
  },
  timeout: 60000
};

// 读取技能包配置
let skillConfig = {};
try {
  if (fs.existsSync(configPath)) {
    skillConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
} catch (e) {
  console.error('Failed to load config.json:', e.message);
}

module.exports = {
  // 讯飞 TTS 配置
  xunfei: {
    appId: process.env.XUNFEI_APP_ID,
    apiKey: process.env.XUNFEI_API_KEY,
    apiSecret: process.env.XUNFEI_API_SECRET,
    host: 'tts-api.xfyun.cn',
    path: '/v2/tts',

    // 发音人：环境变量 > config.json > 默认值
    defaultVoice: process.env.XUNFEI_VOICE || skillConfig.voice || defaultConfig.voice,

    // 音频参数
    audio: skillConfig.audio || defaultConfig.audio,

    // 超时
    timeout: skillConfig.timeout || defaultConfig.timeout
  },

  // 可用音色列表
  availableVoices: skillConfig.availableVoices || {},

  // 输出目录 - 使用 OpenClaw 标准临时目录
  outputDir: '/tmp/openclaw'
};
