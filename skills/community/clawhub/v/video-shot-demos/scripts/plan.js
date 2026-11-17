#!/usr/bin/env node
/* plan.js —— 风格分配草表生成与校验（第 0 步工具化）
   解决缺口②④：风格分配表纯人工、相邻不同风格/整辑不重复/实体锁色靠人脑。
   用法:
     node scripts/plan.js new  <镜头清单.json>              # 生成分配草表(保存 <清单同名>.plan.json)
     node scripts/plan.js check <plan.json>                  # 校验相邻不同风格/整辑不重复/锁色冲突
   镜头清单.json 格式:
     { "project": "my-project", "ananSource": "glm-5.3-range-test",
       "shots": [ {"id":"0-1","title":"两周2436个漏洞","dur":14,"brief":"震撼数字 事件宣告"},
                  {"id":"0-2","title":"CyberGym是什么","dur":12,"brief":"新概念科普"} ],
       "locks": [ {"entity":"GLM","color":"#2dd4ee"} ] }     // locks 可省略，默认用 styles.json 内置锁色
   brief 为内容关键词（空格分隔），用于匹配风格卡 fit 标签；匹配不上的镜头按未用风格轮转补位。 */
const fs = require('fs'), path = require('path');
const DB = JSON.parse(fs.readFileSync(path.join(__dirname, 'styles.json'), 'utf8'));

function die(msg) { console.error('✗ ' + msg); process.exit(1); }
function loadJSON(p) {
  const f = path.resolve(p);
  if (!fs.existsSync(f)) die('文件不存在: ' + f);
  try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) { die('JSON 解析失败: ' + f + ' -> ' + e.message); }
}

/* ---------- 分配核心 ---------- */
function scoreFit(brief, style) {
  const kw = String(brief || '').split(/[\s,，、/]+/).filter(Boolean);
  let s = 0;
  for (const k of kw) for (const f of style.fit) if (k && (k.includes(f) || f.includes(k))) s += 2;
  return s;
}
function pickStyles(shots) {
  const used = new Set(), assign = [];
  shots.forEach((shot, i) => {
    const scored = DB.styles
      .map(st => ({ st, sc: scoreFit(shot.brief, st) }))
      .sort((a, b) => b.sc - a.sc);
    let choice = null;
    // 优先：有匹配分 & 未用 & 与相邻不同
    for (const c of scored) {
      if (c.sc > 0 && !used.has(c.st.name) && c.st.name !== (assign[i - 1] || {}).style) { choice = c.st; break; }
    }
    // 次选：零分但未用且与相邻不同（按序轮转）
    if (!choice) {
      const start = used.size % DB.styles.length;
      for (let k = 0; k < DB.styles.length; k++) {
        const st = DB.styles[(start + k) % DB.styles.length];
        if (!used.has(st.name) && st.name !== (assign[i - 1] || {}).style) { choice = st; break; }
      }
    }
    // 兜底：风格池耗尽（>40 镜头），允许复用但避开相邻
    if (!choice) {
      for (const st of DB.styles) if (st.name !== (assign[i - 1] || {}).style) { choice = st; break; }
    }
    used.add(choice.name);
    assign.push({ id: shot.id, title: shot.title, dur: shot.dur, brief: shot.brief, style: choice.name, series: choice.series, sample: choice.sample, samplePath: choice.samplePath, fonts: choice.fonts, palette: choice.palette });
  });
  return assign;
}

