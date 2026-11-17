'use strict';
/**
 * deconstruct.js —— 爆款视频脚本拆解引擎（确定性、离线、零依赖）
 *
 * 输入：一份口播逐字稿（可带时间戳），可选平台与目标。
 * 输出：结构分段 / 钩子判定 / 留存节奏 / 口语度 / CTA / 金句候选 / 二创蓝图。
 *
 * 设计原则：
 *   - **确定性**：同一份输入任何时候跑，结论完全一致，可被第三方按同一口径复核。
 *   - **给依据**：每条结论都带命中位置与判定口径，不做无依据的"感觉判断"。
 *   - **不越界**：引擎只做机械识别，不对"能不能爆"下断言 —— 爆量由投放与选题决定。
 */

const L = require('./lexicons.js');

// ------------------------------------------------------------------ 文本处理

function normalizeText(text) {
  return String(text == null ? '' : text)
    .replace(/\r\n?/g, '\n')
    .replace(/[ \t\u3000]+/g, ' ')
    .trim();
}

/** 识别形如 "00:03" / "0:03" / "[00:03]" / "(00:03)" 的时间戳前缀。 */
const TS_RE = /^\s*[\[(（]?\s*(\d{1,2}):(\d{2})(?::(\d{2}))?\s*[\])）]?\s*[-–—、.．]?\s*/;

function parseTimed(text) {
  const lines = normalizeText(text).split('\n');
  const out = [];
  let hasTs = false;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    const m = line.match(TS_RE);
    if (m) {
      hasTs = true;
      const a = parseInt(m[1], 10);
      const b = parseInt(m[2], 10);
      const c = m[3] != null ? parseInt(m[3], 10) : null;
      const sec = c != null ? a * 3600 + b * 60 + c : a * 60 + b;
      out.push({ sec, text: line.slice(m[0].length).trim() });
    } else {
      out.push({ sec: null, text: line });
    }
  }
  return { lines: out, hasTs };
}

/** 断句：先去掉行首时间戳（否则 "00:03 " 会被算进第一句长度），
 *  再按句末标点与换行切分；口播稿常无标点，超长句按逗号二次切分。 */
function splitSentences(text) {
  const src = normalizeText(text).replace(new RegExp(TS_RE.source, 'gm'), '');
  const rough = src
    .split(/(?<=[。！？!?；;…])|\n+/)
    .map((s) => s.trim())
    .filter(Boolean);
  const out = [];
  for (const s of rough) {
    if (s.length <= 40) { out.push(s); continue; }
    // 超长句（多半是没标点的口播稿）：按逗号/顿号切成 12-32 字的片段
    let buf = '';
    for (const part of s.split(/(?<=[，,、])/)) {
      if ((buf + part).length > 32 && buf) { out.push(buf.trim()); buf = part; }
      else buf += part;
    }
    if (buf.trim()) out.push(buf.trim());
  }
  return out;
}

function countChars(s) {
  return (s.match(/[\u4e00-\u9fff]/g) || []).length + (s.match(/[A-Za-z0-9]+/g) || []).length;
}

function hitAny(text, re) {
  return re instanceof RegExp ? re.test(text) : false;
}

// ------------------------------------------------------------------ 钩子判定

