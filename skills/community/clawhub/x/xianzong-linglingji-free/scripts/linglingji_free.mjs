#!/usr/bin/env node
/**
 * 灵灵机免费体验版 · 离线事实层速算（零依赖，只用 Node 标准库，不联网、不调用付费接口）
 *
 * 用法：
 *   node linglingji_free.mjs scenes
 *   node linglingji_free.mjs marriage --birth-date 1995-06-23 --birth-hour 20 --gender 女
 *   node linglingji_free.mjs tarot --spread three --question "我和TA的关系走向" [--seed 42]
 *   node linglingji_free.mjs dream --text "昨晚梦见棺材抬进家门"
 *
 * 退出码：0 正常输出；2 参数非法。
 *
 * 说明：本脚本只产出「事实层」（干支、星宫、抽到的牌、命中的意象），
 * 解读由调用方的 AI 依据 references/ 里的表格完成。这样既能保证干支不出错，
 * 又不需要任何模型调用成本。
 */

import process from 'node:process';

const BRAND_URL = 'https://www.xianzongwendao.com/activities/tradition';

const G = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const Z = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
const SX = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];

const WUSHUDUN = {
    甲: '甲',
    乙: '丙',
    丙: '戊',
    丁: '庚',
    戊: '壬',
    己: '甲',
    庚: '丙',
    辛: '戊',
    壬: '庚',
    癸: '壬',
};

// 六合 / 三合 / 天干五合
const LIUHE = { 子: '丑', 丑: '子', 寅: '亥', 亥: '寅', 卯: '戌', 戌: '卯', 辰: '酉', 酉: '辰', 巳: '申', 申: '巳', 午: '未', 未: '午' };
const SANHE_GROUP = [
    ['申', '子', '辰'],
    ['寅', '午', '戌'],
    ['巳', '酉', '丑'],
    ['亥', '卯', '未'],
];
const YINYANG_HE = [['甲', '己'], ['乙', '庚'], ['丙', '辛'], ['丁', '壬'], ['戊', '癸']];

// 十天干五行
const GAN_ELEMENT = {
    甲: '木', 乙: '木', 丙: '火', 丁: '火', 戊: '土', 己: '土', 庚: '金', 辛: '金', 壬: '水', 癸: '水',
};
// 我克者（财）与克我者（官杀）
const KE = { 木: '土', 火: '金', 土: '水', 金: '木', 水: '火' };
const BEI_KE = { 土: '木', 金: '火', 水: '土', 木: '金', 火: '水' };

const mod = (n, m) => ((n % m) + m) % m;

function fail(message) {
    process.stderr.write(`参数错误：${message}\n`);
    process.exit(2);
}

function parseArgs(argv) {
    const out = { _: [] };
    for (let i = 0; i < argv.length; i += 1) {
        const token = argv[i];
        if (token.startsWith('--')) {
            const key = token.slice(2);
            const next = argv[i + 1];
            if (next && !next.startsWith('--')) {
                out[key] = next;
                i += 1;
            } else {
                out[key] = true;
            }
        } else {
            out._.push(token);
        }
    }
    return out;
}

// ---------------- 干支 ----------------

function parseDate(text) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(text || '')) fail('--birth-date 需要 YYYY-MM-DD');
    const [y, m, d] = text.split('-').map(Number);
    const t = Date.UTC(y, m - 1, d);
    const back = new Date(t);
    if (back.getUTCFullYear() !== y || back.getUTCMonth() !== m - 1 || back.getUTCDate() !== d) {
        fail('--birth-date 不是合法公历日期');
    }
    return { y, m, d, t };
}

/** 日柱干支：锚点 1949-10-01 = 甲子（与后端 ganzhi.py 同一锚点） */
function dayPillar(t) {
    const idx = mod((t - Date.UTC(1949, 9, 1)) / 86400000, 60);
    return { gan: G[idx % 10], zhi: Z[idx % 12], idx };
}

/** 年柱干支：1984 = 甲子；立春按 2 月 4 日近似分界 */
function yearPillar({ y, m, d }) {
    const yyyy = m < 2 || (m === 2 && d < 4) ? y - 1 : y;
    const idx = mod(yyyy - 1984, 60);
    return { gan: G[idx % 10], zhi: Z[idx % 12], year: yyyy };
}

