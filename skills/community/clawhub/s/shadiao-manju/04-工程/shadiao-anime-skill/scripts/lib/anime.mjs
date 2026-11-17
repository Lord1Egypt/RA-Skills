import { randomUUID } from 'node:crypto';
import { coverScale } from './media.mjs';

export function genId(prefix = '') {
  return prefix + randomUUID().replace(/-/g, '').slice(0, 16);
}

export function makeCamera(width, height) {
  return { x: width / 2, y: height / 2, width, height, zoom: 1 };
}

export function makeProject({ name, width = 1080, height = 1920, fps = 30 }) {
  return {
    meta: {
      name,
      resolution: { w: width, h: height },
      fps,
      version: '2.0.0',
    },
    assets: { backgrounds: [], props: [], sounds: [], musics: [] },
    expressions: {},
    actors: [],
    narrator: { voice: {} },
    sceneTemplates: [],
    compositeCharacters: [],
    customPresetAnimations: [],
    episodes: [],
  };
}

/**
 * 角色模板：一个根 composite + 一个 symbol（整身图）。
 * v0.1 不做表情叠加；表情图先出着，v0.2 再挂 ExpressionObject。
 */
export function makeCharacter({ mouth = null, name, characterId, gender = 'other', bodyUrl, width, height, expressions = [], bodies = [], face = {} }) {
  const rootId = genId('cc_root_');
  const imgId = genId('cc_img_');
  const matId = genId('mat_');

  const childIds = [imgId];
  const renderChain = [imgId];

  const root = {
    id: rootId,
    type: 'composite',
    name,
    alias: name,
    refId: '',
    x: 0,
    y: 0,
    width,
    height,
    scaleX: 1,
    scaleY: 1,
    rotation: 0,
    alpha: 1,
    flipX: false,
    zIndex: 10,
    visible: true,
    spawned: true,
    childIds,
    compositeLocked: true,
    compositeMode: 'entity',
    renderChain,
    extraInfo: { kind: 'character', characterId },
    animations: { idle: makeIdleAnimation() },
  };

  const image = {
    id: imgId,
    type: 'symbol',
    name: `${name}_body`,
    alias: 'body',
    refId: '',
    parentId: rootId,
    x: 0,
    y: 0,
    width,
    height,
    scaleX: 1,
    scaleY: 1,
    rotation: 0,
    alpha: 1,
    flipX: false,
    zIndex: 10,
    visible: true,
    spawned: true,
    materials: bodies.length
      ? bodies.map((b) => ({ id: b.id || genId('mat_'), name: b.name, type: 'static', url: b.url }))
      : [{ id: matId, name: 'body', type: 'static', url: bodyUrl }],
    currentMaterialId: matId,
  };

  const objects = [root, image];

  // v0.4：整身表情图（8 个 material），直接切整身，不再贴脸
  if (bodies.length) {
    image.currentMaterialId = (image.materials.find((m) => m.name === '平静') || image.materials[0]).id;
  }

  // v0.2：表情对象（脸部叠加），用 set_material 在播放时切 refId（旧模式，保留兼容）
  const defaultExpr = expressions.find((e) => e.name === '平静') || expressions[0];
  if (!bodies.length && defaultExpr) {
    const exprObjId = genId('cc_expr_');
    const fx = Number.isFinite(face.x) ? face.x : 0.5;
    const fy = Number.isFinite(face.y) ? face.y : 0.197;
    const exprObj = {
      id: exprObjId,
      type: 'expression',
      name: `${name}_face`,
      alias: 'face',
      refId: defaultExpr.id,
      defaultRefId: defaultExpr.id,
      parentId: rootId,
      x: (fx - 0.5) * width,
      y: (fy - 0.5) * height,
      width: 1024,
      height: 1024,
      scaleX: 1,
      scaleY: 1,
      rotation: 0,
      alpha: 1,
      flipX: false,
      zIndex: 11,
      visible: true,
      spawned: true,
    };
    objects.push(exprObj);
    childIds.push(exprObjId);
    renderChain.push(exprObjId);
  }

  return {
    id: characterId,
    name,
    gender,
    createdAt: Date.now(),
    updatedAt: Date.now(),
    objects,
    renderChain: [rootId],
    rootCompositeId: rootId,
    editorAnchor: { x: 0, y: 0 },
  };
}

