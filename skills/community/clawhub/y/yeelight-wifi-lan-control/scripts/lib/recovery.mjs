import { randomUUID } from "node:crypto";
import { stableStringify } from "./scenes.mjs";

export const RECOVERY_SCHEMA_VERSION = 1;
export const RECOVERY_KIND = "scene-apply";
export const RECOVERY_CONFIRMATION = "确认恢复场景操作";
export const RECOVERY_TTL_MS = 30 * 60 * 1000;
export const MAX_RECOVERY_RECORDS = 32;
export const MAX_RECOVERY_TARGETS = 256;

const NON_IDEMPOTENT_METHODS = new Set([
  "toggle", "dev_toggle", "bg_toggle", "adjust_bright", "adjust_ct", "adjust_color",
  "bg_adjust_bright", "bg_adjust_ct", "bg_adjust_color", "start_cf", "stop_cf",
  "bg_start_cf", "bg_stop_cf",
]);

export class RecoveryError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "RecoveryError";
    this.code = code;
    this.details = details;
  }
}

const clone = (value) => value === undefined ? undefined : structuredClone(value);
const identityOf = (value) => typeof value === "string" || typeof value === "number" ? String(value) : value?.deviceId ?? value?.id ?? value?.protocolId ?? null;

function nowValue(now) {
  return typeof now === "function" ? now() : (now ?? new Date().toISOString());
}

function requireId(value, code = "recovery_target_invalid") {
  const id = identityOf(value);
  if (typeof id !== "string" || !id.trim() || id.length > 160) throw new RecoveryError(code, "恢复目标 ID 无效。");
  return id.trim();
}

function normalizeState(value) {
  if (value === null || value === undefined) return null;
  if (typeof value !== "object" || Array.isArray(value)) throw new RecoveryError("recovery_state_invalid", "恢复状态必须是对象。");
  return clone(value);
}

function normalizeTarget(raw, index) {
  if (!raw || typeof raw !== "object") throw new RecoveryError("recovery_target_invalid", "恢复目标无效。", { index });
  const deviceId = requireId(raw.deviceId ?? raw.id ?? raw);
  const preState = normalizeState(raw.preState);
  if (!preState || !Object.keys(preState).length) throw new RecoveryError("recovery_pre_state_required", "恢复目标缺少已验证的 pre-state。", { deviceId });
  const action = raw.action ?? raw.requestedAction ?? null;
  const method = typeof action?.method === "string" ? action.method : typeof raw.method === "string" ? raw.method : "";
  return {
    deviceId,
    preState,
    ...(normalizeState(raw.postState ?? raw.expectedState) ? { postState: normalizeState(raw.postState ?? raw.expectedState) } : {}),
    ...(action ? { action: clone(action) } : {}),
    ...(method ? { method } : {}),
    status: "pending",
    touched: false,
    pending: true,
    attempts: 0,
  };
}

export function stateDigest(value) {
  return stableStringify(value ?? null);
}

export function statesEquivalent(expected, actual) {
  if (!expected || !actual || typeof expected !== "object" || typeof actual !== "object") return false;
  return Object.keys(expected).every((key) => stableStringify(expected[key]) === stableStringify(actual[key]));
}

export function isNonIdempotentAction(targetOrAction) {
  const method = typeof targetOrAction === "string" ? targetOrAction : targetOrAction?.method ?? targetOrAction?.action?.method;
  return NON_IDEMPOTENT_METHODS.has(method);
}

