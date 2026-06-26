---
name: yiming-weibo-daily
description: "张一鸣微博金句飞书私聊技能。安装后每小时推送一条张一鸣微博精选，附主题标签和今日练习。适用于安装、配置、试发和排查。"
metadata: {"openclaw":{"emoji":"🌸","homepage":"https://github.com/Rocke1001feller/yiming-weibo-daily","requires":{"env":["ALICE_FEISHU_APP_ID","ALICE_FEISHU_APP_SECRET","ALICE_FEISHU_TARGET_OPEN_ID"],"anyBins":["python3","python"]},"primaryEnv":"ALICE_FEISHU_APP_SECRET"},"publish":{"recommendedVersion":"1.0.0"}}
---

# yiming-weibo-daily

每小时从张一鸣 2009-2016 年微博中精选一条金句，配上主题标签和今日练习，通过飞书私聊发给用户。

## 使用场景

当用户要做下面任一件事时，使用这个技能：

1. 从 GitHub 或 ClawHub 安装这个技能。
2. 让助手自动配置这个技能并尽量复用现有飞书通道配置。
3. 试发一条当前时段的内容。
4. 排查为什么没有自动发送或为什么发送失败。

## 默认工作方式

这个技能的公开分发模型是 chat-first，不是手工下载 ZIP 再自己跑命令。

如果用户在飞书聊天里给出 GitHub 仓库地址或 ClawHub 地址，并说“帮我安装并配置这个技能”，你应当自己完成下面的动作：

1. 安装技能到当前 OpenClaw 工作区。
2. 检查是否已有可复用的飞书通道凭据和用户标识。
3. 为这个技能写入所需环境变量或技能配置。
4. 先预览一次，再试发一次。
5. 成功后再帮助用户接上每小时执行。

## 安装指令

### GitHub 来源

如果用户提供的是 GitHub 仓库地址：

1. 获取仓库内容。
2. 将仓库根目录作为技能目录安装到当前工作区。
3. 如有需要，提示用户开启一个新 session，让 OpenClaw 重新加载技能。

### ClawHub 来源

如果用户提供的是 ClawHub 地址或 slug：

1. 使用 OpenClaw/ClawHub 的标准安装方式安装这个技能。
2. 安装后继续执行配置和验证，不要停在“已安装”。

## 配置优先级

优先按照下面顺序找配置，不要一上来就要求用户手工填写新凭据：

1. 当前 OpenClaw 的飞书通道上下文。
2. 当前运行环境中已存在的飞书相关环境变量。
3. 当前技能或其他现有技能的可复用飞书配置。
4. 只有前面都找不到时，才向用户索取 `App ID`、`App Secret` 和目标 `open_id`。

目标是为本技能提供这三个运行变量：

1. `ALICE_FEISHU_APP_ID`
2. `ALICE_FEISHU_APP_SECRET`
3. `ALICE_FEISHU_TARGET_OPEN_ID`

如果当前聊天上下文可以可靠识别接收人，默认将当前用户作为接收目标。

## 验证步骤

配置完成后按这个顺序验证：

1. 预览当前时段内容，不发消息：

```bash
python3 {baseDir}/scripts/alice_cron.py --preview
```

2. 执行一次真实试发：

```bash
python3 {baseDir}/scripts/alice_cron.py
```

3. 向用户汇报：
   是否安装成功。
   是否复用了现有飞书配置。
   是否试发成功。
   下一次自动发送大致会在什么时候发生。

## 自动运行

这个脚本的核心能力是“单次生成并发送当前时段内容”。

如果当前 OpenClaw 环境支持原生调度、heartbeat 或等价机制，优先使用宿主已有能力实现“每小时执行一次”。

如果环境没有原生调度，再回退到宿主机任务系统，例如 cron。

## 排查规则

如果用户说没有收到消息，按这个顺序排查：

1. 先跑 `--preview`，确认素材和文案生成正常。
2. 再跑一次真实发送，确认飞书接口是否报错。
3. 检查 `ALICE_FEISHU_*` 变量是否存在。
4. 检查目标 `open_id` 是否正确。
5. 检查调度有没有真的执行到脚本。

## 内容说明

1. 素材文件位于 `{baseDir}/assets/weibo_quotes.txt`。
2. 脚本会按日期和小时选择当期内容。
3. 运行时会记录已发送内容和近期练习，以减少短期重复。

## 开发模式

如果用户明确要求手工本地运行，也可以直接用下面的环境变量：

```bash
export ALICE_FEISHU_APP_ID="cli_xxxxxxxxxx"
export ALICE_FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxx"
export ALICE_FEISHU_TARGET_OPEN_ID="ou_xxxxxxxxxxxx"
python3 {baseDir}/scripts/alice_cron.py --preview
python3 {baseDir}/scripts/alice_cron.py
```