/** v0.9：角色待机微动（呼吸）。整身 scale 轻微起伏，解决「站那儿一动不动」。 */
export function makeIdleAnimation(name = 'idle') {
  return {
    type: 'track',
    id: genId('anim_'),
    name,
    description: '待机呼吸',
    loop: true,
    timingMode: 'continuous',
    createdAt: Date.now(),
    updatedAt: Date.now(),
    tracks: [
      {
        trackType: 'effect',
        displayName: '呼吸',
        effectParams: { type: 'breathe', intensity: 0.013, speed: 0.85 },
      },
    ],
  };
}

/** v0.6：说话嘴开合动画（transform 轨道，靠 scaleY 乘数 开→合） */
export function makeTalkAnimation(name = 'talk') {
  return {
    type: 'track',
    id: genId('anim_'),
    name,
    description: '说话时嘴开合',
    loop: true,
    timingMode: 'tts_speech',
    createdAt: Date.now(),
    updatedAt: Date.now(),
    tracks: [
      {
        trackType: 'transform',
        displayName: '嘴开合',
        duration: 400,
        easing: 'linear',
        keyframes: [
          { time: 0, scaleY: 1 },
          { time: 0.14, scaleY: 4.4 },
          { time: 0.3, scaleY: 1 },
          { time: 0.46, scaleY: 3.2 },
          { time: 0.6, scaleY: 1.05 },
          { time: 0.78, scaleY: 4.0 },
          { time: 1, scaleY: 1 },
        ],
      },
    ],
  };
}

/** 把角色模板实例化进场景：重映射 id，挂 actor 身份，摆位 */
export function instantiateCharacter(character, { actorId, actorName, x, y, scale = 1 }) {
  const map = new Map();
  for (const obj of character.objects) map.set(obj.id, genId('obj_'));

  const objects = character.objects.map((src) => {
    const obj = structuredClone(src);
    obj.id = map.get(src.id);
    if (obj.parentId) obj.parentId = map.get(obj.parentId) || undefined;
    if (Array.isArray(obj.childIds)) obj.childIds = obj.childIds.map((id) => map.get(id)).filter(Boolean);
    if (Array.isArray(obj.renderChain)) obj.renderChain = obj.renderChain.map((id) => map.get(id)).filter(Boolean);
    obj.spawned = true;
    return obj;
  });

  const rootId = map.get(character.rootCompositeId) || objects[0]?.id;
  const root = objects.find((o) => o.id === rootId);
  if (root) {
    root.name = actorName;
    root.alias = actorName;
    root.x = x;
    root.y = y;
    root.scaleX = scale;
    root.scaleY = scale;
    root.rotation = 0;
    root.visible = true;
    root.extraInfo = { ...(root.extraInfo || {}), kind: 'actor', actorId };
  }

  return { objects, rootId };
}

export function makeBackgroundObject(asset, { sceneW, sceneH }) {
  const scale = coverScale(asset.width, asset.height, sceneW, sceneH);
  return {
    id: genId('bg_'),
    refId: asset.id,
    type: 'background',
    name: asset.name,
    alias: asset.name,
    x: sceneW / 2,
    y: sceneH / 2,
    width: asset.width,
    height: asset.height,
    scaleX: scale,
    scaleY: scale,
    rotation: 0,
    alpha: 1,
    flipX: false,
    zIndex: -10,
    visible: true,
    spawned: true,
  };
}

export function makePropObject(asset, { x, y, scale = 1 }) {
  return {
    id: genId('prop_'),
    refId: asset.id,
    type: 'prop',
    name: asset.name,
    alias: asset.name,
    x,
    y,
    width: asset.width,
    height: asset.height,
    scaleX: scale,
    scaleY: scale,
    rotation: 0,
    alpha: 1,
    flipX: false,
    zIndex: 10,
    visible: true,
    spawned: true,
  };
}

