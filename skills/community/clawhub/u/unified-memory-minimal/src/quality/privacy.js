/**
 * Memory Privacy - 隐私计算
 * 
 * 支持：
 * - 本地加密
 * - 差分隐私
 * - 隐私检索
 * 
 * Ported from memory_privacy.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { createHash, randomBytes } from 'crypto';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const PRIVACY_DIR = join(MEMORY_DIR, 'privacy');

// ============================================================
// PrivacyComputing
// ============================================================

export class PrivacyComputing {
  constructor(key = null) {
    mkdirSync(PRIVACY_DIR, { recursive: true });
    this.keyFile = join(PRIVACY_DIR, '.key');
    this.key = key || this._loadOrCreateKey();
    this.fernet = null;
    this._initEncryptor();
  }

  _loadOrCreateKey() {
    if (existsSync(this.keyFile)) {
      return readFileSync(this.keyFile);
    }
    const key = randomBytes(32); // 256-bit
    writeFileSync(this.keyFile, key);
    // chmod 0o600 equivalent - only owner can read
    return key;
  }

  _initEncryptor() {
    // In production would use Node crypto module
    this.fernet = null;
  }

  _xorEncrypt(data, key) {
    const keyBytes = Buffer.from(key);
    const dataBytes = Buffer.from(data);
    const encrypted = Buffer.alloc(dataBytes.length);
    for (let i = 0; i < dataBytes.length; i++) {
      encrypted[i] = dataBytes[i] ^ keyBytes[i % keyBytes.length];
    }
    return encrypted.toString('base64');
  }

  _xorDecrypt(encrypted, key) {
    const encryptedBytes = Buffer.from(encrypted, 'base64');
    const keyBytes = Buffer.from(key);
    const decrypted = Buffer.alloc(encryptedBytes.length);
    for (let i = 0; i < encryptedBytes.length; i++) {
      decrypted[i] = encryptedBytes[i] ^ keyBytes[i % keyBytes.length];
    }
    return decrypted.toString('utf-8');
  }

  encrypt(text) {
    if (this.fernet) {
      // Production: use crypto module for proper encryption
      const encrypted = Buffer.from(text).toString('base64');
      return encrypted;
    }
    return this._xorEncrypt(text, this.key);
  }

  decrypt(encrypted) {
    if (this.fernet) {
      return Buffer.from(encrypted, 'base64').toString('utf-8');
    }
    return this._xorDecrypt(encrypted, this.key);
  }

  encryptMemory(memory) {
    const encrypted = { ...memory };
    if (memory.text !== undefined) {
      encrypted.textEncrypted = this.encrypt(memory.text);
      encrypted.text = null;
      encrypted.isEncrypted = true;
    }
    return encrypted;
  }

  decryptMemory(encryptedMemory) {
    if (!encryptedMemory.isEncrypted) return encryptedMemory;
    const decrypted = { ...encryptedMemory };
    if (encryptedMemory.textEncrypted) {
      decrypted.text = this.decrypt(encryptedMemory.textEncrypted);
      decrypted.textEncrypted = null;
      decrypted.isEncrypted = false;
    }
    return decrypted;
  }
}

// ============================================================
// DifferentialPrivacy
// ============================================================

export class DifferentialPrivacy {
  constructor(epsilon = 1.0) {
    this.epsilon = epsilon;
  }

  /**
   * Add Laplace noise
   * @param {number} value
   * @param {number} sensitivity
   */
  addLaplaceNoise(value, sensitivity = 1.0) {
    // Simple approximation of Laplace distribution
    const u = Math.random() - 0.5;
    const noise = -sensitivity / this.epsilon * Math.sign(u) * Math.log(1 - 2 * Math.abs(u));
    return value + noise;
  }

  addNoiseToVector(vector, sensitivity = 1.0) {
    return vector.map(v => this.addLaplaceNoise(v, sensitivity));
  }

  noisyCount(trueCount, sensitivity = 1.0) {
    return Math.max(0, Math.round(this.addLaplaceNoise(trueCount, sensitivity)));
  }

  noisyAverage(values, sensitivity = 1.0) {
    if (!values || values.length === 0) return 0;
    const trueAvg = values.reduce((a, b) => a + b, 0) / values.length;
    return this.addLaplaceNoise(trueAvg, sensitivity / values.length);
  }

  privateHistogram(values, bins = 10) {
    // Simple binning with noise
    const min = Math.min(...values);
    const max = Math.max(...values);
    const binWidth = (max - min) / bins;
    const counts = new Array(bins).fill(0);

    for (const v of values) {
      const binIdx = Math.min(Math.floor((v - min) / binWidth), bins - 1);
      counts[binIdx]++;
    }

    const noisyCounts = counts.map(c => this.noisyCount(c, sensitivity = 1.0));

    return { bins, counts: noisyCounts, epsilon: this.epsilon };
  }
}

