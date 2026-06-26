/**
 * 文生图核心模块
 * 调用火山引擎方舟 API 生成图片
 */

const axios = require('axios');
const {
  downloadImage,
  generateFilename,
  sleep,
  validateApiKey,
  getFromCache,
  setCache,
  generateCacheKey
} = require('./utils');

// 7 种预定义风格提示词
const styleMap = {
  realistic: '写实风格，高清，高质量，专业摄影',
  anime: '动漫风格，二次元，精美，日系动画',
  oil: '油画风格，艺术感，厚重，古典绘画',
  watercolor: '水彩风格，清新，透明感，淡雅',
  sketch: '素描风格，线条感，黑白，手绘',
  cyberpunk: '赛博朋克风格，霓虹灯，未来感，科技',
  fantasy: '奇幻风格，魔法，梦幻，神秘'
};

// 支持的尺寸列表
const supportedSizes = [
  '512x512',
  '512x768',
  '768x512',
  '768x768',
  '1024x1024',
  '1024x1536',
  '1536x1024'
];

/**
 * 验证尺寸是否支持
 * @param {string} size - 尺寸
 * @returns {boolean}
 */
function isValidSize(size) {
  return supportedSizes.includes(size);
}

/**
 * 文生图 - 单个图片生成
 * @param {object} options - 选项
 * @param {string} options.prompt - 提示词
 * @param {string} [options.size='1024x1024'] - 尺寸
 * @param {number} [options.n=1] - 生成数量
 * @param {string} [options.style='realistic'] - 风格
 * @param {string} [options.negative_prompt=''] - 负面提示词
 * @param {number} [options.maxRetries=3] - 最大重试次数
 * @param {boolean} [options.useCache=true] - 是否使用缓存
 * @returns {Promise<object>} 生成结果
 */
async function generateImage({
  prompt,
  size = '1024x1024',
  n = 1,
  style = 'realistic',
  negative_prompt = '',
  maxRetries = 3,
  useCache = true
} = {}) {
  // 验证尺寸（先验证参数，再检查 API Key）
  if (!isValidSize(size)) {
    return {
      success: false,
      error: `不支持的尺寸：${size}，支持的尺寸：${supportedSizes.join(', ')}`,
      code: 400
    };
  }

  // 验证风格
  if (!styleMap[style]) {
    console.warn(`未知风格：${style}，使用默认风格：realistic`);
    style = 'realistic';
  }

  // 验证 API Key
  if (!validateApiKey()) {
    return {
      success: false,
      error: 'VOLC_API_KEY 环境变量未设置，请先配置火山引擎 API Key',
      code: 401
    };
  }

  // 检查缓存
  const cacheKey = generateCacheKey(prompt, { size, style, n });
  if (useCache) {
    const cached = getFromCache(cacheKey);
    if (cached) {
      console.log('✅ 从缓存命中结果');
      return cached;
    }
  }

  const apiKey = process.env.VOLC_API_KEY;
  const apiBase = process.env.VOLC_API_BASE || 'https://ark.cn-beijing.volces.com/api/v3';
  
  // 构建完整提示词（添加风格描述）
  const stylePrompt = styleMap[style];
  const fullPrompt = `${prompt}, ${stylePrompt}`;
  
  // 构建请求体
  const requestBody = {
    model: process.env.VOLC_IMAGE_MODEL || 'doubao-image-x',
    prompt: fullPrompt,
    n: n,
    size: size
  };
  
  // 添加负面提示词（如果有）
  if (negative_prompt) {
    requestBody.negative_prompt = negative_prompt;
  }

  console.log(`🎨 开始生成图片：${prompt.substring(0, 50)}...`);
  console.log(`   风格：${style}, 尺寸：${size}, 数量：${n}`);

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
          timeout: 120000 // 120 秒超时（图片生成可能较慢）
        }
      );
      
      console.log(`✅ API 调用成功，生成 ${response.data.data.length} 张图片`);
      
      // 下载图片到本地
      const images = await Promise.all(
        response.data.data.map(async (img, idx) => {
          const filename = generateFilename('volc');
          const localPath = await downloadImage(img.url, filename);
          return {
            url: img.url,
            local_path: localPath,
            prompt: prompt,
            size: size,
            style: style,
            index: idx + 1
          };
        })
      );
      
      const result = {
        success: true,
        images: images,
        usage: {
          tokens: response.data.usage?.total_tokens || n * 100,
          cost: (response.data.usage?.total_tokens || n * 100) * 0.0012,
          model: requestBody.model
        }
      };
      
      // 缓存结果
      if (useCache) {
        setCache(cacheKey, result);
      }
      
      return result;
      
    } catch (error) {
      const statusCode = error.response?.status;
      const errorMsg = error.response?.data?.error?.message || error.message;
      
      console.error(`❌ 尝试 ${attempt}/${maxRetries} 失败：${errorMsg}`);
      
      // 401 鉴权失败，不重试
      if (statusCode === 401) {
        return {
          success: false,
          error: '鉴权失败 (401) - 请检查 VOLC_API_KEY 是否正确',
          code: 401
        };
      }
      
      // 400 参数错误，不重试
      if (statusCode === 400) {
        return {
          success: false,
          error: `参数错误 (400): ${errorMsg}`,
          code: 400
        };
      }
      
      // 429 限流或 5xx 服务器错误，重试
      if ((statusCode === 429 || statusCode >= 500) && attempt < maxRetries) {
        const waitTime = sleep(calculateBackoff(attempt));
        console.log(`⏳ 等待 ${waitTime}ms 后重试...`);
        await sleep(calculateBackoff(attempt));
        continue;
      }
      
      // 其他错误
      return {
        success: false,
        error: errorMsg,
        code: statusCode,
        details: error.response?.data
      };
    }
  }
  
  // 所有重试失败
  return {
    success: false,
    error: '达到最大重试次数，仍无法完成生成',
    code: 500
  };
}

/**
 * 批量生成图片
 * @param {string[]} prompts - 提示词数组
 * @param {object} options - 选项
 * @param {number} [options.concurrent=3] - 并发数
 * @param {string} [options.size='1024x1024'] - 尺寸
 * @param {string} [options.style='realistic'] - 风格
 * @returns {Promise<object>} 批量生成结果
 */
async function batchGenerate(prompts, {
  concurrent = 3,
  size = '1024x1024',
  style = 'realistic'
} = {}) {
  const pLimit = require('p-limit');
  const limit = pLimit(concurrent);
  
  if (!Array.isArray(prompts) || prompts.length === 0) {
    return {
      success: false,
      error: 'prompts 必须是非空数组'
    };
  }
  
  console.log(`📦 开始批量生成 ${prompts.length} 张图片，并发数：${concurrent}`);
  
  const results = await Promise.all(
    prompts.map((prompt, idx) =>
      limit(async () => {
        console.log(`\n[${idx + 1}/${prompts.length}] 处理：${prompt.substring(0, 30)}...`);
        return await generateImage({ prompt, size, style, n: 1 });
      })
    )
  );
  
  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);
  
  const totalCost = successful.reduce((sum, r) => sum + (r.usage?.cost || 0), 0);
  
  return {
    success: true,
    total: prompts.length,
    successful: successful.length,
    failed: failed.length,
    images: successful.flatMap(r => r.images),
    failed_prompts: failed.map((f, idx) => ({
      prompt: prompts[results.indexOf(f)],
      error: f.error
    })),
    usage: {
      total_cost: totalCost,
      avg_cost: successful.length > 0 ? totalCost / successful.length : 0
    }
  };
}

module.exports = {
  generateImage,
  batchGenerate,
  styleMap,
  supportedSizes
};
