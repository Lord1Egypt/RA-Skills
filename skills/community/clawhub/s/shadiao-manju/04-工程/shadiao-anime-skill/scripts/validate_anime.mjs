#!/usr/bin/env node
/**
 * .anime 工程校验（v0.1）
 *
 * 用法：
 *   node validate_anime.mjs <path/to/xxx.anime>
 *   node validate_anime.mjs <path/to/xxx.anime> --report 校验报告.md
 */

import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { parseArgs } from './lib/project.mjs';

const args = parseArgs(process.argv.slice(2));
const animePath = resolve(args._[0] || args.path || '');
if (!animePath || !existsSync(animePath)) {
  console.error('用法：node validate_anime.mjs <path/to/xxx.anime> [--report 报告.md]');
  process.exit(2);
}

const projectRoot = dirname(animePath);
const errors = [];
const warnings = [];
const infos = [];

const err = (m) => errors.push(m);
const warn = (m) => warnings.push(m);
const info = (m) => infos.push(m);

let anime;
try {
  anime = JSON.parse(readFileSync(animePath, 'utf8'));
} catch (e) {
  console.error(`✗ JSON 解析失败：${e.message}`);
  process.exit(1);
}

const ids = new Map();
function checkId(id, where) {
  if (!id) { err(`${where} 缺 id`); return; }
  if (ids.has(id)) err(`重复 id：${id}（${ids.get(id)} / ${where}）`);
  else ids.set(id, where);
}

// ---------- 顶层 ----------
for (const key of ['meta', 'assets', 'actors', 'narrator', 'compositeCharacters', 'episodes']) {
  if (!(key in anime)) err(`顶层缺少字段：${key}`);
}
if (!anime.meta?.resolution?.w || !anime.meta?.resolution?.h) {
  err('meta.resolution 不完整');
} else {
  info(`画布 ${anime.meta.resolution.w}×${anime.meta.resolution.h} @ ${anime.meta.fps || '?'}fps`);
}

const bgIds = new Set((anime.assets?.backgrounds || []).map((b) => b.id));
const propIds = new Set((anime.assets?.props || []).map((p) => p.id));
const charIds = new Set((anime.compositeCharacters || []).map((c) => c.id));
const actorIds = new Set((anime.actors || []).map((a) => a.id));
const exprIds = new Set(Object.keys(anime.expressions || {}));
const materialIds = new Set();
for (const c of anime.compositeCharacters || []) {
  for (const o of c.objects || []) {
    if (o.type === 'symbol') for (const m of o.materials || []) materialIds.add(m.id);
  }
}

info(`角色 ${anime.actors?.length || 0} 个 / 角色模板 ${anime.compositeCharacters?.length || 0} 个 / 背景 ${bgIds.size} 张 / 表情 ${exprIds.size} 个`);

// ---------- 表情 ----------
for (const [id, expr] of Object.entries(anime.expressions || {})) {
  if (expr.id && expr.id !== id) err(`表情 key 与 id 不一致：${id} / ${expr.id}`);
  const url = expr.defaultFrame?.url;
  if (!url) err(`表情「${expr.name || id}」缺 defaultFrame.url`);
  else if (!existsSync(join(projectRoot, url))) err(`表情「${expr.name || id}」图片不存在：${url}`);
}

