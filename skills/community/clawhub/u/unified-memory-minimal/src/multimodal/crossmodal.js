/**
 * Memory Crossmodal - 跨模态记忆
 * 
 * Ported from memory_crossmodal.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const CROSSMODAL_DIR = join(MEMORY_DIR, 'crossmodal');

// ============================================================
// CrossmodalMemory
// ============================================================

export class CrossmodalMemory {
  constructor() {
    mkdirSync(CROSSMODAL_DIR, { recursive: true });
    this.indexFile = join(CROSSMODAL_DIR, 'index.json');
    this.index = this._loadIndex();
  }

  _loadIndex() {
    if (existsSync(this.indexFile)) {
      try { return JSON.parse(readFileSync(this.indexFile, 'utf-8')); } catch { /* ignore */ }
    }
    return { texts: [], images: [], audio: [], crossrefs: [] };
  }

  _saveIndex() {
    writeFileSync(this.indexFile, JSON.stringify(this.index, null, 2), 'utf-8');
  }

  /**
   * Link text and image
   * @param {string} text
   * @param {string} imageRef
   * @param {object} metadata
   */
  linkTextImage(text, imageRef, metadata = {}) {
    const refId = `xref_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    this.index.texts.push({ id: refId, text, type: 'text', timestamp: new Date().toISOString() });
    this.index.images.push({ id: refId, imageRef, type: 'image', metadata, timestamp: new Date().toISOString() });
    this.index.crossrefs.push({ textId: refId, imageId: refId });
    this._saveIndex();
    return refId;
  }

  /**
   * Get cross references for a text
   * @param {string} textId
   */
  getCrossReferences(textId) {
    const xref = this.index.crossrefs.find(x => x.textId === textId);
    if (!xref) return null;

    const text = this.index.texts.find(t => t.id === textId);
    const image = this.index.images.find(i => i.id === xref.imageId);

    return { text, image };
  }

  /**
   * Search across modalities
   * @param {string} query
   */
  searchCrossmodal(query) {
    const queryLower = query.toLowerCase();
    const results = [];

    // Search in texts
    for (const entry of this.index.texts) {
      if ((entry.text || '').toLowerCase().includes(queryLower)) {
        results.push({ ...entry, modality: 'text' });
      }
    }

    // Search in image metadata
    for (const entry of this.index.images) {
      const metaText = JSON.stringify(entry.metadata || {}).toLowerCase();
      if (metaText.includes(queryLower)) {
        results.push({ ...entry, modality: 'image' });
      }
    }

    return results;
  }

  getStats() {
    return {
      texts: this.index.texts.length,
      images: this.index.images.length,
      crossrefs: this.index.crossrefs.length
    };
  }
}

export default { CrossmodalMemory };