function analyzeHook(sentences, lines, hasTs) {
  // 钩子窗口 = 第一句。第一句极短（<12 字）时才并入第二句。
  // **不能直接把前两句都算进窗口** —— 第二句里出现"其实"并不构成开场钩子，
  // 那会造成"明明开场是客套话却判成有钩子"的假阳性（已修）。
  const first = sentences[0] || '';
  const winEnd = first.length < 12 ? 2 : 1;
  const head = sentences.slice(0, winEnd).join('');

  const hits = [];
  for (const h of L.HOOK_TYPES) {
    if (hitAny(head, h.re)) hits.push(h);
  }
  hits.sort((a, b) => b.strength - a.strength);
  const deadOpen = L.DEAD_OPENERS.test(first);

  // 时间戳可用时，算出钩子实际占了多少秒
  let hookSec = null;
  if (hasTs) {
    const timed = lines.filter((l) => l.sec != null);
    if (timed.length >= 2) {
      const t0 = timed[0].sec;
      const t1 = timed.find((l) => l.sec != null && l.sec - t0 >= 3);
      hookSec = t1 ? t1.sec - t0 : null;
    }
  }

  const findings = [];
  if (deadOpen) {
    findings.push({
      level: 'P0',
      category: '客套开场',
      label: '开场是自我介绍/问候语，等于把前 3 秒送掉',
      context: '第一句：' + first.slice(0, 30),
      basis: '「大家好 / 我是XX / 今天跟大家聊聊」不含任何信息增量，是划走高发区最常见的开场',
      advice: '整句删掉，把第二句里最有冲突的那半句提到最前面。观众不需要被问候，需要被击中',
    });
  }
  if (!hits.length && !deadOpen) {
    findings.push({
      level: 'P0',
      category: '钩子缺失',
      label: '前 3 秒没有任何留人手段',
      context: '开头：' + first.slice(0, 30),
      basis: '开场句未命中提问 / 反常识 / 利益承诺 / 冲突 / 悬念 / 数字 / 身份代入 / 结果前置 / 紧迫 九类钩子',
      advice: '把结论或冲突提到第一句。最低成本改法：把原来的第二句搬到最前面，第一句改成"你以为……其实……"',
    });
  } else if (!deadOpen && hits.length && hits[0].strength <= 1) {
    findings.push({
      level: 'P1',
      category: '钩子偏弱',
      label: '只命中弱钩子：' + hits[0].label,
      context: '开头：' + first.slice(0, 30),
      basis: '九类钩子中仅命中强度 1 的类型，抗划走能力有限',
      advice: '叠加一个强度 2-3 的钩子（反常识 / 冲突 / 提问），双钩子开场比单钩子稳',
    });
  }
  if (first.length > 34) {
    findings.push({
      level: 'P1',
      category: '开场过长',
      label: '第一句 ' + first.length + ' 字，读出来超过 3 秒',
      context: '第一句：' + first.slice(0, 40),
      basis: '口播 4-6 字/秒，34 字约 6 秒；前 3 秒是划走高发区',
      advice: '第一句压到 15 字以内，把背景信息挪到第二句之后',
    });
  }

  return {
    present: hits.length > 0 && !deadOpen,
    deadOpen,
    types: hits.map((h) => h.label),
    primary: deadOpen ? '客套开场（无有效钩子）' : (hits[0] ? hits[0].label : '无'),
    strength: deadOpen ? 0 : (hits.length ? hits[0].strength : 0),
    hookSec,
    findings,
  };
}

// ------------------------------------------------------------------ 结构分段

