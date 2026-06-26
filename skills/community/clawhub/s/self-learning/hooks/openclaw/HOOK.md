# OpenClaw Hook 配置

## 安装

```bash
# 复制 Hook 到 OpenClaw hooks 目录
cp -r hooks/openclaw ~/.openclaw/hooks/self-learning

# 启用 Hook
openclaw hooks enable self-learning
```

## 配置

在 `~/.openclaw/config.json` 中添加:

```json
{
  "hooks": {
    "self-learning": {
      "enabled": true,
      "onSessionStart": true,
      "onPromptSubmit": true,
      "workspace": "/root/.openclaw/workspace"
    }
  }
}
```

## Hook 类型

### onSessionStart
- **触发时机**: 新会话开始时
- **功能**: 检查待处理的高优先级学习记录
- **行为**: 在系统提示后注入提醒消息

### onPromptSubmit
- **触发时机**: 用户提交 prompt 后
- **功能**: 检测用户纠正信号
- **行为**: 建议记录学习内容

## 信号检测

### 纠正信号 (中文)
- "不对"
- "错了"
- "不是这样"
- "应该是"
- "你搞错了"

### 纠正信号 (英文)
- "actually"
- "no,"
- "wrong,"
- "incorrect,"
- "should be"

## 禁用 Hook

```bash
openclaw hooks disable self-learning
```

## 卸载

```bash
rm -rf ~/.openclaw/hooks/self-learning
```
