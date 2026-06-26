---
name: spm-performance
version: 1.0.0
description: 性能规范 — Agent 经常写O(n²)、不缓存、不懒加载。本技能给最低性能底线。SPM Phase 4 自动引用。
---

# SPM Performance — 性能规范

## 自动检测

SPM Phase 4 质量阶段检测到前端/后端/数据库任务 → 自动引用本技能的性能底线。

## 独立使用

不走 SPM 也可以直接说："按 spm-performance 检查这段代码的性能。"

---

## 前端性能底线

| 项 | 底线 | 检查方法 |
|----|------|---------|
| 图片 | `loading="lazy"` + 指定宽高 + WebP 格式 | Lighthouse |
| 字体 | 不超过 2 种，用 `font-display: swap` | DevTools Network |
| 首屏 JS | 不超过 200KB (gzipped) | `npm run build && ls -lh dist/` |
| 列表 > 100 条 | 虚拟滚动 | react-window / vue-virtual-scroller |
| 大体积依赖 | `React.lazy` / `defineAsyncComponent` | `npm ls --depth=0` |
| 重渲染 | React.memo / useMemo / useCallback（只在有性能问题时加） | React DevTools Profiler |
| 动画 | 用 `transform`/`opacity`，不用 `left`/`top`/`width` | 手动审查 |

---

## 后端性能底线

| 项 | 底线 |
|----|------|
| 数据库查询 | 单次请求 ≤ 5 条查询 |
| N+1 | JOIN / `WHERE id IN (...)` 替代循环查询 |
| 缓存 | 高频读取数据加 Redis/内存缓存，设置 TTL |
| 分页 | 所有列表接口默认分页（`LIMIT 20`） |
| 慢查询 | `EXPLAIN ANALYZE` 分析，确保走索引 |
| 并发 | 独立 I/O 操作用 `Promise.all` |

---

## Agent 常见性能反模式

| # | 反模式 | 代价 | 修复 |
|---|--------|------|------|
| 1 | **循环里查数据库** | N+1，1000条数据 = 1001次查询 | `WHERE id IN (...)` 或 JOIN |
| 2 | **全量加载不分页** | 内存炸、首屏 10s+ | `LIMIT 20 OFFSET 40` |
| 3 | **不缓存热数据** | 每次请求重算 | Redis / 内存 Map + TTL |
| 4 | **同步阻塞** | 慢操作堵住所有请求 | async / Worker threads |
| 5 | **前端不拆包** | 首屏下载 2MB JS | `React.lazy` + dynamic import |
| 6 | **useEffect 无限循环** | CPU 100%，页面卡死 | 检查依赖数组 |

---

## 性能规则

```
✅ 先跑 Lighthouse / EXPLAIN，确认慢再优化
✅ 一次只改一个瓶颈，改完就测
✅ 缓存 > 算法优化 > 硬件升级（性价比顺序）

❌ 没测就优化（可能优化了一个不慢的东西）
❌ 过早优化（"我觉得这里会慢"）
❌ micro-optimization（for vs forEach 差 0.1ms）
```

**铁律：没有性能数据不走优化。先 proof 有瓶颈，再动手。**