export function makeLight({ x, y }) {
  return {
    id: genId('light_'),
    refId: '',
    type: 'light',
    name: '环境光',
    alias: '环境光',
    x,
    y,
    width: 96,
    height: 96,
    scaleX: 1,
    scaleY: 1,
    rotation: 0,
    alpha: 1,
    flipX: false,
    zIndex: 1000,
    visible: true,
    spawned: true,
    lightType: 'ambient',
    lightColor: '#ffffff',
    lightIntensity: 1,
    lightRadius: 500,
  };
}

export function makeScene({ title, camera, objects, renderChain, script }) {
  return {
    id: genId('scene_'),
    type: 'scene_container',
    title,
    setup: { camera, objects, renderChain },
    script,
  };
}

function baseBlock({ type, text, speed = 1, tts, note }) {
  return {
    id: genId('blk_'),
    type,
    text,
    speed,
    actions: [],
    ttsConfig: tts,
    productionNote: note || {},
  };
}

export function makeNarrationBlock(args) {
  return baseBlock({ ...args, type: 'narration' });
}

export function makeDialogueBlock({ instanceId, ...args }) {
  return { ...baseBlock({ ...args, type: 'dialogue' }), instanceId };
}

export function makeCameraFollow({ followTarget, slotIndex = 0, zoom, offsetY = -40, damping = 0.2 }) {
  return {
    id: genId('act_'),
    target: 'camera',
    type: 'camera_follow',
    category: 'duration',
    slotIndex,
    slotSpan: 1,
    easing: 'linear',
    params: {
      followTarget,
      damping,
      offsetY,
      ...(zoom ? { zoom } : {}),
      smoothEntry: true,
      smoothEntryDuration: 300,
      constrainBounds: true,
    },
  };
}

export function makeCameraMove({ slotIndex = 0, x, y, zoom } = {}) {
  return {
    id: genId('act_'),
    target: 'camera',
    type: 'camera_move',
    category: 'duration',
    slotIndex,
    slotSpan: 1,
    easing: 'easeInOutQuad',
    params: { x, y, zoom },
  };
}

export function makeSetTransform({ target, slotIndex = 0, params = {} }) {
  return {
    id: genId('act_'),
    target,
    type: 'set_transform',
    category: 'point',
    slotIndex,
    params,
  };
}

export function makeSetVisual({ target, slotIndex = 0, params = {} }) {
  return {
    id: genId('act_'),
    target,
    type: 'set_visual',
    category: 'point',
    slotIndex,
    params,
  };
}

export function makeSetAnim({ target, slotIndex = 0, animations = [], reset = true }) {
  return {
    id: genId('act_'),
    target,
    type: 'set_anim',
    category: 'point',
    slotIndex,
    params: { animations, reset },
  };
}

export function makeTweenTransform({ target, slotIndex = 0, slotSpan = 1, params = {}, easing = 'linear' }) {
  return {
    id: genId('act_'),
    target,
    type: 'tween_transform',
    category: 'duration',
    slotIndex,
    slotSpan,
    easing,
    params,
  };
}

export function makeCameraShake({ slotIndex = 0, intensity = 14, frequency = 9, decay = true } = {}) {
  return {
    id: genId('act_'),
    target: 'camera',
    type: 'camera_shake',
    category: 'duration',
    slotIndex,
    slotSpan: 1,
    params: { intensity, decay, frequency },
  };
}

export function makeSetMaterial({ target, materialId, slotIndex = 0 }) {
  return {
    id: genId('act_'),
    target,
    type: 'set_material',
    category: 'point',
    slotIndex,
    params: { materialId },
  };
}

export function makeEpisode({ number, name, scenes }) {
  const now = Date.now();
  const duration = scenes.reduce(
    (sum, scene) =>
      sum +
      scene.script.reduce((s, block) => s + (block.type === 'action' ? block.duration || 0 : block.ttsConfig?.duration || 0), 0),
    0,
  );
  return {
    id: genId('episode_'),
    episodeNumber: number,
    name,
    scenes,
    bgmTracks: [],
    duration,
    createdAt: now,
    modifiedAt: now,
    version: '6.0',
  };
}
