'use strict';

const PLAYBOOKS = [
  {
    id: 'output-standard',
    name: '输出呈现标准',
    intent: '让输出先判型渲染为可复制格式，再去除 AI 味。',
    keywords: ['输出', '呈现', '渲染', '排版', '可复制', 'AI味', 'AI 味', '润色', '文档', '报告'],
    skills: [
      { slug: 'yotta-present', order: 1, role: '判断内容形态并渲染为可复制 Markdown / 纯文本。' },
      { slug: 'yotta-humanize', order: 2, role: '检测中文 AI 腔，并按用户原意做确定性改写。' },
    ],
  },
  {
    id: 'long-lived-agent',
    name: '长生命周期智能体',
    intent: '让智能体跨会话恢复状态、记忆、经验与历史。',
    keywords: ['长期', '跨会话', '忘了我', '别忘了我', '记忆', '上下文', '状态', '历史'],
    skills: [
      { slug: 'yotta-workflow', order: 1, role: '开工读取项目状态，会话结束更新状态并留下次接续记录。' },
      { slug: 'yotta-memory', order: 2, role: '按权限边界保存与恢复跨会话记忆。' },
      { slug: 'yotta-learn', order: 3, role: '沉淀错误、纠正与洞见，供后续会话复用。' },
      { slug: 'yotta-logs', order: 4, role: '按需检索历史会话与日志记录。' },
    ],
  },
  {
    id: 'delivery-quality-gate',
    name: '交付质量门',
    intent: '交付前做防敷衍、代码质量与发布守门检查。',
    keywords: ['检查', '代码', '质量', '别糊弄', '敷衍', '评审', '发布', '守门', '交付'],
    skills: [
      { slug: 'yotta-anti-shallow', order: 1, role: '强制先分析、再执行、后自检，防止表面化交付。' },
      { slug: 'yotta-code-quality', order: 2, role: '按十二类腐化风险做结对式代码质量评审。' },
      { slug: 'yotta-publish-guard', order: 3, role: '发布前校验版本、发布件与分发通道一致性。' },
    ],
  },
  {
    id: 'preinstall-security-gate',
    name: '装前安全门',
    intent: '安装其他来源技能、插件或 MCP 前做安全判定。',
    keywords: ['安装', '装前', '其他来源', '技能', '插件', 'MCP', '安全扫描'],
    skills: [
      { slug: 'yotta-verify', order: 1, role: '执行确定性装前扫描并给出安全判定。' },
      { slug: 'yotta-vetter', order: 2, role: '按四阶段协议审查来源、代码、权限与风险。' },
      { slug: 'yotta-security-audit', order: 3, role: '做深度静态检测与安全基线兜底。' },
    ],
  },
  {
    id: 'skill-build-publish',
    name: '造技能 / 发版',
    intent: '创建合规技能包，并在发布前完成守门检查。',
    keywords: ['造一个', '新 skill', '新技能', '脚手架', '发版', '发布技能', '技能包'],
    skills: [
      { slug: 'yotta-skill-creator', order: 1, role: '生成符合规范的技能目录与发布件结构。' },
      { slug: 'yotta-publish-guard', order: 2, role: '校验版本四件、发布件与分发通道。' },
    ],
  },
  {
    id: 'security-incident-response',
    name: '安全事件响应',
    intent: '从日志、情报、样本、密钥、供应链与资产侦察看清事件链路。',
    keywords: ['日志', '攻击', '安全事件', '入侵', 'IOC', '威胁情报', '样本', '密钥泄露', '供应链', '资产', '侦察'],
    skills: [
      { slug: 'yotta-logwatch', order: 1, role: '分析安全日志并识别攻击链与告警聚合。' },
      { slug: 'yotta-intel', order: 2, role: '提取、去武器化并规范化威胁情报 IOC。' },
      { slug: 'yotta-triage', order: 3, role: '对可疑样本做静态初筛。' },
      { slug: 'yotta-secret', order: 4, role: '扫描密钥与凭据泄露源头。' },
      { slug: 'yotta-chain', order: 5, role: '校验依赖供应链与 lockfile 一致性。' },
      { slug: 'yotta-recon', order: 6, role: '在授权范围内做端口、服务与版本指纹侦察。' },
    ],
  },
  {
    id: 'entry-install',
    name: '入口 + 安装',
    intent: '需求方向不明确时先澄清意图，再按需安装合适技能。',
    keywords: ['不知道用哪个', '需求模糊', '该用哪个', '怎么说', '技能该用哪个'],
    skills: [
      { slug: 'yotta-prompt', order: 1, role: '澄清需求意图并串联到合适的技能方向。' },
      { slug: 'yotta-skills', order: 2, role: '按场景组合安装所需技能，不默认安装全家。' },
    ],
  },
];

const OTHER_SKILLS_NOTE = '其他已装技能仅作并列候选提示：机械匹配 frontmatter description，未做语义推理、未读取全文指令、未自动调用；数据不出本机。';
const OTHER_SKILL_NOTE = '非元阁家族技能：仅按 frontmatter description 本地机械匹配；不读取全文指令、不自动调用；使用/安装前请先做装前安全扫描。';
const EN_STOPWORDS = new Set([
  'a', 'an', 'the', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with', 'from',
  'this', 'that', 'is', 'are', 'was', 'were', 'be', 'been', 'your', 'you', 'our',
  'we', 'it', 'at', 'by', 'as', 'not', 'no', 'so', 'do', 'does',
]);

/** 元阁家族 slug 集合：playbook 引用 + 已知不入 playbook 的元技能（如 yotta-chart）。 */
function defaultYottaSlugs() {
  const set = new Set(['yotta-chart']);
  for (const playbook of PLAYBOOKS) {
    for (const skill of playbook.skills) set.add(skill.slug);
  }
  return Array.from(set);
}

