# 微信公众号文章读取器 - 优先级与降级

## fetch 抓取正文

| 优先级 | 方法 | 依赖 | 成功率 |
|--------|------|------|--------|
| P1 | curl 多 UA（免费） | 无 | ~80% |
| P2 | mptext API（开源项目，需 API key） | API key | ~70% |
| P3 | requests + Cookie | Cookie | ~60% |

- P1 优先，不需要 Cookie，一次网络请求拿到标题+正文
- P2 为 mptext 开源项目，内容完整但不带标题（需 curl 补标题）
- P3 是最后兜底，需要 Cookie

### 局限性
- **内容被截断**：部分文章（含 JS 验证）只能拿到开头 ~800 字，换 P2 可能拿到完整版

---

## list 公众号文章列表

| 优先级 | 方法 | 依赖 | 成功率 |
|--------|------|------|--------|
| P1 | mptext API（开源项目，需 API key） | API key | ~80% |
| P2 | 原生 API | Cookie | ~90% |

### 局限性
- **历史文章不全**：原生 API 最多约 436 篇，更早历史无法翻到

---

## full 列表 + 每篇摘要

同 list 优先级，先 P1 mptext，失败则 P2 Cookie。

---

## compare / resolve / mpsearch / mparticles / mparticles_by_url

同 list，先 mptext API，失败则 Cookie。

### 局限性
- **resolve**：标题过于泛化可能导致匹配失败



## stats

| 优先级 | 方法 | 依赖 | 成功率 |
|--------|------|------|--------|
| P1 | trends API | 无 | ~60% |

### 局限性
- 仅对爆款文章有效，新文章直接用 fetch 分析正文

---

## Cookie 失效表现

- token 获取返回 ret≠0
- 搜索返回空列表
- 修复见 `../env-guide.md`

## 浏览器兜底

所有 API 失效时：mavis-browser 截图 + 图像理解
