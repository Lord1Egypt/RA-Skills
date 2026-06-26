#!/usr/bin/env node
/**
 * quiz-create.js - 对话式出题工具
 * 用法: node quiz-create.js "文档内容" "标题" "说明"
 */

const https = require('https');

const CLOUD_HOST = '118.196.5.240';
const CLOUD_PORT = '34100';

async function createQuiz(content, title, description) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ content, title, description });
    const options = {
      hostname: CLOUD_HOST,
      port: CLOUD_PORT,
      path: '/api/quiz/create-with-qr',
      method: 'POST',
      rejectUnauthorized: false,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('API响应解析失败: ' + data.substring(0, 200)));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

const content = process.argv[2];
const title = process.argv[3] || '';
const description = process.argv[4] || '';
const quiet = process.argv.includes('--quiet');

if (!content) {
  console.error('用法: node quiz-create.js "<内容>" ["标题"] ["说明"] [--quiet]');
  process.exit(1);
}

if (content.length < 50) {
  console.error('内容太短，至少需要50个字的内容来生成题目');
  process.exit(1);
}

if (!quiet) console.error('正在生成题目，请稍候...');
createQuiz(content, title, description)
  .then(result => {
    if (!result.success) {
      console.error('创建失败:', result.error);
      process.exit(1);
    }
    // --quiet 时只输出 JSON，方便外部解析
    console.log(JSON.stringify(result));
  })
  .catch(err => {
    console.error('请求失败:', err.message);
    process.exit(1);
  });