/** 英文词项：≥3 字母的单词，过滤停用词（保留出现顺序、去重）。 */
function enTokens(text) {
  const tokens = [];
  const seen = new Set();
  for (const m of String(text || '').toLowerCase().match(/[a-z][a-z0-9]{2,}/g) || []) {
    if (EN_STOPWORDS.has(m) || seen.has(m)) continue;
    seen.add(m);
    tokens.push(m);
  }
  return tokens;
}

/** 中文词项：CJK 连续片段内相邻两字 bigram（零依赖确定性分词）。 */
function cjkBigrams(text) {
  const bigrams = [];
  const seen = new Set();
  for (const m of String(text || '').match(/[\u4e00-\u9fff]+/g) || []) {
    for (let i = 0; i < m.length - 1; i++) {
      const g = m.slice(i, i + 2);
      if (seen.has(g)) continue;
      seen.add(g);
      bigrams.push(g);
    }
  }
  return bigrams;
}

/** 需求与候选文本的词项匹配：英文 token + 中文 bigram 交集，按需求侧出现顺序输出。 */
function scoreOtherSkill(request, record) {
  const candidateText = [record.description, record.slug].filter(Boolean).join(' ');
  const reqTokens = enTokens(request);
  const reqBigrams = cjkBigrams(request);
  const candTokens = new Set(enTokens(candidateText));
  const candBigrams = new Set(cjkBigrams(candidateText));
  const matched = [];
  for (const item of reqTokens) if (candTokens.has(item)) matched.push(item);
  for (const item of reqBigrams) if (candBigrams.has(item)) matched.push(item);
  return { score: matched.length, matched_terms: matched };
}

function normalizeText(text) {
  return String(text || '').toLowerCase().replace(/\s+/g, '');
}

function scorePlaybook(request, playbook) {
  const text = normalizeText(request);
  const matchedKeywords = [];
  let score = 0;
  for (const keyword of playbook.keywords) {
    if (text.includes(normalizeText(keyword))) {
      matchedKeywords.push(keyword);
      score += normalizeText(keyword).length >= 3 ? 2 : 1;
    }
  }
  return { score, matchedKeywords };
}

function routeRequest(request, options) {
  const registry = (options && options.registry) || { skills: {} };
  const installed = registry.skills || {};
  const yottaSlugs = new Set((options && options.yottaSlugs) || defaultYottaSlugs());
  const otherSkillsTopN = (options && options.otherSkillsTopN) || 3;
  const ranked = PLAYBOOKS
    .map((playbook) => ({ playbook, ...scorePlaybook(request, playbook) }))
    .sort((a, b) => b.score - a.score || a.playbook.id.localeCompare(b.playbook.id));
  const best = ranked[0];
  const runnerUp = ranked[1];
  const fallback = !best || best.score === 0;
  const playbook = fallback
    ? PLAYBOOKS.find((item) => item.id === 'entry-install')
    : best.playbook;
  const matchedKeywords = fallback ? [] : best.matchedKeywords;
  const margin = fallback ? 0 : best.score - (runnerUp ? runnerUp.score : 0);
  const confidence = !fallback && best.score >= 3 && margin >= 1
    ? 'high'
    : (!fallback && best.score >= 1 ? 'medium' : 'low');

  const skills = playbook.skills.map((skill) => {
    const record = installed[skill.slug];
    const isInstalled = Boolean(record && record.status !== 'gone');
    return {
      ...skill,
      installed: isInstalled,
      version: isInstalled ? record.version || '' : '',
      sources: isInstalled ? record.sources || [] : [],
      variants: isInstalled && Array.isArray(record.variants) ? record.variants : [],
      conflicts: isInstalled && Array.isArray(record.conflicts) ? record.conflicts : [],
    };
  });
  const missingSkills = skills
    .filter((skill) => !skill.installed)
    .map((skill) => ({ slug: skill.slug, scan_required: true }));
  const installCommand = missingSkills.length
    ? 'npx -y @yottameta/yotta-skills install '
      + missingSkills.map((skill) => skill.slug).join(' ')
      + ' --dir <skills-dir>'
    : null;

  const otherCandidates = Object.values(installed)
    .filter((record) => record && record.status !== 'gone' && !yottaSlugs.has(record.slug))
    .map((record) => ({ record, ...scoreOtherSkill(request, record) }))
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.record.slug.localeCompare(b.record.slug))
    .slice(0, otherSkillsTopN)
    .map(({ record, score, matched_terms }) => ({
      slug: record.slug,
      version: record.version || '',
      sources: record.sources || [],
      description: record.description || '',
      score,
      matched_terms,
      scan_status: 'not_scanned',
      note: OTHER_SKILL_NOTE,
    }));

  return {
    request,
    playbook: {
      id: playbook.id,
      name: playbook.name,
      intent: playbook.intent,
    },
    confidence,
    matched_keywords: matchedKeywords,
    skills,
    missing_skills: missingSkills,
    install_command: installCommand,
    auto_install: false,
    application_mode: {
      default: 'explicit',
      options: ['explicit', 'scene-auto'],
      note: '默认用户显式调用；切换为按场景自动调用需要用户确认。',
    },
    disclaimer: '路由建议不保证完全正确；关键动作应由用户确认，数据不出本机。',
    other_skill_candidates: otherCandidates,
    other_skills_note: OTHER_SKILLS_NOTE,
  };
}

module.exports = { PLAYBOOKS, defaultYottaSlugs, routeRequest };
