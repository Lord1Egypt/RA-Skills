# Website Analysis Reference Guide

## 技术栈识别清单

### 前端框架
| 框架 | 识别特征 |
|-----|---------|
| React | `data-reactroot`, `react-`, `_react` |
| Vue | `data-v-xxx`, `__vue__`, `vue-` |
| Angular | `ng-app`, `ng-`, `angular` |
| Next.js | `__NEXT_DATA__`, `next/` |
| Nuxt.js | `__NUXT__`, `nuxt` |

### CMS 识别
| CMS | 识别特征 |
|-----|---------|
| WordPress | `wp-content`, `wp-includes`, generator 包含 WordPress |
| Typecho | `Typecho_`, `typecho` |
| Hexo | `hexo-config`, `hexo-generator` |
| Docusaurus | `docusaurus` |
| VuePress | `vuepress` |

### 电商平台
| 平台 | 识别特征 |
|-----|---------|
| Shopify | `cdn.shopify.com` |
| WooCommerce | `woocommerce` |
| Magento | `by Magento` |
| Shoppy | `shoppy.gg` |
| Gumroad | `gumroad` |

### 分析工具识别
| 工具 | 识别特征 |
|-----|---------|
| Google Analytics | `google-analytics.com/analytics.js` |
| 百度统计 | `hm.js`, `baidu.com/hm.gif` |
| CNZZ | `cnzz.com` |
| Mixpanel | `mixpanel.com` |
| Heap | `heap.io` |
| Hotjar | `hotjar.com` |
| Amplitude | `amplitude.com` |

### CDN 识别
| CDN | 识别特征 |
|-----|---------|
| Cloudflare | `cloudflare.com`, `cloudflarestream` |
| Akamai | `akamaized.net` |
| Fastly | `fastly.net` |
| 阿里云 CDN | `alicdn.com` |
| 腾讯云 CDN | `qcloud.com` |

### 支付集成
| 支付 | 识别特征 |
|-----|---------|
| Stripe | `stripe.com/v3/` |
| PayPal | `paypal.com`, `paypalobjects.com` |
| 支付宝 | `alipay.com` |
| 微信支付 | `wxpay.com`, `wechatpay` |

---

## 功能模块分类标准

### 用户系统复杂度评级

**简单**：仅注册/登录
**中等**：+ 个人资料、头像、地址管理
**复杂**：+ 会员体系、积分、等级、邀请码

### 内容系统复杂度评级

**简单**：静态页面
**中等**：+ 博客/新闻列表
**复杂**：+ 评论、点赞、分享、收藏、打赏

### 交易系统复杂度评级

**简单**：定价页（无交易）
**中等**：+ 立即购买/咨询表单
**复杂**：+ 购物车、在线支付、订单管理、发票、退款

### 社区系统复杂度评级

**简单**：无社区
**中等**：+ 评论区、问答
**复杂**：+ 论坛、私信、等级、勋章、积分商城

---

## 商业模式识别

| 模式 | 典型特征 |
|-----|---------|
| B2B SaaS | 定价分级、演示申请、合同条款、企业客服 |
| B2C 电商 | 产品页、购物车、促销、用户评价 |
| C2C 平台 | 卖家入驻、商品发布、担保交易、评价体系 |
| 内容付费 | 付费墙、会员专属、付费专栏 |
| 广告变现 | 大量广告位、内容引流 |
| 免费+增值 | Freemium、功能分级、高级版 |
