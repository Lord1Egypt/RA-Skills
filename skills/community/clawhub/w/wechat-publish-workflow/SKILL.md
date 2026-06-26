---
name: wechat-publish-workflow
description: "微信公众号发布流水线：视觉排版→主编审核→API发布→数据复盘。在已有Markdown定稿基础上执行微信格式化和发布。触发词：发布到微信、微信排版、微信发布。需先完成内容创作。"
license: MIT
version: 1.0.0
---

# 微信发布流水线

在已有 Markdown 定稿基础上，完成微信公众号的视觉排版、发布和数据复盘。

## 前置条件

- 已通过 `/content-creation` 部署内容创作团队（墨白参与审核）
- 已通过 `/wechat-publisher-setup` 部署微信发布团队（画境、数澜）
- 已有 Markdown 定稿（来自 `/content-workflow` 或用户直接提供）

## 工作流概述

```
定稿 → 画境(排版设计) → 墨白(审核) → 数澜(发布+复盘)
```

## Phase 3：微信排版设计（画境主导，墨白审核）

1. 画境根据定稿完成：
   - 封面大图（900x383px）
   - 封面小图（200x200px）
   - 文章排版（HTML/编辑器源码）
   - 配图/信息图（如有需要）
2. 提交给墨白审核
3. 最多迭代 2 轮
4. 输出物：视觉定稿

## Phase 4：发布与复盘（数澜主导）

### 4.1 发布前准备
1. 数澜根据历史数据确定最佳发布时间
2. 确认 `.env` 中微信 API 凭证已配置
3. 验证 API 连通性：`node {baseDir}/scripts/wechat_publish.cjs token`

### 4.2 素材上传
1. 上传封面大图：
   ```bash
   node {baseDir}/scripts/wechat_publish.cjs upload-thumb <封面图路径>
   ```
2. 如正文含配图，逐张上传：
   ```bash
   node {baseDir}/scripts/wechat_publish.cjs upload-image <图片路径>
   ```

### 4.3 创建草稿
1. 组装文章 JSON 并提交：
   ```bash
   node {baseDir}/scripts/wechat_publish.cjs create-draft draft.json
   ```

### 4.4 用户确认发布
1. 展示发布预览信息
2. **必须获得用户明确确认后才能执行发布**
3. 用户确认后：
   ```bash
   node {baseDir}/scripts/wechat_publish.cjs publish <草稿media_id>
   ```
4. 查询发布状态：
   ```bash
   node {baseDir}/scripts/wechat_publish.cjs get-status <publish_id>
   ```

### 4.5 数据追踪与复盘
1. 发布后 24h 拉取初步数据：
   ```bash
   node {baseDir}/scripts/wechat_publish.cjs get-stats <日期> <日期>
   ```
2. 输出 24h 数据快报
3. 发布后 48h 输出完整数据复盘报告
4. 墨白主持复盘，确定下一轮优化方向

## 灵活调用规则

- 用户可以跳过排版（如"直接发布这篇文章"）
- 用户可以只做排版不发布
- 用户可以单独让数澜分析数据

## 质量门控

- 排版设计需经墨白审核
- 发布操作必须获得用户明确确认
- 发现事实性错误 → 回退到内容创作阶段（使用 /content-workflow）

## 脚本说明

`wechat_publish.cjs` 位于 `{baseDir}/scripts/` 或已部署到 `~/.openclaw/workspace-wechat-publisher/scripts/`。
