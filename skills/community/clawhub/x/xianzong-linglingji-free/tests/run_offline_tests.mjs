#!/usr/bin/env node
/**
 * 离线自测：不联网、不付费，只校验脚本层的事实输出与参数边界。
 * 运行：node "$SKILL_DIR/tests/run_offline_tests.mjs"
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCRIPT = path.resolve(__dirname, '..', 'scripts', 'linglingji_free.mjs');

let passed = 0;
const failures = [];

function run(args) {
    const res = spawnSync(process.execPath, [SCRIPT, ...args], { encoding: 'utf8' });
    return { code: res.status, out: res.stdout || '', err: res.stderr || '' };
}

function check(name, fn) {
    try {
        fn();
        passed += 1;
        console.log(`✅ ${name}`);
    } catch (error) {
        failures.push(`${name} → ${error.message}`);
        console.log(`❌ ${name} → ${error.message}`);
    }
}

function assert(condition, message) {
    if (!condition) throw new Error(message);
}

// 1. scenes 命令列出三个场景
check('scenes 列出 3 个场景', () => {
    const r = run(['scenes']);
    assert(r.code === 0, `退出码 ${r.code}`);
    assert(r.out.includes('KB-T-001'), '缺 KB-T-001');
    assert(r.out.includes('KB-T-016'), '缺 KB-T-016');
    assert(r.out.includes('KB-T-022'), '缺 KB-T-022');
});

// 2. 无参数等价 help
check('无参数输出使用说明', () => {
    const r = run([]);
    assert(r.code === 0, `退出码 ${r.code}`);
    assert(r.out.includes('linglingji_free.mjs'), '缺少命令示例');
});

// 3. 日柱/时柱与后端一致（1995-06-23 20 时 = 乙酉 / 丙戌）
check('日柱乙酉 + 时柱丙戌（与后端 ganzhi.py 一致）', () => {
    const r = run(['marriage', '--birth-date', '1995-06-23', '--birth-hour', '20', '--gender', '女']);
    assert(r.code === 0, `退出码 ${r.code}`);
    assert(r.out.includes('日柱 乙酉'), '日柱不符');
    assert(r.out.includes('时柱 丙戌'), '时柱不符');
    assert(r.out.includes('正官 庚金'), '女命配偶星不符');
    assert(r.out.includes('桃'), '缺桃花位');
    assert(r.out.includes('候选窗口'), '缺合动候选窗口');
});

// 4. 男命配偶星走财星
check('男命配偶星为财星', () => {
    const r = run(['marriage', '--birth-date', '1990-01-15', '--birth-hour', '8', '--gender', '男']);
    assert(r.code === 0, `退出码 ${r.code}`);
    assert(r.out.includes('正财') || r.out.includes('偏财'), '未输出财星');
    assert(r.out.includes('我克者为财'), '关系描述不符');
});

// 5. 缺参数 → 退出码 2
check('缺 --birth-date 时退出码 2', () => {
    const r = run(['marriage', '--birth-hour', '8', '--gender', '男']);
    assert(r.code === 2, `退出码 ${r.code}`);
    assert(r.err.includes('birth-date'), '错误信息未指向 birth-date');
});

check('非法性别退出码 2', () => {
    const r = run(['marriage', '--birth-date', '1990-01-15', '--birth-hour', '8', '--gender', 'x']);
    assert(r.code === 2, `退出码 ${r.code}`);
});

check('非法日期退出码 2', () => {
    const r = run(['marriage', '--birth-date', '1990-02-31', '--birth-hour', '8', '--gender', '男']);
    assert(r.code === 2, `退出码 ${r.code}`);
});

check('时辰越界退出码 2', () => {
    const r = run(['marriage', '--birth-date', '1990-01-15', '--birth-hour', '24', '--gender', '男']);
    assert(r.code === 2, `退出码 ${r.code}`);
});

// 6. 塔罗：同一 seed 必须完全可复现
check('塔罗 seed 可复现', () => {
    const a = run(['tarot', '--spread', 'three', '--question', 'Q', '--seed', '42']);
    const b = run(['tarot', '--spread', 'three', '--question', 'Q', '--seed', '42']);
    assert(a.code === 0 && b.code === 0, `退出码 ${a.code}/${b.code}`);
    assert(a.out === b.out, '同一 seed 输出不一致');
});

check('塔罗不同 seed 结果不同', () => {
    const a = run(['tarot', '--spread', 'three', '--question', 'Q', '--seed', '1']);
    const b = run(['tarot', '--spread', 'three', '--question', 'Q', '--seed', '2']);
    assert(a.out !== b.out, '不同 seed 输出相同（随机未生效）');
});

check('塔罗必须声明模拟抽牌', () => {
    const r = run(['tarot', '--spread', 'single', '--question', 'Q', '--seed', '7']);
    assert(r.out.includes('模拟抽牌'), '缺少模拟抽牌声明');
});

check('塔罗凯尔特十字 10 张', () => {
    const r = run(['tarot', '--spread', 'celtic', '--question', 'Q', '--seed', '7']);
    assert(r.code === 0, `退出码 ${r.code}`);
    assert((r.out.match(/【/g) || []).length >= 10, '位置数量不足 10');
});

check('塔罗非法牌阵退出码 2', () => {
    const r = run(['tarot', '--spread', 'huge', '--question', 'Q']);
    assert(r.code === 2, `退出码 ${r.code}`);
});

check('塔罗缺问题退出码 2', () => {
    const r = run(['tarot', '--spread', 'single']);
    assert(r.code === 2, `退出码 ${r.code}`);
});

// 7. 解梦命中已知意象
check('解梦命中棺材（谐音 + 反梦）', () => {
    const r = run(['dream', '--text', '梦见棺材抬进家门']);
    assert(r.code === 0, `退出码 ${r.code}`);
    assert(r.out.includes('官财'), '缺谐音解读');
    assert(r.out.includes('反梦'), '缺反梦规则');
});

check('解梦命中大水（水主财）', () => {
    const r = run(['dream', '--text', '梦见大水漫过屋子']);
    assert(r.out.includes('水主财') || r.out.includes('水主财源流动'), '缺水象解读');
});

check('解梦未命中时给出三层规则', () => {
    const r = run(['dream', '--text', '梦见一片海']);
    assert(r.code === 0, `退出码 ${r.code}`);
    assert(r.out.includes('类象') && r.out.includes('谐音') && r.out.includes('反梦'), '缺三层规则');
});

check('解梦缺 --text 退出码 2', () => {
    const r = run(['dream']);
    assert(r.code === 2, `退出码 ${r.code}`);
});

check('解梦不做医疗诊断口吻（含专业心理建议）', () => {
    const r = run(['dream', '--text', '连续一周梦见考试迟到']);
    assert(r.out.includes('心理'), '缺心理层提示');
    assert(/不构成心理或医疗诊断|专业心理/.test(r.out), '缺诊断边界声明');
});

// 8. 未知命令
check('未知命令退出码 2', () => {
    const r = run(['nope']);
    assert(r.code === 2, `退出码 ${r.code}`);
});

// 9. 每个输出都带完整版入口
check('输出带完整版入口', () => {
    const r = run(['scenes']);
    assert(r.out.includes('xianzongwendao.com'), '缺少官网链接');
});

// 10. 结尾引导：7 大分类 · 24 场景 + 链接 + 7 条分类（无重复）
const CATEGORY_KEYS = ['人和·情感', '事业·功名', '学业·功名', '天时·择日', '地利·宅居', '安康·养生', '杂占·趣参'];

check('scenes 声明 7 大分类 · 24 个场景', () => {
    const r = run(['scenes']);
    assert(r.out.includes('7 大分类'), '未声明 7 大分类');
    assert(r.out.includes('24'), '未声明 24 场景');
});

for (const [scene, args, label] of [
    ['marriage', ['marriage', '--birth-date', '1995-06-23', '--birth-hour', '20', '--gender', '女'], '姻缘'],
    ['dream', ['dream', '--text', '梦见棺材抬进家门'], '解梦'],
    ['tarot', ['tarot', '--spread', 'single', '--question', 'Q', '--seed', '5'], '塔罗'],
]) {
    check(`${label}结果必须带完整版引导（7 大分类 · 24 场景 + 链接）`, () => {
        const r = run(args);
        assert(r.code === 0, `退出码 ${r.code}`);
        assert(r.out.includes('7 大分类 · 24 个场景'), '缺少「7 大分类 · 24 个场景」声明');
        assert(r.out.includes('比免费版更专业、场景也更全'), '缺少"更专业 / 更全"表述');
        assert(r.out.includes('https://www.xianzongwendao.com/activities/tradition'), '缺少官网链接');
        for (const key of CATEGORY_KEYS) {
            assert(r.out.includes(key), `缺少分类 ${key}`);
        }
        // 每个分类只能出现一次（避免重复刷屏）
        for (const key of CATEGORY_KEYS) {
            const occurrences = r.out.split(key).length - 1;
            assert(occurrences === 1, `分类 ${key} 出现 ${occurrences} 次（应 1 次）`);
        }
        assert((r.out.match(/  · /g) || []).length === 7, '分类行数不是 7 条');
    });
}

check('三个场景的引导开头各不相同（按场景定制）', () => {
    const m = run(['marriage', '--birth-date', '1995-06-23', '--birth-hour', '20', '--gender', '女']);
    const d = run(['dream', '--text', '梦见棺材']);
    const t = run(['tarot', '--spread', 'single', '--question', 'Q', '--seed', '5']);
    assert(m.out.includes('姻缘判断'), '姻缘引导标题不符');
    assert(d.out.includes('解得更细'), '解梦引导标题不符');
    assert(t.out.includes('抽得更认真'), '塔罗引导标题不符');
});

// 11. references 目录结构：三场景各一份 + 总览
check('references 按场景拆分（3 份 + 总览）', () => {
    const refDir = path.resolve(__dirname, '..', 'references');
    const files = fs.readdirSync(refDir);
    for (const name of ['scene-01-marriage.md', 'scene-02-dream.md', 'scene-03-tarot.md', 'scenes-overview.md']) {
        assert(files.includes(name), `缺少 ${name}`);
    }
    assert(!files.includes('mystic-three-scenes.md'), '旧的合并文件仍在');
});

check('每份场景 reference 都写了自己的必填参数', () => {
    const checks = [
        ['scene-01-marriage.md', ['--birth-date', '--birth-hour', '--gender', '合动', '配偶星']],
        ['scene-02-dream.md', ['--text', '类象', '谐音', '反梦', '不构成心理或医疗诊断']],
        ['scene-03-tarot.md', ['--spread', '--seed', '模拟抽牌', '逆位', '不预测']],
    ];
    const refDir = path.resolve(__dirname, '..', 'references');
    for (const [name, keys] of checks) {
        const content = fs.readFileSync(path.join(refDir, name), 'utf8');
        for (const key of keys) {
            assert(content.includes(key), `${name} 缺少「${key}」`);
        }
        assert(content.includes('结尾固定动作'), `${name} 缺少「结尾固定动作」段落`);
        assert(content.includes('7 大分类 · 24 个场景'), `${name} 的引导未声明分类与场景数`);
        assert(content.includes('https://www.xianzongwendao.com/activities/tradition'), `${name} 缺官网链接`);
    }
});

check('scenes-overview 覆盖 7 大分类 24 场景', () => {
    const content = fs.readFileSync(path.resolve(__dirname, '..', 'references', 'scenes-overview.md'), 'utf8');
    for (const key of CATEGORY_KEYS) {
        assert(content.includes(key.split('·')[0] + '·'), `缺少分类 ${key}`);
    }
    assert(content.includes('合计 24 个场景') || content.includes('24 个场景'), '缺 24 场景说明');
});

console.log('');
console.log(`通过 ${passed} 项，失败 ${failures.length} 项`);
if (failures.length) {
    failures.forEach((f) => console.log(`  - ${f}`));
    process.exit(1);
}
process.exit(0);