export function createRecoveryRecord({
  idFactory = () => `recovery-${randomUUID()}`,
  now = () => new Date().toISOString(),
  sceneId,
  sceneRevision,
  sceneHash,
  operationRef,
  targets,
  context = {},
  ttlMs = RECOVERY_TTL_MS,
} = {}) {
  if (!Array.isArray(targets) || targets.length < 1 || targets.length > MAX_RECOVERY_TARGETS) throw new RecoveryError("recovery_targets_invalid", "恢复记录目标数量无效。");
  const normalizedTargets = targets.map(normalizeTarget);
  const ids = normalizedTargets.map((target) => target.deviceId);
  if (new Set(ids).size !== ids.length) throw new RecoveryError("recovery_target_duplicate", "恢复记录目标不能重复。");
  const createdAt = nowValue(now);
  const id = requireId(idFactory(), "recovery_id_invalid");
  return {
    schemaVersion: RECOVERY_SCHEMA_VERSION,
    id,
    kind: RECOVERY_KIND,
    ...(sceneId ? { sceneId: String(sceneId) } : {}),
    ...(sceneRevision !== undefined ? { sceneRevision } : {}),
    ...(sceneHash ? { sceneHash: String(sceneHash) } : {}),
    ...(operationRef ? { operationRef: String(operationRef) } : {}),
    createdAt,
    updatedAt: createdAt,
    revision: 1,
    expiresAt: new Date(new Date(createdAt).getTime() + Math.max(1, ttlMs)).toISOString(),
    phase: "in_progress",
    status: "pending",
    attempts: 0,
    targets: normalizedTargets,
    deviceIds: ids.slice(),
    touchedDeviceIds: [],
    pendingDeviceIds: ids.slice(),
    ...(Object.keys(context).length ? { context: clone(context) } : {}),
  };
}

export function validateRecoveryRecord(record) {
  if (!record || typeof record !== "object" || record.schemaVersion !== RECOVERY_SCHEMA_VERSION || record.kind !== RECOVERY_KIND) throw new RecoveryError("recovery_record_invalid", "恢复记录结构无效。");
  requireId(record.id, "recovery_id_invalid");
  if (!Array.isArray(record.targets) || record.targets.length < 1 || record.targets.length > MAX_RECOVERY_TARGETS) throw new RecoveryError("recovery_targets_invalid", "恢复记录目标数量无效。");
  const ids = record.targets.map((target) => requireId(target.deviceId));
  if (new Set(ids).size !== ids.length) throw new RecoveryError("recovery_target_duplicate", "恢复记录目标不能重复。");
  if (!Array.isArray(record.pendingDeviceIds) || !Array.isArray(record.touchedDeviceIds)) throw new RecoveryError("recovery_journal_invalid", "恢复记录 journal 无效。");
  if (record.pendingDeviceIds.some((id) => !ids.includes(id)) || record.touchedDeviceIds.some((id) => !ids.includes(id))) throw new RecoveryError("recovery_scope_invalid", "恢复记录 journal 超出目标范围。");
  return true;
}

export function serializeRecoveryRecord(record) {
  validateRecoveryRecord(record);
  return clone(record);
}

export const toDurableRecoveryRecord = serializeRecoveryRecord;

function withOutcome(record, outcome, now) {
  validateRecoveryRecord(record);
  const deviceId = requireId(outcome?.deviceId);
  const index = record.targets.findIndex((target) => target.deviceId === deviceId);
  if (index < 0) throw new RecoveryError("recovery_scope_invalid", "恢复结果超出记录目标范围。", { deviceId });
  const status = String(outcome.status ?? "uncertain");
  const allowed = new Set(["pending", "success", "skipped", "failed", "uncertain", "conflict"]);
  if (!allowed.has(status)) throw new RecoveryError("recovery_status_invalid", "恢复结果状态无效.", { status });
  const next = clone(record);
  const target = next.targets[index];
  target.status = status;
  target.touched = outcome.touched === true || target.touched === true;
  target.pending = status === "pending" || status === "failed" || status === "uncertain" || status === "conflict";
  target.attempts = Math.max(0, Number(target.attempts) || 0) + (outcome.attempted === false ? 0 : 1);
  if (outcome.state !== undefined) target.lastState = normalizeState(outcome.state);
  if (outcome.error !== undefined) target.error = clone(outcome.error);
  if (outcome.postState !== undefined) target.postState = normalizeState(outcome.postState);
  if (target.touched && !next.touchedDeviceIds.includes(deviceId)) next.touchedDeviceIds.push(deviceId);
  next.pendingDeviceIds = next.targets.filter((row) => row.pending).map((row) => row.deviceId);
  next.status = next.pendingDeviceIds.length ? (next.targets.some((row) => row.status === "conflict") ? "conflict" : "uncertain") : "complete";
  next.phase = next.pendingDeviceIds.length ? "recovery" : "complete";
  next.updatedAt = nowValue(now);
  next.revision = Number.isInteger(next.revision) ? next.revision + 1 : 1;
  return next;
}

