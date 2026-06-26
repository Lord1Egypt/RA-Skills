#!/usr/bin/env node
/**
 * 小红书爆款笔记生成器
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

let API_KEY = process.env.DEEPSEEK_API_KEY || '';
try {
  const config = JSON.parse(fs.readFileSync(
    path.join(process.env.HOME || '/home/admin', '.openclaw/openclaw.json'), 'utf8'
  ));
  API_KEY = API_KEY || config.models?.providers?.deepseek?.apiKey || '';
} catch(e) {}

function callDeepSeek(prompt) {
  return new Promise((resolve, reject) => {
    if (!API_KEY) return reject(new Error('No API key'));
    const data = JSON.stringify({
      model: 'deepseek-v4-flash',
      messages: [
        { role: 'system', content: '你是一个小红书爆款笔记写手。擅长写种草、测评、教程类内容，语言亲切真实。' },
        { role: 'user', content: prompt }
      ],
      max_tokens: 2000
    });
    const req = https.request({
      hostname: 'api.deepseek.com',
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      }
    }, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve(JSON.parse(d).choices?.[0]?.message?.content || ''); }
        catch(e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function generate(topic) {
  const prompt = `写一篇小红书笔记，主题：${topic}

格式要求：
【标题】吸引眼球的标题（包含表情符号）
【正文】300-500字，口语化，真实分享感受
  - 开头要有代入感
  - 中间是干货/体验分享
  - 结尾引导互动
【标签】5-8个相关热门标签

风格：真实、亲切、有用`;

  const content = await callDeepSeek(prompt);
  return content;
}

// CLI
const args = process.argv.slice(2);
if (args.length >= 1) {
  generate(args.join(' ')).then(r => {
    console.log('\n' + r + '\n');
  }).catch(e => {
    console.error('Error:', e.message);
  });
}

module.exports = { generate };
