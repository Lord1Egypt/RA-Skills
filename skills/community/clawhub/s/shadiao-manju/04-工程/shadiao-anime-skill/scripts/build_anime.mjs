#!/usr/bin/env node
/**
 * 剧本 + 配音 + 素材 → .anime 工程（v0.1）
 *
 * 用法：
 *   node build_anime.mjs --project 周一打工人 --season 1 --episode 1
 *   node build_anime.mjs --project 周一打工人 --season 1 --episode 1 --width 1080 --height 1920
 *
 * 输入：
 *   99-项目/<剧名>/第NN季/01-剧本/剧本.json
 *   99-项目/<剧名>/第NN季/02-配音/第NN集/配音表.json
 *   99-项目/<剧名>/第NN季/03-素材/素材索引.json
 * 输出：
 *   99-项目/<剧名>/第NN季/04-工程/<剧名>.anime
 *   99-项目/<剧名>/第NN季/04-工程/<剧名>_cache/{tts,assets}/
 */

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { basename, dirname, extname, join, resolve } from 'node:path';
import { parseArgs, readJson, safeJoin, seasonDir, writeJson } from './lib/project.mjs';
import { imageSize } from './lib/media.mjs';
import {
  genId,
  instantiateCharacter,
  makeBackgroundObject,
  makeCamera,
  makeCameraFollow,
  makeCharacter,
  makeDialogueBlock,
  makeEpisode,
  makeLight,
  makeNarrationBlock,
  makeProject,
  makePropObject,
  makeScene,
  makeSetMaterial,
  makeCameraShake,
  makeCameraMove,
  makeTweenTransform,
  makeSetTransform,
  makeSetVisual,
  makeSetAnim,
  makeTalkAnimation,
} from './lib/anime.mjs';

const args = parseArgs(process.argv.slice(2));

// 路径越界 / 输入不合法这类错误，只打一行说明，不要甩一屏堆栈
process.on('uncaughtException', (e) => {
  console.error(`✗ ${e?.message || e}`);
  process.exit(2);
});

const project = typeof args.project === 'string' ? args.project : '';
if (!project) {
  console.error('用法：node build_anime.mjs --project <剧名> [--season 1] [--episode 1]');
  process.exit(2);
}

const season = Number(args.season ?? 1);
const episode = Number(args.episode ?? 1);
if (!Number.isInteger(season) || season < 1 || season > 99) {
  console.error(`✗ --season 必须是 1–99 的整数，实际是 ${args.season}`);
  process.exit(2);
}
if (!Number.isInteger(episode) || episode < 1 || episode > 99) {
  console.error(`✗ --episode 必须是 1–99 的整数，实际是 ${args.episode}`);
  process.exit(2);
}

let sd;
try {
  sd = seasonDir(project, season);
} catch (e) {
  console.error(`✗ ${e.message}`);
  process.exit(2);
}

const scriptPath = args.script ? resolve(args.script) : join(sd, '01-剧本', '剧本.json');
const voicePath = args.voice ? resolve(args.voice) : join(sd, '02-配音', `第${String(episode).padStart(2, '0')}集`, '配音表.json');
const assetsPath = args.assets ? resolve(args.assets) : join(sd, '03-素材', '素材索引.json');

const script = readJson(scriptPath);

if (!existsSync(voicePath)) {
  console.error(`✗ 找不到配音表：${voicePath}`);
  console.error(`  先跑：python3 02-配音/shadiao-voice-skill/scripts/tts_batch.py --project ${project} --season ${season} --episode ${episode}`);
  process.exit(1);
}
if (!existsSync(assetsPath)) {
  console.error(`✗ 找不到素材索引：${assetsPath}`);
  console.error('  先出素材并跑：python3 03-素材/shadiao-asset-skill/scripts/make_index.py --season-dir <季目录>');
  process.exit(1);
}

const voiceManifest = readJson(voicePath);
const assetsIndex = readJson(assetsPath);

const aspect = script.aspectRatio || '9:16';
const [aw, ah] = aspect.split(':').map(Number);
const W = Number(args.width) || (ah > aw ? 1080 : 1920);
const H = Number(args.height) || (ah > aw ? 1920 : 1080);
const FPS = Number(args.fps) || 30;