export function recordRecoveryOutcome(record, outcome, { now = () => new Date().toISOString() } = {}) {
  return withOutcome(record, outcome, now);
}

export const appendRecoveryOutcome = recordRecoveryOutcome;

export function markRecoveryTouched(record, deviceId, details = {}) {
  return withOutcome(record, { ...details, deviceId, touched: true, status: details.status ?? "pending", attempted: false });
}

export function finalizeRecoveryRecord(record, { now = () => new Date().toISOString() } = {}) {
  validateRecoveryRecord(record);
  const next = clone(record);
  next.pendingDeviceIds = next.targets.filter((target) => target.pending).map((target) => target.deviceId);
  next.status = next.pendingDeviceIds.length ? (next.targets.some((target) => target.status === "conflict") ? "conflict" : "uncertain") : "complete";
  next.phase = next.pendingDeviceIds.length ? "recovery" : "complete";
  next.updatedAt = nowValue(now);
  next.revision = Number.isInteger(next.revision) ? next.revision + 1 : 1;
  return next;
}

export function recoveryNeedsAttention(record, now = () => new Date().toISOString()) {
  validateRecoveryRecord(record);
  return record.pendingDeviceIds.length > 0 || new Date(record.expiresAt).getTime() <= new Date(nowValue(now)).getTime();
}

export function createRecoveryJournal({ records = [], maxRecords = MAX_RECOVERY_RECORDS } = {}) {
  const map = new Map();
  for (const record of records instanceof Map ? records.values() : records) {
    validateRecoveryRecord(record);
    map.set(record.id, clone(record));
  }
  const trim = () => {
    while (map.size > maxRecords) {
      const oldest = [...map.values()].sort((a, b) => String(a.updatedAt).localeCompare(String(b.updatedAt)))[0];
      map.delete(oldest.id);
    }
  };
  trim();
  return Object.freeze({
    get(id) { const row = map.get(id); return row ? clone(row) : null; },
    list() { return [...map.values()].map(clone); },
    put(record) { validateRecoveryRecord(record); map.set(record.id, clone(record)); trim(); return clone(record); },
    remove(id) { return map.delete(id); },
    clear() { map.clear(); },
  });
}

function readStateResult(value) {
  if (value && typeof value === "object" && Object.prototype.hasOwnProperty.call(value, "state")) return value;
  return { state: value, fresh: true, verified: true };
}