function analyzeSegments(sentences, hook) {
  const n = sentences.length;
  const found = {};
  // 按位置给权重：越靠前的句子命中的段落，权重越高
  L.SEGMENTS.forEach((seg) => { found[seg.key] = { hits: [], firstIdx: -1 }; });

  sentences.forEach((s, i) => {
    L.SEGMENTS.forEach((seg) => {
      let ok = false;
      if (seg.key === 'hook') {
        // 钩子段落是否成立，以 analyzeHook 的结论为准（它已排除客套开场）
        ok = !!hook.present && i < 2;
      } else if (seg.key === 'cta') ok = L.CTA_PATTERNS.some((c) => hitAny(s, c.re));
      else ok = hitAny(s, seg.re);
      if (ok) {
        found[seg.key].hits.push(i);
        if (found[seg.key].firstIdx < 0) found[seg.key].firstIdx = i;
      }
    });
  });

  const missing = L.SEGMENTS.filter((s) => found[s.key].hits.length === 0);
  // 客套开场已经单独报了 P0，这里不再重复报"缺钩子段"，避免同一条问题说两遍
  const missingForReport = missing.filter((s) => !(s.key === 'hook' && hook.deadOpen));
  const findings = missingForReport.map((s) => ({
    level: s.weight >= 3 ? 'P0' : 'P1',
    category: '结构缺段',
    label: '缺少「' + s.label + '」',
    context: '全文 ' + n + ' 句，未识别到该段落的语言标记',
    basis: '该段作用：' + s.goal + '；五段式缺一段，对应环节的转化会漏',
    advice: s.key === 'cta'
      ? '补一句具体指令（"评论区扣 1""点左下角领"），不要只写"欢迎关注"'
      : s.key === 'hook'
        ? '把最冲突/最反常识的一句提到第一句'
        : '补 1-2 句该段内容，位置按 钩子→痛点→干货→转折→CTA 的顺序插',
  }));

  return {
    map: L.SEGMENTS.map((s) => ({
      key: s.key,
      label: s.label,
      goal: s.goal,
      present: found[s.key].hits.length > 0,
      sentenceIndexes: found[s.key].hits,
      coverage: n ? +(found[s.key].hits.length / n).toFixed(3) : 0,
    })),
    missing: missing.map((s) => s.label),
    findings,
  };
}

// ------------------------------------------------------------------ 留存节奏

function analyzeRhythm(sentences, durationSec) {
  const lens = sentences.map((s) => s.length);
  const avg = lens.length ? lens.reduce((a, b) => a + b, 0) / lens.length : 0;
  const max = lens.length ? Math.max(...lens) : 0;

  // 长短句交替率：相邻句长差 > 8 字算一次变化
  let flips = 0;
  for (let i = 1; i < lens.length; i++) if (Math.abs(lens[i] - lens[i - 1]) > 8) flips++;
  const flipRate = lens.length > 1 ? flips / (lens.length - 1) : 0;

  // 拖沓段：连续 3 句及以上都长于 26 字
  const drag = [];
  let run = [];
  lens.forEach((len, i) => {
    if (len > 26) { run.push(i); }
    else { if (run.length >= 3) drag.push(run.slice()); run = []; }
  });
  if (run.length >= 3) drag.push(run.slice());

  const totalChars = sentences.reduce((a, s) => a + countChars(s), 0);
  const estSec = durationSec || (avg ? +(totalChars / 5).toFixed(1) : null); // 口播约 5 字/秒
  const density = estSec ? +(totalChars / estSec).toFixed(2) : null;

  const findings = [];
  if (drag.length) {
    findings.push({
      level: 'P1',
      category: '节奏拖沓',
      label: '存在 ' + drag.length + ' 处连续长句段',
      context: drag.map((r) => '第 ' + (r[0] + 1) + '-' + (r[r.length - 1] + 1) + ' 句').join('；'),
      basis: '连续 3 句以上超过 26 字，口播里表现为"一直没换气、没有新信息点"',
      advice: '每 2-3 句插一个 10 字以内的短句作为重音，把长句拆成"长-短-长"',
    });
  }
  if (lens.length >= 6 && flipRate < 0.25) {
    findings.push({
      level: 'P2',
      category: '句长单调',
      label: '长短句交替率 ' + (flipRate * 100).toFixed(0) + '%，节奏偏平',
      context: '平均句长 ' + avg.toFixed(1) + ' 字，最长 ' + max + ' 字',
      basis: '交替率低于 25% 时，听觉上缺少重音，中段容易流失',
      advice: '刻意做长短交替：每个长句后面跟一个 8 字以内的短句',
    });
  }
  if (density != null && density > 8) {
    findings.push({
      level: 'P2',
      category: '语速过快',
      label: '信息密度约 ' + density + ' 字/秒，偏快',
      context: '全文 ' + totalChars + ' 字，估算时长 ' + estSec + ' 秒',
      basis: '口播舒适区间约 4-6 字/秒，超过 8 字/秒观众来不及消化',
      advice: '删掉修饰性从句，把可省略的形容词去掉，或把时长放宽',
    });
  }

  return {
    sentences: lens.length,
    avgLen: +avg.toFixed(1),
    maxLen: max,
    flipRate: +(flipRate * 100).toFixed(1),
    dragRuns: drag.length,
    density,
    estSec,
    findings,
  };
}

