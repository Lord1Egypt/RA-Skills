/**
 * ToastService — Toast 通知
 *
 * 用法：
 *   import { toast } from '../app.js';
 *   toast.success('操作成功');
 *   toast.error('出错了', 5000);
 *   toast.warning('注意');
 *   toast.info('提示');
 */

export class ToastService {
  constructor() {
    this._container = null;
    this._toasts = new Map(); // id → { el, timer }
    this._counter = 0;
  }

  /**
   * 获取 Toast 容器，不存在则创建
   */
  getContainer() {
    if (!this._container) {
      this._container = document.getElementById('toast-container');
      if (!this._container) {
        this._container = document.createElement('div');
        this._container.id = 'toast-container';
        document.body.appendChild(this._container);
      }
    }
    return this._container;
  }

  /**
   * 显示 Toast
   * @param {string} message
   * @param {string} type - 'success' | 'error' | 'warning' | 'info'
   * @param {number} duration - 显示时长（ms），默认 3000
   * @returns {number} toast ID
   */
  show(message, type = 'info', duration = 3000) {
    const id = ++this._counter;
    const container = this.getContainer();

    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️',
    };

    const el = document.createElement('div');
    el.className = `toast toast-${type}`;
    el.innerHTML = `
      <span class="toast-icon">${icons[type] || icons.info}</span>
      <span class="toast-text">${this._escapeHtml(message)}</span>
      <button class="toast-close" data-toast-close="${id}" aria-label="关闭">&times;</button>
    `;

    // 点击关闭
    el.querySelector('[data-toast-close]').addEventListener('click', () => {
      this.dismiss(id);
    });

    container.appendChild(el);
    this._toasts.set(id, { el, timer: null });

    // 自动关闭
    if (duration > 0) {
      const timer = setTimeout(() => this.dismiss(id), duration);
      this._toasts.get(id).timer = timer;
    }

    return id;
  }

  /** 快捷方法 */
  success(msg, dur) { return this.show(msg, 'success', dur); }
  error(msg, dur) { return this.show(msg, 'error', dur || 5000); }
  warning(msg, dur) { return this.show(msg, 'warning', dur); }
  info(msg, dur) { return this.show(msg, 'info', dur); }

  /**
   * 关闭指定 Toast
   * @param {number} id
   */
  dismiss(id) {
    const entry = this._toasts.get(id);
    if (!entry) return;

    const { el, timer } = entry;
    if (timer) clearTimeout(timer);

    // 退出动画
    el.classList.add('toast-leaving');
    setTimeout(() => {
      if (el.parentNode) el.parentNode.removeChild(el);
      this._toasts.delete(id);
    }, 300);
  }

  /**
   * 清除所有 Toast
   */
  dismissAll() {
    for (const id of this._toasts.keys()) {
      this.dismiss(id);
    }
  }

  _escapeHtml(str) {
    if (str == null) return '';
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(String(str)));
    return div.innerHTML;
  }
}
