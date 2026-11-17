import { createHash, randomUUID } from "node:crypto";
import { stableStringify } from "./scenes.mjs";

export const SCHEDULE_SCHEMA_VERSION = 1;
export const HOST_SCHEDULER_OWNER = "yeelight-wifi-lan-control";
export const MAX_SCHEDULES = 64;
export const MAX_OCCURRENCES = 128;
export const DEFAULT_LEASE_MS = 5 * 60 * 1000;
export const SCHEDULE_STATES = Object.freeze(["draft", "active", "paused", "inactive", "binding_pending", "delete_pending"]);
export const OCCURRENCE_STATES = Object.freeze(["running", "success", "partial", "failed", "uncertain"]);
export const TERMINAL_OCCURRENCE_STATES = Object.freeze(["success", "partial", "failed", "uncertain"]);

export class ScheduleError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "ScheduleError";
    this.code = code;
    this.details = details;
  }
}

const clone = (value) => value === undefined ? undefined : structuredClone(value);
const identityOf = (value) => typeof value === "string" || typeof value === "number" ? String(value) : value?.id ?? value?.deviceId ?? value?.ref ?? null;

function nowValue(now) {
  return typeof now === "function" ? now() : (now ?? new Date().toISOString());
}

function stateAlias(status) {
  return status === "active" ? "enabled" : status;
}

function bump(next, now) {
  next.revision = Number.isInteger(next.revision) ? next.revision + 1 : 1;
  next.updatedAt = nowValue(now);
  return next;
}

function requireString(value, code, message, max = 180) {
  if (typeof value !== "string" || !value.trim() || value.length > max || /[\u0000-\u001f\u007f]/u.test(value)) throw new ScheduleError(code, message);
  return value.trim();
}

function assertPositiveInt(value, code, message) {
  if (!Number.isInteger(value) || value < 1) throw new ScheduleError(code, message);
  return value;
}

export function validateTimezone(timezone) {
  const value = requireString(timezone, "schedule_timezone_required", "调度必须指定 IANA 时区。", 100);
  try {
    new Intl.DateTimeFormat("en-US", { timeZone: value }).format();
  } catch {
    throw new ScheduleError("schedule_timezone_invalid", "调度时区不是有效的 IANA 时区。", { timezone: value });
  }
  return value;
}

function validateTime(time) {
  if (typeof time !== "string" || !/^([01]\d|2[0-3]):[0-5]\d$/u.test(time)) throw new ScheduleError("schedule_cadence_invalid", "固定时间必须使用 HH:MM。", { time });
  return time;
}

function validateDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,3})?)?(?:Z|[+-]\d{2}:?\d{2})$/u.test(value) || Number.isNaN(Date.parse(value))) throw new ScheduleError("schedule_cadence_invalid", "一次性调度时间必须是带时区的 RFC3339 时间。", { at: value });
  return new Date(value).toISOString();
}

const OCCURRENCE_UTC_RE = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{3}))?Z$/u;
const OCCURRENCE_LOCAL_RE = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})$/u;

function normalizeOccurrenceUtc(value) {
  if (typeof value !== "string") throw new ScheduleError("occurrence_invalid", "occurrence scheduledAt 必须是 UTC RFC3339 时间。", { scheduledAt: value });
  const match = OCCURRENCE_UTC_RE.exec(value);
  if (!match) throw new ScheduleError("occurrence_invalid", "occurrence scheduledAt 必须使用带 Z 的 UTC RFC3339 时间。", { scheduledAt: value });
  const date = new Date(value);
  if (Number.isNaN(date.getTime()) || date.toISOString() !== `${match[1]}-${match[2]}-${match[3]}T${match[4]}:${match[5]}:${match[6]}.${match[7] || "000"}Z`) {
    throw new ScheduleError("occurrence_invalid", "occurrence scheduledAt 不是有效的 UTC 时间。", { scheduledAt: value });
  }
  return date.toISOString();
}

function normalizeLocalDateTime(value) {
  if (typeof value !== "string") throw new ScheduleError("occurrence_invalid", "occurrence localDateTime 必须使用 YYYY-MM-DDTHH:MM。", { localDateTime: value });
  const match = OCCURRENCE_LOCAL_RE.exec(value);
  if (!match) throw new ScheduleError("occurrence_invalid", "occurrence localDateTime 必须使用 YYYY-MM-DDTHH:MM。", { localDateTime: value });
  const [, yearText, monthText, dayText, hourText, minuteText] = match;
  const year = Number(yearText);
  const month = Number(monthText);
  const day = Number(dayText);
  const hour = Number(hourText);
  const minute = Number(minuteText);
  const check = new Date(0);
  check.setUTCFullYear(year, month - 1, day);
  check.setUTCHours(hour, minute, 0, 0);
  if (check.getUTCFullYear() !== year || check.getUTCMonth() !== month - 1 || check.getUTCDate() !== day || check.getUTCHours() !== hour || check.getUTCMinutes() !== minute) {
    throw new ScheduleError("occurrence_invalid", "occurrence localDateTime 不是有效的本地时间。", { localDateTime: value });
  }
  return value;
}