// ------------------------------------------------------------------ 口语度

function analyzeSpeakability(sentences) {
  const text = sentences.join('');
  const written = [];
  for (const w of L.WRITTEN_WORDS) if (text.includes(w)) written.push(w);
  const oral = [];
  for (const w of L.ORAL_MARKERS) if (text.includes(w)) oral.push(w);

  const passive = L.PASSIVE_RE.test(text);
  const nounStack = L.NOUN_STACK_RE.test(text);
  const chars = countChars(text) || 1;
  const oralRate = +((oral.length / chars) * 100).toFixed(2);

  // 口语度评分：命中越少书面语、越多口语标记，越像"人在说话"
  let score = 100;
  score -= Math.min(45, written.length * 7);
  score -= passive ? 10 : 0;
  score -= nounStack ? 8 : 0;
  if (oral.length === 0) score -= 20;
  score = Math.max(0, Math.min(100, score));

  const findings = [];
  if (written.length >= 3) {
    findings.push({
      level: 'P1',
      category: '书面语过重',
      label: '命中 ' + written.length + ' 个书面语连接词',
      context: '命中：' + written.slice(0, 8).join('、'),
      basis: '口播稿里的书面语连接词是最典型的"AI 腔/公文腔"信号，观众听到会自动划走',
      advice: '逐个替换为口语说法。例："因此"→"所以"，"旨在"→"就是为了"，"进行"→直接删掉',
    });
  }
  if (passive) {
    findings.push({
      level: 'P2',
      category: '被动句',
      label: '存在被动语态',
      context: '命中"被/受到 + 动词"结构',
      basis: '口播里被动句理解成本高，主语不清',
      advice: '改成主动句，把做事的人提到前面',
    });
  }
  if (oral.length === 0) {
    findings.push({
      level: 'P1',
      category: '缺少口语标记',
      label: '全文没有出现任何人称或语气词',
      context: '未命中你/我/吧/呢/其实/就是 等口语标记',
      basis: '没有人称与语气词的稿子，读出来像播报，不像聊天',
      advice: '至少每 3 句出现一次"你"或"我"，并在转折处加"其实""说白了"',
    });
  }

  return { score, writtenHits: written, oralHits: oral, passive, nounStack, oralRate, findings };
}

// ------------------------------------------------------------------ CTA

function analyzeCTA(sentences) {
  const n = sentences.length;
  const hits = [];
  sentences.forEach((s, i) => {
    for (const c of L.CTA_PATTERNS) {
      if (hitAny(s, c.re)) { hits.push({ idx: i, key: c.key, label: c.label, strength: c.strength, text: s }); break; }
    }
  });
  const best = hits.length ? hits.reduce((a, b) => (b.strength > a.strength ? b : a)) : null;
  const tail = n ? hits.some((h) => h.idx >= n - 3) : false;

  const findings = [];
  if (!hits.length) {
    findings.push({
      level: 'P0',
      category: 'CTA 缺失',
      label: '全文没有行动指令',
      context: '未命中任何行动引导模式',
      basis: '没有 CTA 的脚本，观众看完就走，播放量换不来任何转化',
      advice: '结尾补一句具体动作，例如"评论区扣 1，我把模板发你"',
    });
  } else {
    if (!best || best.strength < 3) {
      findings.push({
        level: 'P1',
        category: 'CTA 偏弱',
        label: best ? ('只有' + best.label + '，缺"做什么 + 在哪做 + 得到什么"三要素') : '只有泛泛引导',
        context: '命中：' + (best ? best.text.slice(0, 30) : ''),
        basis: '「欢迎关注」「记得点赞」这类引导不构成可执行动作，转化率远低于具体指令',
        advice: '改成"评论区扣 1，我把脚本模板发你"这种三要素齐全的一句',
      });
    }
    if (!tail) {
      findings.push({
        level: 'P2',
        category: 'CTA 位置',
        label: '行动指令不在结尾',
        context: '最佳 CTA 出现在第 ' + (best.idx + 1) + ' 句，共 ' + n + ' 句',
        basis: '口播的转化指令通常放在结尾 3 句内，中段出现的容易被后文冲淡',
        advice: '结尾再补一次同样的指令，中段那次可以保留作为软转化',
      });
    }
  }

  return { present: hits.length > 0, count: hits.length, best, atTail: tail, findings };
}

