# 真实案例：电商网站性能优化

## 背景
电商网站页面加载时间长达 8 秒，跳出率高达 75%，转化率仅 1.2%。

## 问题诊断

### 性能指标
```
初始状态：
- 页面加载时间：8.2s
- 跳出率：75%
- 转化率：1.2%
- Lighthouse 评分：38
```

### 瓶颈分析
使用 Chrome DevTools Performance 分析：
```
主要问题：
1. 主产品图片 2.8MB（未压缩）
2. 加载 45 个 JavaScript 文件
3. 未使用 CDN
4. 服务器响应慢（TTFB 1.5s）
5. 渲染阻塞资源
```

## 优化方案

### 第 1 周：资源优化（立竿见影）
1. **图片压缩**
   - 产品图片：2.8MB → 180KB（WebP 格式）
   - 响应式图片：`srcset` 属性
   - 懒加载：`loading="lazy"`

2. **代码合并**
   - 45 个 JS 文件 → 3 个
   - 启用 Tree-shaking
   - 删除未使用代码

效果：加载时间 8.2s → 3.5s

### 第 2 周：架构优化
1. **CDN 部署**
   - 静态资源迁移到 CDN
   - 全球节点加速

2. **服务器优化**
   - 启用 HTTP/2
   - 开启 Gzip 压缩
   - 优化数据库查询

效果：加载时间 3.5s → 2.1s

### 第 3 周：渲染优化
1. **关键 CSS 内联**
2. **延迟加载非关键资源**
3. **预加载关键资源**
4. **优化 CLS（布局偏移）**

效果：加载时间 2.1s → 1.4s

## 技术细节

### 图片优化
```html
<!-- 响应式图片 -->
<img
  src="product-800.jpg"
  srcset="
    product-400.jpg 400w,
    product-800.jpg 800w,
    product-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 400px, 800px"
  loading="lazy"
  decoding="async"
  alt="产品图片"
>

<!-- WebP 回退 -->
<picture>
  <source srcset="product.webp" type="image/webp">
  <source srcset="product.jpg" type="image/jpeg">
  <img src="product.jpg" alt="产品图片">
</picture>
```

### 代码分割
```javascript
// 路由级代码分割
const ProductList = lazy(() => import('./ProductList'));
const ProductDetail = lazy(() => import('./ProductDetail'));

// 组件级代码分割
const ChatWidget = lazy(() => import('./ChatWidget'));

// 预加载关键路由
<Link to="/product/123" onMouseEnter={() => import('./ProductDetail')}>
```

### 缓存策略
```javascript
// SWR + Service Worker
const CACHE_AGE = 3600; // 1 小时

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response && Date.now() - response.date < CACHE_AGE * 1000) {
        return response;
      }
      return fetch(event.request).then((fetchResponse) => {
        const clonedResponse = fetchResponse.clone();
        clonedResponse.date = Date.now();
        caches.open('v1').then((cache) => {
          cache.put(event.request, clonedResponse);
        });
        return fetchResponse;
      });
    })
  );
});
```

## 效果对比

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 页面加载时间 | 8.2s | 1.4s | -83% |
| Lighthouse 性能 | 38 | 94 | +147% |
| 跳出率 | 75% | 35% | -53% |
| 转化率 | 1.2% | 3.8% | +217% |
| 平均订单价值 | $45 | $52 | +16% |

## 业务影响
```
月收入提升：
优化前：100,000 订单 × $45 = $4,500,000
优化后：380,000 订单 × $52 = $19,760,000
月收入增长：+339%

年化影响：+$182,000,000
```

## 经验教训

1. **监控为王**
   - 持续监控真实用户性能（RUM）
   - 设置性能预算
   - 自动化性能测试

2. **平衡艺术**
   - 性能 vs 功能
   - 速度 vs 体验
   - 成本 vs 收益

3. **渐进式优化**
   - 先解决最明显的瓶颈
   - 逐步深入细节优化
   - 持续迭代改进

4. **团队协作**
   - 性能是团队责任
   - 建立性能规范
   - Code Review 包含性能检查

5. **业务对齐**
   - 用业务指标衡量
   - 量化性能价值
   - 获得管理层支持

## 持续优化
```yaml
# 性能监控配置
performance-budget:
  budgets:
    - path: '/*'
      timings:
        - metric: 'FCP'
          budget: 1000
        - metric: 'LCP'
          budget: 2500
      resourceSizes:
        - resourceType: 'image'
          budget: 200000
        - resourceType: 'script'
          budget: 100000
```

## 工具推荐
- Lighthouse（审计）
- WebPageTest（深度分析）
- Chrome DevTools（调试）
- PageSpeed Insights（在线）
- SpeedCurve（持续监控）