function formatLocalDateTime(instant, timezone) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: validateTimezone(timezone),
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(new Date(instant));
  const values = Object.fromEntries(parts.filter((part) => ["year", "month", "day", "hour", "minute"].includes(part.type)).map((part) => [part.type, part.value]));
  return `${String(values.year).padStart(4, "0")}-${values.month}-${values.day}T${values.hour}:${values.minute}`;
}

function formatLocalWeekday(instant, timezone) {
  const weekday = new Intl.DateTimeFormat("en-US", { timeZone: validateTimezone(timezone), weekday: "short" }).format(new Date(instant));
  const values = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 };
  return values[weekday];
}

function normalizeFold(fold, { required = false } = {}) {
  if (fold === undefined || fold === null) {
    if (required) throw new ScheduleError("occurrence_invalid", "daily/weekly occurrence 必须提供数字 DST fold。", { fold });
    return 0;
  }
  if (!Number.isInteger(fold) || (fold !== 0 && fold !== 1)) throw new ScheduleError("occurrence_invalid", "DST fold 必须是数字 0 或 1。", { fold });
  return fold;
}

export function normalizeCadence(cadence) {
  if (!cadence || typeof cadence !== "object" || Array.isArray(cadence)) throw new ScheduleError("schedule_cadence_invalid", "调度 cadence 无效。");
  const type = String(cadence.type ?? cadence.kind ?? "");
  if (type === "once") return { type, at: validateDate(cadence.at) };
  if (type === "daily") return { type, time: validateTime(cadence.time) };
  if (type === "weekly") {
    if (!Array.isArray(cadence.days) || !cadence.days.length || cadence.days.some((day) => !Number.isInteger(day) || day < 1 || day > 7) || new Set(cadence.days).size !== cadence.days.length) throw new ScheduleError("schedule_cadence_invalid", "每周调度的 days 必须是 1-7 的不重复数组。", { days: cadence.days });
    return { type, days: [...cadence.days].sort((a, b) => a - b), time: validateTime(cadence.time) };
  }
  throw new ScheduleError("schedule_cadence_invalid", "仅支持 once、daily、weekly cadence。", { allowed: ["once", "daily", "weekly"] });
}

function normalizeTarget(target) {
  if (target === undefined || target === null) return { type: "home" };
  if (typeof target === "string") return { type: "device", id: requireString(target, "schedule_target_invalid", "调度目标 ID 无效。") };
  if (typeof target !== "object" || Array.isArray(target)) throw new ScheduleError("schedule_target_invalid", "调度目标无效。");
  const type = String(target.type ?? target.targetType ?? "");
  if (!["home", "room", "group", "device", "subset"].includes(type)) throw new ScheduleError("schedule_target_invalid", "调度目标类型无效。");
  if (type === "home") return { type };
  if (type === "subset") {
    if (!Array.isArray(target.deviceIds) || !target.deviceIds.length) throw new ScheduleError("schedule_target_invalid", "subset 调度目标必须指定设备。");
    const ids = target.deviceIds.map((id) => requireString(String(identityOf(id)), "schedule_target_invalid", "调度目标 ID 无效.")).sort();
    if (new Set(ids).size !== ids.length) throw new ScheduleError("schedule_target_invalid", "调度目标设备不能重复。");
    return { type, deviceIds: ids };
  }
  return { type, id: requireString(String(identityOf(target.id ?? target.deviceId ?? target.ref)), "schedule_target_invalid", "调度目标 ID 无效。") };
}

