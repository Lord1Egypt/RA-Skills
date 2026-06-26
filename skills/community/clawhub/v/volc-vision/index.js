#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const API_KEY = process.env.ARK_API_KEY;
const API_URL = 'ark.cn-beijing.volces.com';

// 支持图像理解的 VLM 模型列表
// vision 系列放最前面优先使用，其他按能力强弱排序，不可用的放最后
const VISION_MODELS = [
  // Vision 系列（优先）
  'doubao-seed-1-6-vision-250815',
  'doubao-1-5-vision-pro-32k-250115',
  // 其他模型（按能力强弱）
  'doubao-seed-2-0-pro-260215',
  'doubao-seed-1-8-251228',
  'doubao-seed-2-0-lite-260215',
  'doubao-seed-2-0-mini-260215',
  'deepseek-v3-2-251201',
  // 不可用
  'doubao-1-5-thinking-vision-pro-250428',
  'doubao-1-5-vision-pro-250328',
  'doubao-1-5-vision-lite-250315',
  'doubao-vision-pro-32k-241028',
  'doubao-vision-lite-32k-241015'
];

const MODEL = process.env.VISION_MODEL || VISION_MODELS[0];

function downloadImage(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    // 处理 base64 图片
    if (url.startsWith('data:')) {
      const base64Data = url.replace(/^data:image\/\w+;base64,/, '');
      resolve(Buffer.from(base64Data, 'base64'));
      return;
    }
    
    // 处理文件路径
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      const filePath = path.isAbsolute(url) ? url : path.join(process.cwd(), url);
      if (fs.existsSync(filePath)) {
        resolve(fs.readFileSync(filePath));
        return;
      }
      reject(new Error(`File not found: ${filePath}`));
      return;
    }
    
    protocol.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        downloadImage(res.headers.location).then(resolve).catch(reject);
        return;
      }
      
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks)));
      res.on('error', reject);
    }).on('error', reject);
  });
}

function encodeImage(base64String) {
  return base64String.toString('base64');
}

async function callVisionAPI(imagePath, prompt) {
  const imageBuffer = await downloadImage(imagePath);
  const base64Image = encodeImage(imageBuffer);
  
  // 检测图片类型
  const magicNumbers = {
    'ffd8ff': 'jpeg',
    '89504e47': 'png',
    '47494638': 'gif',
    '424d': 'bmp'
  };
  
  const hex = imageBuffer.toString('hex', 0, 4).toLowerCase();
  let mimeType = 'image/jpeg';
  for (const [magic, type] of Object.entries(magicNumbers)) {
    if (hex.startsWith(magic)) {
      mimeType = `image/${type}`;
      break;
    }
  }
  
  const imageUrl = `data:${mimeType};base64,${base64Image}`;
  
  const requestBody = {
    model: MODEL,
    messages: [{
      role: 'user',
      content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: imageUrl } }
      ]
    }],
    max_tokens: 4096
  };

  return new Promise((resolve, reject) => {
    const options = {
      hostname: API_URL,
      path: '/api/v3/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const response = Buffer.concat(chunks).toString();
        try {
          const json = JSON.parse(response);
          if (json.error) {
            reject(new Error(json.error.message));
          } else if (json.choices && json.choices[0]) {
            resolve(json.choices[0].message.content);
          } else {
            reject(new Error(`Unexpected response: ${response}`));
          }
        } catch (e) {
          reject(new Error(`Failed to parse response: ${response}`));
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(requestBody));
    req.end();
  });
}

// 主入口
async function main() {
  const args = process.argv.slice(2);

  if (!API_KEY) {
    console.error('Missing API key: set ARK_API_KEY');
    process.exit(1);
  }
  
  if (args.length === 0) {
    console.log('Usage: node index.js <image_path> [prompt]');
    console.log('Example: node index.js /path/to/image.jpg "描述这张图片"');
    console.log('Available models:', VISION_MODELS.join(', '));
    process.exit(1);
  }
  
  const imagePath = args[0];
  const prompt = args[1] || '描述这张图片';
  
  // 如果指定了模型，优先使用
  if (process.env.VISION_MODEL) {
    try {
      const result = await callVisionAPI(imagePath, prompt);
      console.log(result);
    } catch (error) {
      console.error(`Error with ${process.env.VISION_MODEL}:`, error.message);
      process.exit(1);
    }
    return;
  }
  
  // 否则尝试所有可用模型
  for (const model of VISION_MODELS) {
    try {
      const result = await callVisionAPIWithModel(imagePath, prompt, model);
      console.log(result);
      console.log(`\n[Model: ${model}]`);
      return;
    } catch (error) {
      console.error(`Model ${model} failed:`, error.message);
    }
  }
  
  console.error('All models failed');
  process.exit(1);
}

async function callVisionAPIWithModel(imagePath, prompt, model) {
  const imageBuffer = await downloadImage(imagePath);
  const base64Image = encodeImage(imageBuffer);
  
  // 检测图片类型
  const magicNumbers = {
    'ffd8ff': 'jpeg',
    '89504e47': 'png',
    '47494638': 'gif',
    '424d': 'bmp'
  };
  
  const hex = imageBuffer.toString('hex', 0, 4).toLowerCase();
  let mimeType = 'image/jpeg';
  for (const [magic, type] of Object.entries(magicNumbers)) {
    if (hex.startsWith(magic)) {
      mimeType = `image/${type}`;
      break;
    }
  }
  
  const imageUrl = `data:${mimeType};base64,${base64Image}`;
  
  const requestBody = {
    model: model,
    messages: [{
      role: 'user',
      content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: imageUrl } }
      ]
    }],
    max_tokens: 4096
  };

  return new Promise((resolve, reject) => {
    const options = {
      hostname: API_URL,
      path: '/api/v3/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const response = Buffer.concat(chunks).toString();
        try {
          const json = JSON.parse(response);
          if (json.error) {
            reject(new Error(json.error.message));
          } else if (json.choices && json.choices[0]) {
            resolve(json.choices[0].message.content);
          } else {
            reject(new Error(`Unexpected response: ${response}`));
          }
        } catch (e) {
          reject(new Error(`Failed to parse response: ${response}`));
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(requestBody));
    req.end();
  });
}

main();