import { createHash, randomUUID } from "node:crypto";

export const SCENE_SCHEMA_VERSION = 1;
export const MAX_SCENES = 128;
export const MAX_SCENE_ACTIONS = 64;
export const MAX_SNAPSHOT_DEVICES = 256;
export const SCENE_SOURCES = Object.freeze(["recommended", "custom", "snapshot"]);
export const SCENE_SCOPE_TYPES = Object.freeze(["home", "room", "group", "device", "subset"]);

export class SceneError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "SceneError";
    this.code = code;
    this.details = details;
  }
}

const RECOMMENDED_ROWS = Object.freeze([
  {
    id: "return-home",
    name: "回家",
    objectiveRecipe: "return-home",
    provenance: "yeelight-smart-home/references/scene-recipes.md#回家",
    description: "明亮、自然的回家照明。",
    properties: { power: true, brightness: 80, colorTemperature: 4000 },
  },
  {
    id: "away",
    name: "离家",
    objectiveRecipe: "away",
    provenance: "yeelight-smart-home/references/scene-recipes.md#离家",
    description: "关闭所选目标的灯光。",
    properties: { power: false },
  },
  {
    id: "daily",
    name: "日常",
    objectiveRecipe: "daily",
    provenance: "yeelight-smart-home/references/scene-recipes.md#日常",
    description: "均衡、低眩光的日常照明。",
    properties: { power: true, brightness: 70, colorTemperature: 4000 },
  },
  {
    id: "guests",
    name: "会客",
    objectiveRecipe: "guests",
    provenance: "yeelight-smart-home/references/scene-recipes.md#会客",
    description: "清爽明亮的会客照明。",
    properties: { power: true, brightness: 85, colorTemperature: 4500 },
  },
  {
    id: "cleaning",
    name: "清洁",
    objectiveRecipe: "cleaning",
    provenance: "yeelight-smart-home/references/scene-recipes.md#清洁",
    description: "提高辨识度和阴影可见性的功能照明。",
    properties: { power: true, brightness: 100, colorTemperature: 5500 },
  },
  {
    id: "late-return",
    name: "深夜归家",
    objectiveRecipe: "late-return",
    provenance: "yeelight-smart-home/references/scene-recipes.md#深夜归家",
    description: "低亮度、暖色的路径照明。",
    properties: { power: true, brightness: 20, colorTemperature: 2700 },
  },
  {
    id: "reading",
    name: "阅读",
    objectiveRecipe: "reading",
    provenance: "yeelight-smart-home/references/scene-recipes.md#阅读",
    description: "清晰的任务光和适度暖色。",
    properties: { power: true, brightness: 80, colorTemperature: 4500 },
  },
  {
    id: "tea",
    name: "品茗",
    objectiveRecipe: "tea",
    provenance: "yeelight-smart-home/references/scene-recipes.md#品茗",
    description: "温润、低压的交谈照明。",
    properties: { power: true, brightness: 70, colorTemperature: 3500 },
  },
  {
    id: "movie",
    name: "观影",
    objectiveRecipe: "movie",
    provenance: "yeelight-smart-home/references/scene-recipes.md#观影",
    description: "低亮度背景光，减少屏幕眩光。",
    properties: { power: true, brightness: 10, colorTemperature: 3000 },
  },
  {
    id: "gathering",
    name: "聚会",
    objectiveRecipe: "gathering",
    provenance: "yeelight-smart-home/references/scene-recipes.md#聚会",
    description: "明亮、自然且克制彩光的聚会照明。",
    properties: { power: true, brightness: 85, colorTemperature: 4000 },
  },
  {
    id: "night-light",
    name: "夜灯",
    objectiveRecipe: "night-light",
    provenance: "yeelight-smart-home/references/scene-recipes.md#夜灯",
    description: "低亮度暖色方位参考光。",
    properties: { power: true, brightness: 10, colorTemperature: 2700 },
  },
  {
    id: "morning-light",
    name: "早安",
    objectiveRecipe: "morning-light",
    provenance: "yeelight-smart-home/references/scene-recipes.md#早安",
    description: "从暖色低亮度开始的温和早安光。",
    properties: { power: true, brightness: 65, colorTemperature: 3500 },
  },
]);

