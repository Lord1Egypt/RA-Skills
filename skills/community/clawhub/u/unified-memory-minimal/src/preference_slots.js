/**
 * preference_slots.js — Structured Preference Slots for unified-memory v1.2
 * Provides typed key-value user preferences that boost relevant memories in search.
 * MCP tool: memory_preference_slots (get/update/merge/reset/delete/stats)
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.OPENCLAW_WORKSPACE_DIR ?? join(process.env.HOME ?? '/root', '.openclaw', 'workspace');
const SKILL_DIR = join(WORKSPACE, 'memory');
const SLOTS_FILE = join(SKILL_DIR, 'preference_slots.json');

const DEFAULT_SLOTS = {
  communication_style: { value: 'balanced',  type: 'string', updated_at: Date.now() },
  timezone:             { value: 'Asia/Shanghai', type: 'string', updated_at: Date.now() },
  language:             { value: 'zh',        type: 'string', updated_at: Date.now() },
  response_length:      { value: 'medium',    type: 'string', updated_at: Date.now() },
  formality_level:      { value: 'semi-formal', type: 'string', updated_at: Date.now() },
  notification_level:   { value: 'normal',    type: 'string', updated_at: Date.now() },
};

let slotsCache = null;

function loadSlots() {
  if (slotsCache) return slotsCache;
  if (!existsSync(SLOTS_FILE)) { slotsCache = { ...DEFAULT_SLOTS }; persist(slotsCache); return slotsCache; }
  try { slotsCache = { ...DEFAULT_SLOTS, ...JSON.parse(readFileSync(SLOTS_FILE, 'utf8')) }; }
  catch { slotsCache = { ...DEFAULT_SLOTS }; }
  return slotsCache;
}

function persist(slots) {
  try { writeFileSync(SLOTS_FILE, JSON.stringify(slots, null, 2), 'utf8'); }
  catch (err) { console.error('[preference_slots] persist error:', err.message); }
}

export function getSlots() {
  return Object.fromEntries(Object.entries(loadSlots()).map(([k, v]) => [k, v.value]));
}

export function getSlot(key) { return loadSlots()[key]?.value ?? null; }

export function updateSlot(key, value) {
  const slots = loadSlots();
  slots[key] = { value: String(value), type: 'string', updated_at: Date.now() };
  persist(slots);
  return { success: true, slot: { key, ...slots[key] } };
}

export function mergeSlots(updates) {
  const slots = loadSlots();
  let count = 0;
  for (const [key, value] of Object.entries(updates)) {
    slots[key] = { value: String(value), type: 'string', updated_at: Date.now() };
    count++;
  }
  persist(slots);
  return { success: true, updated: count };
}

export function resetSlots() { slotsCache = { ...DEFAULT_SLOTS }; persist(slotsCache); return { success: true }; }

export function deleteSlot(key) {
  const slots = loadSlots();
  if (key in DEFAULT_SLOTS) slots[key] = { ...DEFAULT_SLOTS[key] };
  else delete slots[key];
  persist(slots);
  return { success: true };
}

/** Boost score [0.5 – 2.0] based on preference–memory alignment */
export function getPreferenceBoost(query, category = '', tags = []) {
  const slots = loadSlots();
  const q = query.toLowerCase();
  let b = 1.0;
  if (slots.language?.value === 'zh' && /[\u4e00-\u9fa5]/.test(q)) b *= 1.15;
  if (slots.language?.value === 'en' && !/[\u4e00-\u9fa5]/.test(q)) b *= 1.15;
  if (slots.communication_style?.value === 'concise' && q.length < 40) b *= 1.1;
  if (slots.communication_style?.value === 'detailed' && q.length > 80) b *= 1.1;
  const catSlot = { preference: 'communication_style', fact: 'timezone', decision: 'language', entity: 'language', reflection: 'formality_level' };
  if (catSlot[category] && slots[catSlot[category]]) b *= 1.05;
  const preferred = tags.filter(t => [slots.communication_style?.value, slots.language?.value, slots.timezone?.value].includes(t));
  if (preferred.length > 0) b *= 1 + preferred.length * 0.05;
  return Math.min(b, 2.0);
}

export function memoryPreferenceSlotsTool({ action, key, value, slots: slotMap } = {}) {
  try {
    switch (action) {
      case 'get':    return { content: [{ type: 'text', text: JSON.stringify({ success: true, slots: getSlots() }, null, 2) }] };
      case 'update': if (!key) throw new Error('key required'); return { content: [{ type: 'text', text: JSON.stringify(updateSlot(key, value), null, 2) }] };
      case 'merge':  if (!slotMap) throw new Error('slots object required'); return { content: [{ type: 'text', text: JSON.stringify(mergeSlots(slotMap), null, 2) }] };
      case 'delete': if (!key) throw new Error('key required'); return { content: [{ type: 'text', text: JSON.stringify(deleteSlot(key), null, 2) }] };
      case 'reset':  return { content: [{ type: 'text', text: JSON.stringify(resetSlots(), null, 2) }] };
      case 'stats': {
        const s = loadSlots();
        return { content: [{ type: 'text', text: JSON.stringify({ total: Object.keys(s).length, defaults: Object.keys(DEFAULT_SLOTS).length, slots: s }, null, 2) }] };
      }
      default:
        return { content: [{ type: 'text', text: JSON.stringify({ error: `Unknown action: ${action}`, hint: 'get/update/merge/delete/reset/stats' }, null, 2) }], isError: true };
    }
  } catch (err) { return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true }; }
}

export default { getSlots, getSlot, updateSlot, mergeSlots, resetSlots, deleteSlot, getPreferenceBoost, memoryPreferenceSlotsTool };
