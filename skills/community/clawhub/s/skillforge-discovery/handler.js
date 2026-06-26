/**
 * SkillForge - OpenClaw 服务发现与调用 Skill
 * 
 * 此 Skill 使 OpenClaw Agent 能够：
 * 1. 自动检测能力缺口
 * 2. 发现匹配的付费 API 服务
 * 3. 调用服务并返回结果
 */

// 能力清单 - 用于匹配任务需求
// 注意：更具体的关键词应该放在前面，优先级更高
const CAPABILITY_KEYWORDS = {
  ocr: ['ocr', '文字识别', '图片转文字', 'optical character', 'image to text', '识别文字', '识别图中文字', '识别图片里的文字', '识别.*图片.*文字', '图片.*文字.*识别'],
  image_generation: ['生成图片', '生成图像', '画图', '作画', '生成.*图片', '生成.*图像', 'create image', 'generate image', 'draw', 'ai art', 'dall-e', 'stable diffusion', 'midjourney', 'generate a picture', 'create a picture', 'make an image', 'make a picture'],
  image_editing: ['编辑图片', '修改图片', '图片编辑', 'edit image', 'image editing', 'modify image', 'photoshop'],
  speech_synthesis: ['语音合成', '文字转语音', 'tts', 'speech synthesis', 'text to speech', '转成语音', '播放语音', '朗读', 'read aloud', 'speak'],
  speech_recognition: ['语音识别', '转录', '语音转文字', 'speech recognition', 'transcribe', 'speech to text', 'transcription'],
  video_generation: ['生成视频', '视频生成', 'create video', 'generate video', 'video generation'],
  video_editing: ['视频编辑', '剪辑视频', 'edit video', 'video editing'],
  text_translation: ['翻译', 'translate', 'translation', '多语言'],
  text_summarization: ['摘要', '总结', 'summarize', 'summary', 'summarization', '概括'],
  sentiment_analysis: ['情感分析', '情绪分析', 'sentiment analysis', '情感', '情绪'],
  entity_extraction: ['实体提取', '命名实体', 'entity extraction', 'ner', 'named entity'],
  code_generation: ['代码生成', '写代码', 'generate code', 'code generation', '编程'],
  code_review: ['代码审查', '代码检查', 'code review', 'code check'],
  data_analysis: ['数据分析', '统计分析', '分析数据', '分析这份', 'data analysis', 'analyze data'],
  web_search: ['网页搜索', '网络搜索', 'web search', 'search web'],
  web_scraping: ['网页抓取', '爬虫', 'web scraping', 'scrape', 'crawl'],
  email_sending: ['发邮件', '发送邮件', 'send email', 'email'],
  sms_sending: ['发短信', '发送短信', 'send sms', 'send message', '短信'],
  calendar_management: ['日历', '日程', 'calendar', 'schedule', 'appointment'],
  file_conversion: ['文件转换', '格式转换', 'file conversion', 'convert file'],
  pdf_processing: ['pdf处理', 'pdf提取', 'pdf合并', 'pdf', 'pdf processing'],
  qrcode_generation: ['二维码', 'qrcode', 'qr code', '生成二维码'],
  map_geocoding: ['地址解析', '经纬度', 'geocoding', '地理编码', '地图'],
  weather_data: ['天气', 'weather', 'weather data', '气象'],
  stock_data: ['股票', 'stock', '股价', 'stock data', '股市'],
  crypto_data: ['加密货币', 'crypto', '比特币', 'bitcoin', 'ethereum', '加密货币价格']
};

// 能力与类别的映射
const CAPABILITY_CATEGORY_MAP = {
  image_generation: 'image',
  image_editing: 'image',
  speech_synthesis: 'audio',
  speech_recognition: 'audio',
  video_generation: 'video',
  video_editing: 'video',
  text_translation: 'text',
  text_summarization: 'text',
  sentiment_analysis: 'text',
  entity_extraction: 'text',
  code_generation: 'code',
  code_review: 'code',
  data_analysis: 'data',
  web_search: 'web',
  web_scraping: 'web',
  email_sending: 'communication',
  sms_sending: 'communication',
  calendar_management: 'productivity',
  file_conversion: 'utility',
  pdf_processing: 'utility',
  ocr: 'vision',
  qrcode_generation: 'utility',
  map_geocoding: 'location',
  weather_data: 'data',
  stock_data: 'data',
  crypto_data: 'data'
};

/**
 * Skill 配置
 */
