import { validateCanvasAst } from "./canvas-validator.mjs";

export const STREAM_SCHEMA_VERSION = "2.0";

export const STREAM_LIMITS = Object.freeze({
  eventBytes: 64 * 1024,
  idChars: 128,
  textDeltaChars: 8 * 1024,
  turnTextChars: 256 * 1024,
  argSummaryChars: 96,
  resultSummaryChars: 2 * 1024,
  fallbackTextChars: 2 * 1024,
  chipsPerTurn: 64,
});

const EVENT_FIELDS = Object.freeze({
  turn_start: ["schemaVersion", "type", "turnId", "seq", "shape"],
  text_delta: ["schemaVersion", "type", "turnId", "seq", "text"],
  tool_call: ["schemaVersion", "type", "turnId", "seq", "callId", "toolId", "argSummary"],
  tool_result: ["schemaVersion", "type", "turnId", "seq", "callId", "status", "summary"],
  artifact: ["schemaVersion", "type", "turnId", "seq", "artifactId", "kind", "body"],
  turn_end: ["schemaVersion", "type", "turnId", "seq", "status", "fallbackText"],
});

const TERMINAL_STATUSES = new Set(["success", "error", "stopped"]);

export function createStreamState() {
  return { schemaVersion: STREAM_SCHEMA_VERSION, turns: {}, order: [] };
}

function failure(state, code, message, path) {
  return {
    state,
    accepted: false,
    error: { code, message, ...(path ? { path } : {}) },
  };
}

function ignored(state, reason) {
  return { state, accepted: false, ignoredReason: reason };
}

function success(state) {
  return { state, accepted: true };
}

function cloneState(state) {
  return structuredClone(state);
}

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function validId(value) {
  return typeof value === "string"
    && value.length > 0
    && value.length <= STREAM_LIMITS.idChars
    && !/\s/u.test(value);
}

function validateString(value, field, max, state, { allowEmpty = false } = {}) {
  if (typeof value !== "string" || (!allowEmpty && value.length === 0) || value.length > max) {
    return failure(state, "INVALID_FIELD", `${field} must be ${allowEmpty ? "at most" : "1 to"} ${max} characters`, field);
  }
  return null;
}

function validateEnvelope(state, event) {
  if (!isPlainObject(event)) {
    return failure(state, "INVALID_EVENT", "Event must be a JSON object");
  }

  let encoded;
  try {
    encoded = JSON.stringify(event);
  } catch {
    return failure(state, "INVALID_EVENT", "Event must be JSON serializable");
  }
  if (encoded === undefined || new TextEncoder().encode(encoded).length > STREAM_LIMITS.eventBytes) {
    return failure(state, "EVENT_TOO_LARGE", `Event exceeds ${STREAM_LIMITS.eventBytes} bytes`);
  }
  if (event.schemaVersion !== STREAM_SCHEMA_VERSION) {
    return failure(state, "INCOMPATIBLE_VERSION", `Expected schemaVersion ${STREAM_SCHEMA_VERSION}`, "schemaVersion");
  }
  if (!Object.hasOwn(EVENT_FIELDS, event.type)) {
    return failure(state, "UNKNOWN_EVENT", "Unknown event type", "type");
  }
  if (!validId(event.turnId)) {
    return failure(state, "INVALID_FIELD", "turnId must be a non-whitespace identifier of at most 128 characters", "turnId");
  }
  if (!Number.isSafeInteger(event.seq) || event.seq < 0) {
    return failure(state, "INVALID_FIELD", "seq must be a non-negative safe integer", "seq");
  }

  const allowed = new Set(EVENT_FIELDS[event.type]);
  const extra = Object.keys(event).filter((key) => !allowed.has(key));
  if (extra.length > 0) {
    return failure(state, "UNEXPECTED_FIELD", "Event contains an unexpected field", "$event");
  }
  return null;
}