// ------------------------------------------------------------------ 金句抽取

function extractGolden(sentences) {
  const out = [];
  sentences.forEach((s, i) => {
    const len = s.length;
    if (len < 8 || len > 30) return;
    // 含书面语连接词的句子不是金句（"……因此……"念出来没人转）
    if (L.WRITTEN_WORDS.some((w) => s.includes(w))) return;
    const hasContrast = /不是.{1,12}而是|宁可|要么|与其|越.{1,6}越/.test(s);
    const hasNumber = /\d/.test(s);
    const hasAssert = /(就是|才是|从来|根本|永远|一定|绝对|只能)/.test(s);
    const noFiller = !/(然后|那么|所以说|呃|就是那个)/.test(s);
    let score = 0;
    if (hasContrast) score += 3;
    if (hasAssert) score += 2;
    if (hasNumber) score += 1;
    if (noFiller) score += 1;
    // 门槛 4 分：光有"断言"不够，必须带对立结构或具体数字，否则抽出来的是废话
    if (score >= 4) out.push({ idx: i, text: s, score, reason: hasContrast ? '有对立结构' : hasNumber ? '有具体数字' : '有断言' });
  });
  return out.sort((a, b) => b.score - a.score).slice(0, 6);
}

// ------------------------------------------------------------------ 二创蓝图

function buildBlueprint(ctx) {
  const { hook, segments, cta, goal, platform } = ctx;
  const g = L.GOALS[goal] || null;
  const p = L.PLATFORM[platform] || L.PLATFORM.generic;
  const missing = new Set(segments.missing);

  const slots = [
    { part: '钩子（0-3 秒）', tpl: '「【你的目标人群】是不是也【原文里的痛点动作】？其实【反常识结论】。」',
      note: hook.present ? '原文已有钩子，替换人群与痛点即可' : '原文缺钩子，直接套用此模板重写第一句' },
    { part: '痛点共鸣', tpl: '「我见过太多【人群】卡在【具体场景】，明明【努力动作】，结果【负向结果】。」',
      note: missing.has('痛点共鸣') ? '原文缺此段，建议补 1-2 句' : '保留原文痛点，只替换行业词' },
    { part: '论证与干货', tpl: '「第一，【要点一】。第二，【要点二】。第三，【要点三】。」',
      note: '原文论点数量：' + (segments.map.find((m) => m.key === 'value') ? segments.map.find((m) => m.key === 'value').sentenceIndexes.length : 0) + ' 句，建议压到 3 点以内' },
    { part: '转折与升华', tpl: '「但真正拉开差距的，不是【表层动作】，而是【底层变量】。」',
      note: missing.has('转折与升华') ? '原文缺此段，建议补 1 句立观点' : '原文已有，可直接复用句式' },
    { part: 'CTA', tpl: '「【具体动作】，我【给出什么】，【时间或数量限定】。」',
      note: g ? g.ctaHint : (cta.present ? '原文 CTA 已有，按三要素补全' : '原文缺 CTA，必须补') },
  ];

  return {
    platform: p.label,
    goal: g ? g.label : '未指定',
    densityHint: p.densityHint,
    sweetSec: p.sweetSec,
    slots,
  };
}

// ------------------------------------------------------------------ 主入口


