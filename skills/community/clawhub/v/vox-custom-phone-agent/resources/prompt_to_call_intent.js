'use strict';

const { extractPhone, normalizePhone } = require('./phone_validator');
const { parseVoiceType } = require('./voice_type_selector');

const SCENARIOS = [
  { pattern: /会议|会改|开会/, scenario: '会议通知', role: '会议通知助理', style: ['正式', '简洁', '清晰'] },
  { pattern: /售后|维修|满意|回访|投诉/, scenario: '售后回访', role: '售后客服', style: ['耐心', '真诚', '礼貌'] },
  { pattern: /课程|试听|体验课|教育|编程课|培训/, scenario: '课程邀约', role: '课程顾问', style: ['专业', '温和', '克制'] },
  { pattern: /面试|招聘|简历|候选人/, scenario: '面试通知', role: '招聘助理', style: ['正式', '友好', '清晰'] },
  { pattern: /商务|合作|企业|项目|客户/, scenario: '商务沟通', role: '商务经理', style: ['专业', '稳重', '高效'] },
  { pattern: /聊天|聊聊|陪聊|陪伴|关怀|问候|近况|闲聊|生活状态/, scenario: '聊天陪伴', role: '关怀助手', style: ['温和', '自然', '尊重'] },
  { pattern: /活动|报名|签到|参会|讲座/, scenario: '活动提醒', role: '活动通知助理', style: ['清晰', '友好', '简洁'] },
  { pattern: /体检|用药|服药|复诊|健康|老人|长辈/, scenario: '健康提醒', role: '健康提醒助手', style: ['温和', '清楚', '耐心'] }
];

function inferScenario(text) {
  return SCENARIOS.find((item) => item.pattern.test(text)) || null;
}

function extractRole(text) {
  const roleWithSuffix = text.match(/(?:作为|以|扮演|你是|我是)([^，。,.；;\n]{1,24}?(?:助理|顾问|客服|经理|专员|老师|医生|护士|同事|负责人))/);
  if (roleWithSuffix) return roleWithSuffix[1].trim();

  const patterns = [
    /作为([^，。,.；;]{2,16})/,
    /以([^，。,.；;]{2,16})身份/,
    /扮演([^，。,.；;]{2,16})/,
    /你是([^，。,.；;]{2,16})/,
    /我是([^，。,.；;]{2,16})/
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) return cleanFragment(match[1]);
  }
  return '';
}

function extractGoal(text) {
  const explicitGoal = text.match(/(?:目标是|目的是|希望)([^，。；;\n]+)/);
  if (explicitGoal) return cleanFragment(explicitGoal[1]);

  for (const verb of ['通知', '提醒', '告诉', '确认']) {
    const index = text.lastIndexOf(verb);
    if (index >= 0) {
      const value = text.slice(index + verb.length).split(/[，。；;\n]/)[0];
      if (value.trim().length >= 3) return cleanFragment(`${verb}${value}`);
    }
  }

  const patterns = [
    /目标是([^，。；;\n]+)/,
    /目的是([^，。；;\n]+)/,
    /希望([^，。；;\n]+)/,
    /确认([^，。；;\n]+)/,
    /通知([^，。；;\n]+)/,
    /提醒([^，。；;\n]+)/,
    /告诉([^，。；;\n]+)/
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      const prefix = pattern.source.startsWith('确认') ? '确认' : pattern.source.startsWith('通知') ? '通知' : pattern.source.startsWith('提醒') ? '提醒' : pattern.source.startsWith('告诉') ? '告诉' : '';
      return cleanFragment(`${prefix}${match[1]}`);
    }
  }
  const withoutPhone = sanitizeGoalText(text);
  if (/打电话|电话/.test(withoutPhone) && withoutPhone.length >= 10) {
    return cleanFragment(withoutPhone.replace(/帮我|请|给.*?打电话|打个电话|打电话/g, ''));
  }
  return '';
}

function sanitizeGoalText(text) {
  return String(text || '')
    .replace(/(?:\+?86[-\s]?)?1[3-9]\d[-\s]?\d{4}[-\s]?\d{4}/g, '')
    .replace(/^(先)?试用[。,.，；;]?/, '')
    .replace(/使用(?:知愈|安辰|景珩|知言|星苒|商务男声|女声通知|[0-4]号?)音色?[。,.，；;]?/g, '')
    .replace(/作为([^，。,.；;\n]{1,24}?(?:助理|顾问|客服|经理|专员|老师|医生|护士|同事|负责人))/g, '')
    .replace(/给\s*打电话/g, '打电话')
    .trim();
}

function extractTone(text, scenarioDefault = []) {
  const tones = new Set(scenarioDefault);
  const candidates = ['正式', '简洁', '清晰', '专业', '温和', '克制', '热情', '亲切', '耐心', '真诚', '礼貌', '稳重', '高效', '友好'];
  for (const tone of candidates) {
    if (text.includes(tone)) tones.add(tone);
  }
  if (/不要强推|别强推|不强推|不强行推销/.test(text)) tones.add('克制');
  return Array.from(tones).slice(0, 4);
}

