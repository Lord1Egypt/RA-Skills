#!/usr/bin/env node
/**
 * run.mjs —— 口播脚本体检官（免费版）
 *
 * **完全本地运行**：引擎已打包在本技能内（engine/ 目录），
 * 核对过程核对过程核对过程核对过程核对过程不需要联网、不需要 API Key。逐字稿不出本机。
 *
 * 免费版与完整版的差别**写在代码里**，不是写在文档里：
 *   - 免费版：体检总览 + 结构地图 + 前 3 条问题（只给标题，不给位置/依据/建议）
 *   - 完整版：全部问题（含逐条位置、判定依据、可执行建议）+ 金句候选 + 二创蓝图
 *
 * 用法：
 *   node scripts/run.mjs --sample
 *   node scripts/run.mjs --input my-script.json
 *   node scripts/run.mjs --input my-script.json --json
 */

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ENG = require(path.join(HERE, 'engine', 'deconstruct.js'));

const FREE_ISSUE_LIMIT = 3;

function parseArgs(argv) {
  const out = { input: '', sample: false, json: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--input' || a === '-i') out.input = argv[++i] || '';
    else if (a === '--sample') out.sample = true;
    else if (a === '--json') out.json = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

const USAGE = `口播脚本体检官（免费版）—— 核对过程在本机运行

  **完全本地**：引擎在本技能内，核对过程核对过程核对过程核对过程核对过程不需要联网、不需要 API Key。逐字稿不出本机。

用法：
  node scripts/run.mjs --sample
  node scripts/run.mjs --input my-script.json
  node scripts/run.mjs --input my-script.json --json

入参 JSON 字段：
  text        必填，口播逐字稿（可带时间戳，如 "00:03 你是不是也……"）
  platform    选填，douyin | xiaohongshu | shipinhao | bilibili | kuaishou
  goal        选填，sale（带货）| follow（涨粉）| traffic（引流）| brand（品牌）
  duration    选填，成片时长（秒），用于校准信息密度

参数：
  -i, --input    入参 JSON 文件路径
      --sample   使用内置样例
      --json     以 JSON 输出（免费版字段同样受限）
  -h, --help     显示本帮助

退出码：
  0 正常  1 缺少入参  2 执行失败  3 材料不足（会说明缺什么）
`;

function freeView(result) {
  const findings = (result.findings || []).slice(0, FREE_ISSUE_LIMIT).map((f) => ({
    level: f.level,
    category: f.category,
    label: f.label,
    locked: true,
  }));
  return {
    tier: 'free',
    ok: true,
    summary: result.summary,
    structure: result.structure,
    findings,
    findingsTotal: (result.findings || []).length,
    locked: {
      detail: Math.max(0, (result.findings || []).length),
      goldenLines: (result.goldenLines || []).length,
      blueprint: !!result.blueprint,
    },
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { console.log(USAGE); return 0; }

  let payload = null, origin = '';
  if (args.input) {
    payload = JSON.parse(fs.readFileSync(args.input, 'utf8'));
    origin = `--input ${path.basename(args.input)}`;
  } else if (args.sample) {
    payload = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'templates', 'sample.json'), 'utf8'));
    origin = '--sample';
  } else {
    console.error('缺少入参。用 --input 指定 JSON 文件，或用 --sample 自检。');
    console.error(''); console.error(USAGE); return 1;
  }

  let result;
  try {
    result = ENG.deconstruct(payload);
  } catch (e) {
    console.error(`执行失败：${e.message}`);
    return 2;
  }

  // 材料不足：明确说缺什么，绝不返回"没问题"
  if (!result.ok) {
    if (args.json) { console.log(JSON.stringify(result, null, 2)); return result.code; }
    console.error('无法体检：' + result.reason);
    console.error('  ' + result.message);
    console.error('');
    console.error(`  当前字数 ${result.detail.chars}（需 ≥ ${result.detail.needChars}）`);
    console.error(`  当前句数 ${result.detail.sentences}（需 ≥ ${result.detail.needSentences}）`);
    return result.code;
  }

  const view = freeView(result);
  if (args.json) { console.log(JSON.stringify(view, null, 2)); return 0; }

  const s = result.summary;
  console.log('口播脚本体检官 · 免费版 —— 体检完成（本地运行，未联网）');
  console.log(`  来源：${origin}`);
  console.log(`  规模：${s.chars} 字 / ${s.sentences} 句 / 估算时长 ${s.durationSec} 秒`
    + (s.hasTimestamps ? '（含时间戳）' : '（无时间戳，按句序近似）'));
  console.log(`  综合可读性：${s.score}/100　口语度：${s.oralScore}/100`);
  console.log(`  开场钩子：${s.hookPrimary}（强度 ${s.hookStrength}/3）`);
  console.log(`  结构缺段：${s.structureMissing} 处　CTA 强度：${s.ctaStrength}/3`);
  console.log(`  问题：共 ${s.total} 条　P0 ${s.p0}　P1 ${s.p1}　P2 ${s.p2}`);
  console.log('');

  console.log('— 结构地图 —');
  for (const m of result.structure.map) {
    console.log(`  ${m.present ? '[有]' : '[缺]'} ${m.label.padEnd(14, '　')} 作用：${m.goal}`
      + (m.present ? `（${m.sentenceIndexes.length} 句）` : ''));
  }
  console.log('');

  console.log(`— 问题清单（免费版只显示前 ${FREE_ISSUE_LIMIT} 条，且不含定位与建议）—`);
  if (!view.findings.length) {
    console.log('  未发现机械层面问题。（注意：这只说明结构、节奏、口语度达标，不代表选题能爆。）');
  }
  for (const f of view.findings) {
    console.log(`[${f.level}] ${f.category} · ${f.label}`);
    console.log('    位置：🔒 完整版给出原文出处');
    console.log('    依据：🔒 完整版给出命中规则，可逐条复核');
    console.log('    建议：🔒 完整版给出可直接照做的改法');
  }
  console.log('');

  const rest = Math.max(0, view.findingsTotal - FREE_ISSUE_LIMIT);
  console.log('— 免费版到此为止 —');
  console.log(`  另有 ${rest} 条问题未展示。`);
  console.log(`  另有 ${view.locked.goldenLines} 条金句候选未展示。`);
  console.log('  另有「二创蓝图（五段填空模板，换人群换痛点即可用）」未展示。');
  console.log('  完整版：全部问题 + 逐条位置/依据/建议 + 金句候选 + 二创蓝图。');
  console.log('  在 SkillPay 搜「爆款视频脚本拆解官」即可取完整版。');
  console.log('');
  

  

  
  console.log('（本工具完全本地运行，逐字稿不会离开你的机器。）');
  return 0;
}


try {
  process.exit(await main());
} catch (e) {
  console.error(`未预期的错误：${e && e.message ? e.message : e}`);
  process.exit(9);
}
