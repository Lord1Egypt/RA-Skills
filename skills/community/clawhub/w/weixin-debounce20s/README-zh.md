# weixin-debounce20s

**类型**：**纯指导型**设置技能。**不含补丁文件、不安装任何插件包**。agent 执行时按 `SKILL.md` 的规格，**直接修改你机器上已安装的微信渠道插件**，使其具备 20s 连发防抖（**尾窗**：每条可合并的纯文本都会重启 20 秒静默窗口；距最后一条文字满 20 秒后提交；单条也等满 20 秒）。

## 它如何带来能力

agent 按 `SKILL.md` 执行：

1. 定位本机微信插件（`openclaw plugins inspect openclaw-weixin --json`）并记录版本；**已实现则只校验**（幂等）；
2. 按规格在插件的纯文本入站路径上实现防抖（缓冲 + 可重启计时器 + generation 防误触发；8 条 / 6000 字提前提交；媒体与斜杠命令立即处理；串行分发）；
3. 征得你的明确同意，并**先备份**每个被修改的文件；
4. 重启 gateway；
5. 用日志（`debounce: buffered … windowMs=20000`）与连发实测验证。

官方插件升级会覆盖改动——重新运行本技能即可重打。回滚 = 用第 3 步备份覆盖回去（或重装官方同版本）。

文件：`SKILL.md`（规格 + 执行）、`README.md`/`README-zh.md`、`LICENSE`(MIT)。

## 新机用法

```bash
openclaw skills install @yechang1450/weixin-debounce20s
# 然后对 ClawBot 说：启用防抖 / 防抖没生效
```

agent 修改插件文件前一定会先征得同意，并先做备份。

## 触发词（收窄，限渠道语境）

启用微信防抖 / 防抖没生效 / openclaw-weixin 防抖

仅在用户明确要求为 `openclaw-weixin` 渠道启用或修复防抖时执行；改动任何文件前先征得确认，且**绝不以提权方式**执行写入或构建。
