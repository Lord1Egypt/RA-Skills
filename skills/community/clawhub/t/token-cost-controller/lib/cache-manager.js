/**
 * Cache Manager - 智能缓存管理
 * 使用 Ring Buffer 固定内存，使用安全 key 生成
 */
const fs = require('fs');
const path = require('path');

/**
 * Ring Buffer - 固定大小的循环缓冲区
 */
class RingBuffer {
  constructor(maxSize) {
    this.maxSize = maxSize;
    this.buffer = [];
    this.index = 0;
  }

  push(item) {
    if (this.buffer.length < this.maxSize) {
      this.buffer.push(item);
    } else {
      this.buffer[this.index] = item;
    }
    this.index = (this.index + 1) % this.maxSize;
  }

  toArray() {
    if (this.buffer.length < this.maxSize) {
      return [...this.buffer];
    }
    return [...this.buffer.slice(this.index), ...this.buffer.slice(0, this.index)];
  }

  get length() {
    return Math.min(this.buffer.length, this.maxSize);
  }
}

class CacheManager {
  constructor(config = {}) {
    this.maxSize = config.maxSize || 10000;
    this.ttl = config.ttl || 1800; // 30分钟
    this.cache = new Map();
    this.stats = new RingBuffer(1000);
    this.dataDir = config.dataDir || path.join(__dirname, '..', '.openclaw', 'data');
    this.cacheFile = path.join(this.dataDir, 'cache.json');

    this.loadFromDisk();
  }

  /**
   * 生成安全的缓存Key - 对象键排序
   */
  generateKey(data) {
    return JSON.stringify(data, Object.keys(data).sort());
  }

  /**
   * 检查缓存是否存在且有效
   */
  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;

    const now = Date.now();
    if (now - item.timestamp > this.ttl * 1000) {
      this.cache.delete(key);
      return null;
    }

    // 记录命中
    this.stats.push({ hit: true, timestamp: now });
    return item.value;
  }

  /**
   * 设置缓存
   */
  set(key, value) {
    if (this.cache.size >= this.maxSize) {
      // 使用 LRU 策略删除最老的
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }

    this.cache.set(key, {
      value,
      timestamp: Date.now()
    });

    this.stats.push({ hit: false, timestamp: Date.now() });
    this.saveToDisk();
  }

  /**
   * 获取缓存命中率
   */
  getHitRate() {
    const arr = this.stats.toArray();
    if (arr.length === 0) return 0;
    const hits = arr.filter(s => s.hit).length;
    return (hits / arr.length * 100).toFixed(1);
  }

  /**
   * 从磁盘加载缓存
   */
  loadFromDisk() {
    try {
      if (fs.existsSync(this.cacheFile)) {
        const data = JSON.parse(fs.readFileSync(this.cacheFile, 'utf8'));
        const now = Date.now();

        for (const [key, item] of Object.entries(data)) {
          if (now - item.timestamp < this.ttl * 1000) {
            this.cache.set(key, item);
          }
        }
      }
    } catch (e) {
      // 忽略加载错误
    }
  }

  /**
   * 保存缓存到磁盘
   */
  saveToDisk() {
    try {
      const data = Object.fromEntries(this.cache);
      fs.mkdirSync(path.dirname(this.cacheFile), { recursive: true });
      fs.writeFileSync(this.cacheFile, JSON.stringify(data));
    } catch (e) {
      // 忽略保存错误
    }
  }

  /**
   * 获取缓存统计
   */
  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hitRate: this.getHitRate() + '%'
    };
  }
}

module.exports = CacheManager;
