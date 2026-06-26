/**
 * AI 文章改写模块
 * 深度改写文章内容，去 AI 味，提升原创度
 */

import axios from 'axios';
import path from 'path';
import { fileURLToPath } from 'url';
import {
  loadOpenClawEnv,
  resolveDashScopeKey,
  resolveOpenAICompatibleKey,
  getOpenAICompatibleBaseUrl,
  getOpenAICompatibleModel,
  getDashScopeChatModel
} from '../lib/openclaw_env.js';

const __rewriteDir = path.dirname(fileURLToPath(import.meta.url));
loadOpenClawEnv({ skillRoot: path.join(__rewriteDir, '..') });

/**
 * AI 改写文章
 * @param {string} content - 原始文章内容
 * @param {Object} options - 改写选项
 * @returns {Promise<string>} 改写后的文章
 */
export async function rewriteArticle(content, options = {}) {
  const {
    style = 'original',  // original, liurun, casual, formal
    length = 'same',     // same, shorter, longer
    tone = 'neutral'     // neutral, professional, friendly
  } = options;
  
  console.log('  ✍️  开始 AI 改写...');
  console.log(`     风格：${style}, 长度：${length}, 语气：${tone}`);
  
  // 构建提示词
  const prompt = buildRewritePrompt(content, style, length, tone);
  
  try {
    // OpenClaw / 多源 Key：优先使用 OpenAI 兼容 API（Gemini），其次 DashScope
    const openaiApiKey = resolveOpenAICompatibleKey();
    const dashscopeApiKey = resolveDashScopeKey();
    
    if (openaiApiKey) {
      console.log(
        `  🚀 使用 OpenAI 兼容 API (${getOpenAICompatibleModel()})`
      );
      const rewrittenContent = await callOpenAIAPI(prompt, openaiApiKey);
      console.log('  ✅ 改写完成');
      return rewrittenContent;
    } else if (dashscopeApiKey) {
      console.log(
        `  🚀 使用阿里云 DashScope API (${getDashScopeChatModel()})`
      );
      const rewrittenContent = await callDashScopeAPI(prompt, dashscopeApiKey);
      console.log('  ✅ 改写完成');
      return rewrittenContent;
    } else {
      console.log('  ⚠️  未配置 API Key，使用本地改写模式');
      return localRewrite(content, style);
    }
    
  } catch (error) {
    console.error('  ❌ 改写失败:', error.message);
    console.log('  ❌ 禁止降级到本地改写模式，改写终止');
    throw error;
  }
}

/**
 * 构建改写提示词
 */
function buildRewritePrompt(content, style, length, tone) {
  let systemPrompt = '你是一位专业的内容改写专家，擅长深度改写文章，去除 AI 写作痕迹，提升原创度。';
  
  let styleInstruction = '';
  switch (style) {
    case 'liurun':
      styleInstruction = '请参考刘润公众号的写作风格：开篇切入商业案例，引入独特洞察，用 2-3 个真实案例论证，给出明确结论和行动建议。语言简洁有力，逻辑清晰，很少使用 emoji。';
      break;
    case 'casual':
      styleInstruction = '请使用轻松随意的口语化风格，像朋友聊天一样自然。';
      break;
    case 'formal':
      styleInstruction = '请使用正式的专业风格，保持学术严谨性。';
      break;
    default:
      styleInstruction = '请保持原文的核心信息，但用更自然、原创的方式重新表达。';
  }
  
  let lengthInstruction = '';
  switch (length) {
    case 'shorter':
      lengthInstruction = '请将文章压缩到原文的 70% 左右，删除冗余内容。';
      break;
    case 'longer':
      lengthInstruction = '请将文章扩展到原文的 150% 左右，补充更多细节和案例。';
      break;
    default:
      lengthInstruction = '请保持与原文相近的篇幅。';
  }
  
  let toneInstruction = '';
  switch (tone) {
    case 'professional':
      toneInstruction = '请使用专业、权威的语气。';
      break;
    case 'friendly':
      toneInstruction = '请使用友好、亲切的语气。';
      break;
    default:
      toneInstruction = '请保持中性、客观的语气。';
  }
  
  return {
    system: systemPrompt,
    user: `请改写以下文章：

要求：
${styleInstruction}
${lengthInstruction}
${toneInstruction}

改写策略：
1. **结构重组**：调整段落顺序，打乱原文结构
2. **语言改写**：去除 AI 高频词，使用自然表达
3. **论据替换**：用不同的案例或数据论证相同观点
4. **视角转换**：改变叙事角度（如从时间线改为问题导向）

原文：
${content}

请直接输出改写后的全文，不要添加任何解释。`
  };
}