function normalizeScenePin(input) {
  const pin = input.scenePin ?? input.scene ?? {};
  const sceneId = input.sceneId ?? pin.id ?? pin.sceneId;
  if (sceneId === undefined) throw new ScheduleError("schedule_scene_required", "调度必须固定一个情景 ID。");
  const sceneRevision = input.sceneRevision ?? pin.revision ?? pin.sceneRevision;
  assertPositiveInt(sceneRevision, "schedule_scene_revision_required", "调度必须固定正整数情景版本。");
  const sceneHash = input.sceneHash ?? pin.payloadHash ?? pin.hash;
  if (sceneHash !== undefined && (typeof sceneHash !== "string" || !/^[a-f0-9]{32,128}$/iu.test(sceneHash))) throw new ScheduleError("schedule_scene_hash_invalid", "调度情景哈希无效。");
  return { sceneId: requireString(String(sceneId), "schedule_scene_invalid", "调度情景 ID 无效."), sceneRevision, ...(sceneHash ? { sceneHash } : {}) };
}

export function createScheduleDraft(input, { now = () => new Date().toISOString(), idFactory = () => `schedule-${randomUUID()}`, hostSchedulerAvailable = false } = {}) {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new ScheduleError("schedule_invalid", "调度必须是对象。");
  const id = requireString(idFactory(), "schedule_id_invalid", "调度 ID 无效。");
  const timestamp = nowValue(now);
  const cadence = normalizeCadence(input.cadence);
  const timezone = validateTimezone(input.timezone ?? "UTC");
  const pin = normalizeScenePin(input);
  const name = requireString(input.name ?? "未命名调度", "schedule_name_invalid", "调度名称不能为空。", 100);
  const target = normalizeTarget(input.target);
  const schedule = {
    schemaVersion: SCHEDULE_SCHEMA_VERSION,
    id,
    name,
    timezone,
    cadence,
    target,
    sceneId: pin.sceneId,
    sceneRevision: pin.sceneRevision,
    ...(pin.sceneHash ? { sceneHash: pin.sceneHash } : {}),
    status: "inactive",
    state: "inactive",
    revision: 1,
    lifecycle: "draft",
    enabled: false,
    bindingState: "unbound",
    createdBy: HOST_SCHEDULER_OWNER,
    taskId: null,
    taskRevision: null,
    createdAt: timestamp,
    updatedAt: timestamp,
    occurrences: [],
    lease: null,
    ...(input.actions ? { actions: clone(input.actions) } : {}),
    ...(input.description ? { description: requireString(input.description, "schedule_description_invalid", "调度说明无效。", 500) } : {}),
  };
  schedule.hostSchedulerAvailable = hostSchedulerAvailable === true;
  schedule.hostSchedulerRequest = buildHostSchedulerRequest(schedule, "create", { idempotencyKey: input.idempotencyKey });
  return schedule;
}

export const createSchedule = createScheduleDraft;

export function validateSchedule(schedule) {
  if (!schedule || typeof schedule !== "object" || schedule.schemaVersion !== SCHEDULE_SCHEMA_VERSION) throw new ScheduleError("schedule_invalid", "调度结构无效。");
  requireString(schedule.id, "schedule_id_invalid", "调度 ID 无效。");
  validateTimezone(schedule.timezone);
  normalizeCadence(schedule.cadence);
  normalizeTarget(schedule.target);
  normalizeScenePin(schedule);
  if (!SCHEDULE_STATES.includes(schedule.status)) throw new ScheduleError("schedule_state_invalid", "调度状态无效。", { status: schedule.status });
  if (schedule.state !== undefined && !["draft", "inactive", "binding_pending", "enabled", "paused", "delete_pending"].includes(schedule.state)) throw new ScheduleError("schedule_state_invalid", "调度 state 无效。", { state: schedule.state });
  if (schedule.taskId !== null && schedule.taskId !== undefined) requireString(schedule.taskId, "schedule_task_invalid", "Host task ID 无效。");
  if (!Array.isArray(schedule.occurrences) || schedule.occurrences.length > MAX_OCCURRENCES) throw new ScheduleError("schedule_occurrences_invalid", "调度 occurrence 记录超出上限。");
  return true;
}

function requestKey(schedule, action, supplied) {
  if (supplied) return requireString(supplied, "scheduler_idempotency_invalid", "Host scheduler 幂等键无效。", 180);
  return createHash("sha256").update(stableStringify({ scheduleId: schedule.id, action, revision: schedule.sceneRevision, updatedAt: schedule.updatedAt }), "utf8").digest("hex");
}

