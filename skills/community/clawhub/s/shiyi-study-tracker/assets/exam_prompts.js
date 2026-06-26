/**
 * exam_prompts.js
 * 各考试类型的背景知识，注入到识别 prompt 里提升标签精度。
 * 未命中时降级到 _generic。
 *
 * 新增考试：在 EXAM_PROMPTS 里加一条字符串，
 * EXAM_ALIASES 里加同义词映射即可。
 */

const EXAM_PROMPTS = {

  // ── 标化英语 ────────────────────────────────────────────────

  'GRE': `
GRE 分为 Verbal Reasoning、Quantitative Reasoning、Analytical Writing。
Verbal 题型：Text Completion（单空/双空/三空）、Sentence Equivalence、Reading Comprehension（单题/多题/段落）。
Quantitative 题型：Quantitative Comparison、Multiple Choice（单选/多选）、Numeric Entry。
标 knowledge_point 时请具体到：词汇类别（如"转折逻辑词"）、题型技巧（如"双空同向/反向逻辑"）或数学知识点（如"余数定理"）。`,

  'GMAT': `
GMAT 分为 Verbal（CR/RC/SC）、Quantitative（PS/DS）、Integrated Reasoning、AWA。
CR = Critical Reasoning，RC = Reading Comprehension，SC = Sentence Correction。
PS = Problem Solving，DS = Data Sufficiency。
标 knowledge_point 时请具体到题型内的逻辑类型或语法点（如"strengthen题型 反向假设"、"平行结构"）。`,

  'TOEFL': `
托福分为 Reading、Listening、Speaking、Writing。
Reading 题型：词汇题、指代题、句子简化、信息插入、修辞目的、推断题、表格题。
Listening 题型：主旨题、细节题、态度题、推断题、功能题。
标 knowledge_point 时请具体到题型技巧层面（如"词汇题同义替换规律"、"态度题语气词识别"）。`,

  '雅思': `
雅思分为 Listening、Reading、Writing、Speaking。
Reading 题型：True/False/Not Given、Matching Headings、Matching Information、
  Summary Completion、Multiple Choice、Short Answer、Sentence Completion。
Listening 题型：填空、选择、匹配、地图/示意图。
Writing：Task1（图表描述/书信）、Task2（议论文）。
标 knowledge_point 时请具体到题型技巧（如"T/F/NG 绝对词识别"、"Matching Headings 段落主旨定位"）。`,

  '四六级': `
大学英语四六级分为听力、阅读、翻译、写作。
阅读含：选词填空、长篇阅读（匹配）、仔细阅读（选择）。
听力含：短对话、长对话、讲座/报道。
标 knowledge_point 时请具体到词汇/语法/题型技巧层面。`,

  // ── 国内研究生/职业考试 ───────────────────────────────────

  '考研英语': `
考研英语（一/二）分为完形填空、阅读理解（A型精读/B型新题型）、翻译（英译汉）、写作（小作文+大作文）。
阅读A型题型：细节题、主旨题、推断题、词义题、态度题。
新题型（B型）：段落匹配、句子排序、小标题匹配。
标 knowledge_point 时请具体到：词汇（如"转折连词 however 后为重点"）、逻辑（如"主旨题排除绝对化选项"）。`,

  '考研数学': `
考研数学（一/二/三）分为高等数学、线性代数、概率统计（数三含概统）。
高数主要章节：极限与连续、导数与微分、积分（定积分/不定积分/多重积分）、微分方程、级数。
线代：行列式、矩阵、向量、线性方程组、特征值与特征向量。
概率统计：随机事件与概率、随机变量与分布、数字特征、统计推断。
标 knowledge_point 时请具体到知识点（如"换元积分法"、"行列式按行展开"）。`,

  '考研政治': `
考研政治分为马原（马克思主义原理）、毛中特（毛泽东思想和中国特色社会主义理论）、
史纲（中国近现代史纲要）、思修（思想道德与法治）、时政。
题型：选择题（单选/多选）、分析题（大题）。
标 knowledge_point 时请具体到知识点（如"矛盾的普遍性与特殊性"、"新民主主义革命的性质"）。`,

  '考研专业课': `
这是考研专业课题目，请根据图片内容自行判断学科方向。
标 section 为学科名（如"微观经济学"、"有机化学"）。
标 knowledge_point 时尽量具体到知识点层面。`,

  // ── 职业资格 ─────────────────────────────────────────────

  '注会': `
注册会计师考试共六门：会计、审计、财务成本管理、经济法、税法、公司战略与风险管理，
加综合阶段（职业能力综合测试）。
题型：单选、多选、判断、简答/计算/综合题。
标 knowledge_point 时请具体到知识点（如"长期股权投资成本法转权益法"、"实质性程序"）。`,

  '司法考试': `
法考（司法考试）分为客观题（卷一/卷二）和主观题。
涉及科目：民法、刑法、行政法、民事诉讼法、刑事诉讼法、商法、经济法、国际法、法理学、宪法、司法制度。
标 knowledge_point 时请具体到知识点（如"故意杀人罪与故意伤害罪致死的区别"）。`,

  '教师资格证': `
教师资格证分为综合素质、教育知识与能力、学科知识与教学能力。
题型：单选、材料分析、写作（综合素质）；单选、简答、材料分析（教育知识）；
  单选、简答、材料分析、教学设计（学科）。
标 knowledge_point 时请具体到知识点或能力点。`,

  // ── 公务员 ───────────────────────────────────────────────

  '国考': `
国家公务员考试行测含言语理解与表达、数量关系、判断推理、资料分析、常识判断。
判断推理含图形推理、定义判断、类比推理、逻辑判断。
申论含归纳概括、综合分析、提出对策、文章写作。
标 knowledge_point 时请具体到题型技巧（如"假言命题逆否推理"、"倍数增长率估算"）。`,

  '省考': `
省级公务员考试结构与国考类似，行测含言语/数量/判断/资料，另有申论。
部分省份有特色模块，请根据图片内容判断。
标 knowledge_point 时请具体到题型技巧层面。`,

  // ── 高中/大学 ────────────────────────────────────────────

  '高考': `
高考科目：语文、数学、英语为必考，另选考历史/地理/政治/物理/化学/生物（各省略有差异）。
请根据图片内容判断具体科目。
标 knowledge_point 时请具体到知识点（如"等差数列前n项和"、"氧化还原反应配平"）。`,

  '期末考试': `
这是大学或中学期末考试题目，请根据图片内容自行判断课程名称和知识模块。
标 section 为课程名（如"高等数学"、"大学物理"、"线性代数"）。
标 knowledge_point 时尽量具体到章节和知识点。`,

  // ── 通用降级 ────────────────────────────────────────────

  '_generic': `
这是一道考试题目，请根据图片内容自行判断考试类型和科目。
标 section 为科目大类，标 question_type 为题目类型，
标 knowledge_point 时请尽量具体，避免过于宽泛的标签（如"语法"、"计算"）。`,
};

