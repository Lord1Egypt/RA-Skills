# 蚁小二CLI安装助手

这个目录给 SkillHub / skills 市场使用，职责只有一件事：把 `yxer` CLI 和正式 `yixiaoer` skill 安装好。

## 环境要求

开始安装前，请确认环境中已安装：

- Node.js
- npm
- npx

## 第 1 步 安装 CLI

```shell
npm install -g @yixiaoermail/cli@latest
```

## 第 2 步 验证 CLI

```shell
yxer --version
```

## 第 3 步 同步正式 Skill

```shell
yxer skill sync --global
```

## 第 4 步 初始化配置

```shell
yxer config init --api-key <apiKey>
```

## 第 5 步 环境自检

```shell
yxer doctor
```

安装完成后，正式业务能力请切换到：

```text
skills/yixiaoer
```

不要把这个 bootstrap skill 当成发布、上传、查询或排障主技能使用。
