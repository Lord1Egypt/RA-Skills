/**
 * 网页抓取模块
 * 支持多种类型网页的内容提取
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

// DeepSeek LLM 接口
class DeepSeekLLM {
  constructor(config = {}) {
    this.apiKey = config.apiKey || process.env.DEEPSEEK_API_KEY;
    this.model = config.model || 'deepseek-chat';
    this.baseUrl = 'https://api.deepseek.com';
  }

  async complete(prompt) {
    if (!this.apiKey) {
      throw new Error('未配置 DeepSeek API Key');
    }

    const response = await fetch(`${this.baseUrl}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: this.model,
        messages: [
          { role: 'system', content: '你是一个智能助手，负责生成结构化摘要。只返回JSON格式，不要其他内容。' },
          { role: 'user', content: prompt }
        ]
      })
    });

    const data = await response.json();
    if (data.choices && data.choices[0]) {
      return data.choices[0].message.content;
    }
    throw new Error('DeepSeek LLM 调用失败: ' + JSON.stringify(data));
  }
}

// 简单提取 - 不需要 LLM
function extractKeywords(text) {
  const commonWords = ['的', '是', '在', '了', '和', '与', '或', '等', '可以', '进行', '使用', '通过', '以及', '对于', '关于'];
  const words = text.split(/[，。、！？：；""''（）【】《》\s]+/).filter(w => w.length > 1);
  const wordCount = {};
  words.forEach(w => {
    if (!commonWords.includes(w)) wordCount[w] = (wordCount[w] || 0) + 1;
  });
  return Object.entries(wordCount).sort((a, b) => b[1] - a[1]).slice(0, 5).map(e => e[0]);
}

function suggestCategory(tags) {
  const categoryMap = {
    'AI': 'AI', '大模型': 'AI', '模型': 'AI', 'GPT': 'AI', 'LLM': 'AI',
    '产品': '产品', '功能': '产品', '设计': '产品', '用户': '产品',
    '代码': '编程', '开发': '编程', '技术': '编程', 'API': '编程',
    '学习': '阅读', '教程': '阅读', '文章': '阅读', '观点': '阅读',
    '生活': '生活', '健康': '生活', '工作': '生活'
  };
  for (const tag of tags) {
    for (const [key, cat] of Object.entries(categoryMap)) {
      if (tag.includes(key)) return cat;
    }
  }
  return '阅读';
}

// LLM 接口 - 暂时使用简单提取
class SimpleLLM {
  async complete(content) {
    // 简单关键词提取 + 分类
    const tags = extractKeywords(content);
    const summary = content.split(/[。！？\n]/).filter(s => s.length > 10).slice(0, 3).map(s => s.trim() + '。');
    const category = suggestCategory(tags);
    
    return {
      summary: summary.length ? summary : ['内容提取完成'],
      tags: tags.length ? tags : ['未分类'],
      category
    };
  }
}

// 简单 Readability 提取（基础版）
function simpleExtract(html) {
  // 移除脚本和样式
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '');
  
  // 提取正文
  const paragraphs = text.match(/<p[^>]*>([\s\S]*?)<\/p>/gi) || [];
  const content = paragraphs
    .map(p => p.replace(/<[^>]+>/g, '').trim())
    .filter(t => t.length > 20)
    .slice(0, 20);
  
  return content.join('\n\n');
}

// 检测网页类型
function detectType(url) {
  const urlStr = url.toLowerCase();
  
  if (urlStr.includes('github.com') || urlStr.includes('github.io')) {
    return 'github';
  }
  if (urlStr.includes('mp.weixin.qq.com')) {
    return 'weixin';
  }
  if (urlStr.includes('xiaohongshu.com')) {
    return 'xiaohongshu';
  }
  if (urlStr.includes('x.com') || urlStr.includes('twitter.com')) {
    return 'twitter';
  }
  if (urlStr.includes('medium.com') || urlStr.includes('dev.to')) {
    return 'blog';
  }
  return 'general';
}

// HTTP GET 请求
function httpGet(urlStr) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const protocol = url.protocol === 'https:' ? https : http;

    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
      },
      timeout: 30000
    };

    protocol.get(options, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpGet(res.headers.location).then(resolve).catch(reject);
      }

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject).setTimeout(options.timeout, () => {
      reject(new Error('请求超时'));
    });
  });
}

class Fetcher {
  constructor(config = {}) {
    this.config = config;
    this.tools = {
      // 预留：可集成专门的抓取工具
      // 例如：gitclone, playwright, mineru 等
    };
  }

  /**
   * 抓取网页
   * @param {string} url - 网页URL
   * @returns {Promise<Object>} - 抓取结果
   */
  async fetch(url) {
    const type = detectType(url);
    let result = {
      url,
      type,
      status: 'success',
      title: '',
      content: '',
      error: null
    };

    try {
      // 根据类型选择抓取策略
      switch (type) {
        case 'github':
          result = await this._fetchGitHub(url, result);
          break;
        case 'twitter':
          // Twitter/X 需要用浏览器抓取
          result = await this._fetchWithBrowser(url, result);
          break;
        case 'weixin':
        case 'xiaohongshu':
          // 尝试简单提取，失败再用浏览器
          try {
            result.content = await simpleExtract(await httpGet(url));
            result.title = this._extractTitle(result.content);
          } catch (e) {
            // 失败后尝试浏览器
            result = await this._fetchWithBrowser(url, result);
          }
          break;
        default:
          result.content = await simpleExtract(await httpGet(url));
          result.title = this._extractTitle(result.content);
      }

      // 提取失败
      if (!result.content || result.content.length < 100) {
        result.status = 'needs-review';
        result.error = '内容提取失败，需要手动处理';
      }

    } catch (err) {
      result.status = 'failed';
      result.error = err.message;
    }

    return result;
  }

  async _fetchGitHub(url, result) {
    // 提取 owner/repo
    const match = url.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    if (!match) {
      result.content = await simpleExtract(await httpGet(url));
      return result;
    }

    const [_, owner, repo] = match;
    const apiUrl = `https://api.github.com/repos/${owner}/${repo}`;

    const data = JSON.parse(await httpGet(apiUrl));
    result.title = data.name || '';
    result.content = data.description || '';
    result.stars = data.stargazers_count || 0;
    result.forks = data.forks_count || 0;
    result.language = data.language || '';
    result.updatedAt = data.updated_at || '';

    return result;
  }

  // 用浏览器抓取动态页面
  async _fetchWithBrowser(url, result) {
    const { spawn } = require('child_process');
    
    return new Promise((resolve) => {
      // 使用 OpenClaw 的 browser 工具通过 curl 调用
      const curlCmd = `curl -s "http://127.0.0.1:18800/snapshot?url=${encodeURIComponent(url)}" 2>/dev/null || echo ""`;
      
      // 尝试直接用 node fetch
      result.content = '';
      result.title = '';
      
      // 返回需要用浏览器抓取的标记
      result.needBrowser = true;
      result.error = '需要使用浏览器抓取';
      resolve(result);
    });
  }

  _extractTitle(content) {
    const match = content.match(/<title>([^<]+)<\/title>/i);
    return match ? match[1].trim() : '';
  }

  /**
   * 生成 AI 摘要
   * @param {string} content - 网页正文
   * @param {Object} llm - LLM 实例
   * @returns {Promise<Object>} - AI 生成结果
   */
  async generateSummary(content, llm) {
    const prompt = `请分析以下网页内容，生成结构化摘要。

要求：
1. 生成 3-5 点结构化摘要
2. 生成 3-5 个中文标签
3. 给出自动分类建议（如：阅读 / 产品 / AI / 生活 / 编程 / 其他）

返回严格 JSON 格式：
{"summary":["点1","点2","点3"],"tags":["标签1","标签2"],"category":"分类"}

内容如下：
${content.slice(0, 5000)}`;

    try {
      const response = await llm.complete(prompt);
      // 尝试解析 JSON
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('无法解析 LLM 响应');
    } catch (err) {
      return {
        summary: ['摘要生成失败: ' + err.message],
        tags: [],
        category: '未分类'
      };
    }
  }
}

module.exports = { Fetcher, DeepSeekLLM };
