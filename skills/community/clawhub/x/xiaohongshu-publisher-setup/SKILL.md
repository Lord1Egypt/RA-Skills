---
name: xiaohongshu-publisher-setup
description: "部署小红书发布Agent团队（灵格排版设计+星阑运营发布），含XHS格式排版、浏览器自动化发布、数据分析。使用 /xiaohongshu-publisher-setup 触发部署，需先安装 content-creation。"
license: MIT
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["node","npm"]}}}
---

# 小红书发布团队 - 自动部署

当用户调用 /xiaohongshu-publisher-setup 时，执行以下步骤部署 2 人小红书发布 Agent 团队。

## 概述

部署小红书专属的发布团队：
- 灵格（小红书排版设计师）、星阑（小红书运营发布师）

## Step 1：环境检查

1. 确认 OpenClaw 已安装
2. 确认 content-creation 团队已部署（检查 mobai/tanfeng/jinshu 是否已注册）
   - 未部署 → 提示"请先运行 /content-creation 部署内容创作团队"→ **终止**
3. 检查 Playwright 是否已安装：
   ```bash
   node -e "require('playwright')" 2>/dev/null && echo "OK" || echo "MISSING"
   ```
   - 未安装 → 提示：
     ```
     ⚠️  需要安装 Playwright 用于浏览器自动化发布
     请在小红书发布工作目录运行：
       npm install playwright
       npx playwright install chromium
     安装后重新运行 /xiaohongshu-publisher-setup
     ```
     → **终止**
4. 检查是否已存在 lingge/xinglan Agent
   - 已存在 → 提示是否覆盖

## Step 2：收集账号信息

向用户说明：以下信息将写入 Agent 的 USER.md，帮助生成更精准的小红书内容。

依次询问：
1. 账号昵称和定位（如"职场穿搭博主"）
2. 目标受众（如"18-30岁职场女性"）
3. 主要内容方向/领域（如"穿搭、职场、生活方式"）
4. 内容风格偏好（如"干货为主 / 故事化 / 轻松幽默"）

可选：
5. 发布频率（如"每周2-3篇"）
6. 账号目前粉丝规模（帮助星阑设定数据预期）

将账号信息写入配置：
```bash
mkdir -p ~/.openclaw/workspace-xiaohongshu-publisher
cat > ~/.openclaw/workspace-xiaohongshu-publisher/.env << 'EOF'
XHS_ACCOUNT_NAME=用户输入的账号名
XHS_POSITIONING=用户输入的账号定位
XHS_TARGET_AUDIENCE=用户输入的目标受众
XHS_CONTENT_TOPICS=用户输入的内容方向
XHS_WRITING_STYLE=用户输入的风格偏好
XHS_POST_FREQUENCY=用户输入的发布频率
XHS_FOLLOWER_SCALE=用户输入的粉丝规模
EOF
chmod 600 ~/.openclaw/workspace-xiaohongshu-publisher/.env 2>/dev/null || true
```

## Step 3：部署文件

1. 从 `{baseDir}/templates/` 复制文件到：
   ```
   ~/.openclaw/workspace-xiaohongshu-publisher/lingge/
   ~/.openclaw/workspace-xiaohongshu-publisher/xinglan/
   ```
2. 复制 `{baseDir}/scripts/xhs_publish.cjs` 到 `~/.openclaw/workspace-xiaohongshu-publisher/scripts/`
3. 将 Step 2 收集的信息填充到两个 Agent 的 USER.md 中
4. 创建 session 目录：
   ```bash
   mkdir -p ~/.openclaw/workspace-xiaohongshu-publisher/.session
   ```
5. 输出进度：
   ```
   [1/2] lingge（灵格 - 小红书排版设计师）→ 已部署
   [2/2] xinglan（星阑 - 小红书运营发布师）→ 已部署
   ```

## Step 4：注册 Agent

```bash
openclaw agents add lingge \
  --name "灵格" \
  --workspace "~/.openclaw/workspace-xiaohongshu-publisher/lingge" \
  --description "小红书排版设计师 - XHS格式排版与内容包生成"

openclaw agents add xinglan \
  --name "星阑" \
  --workspace "~/.openclaw/workspace-xiaohongshu-publisher/xinglan" \
  --description "小红书运营发布师 - 自动化发布与数据分析"
```

## Step 5：初始化登录（强烈建议）

询问用户是否现在初始化小红书登录（后续发布必须登录）：
- 用户同意 → 执行：
  ```bash
  node ~/.openclaw/workspace-xiaohongshu-publisher/scripts/xhs_publish.cjs login
  ```
  浏览器将打开小红书，用户手动扫码登录，session 自动保存。
- 用户跳过 → 提示发布前需运行 `check-login` 命令

## Step 6：验证

1. 确认 2 个 agent 注册成功
2. 输出部署报告：
   ```
   ✅ 小红书发布团队部署完成
   ├── 🎭 灵格（排版设计师）    → 已就绪
   └── 📈 星阑（运营发布师）    → 已就绪
   ```
3. 提示：使用 `/xiaohongshu-publish-workflow` 启动小红书发布流水线
4. 发布脚本位置：`~/.openclaw/workspace-xiaohongshu-publisher/scripts/xhs_publish.cjs`

## 错误处理

- content-creation 未部署 → 提示先安装
- Playwright 未安装 → 提示安装命令
- Agent 注册失败 → 检查重名
- 登录失败 → 提示检查网络，或重新运行 login 命令
