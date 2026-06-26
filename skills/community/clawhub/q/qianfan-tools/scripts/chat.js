#!/usr/bin/env node

/**
 * 百度千帆 - 文本对话 (文心大模型)
 */

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const CHAT_URL = `${BASE_URL}/text/chatcompletion`;

async function chat(prompt, model = 'ernie-4.0-8k') {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY，请在 OpenClaw Skills 配置页面填入，或本地编辑 config.json。');
  }

  if (!prompt) {
    return emptyResult('对话内容不能为空。');
  }

  try {
    const body = {
      model,
      messages: [
        { role: 'user', content: prompt }
      ]
    };

    const { data } = await axios.post(CHAT_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`对话服务错误: ${data.message || '未知错误'}`);
    }

    const result = data?.result || data?.choices?.[0]?.message?.content;
    
    return successResult({
      prompt,
      response: result,
      model: data?.model || model,
      usage: data?.usage,
      engine: 'qianfan-chat'
    });

  } catch (e) {
    // 尝试其他端点
    try {
      const altBody = {
        prompt,
        temperature: 0.7,
        top_p: 0.9
      };
      
      const { data } = await axios.post(`${BASE_URL}/text/chatprompt`, altBody, {
        timeout: TIMEOUT_MS,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
        },
      });
      
      if (data && data.code) {
        return emptyResult(`对话服务错误: ${data.message || '需开通文心大模型 API'}`);
      }

      return successResult({
        prompt,
        response: data?.result || data?.text || '无响应',
        engine: 'qianfan-chat-alt'
      });
    } catch (e2) {
      return emptyResult(`对话失败: ${e.message} (需开通文心大模型 API)`);
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  const prompt = args.join(' ').trim();

  const result = await chat(prompt);
  console.log(JSON.stringify(result, null, 2));
}

main();