export function buildHostSchedulerRequest(schedule, action = "create", { idempotencyKey, taskId, taskRevision } = {}) {
  validateSchedule(schedule);
  const lifecycle = String(action);
  if (!["create", "update", "pause", "resume", "remove"].includes(lifecycle)) throw new ScheduleError("scheduler_action_invalid", "Host scheduler lifecycle action 无效。", { action: lifecycle });
  if (taskId !== undefined && taskId !== null) requireString(taskId, "schedule_task_invalid", "Host task ID 无效。");
  if (taskRevision !== undefined && taskRevision !== null) assertPositiveInt(taskRevision, "scheduler_task_revision_invalid", "Host task revision 无效。");
  const request = {
    contractVersion: "1.0",
    kind: "yeelight-wifi-lan-control.schedule",
    scheduleId: schedule.id,
    idempotencyKey: requestKey(schedule, lifecycle, idempotencyKey),
    createdBy: HOST_SCHEDULER_OWNER,
    action: lifecycle,
    ...(taskId !== undefined && taskId !== null ? { taskId } : schedule.taskId ? { taskId: schedule.taskId } : {}),
    ...(taskRevision !== undefined && taskRevision !== null ? { taskRevision } : schedule.taskRevision ? { taskRevision: schedule.taskRevision } : {}),
    timezone: schedule.timezone,
    cadence: clone(schedule.cadence),
    scenePin: { sceneId: schedule.sceneId, sceneRevision: schedule.sceneRevision, ...(schedule.sceneHash ? { sceneHash: schedule.sceneHash } : {}) },
    target: clone(schedule.target),
  };
  return request;
}

export const makeHostSchedulerRequest = buildHostSchedulerRequest;

export function validateHostSchedulerReply(reply, expected = {}) {
  if (!reply || typeof reply !== "object" || Array.isArray(reply)) throw new ScheduleError("scheduler_reply_invalid", "Host scheduler 回执无效。");
  const scheduleId = requireString(reply.scheduleId, "scheduler_reply_invalid", "Host 回执缺少 scheduleId。");
  const taskId = requireString(reply.taskId, "scheduler_reply_invalid", "Host 回执缺少精确 taskId。");
  const createdBy = requireString(reply.createdBy ?? reply.owner, "scheduler_ownership_invalid", "Host 回执缺少 createdBy ownership marker。");
  if (createdBy !== HOST_SCHEDULER_OWNER) throw new ScheduleError("scheduler_ownership_invalid", "Host task 不属于本 Skill。", { expected: HOST_SCHEDULER_OWNER, actual: createdBy });
  if (expected.scheduleId !== undefined && scheduleId !== expected.scheduleId) throw new ScheduleError("scheduler_reply_mismatch", "Host 回执 scheduleId 不匹配。");
  if (expected.taskId !== undefined && expected.taskId !== null && taskId !== expected.taskId) throw new ScheduleError("scheduler_task_mismatch", "Host 回执 taskId 不匹配。");
  if (expected.createdBy !== undefined && createdBy !== expected.createdBy) throw new ScheduleError("scheduler_ownership_invalid", "Host 回执 ownership 不匹配。");
  const action = String(reply.action ?? expected.action ?? "");
  if (!["create", "update", "pause", "resume", "remove"].includes(action)) throw new ScheduleError("scheduler_reply_invalid", "Host 回执 action 无效。");
  if (expected.action && action !== expected.action) throw new ScheduleError("scheduler_reply_mismatch", "Host 回执 action 不匹配。");
  const idempotencyKey = requireString(reply.idempotencyKey ?? expected.idempotencyKey, "scheduler_idempotency_invalid", "Host 回执缺少幂等键。", 180);
  if (expected.idempotencyKey && idempotencyKey !== expected.idempotencyKey) throw new ScheduleError("scheduler_reply_mismatch", "Host 回执幂等键不匹配。");
  const taskRevision = reply.taskRevision ?? expected.taskRevision ?? null;
  if (taskRevision !== null) assertPositiveInt(taskRevision, "scheduler_task_revision_invalid", "Host task revision 无效。");
  return { ok: reply.ok !== false, scheduleId, taskId, createdBy, action, idempotencyKey, taskRevision, ...(reply.message ? { message: String(reply.message).slice(0, 500) } : {}) };
}

export const validateSchedulerReply = validateHostSchedulerReply;

export function bindSchedule(schedule, reply, { now = () => new Date().toISOString() } = {}) {
  validateSchedule(schedule);
  const request = schedule.hostSchedulerRequest ?? buildHostSchedulerRequest(schedule, "create");
  const normalized = validateHostSchedulerReply(reply, { scheduleId: schedule.id, action: "create", idempotencyKey: request.idempotencyKey });
  const next = clone(schedule);
  next.taskId = normalized.taskId;
  next.hostTaskId = normalized.taskId;
  next.taskRevision = normalized.taskRevision ?? 1;
  next.createdBy = normalized.createdBy;
  next.bindingState = "bound";
  next.lifecycle = "bound";
  next.status = "active";
  next.state = "enabled";
  next.enabled = true;
  bump(next, now);
  next.hostSchedulerRequest = null;
  return next;
}