function validateTypeFields(state, event) {
  if (event.type === "turn_start") {
    if (event.seq !== 0) return failure(state, "INVALID_SEQUENCE", "turn_start must use seq 0", "seq");
    if (!new Set(["text", "canvas"]).has(event.shape)) {
      return failure(state, "INVALID_FIELD", "shape must be text or canvas", "shape");
    }
  }
  if (event.type === "text_delta") {
    return validateString(event.text, "text", STREAM_LIMITS.textDeltaChars, state);
  }
  if (event.type === "tool_call") {
    if (!validId(event.callId)) return failure(state, "INVALID_FIELD", "callId is invalid", "callId");
    if (!validId(event.toolId)) return failure(state, "INVALID_FIELD", "toolId is invalid", "toolId");
    return validateString(event.argSummary, "argSummary", STREAM_LIMITS.argSummaryChars, state);
  }
  if (event.type === "tool_result") {
    if (!validId(event.callId)) return failure(state, "INVALID_FIELD", "callId is invalid", "callId");
    if (!new Set(["success", "error"]).has(event.status)) {
      return failure(state, "INVALID_FIELD", "tool_result status must be success or error", "status");
    }
    return validateString(event.summary, "summary", STREAM_LIMITS.resultSummaryChars, state);
  }
  if (event.type === "artifact") {
    if (!validId(event.artifactId)) return failure(state, "INVALID_FIELD", "artifactId is invalid", "artifactId");
    if (event.kind !== "canvas") return failure(state, "INVALID_FIELD", "kind must be canvas", "kind");
  }
  if (event.type === "turn_end") {
    if (!TERMINAL_STATUSES.has(event.status)) {
      return failure(state, "INVALID_FIELD", "turn_end status must be success, error, or stopped", "status");
    }
    if (event.fallbackText !== undefined) {
      return validateString(event.fallbackText, "fallbackText", STREAM_LIMITS.fallbackTextChars, state);
    }
  }
  return null;
}

/**
 * Apply one renderer event without mutating the state or event.
 * Rejected transitions return the original state. Events after turn_end are ignored.
 */
