/**
 * TikTok Shop API 适配器
 * 支持 Mock API 和真实 API 切换
 */

import { loadConfig } from './config.js';
import { TikTokMockAPI } from './mock-api.js';

/**
 * TikTok Shop API 真实实现（占位符）
 * 实际使用时需要实现真实的 API 调用
 */
class TikTokRealAPI {
  constructor(config) {
    this.config = config;
    this.baseUrl = 'https://open.tiktokapis.com/v2';
    this.accessToken = null;
  }

  async getAccessToken(shopId) {
    console.log('🔐 获取 TikTok Access Token...');
    
    // TODO: 实现真实的 OAuth 2.0 流程
    // 1. 构建授权 URL
    // 2. 用户授权
    // 3. 获取 code
    // 4. 用 code 换取 access_token
    
    throw new Error('真实 API 尚未实现，请使用 Mock 模式或等待 API 权限');
  }

  async listProducts(shopId, options) {
    console.log('📦 获取商品列表...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async createProduct(shopId, productData) {
    console.log('📦 创建商品...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async updateStock(shopId, skuId, quantity) {
    console.log('📦 更新库存...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async listOrders(shopId, options) {
    console.log('📋 获取订单列表...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async getOrderDetail(shopId, orderId) {
    console.log('📋 获取订单详情...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async updateOrderStatus(shopId, orderId, status, trackingNumber) {
    console.log('📋 更新订单状态...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async uploadVideo(shopId, videoData) {
    console.log('📹 上传视频...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async publishVideo(shopId, videoId, options) {
    console.log('📹 发布视频...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async listVideos(shopId, options) {
    console.log('📹 获取视频列表...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async getShopOverview(shopId, period) {
    console.log('📊 获取店铺概览...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }

  async getDailySales(shopId, startDate, endDate) {
    console.log('📊 获取销售数据...');
    // TODO: 实现真实 API 调用
    throw new Error('真实 API 尚未实现');
  }
}

/**
 * API 适配器 - 自动选择 Mock 或真实 API
 */
export class TikTokAPIAdapter {
  constructor(config = null) {
    this.config = config || loadConfig();
    this.useMock = this.config.tiktok?.useMock !== false; // 默认使用 Mock
    
    if (this.useMock) {
      console.log('🔧 使用 Mock API 模式');
      this.api = new TikTokMockAPI(this.config);
    } else {
      console.log('🔧 使用真实 API 模式');
      this.api = new TikTokRealAPI(this.config);
    }
  }

  /**
   * 获取 Access Token
   */
  async getAccessToken(shopId) {
    return await this.api.getAccessToken(shopId);
  }

  /**
   * 商品管理
   */
  async listProducts(shopId, options) {
    return await this.api.listProducts(shopId, options);
  }

  async createProduct(shopId, productData) {
    return await this.api.createProduct(shopId, productData);
  }

  async updateStock(shopId, skuId, quantity) {
    return await this.api.updateStock(shopId, skuId, quantity);
  }

  /**
   * 订单管理
   */
  async listOrders(shopId, options) {
    return await this.api.listOrders(shopId, options);
  }

  async getOrderDetail(shopId, orderId) {
    return await this.api.getOrderDetail(shopId, orderId);
  }

  async updateOrderStatus(shopId, orderId, status, trackingNumber) {
    return await this.api.updateOrderStatus(shopId, orderId, status, trackingNumber);
  }

  /**
   * 视频管理
   */
  async uploadVideo(shopId, videoData) {
    return await this.api.uploadVideo(shopId, videoData);
  }

  async publishVideo(shopId, videoId, options) {
    return await this.api.publishVideo(shopId, videoId, options);
  }

  async listVideos(shopId, options) {
    return await this.api.listVideos(shopId, options);
  }

  /**
   * 数据分析
   */
  async getShopOverview(shopId, period) {
    return await this.api.getShopOverview(shopId, period);
  }

  async getDailySales(shopId, startDate, endDate) {
    return await this.api.getDailySales(shopId, startDate, endDate);
  }

  /**
   * 切换到 Mock 模式
   */
  useMockMode() {
    if (!this.useMock) {
      console.log('切换到 Mock API 模式');
      this.useMock = true;
      this.api = new TikTokMockAPI(this.config);
    }
  }

  /**
   * 切换到真实 API 模式
   */
  useRealMode() {
    if (this.useMock) {
      console.log('切换到真实 API 模式');
      this.useMock = false;
      this.api = new TikTokRealAPI(this.config);
    }
  }
}

/**
 * 创建 API 实例
 */
export function createTikTokAPI(config) {
  return new TikTokAPIAdapter(config);
}

export default TikTokAPIAdapter;