const outDir = args.out ? dirname(resolve(args.out)) : join(sd, '04-工程');
const animeName = args.out ? basename(resolve(args.out)) : `${project}.anime`;
const animePath = join(outDir, animeName);
const animeBase = animeName.replace(/\.anime$/i, '');
const cacheDirName = `${animeBase}_cache`;
const cacheDir = join(outDir, cacheDirName);
mkdirSync(join(cacheDir, 'tts'), { recursive: true });
mkdirSync(join(cacheDir, 'assets', 'characters'), { recursive: true });
mkdirSync(join(cacheDir, 'assets', 'backgrounds'), { recursive: true });
mkdirSync(join(cacheDir, 'assets', 'props'), { recursive: true });

const EXPRESSION_NAMES = ['平静', '开心', '愤怒', '悲伤', '惊讶', '无语', '得意', '崩溃'];
const EMOTION_TO_EXPRESSION = {
  平静: '平静', 中性: '平静', 温柔: '平静', 慵懒: '平静',
  开心: '开心', 喜悦: '开心', 高兴: '开心', 惊喜: '开心',
  愤怒: '愤怒', 暴怒: '愤怒', 生气: '愤怒', 抓狂: '愤怒',
  悲伤: '悲伤', 低落: '悲伤', 哽咽: '悲伤', 哭腔: '悲伤', 委屈: '悲伤',
  惊讶: '惊讶', 震惊: '惊讶', 惊恐: '惊讶', 害怕: '惊讶',
  无语: '无语', 无奈: '无语', 尴尬: '无语', 敷衍: '无语', 摆烂: '无语', 疑惑: '无语', 质疑: '无语', 纳闷: '无语',
  得意: '得意', 厌恶: '得意', 嘲讽: '得意', 冷笑: '得意', 嫌弃: '得意',
  崩溃: '崩溃', 社死: '崩溃', 心虚: '崩溃',
};
function emotionToExpression(emotion) {
  return EMOTION_TO_EXPRESSION[emotion] || '平静';
}

const warnings = [];
const warn = (m) => { warnings.push(m); console.warn(`  ! ${m}`); };

// ---------- 1. 工程骨架 ----------
const anime = makeProject({ name: script.title || project, width: W, height: H, fps: FPS });
anime.episodes = [];

// ---------- 2. 素材登记 + 拷贝 ----------
const assetByName = new Map();
for (const c of assetsIndex.characters || []) assetByName.set(c.name, c);
const bgByName = new Map();
for (const b of assetsIndex.backgrounds || []) bgByName.set(b.name, b);
const propByName = new Map();
for (const p of assetsIndex.props || []) propByName.set(p.name, p);

