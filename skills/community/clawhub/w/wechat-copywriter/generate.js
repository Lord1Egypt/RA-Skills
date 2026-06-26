#!/usr/bin/env node
/**
 * 朋友圈文案生成器 - AI自动生成营销文案
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Get API key
let API_KEY = process.env.DEEPSEEK_API_KEY || '';
try {
  const config = JSON.parse(fs.readFileSync(
    path.join(process.env.HOME || '/home/admin', '.openclaw/openclaw.json'), 'utf8'
  ));
  API_KEY = API_KEY || config.models?.providers?.deepseek?.apiKey || '';
} catch(e) {}

const STYLES = {
  '促销': '限时优惠、饥饿营销、促单转化',
  '种草': '产品体验分享、真实感受、用户见证',
  '情感': '走心故事、情感共鸣、人设打造',
  '干货': '行业知识、实用技巧、价值输出',
  '互动': '投票/问答/抽奖、粉丝互动',
  '新品': '新品发布、首发优惠、抢先体验'
};

function callDeepSeek(prompt) {
  return new Promise((resolve, reject) => {
    if (!API_KEY) return reject(new Error('No API key'));
    const data = JSON.stringify({
      model: 'deepseek-v4-flash',
      messages: [
        { role: 'system', content: '你是一个朋友圈营销文案专家。生成短小精悍(50-150字)、有吸引力的文案。' },
        { role: 'user', content: prompt }
      ],
      max_tokens: 1000
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

async function generate(product, style = '促销') {
  const styleDesc = STYLES[style] || '普通推广';
  const prompt = `写一条朋友圈营销文案。
产品：${product}
风格：${styleDesc}
要求：
1. 50-150字
2. 有吸引力的开头
3. 包含产品卖点
4. 引导行动（下单/咨询）
5. 不要过于广告感`;

  return await callDeepSeek(prompt);
}

// CLI
const args = process.argv.slice(2);
if (args.length >= 1) {
  const product = args[0];
  const style = args[1] || '促销';
  generate(product, style).then(r => {
    console.log('\n' + r + '\n');
  }).catch(e => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = { generate };
