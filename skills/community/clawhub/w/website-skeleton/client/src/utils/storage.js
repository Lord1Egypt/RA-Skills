/**
 * storage — localStorage 封装
 *
 * 特性：
 * - 统一前缀，避免 key 冲突
 * - Private 模式检测（ios safari / firefox）
 * - JSON 自动序列化/反序列化
 * - 异常安全（写入失败静默处理）
 */

const PREFIX = 'geekshop:';
const _available = (() => {
  try {
    const k = `__test_${Date.now()}__`;
    localStorage.setItem(k, '1');
    localStorage.removeItem(k);
    return true;
  } catch {
    return false;
  }
})();

function prefixed(key) {
  return `${PREFIX}${key}`;
}

export const storage = {
  /**
   * 是否可用（非 private 模式）
   */
  get available() { return _available; },

  /**
   * 读取值
   * @param {string} key
   * @param {*} fallback - 缺省值
   */
  get(key, fallback = null) {
    if (!_available) return fallback;
    try {
      const raw = localStorage.getItem(prefixed(key));
      if (raw === null) return fallback;
      return JSON.parse(raw);
    } catch {
      return fallback;
    }
  },

  /**
   * 写入值
   * @param {string} key
   * @param {*} value
   */
  set(key, value) {
    if (!_available) return;
    try {
      localStorage.setItem(prefixed(key), JSON.stringify(value));
    } catch { /* 配额超限/private 模式静默忽略 */ }
  },

  /**
   * 删除值
   * @param {string} key
   */
  remove(key) {
    if (!_available) return;
    try {
      localStorage.removeItem(prefixed(key));
    } catch { /* ignore */ }
  },

  /**
   * 清空所有带前缀的 key
   */
  clear() {
    if (!_available) return;
    try {
      const keys = Object.keys(localStorage).filter(k => k.startsWith(PREFIX));
      keys.forEach(k => localStorage.removeItem(k));
    } catch { /* ignore */ }
  },

  /**
   * 获取所有带前缀的 key（不含前缀本身）
   * @returns {string[]}
   */
  keys() {
    if (!_available) return [];
    try {
      return Object.keys(localStorage)
        .filter(k => k.startsWith(PREFIX))
        .map(k => k.slice(PREFIX.length));
    } catch {
      return [];
    }
  }
};
