/**
 * 图生图核心模块
 * 支持图片编辑、重绘、变体生成
 */

const axios = require('axios');
const {
  downloadImage,
  generateFilename,
  sleep,
  validateApiKey,
  loadImage,
  calculateBackoff
} = require('./utils');

/**
 * 图生图 - 图片编辑
 * @param {object} options - 选项
 * @param {string} options.image - 输入图片（URL 或本地路径）
 * @param {string} options.prompt - 编辑提示词
 * @param {number} [options.strength=0.7] - 重绘强度（0-1）
 * @param {string} [options.size='1024x1024'] - 输出尺寸
 * @param {number} [options.maxRetries=3] - 最大重试次数
 * @returns {Promise<object>} 生成结果
 */
async function editImage({
  image,
  prompt,
  strength = 0.7,
  size = '1024x1024',
  maxRetries = 3
} = {}) {
  // 验证 API Key
  if (!validateApiKey()) {
    return {
      success: false,
      error: 'VOLC_API_KEY 环境变量未设置',
      code: 401
    };
  }

  // 验证强度参数
  if (strength < 0 || strength > 1) {
    return {
      success: false,
      error: 'strength 必须在 0-1 之间',
      code: 400
    };
  }

  const apiKey = process.env.VOLC_API_KEY;
  const apiBase = process.env.VOLC_API_BASE || 'https://ark.cn-beijing.volces.com/api/v3';

  console.log(`🖼️ 开始编辑图片...`);
  console.log(`   提示词：${prompt}`);
  console.log(`   强度：${strength}`);

  // 加载输入图片
  let imageBase64;
  try {
    imageBase64 = await loadImage(image);
    console.log('✅ 图片加载成功');
  } catch (error) {
    return {
      success: false,
      error: `图片加载失败：${error.message}`,
      code: 400
    };
  }

  // 构建请求体
  const requestBody = {
    model: process.env.VOLC_IMAGE_MODEL || 'doubao-image-x',
    prompt: prompt,
    image: imageBase64,
    strength: strength,
    size: size,
    n: 1
  };

  // 带重试的 API 调用
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await axios.post(
        `${apiBase}/images/generations`,
        requestBody,
        {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
          },
          timeout: 120000
        }
      );

      console.log('✅ API 调用成功');

      // 下载生成的图片
      const images = await Promise.all(
        response.data.data.map(async (img, idx) => {
          const filename = generateFilename('volc_edit');
          const localPath = await downloadImage(img.url, filename);
          return {
            url: img.url,
            local_path: localPath,
            prompt: prompt,
            size: size,
            strength: strength,
            index: idx + 1
          };
        })
      );

      return {
        success: true,
        images: images,
        usage: {
          tokens: response.data.usage?.total_tokens || 150,
          cost: (response.data.usage?.total_tokens || 150) * 0.0015,
          model: requestBody.model
        }
      };

    } catch (error) {
      const statusCode = error.response?.status;
      const errorMsg = error.response?.data?.error?.message || error.message;

      console.error(`❌ 尝试 ${attempt}/${maxRetries} 失败：${errorMsg}`);

      if (statusCode === 401) {
        return {
          success: false,
          error: '鉴权失败 (401) - 请检查 API Key',
          code: 401
        };
      }

      if (statusCode === 400) {
        return {
          success: false,
          error: `参数错误 (400): ${errorMsg}`,
          code: 400
        };
      }

      if ((statusCode === 429 || statusCode >= 500) && attempt < maxRetries) {
        const waitTime = calculateBackoff(attempt);
        console.log(`⏳ 等待 ${waitTime}ms 后重试...`);
        await sleep(waitTime);
        continue;
      }

      return {
        success: false,
        error: errorMsg,
        code: statusCode
      };
    }
  }

  return {
    success: false,
    error: '达到最大重试次数',
    code: 500
  };
}

/**
 * 生成图片变体
 * @param {string} image - 输入图片（URL 或本地路径）
 * @param {object} options - 选项
 * @param {number} [options.n=3] - 生成变体数量
 * @param {number} [options.strength=0.5] - 变体强度
 * @param {string} [options.size='1024x1024'] - 尺寸
 * @returns {Promise<object>} 变体生成结果
 */
async function createVariations(image, {
  n = 3,
  strength = 0.5,
  size = '1024x1024'
} = {}) {
  const results = [];
  
  console.log(`🔄 开始生成 ${n} 个变体...`);
  
  for (let i = 0; i < n; i++) {
    console.log(`\n[${i + 1}/${n}] 生成变体...`);
    
    const result = await editImage({
      image,
      prompt: '保持原图风格和内容，生成相似变体',
      strength,
      size,
      maxRetries: 2
    });
    
    if (result.success) {
      results.push(...result.images);
    } else {
      console.error(`变体 ${i + 1} 生成失败：${result.error}`);
    }
  }
  
  if (results.length === 0) {
    return {
      success: false,
      error: '所有变体生成失败'
    };
  }
  
  return {
    success: true,
    variations: results,
    count: results.length,
    usage: {
      total_cost: results.length * 0.0015
    }
  };
}

module.exports = {
  editImage,
  createVariations
};