/**
 * 调用阿里云 DashScope API
 */
async function callDashScopeAPI(prompt, apiKey) {
  try {
    const response = await axios.post(
      'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
      {
        model: getDashScopeChatModel(),
        messages: [
          { role: 'system', content: prompt.system },
          { role: 'user', content: prompt.user }
        ],
        temperature: 0.7,
        max_tokens: 12000
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return response.data.choices[0].message.content;
  } catch (error) {
    if (error.response) {
      console.error('  DashScope API 错误:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('  DashScope API 网络错误:', error.message);
    } else {
      console.error('  DashScope API 请求错误:', error.message);
    }
    throw error;
  }
}

/**
 * 调用 OpenAI API
 */
async function callOpenAIAPI(prompt, apiKey) {
  const baseUrl = getOpenAICompatibleBaseUrl();
  const response = await axios.post(
    `${baseUrl}/chat/completions`,
    {
      model: getOpenAICompatibleModel(),
      messages: [
        { role: 'system', content: prompt.system },
        { role: 'user', content: prompt.user }
      ],
      temperature: 0.7,
      max_tokens: 12000
    },
    {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data.choices[0].message.content;
}

/**
 * 本地改写（降级方案，不使用 LLM）
 */
function localRewrite(content, style) {
  console.log('  📝 使用本地规则改写...');
  
  let rewritten = content;
  
  // 1. 替换 AI 高频词
  const aiWords = {
    '赋能': '提供能力支持',
    '闭环': '完整流程',
    '生态': '生态系统',
    '抓手': '关键手段',
    '底层逻辑': '基本原理',
    '范式': '模式',
    '沉淀': '积累',
    '势能': '优势',
    '值得注意的是': '',
    '事实上': '',
    '总体来说': '',
    '不难发现': '',
    '提升能力': '增强能力',
    '推动进程': '促进发展'
  };
  
  Object.entries(aiWords).forEach(([aiWord, replacement]) => {
    const regex = new RegExp(aiWord, 'g');
    rewritten = rewritten.replace(regex, replacement);
  });
  
  // 2. 简化长句
  rewritten = rewritten.replace(/，([^，]{50,})，/g, '。$1。');
  
  // 3. 删除意义膨胀句
  rewritten = rewritten.replace(/(标志性|里程碑|深远影响|重要意义)/g, '重要');
  
  // 4. 去除虚假权威
  rewritten = rewritten.replace(/(专家认为|业内普遍认为|研究表明)(.*?)(。|，)/g, '$2$3');
  
  // 5. 删除空洞结尾
  rewritten = rewritten.replace(/(未来可期|值得期待|前景广阔|潜力巨大)(。|！)/g, '。');
  
  // 6. 减少破折号滥用
  rewritten = rewritten.replace(/——(.*?)——/g, '，$1，');
  
  // 7. 去除过度加粗
  rewritten = rewritten.replace(/\*\*(.*?)\*\*/g, '$1');
  
  // 8. 简化列表格式
  rewritten = rewritten.replace(/\*\*(\d+)\.\*\*/g, '$1.');
  
  console.log('  ✅ 本地改写完成');
  return rewritten;
}

/**
 * 去 AI 味处理
 * @param {string} content - 文章内容
 * @returns {string} 处理后的内容
 */
export function removeAiTrace(content) {
  console.log('  🔍 去除 AI 写作痕迹...');
  
  let cleaned = content;
  
  // AI 痕迹识别清单
  const patterns = [
    // 1. 意义膨胀
    { pattern: /(具有|标志着|意味着)(.*?)(里程碑|划时代|深远)意义/g, replacement: '$1$2重要意义' },
    
    // 2. 虚假权威
    { pattern: /(专家|业内|研究)(表明|认为|指出)(.*?)(。|，)/g, replacement: '$3$4' },
    
    // 3. 伪深度动词
    { pattern: /(提升|赋能|推动|促进)(.*?)(能力|进程|发展)/g, replacement: '增强$2能力' },
    
    // 4. 广告语气
    { pattern: /(卓越|极致|全方位|多维度)(.*?)(体验|服务|方案)/g, replacement: '优质$2服务' },
    
    // 5. 填充短语
    { pattern: /(事实上|值得注意的是|总体来说|不难发现)(，|。)/g, replacement: '$2' },
    
    // 6. 空洞结尾
    { pattern: /(未来可期|值得期待|前景广阔|潜力巨大|任重道远)(。|！)/g, replacement: '。' },
    
    // 7. 负向并列
    { pattern: /不仅(.*?)，而且(.*?)，更(.*?)/g, replacement: '$1。$2。$3' },
    
    // 8. 三段式强拆
    { pattern: /第一，(.*?)。第二，(.*?)。第三，(.*?)。/g, replacement: '$1。$2。$3' },
    
    // 9. 破折号滥用
    { pattern: /——(.*?)——/g, replacement: '，$1，' },
    
    // 10. 过度强调
    { pattern: /\*\*(.*?)\*\*/g, replacement: '$1' }
  ];
  
  patterns.forEach(({ pattern, replacement }) => {
    cleaned = cleaned.replace(pattern, replacement);
  });
  
  console.log('  ✅ AI 痕迹清理完成');
  return cleaned;
}

/**
 * 生成备选标题
 * @param {string} content - 文章内容
 * @returns {Promise<string[]>} 备选标题列表
 */
export async function generateTitles(content) {
  console.log('  🎯 生成备选标题...');
  
  // 提取关键词
  const keywords = extractKeywords(content);
  
  const titles = [];
  
  // 疑问型
  titles.push(`为什么${keywords[0] || '它'}还在用这种方法？`);
  
  // 数字型
  titles.push(`3 个被忽略的${keywords[0] || '关键'}技巧`);
  
  // 悬念型
  titles.push(`${keywords[0] || '这'}的真相，90% 的人不知道`);
  
  // 痛点型
  titles.push(`别再${keywords[1] || '这样做'}了，试试这个方法`);
  
  // 观点型
  titles.push(`${keywords[0] || '这件事'}，可能一开始就做错了`);
  
  console.log('  ✅ 生成 5 个备选标题');
  return titles;
}

/**
 * 提取关键词（优化版本）
 */
function extractKeywords(content) {
  // 1. 清理 HTML 标签
  let cleanContent = content.replace(/<[^>]+>/g, ' ');
  
  // 2. 解码 HTML 实体
  cleanContent = cleanContent
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&ldquo;/g, '"')
    .replace(/&rdquo;/g, '"')
    .replace(/&lsquo;/g, "'")
    .replace(/&rsquo;/g, "'")
    .replace(/&mdash;/g, '—')
    .replace(/&hellip;/g, '…');
  
  // 3. 移除特殊字符和多余空格
  cleanContent = cleanContent
    .replace(/[^\w\s\u4e00-\u9fa5]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  
  // 4. 分词
  const words = cleanContent.split(/\s+/);
  
  // 5. 停用词表（扩展版）
  const stopWords = new Set([
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
    '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
    '他', '她', '它', '们', '这个', '那个', '什么', '怎么', '可以',
    '我们', '他们', '她们', '它们', '这些', '那些', '一些', '很多',
    '问题', '系统', '用户', '数据', '技术', '方法', '方式', '进行',
    '然后', '最后', '最后', '但是', '而且', '并且', '或者', '如果',
    '因为', '所以', '虽然', '但是', '不仅', '而且', '除了', '关于',
    '对于', '通过', '为了', '除了', '包括', '比如', '例如'
  ]);
  
  // 6. 统计词频
  const freq = {};
  words.forEach(word => {
    // 过滤：长度 2-10 的中文或英文单词
    if (word.length >= 2 && word.length <= 10 && !stopWords.has(word)) {
      // 只保留包含中文或至少 3 个英文字母的词
      if (/[\u4e00-\u9fa5]/.test(word) || word.length >= 3) {
        freq[word] = (freq[word] || 0) + 1;
      }
    }
  });
  
  // 7. 返回最高频的 5 个词
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([word]) => word);
}
