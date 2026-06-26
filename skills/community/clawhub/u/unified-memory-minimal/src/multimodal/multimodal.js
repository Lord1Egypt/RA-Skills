/**
 * Memory Multimodal - 多模态记忆系统
 * 
 * Ported from memory_multimodal.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const MULTIMODAL_DIR = join(MEMORY_DIR, 'multimodal');

// ============================================================
// MultimodalMemory
// ============================================================

export class MultimodalMemory {
  constructor() {
    mkdirSync(MULTIMODAL_DIR, { recursive: true });
    this.storeFile = join(MULTIMODAL_DIR, 'store.json');
    this.store = this._loadStore();
  }

  _loadStore() {
    if (existsSync(this.storeFile)) {
      try { return JSON.parse(readFileSync(this.storeFile, 'utf-8')); } catch { /* ignore */ }
    }
    return { items: [] };
  }

  _saveStore() {
    writeFileSync(this.storeFile, JSON.stringify(this.store, null, 2), 'utf-8');
  }

  /**
   * Store a multimodal memory item
   * @param {object} item
   */
  store(item) {
    const id = item.id || `mm_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const entry = {
      ...item,
      id,
      created_at: new Date().toISOString(),
      modalities: item.modalities || [item.type].filter(Boolean)
    };
    this.store.items.push(entry);
    this._saveStore();
    return id;
  }

  /**
   * Store image with caption
   * @param {string} imageRef
   * @param {string} caption
   * @param {object} metadata
   */
  storeImage(imageRef, caption, metadata = {}) {
    return this.store({
      type: 'image',
      imageRef,
      text: caption,
      modalities: ['visual', 'text'],
      metadata
    });
  }

  /**
   * Store audio with transcript
   * @param {string} audioRef
   * @param {string} transcript
   * @param {object} metadata
   */
  storeAudio(audioRef, transcript, metadata = {}) {
    return this.store({
      type: 'audio',
      audioRef,
      text: transcript,
      modalities: ['audio', 'text'],
      metadata
    });
  }

  /**
   * Search multimodal memories
   * @param {string} query
   * @param {number} limit
   */
  search(query, limit = 20) {
    const queryLower = query.toLowerCase();
    const results = [];

    for (const item of this.store.items) {
      const text = (item.text || '').toLowerCase();
      const metaText = JSON.stringify(item.metadata || {}).toLowerCase();

      if (text.includes(queryLower) || metaText.includes(queryLower)) {
        results.push(item);
      }
    }

    return results.slice(0, limit);
  }

  /**
   * Get memories by type
   * @param {string} type
   */
  getByType(type) {
    return this.store.items.filter(item => item.type === type);
  }

  /**
   * Get stats
   */
  getStats() {
    const byType = {};
    for (const item of this.store.items) {
      byType[item.type] = (byType[item.type] || 0) + 1;
    }
    return { total: this.store.items.length, by_type: byType };
  }
}

export default { MultimodalMemory };