// ============================================================
// PrivacySearch
// ============================================================

export class PrivacySearch {
  constructor(privacy) {
    this.privacy = privacy;
  }

  searchableEncrypt(text, keywords = null) {
    if (!keywords) keywords = this._extractKeywords(text);
    return {
      encryptedText: this.privacy.encrypt(text),
      keywords,
      keywordHashes: keywords.map(kw => createHash('sha256').update(kw).digest('hex').slice(0, 16))
    };
  }

  _extractKeywords(text) {
    const words = text.replace(/[,。！]/g, ' ').split(/\s+/);
    const stopwords = new Set(['的', '了', '是', '在', '和', '与', '或', '以及', '等', '这', '那']);
    const keywords = words.filter(w => !stopwords.has(w) && w.length > 1);
    return [...new Set(keywords)].slice(0, 10);
  }

  _hashKeyword(keyword) {
    return createHash('sha256').update(keyword).digest('hex').slice(0, 16);
  }

  search(query, encryptedItems) {
    const queryKeywords = this._extractKeywords(query);
    const queryHashes = queryKeywords.map(kw => this._hashKeyword(kw));

    /** @type {Array} */
    const results = [];

    for (const item of encryptedItems) {
      const itemHashes = new Set(item.keywordHashes || []);
      const queryHashSet = new Set(queryHashes);
      const overlap = [...itemHashes].filter(h => queryHashSet.has(h));

      if (overlap.length > 0) {
        results.push({
          ...item,
          matchScore: overlap.length / Math.max(itemHashes.size, queryHashSet.size)
        });
      }
    }

    results.sort((a, b) => (b.matchScore || 0) - (a.matchScore || 0));
    return results;
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdPrivacy(command, args) {
  const privacy = new PrivacyComputing();

  switch (command) {
    case 'encrypt': {
      if (!args.text) return { error: '请提供 --text' };
      const encrypted = privacy.encrypt(args.text);
      return {
        type: 'text',
        text: `🔐 加密结果:\n   原文: ${args.text}\n   密文: ${encrypted.slice(0, 50)}...`
      };
    }

    case 'decrypt': {
      if (!args.ciphertext) return { error: '请提供 --ciphertext' };
      try {
        const decrypted = privacy.decrypt(args.ciphertext);
        return {
          type: 'text',
          text: `🔓 解密结果:\n   密文: ${args.ciphertext.slice(0, 50)}...\n   原文: ${decrypted}`
        };
      } catch {
        return { error: '解密失败' };
      }
    }

    case 'dp': {
      // Differential privacy demo
      const dp = new DifferentialPrivacy(parseFloat(args.epsilon) || 1.0);
      const values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
      const noisyValues = values.map(v => Math.round(dp.addLaplaceNoise(v) * 100) / 100);
      return {
        type: 'text',
        text: `📊 差分隐私演示:\n   真实值: ${values.join(', ')}\n   加噪后: ${noisyValues.join(', ')}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { PrivacyComputing, DifferentialPrivacy, PrivacySearch, cmdPrivacy };
