#!/usr/bin/env node

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const OCR_URL = `${BASE_URL}/wenku/ocr_essay`;

async function ocrEssay(imageUrl, level = '高中') {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY，请在 OpenClaw Skills 配置页面填入，或本地编辑 config.json。');
  }

  if (!imageUrl) {
    return emptyResult('图片URL不能为空。');
  }

  try {
    const body = {
      image_url: imageUrl,
      level: level === '初中' ? 'middle' : 'high'
    };

    const { data } = await axios.post(OCR_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`OCR服务错误: ${data.message || '未知错误'}`);
    }

    const result = data?.result || {};
    
    return successResult({
      title: result?.title || '无标题',
      content: result?.content || result?.text || '未能识别内容',
      level,
      wordCount: result?.word_count,
      engine: 'baidu-ocr-essay'
    });

  } catch (e) {
    return emptyResult(`作文识别失败: ${e.message}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const imageUrl = args[0];
  const level = args[1] || '高中';

  if (!imageUrl) {
    console.log(JSON.stringify(emptyResult('用法: node ocr-essay.js <图片URL> [初中|高中]')));
    process.exit(1);
  }

  const result = await ocrEssay(imageUrl, level);
  console.log(JSON.stringify(result, null, 2));
}

main();