let config = {
  platform_url: null,
  api_key: null,
  auto_discover: true,
  discover_limit: 3,
  max_cost_per_call: 1.00,
  auto_confirm_free: false
};

/**
 * 初始化 Skill
 * @param {Object} skillConfig - Skill 配置
 */
function init(skillConfig) {
  if (skillConfig) {
    config = { ...config, ...skillConfig };
  }
  
  // 验证必需配置
  if (!config.platform_url) {
    console.error('[SkillForge] 缺少 platform_url 配置');
    return false;
  }
  
  if (!config.api_key) {
    console.error('[SkillForge] 缺少 api_key 配置');
    return false;
  }
  
  console.log('[SkillForge] 初始化成功');
  return true;
}

/**
 * 检测任务中的能力缺口
 * @param {string} task - 用户任务描述
 * @returns {Array<string>} 需要的能力列表
 */
function detectCapabilityGap(task) {
  const taskLower = task.toLowerCase();
  const detectedCapabilities = [];
  
  for (const [capability, keywords] of Object.entries(CAPABILITY_KEYWORDS)) {
    for (const keyword of keywords) {
      // 支持正则表达式匹配（包含特殊字符的关键词）
      if (keyword.includes('.*') || keyword.includes('.+')) {
        const regex = new RegExp(keyword, 'i');
        if (regex.test(task) || regex.test(taskLower)) {
          detectedCapabilities.push(capability);
          break;
        }
      } else {
        // 普通字符串匹配
        if (taskLower.includes(keyword.toLowerCase())) {
          detectedCapabilities.push(capability);
          break;
        }
      }
    }
  }
  
  return [...new Set(detectedCapabilities)];
}

/**
 * 发现服务
 * @param {string} capability - 能力类型
 * @param {number} limit - 返回数量限制
 * @returns {Promise<Object>} 发现结果
 */
async function discoverServices(capability, limit = 3) {
  if (!config.platform_url || !config.api_key) {
    throw new Error('[SkillForge] 未配置 platform_url 或 api_key');
  }
  
  const category = CAPABILITY_CATEGORY_MAP[capability];
  const url = new URL(`${config.platform_url}/v1/discover`);
  url.searchParams.set('capability', capability);
  if (category) {
    url.searchParams.set('category', category);
  }
  url.searchParams.set('limit', limit.toString());
  
  try {
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${config.api_key}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error?.message || `HTTP ${response.status}`);
    }
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('[SkillForge] 服务发现失败:', error.message);
    throw error;
  }
}

/**
 * 调用服务
 * @param {string} serviceId - 服务 ID
 * @param {Object} input - 调用输入
 * @param {Object} options - 调用选项
 * @returns {Promise<Object>} 调用结果
 */
async function invokeService(serviceId, input, options = {}) {
  if (!config.platform_url || !config.api_key) {
    throw new Error('[SkillForge] 未配置 platform_url 或 api_key');
  }
  
  const url = `${config.platform_url}/v1/services/${serviceId}/invoke`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${config.api_key}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ input, options })
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      
      // 处理特定错误
      if (error.error?.code === 'INSUFFICIENT_BALANCE') {
        return {
          success: false,
          error: {
            code: 'INSUFFICIENT_BALANCE',
            message: '余额不足，请充值后重试',
            details: error.error.details
          }
        };
      }
      
      if (error.error?.code === 'SERVICE_OFFLINE') {
        return {
          success: false,
          error: {
            code: 'SERVICE_OFFLINE',
            message: '服务暂时不可用，请选择其他服务'
          }
        };
      }
      
      throw new Error(error.error?.message || `HTTP ${response.status}`);
    }
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('[SkillForge] 服务调用失败:', error.message);
    throw error;
  }
}

/**
 * 格式化服务列表供用户选择
 * @param {Array} services - 服务列表
 * @returns {string} 格式化的文本
 */
function formatServiceList(services) {
  if (!services || services.length === 0) {
    return '未找到匹配的服务';
  }
  
  const lines = ['发现以下可用服务:\n'];
  
  services.forEach((service, index) => {
    const priceStr = service.priceUnit === 'free' 
      ? '免费' 
      : `$${service.price.toFixed(4)}/次`;
    
    const ratingStr = service.rating 
      ? ` ⭐${service.rating.toFixed(1)}` 
      : '';
    
    const callsStr = service.calls 
      ? ` (${(service.calls / 1000).toFixed(1)}k次调用)` 
      : '';
    
    lines.push(`${index + 1}. **${service.name}** - ${priceStr}${ratingStr}${callsStr}`);
    lines.push(`   ${service.description}`);
    lines.push(`   开发者: ${service.developer || '匿名'}\n`);
  });
  
  return lines.join('\n');
}

