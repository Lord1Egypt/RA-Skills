/**
 * Entity Extraction - 从记忆文本中提取实体
 * 支持：PERSON, ORGANIZATION, PROJECT, TOPIC, TOOL, LOCATION, DATE, EVENT
 *
 * @module graph/entity
 */

import { createHash } from 'crypto';
import { config } from '../config.js';

// 实体类型定义
export const ENTITY_TYPES = {
  PERSON: 'person',
  ORGANIZATION: 'organization',
  PROJECT: 'project',
  TOPIC: 'topic',
  TOOL: 'tool',
  LOCATION: 'location',
  DATE: 'date',
  EVENT: 'event',
};

// 生成实体唯一 ID: ent_${hash(name+type).slice(0,8)}
export function generateEntityId(name, type) {
  const hash = createHash('md5').update(`${name}::${type}`).digest('hex');
  return `ent_${hash.slice(0, 8)}`;
}

/**
 * 规则预提取（正则）：@人名、#项目、##主题、日期、组织名
 * @param {string} text
 * @returns {Array<{ name: string, type: string, method: 'rule' }>}
 */
export function extractEntitiesRuleBased(text) {
  /** @type {Array<{ name: string, type: string, method: string }>} */
  const entities = [];

  // @xxx → person
  const atMentions = text.match(/@([^\s@,，、。！？!?,.\n]+)/g) || [];
  for (const m of atMentions) {
    const name = m.slice(1);
    if (name.length > 0 && name.length < 50) {
      entities.push({ name, type: ENTITY_TYPES.PERSON, method: 'rule' });
    }
  }

  // #xxx → topic 或 project（通过上下文判断）
  const hashtags = text.match(/#([^\s#,，、。！？!?,.\n]+)/g) || [];
  for (const m of hashtags) {
    const name = m.slice(1);
    if (name.length > 0 && name.length < 50) {
      const lower = name.toLowerCase();
      const type = lower.includes('project') || lower.includes('项目') || lower.includes('任务')
        ? ENTITY_TYPES.PROJECT
        : ENTITY_TYPES.TOPIC;
      entities.push({ name, type, method: 'rule' });
    }
  }

  // 中文关键词识别：飞书、钉钉、OpenClaw、MetaGPT 等（用已有 toolKeywords 更安全）
  // 中文姓名用 @ 提及更可靠，不再用正则猜测

  // 组织/公司名：xxx有限公司、xxx实验室、xxx公司、xxx团队、xxx部门
  const orgPatterns = [
    /([^\s]{2,20})(?:有限公司|股份有限公司|Ltd\.?|Inc\.?|Corp\.?|实验室|研究院|研究所|团队|部门|公司|机构|组织)/g,
  ];
  for (const pat of orgPatterns) {
    let match;
    pat.lastIndex = 0;
    while ((match = pat.exec(text)) !== null) {
      const name = match[1].trim();
      if (name.length > 1) {
        entities.push({ name, type: ENTITY_TYPES.ORGANIZATION, method: 'rule' });
      }
    }
  }

  // 日期：YYYY年MM月DD日、YYYY-MM-DD、MM/DD/YYYY、MM月DD日、今天/明天/昨天
  const datePatterns = [
    /(\d{4}年\d{1,2}月\d{1,2}日)/g,
    /(\d{4}-\d{2}-\d{2})/g,
    /(\d{1,2}\/\d{1,2}\/\d{4})/g,
    /(\d{1,2}月\d{1,2}日)/g,
    /(今天|明天|昨天|后天|前天|大前天|大后天)/g,
    /(周一|周二|周三|周四|周五|周六|周日|星期一|星期二|星期三|星期四|星期五|星期六|星期日)/g,
  ];
  for (const pat of datePatterns) {
    let match;
    pat.lastIndex = 0;
    while ((match = pat.exec(text)) !== null) {
      const name = match[1];
      entities.push({ name, type: ENTITY_TYPES.DATE, method: 'rule' });
    }
  }

  // 工具类关键词
  const toolKeywords = [
    '飞书', '钉钉', 'Slack', '微信', 'QQ', '企业微信', 'Teams', 'Telegram',
    'VSCode', 'Vim', 'Neovim', 'Emacs', 'Sublime', 'JetBrains',
    'GitHub', 'GitLab', 'Gitee', 'Jira', 'Notion', 'Figma', 'Sketch',
    'Docker', 'Kubernetes', 'k8s', 'Nginx', 'Redis', 'MongoDB', 'MySQL', 'PostgreSQL',
    'Python', 'JavaScript', 'TypeScript', 'Go', 'Rust', 'Java', 'C++', 'Ruby',
    'Ollama', 'OpenAI', 'Claude', 'DeepSeek', 'Qwen', 'Kimi', 'ChatGPT', 'Cursor',
    'npm', 'yarn', 'pnpm', 'pip', 'conda', 'brew',
  ];
  for (const tool of toolKeywords) {
    const escaped = tool.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`\\b${escaped}\\b`, 'gi');
    let match;
    while ((match = regex.exec(text)) !== null) {
      entities.push({ name: tool, type: ENTITY_TYPES.TOOL, method: 'rule' });
    }
  }

  // 事件关键词
  const eventKeywords = [
    '会议', 'meeting', '讨论', '评审', '面试', '发布会', '发布', '上线', '版本发布',
    'debug', '重构', '迁移', '部署', '培训', '周会', '例会', '头脑风暴',
  ];
  for (const kw of eventKeywords) {
    const escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`\\b${escaped}\\b`, 'gi');
    let match;
    while ((match = regex.exec(text)) !== null) {
      entities.push({ name: kw, type: ENTITY_TYPES.EVENT, method: 'rule' });
    }
  }

  return entities;
}