function copyAsset(srcRel, subdir, name) {
  const src = safeJoin(sd, '03-素材', srcRel);
  if (!existsSync(src)) {
    warn(`素材不存在：${src}`);
    return null;
  }
  const ext = extname(src).toLowerCase() || '.png';
  const safe = String(name).replace(/[\\/:*?"<>|]/g, '_');
  const dst = join(cacheDir, 'assets', subdir, `${safe}${ext}`);
  copyFileSync(src, dst);
  return {
    abs: dst,
    rel: `${cacheDirName}/assets/${subdir}/${safe}${ext}`,
  };
}

// 背景
for (const bg of assetsIndex.backgrounds || []) {
  const copied = copyAsset(bg.file, 'backgrounds', bg.name);
  if (!copied) continue;
  const size = imageSize(copied.abs);
  anime.assets.backgrounds.push({
    id: genId('bgasset_'),
    name: bg.name,
    type: 'static',
    url: copied.rel,
    createdAt: Date.now(),
  });
  bg.assetId = anime.assets.backgrounds.at(-1).id;
  bg.width = size.width;
  bg.height = size.height;
}

// 道具
for (const p of assetsIndex.props || []) {
  const copied = copyAsset(p.file, 'props', p.name);
  if (!copied) continue;
  const size = imageSize(copied.abs);
  anime.assets.props.push({
    id: genId('propasset_'),
    name: p.name,
    type: 'static',
    url: copied.rel,
    createdAt: Date.now(),
  });
  p.assetId = anime.assets.props.at(-1).id;
  p.width = size.width;
  p.height = size.height;
}

// ---------- 3. 角色 + 演员 ----------
const VOICE_POOL = {
  male: [502005, 502006, 501007, 603000, 603003],
  female: [502001, 502003, 501001, 603001, 603004],
  other: [502001],
  child: [603002],
};
const usedVoice = new Set([101026]);
const actorByName = new Map();
const characterByName = new Map();
const characterExpression = new Map();

/**
 * 把 mouth.json 里的归一化嘴位换算成「角色根节点本地坐标 + 缩放」
 * 角色根节点与整身图同尺寸，本地 (0,0) 即图片中心。
 */
function mouthTransform(info, poseName) {
  const m = info?.map?.[poseName];
  if (!m) return null;
  const sp = info.map._sprite || {};
  const shapeW = Number(sp.mouthW) || 108;
  const shapeH = Number(sp.mouthH) || 84;
  const closedH = Number(sp.closedHeight) || 7;
  const cw = info.charW;
  const ch = info.charH;
  return {
    x: (m.x - 0.5) * cw,
    y: (m.y - 0.5) * ch,
    scaleX: (m.w * cw) / shapeW,
    scaleY: closedH / shapeH,
  };
}

function pickVoiceId(gender, presetName = '') {
  const isChild = /童|熊孩子|萌娃/.test(presetName);
  const pool = isChild ? VOICE_POOL.child : VOICE_POOL[gender] || VOICE_POOL.other;
  for (const id of pool) {
    if (!usedVoice.has(id)) { usedVoice.add(id); return id; }
  }
  const fallback = (VOICE_POOL[gender] || VOICE_POOL.other)[0];
  return fallback;
}

anime.narrator = { voice: { voiceId: 101026, speed: 0 } };

for (const c of script.characters || []) {
  const asset = assetByName.get(c.name);
  if (!asset) {
    warn(`角色「${c.name}」没有素材目录（03-素材/角色/${c.name}/），已跳过`);
    continue;
  }
  if (!asset.body) {
    warn(`角色「${c.name}」缺 body.png，已跳过`);
    continue;
  }
  const srcBody = safeJoin(sd, '03-素材', asset.body);
  if (!existsSync(srcBody)) {
    warn(`角色「${c.name}」body 不存在：${srcBody}，已跳过`);
    continue;
  }
  const charDir = String(c.name).replace(/[\\/:*?"<>|]/g, '_');
  const dstDir = join(cacheDir, 'assets', 'characters', charDir);
  mkdirSync(dstDir, { recursive: true });
  const dst = join(dstDir, `body${extname(asset.body).toLowerCase() || '.png'}`);
  copyFileSync(safeJoin(sd, '03-素材', asset.body), dst);
  const rel = `${cacheDirName}/assets/characters/${charDir}/body${extname(asset.body).toLowerCase() || '.png'}`;
  const size = imageSize(dst);
  const characterId = genId('char_');
  // v0.4：优先用「整身表情图」（8 个 material），没有才退回「表情贴脸」
  const fullBodies = [];
  const fullByEmotion = new Map();
  for (const emo of Object.keys(asset.fullBodies || {})) {
    const relFile = asset.fullBodies?.[emo];
    if (!relFile) continue;
    const src = safeJoin(sd, '03-素材', relFile);
    if (!existsSync(src)) continue;
    const dst = join(dstDir, `full_${emo}.png`);
    copyFileSync(src, dst);
    const matId = genId('mat_');
    fullBodies.push({ name: emo, url: `${cacheDirName}/assets/characters/${charDir}/full_${emo}.png`, id: matId });
    fullByEmotion.set(emo, matId);
  }

  const exprList = [];
  const exprByEmotion = new Map();
  if (!fullBodies.length) for (const emo of EXPRESSION_NAMES) {
    const relFile = asset.expressions?.[emo];
    if (!relFile) continue;
    const src = safeJoin(sd, '03-素材', relFile);
    if (!existsSync(src)) continue;
    const dst = join(dstDir, `exp_${emo}.png`);
    copyFileSync(src, dst);
    const exprId = genId('expr_');
    anime.expressions[exprId] = {
      id: exprId,
      name: `${c.name}_${emo}`,
      tags: [c.name, emo],
      gender: c.gender || asset.gender || 'other',
      defaultFrame: {
        id: genId('frame_'),
        url: `${cacheDirName}/assets/characters/${charDir}/exp_${emo}.png`,
      },
      speakingFrames: [],
      anchor: { x: 0.5, y: 0.5 },
      speakingFps: 12,
      speakingLoop: true,
      flipHorizontal: false,
      defaultScale: Number(asset.face?.scale ?? 0.6),
      createdAt: Date.now(),
    };
    exprList.push({ name: emo, id: exprId });
    exprByEmotion.set(emo, exprId);
  }

  // v0.6：嘴叠加层资源（03-素材/角色/<角色>/mouth.png + mouth.json）
  let mouth = null;
  const mouthJsonPath = safeJoin(sd, '03-素材', '角色', charDir, 'mouth.json');
  const mouthPngPath = safeJoin(sd, '03-素材', '角色', charDir, 'mouth.png');
  if (existsSync(mouthJsonPath) && existsSync(mouthPngPath)) {
    try {
      const map = JSON.parse(readFileSync(mouthJsonPath, 'utf8'));
      const dstMouth = join(dstDir, 'mouth.png');
      copyFileSync(mouthPngPath, dstMouth);
      const msize = imageSize(dstMouth);
      const mouthAssetId = genId('prop_');
      anime.assets.props.push({
        id: mouthAssetId,
        name: `嘴-${c.name}`,
        type: 'static',
        url: `${cacheDirName}/assets/characters/${charDir}/mouth.png`,
        width: msize.width,
        height: msize.height,
        createdAt: Date.now(),
      });
      mouth = { assetId: mouthAssetId, map };
    } catch (e) {
      warn(`角色「${c.name}」mouth.json 解析失败：${e.message}`);
    }
  }

  const character = makeCharacter({
    mouth,
    name: c.name,
    characterId,
    gender: c.gender || asset.gender || 'other',
    bodyUrl: rel,
    width: size.width,
    height: size.height,
    expressions: exprList,
    bodies: fullBodies,
    face: asset.face || {},
  });
  anime.compositeCharacters.push(character);
  characterByName.set(c.name, character);
  characterExpression.set(c.name, fullBodies.length
    ? { targetType: 'symbol', byEmotion: fullByEmotion, defaultId: fullByEmotion.get('平静') || fullBodies[0]?.id }
    : { targetType: 'expression', byEmotion: exprByEmotion, defaultId: exprByEmotion.get('平静') || exprList[0]?.id });

  const voiceId = pickVoiceId(c.gender || 'other', c.voice || '');
  anime.actors.push({
    id: genId('actor_'),
    name: c.name,
    characterId,
    voice: { voiceId, speed: 0 },
    alias: c.voice || '',
  });
  actorByName.set(c.name, {
    id: anime.actors.at(-1).id,
    name: c.name,
    character,
    voiceId,
    preset: c.voice || '',
    gender: c.gender || 'other',
    bodyScale: Number(asset.face?.bodyScale ?? 1),
    mouth,
    charSize: { width: size.width, height: size.height },
  });
}

if (!anime.actors.length) {
  console.error('✗ 没有任何可用角色。先跑 03-素材 并确认 03-素材/角色/<角色名>/body.png 存在。');
  process.exit(1);
}

// ---------- 4. 按场景分组台词 ----------
const manifestBySeq = new Map();
for (const l of voiceManifest.lines || []) manifestBySeq.set(Number(l.seq), l);

const sceneOrder = [];
const sceneById = new Map();
for (const s of script.scenes || []) {
  sceneById.set(s.id, s);
}
for (const line of script.lines || []) {
  const sid = line.scene || (script.scenes?.[0]?.id ?? 'S1');
  if (!sceneById.has(sid)) {
    sceneById.set(sid, { id: sid, title: sid, actors: [] });
  }
  if (!sceneOrder.includes(sid)) sceneOrder.push(sid);
}
for (const s of script.scenes || []) {
  if (!sceneOrder.includes(s.id)) warn(`场景「${s.id} ${s.title}」没有台词，已跳过`);
}

const camera = makeCamera(W, H);
// 相机以场景中心为视口中心（app 的视口基准是固定 1456×819 或补丁后的 819×1456）
const scenes = [];

for (const sid of sceneOrder) {
  const sceneMeta = sceneById.get(sid);
  const lines = (script.lines || []).filter((l) => (l.scene || sceneOrder[0]) === sid);
  if (!lines.length) continue;

  const speakerNames = [];
  for (const l of lines) {
    const sp = String(l.speaker || '').replace(/[：:]\s*$/, '');
    if (!['旁白', '叙述', '解说'].includes(sp) && !speakerNames.includes(sp)) speakerNames.push(sp);
  }
  const wantActors = [...new Set([...(sceneMeta.actors || []), ...speakerNames])].filter((n) => actorByName.has(n));
  if (!wantActors.length) {
    warn(`场景「${sceneMeta.title || sid}」没有可用角色`);
    continue;
  }

  const cam = sceneMeta.camera || {};
  const sceneCamera = {
    ...camera,
    x: (Number.isFinite(cam.x) ? cam.x : 0.5) * W,
    y: (Number.isFinite(cam.y) ? cam.y : 0.5) * H,
    zoom: Number.isFinite(cam.zoom) ? cam.zoom : 1,
  };

  const objects = [];
  const renderChain = [];

  const bg = bgByName.get(sceneMeta.background) || bgByName.get(sceneMeta.title) || null;
  if (bg?.assetId) {
    const bgAsset = anime.assets.backgrounds.find((b) => b.id === bg.assetId);
    const obj = makeBackgroundObject(
      { id: bg.assetId, name: bgAsset.name, width: bg.width, height: bg.height },
      { sceneW: W, sceneH: H },
    );
    objects.push(obj);
    renderChain.push(obj.id);
  } else {
    warn(`场景「${sceneMeta.title || sid}」找不到背景「${sceneMeta.background || ''}」，用纯色底`);
  }

  // v0.3：道具摆位（简单左右分布，zIndex 低于角色）
  for (const [i, propEntry] of (sceneMeta.props || []).entries()) {
    const propName = typeof propEntry === 'string' ? propEntry : propEntry?.name;
    const propCfg = typeof propEntry === 'string' ? {} : (propEntry || {});
    const prop = propByName.get(propName);
    if (!prop?.assetId) {
      warn(`场景「${sceneMeta.title || sid}」找不到道具「${propName}」，已跳过`);
      continue;
    }
    const propScale = Number.isFinite(propCfg.scale)
      ? propCfg.scale
      : (H * 0.14) / (prop.height || 1024);
    const propX = Number.isFinite(propCfg.x) ? propCfg.x : 0.24 + i * 0.18;
    const propY = Number.isFinite(propCfg.y) ? propCfg.y : 0.64;
    const propObj = makePropObject(
      { id: prop.assetId, name: prop.name, width: prop.width, height: prop.height },
      { x: W * propX, y: H * propY, scale: propScale },
    );
    propObj.zIndex = 6;
    objects.push(propObj);
    renderChain.push(propObj.id);
  }

  const n = wantActors.length;
  const defaultPositions = n === 1 ? [0.5] : n === 2 ? [0.36, 0.64] : Array.from({ length: n }, (_, i) => (i + 1) / (n + 1));
  // 角色高度按 app 相机视口（竖屏补丁后 819×1456 / 默认 1456×819）来定
  const VIEW_H = H > W ? 1456 : 819;
  const factor = n === 1
    ? (H > W ? 0.62 : 0.70)
    : n === 2
      ? (H > W ? 0.48 : 0.60)
      : (H > W ? 0.40 : 0.50);
  const scale = factor * (VIEW_H / 1536);
  const feetY = H / 2 + VIEW_H * 0.36;
  // v1.0：bodyScale（有的角色设定得更高/更壮）必须逐角色算根节点位置，
  // 否则放大一号的脚会陷进地板、缩小一号的会悬空。
  const rootYFor = (bs) => feetY - (1536 * scale * bs) / 2;
  const rootY = rootYFor(1);
  const actorRoot = new Map();
  const actorExprRoot = new Map();
  const actorMouth = new Map();

  wantActors.forEach((name, i) => {
    const a = actorByName.get(name);
    const posX = Number.isFinite(sceneMeta.positions?.[name]) ? sceneMeta.positions[name] : defaultPositions[i];
    const { objects: actorObjects, rootId } = instantiateCharacter(a.character, {
      actorId: a.id,
      actorName: name,
      x: W * posX,
      y: rootYFor(a.bodyScale || 1),
      scale: scale * (a.bodyScale || 1),
    });
    objects.push(...actorObjects);
    renderChain.push(rootId);
    actorRoot.set(name, rootId);
    const info = characterExpression.get(name);
    const targetObj = actorObjects.find((o) => o.type === (info?.targetType === 'symbol' ? 'symbol' : 'expression'));
    if (targetObj) actorExprRoot.set(name, targetObj.id);
    if (a.mouth) {
      actorMouth.set(name, {
        id: null,
        assetId: a.mouth.assetId,
        map: a.mouth.map,
        charW: a.charSize.width,
        charH: a.charSize.height,
        posX: W * posX,
        rootY: rootYFor(a.bodyScale || 1),
        scale: scale * (a.bodyScale || 1),
      });
    }
    const poseName = sceneMeta.poses?.[name];
    if (poseName && targetObj && info?.byEmotion?.has(poseName)) {
      const pid = info.byEmotion.get(poseName);
      if (targetObj.type === 'symbol') targetObj.currentMaterialId = pid;
      else { targetObj.refId = pid; targetObj.defaultRefId = pid; }
    }
  });

  // v0.6：场景级「嘴」图层（挂在场景根上，动画坐标才不会被复合容器改写）
  for (const [name, info] of actorMouth) {
    const firstLine = lines.find((l) => String(l.speaker || '').replace(/[：:]\s*$/, '') === name);
    const initPose = sceneMeta.poses?.[name] || emotionToExpression(firstLine?.emotion || '平静');
    const t = mouthTransform(info, initPose);
    const mouthId = genId('obj_');
    const mouthObj = {
      id: mouthId,
      type: 'prop',
      name: `${name}_mouth`,
      alias: 'mouth',
      refId: info.assetId,
      x: t ? info.posX + t.x * info.scale : info.posX,
      y: t ? info.rootY + t.y * info.scale : info.rootY,
      width: 120,
      height: 120,
      scaleX: t ? t.scaleX * info.scale : 0.5,
      scaleY: t ? t.scaleY * info.scale : 0.05,
      rotation: 0,
      alpha: 1,
      flipX: false,
      zIndex: 30,
      visible: !!t,
      spawned: true,
      animations: { talk: makeTalkAnimation() },
    };
    objects.push(mouthObj);
    renderChain.push(mouthId);
    info.id = mouthId;
  }

  const light = makeLight({ x: W / 2, y: H / 2 });
  objects.push(light);
  renderChain.push(light.id);

  const blocks = [];
  let lastFollow = wantActors.length ? actorRoot.get(wantActors[0]) : null;
  const firstExpr = {
    root: actorExprRoot.get(wantActors[0]) || null,
    info: characterExpression.get(wantActors[0]) || null,
  };
  let lastDialogueExpr = firstExpr;
  for (const line of lines) {
    const seq = Number(line.seq);
    const m = manifestBySeq.get(seq);
    const speaker = String(line.speaker || '').replace(/[：:]\s*$/, '') || '旁白';
    const isNarration = ['旁白', '叙述', '解说'].includes(speaker);
    const duration = Math.max(300, Number(m?.duration) || estimateDuration(line.text));
    const hash = m?.hash || simpleHash(`${line.text}|${speaker}`);
    const audioPath = `${cacheDirName}/tts/${hash}.mp3`;

    const voiceId = isNarration ? 101026 : actorByName.get(speaker)?.voiceId || 101026;
    const voiceSpeed = 0;
    const tts = {
      duration,
      audioPath,
      voiceId,
      generatedFrom: {
        ...(isNarration ? {} : { instanceId: actorRoot.get(speaker) || '' }),
        text: line.text,
        voiceId,
        speed: voiceSpeed,
        volume: 1,
      },
    };
    const note = {
      seq,
      emotion: line.emotion || '',
      sfx: line.sfx || '',
      sceneTitle: sceneMeta.title || sid,
    };

    const block = isNarration
      ? makeNarrationBlock({ text: line.text, tts, note })
      : (() => {
          const instanceId = actorRoot.get(speaker);
          if (!instanceId) {
            warn(`第 ${seq} 行角色「${speaker}」不在本场，已按旁白处理`);
            return makeNarrationBlock({ text: line.text, tts, note });
          }
          return makeDialogueBlock({ text: line.text, instanceId, tts, note });
        })();

    const speakerRoot = actorRoot.get(speaker) || null;
    if (speakerRoot) lastFollow = speakerRoot;
    const follow = isNarration ? lastFollow : (speakerRoot || lastFollow);
    const punch = ['得意', '愤怒', '暴怒', '崩溃', '惊讶', '震惊', '嘲讽'].includes(line.emotion);
    const multi = wantActors.length >= 2;
    const fixedZoom = Number.isFinite(sceneMeta.camera?.zoom) && sceneMeta.camera.zoom !== 1;
    if (fixedZoom) {
      // 近景/特写镜头：保持场景相机，不再自动跟拍/推镜，避免把 1.45 的 zoom 拉回 1.1
    } else if (multi) {
      // 双人场：固定二人同框，只用推镜/震屏加节奏，不跟拍，避免把另一个角色挤出画面
      if (punch) {
        block.actions.push(makeCameraMove({ x: W / 2, y: H / 2, zoom: 1.08 }));
      }
    } else if (follow) {
      block.actions.push(makeCameraFollow({
        followTarget: follow,
        damping: isNarration ? 0.35 : 0.2,
        offsetY: isNarration ? -60 : -40,
        zoom: punch ? 1.10 : undefined,
      }));
    }
    if (/咚|啪|轰|撞|砰|灵魂/.test(line.sfx || '')) {
      block.actions.push(makeCameraShake({ intensity: 16, frequency: 10 }));
    } else if (/开门/.test(line.sfx || '')) {
      block.actions.push(makeCameraShake({ intensity: 8, frequency: 6 }));
    }

    // v0.2：按情绪切表情
    const speakerExpr = {
      root: actorExprRoot.get(speaker) || null,
      info: characterExpression.get(speaker) || null,
    };
    let chosenExpr;
    if (isNarration) {
      // 旁白默认给「主角」（场里第一个角色）；主角的表情才是观众代入的反应
      chosenExpr = firstExpr;
    } else {
      chosenExpr = speakerExpr.root ? speakerExpr : lastDialogueExpr;
      if (chosenExpr?.root) lastDialogueExpr = chosenExpr;
    }
    if (chosenExpr?.root && chosenExpr.info) {
      const targetEmo = emotionToExpression(line.emotion);
      // v0.7：场景 poses 锁死姿态（坐着/崩溃等），不被 emotion 覆盖；
      // 单行 line.pose 优先级最高
      const exprActor = isNarration ? wantActors[0] : speaker;
      const lockPose = sceneMeta.poses?.[exprActor] || null;
      const poseWant = line.pose || lockPose;
      const poseId = poseWant ? chosenExpr.info.byEmotion.get(poseWant) : null;
      const materialId = poseId || chosenExpr.info.byEmotion.get(targetEmo) || chosenExpr.info.defaultId;
      if (materialId) {
        block.actions.push(makeSetMaterial({ target: chosenExpr.root, materialId }));
      }
    }

    // v0.6：说话时嘴开合（场景级图层，跟着当前表情的嘴位走）
    const mInfo = actorMouth.get(speaker);
    if (mInfo?.id) {
      const lockPoseM = sceneMeta.poses?.[speaker] || null;
      const poseK = line.pose || lockPoseM || emotionToExpression(line.emotion);
      const mt = mouthTransform(mInfo, poseK);
      if (mt) {
        block.actions.push(
          makeSetTransform({
            target: mInfo.id,
            params: {
              x: mInfo.posX + mt.x * mInfo.scale,
              y: mInfo.rootY + mt.y * mInfo.scale,
              scaleX: mt.scaleX * mInfo.scale,
              scaleY: mt.scaleY * mInfo.scale,
            },
          }),
        );
        block.actions.push(makeSetVisual({ target: mInfo.id, params: { visible: true } }));
        block.actions.push(
          makeSetAnim({
            target: mInfo.id,
            animations: [{ animName: 'talk', timingMode: 'tts_speech', autoStopOnBlockEnd: true }],
          }),
        );
      } else {
        // 该表情本来就是大张嘴（哭/笑/惊），不叠加
        block.actions.push(makeSetVisual({ target: mInfo.id, params: { visible: false } }));
      }
    }
    if (line.move) {
      const moveTarget = actorRoot.get(speaker) || actorRoot.get(wantActors[0]);
      if (moveTarget) {
        block.actions.push(makeTweenTransform({
          target: moveTarget,
          slotIndex: 0,
          slotSpan: 1,
          easing: 'linear',
          params: {
            ...(Number.isFinite(line.move.x) ? { x: W * line.move.x } : {}),
            ...(Number.isFinite(line.move.y) ? { y: H * line.move.y } : {}),
          },
        }));
      }
    }

    blocks.push(block);

    // 拷贝音频
    if (m?.audio) {
      const src = safeJoin(sd, m.audio);
      const dst = join(cacheDir, 'tts', `${hash}.mp3`);
      if (existsSync(src)) {
        if (!existsSync(dst)) copyFileSync(src, dst);
      } else {
        warn(`第 ${seq} 行音频不存在：${src}`);
      }
    }
  }

  // v0.9：整场开「呼吸」，让角色不是一张静态图
  if (blocks.length) {
    for (const nm of wantActors) {
      const rid = actorRoot.get(nm);
      if (!rid) continue;
      blocks[0].actions.unshift(
        makeSetAnim({
          target: rid,
          animations: [{ animName: 'idle', autoStopOnBlockEnd: false, loop: true }],
        }),
      );
    }
  }

  scenes.push(
    makeScene({
      title: sceneMeta.title || sid,
      camera: sceneCamera,
      objects,
      renderChain,
      script: blocks,
    }),
  );
}

if (!scenes.length) {
  console.error('✗ 没有生成任何场景。检查剧本 lines 的 scene 字段与素材。');
  process.exit(1);
}

// ---------- 5. 集信息 ----------
anime.episodes.push(
  makeEpisode({
    number: episode,
    name: script.title || `第${episode}集`,
    scenes,
  }),
);
anime.modifiedAt = Date.now();

// ---------- 6. 写盘 ----------
writeJson(animePath, anime);

const totalBlocks = scenes.reduce((s, sc) => s + sc.script.length, 0);
const totalMs = scenes.reduce((s, sc) => s + sc.script.reduce((x, b) => x + (b.ttsConfig?.duration || 0), 0), 0);

console.log('');
console.log('========================================');
console.log(`工程：${animePath}`);
console.log(`画布：${W}×${H} @ ${FPS}fps`);
console.log(`场景：${scenes.length} 个 / 脚本块：${totalBlocks} 条 / 时长：${(totalMs / 1000).toFixed(1)}s`);
console.log(`角色：${anime.compositeCharacters.map((c) => c.name).join('、')}`);
console.log(`缓存：${cacheDir}`);
if (warnings.length) {
  console.log('');
  console.log(`警告 ${warnings.length} 条：`);
  for (const w of warnings.slice(0, 20)) console.log(`  - ${w}`);
  if (warnings.length > 20) console.log(`  ...还有 ${warnings.length - 20} 条`);
}
console.log('========================================');
console.log('');
console.log('下一步：');
console.log(`  1) node 04-工程/shadiao-anime-skill/scripts/validate_anime.mjs "${animePath}"`);
console.log(`  2) 浏览器打开 app →「打开项目文件夹」→ 选 ${outDir}`);
console.log(`  3) 打开 ${animeName} → 预览 → 导出`);

function estimateDuration(text = '') {
  return Math.max(1200, String(text).length * 320);
}

function simpleHash(text) {
  let h = 0;
  for (let i = 0; i < text.length; i++) h = (h * 31 + text.charCodeAt(i)) >>> 0;
  return h.toString(16).padStart(8, '0');
}