// 同义词映射，用户输入的各种说法都能命中
const EXAM_ALIASES = {
  'GRE':        ['gre', 'GRE', '研究生入学考试'],
  'GMAT':       ['gmat', 'GMAT'],
  'TOEFL':      ['toefl', 'TOEFL', '托福'],
  '雅思':       ['雅思', 'ielts', 'IELTS'],
  '四六级':     ['四级', '六级', '英语四级', '英语六级', 'CET4', 'CET6', 'cet'],
  '考研英语':   ['考研英语', '考研 英语'],
  '考研数学':   ['考研数学', '考研 数学', '数学一', '数学二', '数学三'],
  '考研政治':   ['考研政治', '考研 政治', '政治'],
  '考研专业课': ['考研专业课', '专业课'],
  '注会':       ['注会', 'cpa', 'CPA', '注册会计师'],
  '司法考试':   ['司法', '法考', '司法考试', '律师资格'],
  '教师资格证': ['教资', '教师资格', '教师资格证'],
  '国考':       ['国考', '国家公务员', '国家公务员考试'],
  '省考':       ['省考', '省级公务员', '公务员'],
  '高考':       ['高考', '联考'],
  '期末考试':   ['期末', '期末考', '期中', '期中考', '期末考试'],
};

/**
 * 根据用户输入的考试名称，找到最匹配的 prompt key。
 * @param {string} input
 * @returns {{ key: string, prompt: string }}
 */
function resolveExam(input) {
  if (!input) return { key: '_generic', prompt: EXAM_PROMPTS['_generic'] };

  const lower = input.toLowerCase().trim();

  // 精确匹配
  if (EXAM_PROMPTS[input]) return { key: input, prompt: EXAM_PROMPTS[input] };

  // 别名匹配
  for (const [key, aliases] of Object.entries(EXAM_ALIASES)) {
    if (aliases.some(a => lower.includes(a.toLowerCase()))) {
      return { key, prompt: EXAM_PROMPTS[key] };
    }
  }

  // 模糊匹配（key 包含 input 或 input 包含 key）
  for (const key of Object.keys(EXAM_PROMPTS)) {
    if (key === '_generic') continue;
    if (lower.includes(key.toLowerCase()) || key.toLowerCase().includes(lower)) {
      return { key, prompt: EXAM_PROMPTS[key] };
    }
  }

  return { key: '_generic', prompt: EXAM_PROMPTS['_generic'] };
}

/**
 * 列出所有已预置的考试名称（用于 onboarding 展示）。
 */
function listSupportedExams() {
  return Object.keys(EXAM_PROMPTS).filter(k => k !== '_generic');
}

module.exports = { resolveExam, listSupportedExams, EXAM_PROMPTS };