export function markBindingPending(schedule, action = "create", { now = () => new Date().toISOString(), idempotencyKey } = {}) {
  validateSchedule(schedule);
  const next = clone(schedule);
  next.status = "binding_pending";
  next.state = "binding_pending";
  next.lifecycle = "binding_pending";
  next.bindingState = "pending";
  next.enabled = false;
  bump(next, now);
  next.hostSchedulerRequest = buildHostSchedulerRequest(next, action, { idempotencyKey });
  return next;
}

export function applySchedulerLifecycleReply(schedule, reply, { action = reply?.action, now = () => new Date().toISOString() } = {}) {
  validateSchedule(schedule);
  const request = schedule.hostSchedulerRequest ?? buildHostSchedulerRequest(schedule, action, { taskId: schedule.taskId, taskRevision: schedule.taskRevision });
  const normalized = validateHostSchedulerReply(reply, { scheduleId: schedule.id, taskId: schedule.taskId ?? undefined, action, idempotencyKey: request.idempotencyKey });
  const next = clone(schedule);
  next.taskId = normalized.taskId;
  next.hostTaskId = normalized.taskId;
  next.taskRevision = normalized.taskRevision ?? next.taskRevision;
  next.createdBy = normalized.createdBy;
  next.hostSchedulerRequest = null;
  if (action === "pause") { next.status = "paused"; next.state = "paused"; next.lifecycle = "paused"; next.enabled = false; next.bindingState = "bound"; }
  else if (action === "resume") { next.status = "active"; next.state = "enabled"; next.lifecycle = "bound"; next.enabled = true; next.bindingState = "bound"; }
  else if (action === "update") { next.status = "active"; next.state = "enabled"; next.lifecycle = "bound"; next.enabled = true; next.bindingState = "bound"; }
  else if (action === "remove") { next.status = "delete_pending"; next.state = "delete_pending"; next.lifecycle = "delete_pending"; next.enabled = false; next.bindingState = "delete_pending"; }
  else return bindSchedule(next, reply, { now });
  return bump(next, now);
}

export function markDeletePending(schedule, { now = () => new Date().toISOString(), idempotencyKey } = {}) {
  const next = markBindingPending(schedule, "remove", { now, idempotencyKey });
  next.status = "delete_pending";
  next.state = "delete_pending";
  next.lifecycle = "delete_pending";
  next.bindingState = "delete_pending";
  next.enabled = false;
  return next;
}

export function completeScheduleDelete(schedule, reply, options = {}) {
  const next = applySchedulerLifecycleReply(schedule, reply, { ...options, action: "remove" });
  return { deleted: true, scheduleId: next.id, schedule: null };
}

export function deleteSchedule(schedule, options = {}) {
  validateSchedule(schedule);
  if (!schedule.taskId) return { deleted: true, scheduleId: schedule.id, schedule: null, hostSchedulerRequest: null };
  const pending = markDeletePending(schedule, options);
  return { deleted: false, scheduleId: schedule.id, schedule: pending, hostSchedulerRequest: pending.hostSchedulerRequest };
}

export function updateSchedule(schedule, replacement, { now = () => new Date().toISOString(), expectedRevision } = {}) {
  validateSchedule(schedule);
  if (expectedRevision !== undefined && schedule.sceneRevision !== expectedRevision) throw new ScheduleError("schedule_scene_revision_conflict", "调度情景版本已变化。");
  if (schedule.occurrences?.some((occurrence) => occurrence.status === "running")) {
    throw new ScheduleError("schedule_occurrence_running", "调度当前有正在执行的 occurrence，请等待其完成后再更新。");
  }
  const nextInput = { ...schedule, ...replacement, id: schedule.id, sceneId: replacement.sceneId ?? schedule.sceneId, sceneRevision: replacement.sceneRevision ?? schedule.sceneRevision, source: undefined };
  const next = createScheduleDraft(nextInput, { now, idFactory: () => schedule.id, hostSchedulerAvailable: schedule.hostSchedulerAvailable === true });
  next.createdAt = schedule.createdAt;
  next.occurrences = clone(schedule.occurrences);
  next.lease = clone(schedule.lease);
  next.taskId = schedule.taskId;
  next.hostTaskId = schedule.taskId;
  next.taskRevision = schedule.taskRevision;
  next.bindingState = schedule.taskId ? "pending" : "unbound";
  next.status = schedule.taskId ? "binding_pending" : "inactive";
  next.state = schedule.taskId ? "binding_pending" : "inactive";
  next.lifecycle = schedule.taskId ? "binding_pending" : "draft";
  next.enabled = false;
  next.revision = schedule.revision + 1;
  next.updatedAt = nowValue(now);
  next.hostSchedulerRequest = buildHostSchedulerRequest(next, schedule.taskId ? "update" : "create", { taskId: schedule.taskId, taskRevision: schedule.taskRevision });
  return next;
}

