# Changelog

## v1.0.1 (2026-06-24) — Security audit fixes

### 隐私与安全增强
- 隐私表新增：数据保留期限（日志 14 天）、删除策略、第三方共享声明（明确"无"）
- `core/recipe.py` `find_dishes()` 和 `find_disease_recipes()` 添加内联隐私警告
- SKILL.md / SKILL.zh.md curl 示例前增加隐私提示
- 添加隐私政策链接 (https://tcmplate.com/privacy)

## v1.0.0 (2026-06-12) — 首次发布

### 核心功能
- POST /api/diagnose — 症状辨证 → 证型 + 食疗方案
- POST /api/search — 9 个知识库全文检索
- 免费 10 次/日，无需 API Key（零认证）
- 付费 $5/月，不限次数

### Python 客户端
- `core/diagnose.py` — 辨证引擎
- `core/search.py` — 知识检索（含 get_ingredient）
- `core/recipe.py` — 食谱推荐
- `core/tea.py` — 茶饮推荐

### 隐私与安全
- 代码层字段白名单过滤（防个人信息误传）
- HTTPS 加密传输
- 服务端不保留症状查询内容日志
- 完整隐私披露 + consent 声明
