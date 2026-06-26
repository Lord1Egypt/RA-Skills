#!/usr/bin/env node

/**
 * 百度千帆 - 图像生成
 */

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const IMAGE_URL = `${BASE_URL}/text2image/sd`;

// 图像生成是异步的，需要轮询
async function pollForResult(url, apiKey, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const { data } = await axios.get(url, {
        headers: { Authorization: `Bearer ${apiKey}` },
        timeout: TIMEOUT_MS
      });
      
      if (data?.result?.image) {
        return data.result;
      } else if (data?.result?.status === 'failed') {
        throw new Error(data.result?.message || '生成失败');
      }
      
      await new Promise(r => setTimeout(r, 2000));
    } catch (e) {
      if (i === maxAttempts - 1) throw e;
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  throw new Error('生成超时');
}

async function generateImage(prompt, style = '二次元') {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY');
  }

  if (!prompt) {
    return emptyResult('图像描述不能为空。');
  }

  try {
    const body = {
      prompt,
      style,
      size: '1024x1024',
      num: 1
    };

    const { data } = await axios.post(IMAGE_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`图像服务错误: ${data.message || '需开通图像生成 API'}`);
    }

    const taskId = data?.result?.task_id;
    if (!taskId) {
      // 同步返回
      return successResult({
        prompt,
        images: data?.result?.image || [],
        engine: 'qianfan-image'
      });
    }

    // 轮询获取结果
    const resultUrl = `${IMAGE_URL}/status/${taskId}`;
    const result = await pollForResult(resultUrl, apiKey);

    return successResult({
      prompt,
      taskId,
      images: result?.image ? [result.image] : [],
      engine: 'qianfan-image'
    });

  } catch (e) {
    return emptyResult(`图像生成失败: ${e.message} (需开通图像生成 API)`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const prompt = args.join(' ').trim();

  if (!prompt) {
    console.log(JSON.stringify(emptyResult('用法: node image.js <图像描述> [风格]')));
    console.log('示例: node image.js "一只可爱的猫咪" 二次元');
    process.exit(1);
  }

  const result = await generateImage(prompt);
  console.log(JSON.stringify(result, null, 2));
}

main();
