# 高级示例：性能优化

## 场景
网站加载速度慢，Lighthouse 评分只有 45 分。

## 前置条件
- 了解 Web 性能指标
- 会使用 Chrome DevTools

## 执行步骤
1. 运行 Lighthouse 审计
2. 分析性能瓶颈
3. 制定优化方案
4. 实施优化
5. 验证效果

## Lighthouse 报告分析
```
性能评分：45

主要问题：
1. FCP（首次内容绘制）3.2s - 目标 <1.8s
2. LCP（最大内容绘制）5.1s - 目标 <2.5s
3. CLS（累积布局偏移）0.25 - 目标 <0.1
4. 总阻塞时间 1.2s - 目标 <200ms
```

## 优化方案

### 1. 资源优化
```html
<!-- 延迟加载非关键 CSS -->
<link rel="preload" href="critical.css" as="style">
<link rel="preload" href="non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

<!-- 异步加载 JavaScript -->
<script src="analytics.js" async></script>
<script src="main.js" defer></script>

<!-- 图片优化 -->
<img src="image.jpg" loading="lazy" decoding="async">
```

### 2. 代码分割
```javascript
// 动态导入
const module = await import('./heavy-module.js');

// React 懒加载
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

### 3. 缓存策略
```javascript
// Service Worker 缓存
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

### 4. 压缩和优化
```bash
# 图片压缩
convert image.jpg -quality 85 image-optimized.jpg

# 代码压缩
npm run build -- --prod

# Gzip/Brotli 压缩
```

## 优化后结果
```
性能评分：92 ✅

FCP：0.8s
LCP：1.5s
CLS：0.05
TBT：80ms
```

## 关键要点
- 优先优化 Largest Contentful Paint
- 减少主线程工作
- 优化资源加载顺序
- 使用浏览器缓存
- 压缩所有资源