export const RECOMMENDED_SCENES = RECOMMENDED_ROWS;

const PROPERTY_METHODS = Object.freeze({
  power: ["set_power"],
  brightness: ["set_bright"],
  colorTemperature: ["set_ct_abx"],
  color: ["set_rgb"],
  hue: ["set_hsv"],
  saturation: ["set_hsv"],
  flow: ["start_cf"],
});

const SNAPSHOT_PROPERTIES = Object.freeze([
  "power", "brightness", "colorTemperature", "color", "hue", "saturation",
  "bgPower", "bgBrightness", "bgColorTemperature", "bgColor", "bgHue", "bgSaturation",
]);

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function clone(value) {
  if (value === undefined) return undefined;
  return structuredClone(value);
}

function requireString(value, code, message, max = 160) {
  if (typeof value !== "string" || !value.trim() || value.length > max || /[\u0000-\u001f\u007f]/u.test(value)) {
    throw new SceneError(code, message);
  }
  return value.trim();
}

function identityOf(device) {
  if (typeof device === "string" || typeof device === "number") return String(device);
  return device?.id ?? device?.deviceId ?? device?.protocolId ?? device?.protocolID ?? null;
}

function sortedUniqueIds(values, code = "scene_target_invalid") {
  if (!Array.isArray(values) || values.length < 1 || values.length > MAX_SNAPSHOT_DEVICES) {
    throw new SceneError(code, "情景目标设备列表无效。", { max: MAX_SNAPSHOT_DEVICES });
  }
  const ids = values.map((value) => identityOf(value));
  if (ids.some((id) => typeof id !== "string" || !id.trim())) throw new SceneError(code, "情景目标设备 ID 无效。");
  const unique = [...new Set(ids.map((id) => id.trim()))].sort();
  if (unique.length !== ids.length) throw new SceneError(code, "情景目标设备不可重复。");
  return unique;
}

function normalizeScope(rawScope, rawTarget) {
  const raw = rawScope ?? rawTarget ?? { type: "home" };
  if (typeof raw === "string") return normalizeScope({ type: raw });
  if (!isRecord(raw)) throw new SceneError("scene_scope_invalid", "情景作用域无效。", { allowed: SCENE_SCOPE_TYPES });
  const type = String(raw.type ?? raw.targetType ?? "").trim();
  if (!SCENE_SCOPE_TYPES.includes(type)) throw new SceneError("scene_scope_invalid", "情景作用域类型无效。", { allowed: SCENE_SCOPE_TYPES });
  if (type === "home") return { type };
  if (type === "subset") return { type, deviceIds: sortedUniqueIds(raw.deviceIds ?? raw.devices ?? raw.ids) };
  const id = identityOf(raw.id ?? raw.targetId ?? raw.deviceId ?? raw.ref);
  if (typeof id !== "string" || !id.trim()) throw new SceneError("scene_scope_invalid", "情景作用域缺少稳定 ID。", { type });
  return { type, id: id.trim() };
}

function normalizeScalar(name, value) {
  if (name === "power" || name === "bgPower") {
    if (typeof value !== "boolean") throw new SceneError("scene_action_invalid", `${name} 必须是布尔值。`);
  } else if (["brightness", "bgBrightness"].includes(name)) {
    if (!Number.isInteger(value) || value < 1 || value > 100) throw new SceneError("scene_action_invalid", `${name} 必须在 1-100。`);
  } else if (["colorTemperature", "bgColorTemperature"].includes(name)) {
    if (!Number.isInteger(value) || value < 1700 || value > 6500) throw new SceneError("scene_action_invalid", `${name} 必须在 1700-6500。`);
  } else if (["color", "bgColor"].includes(name)) {
    if (!Number.isInteger(value) || value < 0 || value > 0xFFFFFF) throw new SceneError("scene_action_invalid", `${name} 必须在 RGB 整数范围。`);
  } else if (["hue", "bgHue"].includes(name)) {
    if (!Number.isInteger(value) || value < 0 || value > 359) throw new SceneError("scene_action_invalid", `${name} 必须在 0-359。`);
  } else if (["saturation", "bgSaturation"].includes(name)) {
    if (!Number.isInteger(value) || value < 0 || value > 100) throw new SceneError("scene_action_invalid", `${name} 必须在 0-100。`);
  }
  return value;
}