/* ---------- 校验核心（new/check 共用） ---------- */
function verify(plan) {
  const errs = [], warns = [], infos = [];
  const rows = plan.assign || plan.shots || [];
  if (!rows.length) errs.push('没有任何镜头条目');
  const names = rows.map(r => r.style).filter(Boolean);
  rows.forEach((r, i) => {
    if (!r.style) { errs.push(`镜头 ${r.id}: 未分配风格`); return; }
    if (!DB.styles.some(s => s.name === r.style)) errs.push(`镜头 ${r.id}: 风格「${r.style}」不在 40 风格库中`);
    if (i > 0 && r.style === rows[i - 1].style) errs.push(`镜头 ${r.id} 与 ${rows[i - 1].id} 相邻同风格「${r.style}」`);
    if (!r.dur || r.dur <= 0) errs.push(`镜头 ${r.id}: 时长缺失或非法`);
    else if (r.dur > 100) warns.push(`镜头 ${r.id}: DUR=${r.dur}s 超长页，角色需 3 次出场（SKILL 交付标准）`);
    else if (r.dur < 10) warns.push(`镜头 ${r.id}: DUR=${r.dur}s 短页，角色仅结尾 1 次定场即可`);
  });
  const dup = names.filter((n, i) => names.indexOf(n) !== i);
  if (dup.length) warns.push('整辑重复风格: ' + [...new Set(dup)].join('、') + '（风格池 40 种，镜头数超限或匹配冲突）');
  else infos.push(`整辑 ${names.length} 镜头风格零重复 ✓`);
  // 锁色：实体名重复但颜色不一致
  const locks = plan.locks || DB.locks;
  const byEnt = {};
  for (const l of locks) {
    const key = l.entity.trim();
    if (byEnt[key] && byEnt[key].toLowerCase() !== l.color.toLowerCase())
      errs.push(`实体「${key}」锁色冲突: ${byEnt[key]} vs ${l.color}`);
    byEnt[key] = l.color;
  }
  // brief 提到实体但未声明锁色
  const briefAll = rows.map(r => r.brief || '').join(' ');
  for (const ent of Object.keys(byEnt)) if (briefAll.includes(ent)) infos.push(`实体锁色已声明: ${ent} = ${byEnt[ent]}（相关页面必须使用该色）`);
  return { errs, warns, infos };
}

function printReport(v, label) {
  console.log(`\n===== 校验报告: ${label} =====`);
  v.infos.forEach(m => console.log('  ✓ ' + m));
  v.warns.forEach(m => console.log('  ⚠ ' + m));
  v.errs.forEach(m => console.log('  ✗ ' + m));
  console.log(`  小计: ${v.infos.length} 通过 / ${v.warns.length} 警告 / ${v.errs.length} 错误`);
}

function mdTable(assign) {
  const lines = ['| 镜头 | 时长 | 风格 | 字体组合 | 主色/材质 |', '|---|---|---|---|---|'];
  for (const a of assign) lines.push(`| ${a.id} | ${a.dur}s | ${a.style} | ${a.fonts} | ${a.palette} |`);
  return lines.join('\n');
}

/* ---------- CLI ---------- */
const [, , cmd, arg] = process.argv;
if (cmd === 'new') {
  if (!arg) die('用法: node scripts/plan.js new <镜头清单.json>');
  const input = loadJSON(arg);
  if (!input.project) die('清单缺少 project 字段');
  if (!Array.isArray(input.shots) || !input.shots.length) die('清单缺少 shots 数组');
  const assign = pickStyles(input.shots);
  const plan = {
    _format: 'video-shot-demos/plan v1（plan.js 生成，init.js / lint.js / gen-index.js 消费）',
    project: input.project,
    ananSource: input.ananSource || 'glm-5.3-range-test',
    locks: input.locks && input.locks.length ? input.locks : DB.locks,
    generatedAt: new Date().toISOString(),
    assign
  };
  const v = verify(plan);
  console.log(`\n项目「${plan.project}」风格分配草表（${assign.length} 镜头 / 风格池 ${DB.styles.length} 种）：\n`);
  console.log(mdTable(assign));
  console.log('\n锁色声明: ' + plan.locks.map(l => `${l.entity}=${l.color}`).join('，'));
  printReport(v, '草表自检');
  const out = path.resolve(arg).replace(/\.json$/i, '') + '.plan.json';
  fs.writeFileSync(out, JSON.stringify(plan, null, 2), 'utf8');
  console.log(`\n已保存: ${out}\n下一步: node scripts/init.js ${out} --root <输出根目录>`);
  process.exit(v.errs.length ? 1 : 0);
} else if (cmd === 'check') {
  if (!arg) die('用法: node scripts/plan.js check <plan.json>');
  const plan = loadJSON(arg);
  const v = verify(plan);
  printReport(v, arg);
  process.exit(v.errs.length ? 1 : 0);
} else {
  console.log('用法:\n  node scripts/plan.js new  <镜头清单.json>   生成风格分配草表\n  node scripts/plan.js check <plan.json>       校验已有分配表\n镜头清单 JSON 格式见本文件头部注释。');
}
