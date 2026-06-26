#!/usr/bin/env node

/**
 * 百度千帆 - 通用 OCR 文字识别
 */

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const OCR_URL = `${BASE_URL}/ocr/general`;

async function ocr(imageUrl) {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY');
  }

  if (!imageUrl) {
    return emptyResult('图片URL不能为空。');
  }

  try {
    const body = {
      url: imageUrl
    };

    const { data } = await axios.post(OCR_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`OCR服务错误: ${data.message || '需开通 OCR API'}`);
    }

    const words = data?.result?.words_list || [];
    const text = words.map(w => w?.words || '').join('\n');

    return successResult({
      imageUrl,
      texts: words.map(w => ({
        text: w?.words || '',
        confidence: w?.confidence
      })),
      fullText: text,
      count: words.length,
      engine: 'qianfan-ocr'
    });

  } catch (e) {
    return emptyResult(`OCR识别失败: ${e.message} (需开通 OCR API)`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const imageUrl = args[0];

  if (!imageUrl) {
    console.log(JSON.stringify(emptyResult('用法: node ocr.js <图片URL>')));
    process.exit(1);
  }

  const result = await ocr(imageUrl);
  console.log(JSON.stringify(result, null, 2));
}

main();