export function pauseSchedule(schedule, options = {}) {
  return markBindingPending({ ...schedule, status: "paused" }, "pause", options);
}

export function resumeSchedule(schedule, options = {}) {
  return markBindingPending({ ...schedule, status: "active" }, "resume", options);
}

export function sceneRevisionMatches(schedule, scene) {
  if (!scene || schedule.sceneId !== scene.id || schedule.sceneRevision !== scene.revision) return false;
  return !schedule.sceneHash || schedule.sceneHash === scene.payloadHash;
}

export function scheduleRunnable(schedule, { scene } = {}) {
  try { validateSchedule(schedule); } catch (error) { return { ok: false, reason: error.code }; }
  if (schedule.status === "delete_pending" || schedule.bindingState === "delete_pending") return { ok: false, reason: "delete_pending" };
  if (schedule.status === "binding_pending" || schedule.bindingState === "pending" || !schedule.taskId || schedule.createdBy !== HOST_SCHEDULER_OWNER) return { ok: false, reason: "binding_pending" };
  if (schedule.status !== "active" || schedule.enabled !== true) return { ok: false, reason: "inactive" };
  if (schedule.bindingState !== "bound") return { ok: false, reason: "binding_pending" };
  if (scene && !sceneRevisionMatches(schedule, scene)) return { ok: false, reason: "scene_revision_drift" };
  return { ok: true };
}

export const isScheduleRunnable = scheduleRunnable;

export function makeOccurrenceKey({ scheduleId, scheduledAt, occurrence } = {}) {
  const id = requireString(String(scheduleId ?? ""), "occurrence_invalid", "occurrence 缺少 scheduleId。");
  const instant = normalizeOccurrenceUtc(scheduledAt ?? occurrence);
  // localDateTime/fold are audit metadata, not part of the dedupe identity. A
  // repeated UTC instant must not acquire a second lease merely because a Host
  // formatted its local DST metadata differently.
  return `${id}|${instant}`;
}

export function normalizeOccurrenceMetadata(schedule, { scheduledAt, localDateTime, fold } = {}) {
  validateSchedule(schedule);
  const cadence = normalizeCadence(schedule.cadence);
  const instant = normalizeOccurrenceUtc(scheduledAt);
  const local = normalizeLocalDateTime(localDateTime);
  const expectedLocal = formatLocalDateTime(instant, schedule.timezone);
  if (local !== expectedLocal) throw new ScheduleError("occurrence_invalid", "occurrence localDateTime 与调度时区中的 UTC instant 不一致。", { expected: expectedLocal, actual: local });

  let normalizedFold;
  if (cadence.type === "once") {
    if (instant !== cadence.at) throw new ScheduleError("occurrence_invalid", "once occurrence scheduledAt 必须等于调度的 cadence.at。", { expected: cadence.at, actual: instant });
    if (fold !== undefined && fold !== 0) throw new ScheduleError("occurrence_invalid", "once occurrence 的 DST fold 必须省略或为数字 0。", { fold });
    normalizedFold = 0;
  } else {
    normalizedFold = normalizeFold(fold, { required: true });
    if (cadence.type === "daily" && local.slice(11) !== cadence.time) {
      throw new ScheduleError("occurrence_invalid", "daily occurrence localDateTime 必须命中 cadence.time。", { expected: cadence.time, actual: local.slice(11) });
    }
    if (cadence.type === "weekly") {
      if (local.slice(11) !== cadence.time) throw new ScheduleError("occurrence_invalid", "weekly occurrence localDateTime 必须命中 cadence.time。", { expected: cadence.time, actual: local.slice(11) });
      const weekday = formatLocalWeekday(instant, schedule.timezone);
      if (!cadence.days.includes(weekday)) throw new ScheduleError("occurrence_invalid", "weekly occurrence 的本地星期不在 cadence.days 中。", { expected: cadence.days, actual: weekday });
    }
  }

  const key = makeOccurrenceKey({ scheduleId: schedule.id, scheduledAt: instant });
  return {
    key,
    scheduledAt: instant,
    localDateTime: local,
    fold: normalizedFold,
  };
}