/** 时柱干支：五鼠遁 + 时辰（子时 23:00-00:59） */
function hourPillar(dayGan, hour) {
    const shichen = mod(Math.floor((hour + 1) / 2), 12);
    const ziGan = WUSHUDUN[dayGan];
    return { gan: G[(G.indexOf(ziGan) + shichen) % 10], zhi: Z[shichen], name: `${Z[shichen]}时` };
}

function spouseStar(dayGan, gender) {
    const element = GAN_ELEMENT[dayGan];
    const target = gender === '男' ? KE[element] : BEI_KE[element];
    const found = G.filter((g) => GAN_ELEMENT[g] === target);
    // 同阴阳为偏（男：偏财；女：七杀），异阴阳为正（男：正财；女：正官）
    const dayIsYang = G.indexOf(dayGan) % 2 === 0;
    const mapper = found.map((g) => {
        const isYang = G.indexOf(g) % 2 === 0;
        const same = isYang === dayIsYang;
        const label = gender === '男' ? (same ? '偏财' : '正财') : same ? '七杀' : '正官';
        return `${label} ${g}${target}`;
    });
    return { target, labels: mapper, relation: gender === '男' ? '我克者为财（妻星）' : '克我者为官杀（夫星）' };
}

/** 桃花：以三合局（申子辰→酉 / 寅午戌→卯 / 巳酉丑→午 / 亥卯未→子） */
function peachBlossom(zhi) {
    const table = { 申: '酉', 子: '酉', 辰: '酉', 寅: '卯', 午: '卯', 戌: '卯', 巳: '午', 酉: '午', 丑: '午', 亥: '子', 卯: '子', 未: '子' };
    return table[zhi] || '—';
}

function sameGroup(a, b) {
    return SANHE_GROUP.some((group) => group.includes(a) && group.includes(b));
}

function heYingYears(dayGan, dayZhi, fromYear, count = 10) {
    const lines = [];
    for (let y = fromYear; y < fromYear + count; y += 1) {
        const idx = mod(y - 1984, 60);
        const gan = G[idx % 10];
        const zhi = Z[idx % 12];
        const marks = [];
        if (LIUHE[dayZhi] === zhi) marks.push(`流年支${zhi} 与日支${dayZhi} 六合 → 合动夫妻宫`);
        else if (sameGroup(dayZhi, zhi) && zhi !== dayZhi) marks.push(`流年支${zhi} 与日支${dayZhi} 三合 → 合局助动`);
        if (YINYANG_HE.some((pair) => pair.includes(dayGan) && pair.includes(gan) && gan !== dayGan)) marks.push(`流年干${gan} 与日干${dayGan} 五合 → 日干被合`);
        if (marks.length) lines.push(`${y} ${gan}${zhi}：${marks.join('；')}`);
    }
    return lines;
}

// ---------------- 塔罗 ----------------

const MAJORS = [
    ['愚人', '新的开始 / 冒险 / 纯真', '鲁莽 / 缺乏方向'],
    ['魔术师', '创造 / 行动力 / 技能', '欺瞒 / 才能被滥用'],
    ['女祭司', '直觉 / 潜意识', '压抑 / 表面平静'],
    ['皇后', '丰盛 / 滋养 / 母性', '过度付出 / 依赖'],
    ['皇帝', '权威 / 结构 / 领导', '固执 / 控制欲'],
    ['教皇', '传统 / 信仰 / 教育', '教条 / 僵化'],
    ['恋人', '爱情 / 选择 / 结合', '分离 / 优柔寡断'],
    ['战车', '胜利 / 决心 / 控制', '失控 / 内耗冲突'],
    ['力量', '勇气 / 耐心 / 内在力量', '自我怀疑 / 软弱'],
    ['隐士', '内省 / 独处 / 智慧', '孤立 / 逃避'],
    ['命运之轮', '循环 / 转折 / 机遇', '停滞 / 重复旧局'],
    ['正义', '平衡 / 公正 / 因果', '失衡 / 双重标准'],
    ['倒吊人', '牺牲 / 换位 / 新视角', '无谓牺牲 / 拖延'],
    ['死神', '结束 / 转变 / 新生', '抗拒改变 / 僵持'],
    ['节制', '平衡 / 耐心 / 调和', '失衡 / 过犹不及'],
    ['恶魔', '束缚 / 欲望 / 阴影', '挣脱 / 看清执念'],
    ['高塔', '突变 / 崩塌 / 启示', '压抑后的爆发'],
    ['星星', '希望 / 灵感 / 治愈', '失望 / 失去信心'],
    ['月亮', '幻觉 / 潜意识 / 不确定', '真相浮现 / 焦虑'],
    ['太阳', '快乐 / 成功 / 活力', '暂时的阴霾'],
    ['审判', '觉醒 / 宽恕 / 转化', '自我怀疑 / 错失'],
    ['世界', '完成 / 圆满 / 整合', '未竟 / 缺一环'],
];

