/**
 * EventBus — 轻量发布订阅
 *
 * 用法：
 *   import { bus } from '../app.js';
 *   bus.on('cart:updated', (count) => updateBadge(count));
 *   bus.emit('cart:updated', 3);
 *   bus.off('cart:updated', handler);
 */
export class EventBus {
  constructor() {
    this._handlers = {};
  }

  /**
   * 订阅事件
   * @param {string} event
   * @param {Function} fn
   * @returns {Function} 取消订阅函数
   */
  on(event, fn) {
    (this._handlers[event] = this._handlers[event] || []).push(fn);
    return () => this.off(event, fn);
  }

  /**
   * 取消订阅
   * @param {string} event
   * @param {Function} fn
   */
  off(event, fn) {
    if (!this._handlers[event]) return;
    this._handlers[event] = this._handlers[event].filter(h => h !== fn);
  }

  /**
   * 触发事件
   * @param {string} event
   * @param {*} data
   */
  emit(event, data) {
    if (!this._handlers[event]) return;
    this._handlers[event].forEach(fn => {
      try { fn(data); } catch (e) { console.error(`[EventBus] handler error:`, e); }
    });
  }

  /** 清除所有订阅 */
  clear() {
    this._handlers = {};
  }
}
