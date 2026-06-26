#!/usr/bin/env node

/**
 * time-weaver CLI Tool (Demo)
 * Usage:
 *   node cli.js login
 *   node cli.js publish "Book Title" "Chapter Title" ./content.txt
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const CONFIG_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.time-weaver-config');
const API_URL = process.env.APP_URL || 'https://time-weaver-782300018128.us-west1.run.app';

const command = process.argv[2];

if (command === 'login') {
  console.log('请输入你的 API 密钥 (在网站个人资料页获取):');
  process.stdin.on('data', (data) => {
    const key = data.toString().trim();
    fs.writeFileSync(CONFIG_FILE, JSON.stringify({ apiKey: key }));
    console.log('登录成功！密钥已保存。');
    process.exit();
  });
} else if (command === 'publish') {
  const bookTitle = process.argv[3];
  const chapterTitle = process.argv[4];
  const filePath = process.argv[5];

  if (!bookTitle || !chapterTitle || !filePath) {
    console.log('用法: time-weaver publish "书名" "章节名" 文件路径');
    process.exit(1);
  }

  if (!fs.existsSync(CONFIG_FILE)) {
    console.log('请先运行 time-weaver login 登录。');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(CONFIG_FILE));
  const content = fs.readFileSync(filePath, 'utf8');

  const postData = Buffer.from(JSON.stringify({
    token: config.apiKey,
    bookTitle,
    chapterTitle,
    content
  }));

  const options = {
    hostname: new URL(API_URL).hostname,
    port: 443,
    path: '/api/cli/publish',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': postData.length
    }
  };

  const req = https.request(options, (res) => {
    let responseData = '';
    res.on('data', (chunk) => responseData += chunk);
    res.on('end', () => {
      if (res.statusCode !== 200) {
        console.log(`❌ 服务器返回错误 (${res.statusCode}):`);
        console.log(responseData.substring(0, 200)); // Print first 200 chars of response
        return;
      }
      try {
        const result = JSON.parse(responseData);
        if (result.success) {
          console.log(`✅ 发布成功: ${result.message}`);
        } else {
          console.log(`❌ 发布失败: ${result.error}`);
        }
      } catch (e) {
        console.log('❌ 解析服务器响应失败，可能不是 JSON 格式。');
        console.log('响应内容预览:', responseData.substring(0, 200));
      }
    });
  });

  req.on('error', (e) => console.error(`请求错误: ${e.message}`));
  req.write(postData);
  req.end();
} else {
  console.log('可用命令: login, publish');
}