function normalizeSet(rawSet) {
  if (!isRecord(rawSet)) throw new SceneError("scene_action_invalid", "情景动作必须包含对象 set。", { accepted: SNAPSHOT_PROPERTIES });
  const set = {};
  for (const [key, value] of Object.entries(rawSet)) {
    if (!/^[A-Za-z][A-Za-z0-9_]*$/u.test(key) || key.length > 64) throw new SceneError("scene_action_invalid", "情景动作属性名无效。");
    set[key] = normalizeScalar(key, clone(value));
  }
  if (!Object.keys(set).length) throw new SceneError("scene_action_invalid", "情景动作不能为空。");
  return set;
}

function normalizeActions(rawActions, sceneScope) {
  if (!Array.isArray(rawActions) || rawActions.length < 1 || rawActions.length > MAX_SCENE_ACTIONS) {
    throw new SceneError("scene_actions_invalid", "情景必须包含 1-64 个完整动作。", { max: MAX_SCENE_ACTIONS });
  }
  return rawActions.map((raw, index) => {
    if (!isRecord(raw)) throw new SceneError("scene_action_invalid", "情景动作必须是对象。", { index });
    const targetRaw = raw.target ?? (raw.targetType ? raw : undefined);
    const target = targetRaw === undefined ? undefined : normalizeScope(targetRaw);
    const set = normalizeSet(raw.set ?? raw.properties);
    return {
      ...(target ? { target } : {}),
      set,
      ...(typeof raw.rank === "number" && Number.isInteger(raw.rank) ? { rank: raw.rank } : {}),
    };
  });
}

function payloadForHash(scene) {
  return {
    source: scene.source,
    recommendedId: scene.recommendedId ?? null,
    scope: scene.scope,
    actions: scene.actions,
    snapshotDeviceIds: scene.snapshotDeviceIds ?? null,
  };
}

