#!/usr/bin/env node

/**
 * 页面生成器
 */

const fs = require('fs');
const path = require('path');

// 页面模板
const pageTemplates = {
  'home': {
    js: `// 首页
Page({
  data: {
    banners: [],
    products: []
  },

  onLoad() {
    this.loadBanners()
    this.loadProducts()
  },

  async loadBanners() {
    // TODO: 加载轮播图
  },

  async loadProducts() {
    const res = await wx.cloud.callFunction({
      name: 'getProducts'
    })
    this.setData({ products: res.result.data })
  },

  goToDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: \`/pages/product-detail/product-detail?id=\${id}\`
    })
  }
})`,
    wxml: `<view class="container">
  <!-- 轮播图 -->
  <swiper class="banner" autoplay circular>
    <swiper-item wx:for="{{banners}}" wx:key="id">
      <image src="{{item.image}}" mode="aspectFill" />
    </swiper-item>
  </swiper>

  <!-- 商品列表 -->
  <view class="section">
    <view class="section-title">热门商品</view>
    <view class="product-grid">
      <view
        wx:for="{{products}}"
        wx:key="_id"
        class="product-card"
        data-id="{{item._id}}"
        bindtap="goToDetail"
      >
        <image src="{{item.image}}" mode="aspectFill" />
        <view class="product-info">
          <text class="product-name">{{item.name}}</text>
          <text class="product-price">¥{{item.price}}</text>
        </view>
      </view>
    </view>
  </view>
</view>`,
    wxss: `.container {
  padding: 20rpx;
}

.banner {
  height: 300rpx;
  border-radius: 12rpx;
  overflow: hidden;
}

.banner image {
  width: 100%;
  height: 100%;
}

.section {
  margin-top: 40rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.product-card {
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
}

.product-card image {
  width: 100%;
  height: 300rpx;
}

.product-info {
  padding: 16rpx;
}

.product-name {
  font-size: 28rpx;
  display: block;
}

.product-price {
  font-size: 32rpx;
  color: #ff4d4f;
  font-weight: bold;
  margin-top: 8rpx;
  display: block;
}`
  },

  'product-detail': {
    js: `// 商品详情页
Page({
  data: {
    product: {},
    quantity: 1
  },

  onLoad(options) {
    const { id } = options
    this.loadProduct(id)
  },

  async loadProduct(id) {
    const res = await wx.cloud.callFunction({
      name: 'getProducts',
      data: { id }
    })
    this.setData({ product: res.result.data[0] })
  },

  onQuantityChange(e) {
    const { action } = e.currentTarget.dataset
    let { quantity } = this.data
    if (action === 'add') quantity++
    if (action === 'sub' && quantity > 1) quantity--
    this.setData({ quantity })
  },

  async buy() {
    const { product, quantity } = this.data
    const res = await wx.cloud.callFunction({
      name: 'createOrder',
      data: {
        productId: product._id,
        quantity
      }
    })
    wx.showToast({ title: '下单成功', icon: 'success' })
    wx.navigateTo({ url: '/pages/order/order' })
  }
})`,
    wxml: `<view class="container">
  <image class="product-image" src="{{product.image}}" mode="aspectFill" />

  <view class="product-info">
    <text class="product-name">{{product.name}}</text>
    <text class="product-price">¥{{product.price}}</text>
    <text class="product-desc">{{product.description}}</text>
  </view>

  <view class="quantity-picker">
    <button data-action="sub" bindtap="onQuantityChange">-</button>
    <text>{{quantity}}</text>
    <button data-action="add" bindtap="onQuantityChange">+</button>
  </view>

  <button class="buy-btn" bindtap="buy">立即购买</button>
</view>`,
    wxss: `.container {
  padding: 20rpx;
}

.product-image {
  width: 100%;
  height: 500rpx;
  border-radius: 12rpx;
}

.product-info {
  padding: 20rpx 0;
}

.product-name {
  font-size: 36rpx;
  font-weight: bold;
  display: block;
}

.product-price {
  font-size: 40rpx;
  color: #ff4d4f;
  font-weight: bold;
  margin: 16rpx 0;
  display: block;
}

.product-desc {
  font-size: 28rpx;
  color: #666;
  display: block;
}

.quantity-picker {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin: 40rpx 0;
}

.quantity-picker button {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: #f5f5f5;
  border: none;
  font-size: 32rpx;
}

.quantity-picker text {
  font-size: 36rpx;
  font-weight: bold;
}

.buy-btn {
  background: #ff4d4f;
  color: #fff;
  border-radius: 40rpx;
  margin-top: 40rpx;
}`
  },

  'order': {
    js: `// 订单页
Page({
  data: {
    orders: []
  },

  onLoad() {
    this.loadOrders()
  },

  async loadOrders() {
    const res = await wx.cloud.callFunction({
      name: 'getOrders'
    })
    this.setData({ orders: res.result.data })
  },

  async cancelOrder(e) {
    const { id } = e.currentTarget.dataset
    await wx.cloud.callFunction({
      name: 'updateOrder',
      data: { id, status: 'cancelled' }
    })
    this.loadOrders()
  }
})`,
    wxml: `<view class="container">
  <view wx:for="{{orders}}" wx:key="_id" class="order-card">
    <view class="order-header">
      <text>订单号: {{item._id}}</text>
      <text class="status">{{item.status}}</text>
    </view>
    <view class="order-body">
      <text>{{item.productName}}</text>
      <text>¥{{item.totalPrice}}</text>
    </view>
    <view class="order-footer">
      <text>{{item.createdAt}}</text>
      <button
        wx:if="{{item.status === 'pending'}}"
        data-id="{{item._id}}"
        bindtap="cancelOrder"
      >取消订单</button>
    </view>
  </view>

  <view wx:if="{{orders.length === 0}}" class="empty">
    <text>暂无订单</text>
  </view>
</view>`,
    wxss: `.container {
  padding: 20rpx;
}

.order-card {
  background: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
}

.order-header {
  display: flex;
  justify-content: space-between;
  padding-bottom: 16rpx;
  border-bottom: 1px solid #f5f5f5;
}

.status {
  color: #ff4d4f;
}

.order-body {
  padding: 20rpx 0;
  display: flex;
  justify-content: space-between;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-footer button {
  font-size: 24rpx;
  padding: 8rpx 24rpx;
}

.empty {
  text-align: center;
  padding: 100rpx 0;
  color: #999;
}`
  }
};

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(`
📖 页面生成器

用法:
  node generate-page.js <页面类型>

页面类型:
  home            首页（轮播图 + 商品列表）
  product-detail  商品详情页
  order           订单页

示例:
  node generate-page.js home
`);
  process.exit(0);
}

const pageType = args[0];

if (!pageTemplates[pageType]) {
  console.error(`❌ 不支持的页面类型: ${pageType}`);
  console.log(`支持的类型: ${Object.keys(pageTemplates).join(', ')}`);
  process.exit(1);
}

// 创建页面目录
const pageDir = path.join(process.cwd(), 'pages', pageType);
if (fs.existsSync(pageDir)) {
  console.error(`❌ 页面已存在: ${pageType}`);
  process.exit(1);
}

fs.mkdirSync(pageDir, { recursive: true });

// 写入页面文件
const template = pageTemplates[pageType];
fs.writeFileSync(path.join(pageDir, `${pageType}.js`), template.js);
fs.writeFileSync(path.join(pageDir, `${pageType}.wxml`), template.wxml);
fs.writeFileSync(path.join(pageDir, `${pageType}.wxss`), template.wxss);
fs.writeFileSync(path.join(pageDir, `${pageType}.json`), '{}');

console.log(`\n✅ 页面已创建: pages/${pageType}/
📁 位置: ${pageDir}

下一步:
1. 在 app.json 中添加页面路径
2. 修改云函数名称适配你的后端
`);
