#!/usr/bin/env node
/**
 * Auto Discover - 自动发现与安装
 *
 * Phase 2: 自动化（A+B）
 * A. 自动发现需求
 * B. 自动执行流程
 */

const { skillsList, skillsFind, skillsAdd, clawhubAdd } = require('./skills-cli');
const { MAGIC, ERROR_CODES, LOG_SCHEMA, DISCOVER_CONFIG } = require('./constants');

// ==================== 预编译正则（避免重复编译）====================
const RE = {
  // 明确触发词（英文）
  explicitTriggers: [
    { re: /find a skill for/i, weight: MAGIC.WEIGHT_EXPLICIT },
    { re: /is there a skill (for|that|to)/i, weight: MAGIC.WEIGHT_EXPLICIT },
    { re: /how do i (do|make|create|build)/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /can you (help me with|do)/i, weight: MAGIC.WEIGHT_MEDIUM },
    { re: /i need (a skill|help with)/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /can i use/i, weight: MAGIC.WEIGHT_MEDIUM },
    { re: /help me (with|to|build|create|make|do)/i, weight: MAGIC.WEIGHT_MEDIUM },
    { re: /looking for/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /\bi want (to|a|an)/i, weight: MAGIC.WEIGHT_MEDIUM },
    // 英文推荐句式
    { re: /recommend.*(tool|library|package|skill|plugin)/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /any.*(tool|library|package|skill|plugin).*(for|that)/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /what('s| is).*tool/i, weight: MAGIC.WEIGHT_MEDIUM },
    // 中文明确触发词（优先级1）
    { re: /找.*?(skill|技能|工具)/i, weight: MAGIC.WEIGHT_EXPLICIT },
    { re: /有没有.*?(skill|技能|工具)/i, weight: MAGIC.WEIGHT_EXPLICIT },
    { re: /安装.*?(skill|技能)/i, weight: MAGIC.WEIGHT_EXPLICIT },
    // 中文触发词（优先级0.8-0.9）
    { re: /有什么工具/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /有什么工具可以/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /推荐一个/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /能不能/i, weight: MAGIC.WEIGHT_MEDIUM },
    { re: /想要/i, weight: MAGIC.WEIGHT_MEDIUM },
    { re: /求推荐/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /能帮我/i, weight: MAGIC.WEIGHT_MEDIUM },
    { re: /帮我推荐/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /帮我找个/i, weight: MAGIC.WEIGHT_HIGH },
    // 中文句式（优先级0.9）
    { re: /怎么.*?(做|实现|创建|部署|写)/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /如何.*?(做|实现|创建|部署|写)/i, weight: MAGIC.WEIGHT_HIGH },
    // 中文句式（优先级0.8）
    { re: /能.*?(帮我|给我).*?(做|写|优化|部署)/i, weight: MAGIC.WEIGHT_MEDIUM },
    { re: /需要.*?(skill|技能|工具)/i, weight: MAGIC.WEIGHT_HIGH },
    { re: /帮我.*?(做|写|优化|部署|处理)/i, weight: MAGIC.WEIGHT_MEDIUM_HIGH },
    // "怎么样才能" 是需求导向，正面触发
    { re: /怎么样才能/i, weight: MAGIC.WEIGHT_HIGH }
  ],

  // 领域关键词（英文）
  domainKeywordsEn: [
    { re: /deploy|deployment|ci[\/\\-]cd|docker|kubernetes|k8s/i, domain: 'devops' },
    { re: /test|testing|jest|playwright|cypress|vitest/i, domain: 'testing' },
    { re: /design|ui|ux|css|tailwind|component/i, domain: 'design' },
    { re: /doc|documentation|readme|changelog/i, domain: 'docs' },
    { re: /review|lint|refactor|best practice/i, domain: 'code-quality' },
    { re: /pdf|excel|csv|json.*process/i, domain: 'data-processing' },
    { re: /image|photo|compress|resize|ocr/i, domain: 'image-processing' },
    { re: /video|ffmpeg|convert/i, domain: 'video-processing' },
    { re: /performance|optimize|speed|fast/i, domain: 'performance' },
    // 英文领域关键词（网络/API、数据库、AI/ML、安全、移动端、游戏）
    { re: /api|rest|graphql|endpoint|http/i, domain: 'network-api' },
    { re: /database|db|sql|mongodb|postgresql|mysql|redis/i, domain: 'database' },
    {
      re: /ai|ml|machine learning|nlp|gpt|llm|chatgpt|openai|deep learning|tensorflow|pytorch/i,
      domain: 'ai-ml'
    },
    { re: /security|secure|crypto|encrypt|auth|authentication|authorization/i, domain: 'security' },
    { re: /mobile|ios|android|react native|flutter|swift|kotlin/i, domain: 'mobile' },
    { re: /game|unity|unreal|godot|game dev|2d|3d/i, domain: 'gaming' }
  ],

  // 领域关键词（中文）
  domainKeywordsZh: [
    { re: /部署|发布|上线/i, domain: 'devops' },
    { re: /测试|单元测试|e2e|自动化测试/i, domain: 'testing' },
    { re: /设计|样式|组件|界面/i, domain: 'design' },
    { re: /文档|说明/i, domain: 'docs' },
    { re: /审查|检查|重构|最佳实践|代码质量/i, domain: 'code-quality' },
    { re: /pdf|excel|csv|数据处理|解析|转换/i, domain: 'data-processing' },
    { re: /图片|图像|压缩|裁剪|ocr|识别/i, domain: 'image-processing' },
    { re: /视频|剪辑|转码|压缩/i, domain: 'video-processing' },
    { re: /性能|优化|加速|提升/i, domain: 'performance' },
    // 中文领域关键词（网络/API、数据库、AI/ML、安全、移动端、游戏）
    { re: /api|接口|rest|graphql|网络请求|http/i, domain: 'network-api' },
    { re: /数据库|db|sql|mongodb|postgresql|mysql|redis/i, domain: 'database' },
    {
      re: /人工智能|ai|机器学习|nlp|gpt|llm|chatgpt|深度学习|tensorflow|pytorch/i,
      domain: 'ai-ml'
    },
    { re: /安全|加密|解密|认证|授权|权限/i, domain: 'security' },
    { re: /移动端|ios|android|react native|flutter|swift|kotlin|手机端/i, domain: 'mobile' },
    { re: /游戏|unity|unreal|godot|游戏开发|2d|3d/i, domain: 'gaming' }
  ],

  // 负面模式（英文）
  negativePatternsEn: [
    /^(what is|what's|how to|explain|describe)/i,
    /^(why|when|who|where)/i,
    /how (much|many|long)/i,
    /tell me (about|what)/i,
    /^(just|only) (a|one)/i,
    /^(i|i'm|i am) (just|only) (a|one)/i,
    /can i ask/i
  ],

  // 负面模式（中文 - 精确匹配避免误杀"怎么样才能"）
  negativePatternsZh: [
    /^什么/i,
    /^为什么/i,
    /^什么时候/i,
    /^谁/i,
    /^哪里/i,
    /^(是|有).*吗$/i, // "是xxx吗？"纯询问
    /天气|时间|日期|新闻/i, // 纯信息查询
    /错误|bug|修复|问题|报错/i, // 调试问题
    /(?:^|有)什么(?:问题|bug|错|报错)/i, // "有什么问题"纯询问
    /(?:咋样|怎么样)$/i // 精确匹配 "怎么样" 或 "咋样" 结尾（避免误杀"怎么样才能..."）
  ]
};

// ==================== 配置 ====================
const CONFIG = {
  ...DISCOVER_CONFIG,
  cache: {
    findResults: new Map(),
    ttl: DISCOVER_CONFIG.cache.ttl,
    maxSize: DISCOVER_CONFIG.cache.maxSize
  }
};

// ==================== A. 自动发现需求 ====================

/**
 * 分析用户输入，判断是否需要搜索 skill
 * 基于官方 find-skills 的触发条件
 *
 * 修复：负面模式采用行首锚定（^）避免误杀
 * "怎么样才能..."中的"怎么样"不是行首，不会被^什么匹配
 */
function analyzeNeed(userInput) {
  const input = userInput.toLowerCase().trim();

  let confidence = 0;
  let matchedDomain = null;
  let query = input;

  // ---- 1. 检查明确触发词 ----
  for (const trigger of RE.explicitTriggers) {
    if (trigger.re.test(input)) {
      confidence = Math.max(confidence, trigger.weight);
      query = input.replace(trigger.re, '').trim();
    }
  }

  // ---- 2. 检查领域关键词（英文） ----
  for (const kw of RE.domainKeywordsEn) {
    if (kw.re.test(input)) {
      confidence = Math.max(confidence, MAGIC.WEIGHT_DOMAIN);
      matchedDomain = kw.domain;
    }
  }

  // ---- 3. 检查领域关键词（中文） ----
  for (const kw of RE.domainKeywordsZh) {
    if (kw.re.test(input)) {
      confidence = Math.max(confidence, MAGIC.WEIGHT_DOMAIN);
      matchedDomain = kw.domain;
    }
  }

  // 领域关键词触发时使用完整输入作为搜索词
  if (matchedDomain && confidence < MAGIC.DOMAIN_MIN_CONFIDENCE) {
    query = input;
  }

  // ---- 4. 检查负面模式（英文，行首锚定避免误杀）----
  for (const neg of RE.negativePatternsEn) {
    if (neg.test(input)) {
      confidence *= MAGIC.NEGATIVE_MULTIPLIER;
    }
  }

  // ---- 5. 检查负面模式（中文，行首锚定避免误杀）----
  for (const neg of RE.negativePatternsZh) {
    if (neg.test(input)) {
      confidence *= MAGIC.NEGATIVE_MULTIPLIER;
    }
  }

  return {
    shouldSearch: confidence >= CONFIG.confidenceThreshold,
    confidence,
    query: query.substring(0, MAGIC.QUERY_MAX_LENGTH),
    domain: matchedDomain
  };
}

// ==================== B. 自动执行流程 ====================

/**
 * 选择最佳 skill
 */
function selectBest(skills) {
  // skills.sh 已验证，仅按安装量 + 来源偏好排序
  const scored = skills.map((skill) => {
    let score = 0;

    // 安装量分数 (0-40)
    score += Math.min(skill.installs / MAGIC.MIN_INSTALLS_SCALE, 4) * MAGIC.INSTALLS_SCORE_FACTOR;

    // 可信来源加分
    const isTrusted = CONFIG.trustedOwners.includes(skill.owner);
    score += isTrusted ? MAGIC.TRUSTED_SCORE : MAGIC.UNTRUSTED_SCORE;

    return { skill, score };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored[0];
}

/**
 * 参数校验
 */
function validateParams(userInput, options) {
  const errors = [];

  // 校验 userInput 类型和长度
  if (typeof userInput !== 'string') {
    errors.push('userInput 必须是字符串');
  } else if (userInput.trim().length === 0) {
    errors.push('userInput 不能为空');
  } else if (userInput.length > 500) {
    errors.push('userInput 不能超过 500 字符');
  }

  // 校验 options 为 object 或 undefined
  if (options !== undefined && typeof options !== 'object') {
    errors.push('options 必须是对象');
  } else if (options && typeof options === 'object') {
    if ('dryRun' in options && typeof options.dryRun !== 'boolean') {
      errors.push('options.dryRun 必须是布尔值');
    }
  }

  return errors;
}

/**
 * 带缓存 + 容量上限的搜索
 * 缓存超过 maxSize 时清除最旧的条目
 */
async function skillsFindCached(query) {
  // 参数校验
  if (typeof query !== 'string' || query.trim().length === 0) {
    throw new Error('query 参数无效：必须是非空字符串');
  }

  const cacheKey = query.toLowerCase().trim();
  const cached = CONFIG.cache.findResults.get(cacheKey);

  if (cached && Date.now() - cached.timestamp < CONFIG.cache.ttl) {
    console.log(`📋 使用缓存: "${query}"`);
    return cached.results;
  }

  const results = await skillsFind(query);

  // 缓存超过上限时清除最旧的条目（淘汰最久未使用的）
  if (CONFIG.cache.findResults.size >= CONFIG.cache.maxSize) {
    let oldestKey = null;
    let oldestTime = Infinity;
    for (const [key, val] of CONFIG.cache.findResults) {
      if (val.timestamp < oldestTime) {
        oldestTime = val.timestamp;
        oldestKey = key;
      }
    }
    if (oldestKey) {
      CONFIG.cache.findResults.delete(oldestKey);
      console.log(`🗑️  缓存已满，淘汰最旧条目: "${oldestKey}"`);
    }
  }

  CONFIG.cache.findResults.set(cacheKey, {
    results,
    timestamp: Date.now()
  });

  return results;
}

// LOG_SCHEMA 从 constants.js 导入

/**
 * 统一日志格式（供外部 logDiscovery 调用）
 * @param {string} action - 操作类型（必须是 LOG_SCHEMA.ACTIONS 之一）
 * @param {Object} data - 日志数据
 * @returns {Object} 符合 Schema 的日志对象
 */
function buildLogEntry(action, data) {
  if (!LOG_SCHEMA.ACTIONS.includes(action)) {
    action = 'error';
  }
  return {
    schema: LOG_SCHEMA.VERSION,
    timestamp: new Date().toISOString(),
    action,
    ...data
  };
}

// ==================== 脱敏工具 ====================

/** 字段名匹配这些模式时，值会被遮蔽 */
const SANITIZE_REDACT_KEY_PATTERNS = [
  /\btoken\b/i,
  /\bsecret\b/i,
  /\bpassword\b/i,
  /\bapi[_-]?key\b/i,
  /\bcredential\b/i,
  /\bauthorization\b/i
];

/** 字符串值匹配这些模式时，整个值会被遮蔽 */
const SANITIZE_REDACT_VALUE_PATTERNS = [
  /\bBearer\s+[\w.-]+/i,
  /\bsk-[\w.-]+/,
  /ghp_[\w]+/,
  /===+\s*[A-Za-z]+\s*===+/ // OAUTH 授权页特征（精确匹配）
];

/**
 * 递归脱敏对象中的敏感信息（用于日志记录）
 *
 * 策略：只遮蔽真正敏感的字段（token/password/apiKey 等），
 * 业务字段（installs/confidence/domain/success 等）保留原值以保证日志可用性。
 */
function sanitize(obj, depth = 0) {
  if (depth > MAGIC.SANITIZE_MAX_DEPTH) return '[MAX_DEPTH]';
  if (obj === null || obj === undefined) return obj;
  if (typeof obj !== 'object') {
    if (typeof obj === 'string') {
      for (const p of SANITIZE_REDACT_VALUE_PATTERNS) {
        if (p.test(obj)) return '***';
      }
    }
    return obj;
  }
  if (Array.isArray(obj)) {
    return obj.map((item) => sanitize(item, depth + 1));
  }

  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    // 字段名匹配敏感模式 → 遮蔽值
    let isSensitiveKey = false;
    for (const p of SANITIZE_REDACT_KEY_PATTERNS) {
      if (p.test(key)) {
        isSensitiveKey = true;
        break;
      }
    }

    if (isSensitiveKey) {
      result[key] = '***';
    } else {
      result[key] = sanitize(value, depth + 1);
    }
  }
  return result;
}

// ==================== 管道函数 ====================

/**
 * 搜索 skill（带缓存 + 错误分类）
 */
async function searchSkills(query) {
  console.log(`💡 搜索: "${query}"`);

  let results;
  try {
    results = await skillsFindCached(query);
  } catch (error) {
    const errorCode =
      error.message.includes('not found') || error.message.includes('ENOENT')
        ? ERROR_CODES.CLI_NOT_FOUND
        : error.message.includes('ETIMEDOUT') || error.message.includes('network')
          ? ERROR_CODES.NETWORK_ERROR
          : ERROR_CODES.SEARCH_FAILED;

    return {
      success: false,
      stage: 'search',
      outcome: 'failed',
      reason: 'search_failed',
      errorCode,
      error: error.message,
      skill: null,
      candidates: [],
      message: '搜索失败，请稍后重试'
    };
  }

  console.log(`📋 找到 ${results.length} 个结果`);

  if (results.length === 0) {
    return {
      success: false,
      stage: 'search',
      outcome: 'failed',
      reason: 'no_results',
      errorCode: ERROR_CODES.NO_RESULTS,
      skill: null,
      candidates: [],
      message: '未找到相关 skill'
    };
  }

  return { success: true, results };
}

/**
 * 筛选并选择最佳 skill
 */
function filterAndSelect(results) {
  // skills.sh 上的 skill 均已验证，无需二次过滤，直接选最佳
  const best = selectBest(results);
  console.log(`⭐ 最佳: ${best.skill.fullName} (评分: ${Math.round(best.score)})`);

  return { success: true, best };
}

/**
 * 决定安装并执行
 */
async function resolveInstall(best, dryRun) {
  // 检查是否已安装
  try {
    const installed = await skillsList({ global: true });
    const isInstalled = installed.some(
      (s) => s.name === best.skill.skill || s.name === best.skill.fullName.replace(/[@/]/g, '-')
    );

    if (isInstalled) {
      return {
        success: true,
        stage: 'install',
        outcome: 'already_installed',
        reason: null,
        errorCode: null,
        alreadyInstalled: true,
        skill: best.skill,
        candidates: [],
        message: `✅ ${best.skill.fullName} 已安装`
      };
    }
  } catch (_e) {
    // 忽略检查错误，继续安装
  }

  const isClawhub = best.skill.source === 'clawhub';
  const installCmd = isClawhub ? 'clawhub install' : 'npx skills add';

  if (dryRun) {
    return {
      success: true,
      stage: 'install',
      outcome: 'dry_run',
      reason: null,
      errorCode: null,
      dryRun: true,
      skill: best.skill,
      validation: best.validation,
      candidates: [],
      message: `[模拟] 将安装 ${best.skill.fullName}${isClawhub ? ' (ClawHub)' : ''}`
    };
  }

  console.log(`📦 安装${isClawhub ? ' (ClawHub)' : ''}: ${best.skill.fullName}`);
  try {
    const installResult = isClawhub
      ? await clawhubAdd(best.skill.fullName)
      : await skillsAdd(best.skill.fullName, { global: true, yes: true });

    return {
      success: true,
      stage: 'install',
      outcome: 'installed',
      reason: null,
      errorCode: null,
      installed: true,
      skill: best.skill,
      validation: best.validation,
      result: installResult,
      candidates: [],
      message: `✅ 已自动安装 ${best.skill.fullName}${isClawhub ? ' (ClawHub)' : ''}`
    };
  } catch (error) {
    return {
      success: false,
      stage: 'install',
      outcome: 'failed',
      reason: 'install_failed',
      errorCode: ERROR_CODES.INSTALL_FAILED,
      skill: best.skill,
      error: error.message,
      fallback: `手动安装: ${installCmd} ${best.skill.fullName}`,
      candidates: [],
      message: `安装失败: ${error.message}`
    };
  }
}

// ==================== 主流程（编排） ====================

/**
 * 主流程：自动发现与安装
 *
 * 编排 analyzeNeed → searchSkills → filterAndSelect → resolveInstall
 */
async function autoDiscover(userInput, options = {}) {
  const validationErrors = validateParams(userInput, options);
  if (validationErrors.length > 0) {
    throw new Error(`参数校验失败: ${validationErrors.join('; ')}`);
  }

  const { dryRun = true } = options;

  console.log(`🔍 分析: "${userInput.substring(0, 50)}..."`);

  // 1. 分析需求
  const need = analyzeNeed(userInput);
  console.log(`📊 置信度: ${Math.round(need.confidence * 100)}%`);

  if (!need.shouldSearch) {
    return {
      success: false,
      stage: 'analyze',
      outcome: 'skipped',
      reason: 'confidence_too_low',
      errorCode: ERROR_CODES.CONFIDENCE_TOO_LOW,
      confidence: need.confidence,
      skill: null,
      candidates: [],
      message: '置信度不足，跳过自动发现'
    };
  }

  // 2. 搜索
  const searchResult = await searchSkills(need.query);
  if (!searchResult.success) return searchResult;

  // 3. 筛选
  const selectResult = filterAndSelect(searchResult.results);
  if (!selectResult.success) return selectResult;

  // 4. 安装
  return resolveInstall(selectResult.best, dryRun);
}

// ==================== 导出 ====================
module.exports = {
  // 公共 API
  analyzeNeed,
  validateParams,
  selectBest,
  autoDiscover,
  searchSkills,
  filterAndSelect,
  resolveInstall,
  // 内部工具（供 openclaw-hook 使用）
  buildLogEntry,
  sanitize,
  LOG_SCHEMA,
  skillsFindCached,
  CONFIG
};
