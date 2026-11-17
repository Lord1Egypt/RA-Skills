---
name: xinling-bushou-v2
description: 心灵补手 V4.0 - explicit, session-scoped companion personas
author: William Chen
homepage: https://aceworld.top
tags: [personality, companion, session-scoped, openclaw]
metadata: {"clawdbot":{"emoji":"💖","version":"4.0.0","requires":{}}}
---

# 心灵补手 V4.0

心灵补手提供可选的人格风格和陪伴语气。人格只有在用户明确选择后，才作用于当前会话或当前子代理。

## 安全边界

- 只生成会话级风格片段，不修改宿主代理的持久身份文件。
- 不自动执行 shell 命令，不请求权限提升，不读取外部凭证。
- 不根据普通关键词或情绪自动激活。
- 外部 persona 文件会经过格式、长度、路径和内容边界检查。
- 人格风格不能覆盖平台、开发者、安全规则或当前用户任务。

## 安装

```bash
./scripts/install.sh
```

安装只复制运行时文件，并创建独立的状态目录。

## CLI

```bash
xinling list
xinling show songzhiwen
xinling test songzhiwen
xinling activate songzhiwen --session-id my-session
```

`activate` 输出可传给当前会话或子代理的风格片段，不会自动写入宿主配置。

## 人格

包内提供六种可选人格：魏忠贤、平儿、早喵、来问司机、宋之问和刘伯温。刘伯温的玄学内容属于用户明确选择后的角色化表达，不会在普通对话中主动触发，也不替代现实世界的专业判断。

## 版本

| 版本 | 变化 |
| --- | --- |
| 4.0.0 | 移除持久身份注入，关闭默认自动触发，增加路径和 persona 边界校验，发布包改为 allowlist |
| 3.5.1 | 旧版人格模块 |
