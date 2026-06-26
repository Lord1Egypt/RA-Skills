#!/usr/bin/env node

/**
 * 百度千帆 - 文本续写
 */

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const CONTINUE_URL = `${BASE_URL}/text/continuation`;

async function continueText(prompt, model = 'ernie-3.5-8k') {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY');
  }

  if (!prompt) {
    return emptyResult('续写内容不能为空。');
  }

  try {
    const body = {
      prompt,
      model,
      temperature: 0.8,
      top_p: 0.9,
      penalty: 1.0
    };

    const { data } = await axios.post(CONTINUE_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`续写服务错误: ${data.message || '需开通续写 API'}`);
    }

    return successResult({
      prompt,
      continuation: data?.result || data?.text || '无响应',
      model: data?.model || model,
      engine: 'qianfan-continue'
    });

  } catch (e) {
    return emptyResult(`续写失败: ${e.message} (需开通续写 API)`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const prompt = args.join(' ').trim();

  if (!prompt) {
    console.log(JSON.stringify(emptyResult('用法: node continue.js <续写内容>')));
    process.exit(1);
  }

  const result = await continueText(prompt);
  console.log(JSON.stringify(result, null, 2));
}

main();
