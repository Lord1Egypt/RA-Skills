/**
 * CartService — 购物车服务
 *
 * 支持本地游购物车（未登录）与服务端购物车（已登录）的合并。
 *
 * 事件：
 *   cart:updated — 购物车变更，携带 { count } 总数量
 *   cart:synced  — 本地→服务端合并完成
 *
 * 用法：
 *   import { cart } from '../app.js';
 *   await cart.addItem(productId, 1);
 *   console.log(cart.getCart());
 */

import { api } from './api.js';
import { bus, auth } from '../app.js';
import { storage } from '../utils/storage.js';

const CART_KEY = 'cart';

export class CartService {
  constructor() {
    /** @type {Array<{id: string, productId: string, name: string, price: number, qty: number, image?: string}>} */
    this._items = [];
    /** @type {boolean} */
    this._initialized = false;
  }

  // ===================== 初始化 =====================

  /**
   * 初始化购物车
   * - 已登录 → 从服务端加载
   * - 未登录 → 从 localStorage 加载
   */
  async init() {
    if (auth.isLoggedIn()) {
      await this._loadFromServer();
    } else {
      this._loadFromLocal();
    }
    this._initialized = true;
    this._notify();

    // 监听登录事件 → 合并本地购物车到服务端
    bus.on('auth:login', () => this.syncOnLogin());
  }

  // ===================== 读取 =====================

  /**
   * 获取购物车列表
   * @returns {Array}
   */
  getCart() {
    return [...this._items];
  }

  /**
   * 获取商品总数
   * @returns {number}
   */
  getCount() {
    return this._items.reduce((sum, item) => sum + item.qty, 0);
  }

  /**
   * 获取总价
   * @returns {number}
   */
  getTotal() {
    return this._items.reduce((sum, item) => sum + item.price * item.qty, 0);
  }

  // ===================== 增删改 =====================

  /**
   * 添加商品
   * @param {string} productId
   * @param {number} qty - 数量，默认 1
   */
  async addItem(productId, qty = 1) {
    const existing = this._items.find(i => i.productId === productId);
    if (existing) {
      existing.qty += qty;
    } else {
      // 从服务端获取商品详情（简化处理，可从本地缓存或服务端获取）
      const product = await api.get(`/products/${productId}`);
      this._items.push({
        id: `local_${Date.now()}`,
        productId,
        name: product.name,
        price: product.price,
        image: product.image,
        qty,
      });
    }

    await this._persist();
    this._notify();
  }

  /**
   * 修改数量
   * @param {string} productId
   * @param {number} qty
   */
  async updateItem(productId, qty) {
    const item = this._items.find(i => i.productId === productId);
    if (!item) return;

    if (qty <= 0) {
      return this.removeItem(productId);
    }

    item.qty = qty;
    await this._persist();
    this._notify();
  }

  /**
   * 删除商品
   * @param {string} productId
   */
  async removeItem(productId) {
    this._items = this._items.filter(i => i.productId !== productId);
    await this._persist();
    this._notify();
  }

  /**
   * 清空购物车
   */
  async clear() {
    this._items = [];
    await this._persist();
    this._notify();
  }

  // ===================== 登录合并 =====================

  /**
   * 登录后将本地购物车合并到服务端
   */
  async syncOnLogin() {
    const localItems = this._items;
    if (localItems.length === 0) return;

    try {
      // 逐项推送到服务端
      for (const item of localItems) {
        await api.post('/cart/add', {
          productId: item.productId,
          qty: item.qty,
        });
      }
      // 合并成功 → 清除本地，加载服务端数据
      storage.remove(CART_KEY);
      await this._loadFromServer();
      bus.emit('cart:synced', { count: this.getCount() });
    } catch {
      console.warn('[Cart] 合并购物车失败，保留本地数据');
    }
  }

  // ===================== 内部 =====================

  /** 从服务端加载购物车 */
  async _loadFromServer() {
    try {
      const data = await api.get('/cart');
      this._items = data.items || [];
    } catch {
      this._items = [];
    }
  }

  /** 从 localStorage 加载购物车 */
  _loadFromLocal() {
    this._items = storage.get(CART_KEY, []);
  }

  /** 持久化（已登录→服务端，未登录→localStorage） */
  async _persist() {
    if (auth.isLoggedIn()) {
      try {
        // 将全量购物车同步到服务端
        await api.put('/cart', { items: this._items.map(i => ({
          productId: i.productId,
          qty: i.qty,
        })) });
      } catch {
        // 网络失败时写本地做兜底
        storage.set(CART_KEY, this._items);
      }
    } else {
      storage.set(CART_KEY, this._items);
    }
  }

  /** 通知购物车变更 */
  _notify() {
    bus.emit('cart:updated', { count: this.getCount(), items: this.getCart() });
  }
}
