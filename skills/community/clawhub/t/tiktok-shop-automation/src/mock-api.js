/**
 * TikTok Shop Mock API - 模拟 API 层
 * 用于开发和测试，无需真实 API 权限
 */

import { v4 as uuidv4 } from 'uuid';

// Mock 数据
const mockProducts = [
  {
    product_id: 'PROD001',
    title: 'Wireless Earbuds Pro',
    price: 29.99,
    stock: 150,
    status: 'active',
    sales: 1250,
    created_at: '2024-02-01T10:00:00Z'
  },
  {
    product_id: 'PROD002',
    title: 'Smart Watch Ultra',
    price: 89.99,
    stock: 75,
    status: 'active',
    sales: 890,
    created_at: '2024-02-05T14:30:00Z'
  },
  {
    product_id: 'PROD003',
    title: 'Phone Case Premium',
    price: 15.99,
    stock: 500,
    status: 'active',
    sales: 2340,
    created_at: '2024-02-10T09:15:00Z'
  }
];

const mockOrders = [
  {
    order_id: 'ORD001',
    status: 'pending',
    amount: 29.99,
    items: [{ product_id: 'PROD001', quantity: 1 }],
    customer: { name: 'John Doe', email: 'john@example.com' },
    created_at: '2024-03-14T10:00:00Z'
  },
  {
    order_id: 'ORD002',
    status: 'pending',
    amount: 105.98,
    items: [
      { product_id: 'PROD002', quantity: 1 },
      { product_id: 'PROD003', quantity: 1 }
    ],
    customer: { name: 'Jane Smith', email: 'jane@example.com' },
    created_at: '2024-03-14T11:30:00Z'
  },
  {
    order_id: 'ORD003',
    status: 'shipped',
    amount: 45.97,
    items: [{ product_id: 'PROD003', quantity: 2 }, { product_id: 'PROD001', quantity: 1 }],
    customer: { name: 'Bob Wilson', email: 'bob@example.com' },
    created_at: '2024-03-13T15:20:00Z',
    tracking_number: 'FX123456789'
  }
];

const mockVideos = [
  {
    video_id: 'VID001',
    title: 'Product Demo - Wireless Earbuds',
    description: 'Check out our amazing wireless earbuds!',
    status: 'published',
    views: 15420,
    likes: 1250,
    shares: 340,
    created_at: '2024-03-10T18:00:00Z'
  },
  {
    video_id: 'VID002',
    title: 'Smart Watch Features',
    description: 'All the features you need',
    status: 'published',
    views: 8930,
    likes: 670,
    shares: 180,
    created_at: '2024-03-12T19:30:00Z'
  }
];

const mockAnalytics = {
  shop_overview: {
    total_sales: 45670.50,
    total_orders: 1250,
    total_products: 25,
    conversion_rate: 3.5,
    period: 'last_30_days'
  },
  daily_sales: [
    { date: '2024-03-08', sales: 1250.00, orders: 42 },
    { date: '2024-03-09', sales: 1580.50, orders: 55 },
    { date: '2024-03-10', sales: 2100.00, orders: 68 },
    { date: '2024-03-11', sales: 1890.25, orders: 61 },
    { date: '2024-03-12', sales: 2350.75, orders: 75 },
    { date: '2024-03-13', sales: 1950.00, orders: 63 },
    { date: '2024-03-14', sales: 2200.50, orders: 71 }
  ]
};

/**
 * Mock API 类 - 模拟 TikTok Shop API
 */
export class TikTokMockAPI {
  constructor(config) {
    this.config = config;
    this.baseUrl = 'https://mock.tiktokshop.com/api/v1';
  }

  /**
   * 认证 - 模拟获取 access token
   */
  async getAccessToken(shopId) {
    console.log('🔐 [Mock] 获取 Access Token...');
    await this._delay(500);
    
    return {
      access_token: `mock_token_${uuidv4()}`,
      expires_in: 86400,
      token_type: 'Bearer',
      shop_id: shopId
    };
  }

  /**
   * 商品管理
   */
  async listProducts(shopId, options = {}) {
    console.log('📦 [Mock] 获取商品列表...');
    await this._delay(300);
    
    const page = options.page || 1;
    const pageSize = options.pageSize || 20;
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    
    return {
      code: 0,
      message: 'Success',
      data: {
        products: mockProducts.slice(start, end),
        total: mockProducts.length,
        page,
        pageSize
      }
    };
  }

