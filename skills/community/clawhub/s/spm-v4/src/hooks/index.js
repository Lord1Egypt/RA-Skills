// @ts-check

/**
 * Central hook registry and middleware runner for SPM v4.
 *
 * Hooks provide a plugin-like mechanism for intercepting tool calls and
 * phase transitions.  Each hook is registered by name with a handler
 * function and one of four event types:
 *
 * - **preToolUse**   — Invoked before a tool call.  May mutate context.
 * - **postToolUse**  — Invoked after a tool call.  Receives the result.
 * - **onPhaseEnter** — Invoked when a phase is entered.
 * - **onPhaseExit**  — Invoked when a phase is exited.
 *
 * Handlers are called in registration order.  All handlers are async;
 * the runner awaits each one in series.
 *
 * @module hooks/index
 */

/**
 * @typedef {Object} HookDescriptor
 * @property {string}       name    – Unique hook name
 * @property {HookHandler}  handler – Async handler function
 * @property {HookEvent}    event   – Event type this hook is registered for
 */

/**
 * @callback HookHandler
 * @param {Object} context – Mutable context object (event-type-specific shape)
 * @returns {Promise<void>}
 */

/** "preToolUse" | "postToolUse" | "onPhaseEnter" | "onPhaseExit" */
const HOOK_TYPES = /** @type {const} */ ([
  'preToolUse',
  'postToolUse',
  'onPhaseEnter',
  'onPhaseExit',
]);

/**
 * @typedef {'preToolUse'|'postToolUse'|'onPhaseEnter'|'onPhaseExit'} HookEvent
 */

/** @type {Map<HookEvent, HookDescriptor[]>} */
const registry = new Map();

// Initialise empty slot for each event type.
for (const t of HOOK_TYPES) {
  registry.set(t, []);
}

/**
 * Register a hook handler.
 *
 * The handler will be invoked when the given event type fires.
 *
 * @param {string}          name    – Unique identifier for this hook
 * @param {HookHandler}     handler – Async function receiving a mutable context
 * @param {HookEvent}       event   – Event type to attach to
 * @throws {Error} If a hook with the same name is already registered for *any* event type
 */
export function register(name, handler, event = 'preToolUse') {
  if (!HOOK_TYPES.includes(event)) {
    throw new Error(
      `Unknown hook event "${event}". Valid types: ${HOOK_TYPES.join(', ')}`
    );
  }

  // Enforce unique names across all event types so we can look them up easily.
  for (const [, hooks] of registry) {
    if (hooks.some((h) => h.name === name)) {
      throw new Error(`Hook "${name}" is already registered.`);
    }
  }

  const slot = /** @type {HookDescriptor[]} */ (registry.get(event));
  slot.push({ name, handler, event });
}

/**
 * Unregister a hook by name.
 *
 * Removes the hook from whichever event type it belongs to.  This is a
 * no-op when no hook with that name exists.
 *
 * @param {string} name – The name of the hook to remove
 */
export function unregister(name) {
  for (const [, hooks] of registry) {
    const idx = hooks.findIndex((h) => h.name === name);
    if (idx !== -1) {
      hooks.splice(idx, 1);
      return;
    }
  }
}

/**
 * Run all hooks registered for a given event type.
 *
 * Handlers are invoked in registration order and each receives the
 * provided context object.  The context is **mutable** – handlers may
 * enrich or modify it for downstream consumers.
 *
 * @param {HookEvent} event   – The event type to fire
 * @param {Object}    context – Mutable context passed to every handler
 * @returns {Promise<void>}
 */
export async function run(event, context = {}) {
  const hooks = /** @type {HookDescriptor[]} */ (registry.get(event));
  if (!hooks) {
    return;
  }
  for (const hook of hooks) {
    await hook.handler(context);
  }
}

/**
 * Return a snapshot of every currently registered hook, grouped by event
 * type.
 *
 * @returns {Record<HookEvent, string[]>} Map of event → hook names
 */
export function list() {
  /** @type {Record<string, string[]>} */
  const result = {};
  for (const [event, hooks] of registry) {
    result[event] = hooks.map((h) => h.name);
  }
  return /** @type {Record<HookEvent, string[]>} */ (result);
}

/**
 * Remove all registered hooks.
 *
 * Useful for testing or resetting state between workflow runs.
 */
export function clear() {
  for (const [, hooks] of registry) {
    hooks.length = 0;
  }
}