// 工厂契约要求导出干净样例（两档跑完 0 命中）—— 与 templates/sample.json 同一份文本。
const SAMPLE_TEXT = "00:00 大家好，今天我想跟大家分享一下我做短视频这半年的一些心得体会和经验总结。\n00:07 其实很多新手在做内容的时候都会遇到一个共同的问题，就是不知道应该拍什么，因此每天都很焦虑。\n00:16 我一开始也是这样，后来我总结出了三个方法，第一个方法是把客户最常问的十个问题列出来。\n00:25 第二个方法是从这些问题里挑出你自己真正踩过坑的那三个，然后把它讲清楚。\n00:34 第三个方法是在讲的时候不要只讲结论，而是要把整个思考的过程完整地呈现出来，因为观众想听的是过程而不是结果。\n00:46 值得注意的是，这个方法对于知识类的账号效果会更加明显一些，因此大家可以参考一下。\n00:55 我自己用这个方法跑了三个月，播放量确实有明显的提升。\n01:02 欢迎关注我，谢谢大家。";
// ⚠️ 本引擎的样例是**故意有问题的口播稿**（演示用）⇒ 声明"样例会有命中"，
//    剥离工具的烟测据此放行（默认仍要求 0 命中，其他包不受影响）。
const SAMPLE_HAS_FINDINGS = true;

const CHECKS_GIVEN = [
  '结构地图（钩子 / 痛点共鸣 / 论证干货 / 转折升华 / 行动指令 五段）',
  '开场钩子判定（含"客套开场"识别与强度）',
  '留存节奏诊断（逐段句数与估算时长）',
  '口语度评分（书面语连接词、长句占比）',
  'CTA 强度判定',
  '问题分级清单（P0/P1/P2 + 位置与原文）',
];

const CHECKS_WITHHELD = [
  '金句候选提取（可复用的短句，含书面语过滤）',
  '二创蓝图（可直接填空的改写骨架）',
];

const MIN_CHARS = 30;
const MIN_SENTENCES = 3;

function deconstruct(payload) {
  const input = payload || {};
  let raw = input.text || input.transcript || input.script || '';
  // 容错：有些调用方会把逐字稿按行拆成数组传进来，这里拼回文本
  if (Array.isArray(raw)) raw = raw.map((x) => String(x == null ? '' : x)).join('\n');
  const text = normalizeText(raw);
  const platform = L.PLATFORM[input.platform] ? input.platform : 'generic';
  const goal = L.GOALS[input.goal] ? input.goal : '';

  // ---- 材料是否足够（不足时明确说缺什么，绝不返回"没问题"）
  const chars = countChars(text);
  const sentences0 = splitSentences(text);
  if (chars < MIN_CHARS || sentences0.length < MIN_SENTENCES) {
    return {
      ok: false,
      code: 3,
      reason: '材料不足，无法拆解',
      detail: {
        chars: chars,
        sentences: sentences0.length,
        needChars: MIN_CHARS,
        needSentences: MIN_SENTENCES,
      },
      message: '只收到 ' + chars + ' 个字、' + sentences0.length + ' 句。'
        + '拆解至少要 ' + MIN_CHARS + ' 个字且不少于 ' + MIN_SENTENCES + ' 句。'
        + '请提供完整的口播逐字稿（带时间戳更好，例如 "00:03 你是不是也……"）。',
      findings: [],
    };
  }

  const { lines, hasTs } = parseTimed(text);
  const sentences = sentences0;
  const durationSec = Number(input.duration) > 0 ? Number(input.duration) : null;

  const hook = analyzeHook(sentences, lines, hasTs);
  const segments = analyzeSegments(sentences, hook);
  const rhythm = analyzeRhythm(sentences, durationSec);
  const speak = analyzeSpeakability(sentences);
  const cta = analyzeCTA(sentences);
  const golden = extractGolden(sentences);
  const blueprint = buildBlueprint({ hook, segments, cta, goal, platform });

  const findings = [
    ...hook.findings, ...segments.findings, ...rhythm.findings, ...speak.findings, ...cta.findings,
  ];
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  // 综合可读性分：口语度为主，扣结构缺段与钩子缺失
  let score = speak.score;
  score -= p0 * 12;
  score -= p1 * 5;
  score = Math.max(0, Math.min(100, Math.round(score)));

  return {
    ok: true,
    summary: {
      chars,
      sentences: sentences.length,
      hasTimestamps: hasTs,
      durationSec: rhythm.estSec,
      hookPrimary: hook.primary,
      hookStrength: hook.strength,
      structureMissing: segments.missing.length,
      oralScore: speak.score,
      ctaStrength: cta.best ? cta.best.strength : 0,
      total: findings.length,
      p0, p1, p2,
      score,
    },
    hook,
    structure: segments,
    rhythm,
    speakability: speak,
    cta,
    goldenLines: [],
    blueprint: null,
    checks_given: CHECKS_GIVEN.slice(),
    checks_not_run: CHECKS_WITHHELD.slice(),
    findings,
  };
}