  async createProduct(shopId, productData) {
    console.log('📦 [Mock] 创建商品...');
    await this._delay(500);
    
    const newProduct = {
      product_id: `PROD${String(mockProducts.length + 1).padStart(3, '0')}`,
      ...productData,
      status: 'active',
      sales: 0,
      created_at: new Date().toISOString()
    };
    
    mockProducts.push(newProduct);
    
    return {
      code: 0,
      message: 'Success',
      data: {
        product_id: newProduct.product_id
      }
    };
  }

  async updateStock(shopId, skuId, quantity) {
    console.log('📦 [Mock] 更新库存...');
    await this._delay(200);
    
    const product = mockProducts.find(p => p.product_id === skuId);
    if (product) {
      product.stock = quantity;
    }
    
    return {
      code: 0,
      message: 'Success',
      data: {
        updated: true,
        product_id: skuId,
        new_stock: quantity
      }
    };
  }

  /**
   * 订单管理
   */
  async listOrders(shopId, options = {}) {
    console.log('📋 [Mock] 获取订单列表...');
    await this._delay(300);
    
    const status = options.status;
    let filteredOrders = mockOrders;
    
    if (status) {
      filteredOrders = mockOrders.filter(o => o.status === status);
    }
    
    return {
      code: 0,
      message: 'Success',
      data: {
        orders: filteredOrders,
        total: filteredOrders.length
      }
    };
  }

  async getOrderDetail(shopId, orderId) {
    console.log('📋 [Mock] 获取订单详情...');
    await this._delay(200);
    
    const order = mockOrders.find(o => o.order_id === orderId);
    
    if (!order) {
      return {
        code: 404,
        message: 'Order not found'
      };
    }
    
    return {
      code: 0,
      message: 'Success',
      data: {
        order
      }
    };
  }

  async updateOrderStatus(shopId, orderId, status, trackingNumber = null) {
    console.log('📋 [Mock] 更新订单状态...');
    await this._delay(200);
    
    const order = mockOrders.find(o => o.order_id === orderId);
    if (order) {
      order.status = status;
      if (trackingNumber) {
        order.tracking_number = trackingNumber;
      }
    }
    
    return {
      code: 0,
      message: 'Success',
      data: {
        updated: true,
        order_id: orderId,
        new_status: status
      }
    };
  }

  /**
   * 视频管理
   */
  async uploadVideo(shopId, videoData) {
    console.log('📹 [Mock] 上传视频...');
    await this._delay(1000);
    
    const newVideo = {
      video_id: `VID${String(mockVideos.length + 1).padStart(3, '0')}`,
      ...videoData,
      status: 'uploaded',
      views: 0,
      likes: 0,
      shares: 0,
      created_at: new Date().toISOString()
    };
    
    mockVideos.push(newVideo);
    
    return {
      code: 0,
      message: 'Success',
      data: {
        video_id: newVideo.video_id,
        upload_url: `https://mock.tiktok.com/upload/${newVideo.video_id}`
      }
    };
  }

  async publishVideo(shopId, videoId, options = {}) {
    console.log('📹 [Mock] 发布视频...');
    await this._delay(500);
    
    const video = mockVideos.find(v => v.video_id === videoId);
    if (video) {
      video.status = 'published';
      video.description = options.description || video.description;
      video.tags = options.tags || [];
    }
    
    return {
      code: 0,
      message: 'Success',
      data: {
        video_id: videoId,
        video_url: `https://www.tiktok.com/@shop/video/${videoId}`,
        status: 'published'
      }
    };
  }

  async listVideos(shopId, options = {}) {
    console.log('📹 [Mock] 获取视频列表...');
    await this._delay(300);
    
    return {
      code: 0,
      message: 'Success',
      data: {
        videos: mockVideos,
        total: mockVideos.length
      }
    };
  }

  /**
   * 数据分析
   */
  async getShopOverview(shopId, period = 'last_30_days') {
    console.log('📊 [Mock] 获取店铺概览...');
    await this._delay(300);
    
    return {
      code: 0,
      message: 'Success',
      data: mockAnalytics.shop_overview
    };
  }

  async getDailySales(shopId, startDate, endDate) {
    console.log('📊 [Mock] 获取销售数据...');
    await this._delay(300);
    
    return {
      code: 0,
      message: 'Success',
      data: {
        daily_sales: mockAnalytics.daily_sales,
        period: { start: startDate, end: endDate }
      }
    };
  }

  /**
   * 工具方法
   */
  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

/**
 * 创建 Mock API 实例
 */
export function createMockAPI(config) {
  return new TikTokMockAPI(config);
}

export default TikTokMockAPI;
