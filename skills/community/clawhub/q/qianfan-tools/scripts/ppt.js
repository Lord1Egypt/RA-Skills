#!/usr/bin/env node

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const PPT_URL = `${BASE_URL}/wenku/ppt`;

// PPT 生成是异步的，需要轮询
async function pollForResult(url, apiKey, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const { data } = await axios.get(url, {
        headers: { Authorization: `Bearer ${apiKey}` },
        timeout: TIMEOUT_MS
      });
      
      if (data?.result?.status === 'success') {
        return data.result;
      } else if (data?.result?.status === 'failed') {
        throw new Error(data.result?.message || 'PPT生成失败');
      }
      
      // 等待后继续轮询
      await new Promise(r => setTimeout(r, 2000));
    } catch (e) {
      if (i === maxAttempts - 1) throw e;
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  throw new Error('PPT生成超时');
}

async function generatePpt(topic) {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY，请在 OpenClaw Skills 配置页面填入，或本地编辑 config.json。');
  }

  if (!topic) {
    return emptyResult('PPT主题不能为空。');
  }

  try {
    const body = {
      query: topic,
      style: 'general',
      pages: 10
    };

    const { data } = await axios.post(PPT_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`PPT服务错误: ${data.message || '未知错误'}`);
    }

    const taskId = data?.result?.task_id;
    if (!taskId) {
      return emptyResult('未能获取任务ID');
    }

    // 轮询获取结果
    const resultUrl = `${PPT_URL}/status/${taskId}`;
    const result = await pollForResult(resultUrl, apiKey);

    return successResult({
      topic,
      taskId,
      downloadUrl: result?.download_url || result?.url,
      previewUrl: result?.preview_url,
      pages: result?.pages || 10,
      engine: 'baidu-ppt'
    });

  } catch (e) {
    return emptyResult(`PPT生成失败: ${e.message}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const topic = args.join(' ').trim();

  const result = await generatePpt(topic);
  console.log(JSON.stringify(result, null, 2));
}

main();