export function stableStringify(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map((item) => stableStringify(item)).join(",")}]`;
  return `{${Object.keys(value).sort().filter((key) => value[key] !== undefined).map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
}

export function payloadHash(value) {
  const payload = isRecord(value) && value.actions && value.scope ? payloadForHash(value) : value;
  return createHash("sha256").update(stableStringify(payload), "utf8").digest("hex");
}

export const scenePayloadHash = payloadHash;

export function normalizeSceneInput(input, { now = () => new Date().toISOString(), idFactory = () => randomUUID() } = {}) {
  if (!isRecord(input)) throw new SceneError("scene_invalid", "情景必须是对象。");
  const source = String(input.source ?? "custom");
  if (!SCENE_SOURCES.includes(source)) throw new SceneError("scene_source_invalid", "情景来源无效。", { allowed: SCENE_SOURCES });
  const name = requireString(input.name, "scene_name_invalid", "情景名称不能为空。", 80);
  const scope = normalizeScope(input.scope, input.target);
  const actions = normalizeActions(input.actions, scope);
  const id = requireString(input.id ?? idFactory(), "scene_id_invalid", "情景 ID 无效。", 160);
  const timestamp = typeof now === "function" ? now() : now;
  const scene = {
    schemaVersion: SCENE_SCHEMA_VERSION,
    id,
    name,
    source,
    scope,
    actions,
    revision: Number.isInteger(input.revision) && input.revision > 0 ? input.revision : 1,
    createdAt: input.createdAt ?? timestamp,
    updatedAt: input.updatedAt ?? timestamp,
    ...(input.description ? { description: requireString(input.description, "scene_description_invalid", "情景说明无效。", 500) } : {}),
    ...(input.recommendedId ? { recommendedId: requireString(input.recommendedId, "scene_recommended_id_invalid", "推荐情景 ID 无效。", 80) } : {}),
    ...(input.provenance ? { provenance: requireString(input.provenance, "scene_provenance_invalid", "情景来源无效。", 240) } : {}),
    ...(input.readonly === true || source === "recommended" ? { readonly: true } : {}),
  };
  if (source === "snapshot") {
    scene.snapshotDeviceIds = sortedUniqueIds(input.snapshotDeviceIds ?? input.deviceIds ?? (scope.type === "subset" ? scope.deviceIds : undefined));
    scene.deviceIds = [...scene.snapshotDeviceIds];
    if (scope.type !== "subset" && scene.snapshotDeviceIds.length < 1) throw new SceneError("snapshot_targets_required", "快照情景必须固定设备目标。");
  }
  scene.payloadHash = payloadHash(scene);
  return scene;
}

export function createScene(input, options = {}) {
  if (String(input?.source ?? "custom") === "recommended") throw new SceneError("recommended_read_only", "推荐情景是只读模板。请先复制后修改。");
  return normalizeSceneInput(input, options);
}

export function createCustomScene(input, options = {}) {
  return createScene({ ...input, source: "custom" }, options);
}

export function updateScene(existing, replacement, { now = () => new Date().toISOString(), expectedRevision, schedules = [], force = false } = {}) {
  if (!isRecord(existing)) throw new SceneError("scene_not_found", "情景不存在。");
  if (existing.readonly || existing.source === "recommended") throw new SceneError("recommended_read_only", "推荐情景是只读模板。请先复制后修改。");
  if (expectedRevision !== undefined && existing.revision !== expectedRevision) throw new SceneError("scene_revision_conflict", "情景版本已变化。", { expectedRevision, actualRevision: existing.revision });
  assertSceneScheduleMutation(existing, schedules, force);
  if (!isRecord(replacement) || !Array.isArray(replacement.actions) || replacement.scope === undefined || replacement.name === undefined) {
    throw new SceneError("scene_full_replacement_required", "情景更新必须提交完整 name、scope 和 actions。");
  }
  const next = normalizeSceneInput({ ...replacement, id: existing.id, source: existing.source, revision: existing.revision + 1, createdAt: existing.createdAt, updatedAt: typeof now === "function" ? now() : now }, { now, idFactory: () => existing.id });
  return next;
}

export function deleteScene(existing, { schedules = [], force = false } = {}) {
  if (!isRecord(existing)) throw new SceneError("scene_not_found", "情景不存在。");
  if (existing.readonly || existing.source === "recommended") throw new SceneError("recommended_read_only", "推荐情景不能删除。");
  assertSceneScheduleMutation(existing, schedules, force);
  return { deleted: true, sceneId: existing.id, revision: existing.revision };
}

export function copyScene(existing, { name, now = () => new Date().toISOString(), idFactory = () => randomUUID(), schedules = [] } = {}) {
  if (!isRecord(existing)) throw new SceneError("scene_not_found", "情景不存在。");
  const copy = createScene({ ...clone(existing), id: idFactory(), name: name ?? `${existing.name} 副本`, source: "custom", readonly: false, revision: 1, createdAt: undefined, updatedAt: undefined }, { now, idFactory });
  // Copying is read-only with respect to the source schedule bindings.
  void schedules;
  return copy;
}

function assertSceneScheduleMutation(scene, schedules, force) {
  if (force) return;
  const refs = (Array.isArray(schedules) ? schedules : []).filter((schedule) => schedule?.enabled === true || schedule?.status === "active" || schedule?.state === "enabled").filter((schedule) => schedule.sceneId === scene.id);
  if (refs.length) throw new SceneError("scene_schedule_reconfirmation_required", "情景被启用的调度引用，必须先暂停或重新确认版本。", { scheduleIds: refs.map((schedule) => schedule.id) });
}

export function createSceneCollection(initial = []) {
  if (!Array.isArray(initial)) throw new SceneError("scene_collection_invalid", "情景集合必须是数组。");
  const rows = initial.map((scene) => normalizeSceneInput(scene));
  assertUniqueSceneIds(rows);
  return rows;
}

export function listScenes(scenes, { source, scopeType } = {}) {
  const rows = Array.isArray(scenes) ? scenes : [];
  return rows.filter((scene) => (source ? scene.source === source : true)).filter((scene) => (scopeType ? scene.scope?.type === scopeType : true)).map(clone);
}

export function getScene(scenes, id) {
  const row = (Array.isArray(scenes) ? scenes : []).find((scene) => scene?.id === id);
  return row ? clone(row) : null;
}

export function createSceneInCollection(scenes, input, options = {}) {
  const rows = Array.isArray(scenes) ? scenes : [];
  if (rows.length >= MAX_SCENES) throw new SceneError("scene_limit_exceeded", "本地情景数量已达到上限。", { max: MAX_SCENES });
  const scene = createScene(input, options);
  if (rows.some((row) => row.id === scene.id)) throw new SceneError("scene_id_conflict", "情景 ID 已存在。");
  if (rows.some((row) => row.name.normalize("NFKC").toLocaleLowerCase() === scene.name.normalize("NFKC").toLocaleLowerCase())) throw new SceneError("scene_name_conflict", "同一家庭中的情景名称不能重复。");
  return { scenes: [...rows.map(clone), scene], scene };
}

export function updateSceneInCollection(scenes, id, replacement, options = {}) {
  const rows = Array.isArray(scenes) ? scenes : [];
  const index = rows.findIndex((row) => row.id === id);
  if (index < 0) throw new SceneError("scene_not_found", "情景不存在。");
  const scene = updateScene(rows[index], replacement, options);
  const next = rows.slice();
  next[index] = scene;
  return { scenes: next.map(clone), scene };
}

export function deleteSceneInCollection(scenes, id, options = {}) {
  const rows = Array.isArray(scenes) ? scenes : [];
  const index = rows.findIndex((row) => row.id === id);
  if (index < 0) throw new SceneError("scene_not_found", "情景不存在。");
  const result = deleteScene(rows[index], options);
  return { scenes: rows.filter((_, rowIndex) => rowIndex !== index).map(clone), ...result };
}

export function assertUniqueSceneIds(scenes) {
  const ids = scenes.map((scene) => scene?.id);
  if (ids.some((id) => typeof id !== "string" || !id)) throw new SceneError("scene_id_invalid", "情景 ID 无效。");
  if (new Set(ids).size !== ids.length) throw new SceneError("scene_id_conflict", "情景 ID 不能重复。");
  return true;
}

export function recommendedSceneCatalog({ now = () => new Date().toISOString(), idFactory = (id) => id } = {}) {
  return RECOMMENDED_ROWS.map((row) => normalizeSceneInput({
    id: idFactory(row.id), name: row.name, source: "recommended", readonly: true,
    recommendedId: row.id, provenance: row.provenance, description: row.description,
    scope: { type: "home" }, actions: [{ set: row.properties }],
  }, { now, idFactory: () => row.id }));
}

export const createRecommendedScenes = recommendedSceneCatalog;

function supportSet(device) {
  const support = device?.support ?? device?.supportedMethods ?? device?.capabilities?.methods;
  if (Array.isArray(support)) return new Set(support.map(String));
  if (typeof support === "string") return new Set(support.split(/[\s,]+/u).filter(Boolean));
  return null;
}

export function supportsSceneProperty(device, property, { background = false } = {}) {
  const methods = supportSet(device);
  if (!methods) return true;
  const suffix = background ? "bg_" : "";
  const candidates = PROPERTY_METHODS[property] ?? [];
  return candidates.some((method) => methods.has(method.startsWith("bg_") ? method : `${suffix}${method}`));
}

function propertyNameForDevice(property, background) {
  if (!background) return property;
  return property.startsWith("bg") ? property : `bg${property[0].toUpperCase()}${property.slice(1)}`;
}

export function compileSceneForDevice(scene, device, { background = false } = {}) {
  const set = {};
  const skipped = [];
  const sourceSet = scene?.actions?.[0]?.set ?? {};
  for (const [property, value] of Object.entries(sourceSet)) {
    const methodProperty = background && !property.startsWith("bg") ? property : property.replace(/^bg/, (match) => match);
    if (supportsSceneProperty(device, methodProperty, { background })) set[propertyNameForDevice(property, background)] = clone(value);
    else skipped.push({ property, reason: "unsupported" });
  }
  return { deviceId: identityOf(device), set, skipped, supported: skipped.length === 0 };
}

export function compileRecommendedScene(sceneOrId, devices, options = {}) {
  const scene = typeof sceneOrId === "string" ? RECOMMENDED_ROWS.find((row) => row.id === sceneOrId) : sceneOrId;
  if (!scene) throw new SceneError("recommended_scene_not_found", "推荐情景不存在。");
  const normalized = scene.actions ? scene : { actions: [{ set: scene.properties }] };
  const rows = (Array.isArray(devices) ? devices : []).map((device) => compileSceneForDevice(normalized, device, options));
  return { sceneId: scene.id ?? scene.recommendedId, actions: rows, skipped: rows.flatMap((row) => row.skipped.map((item) => ({ deviceId: row.deviceId, ...item }))) };
}

function collectionById(values) {
  return new Map((Array.isArray(values) ? values : []).map((value) => [String(identityOf(value)), value]));
}

export function expandSceneTargets(scene, { devices = [], rooms = [], groups = [], resolveTarget } = {}) {
  if (!scene?.scope) throw new SceneError("scene_scope_invalid", "情景缺少作用域。");
  const deviceById = collectionById(devices);
  let ids;
  const scope = scene.scope;
  if (typeof resolveTarget === "function") {
    const resolved = resolveTarget(scope, { devices, rooms, groups });
    ids = Array.isArray(resolved) ? resolved.map(identityOf) : resolved?.deviceIds;
  }
  if (!ids) {
    if (scope.type === "home") ids = [...deviceById.keys()];
    else if (scope.type === "subset") ids = scope.deviceIds;
    else if (scope.type === "device") ids = [scope.id];
    else if (scope.type === "room") ids = idsFromMember(collectionById(rooms).get(scope.id), "deviceIds", "members");
    else if (scope.type === "group") ids = idsFromMember(collectionById(groups).get(scope.id), "deviceIds", "memberIds", "members");
  }
  ids = [...new Set((ids ?? []).map((id) => String(id)).filter(Boolean))].sort();
  const missingDeviceIds = ids.filter((id) => !deviceById.has(id));
  return { scope: clone(scope), deviceIds: ids, devices: ids.filter((id) => deviceById.has(id)).map((id) => deviceById.get(id)), missingDeviceIds };
}

function idsFromMember(value, ...keys) {
  if (!value) return [];
  for (const key of keys) if (Array.isArray(value[key])) return value[key].map(identityOf);
  return [];
}

export const expandTargets = expandSceneTargets;

export function planSceneApplication(scene, context = {}) {
  const expansion = expandSceneTargets(scene, context);
  const actions = scene.actions ?? [];
  const actionByTarget = new Map();
  for (const action of actions) {
    const target = action.target ? expandSceneTargets({ scope: action.target }, context).deviceIds : expansion.deviceIds;
    for (const id of target) {
      const previous = actionByTarget.get(id);
      if (previous && stableStringify(previous.set) !== stableStringify(action.set)) throw new SceneError("scene_action_conflict", "同一设备收到相互冲突的情景动作。", { deviceId: id });
      actionByTarget.set(id, { deviceId: id, set: clone(action.set) });
    }
  }
  return { sceneId: scene.id, revision: scene.revision, payloadHash: scene.payloadHash, deviceIds: [...actionByTarget.keys()].sort(), actions: [...actionByTarget.values()].sort((a, b) => a.deviceId.localeCompare(b.deviceId)), missingDeviceIds: expansion.missingDeviceIds };
}

export async function applyScene(scene, {
  devices = [],
  rooms = [],
  groups = [],
  resolveTarget,
  readState,
  execute,
  persistRecovery,
  now = () => new Date().toISOString(),
  idFactory,
  signal,
} = {}) {
  if (typeof execute !== "function") throw new SceneError("scene_executor_required", "应用情景需要注入 execute 钩子。");
  const context = { devices, rooms, groups, resolveTarget };
  const plan = planSceneApplication(scene, context);
  const deviceById = collectionById(devices);
  const preStates = new Map();
  if (typeof readState === "function") {
    for (const row of plan.actions) {
      const state = await readState(deviceById.get(row.deviceId) ?? row.deviceId, { fresh: true, signal });
      if (!state || state.verified === false || state.fresh === false || typeof state !== "object") throw new SceneError("scene_pre_state_untrusted", "情景应用需要每个目标的新鲜已验证状态。", { deviceId: row.deviceId });
      preStates.set(row.deviceId, clone(state.state ?? state));
    }
  }
  let recovery;
  let recoveryApi;
  if (typeof persistRecovery === "function" && preStates.size === plan.actions.length && plan.actions.length) {
    recoveryApi = await import("./recovery.mjs");
    recovery = recoveryApi.createRecoveryRecord({
      idFactory,
      now,
      sceneId: scene.id,
      sceneRevision: scene.revision,
      sceneHash: scene.payloadHash,
      targets: plan.actions.map((row) => ({ deviceId: row.deviceId, preState: preStates.get(row.deviceId), postState: { ...preStates.get(row.deviceId), ...row.set }, action: row })),
    });
    await persistRecovery(recoveryApi.serializeRecoveryRecord(recovery));
  }
  const rows = [];
  for (const row of plan.actions) {
    if (signal?.aborted) {
      rows.push({ deviceId: row.deviceId, status: "uncertain", reason: "aborted" });
      continue;
    }
    const device = deviceById.get(row.deviceId) ?? row.deviceId;
    try {
      const result = await execute(device, clone(row.set), { scene: clone(scene), deviceId: row.deviceId, signal });
      const status = result?.status === "failed" ? "failed" : result?.status === "uncertain" ? "uncertain" : "success";
      rows.push({ deviceId: row.deviceId, status, result: clone(result) });
      if (recovery && recoveryApi) recovery = recoveryApi.recordRecoveryOutcome(recovery, { deviceId: row.deviceId, status, touched: true, postState: { ...preStates.get(row.deviceId), ...row.set }, state: result?.state }, { now });
    } catch (error) {
      rows.push({ deviceId: row.deviceId, status: "uncertain", error: { code: "scene_execute_failed", message: String(error?.message ?? error) } });
      if (recovery && recoveryApi) recovery = recoveryApi.recordRecoveryOutcome(recovery, { deviceId: row.deviceId, status: "uncertain", touched: true, error: { code: "scene_execute_failed" } }, { now });
    }
    if (recovery && recoveryApi) await persistRecovery(recoveryApi.serializeRecoveryRecord(recovery));
  }
  const failed = rows.filter((row) => row.status === "failed").length;
  const uncertain = rows.filter((row) => row.status === "uncertain").length;
  const status = uncertain ? "uncertain" : failed ? (rows.some((row) => row.status === "success") ? "partial" : "failed") : "success";
  return { status, sceneId: scene.id, revision: scene.revision, payloadHash: scene.payloadHash, rows, recoveryId: recovery && recovery.pendingDeviceIds.length ? recovery.id : null, recovery };
}

export function staticSnapshotState(state) {
  if (!isRecord(state)) throw new SceneError("snapshot_state_invalid", "快照状态无效。");
  const output = {};
  const aliases = {
    bright: "brightness", ct: "colorTemperature", rgb: "color", sat: "saturation",
    bg_power: "bgPower", bg_bright: "bgBrightness", bg_ct: "bgColorTemperature", bg_rgb: "bgColor", bg_hue: "bgHue", bg_sat: "bgSaturation",
  };
  for (const property of SNAPSHOT_PROPERTIES) if (state[property] !== undefined) output[property] = normalizeSnapshotValue(property, state[property]);
  for (const [source, property] of Object.entries(aliases)) if (output[property] === undefined && state[source] !== undefined) output[property] = normalizeSnapshotValue(property, state[source]);
  if (!Object.keys(output).length) throw new SceneError("snapshot_state_empty", "快照没有可恢复的静态状态。");
  return output;
}

function normalizeSnapshotValue(property, value) {
  if (["power", "bgPower"].includes(property) && typeof value === "string" && ["on", "off"].includes(value)) return value === "on";
  if (["brightness", "colorTemperature", "color", "hue", "saturation", "bgBrightness", "bgColorTemperature", "bgColor", "bgHue", "bgSaturation"].includes(property) && typeof value === "string" && /^-?\d+$/u.test(value)) return Number(value);
  return clone(value);
}

export function snapshotSceneFromStates({ name, scope, states, deviceIds, now = () => new Date().toISOString(), idFactory = () => randomUUID(), description, provenance } = {}) {
  if (!Array.isArray(states) || !states.length) throw new SceneError("snapshot_states_required", "快照必须包含至少一个设备状态。");
  const ids = sortedUniqueIds(deviceIds ?? states.map((state) => identityOf(state)));
  const byId = new Map(states.map((state) => [String(identityOf(state)), state]));
  const actions = ids.map((id) => {
    const state = byId.get(id);
    if (!state) throw new SceneError("snapshot_state_missing", "快照缺少设备状态。", { deviceId: id });
    if (state.verified === false || state.fresh === false) throw new SceneError("snapshot_state_not_fresh", "快照只接受新鲜且已验证的状态。", { deviceId: id });
    return { target: { type: "device", id }, set: staticSnapshotState(state) };
  });
  const normalizedScope = normalizeScope(scope ?? { type: "subset", deviceIds: ids });
  return normalizeSceneInput({ name, source: "snapshot", scope: normalizedScope, snapshotDeviceIds: ids, actions, description, provenance }, { now, idFactory });
}

export const createSnapshotScene = snapshotSceneFromStates;

export async function captureSnapshotScene({ name, scope, targetContext, readState, now = () => new Date().toISOString(), idFactory = () => randomUUID(), ...options } = {}) {
  if (typeof readState !== "function") throw new SceneError("snapshot_reader_required", "快照需要注入 readState 读取钩子。");
  const expansion = expandSceneTargets({ scope: normalizeScope(scope) }, targetContext ?? {});
  const states = [];
  for (const device of expansion.devices) {
    const state = await readState(device);
    states.push({ ...state, id: identityOf(device) });
  }
  return snapshotSceneFromStates({ name, scope, states, deviceIds: expansion.deviceIds, now, idFactory, ...options });
}

function assertRecoverySceneRevision(scene, schedules = []) {
  if (!scene) return;
  const refs = schedules.filter((schedule) => schedule?.status === "active" && schedule.sceneId === scene.id && schedule.sceneRevision !== scene.revision);
  if (refs.length) throw new SceneError("scene_schedule_revision_drift", "调度引用的情景版本已变化。", { scheduleIds: refs.map((schedule) => schedule.id) });
}

export const __testing = {
  RECOMMENDED_ROWS,
  SNAPSHOT_PROPERTIES,
  PROPERTY_METHODS,
  normalizeScope,
  normalizeActions,
  assertRecoverySceneRevision,
};
