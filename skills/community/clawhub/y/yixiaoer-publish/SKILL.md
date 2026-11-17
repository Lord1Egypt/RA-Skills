---
name: yixiaoer-bootstrap
version: 1.0.0
description: "用于安装蚁小二 CLI、同步正式技能并完成基础配置与环境自检。"
metadata:
  category: "productivity"
  requires:
    bins: ["npm", "npx"]
  cliHelp: "npm install -g @yixiaoermail/cli@latest; yxer --version; yxer skill sync --global; yxer config init --api-key <apiKey>; yxer doctor"
---

# 蚁小二CLI安装助手

以下步骤面向 AI Agent。这个 bootstrap skill 只负责安装 `yxer` CLI 和正式 `yixiaoer` skill；安装、升级、同步完成后应停止，不继续执行发布、账号查询、素材上传或 payload 校验。

## 适用场景

- 用户要在 SkillHub / skills 市场中安装蚁小二能力
- 用户要首次接入 `yxer`
- 用户要升级 CLI 并重新同步正式 skill
- 用户只想看标准安装命令

## 环境要求

开始安装前，请确认环境中已安装：

- Node.js
- npm
- npx

默认优先使用 npm 安装，不引导普通用户从源码构建。

## 第 1 步 安装 CLI

```shell
npm install -g @yixiaoermail/cli@latest
```

说明：

- 这是 bootstrap skill 的标准安装方式。
- 如用户环境限制全局安装，需要明确告知风险后再改用非全局方案。

## 第 2 步 验证 CLI

```shell
yxer --version
```

预期结果：

- 命令成功返回 JSON 版本信息。
- 如果命令不存在或版本检查失败，先回到第 1 步重新安装。

## 第 3 步 同步正式 Skill

```shell
yxer skill sync --global
```

说明：

- `yxer skill sync --global` 是 bootstrap skill 的默认同步方式。
- 如果用户明确只想当前宿主可见、不要求全局安装，可改用 `yxer skill sync`。

## 第 4 步 初始化配置

```shell
yxer config init --api-key <apiKey>
```

说明：

- 让用户提供有效的 API Key 后再执行。
- 如果当前环境已完成配置，可跳过这一步。

## 第 5 步 环境自检

```shell
yxer doctor
```

说明：

- 如果 `doctor` 提示 `_notice.skills` 不一致，优先重新执行 `yxer skill sync --global`。
- 自检通过后，bootstrap 任务结束。

## 升级流程

```shell
npm install -g @yixiaoermail/cli@latest
yxer --version
yxer skill sync --global
yxer doctor
```

## 安装后进入正式能力

安装完成后，引导用户切换到正式 skill：

- 正式 skill 名称：`yixiaoer`
- 正式入口文档：`../yixiaoer/SKILL.md`
- 典型下一步命令：
  - `yxer doctor`
  - `yxer accounts list --help`
  - `yxer publish --help`

## 故障排查

如果安装失败，按以下顺序排查：

1. 确认 Node.js、npm、npx 可用
2. 重新执行 `npm install -g @yixiaoermail/cli@latest`
3. 执行 `yxer --version`
4. 执行 `yxer skill sync --global`
5. 执行 `yxer doctor`

如果需要详细业务文档或正式发布能力，不要在本 skill 内继续，切换到 `yixiaoer` 正式 skill。