/**
 * 调用 LLM 二次提取（更精准）
 * @param {string} text
 * @param {object} context
 * @returns {Promise<Array<{ name: string, type: string, method: 'llm' }>>}
 */
export async function extractEntitiesLLM(text, context = {}) {
  const providers = config.llmProviders || [];
  if (providers.length === 0) {
    return [];
  }

  const provider = providers[0];
  const url = `${provider.baseURL}/api/generate`;

  const prompt = `从以下文本中提取所有实体（人物、组织、项目、主题、工具、地点、日期、事件），返回 JSON 数组格式。

要求：
- 每条实体包含：name（名称）、type（类型，可选值：person/organization/project/topic/tool/location/date/event）
- 只返回你知道确实存在的实体，不要猜测
- 如果不确定类型，优先使用最具体的类型
- 返回纯 JSON 数组，不要其他文字

文本：
${text.slice(0, 2000)}

返回格式示例：
[
  {"name": "刘总", "type": "person"},
  {"name": "OpenClaw", "type": "project"},
  {"name": "飞书", "type": "tool"}
]`;

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: provider.model,
        prompt,
        stream: false,
        options: { temperature: 0.1 },
      }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!res.ok) return [];

    const data = await res.json();
    const response = data.response || data.output || '';

    // Try to extract JSON from response
    let jsonStr = response.trim();
    const jsonMatch = jsonStr.match(/\[[\s\S]*\]/);
    if (jsonMatch) {
      jsonStr = jsonMatch[0];
    }

    const extracted = JSON.parse(jsonStr);
    if (!Array.isArray(extracted)) return [];

    return extracted
      .filter(e => e.name && e.type && Object.values(ENTITY_TYPES).includes(e.type))
      .map(e => ({ name: e.name.trim(), type: e.type, method: 'llm' }));
  } catch (err) {
    // Fallback silently
    return [];
  }
}

/**
 * 规则 + LLM 混合提取
 * @param {string} text
 * @param {object} options
 * @returns {Promise<Array<{ id: string, name: string, type: string, method: string }>>}
 */
export async function extractEntities(text, options = {}) {
  const { useLLM = true } = options;

  // 1. 规则预提取
  const ruleEntities = extractEntitiesRuleBased(text);

  // 2. LLM 二次提取（可选）
  let llmEntities = [];
  if (useLLM && text.length >= 10) {
    llmEntities = await extractEntitiesLLM(text, options);
  }

  // 3. 合并去重
  const merged = [...ruleEntities, ...llmEntities];
  const deduped = mergeDuplicateEntities(merged);

  // 4. 添加 ID
  return deduped.map(e => ({
    id: generateEntityId(e.name, e.type),
    name: e.name,
    type: e.type,
    method: e.method,
  }));
}

/**
 * 实体消歧（同义实体合并）
 * 基于精确匹配 + 类型相同合并
 * @param {Array<{ name: string, type: string, method?: string }>} entities
 * @returns {Array<{ name: string, type: string, method: string }>}
 */
export function mergeDuplicateEntities(entities) {
  /** @type {Map<string, { name: string, type: string, method: string, count: number }>} */
  const map = new Map();

  for (const e of entities) {
    // Normalize: trim + lowercase for comparison
    const key = `${e.name.trim()}::${e.type}`;
    if (map.has(key)) {
      map.get(key).count++;
    } else {
      map.set(key, { name: e.name.trim(), type: e.type, method: e.method || 'rule', count: 1 });
    }
  }

  return Array.from(map.values()).map(({ name, type, method, count }) => ({
    name,
    type,
    method,
    count,
  }));
}
