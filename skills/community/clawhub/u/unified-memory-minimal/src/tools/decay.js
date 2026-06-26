/**
 * memory_decay - 记忆时效性智能衰减
 * 基于半衰期的置信度自动衰减系统
 */

import { getAllMemories, saveMemories } from '../storage.js';
import { log } from '../config.js';

const DECAY_RULES = {
  task: { halfLife: 7, rate: 0.1 },
  preference: { halfLife: 30, rate: 0.03 },
  project: { halfLife: 90, rate: 0.02 },
  event: { halfLife: 14, rate: 0.05 },
  fact: { halfLife: 365, rate: 0.005 },
  decision: { halfLife: 180, rate: 0.01 },
  default: { halfLife: 30, rate: 0.03 }
};

const CATEGORY_MAP = {
  task: 'task', todo: 'task', action: 'task',
  preference: 'preference', like: 'preference', habit: 'preference',
  project: 'project',
  event: 'event', meeting: 'event',
  fact: 'fact', knowledge: 'fact', info: 'fact',
  decision: 'decision', choice: 'decision', critical: 'decision',
  other: 'default', legacy: 'default', entity: 'fact', relation: 'fact'
};

function getDecayRule(category) {
  const type = CATEGORY_MAP[category] || 'default';
  return DECAY_RULES[type] || DECAY_RULES.default;
}

function calculateDecay(mem, currentTime) {
  const rule = getDecayRule(mem.category || 'other');
  const created = new Date(mem.created_at || Date.now()).getTime();
  const ageInDays = (currentTime - created) / (1000 * 60 * 60 * 24);
  
  // Exponential decay using half-life
  const importance = mem.importance ?? 0.5;
  const decayFactor = Math.pow(0.5, ageInDays / rule.halfLife);
  const newImportance = Math.max(0.1, importance * decayFactor);
  
  return {
    id: mem.id,
    original: importance,
    new: Math.round(newImportance * 1000) / 1000,
    age_days: Math.round(ageInDays * 10) / 10,
    category: mem.category
  };
}

export async function decayMemories({ apply = false } = {}) {
  const memories = await getAllMemories();
  const currentTime = Date.now();
  
  const decayed = memories.map(mem => calculateDecay(mem, currentTime));
  
  // Stats
  const stats = {
    total: memories.length,
    significantly_decayed: decayed.filter(d => d.new < d.original * 0.5).length,
    slightly_decayed: decayed.filter(d => d.new < d.original * 0.9 && d.new >= d.original * 0.5).length,
    unchanged: decayed.filter(d => d.new >= d.original * 0.9).length
  };
  
  if (apply) {
    const updated = memories.map(mem => {
      const d = decayed.find(x => x.id === mem.id);
      return { ...mem, importance: d.new };
    });
    saveMemories(updated);
    log('INFO', `Applied decay to ${memories.length} memories`);
  }
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({ stats, decayed: decayed.slice(0, 20), applied: apply }, null, 2)
    }]
  };
}