// ---------- 角色模板 ----------
for (const c of anime.compositeCharacters || []) {
  checkId(c.id, `角色模板 ${c.name}`);
  if (!c.rootCompositeId) err(`角色模板「${c.name}」缺 rootCompositeId`);
  const root = (c.objects || []).find((o) => o.id === c.rootCompositeId);
  if (!root) err(`角色模板「${c.name}」的 rootCompositeId 不在 objects 里`);
  else if (root.type !== 'composite') err(`角色模板「${c.name}」的根不是 composite`);

  for (const obj of c.objects || []) {
    checkId(obj.id, `角色模板「${c.name}」对象 ${obj.name || obj.type}`);
    if (obj.type === 'symbol') {
      const mats = obj.materials || [];
      if (!mats.length) err(`角色「${c.name}」的 symbol 没有 materials`);
      for (const mat of mats) {
        if (mat.url) {
          const p = join(projectRoot, mat.url);
          if (!existsSync(p)) err(`角色「${c.name}」图片不存在：${mat.url}`);
        } else {
          err(`角色「${c.name}」的 material「${mat.name || mat.id}」没有 url`);
        }
      }
      if (!mats.some((m) => m.id === obj.currentMaterialId)) {
        err(`角色「${c.name}」的 currentMaterialId 不在 materials 里`);
      }
    }
  }
}

// ---------- 演员 ----------
const voiceIds = new Set();
for (const a of anime.actors || []) {
  checkId(a.id, `演员 ${a.name}`);
  if (!charIds.has(a.characterId)) err(`演员「${a.name}」的 characterId 不存在`);
  const vid = a.voice?.voiceId;
  if (vid !== undefined && vid !== null && vid !== '') {
    if (voiceIds.has(String(vid))) warn(`voiceId 重复：${vid}（${a.name}）`);
    voiceIds.add(String(vid));
  } else {
    warn(`演员「${a.name}」没有 voiceId`);
  }
}

// ---------- 集 / 场景 / 块 ----------
if (!anime.episodes?.length) err('没有任何 episode');

let totalBlocks = 0;
let totalMs = 0;
const audioPaths = new Map();

for (const ep of anime.episodes || []) {
  checkId(ep.id, `集 ${ep.name}`);
  if (!ep.scenes?.length) err(`第 ${ep.episodeNumber} 集没有场景`);
  for (const scene of ep.scenes || []) {
    checkId(scene.id, `场景 ${scene.title}`);
    if (scene.type !== 'scene_container') err(`场景「${scene.title}」type 不是 scene_container`);
    const setup = scene.setup || {};
    if (!setup.camera) err(`场景「${scene.title}」缺 camera`);
    if (!Array.isArray(setup.objects)) { err(`场景「${scene.title}」缺 objects`); continue; }
    if (!Array.isArray(setup.renderChain)) err(`场景「${scene.title}」缺 renderChain`);

    const objIds = new Set(setup.objects.map((o) => o.id));
    for (const oid of setup.renderChain || []) {
      if (!objIds.has(oid)) err(`场景「${scene.title}」renderChain 指向不存在的对象：${oid}`);
    }

    for (const obj of setup.objects) {
      checkId(obj.id, `场景「${scene.title}」对象 ${obj.name || obj.type}`);
      if (obj.type === 'background' && !bgIds.has(obj.refId)) {
        err(`场景「${scene.title}」背景 refId 不存在：${obj.refId}`);
      }
      if (obj.type === 'prop' && !propIds.has(obj.refId)) {
        err(`场景「${scene.title}」道具 refId 不存在：${obj.refId}`);
      }
      if (obj.type === 'composite') {
        const actorId = obj.extraInfo?.actorId;
        if (actorId && !actorIds.has(actorId)) err(`场景对象「${obj.name}」的 actorId 不存在：${actorId}`);
      }
      if (obj.type === 'expression') {
        if (!exprIds.has(obj.refId)) err(`表情对象「${obj.name}」的 refId 不存在：${obj.refId}`);
        if (obj.defaultRefId && !exprIds.has(obj.defaultRefId)) err(`表情对象「${obj.name}」的 defaultRefId 不存在：${obj.defaultRefId}`);
      }
    }

    if (!setup.objects.some((o) => o.type === 'background')) {
      warn(`场景「${scene.title}」没有背景对象`);
    }
    if (!setup.objects.some((o) => o.type === 'light')) {
      warn(`场景「${scene.title}」没有环境光`);
    }

    if (!scene.script?.length) err(`场景「${scene.title}」没有脚本块`);
    for (const block of scene.script || []) {
      totalBlocks++;
      checkId(block.id, `脚本块 ${block.type}`);
      if (!block.text) err(`脚本块 ${block.id} 没有 text`);
      if (!['dialogue', 'narration', 'action'].includes(block.type)) {
        err(`脚本块 ${block.id} type 非法：${block.type}`);
      }
      const tts = block.ttsConfig;
      if (!tts) {
        err(`脚本块 ${block.id} 缺 ttsConfig`);
      } else {
        if (!(Number(tts.duration) > 0)) err(`脚本块 ${block.id} duration 非法：${tts.duration}`);
        else totalMs += Number(tts.duration);
        if (!tts.audioPath) {
          err(`脚本块 ${block.id} 缺 audioPath`);
        } else {
          const p = join(projectRoot, tts.audioPath);
          if (!existsSync(p)) err(`脚本块 ${block.id} 音频不存在：${tts.audioPath}`);
          const prev = audioPaths.get(tts.audioPath);
          if (prev && prev !== block.id) warn(`audioPath 被多个块复用：${tts.audioPath}`);
          else audioPaths.set(tts.audioPath, block.id);
        }
      }
      if (block.type === 'dialogue') {
        if (!block.instanceId) err(`对话块 ${block.id} 缺 instanceId`);
        else if (!objIds.has(block.instanceId)) err(`对话块 ${block.id} 的 instanceId 不在场景对象里：${block.instanceId}`);
      }
      for (const action of block.actions || []) {
        if (action.type === 'camera_follow') {
          const target = action.params?.followTarget;
          if (target && !objIds.has(target)) err(`动作 ${action.id} 跟随目标不存在：${target}`);
        }
        if (action.type === 'set_material') {
          if (!objIds.has(action.target)) err(`动作 ${action.id} 目标不存在：${action.target}`);
          const materialId = action.params?.materialId;
          if (materialId && !exprIds.has(materialId) && !materialIds.has(materialId)) {
            err(`动作 ${action.id} 的 materialId 不存在：${materialId}`);
          }
        }
      }
      if (!(block.actions || []).length) warn(`脚本块 ${block.id} 没有动作（会显得很静）`);
    }
  }
}

