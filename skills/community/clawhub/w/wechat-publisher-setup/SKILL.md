---
name: wechat-publisher-setup
description: "部署微信公众号发布Agent团队（画境视觉设计+数澜运营发布），含封面设计、排版美化、API发布、数据分析。使用 /wechat-publisher-setup 触发部署，需先安装 content-creation。"
license: MIT
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---

# 微信公众号发布团队 - 自动部署

当用户调用 /wechat-publisher-setup 时，执行以下步骤部署 2 人微信发布 Agent 团队。

## 概述

部署微信公众号专属的发布团队：
- 画境（视觉设计师）、数澜（运营分析师）

## Step 1：环境检查

1. 确认 OpenClaw 已安装
2. 确认 content-creation 团队已部署（检查 mobai/tanfeng/jinshu 是否已注册）
   - 未部署 → 提示"请先运行 /content-creation 部署内容创作团队"→ **终止**
3. 检查是否已存在 huajing/shulan Agent
   - 已存在 → 提示是否覆盖

## Step 2：配置微信公众平台 API

向用户说明：API 对接用于自动化发布和数据拉取。

依次询问：
1. 账号类型：订阅号 / 服务号
2. AppID（公众平台后台 → 开发 → 基本配置）
3. AppSecret

可选：
4. 是否已将服务器 IP 加入白名单？

将凭证写入安全配置文件：
```bash
mkdir -p ~/.openclaw/workspace-wechat-publisher
cat > ~/.openclaw/workspace-wechat-publisher/.env << 'EOF'
WECHAT_APP_ID=用户输入的AppID
WECHAT_APP_SECRET=用户输入的AppSecret
WECHAT_API_BASE=https://api.weixin.qq.com
WECHAT_ACCOUNT_TYPE=用户选择的账号类型
EOF
chmod 600 ~/.openclaw/workspace-wechat-publisher/.env 2>/dev/null || true
```

验证连通性：
```bash
node {baseDir}/scripts/wechat_publish.cjs token
```

## Step 3：部署文件

1. 从 `{baseDir}/templates/` 复制文件到：
   ```
   ~/.openclaw/workspace-wechat-publisher/huajing/
   ~/.openclaw/workspace-wechat-publisher/shulan/
   ```
2. 复制 `{baseDir}/scripts/wechat_publish.cjs` 到 `~/.openclaw/workspace-wechat-publisher/scripts/`
3. 输出进度：
   ```
   [1/2] huajing（画境 - 视觉设计师）→ 已部署
   [2/2] shulan（数澜 - 运营分析师）→ 已部署
   ```

## Step 4：注册 Agent

```bash
openclaw agents add huajing \
  --name "画境" \
  --workspace "~/.openclaw/workspace-wechat-publisher/huajing" \
  --description "微信视觉设计师 - 封面设计与排版美化"

openclaw agents add shulan \
  --name "数澜" \
  --workspace "~/.openclaw/workspace-wechat-publisher/shulan" \
  --description "微信运营分析师 - API发布与数据分析"
```

## Step 5：验证

1. 确认 2 个 agent 注册成功
2. 输出部署报告：
   ```
   ✅ 微信发布团队部署完成
   ├── 🎨 画境（视觉设计师）    → 已就绪
   └── 📊 数澜（运营分析师）    → 已就绪
   ```
3. 提示：使用 `/wechat-publish-workflow` 启动微信发布流水线
4. 发布脚本位置：`{baseDir}/scripts/wechat_publish.cjs`

## 错误处理

- content-creation 未部署 → 提示先安装
- 微信 API token 获取失败 → 检查 AppID/AppSecret、IP 白名单
- Agent 注册失败 → 检查重名