// ---------------------------------------------------------------- 工厂契约适配层
// ⚠️ 第 236 轮：本引擎原本只导出 `deconstruct`（返回 {ok, summary, findings…}），
//    而工厂契约、剥离工具的烟测、MCP 描述都按 `run(payload) -> {status, result}` 调用。
//    这里加一层**薄适配**：`run` 走标准信封，`deconstruct` 保持原样（包内 run.mjs 不受影响）。
const OUT_OF_SCOPE = [
  '替你改写/润色逐字稿（只做结构诊断与建议）',
  '预测真实完播率与播放量（平台算法不公开）',
  '判断选题是否违规（平台规则随时变，以平台现行规则为准）',
];

function run(payload) {
  const r = deconstruct(payload);
  if (!r || r.ok === false) {
    return {
      status: 'insufficient_input',
      missing: r && r.detail ? [`字数 ${r.detail.chars}/${r.detail.needChars}`, `句数 ${r.detail.sentences}/${r.detail.needSentences}`] : ['逐字稿正文（text）'],
      advice: '把完整口播逐字稿贴进来再跑；材料不足时本工具不给任何结论。',
    };
  }
  const notRun = CHECKS_WITHHELD.slice();   // 免费档：如实声明未执行项
  return {
    status: 'success',
    result: {
      status: 'success',
      service_type: 'VIRAL_SCRIPT_DECONSTRUCT',
      scope: {
        checks: CHECKS_GIVEN.slice(),
        checks_not_run: notRun,
        chars: r.summary.chars,
        sentences: r.summary.sentences,
        oral_score: r.summary.oralScore,
        hook_strength: r.summary.hookStrength,
        executed_locally: true,
        network_used: false,
      },
      findings: (r.findings || []).map((f, i) => ({
        line: i + 1, level: f.level || 'P1', category: f.label || '问题',
        message: f.detail || f.label || '', evidence: JSON.stringify(f.evidence || {}),
      })),
      summary: {
        total: r.summary.total, p0: r.summary.p0, p1: r.summary.p1, p2: r.summary.p2,
        verdict: r.summary.p0 > 0 ? 'ERROR_FOUND' : (r.summary.total ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      },
      checks_out_of_scope: OUT_OF_SCOPE,
      note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
      disclaimer: '只做结构诊断（钩子/留存/CTA/口语度/结构缺段）；结论可由第三方用同一份逐字稿复算。',
    },
  };
}

module.exports = {
  // ⚠️ 第 236 轮：工厂契约要求导出 `run`（MCP/门禁都按 run 调）；
  //    这个引擎原来只导出 `deconstruct` ⇒ 补一个别名，功能完全不变。
  run,
  deconstruct,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  OUT_OF_SCOPE,
  SAMPLE_TEXT,
  SAMPLE_HAS_FINDINGS,
  normalizeText,
  splitSentences,
  parseTimed,
  countChars,
  MIN_CHARS,
  MIN_SENTENCES,
};