function extractConstraint(text) {
  const constraints = [];
  if (/不要强推|别强推|不强推|不强行推销/.test(text)) constraints.push('不要强行推销');
  if (/拒绝.*结束|没兴趣.*结束|不方便.*结束/.test(text)) constraints.push('对方拒绝或不方便时礼貌结束');
  if (/不要.*承诺|不能.*承诺/.test(text)) constraints.push('不得承诺未授权事项');
  if (/不要.*隐私|不问.*隐私/.test(text)) constraints.push('不得索要敏感隐私信息');
  return constraints.join('；');
}

function extractUseMode(text) {
  const value = String(text || '');
  if (/正式|注册|企业账号|自己的凭证|专属凭证|生产/.test(value)) return 'formal';
  if (/试用|体验|先试|推广/.test(value)) return 'trial';
  if (/\btrial\b/i.test(value)) return 'trial';
  if (/\bformal\b|\bproduction\b/i.test(value)) return 'formal';
  return '';
}

function extractWorkflow(text) {
  const clauses = splitClauses(text)
    .map(normalizeWorkflowClause)
    .filter(Boolean);
  const flowClauses = clauses.filter((clause) => /^(先|然后|再|最后|如果|若|如|当|遇到|对方|客户|用户|结束|询问|确认|追问|说明|感谢|礼貌|记录|安排)/.test(clause));
  if (flowClauses.length >= 2) return flowClauses.join(' -> ');
  if (/如果|若|如.*则|先.*再|满意|不满意|方便|不方便/.test(text)) {
    return clauses.slice(0, 8).join(' -> ');
  }
  return '';
}

function extractMustSay(text) {
  const matches = [];
  for (const pattern of [/通知对方[:：]?([^。；;\n]+)/g, /告诉对方[:：]?([^。；;\n]+)/g, /提醒对方[:：]?([^。；;\n]+)/g]) {
    for (const match of text.matchAll(pattern)) matches.push(match[1].trim());
  }
  return Array.from(new Set(matches)).join('；');
}

function splitClauses(text) {
  return String(text || '')
    .replace(/\s+/g, '')
    .split(/[。；;\n]+|(?=如果)|(?=若)|(?=如对方)|(?=当对方)|(?=先)|(?=然后)|(?=再)|(?=最后)/)
    .map((part) => part.replace(/^[，,、]+|[，,、]+$/g, '').trim())
    .filter((part) => part.length >= 3);
}

function normalizeWorkflowClause(clause) {
  return clause
    .replace(/^给(?:\+?86[-\s]?)?1[3-9]\d[-\s]?\d{4}[-\s]?\d{4}打电话，?/, '')
    .replace(/^帮我/, '')
    .replace(/使用(?:知愈|安辰|景珩|知言|星苒|[0-4]号?)音色?$/, '')
    .replace(/语气(?:要)?[^。；;\n]+$/, '')
    .trim();
}

function cleanFragment(value) {
  let text = String(value || '')
    .replace(/^(一下|一下子|这通电话|这个电话|客户|对方|他|她|用户)/, '')
    .replace(/^[，。,.；;\s]+/g, '')
    .replace(/[，。,.；;\s]+$/g, '')
    .trim();
  text = text.split(/(?=介绍|通知|提醒|告诉|确认|沟通|联系|邀约|邀请|目标是|目的是|希望)/)[0].trim() || text;
  return text
    .replace(/^[，。,.；;\s]+/g, '')
    .replace(/[，。,.；;\s]+$/g, '')
    .trim();
}

function mergeIntent(base = {}, next = {}) {
  const merged = { ...base, ...next };
  if (!merged.rawPrompt) merged.rawPrompt = [base.rawPrompt, next.rawPrompt].filter(Boolean).join('\n');
  if (!merged.callee && next.rawPrompt) merged.callee = extractPhone(next.rawPrompt);
  if (merged.callee) merged.callee = normalizePhone(merged.callee);
  return merged;
}

function parsePromptToIntent(prompt, previousIntent = {}) {
  const rawPrompt = String(prompt || '').trim();
  const scenario = inferScenario(rawPrompt);
  const extracted = {
    rawPrompt,
    callee: extractPhone(rawPrompt),
    scenario: scenario ? scenario.scenario : '',
    role: extractRole(rawPrompt) || (scenario ? scenario.role : ''),
    goal: extractGoal(rawPrompt),
    communicationStyle: extractTone(rawPrompt, scenario ? scenario.style : []),
    constraint: extractConstraint(rawPrompt),
    workflow: extractWorkflow(rawPrompt),
    mustSay: extractMustSay(rawPrompt),
    useMode: extractUseMode(rawPrompt),
    background: scenario ? scenario.scenario : '',
    voiceType: parseVoiceType(rawPrompt)
  };
  return mergeIntent(previousIntent, removeEmpty(extracted));
}

function removeEmpty(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([, value]) => {
    if (Array.isArray(value)) return value.length > 0;
    return value !== undefined && value !== null && value !== '';
  }));
}

module.exports = {
  parsePromptToIntent,
  mergeIntent,
  inferScenario,
  extractWorkflow,
  extractUseMode
};