export function acquireOccurrence(schedule, occurrenceKey, { now = () => new Date().toISOString(), leaseMs = DEFAULT_LEASE_MS, leaseIdFactory = () => `lease-${randomUUID()}`, occurrenceMetadata } = {}) {
  validateSchedule(schedule);
  const key = requireString(occurrenceKey, "occurrence_invalid", "occurrence key 无效。", 500);
  const currentTime = new Date(nowValue(now)).getTime();
  if (!Number.isFinite(currentTime)) throw new ScheduleError("occurrence_invalid", "now 无效。");
  const next = clone(schedule);
  const existing = next.occurrences.find((item) => item.key === key);
  if (existing) {
    if (["success", "partial", "failed", "uncertain"].includes(existing.status)) return { schedule: next, acquired: false, status: "duplicate", occurrence: clone(existing) };
    if (existing.status === "running" && new Date(existing.leaseExpiresAt).getTime() > currentTime) return { schedule: next, acquired: false, status: "leased", occurrence: clone(existing) };
    if (existing.status === "running") {
      existing.status = "uncertain";
      existing.uncertainReason = "lease_expired";
      existing.finishedAt = nowValue(now);
      next.lease = null;
      bump(next, now);
      return { schedule: next, acquired: false, status: "uncertain", occurrence: clone(existing) };
    }
  }
  if (next.lease && new Date(next.lease.expiresAt).getTime() > currentTime) return { schedule: next, acquired: false, status: "leased", occurrence: null };
  if (next.lease && new Date(next.lease.expiresAt).getTime() <= currentTime) {
    const previous = next.occurrences.find((item) => item.key === next.lease.occurrenceKey);
    if (previous?.status === "running") { previous.status = "uncertain"; previous.uncertainReason = "lease_expired"; }
    next.lease = null;
  }
  const leaseId = requireString(leaseIdFactory(), "occurrence_lease_invalid", "occurrence lease ID 无效。", 180);
  const occurrence = {
    key,
    status: "running",
    leaseId,
    startedAt: nowValue(now),
    leaseExpiresAt: new Date(currentTime + Math.max(1000, leaseMs)).toISOString(),
    ...(occurrenceMetadata ? {
      scheduledAt: occurrenceMetadata.scheduledAt,
      localDateTime: occurrenceMetadata.localDateTime,
      fold: occurrenceMetadata.fold,
    } : {}),
  };
  next.occurrences = [ ...next.occurrences, occurrence ].slice(-MAX_OCCURRENCES);
  next.lease = { occurrenceKey: key, leaseId, expiresAt: occurrence.leaseExpiresAt };
  bump(next, now);
  return { schedule: next, acquired: true, status: "acquired", occurrence: clone(occurrence) };
}

export function completeOccurrence(schedule, occurrenceKey, { status, result, leaseId, now = () => new Date().toISOString() } = {}) {
  validateSchedule(schedule);
  if (!TERMINAL_OCCURRENCE_STATES.includes(status)) throw new ScheduleError("occurrence_status_invalid", "完成 occurrence 只能使用终态。", { status, allowed: TERMINAL_OCCURRENCE_STATES });
  const next = clone(schedule);
  const occurrence = next.occurrences.find((item) => item.key === occurrenceKey);
  if (!occurrence) throw new ScheduleError("occurrence_not_found", "occurrence 不存在。");
  if (typeof leaseId !== "string" || !leaseId) throw new ScheduleError("occurrence_lease_required", "完成 occurrence 必须提供 lease ID。");
  if (occurrence.status !== "running") throw new ScheduleError("occurrence_lease_conflict", "occurrence 已经结束，旧执行者不能再次提交结果。");
  if (occurrence.leaseId !== leaseId || next.lease?.occurrenceKey !== occurrenceKey || next.lease?.leaseId !== leaseId) throw new ScheduleError("occurrence_lease_conflict", "occurrence lease 不匹配。");
  const currentTime = new Date(nowValue(now)).getTime();
  const occurrenceExpiry = new Date(occurrence.leaseExpiresAt).getTime();
  const scheduleExpiry = new Date(next.lease.expiresAt).getTime();
  if (!Number.isFinite(currentTime) || !Number.isFinite(occurrenceExpiry) || !Number.isFinite(scheduleExpiry)) throw new ScheduleError("occurrence_lease_invalid", "occurrence lease 时间无效。");
  if (occurrenceExpiry <= currentTime || scheduleExpiry <= currentTime) throw new ScheduleError("occurrence_lease_expired", "occurrence lease 已过期，执行结果不能被接受。");
  occurrence.status = status;
  occurrence.finishedAt = nowValue(now);
  if (result !== undefined) occurrence.result = clone(result);
  if (next.lease?.occurrenceKey === occurrenceKey) next.lease = null;
  bump(next, now);
  return next;
}