if (totalMs > 0) info(`总时长 ${(totalMs / 1000).toFixed(1)}s / 脚本块 ${totalBlocks} 条`);

// ---------- 输出 ----------
console.log('');
console.log(`校验：${animePath}`);
console.log('-'.repeat(52));
for (const m of infos) console.log(`  · ${m}`);
for (const m of warnings) console.log(`  ! ${m}`);
for (const m of errors) console.log(`  ✗ ${m}`);
console.log('');
const passed = errors.length === 0;
console.log(passed
  ? `结果：通过${warnings.length ? `（${warnings.length} 个警告）` : ''}`
  : `结果：不通过（${errors.length} 个错误，${warnings.length} 个警告）`);

if (args.report) {
  const lines = [
    '# 工程校验报告',
    '',
    `- 工程：\`${animePath}\``,
    `- 时间：${new Date().toLocaleString()}`,
    `- 结果：${passed ? '通过' : '不通过'}`,
    `- 错误：${errors.length} / 警告：${warnings.length}`,
    '',
    '## 概况',
    '',
    ...infos.map((m) => `- ${m}`),
    '',
    '## 错误',
    '',
    ...(errors.length ? errors.map((m) => `- ✗ ${m}`) : ['- 无']),
    '',
    '## 警告',
    '',
    ...(warnings.length ? warnings.map((m) => `- ! ${m}`) : ['- 无']),
    '',
  ];
  const reportPath = resolve(args.report);
  writeFileSync(reportPath, lines.join('\n'), 'utf8');
  console.log(`报告：${reportPath}`);
}

process.exit(passed ? 0 : 1);