/**
 * 格式化调用结果
 * @param {Object} result - 调用结果
 * @returns {string} 格式化的文本
 */
function formatInvocationResult(result) {
  if (!result.success) {
    return `调用失败: ${result.error?.message || '未知错误'}`;
  }
  
  const lines = ['服务调用成功!\n'];
  
  // 添加计费信息
  if (result.billing) {
    const charged = result.billing.charged || 0;
    const remaining = result.billing.remaining || 0;
    if (charged > 0) {
      lines.push(`💰 本次消费: $${charged.toFixed(4)}`);
      lines.push(`📊 账户余额: $${remaining.toFixed(2)}\n`);
    } else {
      lines.push(`✅ 免费调用`);
    }
  }
  
  // 添加元信息
  if (result.meta) {
    lines.push(`📡 服务: ${result.meta.serviceName}`);
    lines.push(`⏱️ 耗时: ${result.meta.duration}ms`);
  }
  
  return lines.join('\n');
}

/**
 * Skill 主处理器
 * 根据输入内容决定执行的操作
 * 
 * @param {Object} context - Skill 执行上下文
 * @param {string} context.task - 用户任务描述
 * @param {string} context.action - 执行动作 (detect|discover|invoke)
 * @param {string} context.capability - 指定的能力
 * @param {string} context.serviceId - 服务 ID (调用时)
 * @param {Object} context.input - 调用输入
 * @returns {Promise<Object>} 执行结果
 */
async function handler(context) {
  const { task, action, capability, serviceId, input } = context;
  
  // 1. 检测能力缺口
  if (action === 'detect' || (!action && task)) {
    const capabilities = detectCapabilityGap(task);
    
    if (capabilities.length === 0) {
      return {
        success: true,
        action: 'detect',
        message: '未检测到能力缺口，当前任务可在本地完成',
        capabilities: []
      };
    }
    
    return {
      success: true,
      action: 'detect',
      message: `检测到 ${capabilities.length} 个能力缺口: ${capabilities.join(', ')}`,
      capabilities,
      suggestion: '建议调用 discover 动作查找匹配服务'
    };
  }
  
  // 2. 发现服务
  if (action === 'discover' || capability) {
    const targetCapability = capability || (await detectCapabilityGap(task))[0];
    
    if (!targetCapability) {
      return {
        success: false,
        action: 'discover',
        error: '未指定能力类型，且无法从任务中检测'
      };
    }
    
    try {
      const result = await discoverServices(targetCapability, config.discover_limit);
      
      return {
        success: true,
        action: 'discover',
        capability: targetCapability,
        services: result.data || [],
        formatted: formatServiceList(result.data),
        suggestion: '请让用户选择服务后调用 invoke 动作'
      };
    } catch (error) {
      return {
        success: false,
        action: 'discover',
        error: error.message
      };
    }
  }
  
  // 3. 调用服务
  if (action === 'invoke') {
    if (!serviceId) {
      return {
        success: false,
        action: 'invoke',
        error: '缺少服务 ID (serviceId)'
      };
    }
    
    try {
      // 检查费用限制
      if (config.max_cost_per_call && input?._estimatedCost > config.max_cost_per_call) {
        return {
          success: false,
          action: 'invoke',
          error: `预估费用 $${input._estimatedCost} 超过限制 $${config.max_cost_per_call}`
        };
      }
      
      const result = await invokeService(serviceId, input);
      
      return {
        success: result.success,
        action: 'invoke',
        serviceId,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
        formatted: formatInvocationResult(result),
        error: result.error
      };
    } catch (error) {
      return {
        success: false,
        action: 'invoke',
        serviceId,
        error: error.message
      };
    }
  }
  
  // 未知操作
  return {
    success: false,
    error: `未知操作: ${action}。支持的操作: detect, discover, invoke`
  };
}

// 导出 Skill 接口
export {
  init,
  handler,
  detectCapabilityGap,
  discoverServices,
  invokeService,
  formatServiceList,
  formatInvocationResult,
  CAPABILITY_KEYWORDS,
  CAPABILITY_CATEGORY_MAP
};

// 默认导出
export default {
  init,
  handler,
  detectCapabilityGap,
  discoverServices,
  invokeService
};