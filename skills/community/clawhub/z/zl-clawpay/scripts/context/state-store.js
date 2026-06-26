'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const constants = require('../constants');

const STATE_DIR = path.join(os.homedir(), constants.STATE_DIR);
const STATE_FILE = path.join(STATE_DIR, constants.STATE_FILE);

const SECRET_KEYS = ['apiKey'];

class StateStore {
  constructor() {
    this.filePath = STATE_FILE;
    this._cache = null;
    this._machineKey = null;
    this._ensureDir();
  }

  _deriveMachineKey() {
    if (this._machineKey) return this._machineKey;
    const seed = [os.hostname(), os.platform(), os.arch(), 'zl-clawpay-v2'].join(':');
    this._machineKey = crypto.createHash('sha256').update(seed).digest();
    return this._machineKey;
  }

  _encrypt(plaintext) {
    const key = this._deriveMachineKey();
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
    const encrypted = Buffer.concat([cipher.update(plaintext, 'utf-8'), cipher.final()]);
    const authTag = cipher.getAuthTag();
    return {
      iv: iv.toString('hex'),
      data: encrypted.toString('hex'),
      tag: authTag.toString('hex')
    };
  }

  _decrypt(encrypted) {
    const key = this._deriveMachineKey();
    const decipher = crypto.createDecipheriv(
      'aes-256-gcm',
      key,
      Buffer.from(encrypted.iv, 'hex')
    );
    decipher.setAuthTag(Buffer.from(encrypted.tag, 'hex'));
    const decrypted = Buffer.concat([
      decipher.update(Buffer.from(encrypted.data, 'hex')),
      decipher.final()
    ]);
    return decrypted.toString('utf-8');
  }

  _ensureDir() {
    const dir = path.dirname(this.filePath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  }

  _loadState() {
    if (this._cache) return this._cache;
    if (!fs.existsSync(this.filePath)) {
      this._cache = { user_preferences: {}, _secrets: {} };
      return this._cache;
    }
    try {
      const raw = fs.readFileSync(this.filePath, 'utf-8');
      this._cache = JSON.parse(raw);
      if (!this._cache.user_preferences) this._cache.user_preferences = {};
      if (!this._cache._secrets) this._cache._secrets = {};
      return this._cache;
    } catch (_) {
      this._cache = { user_preferences: {}, _secrets: {} };
      return this._cache;
    }
  }

  _saveState(state) {
    this._cache = state;
    fs.writeFileSync(this.filePath, JSON.stringify(state, null, 2), { encoding: 'utf-8', mode: 0o600 });
    try { fs.chmodSync(this.filePath, 0o600); } catch (_) {}
  }

  savePreference(key, value) {
    const state = this._loadState();
    if (SECRET_KEYS.includes(key)) {
      state._secrets[key] = this._encrypt(value);
    } else {
      state.user_preferences[key] = value;
    }
    this._saveState(state);
  }

  getPreference(key, defaultValue) {
    const state = this._loadState();
    if (SECRET_KEYS.includes(key)) {
      if (state._secrets && state._secrets[key]) {
        try {
          return this._decrypt(state._secrets[key]);
        } catch (_) {
          return defaultValue !== undefined ? defaultValue : null;
        }
      }
      return defaultValue !== undefined ? defaultValue : null;
    }
    return state.user_preferences.hasOwnProperty(key)
      ? state.user_preferences[key]
      : (defaultValue !== undefined ? defaultValue : null);
  }

  deletePreference(key) {
    const state = this._loadState();
    if (SECRET_KEYS.includes(key)) {
      delete state._secrets[key];
    } else {
      delete state.user_preferences[key];
    }
    this._saveState(state);
  }
}

module.exports = { StateStore };