export async function recoverOperation(record, {
  confirmation,
  readState,
  restoreState,
  persist,
  now = () => new Date().toISOString(),
  expectedConfirmation = RECOVERY_CONFIRMATION,
  signal,
} = {}) {
  validateRecoveryRecord(record);
  if (confirmation !== expectedConfirmation) throw new RecoveryError("recovery_confirmation_required", "恢复操作需要明确确认。", { expectedConfirmation });
  if (typeof readState !== "function") throw new RecoveryError("recovery_reader_required", "恢复操作需要注入 fresh read 钩子。");
  if (typeof restoreState !== "function") throw new RecoveryError("recovery_restorer_required", "恢复操作需要注入恢复写入钩子。");
  const started = finalizeRecoveryRecord(record, { now });
  let next = clone(started);
  if (!next.pendingDeviceIds.length) return { status: "complete", complete: true, record: next, rows: [] };
  const rows = [];
  for (const deviceId of next.pendingDeviceIds.slice()) {
    if (signal?.aborted) {
      next = recordRecoveryOutcome(next, { deviceId, status: "uncertain", error: { code: "aborted" }, attempted: false }, { now });
      rows.push({ deviceId, status: "uncertain", reason: "aborted" });
      continue;
    }
    const target = next.targets.find((row) => row.deviceId === deviceId);
    let observed;
    try {
      observed = readStateResult(await readState(deviceId, clone(target), { signal }));
    } catch (error) {
      next = recordRecoveryOutcome(next, { deviceId, status: "uncertain", error: { code: "fresh_read_failed", message: String(error?.message ?? error) } }, { now });
      rows.push({ deviceId, status: "uncertain", reason: "fresh_read_failed" });
      await persistRecord(persist, next);
      continue;
    }
    const current = observed.state;
    if (observed.fresh === false || observed.verified === false || !current) {
      next = recordRecoveryOutcome(next, { deviceId, status: "uncertain", state: current, error: { code: "fresh_read_untrusted" } }, { now });
      rows.push({ deviceId, status: "uncertain", reason: "fresh_read_untrusted" });
      await persistRecord(persist, next);
      continue;
    }
    if (statesEquivalent(target.preState, current)) {
      next = recordRecoveryOutcome(next, { deviceId, status: "skipped", state: current, touched: target.touched, attempted: false }, { now });
      rows.push({ deviceId, status: "skipped", reason: "already_pre_state" });
      await persistRecord(persist, next);
      continue;
    }
    const expectedPost = target.postState ?? target.expectedState;
    if (!expectedPost || !statesEquivalent(expectedPost, current)) {
      next = recordRecoveryOutcome(next, { deviceId, status: "conflict", state: current, error: { code: "state_drift" } }, { now });
      rows.push({ deviceId, status: "conflict", reason: "state_drift" });
      await persistRecord(persist, next);
      continue;
    }
    try {
      const result = await restoreState(deviceId, clone(target.preState), { signal, recovery: true, nonIdempotentOriginal: isNonIdempotentAction(target) });
      if (result?.status === "failed" || result?.status === "uncertain" || result?.verified === false) {
        next = recordRecoveryOutcome(next, { deviceId, status: result.status === "failed" ? "failed" : "uncertain", state: result.state, error: result.error ?? { code: "restore_unverified" } }, { now });
        rows.push({ deviceId, status: result.status === "failed" ? "failed" : "uncertain", reason: "restore_unverified" });
      } else {
        const finalRead = typeof result?.state === "object" ? result : readStateResult(await readState(deviceId, clone(target), { signal }));
        if (finalRead.fresh === false || finalRead.verified === false || !statesEquivalent(target.preState, finalRead.state)) {
          next = recordRecoveryOutcome(next, { deviceId, status: "uncertain", state: finalRead.state, error: { code: "restore_readback_mismatch" } }, { now });
          rows.push({ deviceId, status: "uncertain", reason: "restore_readback_mismatch" });
        } else {
          next = recordRecoveryOutcome(next, { deviceId, status: "success", state: finalRead.state, postState: target.postState, touched: target.touched }, { now });
          rows.push({ deviceId, status: "success" });
        }
      }
    } catch (error) {
      next = recordRecoveryOutcome(next, { deviceId, status: "uncertain", error: { code: "restore_failed", message: String(error?.message ?? error) } }, { now });
      rows.push({ deviceId, status: "uncertain", reason: "restore_failed" });
    }
    await persistRecord(persist, next);
  }
  next = finalizeRecoveryRecord(next, { now });
  await persistRecord(persist, next);
  return { status: next.status, complete: next.status === "complete", recoveryId: next.status === "complete" ? null : next.id, record: next, rows };
}

async function persistRecord(persist, record) {
  if (typeof persist === "function") await persist(serializeRecoveryRecord(record));
}

export const operationRecover = recoverOperation;
export const recoverRecoveryRecord = recoverOperation;

export const __testing = { NON_IDEMPOTENT_METHODS, normalizeTarget, readStateResult, persistRecord };