export function reduceStreamEvent(state, event) {
  if (!isPlainObject(state) || state.schemaVersion !== STREAM_SCHEMA_VERSION
      || !isPlainObject(state.turns) || !Array.isArray(state.order)) {
    return failure(state, "INVALID_STATE", "State was not created by createStreamState");
  }

  const knownTurnId = isPlainObject(event) && validId(event.turnId) ? event.turnId : null;
  const knownTurn = knownTurnId && Object.hasOwn(state.turns, knownTurnId) ? state.turns[knownTurnId] : null;
  if (knownTurn && knownTurn.status !== "active") {
    return ignored(state, "turn_already_terminal");
  }

  const envelopeError = validateEnvelope(state, event);
  if (envelopeError) return envelopeError;

  const existing = Object.hasOwn(state.turns, event.turnId) ? state.turns[event.turnId] : null;
  if (existing && existing.status !== "active") {
    return ignored(state, "turn_already_terminal");
  }

  const typeError = validateTypeFields(state, event);
  if (typeError) return typeError;

  if (event.type === "turn_start") {
    if (existing) return failure(state, "DUPLICATE_TURN", "turnId already exists", "turnId");
    const next = cloneState(state);
    next.order.push(event.turnId);
    Object.defineProperty(next.turns, event.turnId, { enumerable: true, configurable: true, writable: true, value: {
      shape: event.shape,
      status: "active",
      lastSeq: 0,
      text: "",
      bufferedText: "",
      chips: [],
      artifact: null,
      fallbackText: null,
    } });
    return success(next);
  }

  if (!existing) return failure(state, "ORPHAN_EVENT", "turn_start must be the first event for a turn", "turnId");
  if (event.seq !== existing.lastSeq + 1) {
    return failure(state, "INVALID_SEQUENCE", `Expected seq ${existing.lastSeq + 1}`, "seq");
  }

  const next = cloneState(state);
  const turn = next.turns[event.turnId];

  if (event.type === "text_delta") {
    const field = turn.shape === "text" ? "text" : "bufferedText";
    if (turn[field].length + event.text.length > STREAM_LIMITS.turnTextChars) {
      return failure(state, "TURN_TEXT_TOO_LARGE", `Turn text exceeds ${STREAM_LIMITS.turnTextChars} characters`, "text");
    }
    turn[field] += event.text;
  }

  if (event.type === "tool_call") {
    if (turn.chips.length >= STREAM_LIMITS.chipsPerTurn) {
      return failure(state, "TOO_MANY_TOOL_CALLS", `Turn exceeds ${STREAM_LIMITS.chipsPerTurn} tool chips`);
    }
    if (turn.chips.some((chip) => chip.callId === event.callId)) {
      return failure(state, "DUPLICATE_CALL", "callId already exists", "callId");
    }
    turn.chips.push({
      callId: event.callId,
      toolId: event.toolId,
      argSummary: event.argSummary,
      status: "pending",
      summary: null,
    });
  }

  if (event.type === "tool_result") {
    const chip = turn.chips.find((candidate) => candidate.callId === event.callId);
    if (!chip) return failure(state, "ORPHAN_TOOL_RESULT", "tool_result has no matching tool_call", "callId");
    if (chip.status !== "pending") return failure(state, "DUPLICATE_TOOL_RESULT", "tool call is already settled", "callId");
    chip.status = event.status;
    chip.summary = event.summary;
  }

  if (event.type === "artifact") {
    if (turn.shape !== "canvas") return failure(state, "SHAPE_MISMATCH", "Text turns cannot emit artifacts", "type");
    if (turn.artifact) return failure(state, "DUPLICATE_ARTIFACT", "Canvas turns can commit only one artifact", "artifactId");
    const checked = validateCanvasAst(event.body);
    if (!checked.ok) {
      return {
        state,
        accepted: false,
        error: { code: "INVALID_CANVAS", message: "Canvas validation failed", path: "body", detailCode: checked.error.code },
      };
    }
    if (checked.canvas.id !== event.artifactId) {
      return failure(state, "ARTIFACT_ID_MISMATCH", "artifactId must match body.id", "artifactId");
    }
    turn.artifact = { artifactId: event.artifactId, kind: event.kind, body: structuredClone(checked.canvas) };
  }

  if (event.type === "turn_end") {
    const pending = turn.chips.filter((chip) => chip.status === "pending");
    if (event.status === "success" && pending.length > 0) {
      return failure(state, "PENDING_TOOL_CALLS", "A successful turn cannot end with pending tool calls");
    }
    if (turn.shape === "canvas") {
      if (event.status === "success" && !turn.artifact) {
        return failure(state, "MISSING_ARTIFACT", "A successful canvas turn requires one artifact");
      }
      if (!turn.artifact && event.status === "error" && event.fallbackText === undefined) {
        return failure(state, "MISSING_FALLBACK", "A failed canvas turn requires fallbackText", "fallbackText");
      }
      if (event.fallbackText !== undefined && (turn.artifact || event.status !== "error")) {
        return failure(state, "INVALID_FALLBACK", "fallbackText is only valid for a failed canvas turn with no artifact", "fallbackText");
      }
    } else if (event.fallbackText !== undefined) {
      return failure(state, "INVALID_FALLBACK", "Text turns cannot emit fallbackText", "fallbackText");
    }
    if (event.status !== "success") {
      for (const chip of pending) {
        chip.status = "interrupted";
        chip.summary = event.status === "stopped" ? "Stopped before completion" : "Turn ended before completion";
      }
    }
    turn.status = event.status;
    turn.fallbackText = event.fallbackText ?? null;
  }

  turn.lastSeq = event.seq;
  return success(next);
}