const SUITS = [
    ['权杖', '火', '行动、热情、创造'],
    ['圣杯', '水', '情感、关系、直觉'],
    ['宝剑', '风', '思想、沟通、冲突'],
    ['星币', '土', '现实、金钱、工作'],
];
const NUM_MEANING = ['开始 / 种子（Ace）', '平衡 / 选择', '成长 / 协作', '稳定 / 结构', '变化 / 冲突', '调和 / 给予', '评估 / 内省', '推进 / 力量', '接近完成', '完成 / 循环'];
const COURT = [
    ['侍从', '学习者 / 消息'],
    ['骑士', '行动 / 追求'],
    ['皇后', '成熟内化 / 滋养'],
    ['国王', '掌控 / 外显'],
];

const SPREADS = {
    single: ['单张牌'],
    three: ['过去', '现在', '未来'],
    celtic: ['1 现状', '2 阻碍', '3 潜意识', '4 过去', '5 目标', '6 近期未来', '7 自我', '8 环境', '9 希望 / 恐惧', '10 结果'],
};

function makeRng(seedText) {
    let a = (seedText === undefined || seedText === null ? Date.now() : Number(seedText)) >>> 0;
    if (!Number.isFinite(a)) a = Date.now() >>> 0;
    return () => {
        a = (a + 0x6d2b79f5) >>> 0;
        let t = a;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
}

function drawOne(rng) {
    const total = MAJORS.length + SUITS.length * 14;
    const i = Math.floor(rng() * total);
    const upright = rng() < 0.5;
    if (i < MAJORS.length) {
        const [name, up, rev] = MAJORS[i];
        return { card: name, upright, major: true, keyword: upright ? up : rev };
    }
    const rest = i - MAJORS.length;
    const suitIdx = Math.floor(rest / 14);
    const rank = rest % 14;
    const [suitName, element, theme] = SUITS[suitIdx];
    if (rank < 10) {
        const num = rank + 1;
        return {
            card: `${suitName}${num === 1 ? 'Ace' : num}`,
            upright,
            major: false,
            keyword: `${theme} · ${NUM_MEANING[rank]}${upright ? '' : '（逆位：能量受阻 / 内化 / 延迟）'}`,
            element,
        };
    }
    const [court] = COURT[rank - 10];
    return {
        card: `${suitName}${court}`,
        upright,
        major: false,
        keyword: `${theme} · ${COURT[rank - 10][1]}${upright ? '' : '（逆位：能量受阻 / 过度 / 内化）'}`,
        element,
    };
}

// ---------------- 解梦 ----------------

const DREAM_TABLE = [
    { keys: ['棺材', '灵柩'], trad: '谐音“官财”，反梦典型（凶象吉断）→ 主升迁 / 进财之机', rule: '谐音 + 反梦', psy: '对“结束与开始”这类转变心存焦虑' },
    { keys: ['死人', '去世', '过世', '丧事', '葬礼'], trad: '“梦死得生”，反梦 → 主新阶段开始', rule: '反梦', psy: '告别、转化、旧阶段收尾' },
    { keys: ['掉牙', '牙齿掉', '牙松'], trad: '民俗主亲人 / 自身有变故；也主“齿为骨之余”，留意精力', rule: '类象', psy: '焦虑、对衰老或失控的担忧' },
    { keys: ['蛇'], trad: '财 / 小人 / 变化象征，视细节；龙蛇之变也主转运', rule: '类象', psy: '潜藏的欲望或威胁感' },
    { keys: ['大水', '洪水', '涨水', '发水'], trad: '水主财与流动：清水吉、浊水忧；大水漫屋主财务有波动', rule: '类象', psy: '情绪如水漫溢，需疏导' },
    { keys: ['水'], trad: '水主财源流动；清浊定吉凶', rule: '类象', psy: '情绪流动与安全感' },
    { keys: ['大火', '着火', '烧屋', '火灾'], trad: '旺火吉、烧屋凶，火势定吉凶', rule: '类象', psy: '情绪激烈或能量高涨' },
    { keys: ['金银', '捡钱', '发钱', '财宝'], trad: '直接财象；失金主失财之忧', rule: '类象', psy: '对资源与安全感的关注' },
    { keys: ['飞', '飞翔'], trad: '升迁 / 自由 / 压力释放', rule: '类象', psy: '渴望摆脱束缚' },
    { keys: ['已故', '奶奶', '爷爷', '外婆', '外公', '母亲', '父亲'], trad: '思念与情感投射，以安抚为主；不渲染“托梦 / 缠身”', rule: '民俗', psy: '未完成的告别与思念' },
    { keys: ['考试', '迟到', '赶不上', '考场'], trad: '非凶梦，多为现实压力的象征', rule: '心理映射', psy: '考核 / 绩效 / 被评判的压力' },
    { keys: ['追', '逃', '逃跑', '被追'], trad: '压力与回避的象征，不作吉凶断', rule: '心理映射', psy: '回避冲突、被推着走' },
    { keys: ['坠落', '掉下去', '摔下', '悬崖'], trad: '失控感，不作吉凶断', rule: '心理映射', psy: '对失去掌控的担忧' },
    { keys: ['大便', '屎', '拉屎'], trad: '谐“变 / 发”，民俗主财运；也主“清空 / 放下”', rule: '谐音', psy: '释放、排空、卸下负担' },
    { keys: ['鱼'], trad: '谐“余”，主有余财、结余', rule: '谐音', psy: '丰足感与积累' },
    { keys: ['梨'], trad: '谐“离”，主分离议题', rule: '谐音', psy: '关系中的距离感' },
    { keys: ['血'], trad: '传统主耗损 / 情绪激烈；不据此判断健康', rule: '类象', psy: '强烈情绪或耗竭感' },
    { keys: ['猫', '狗', '鸟', '小动物'], trad: '视情境，多为陪伴、本能与情绪投射', rule: '类象', psy: '对陪伴与被照顾的需求' },
    { keys: ['头发', '掉发'], trad: '形象与精力议题，不作吉凶断', rule: '类象', psy: '对自我形象 / 状态的焦虑' },
    { keys: ['房子', '房屋', '家', '老宅'], trad: '家宅与安全感的结构象征', rule: '类象', psy: '对归属与安全的需求' },
    { keys: ['迷路', '找不到路', '不认识路'], trad: '方向感与选择焦虑', rule: '心理映射', psy: '对未来路径不确定' },
    { keys: ['裸体', '没穿衣服', '裸'], trad: '暴露与被看见的焦虑', rule: '心理映射', psy: '害怕被评判 / 被看穿' },
    { keys: ['雪', '结冰', '冰'], trad: '停滞与冷静期，主“暂缓”而非凶兆', rule: '类象', psy: '情绪进入冷却与静止' },
    { keys: ['结婚', '婚礼', '喜事'], trad: '结合与承诺议题', rule: '类象', psy: '对承诺 / 进入新阶段的期待或压力' },
    { keys: ['怀孕', '生孩子', '婴儿'], trad: '创造与新阶段象征；不据此判断身体状况', rule: '类象', psy: '新计划、新身份即将诞生' },
];

// ---------------- 输出 ----------------

// 7 大分类（顺序固定；每个场景引导时把最相关的那个提到最前）
const CATEGORIES = {
    renhe: '人和·情感：问姻缘 / 问相处 / 问婚姻',
    shiye: '事业·功名：问事业 / 问功名 / 问合伙 / 问财运',
    xueye: '学业·功名：问学业 / 问孩童文昌位',
    tianshi: '天时·择日：问乔迁 / 问出行 / 问吉日 / 问今辰',
    dili: '地利·宅居：问宅居（可出 3D 效果图）/ 问宅安',
    ankang: '安康·养生：问安康',
    zazhan: '杂占·趣参：问梦境 / 问失物 / 问测字 / 问数字 / 问手机号 / 问塔罗 / 问紫微 / 问命卦',
};
const CATEGORY_ORDER = ['renhe', 'shiye', 'xueye', 'tianshi', 'dili', 'ankang', 'zazhan'];

const SCENE_HINTS = {
    marriage: {
        title: '想知道更准的姻缘判断？',
        line: '免费版只给日柱与合动候选年份；完整版会排完整八字（月令旺衰与十神、大运流年逐运推演），再叠加六壬三传定应期，能给出对象画像与正缘偏缘的辨别方向。',
        lead: 'renhe',
    },
    dream: {
        title: '想解得更细？',
        line: '免费版是一张 25 条意象速查表；完整版接的是完整占梦知识库，能区分水清水浊、火势大小等细节，支持上传梦境图辅助提取意象，还可选做梅花易数梦象起卦。',
        lead: 'zazhan',
    },
    tarot: {
        title: '想抽得更认真一点？',
        line: '免费版只给 22 张大阿卡纳的关键词；完整版有 78 张逐张牌意，会把整个牌阵当一个故事讲（牌与牌的呼应、矛盾、能量走向），重要抉择还能与八字、事件应期交叉验证。',
        lead: 'zazhan',
    },
};

function footer(scene) {
    const hint = SCENE_HINTS[scene];
    // 把关切的分类提到第一个，其余按固定顺序补齐
    const order = [hint.lead, ...CATEGORY_ORDER.filter((key) => key !== hint.lead)];
    return [
        '',
        '---',
        '【合规声明】',
        '本内容是传统文化与心理视角的参考解读，不构成预测、医疗、心理、法律或投资建议。',
        '重大决定请结合实际情况并咨询对应专业人士。',
        '',
        `【${hint.title}去灵灵机完整版】`,
        hint.line,
        '',
        '完整版是 7 大分类 · 24 个场景，比免费版更专业、场景也更全：',
        ...order.map((key) => `  · ${CATEGORIES[key]}`),
        '',
        '另外，完整版还能上传户型图生成 3D 改造效果图、把咨询结果导出成排版 PDF 报告，',
        '并且支持多轮对话——会记住你的出生信息与双人资料，不用每次重复交代。',
        '👉 仙踪问道 · 灵灵机：',
        `   ${BRAND_URL}`,
    ].join('\n');
}

function cmdScenes() {
    return [
        '灵灵机免费体验版 · 开放的 3 个场景（完整版 7 大分类 · 24 个场景）',
        '',
        '1) 问姻缘·佳偶之期（KB-T-001）  需要：出生日期 + 时辰 + 性别',
        '2) 问梦境·意象之解（KB-T-016）  需要：梦境描述（情节 / 人物 / 情绪 / 醒来感受）',
        '3) 问塔罗·西方占卜（KB-T-022）  需要：一个具体问题（+ 可选牌阵）',
        '',
        '命令：',
        '  node linglingji_free.mjs marriage --birth-date 1995-06-23 --birth-hour 20 --gender 女',
        '  node linglingji_free.mjs dream --text "梦见棺材抬进家门"',
        '  node linglingji_free.mjs tarot --spread three --question "我和TA的关系走向"',
        '',
        `完整版 7 大分类 · 24 场景：${BRAND_URL}`,
    ].join('\n');
}

function cmdMarriage(args) {
    if (!args['birth-date']) fail('缺少 --birth-date');
    if (!args['birth-hour']) fail('缺少 --birth-hour（0-23）');
    if (!args.gender || !['男', '女'].includes(args.gender)) fail('--gender 只能是 男 / 女');

    const hour = Number(args['birth-hour']);
    if (!Number.isInteger(hour) || hour < 0 || hour > 23) fail('--birth-hour 需要 0-23 的整数');

    const date = parseDate(args['birth-date']);
    const day = dayPillar(date.t);
    const year = yearPillar(date);
    const hourPillarInfo = hourPillar(day.gan, hour);
    const star = spouseStar(day.gan, args.gender);
    const peachDay = peachBlossom(day.zhi);
    const peachYear = peachBlossom(year.zhi);
    const fromYear = Number(args['from-year']) || new Date().getFullYear();
    const heYing = heYingYears(day.gan, day.zhi, fromYear);

    return [
        '【事实层 · 简化四柱】',
        `公历 ${args['birth-date']} ${String(hour).padStart(2, '0')} 时 · ${args.gender}命`,
        `年柱 ${year.gan}${year.zhi}（立春按 2 月 4 日近似分界；所属农历年 ${year.year}）`,
        `日柱 ${day.gan}${day.zhi}（日主 ${day.gan}${GAN_ELEMENT[day.gan]}，夫妻宫＝日支 ${day.zhi}）`,
        `时柱 ${hourPillarInfo.gan}${hourPillarInfo.zhi}（${hourPillarInfo.name}，五鼠遁）`,
        `生肖 ${SX[Z.indexOf(year.zhi)]}`,
        '',
        '【事实层 · 姻缘要素】',
        `配偶星（${star.relation}）：${star.labels.join(' / ')}`,
        `桃花（按年支三合）：${peachYear}；按日支三合：${peachDay}`,
        '（月令旺衰、大运流年、六壬三传需要完整排盘，免费版不给强弱结论）',
        '',
        `【合动候选窗口 · ${fromYear} 起 10 年】`,
        heYing.length ? heYing.map((line) => `· ${line}`).join('\n') : '· 未来 10 年未出现明显的合动组合（不代表没有机会，只是本年表无强信号）',
        '（合动是传统应期规则的“候选年份”，不等于必然发生，也不给具体日期）',
        '',
        footer('marriage'),
    ].join('\n');
}

function cmdTarot(args) {
    const spread = args.spread || 'single';
    if (!SPREADS[spread]) fail('--spread 只能是 single / three / celtic');
    const question = args.question === true || !args.question ? '' : String(args.question);
    if (!question) fail('缺少 --question（一句话描述你要问的事）');

    const rng = makeRng(args.seed === true ? undefined : args.seed);
    const lines = [
        '【事实层 · 模拟抽牌】',
        '⚠️ 本次为程序模拟抽牌，非真实洗牌；如条件允许，请用实体牌自行洗牌。',
        `问题：${question}`,
        `牌阵：${spread}（${SPREADS[spread].length} 张）`,
        '',
    ];
    for (const position of SPREADS[spread]) {
        const card = drawOne(rng);
        lines.push(`【${position}】${card.card}（${card.upright ? '正位' : '逆位'}）→ ${card.keyword}`);
    }
    lines.push(
        '',
        '解读顺序：位置含义 → 正逆位能量 → 牌面关键词 → 元素（火 / 水 / 风 / 土）→ 数字（1-10 进程）→ 与问题的对应',
        '平衡原则：不要因一张好牌过度乐观；一张好牌配一张逆位多为中等；大阿卡纳主导长期，小阿卡纳主导近期。',
        '',
        footer('tarot'),
    );
    return lines.join('\n');
}

function cmdDream(args) {
    const text = args.text === true || !args.text ? '' : String(args.text);
    if (!text) fail('缺少 --text（梦境描述）');
    const hits = DREAM_TABLE.filter((item) => item.keys.some((k) => text.includes(k)));

    const lines = ['【事实层 · 意象速查】', `梦境描述：${text}`, ''];
    if (hits.length) {
        for (const hit of hits) {
            lines.push(`· 命中意象：${hit.keys[0]}`);
            lines.push(`  传统解：${hit.trad}（规则：${hit.rule}）`);
            lines.push(`  心理层：${hit.psy}`);
        }
    } else {
        lines.push('· 未命中速查表中的常见意象，按下面的三层规则自行拆解。');
    }
    lines.push(
        '',
        '【三层拆解规则】',
        '1) 类象：梦象对应的事物属性（梦水＝坎 / 财与流动，梦火＝离 / 心与激烈）',
        '2) 谐音：梨→离、棺材→官财、鱼→余',
        '3) 反梦：梦死得生、梦失得得、凶象常反断吉',
        '',
        '【还缺什么信息】',
        '· 梦里的情绪（害怕 / 开心 / 委屈 / 麻木）',
        '· 醒来那一刻的感受',
        '· 近期最在意的现实压力（工作 / 感情 / 家人 / 金钱）',
        '',
        '【边界】',
        '不做心理或医疗诊断；不因梦象渲染灾祸；长期噩梦影响睡眠时建议寻求专业心理支持。',
        '',
        footer('dream'),
    );
    return lines.join('\n');
}

// ---------------- 入口 ----------------

function main() {
    const args = parseArgs(process.argv.slice(2));
    const command = args._[0];

    if (!command || command === 'help' || command === '--help') {
        process.stdout.write(`${cmdScenes()}\n`);
        return;
    }

    let output;
    switch (command) {
        case 'scenes':
            output = cmdScenes();
            break;
        case 'marriage':
            output = cmdMarriage(args);
            break;
        case 'tarot':
            output = cmdTarot(args);
            break;
        case 'dream':
            output = cmdDream(args);
            break;
        default:
            fail(`未知命令 ${command}，可用：scenes / marriage / tarot / dream`);
    }
    process.stdout.write(`${output}\n`);
}

main();
