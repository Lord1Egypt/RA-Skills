/**
 * 意图澄清缓存管理器
 * 管理 ~/.openclaw/data/intent-clarifier/ 下的缓存文件
 */

const fs = require('fs');
const path = require('path');

const CACHE_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'data', 'intent-clarifier');
const CACHE_FILE = path.join(CACHE_DIR, 'cache.json');
const PREFS_FILE = path.join(CACHE_DIR, 'prefs.json');
const TRANSLATIONS_FILE = path.join(CACHE_DIR, 'translations.json');

// 缓存TTL：10分钟
const CACHE_TTL = 10 * 60 * 1000;

class IntentClarifierCache {
  constructor() {
    this.ensureDir();
  }

  ensureDir() {
    if (!fs.existsSync(CACHE_DIR)) {
      fs.mkdirSync(CACHE_DIR, { recursive: true });
    }
  }

  // ===== 缓存操作 =====

  /**
   * 保存澄清缓存
   */
  saveClarification(sessionId, originalIntent, vulnerabilities) {
    const cache = {
      sessionId,
      originalIntent,
      vulnerabilities,
      createdAt: Date.now(),
      expiresAt: Date.now() + CACHE_TTL
    };
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
    return cache;
  }

  /**
   * 获取澄清缓存
   */
  getClarification() {
    if (!fs.existsSync(CACHE_FILE)) return null;
    
    try {
      const cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
      
      // 检查是否过期
      if (Date.now() > cache.expiresAt) {
        this.clearClarification();
        return null;
      }
      
      return cache;
    } catch (e) {
      return null;
    }
  }

  /**
   * 清除澄清缓存
   */
  clearClarification() {
    if (fs.existsSync(CACHE_FILE)) {
      fs.unlinkSync(CACHE_FILE);
    }
  }

  /**
   * 更新缓存（延长有效期）
   */
  touchClarification() {
    if (!fs.existsSync(CACHE_FILE)) return null;
    
    try {
      const cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
      cache.expiresAt = Date.now() + CACHE_TTL;
      fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
      return cache;
    } catch (e) {
      return null;
    }
  }

  // ===== 偏好操作 =====

  /**
   * 获取用户偏好
   */
  getPrefs(userId = 'default') {
    if (!fs.existsSync(PREFS_FILE)) return {};
    
    try {
      const prefs = JSON.parse(fs.readFileSync(PREFS_FILE, 'utf8'));
      return prefs[userId] || {};
    } catch (e) {
      return {};
    }
  }

  /**
   * 更新用户偏好
   */
  updatePrefs(userId, taskType, field, value) {
    let prefs = {};
    if (fs.existsSync(PREFS_FILE)) {
      try {
        prefs = JSON.parse(fs.readFileSync(PREFS_FILE, 'utf8'));
      } catch (e) {}
    }

    if (!prefs[userId]) prefs[userId] = {};
    if (!prefs[userId][taskType]) prefs[userId][taskType] = {};

    // 记录选择次数
    if (!prefs[userId][taskType][field]) {
      prefs[userId][taskType][field] = { value, count: 1 };
    } else if (prefs[userId][taskType][field].value === value) {
      prefs[userId][taskType][field].count += 1;
    } else {
      // 换了选项，重置计数
      prefs[userId][taskType][field] = { value, count: 1 };
    }

    fs.writeFileSync(PREFS_FILE, JSON.stringify(prefs, null, 2));
    return prefs[userId][taskType][field];
  }

  /**
   * 获取默认偏好（连续3次相同选择）
   */
  getDefaultPrefs(userId = 'default', taskType) {
    const prefs = this.getPrefs(userId);
    if (!prefs[taskType]) return {};

    const defaults = {};
    for (const [field, data] of Object.entries(prefs[taskType])) {
      if (data.count >= 3) {
        defaults[field] = data.value;
      }
    }
    return defaults;
  }

  /**
   * 清除指定用户的偏好
   */
  clearPrefs(userId = 'default') {
    if (!fs.existsSync(PREFS_FILE)) return;
    
    try {
      const prefs = JSON.parse(fs.readFileSync(PREFS_FILE, 'utf8'));
      delete prefs[userId];
      fs.writeFileSync(PREFS_FILE, JSON.stringify(prefs, null, 2));
    } catch (e) {}
  }

  // ===== 翻译表操作 =====

  /**
   * 获取翻译表
   */
  getTranslations() {
    if (!fs.existsSync(TRANSLATIONS_FILE)) return {};
    try {
      return JSON.parse(fs.readFileSync(TRANSLATIONS_FILE, 'utf8'));
    } catch (e) {
      return {};
    }
  }

  /**
   * 添加翻译记录
   */
  addTranslation(original,补充, interpretation) {
    let translations = this.getTranslations();
    const key = original.toLowerCase().trim();
    
    if (!translations[key]) translations[key] = [];
    
    // 避免重复
    const exists = translations[key].some(t => 
      t.supplement === supplement && t.interpolation === interpretation
    );
    
    if (!exists) {
      translations[key].push({ supplement, interpretation, count: 1 });
    } else {
      translations[key].find(t => 
        t.supplement === supplement && t.interpolation === interpretation
      ).count += 1;
    }

    fs.writeFileSync(TRANSLATIONS_FILE, JSON.stringify(translations, null, 2));
  }

  /**
   * 查找翻译
   */
  findTranslation(original, supplement) {
    const translations = this.getTranslations();
    const key = original.toLowerCase().trim();
    return translations[key]?.find(t => t.supplement === supplement);
  }

  // ===== 清理操作 =====

  /**
   * 清理所有过期缓存
   */
  cleanup() {
    // 清理过期缓存
    if (fs.existsSync(CACHE_FILE)) {
      try {
        const cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
        if (Date.now() > cache.expiresAt) {
          this.clearClarification();
        }
      } catch (e) {
        this.clearClarification();
      }
    }

    // 清理过旧的翻译记录（超过30天未使用）
    if (fs.existsSync(TRANSLATIONS_FILE)) {
      try {
        const translations = JSON.parse(fs.readFileSync(TRANSLATIONS_FILE, 'utf8'));
        const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
        for (const [key, entries] of Object.entries(translations)) {
          translations[key] = entries.filter(t => 
            !t.lastUsed || t.lastUsed > cutoff
          );
        }
        fs.writeFileSync(TRANSLATIONS_FILE, JSON.stringify(translations, null, 2));
      } catch (e) {}
    }
  }
}

// CLI接口
if (require.main === module) {
  const cache = new IntentClarifierCache();
  const action = process.argv[2];

  switch (action) {
    case 'clear':
      cache.clearClarification();
      console.log('Clarification cache cleared.');
      break;
    case 'prefs':
      console.log(JSON.stringify(cache.getPrefs(), null, 2));
      break;
    case 'translations':
      console.log(JSON.stringify(cache.getTranslations(), null, 2));
      break;
    case 'cleanup':
      cache.cleanup();
      console.log('Cleanup done.');
      break;
    default:
      const current = cache.getClarification();
      if (current) {
        console.log('Active clarification:');
        console.log(JSON.stringify(current, null, 2));
      } else {
        console.log('No active clarification.');
      }
  }
}

module.exports = IntentClarifierCache;