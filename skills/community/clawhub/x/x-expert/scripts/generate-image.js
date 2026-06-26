#!/usr/bin/env node

/**
 * X Expert - 图片生成脚本
 * 支持多种图像生成服务：DALL-E, MiniMax, Nano Banana, Leonardo.ai
 * Usage: node generate-image.js "prompt" [service]
 */

// 图像服务配置
const imageServices = {
  dalle: {
    name: 'DALL-E 3',
    envVars: ['OPENAI_API_KEY'],
    generate: generateWithDalle,
  },
  minimax: {
    name: 'MiniMax Image',
    envVars: ['MINIMAX_API_KEY'],
    generate: generateWithMiniMax,
  },
  'nano-banana': {
    name: 'Nano Banana',
    envVars: ['NANO_BANANA_API_KEY'],
    generate: generateWithNanoBanana,
  },
  leonardo: {
    name: 'Leonardo.ai',
    envVars: ['LEONARDO_API_KEY'],
    generate: generateWithLeonardo,
  },
};

/**
 * DALL-E 3 生成
 */
async function generateWithDalle(prompt) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error('OPENAI_API_KEY not set');

  const response = await fetch('https://api.openai.com/v1/images/generations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'dall-e-3',
      prompt,
      n: 1,
      size: '1024x1024',
      quality: 'standard',
    }),
  });

  const data = await response.json();
  if (data.error) throw new Error(data.error.message);
  return data.data[0].url;
}

/**
 * MiniMax Image 生成
 */
async function generateWithMiniMax(prompt) {
  const apiKey = process.env.MINIMAX_API_KEY;
  if (!apiKey) throw new Error('MINIMAX_API_KEY not set');

  const response = await fetch('https://api.minimax.chat/v1/image_generation', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'minimax-01',
      prompt,
      num_samples: 1,
      width: 1024,
      height: 1024,
    }),
  });

  const data = await response.json();
  if (data.base_resp?.status_code !== 0) throw new Error(data.base_resp?.status_msg || 'Error');
  return data.data?.images?.[0]?.image_url;
}

/**
 * Nano Banana 生成
 */
async function generateWithNanoBanana(prompt) {
  const apiKey = process.env.NANO_BANANA_API_KEY;
  if (!apiKey) throw new Error('NANO_BANANA_API_KEY not set');

  const response = await fetch('https://api.nano-banana.com/v1/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'flux-pro',
      prompt,
      width: 1024,
      height: 1024,
    }),
  });

  const data = await response.json();
  if (data.error) throw new Error(data.error);
  return data.url;
}

/**
 * Leonardo.ai 生成
 */
async function generateWithLeonardo(prompt) {
  const apiKey = process.env.LEONARDO_API_KEY;
  if (!apiKey) throw new Error('LEONARDO_API_KEY not set');

  // 先创建生成任务
  const response = await fetch('https://api.leonardo.ai/v1/generations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      prompt,
      model_id: '6bef0f53-f484-4c86-809a-a88c4c2e2b6e', // Leonardo Phoenix
      width: 1024,
      height: 1024,
    }),
  });

  const data = await response.json();
  if (data.generations) {
    // 轮询等待生成完成
    const generationId = data.generations[0].id;
    return await pollLeonardo(apiKey, generationId);
  }
  throw new Error('Generation failed');
}

async function pollLeonardo(apiKey, generationId, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    await new Promise((r) => setTimeout(r, 2000));

    const response = await fetch(
      `https://api.leonardo.ai/v1/generations/${generationId}`,
      {
        headers: { Authorization: `Bearer ${apiKey}` },
      }
    );

    const data = await response.json();
    const status = data.generations_by_id?.[generationId]?.status;

    if (status === 'COMPLETE') {
      return data.generations_by_id[generationId].generated_images[0].url;
    }
    if (status === 'FAILED') {
      throw new Error('Image generation failed');
    }
  }
  throw new Error('Timeout waiting for image');
}

/**
 * 主函数
 */
async function generateImage(prompt, service = 'dalle') {
  const serviceConfig = imageServices[service.toLowerCase()];
  if (!serviceConfig) {
    throw new Error(
      `Unknown service: ${service}. Available: ${Object.keys(imageServices).join(', ')}`
    );
  }

  console.log(`🎨 正在使用 ${serviceConfig.name} 生成图片...`);
  console.log(`Prompt: ${prompt}`);
  console.log('---');

  const imageUrl = await serviceConfig.generate(prompt);
  console.log('✅ 图片生成成功!');
  console.log(`URL: ${imageUrl}`);

  return {
    service: serviceConfig.name,
    url: imageUrl,
    prompt,
  };
}

// CLI 入口
const prompt = process.argv[2];
const service = process.argv[3] || 'dalle';

if (!prompt) {
  console.error('Usage: node generate-image.js "图片描述" [service]');
  console.error('Services:', Object.keys(imageServices).join(', '));
  process.exit(1);
}

generateImage(prompt, service).catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});

module.exports = { generateImage, imageServices };
