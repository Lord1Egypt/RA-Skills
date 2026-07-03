# Unified Digest

这个 skill 不是摘要生成器，而是一个统一订阅入口。它放在：

- `follow-builders`
- `med-builders`

前面，负责在会话开始时判断是否要主动询问用户是否订阅。

共享状态文件保存在 `~/.unified-digest/subscriptions.json`。

## 它解决的问题

- 避免两个 skill 分别各问一遍
- 支持“暂不”和“不再提示”
- 共享频率、时间、时区、语言、投递方式等默认设置
- 让 `follow-builders` 和 `med-builders` 可以并存

## 目录说明

- `SKILL.md`：agent 的路由规则
- `config/subscription-schema.json`：订阅状态结构
- `scripts/subscription-state.js`：读写共享状态的辅助脚本
- `scripts/state-lib.js`：给钩子和状态脚本复用的状态库
- `scripts/startup-hook.js`：给宿主调用的启动钩子
- `templates/`：宿主接入模板

## 典型流程

1. agent 先执行 `node scripts/subscription-state.js should-prompt`
2. 如果需要询问，就向用户展示统一订阅问题
3. 把用户回答写入共享状态
4. 再分流到 `follow-builders`、`med-builders` 或两个都走

## 宿主接入

如果你的 runtime 支持“新会话启动前执行命令”，直接调用：

```bash
node /absolute/path/to/unified-digest/scripts/startup-hook.js --format json --lang zh --mark-asked
```

返回的 JSON 会告诉宿主：

- 当前是否应该主动询问
- 应该展示给用户的精确文案
- 这轮是否继续正常 agent 路由