export function markOccurrenceUncertain(schedule, occurrenceKey, { leaseId, reason = "lease_expired", now = () => new Date().toISOString() } = {}) {
  validateSchedule(schedule);
  const next = clone(schedule);
  const occurrence = next.occurrences.find((item) => item.key === occurrenceKey);
  if (!occurrence) throw new ScheduleError("occurrence_not_found", "occurrence 不存在。");
  if (leaseId !== undefined && occurrence.leaseId !== leaseId) throw new ScheduleError("occurrence_lease_conflict", "occurrence lease 不匹配。");
  if (occurrence.status !== "running") return next;
  occurrence.status = "uncertain";
  occurrence.uncertainReason = reason;
  occurrence.finishedAt = nowValue(now);
  if (next.lease?.occurrenceKey === occurrenceKey && (!leaseId || next.lease.leaseId === leaseId)) next.lease = null;
  bump(next, now);
  return next;
}

export const recordOccurrence = completeOccurrence;

export async function runScheduledOccurrence(schedule, { scene, occurrenceKey, scheduledAt, localDateTime, fold, now = () => new Date().toISOString(), readScene, execute, leaseMs = DEFAULT_LEASE_MS, signal } = {}) {
  let current = clone(schedule);
  const metadata = normalizeOccurrenceMetadata(current, { scheduledAt, localDateTime, fold });
  occurrenceKey = metadata.key;
  const runnable = scheduleRunnable(current, { scene: scene ?? (typeof readScene === "function" ? await readScene(current.sceneId) : undefined) });
  if (!runnable.ok) return { status: "blocked", reason: runnable.reason, schedule: current, occurrenceKey };
  const lease = acquireOccurrence(current, occurrenceKey, { now, leaseMs, occurrenceMetadata: metadata });
  current = lease.schedule;
  if (!lease.acquired) return { status: lease.status, schedule: current, occurrenceKey, occurrence: lease.occurrence };
  if (typeof execute !== "function") {
    current = completeOccurrence(current, occurrenceKey, { status: "uncertain", leaseId: lease.occurrence.leaseId, result: { code: "executor_unavailable" }, now });
    return { status: "uncertain", schedule: current, occurrenceKey };
  }
  try {
    const result = await execute({ schedule: clone(current), scene: clone(scene), occurrenceKey, signal });
    const status = result?.status === undefined ? "success" : result.status;
    if (!TERMINAL_OCCURRENCE_STATES.includes(status)) throw new ScheduleError("occurrence_status_invalid", "executor 返回了非终态 occurrence 状态。", { status });
    current = completeOccurrence(current, occurrenceKey, { status, leaseId: lease.occurrence.leaseId, result, now });
    return { status, schedule: current, occurrenceKey, result };
  } catch (error) {
    try {
      current = completeOccurrence(current, occurrenceKey, { status: "uncertain", leaseId: lease.occurrence.leaseId, result: { code: "execution_uncertain", message: String(error?.message ?? error) }, now });
    } catch (completionError) {
      if (!["occurrence_lease_expired", "occurrence_lease_conflict", "occurrence_lease_required"].includes(completionError?.code)) throw completionError;
      current = markOccurrenceUncertain(current, occurrenceKey, { leaseId: lease.occurrence.leaseId, reason: completionError.code, now });
    }
    return { status: "uncertain", schedule: current, occurrenceKey, error };
  }
}

export function pauseSchedulesForSceneRevision(schedules, scene, { now = () => new Date().toISOString() } = {}) {
  return (Array.isArray(schedules) ? schedules : []).map((schedule) => {
    if (schedule.sceneId !== scene?.id || (schedule.status !== "active" && schedule.state !== "enabled") || schedule.sceneRevision === scene.revision) return clone(schedule);
    const next = clone(schedule);
    next.status = "paused";
    next.state = "paused";
    next.lifecycle = "paused_reconfirmation_required";
    next.enabled = false;
    next.bindingState = "bound";
    bump(next, now);
    return next;
  });
}

export const __testing = { clone, identityOf, nowValue, normalizeTarget, normalizeScenePin, requestKey };
