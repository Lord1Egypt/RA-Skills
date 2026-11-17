# safe-execution

防工具循环烧钱的自律技能。详见 [SKILL.md](./SKILL.md)。

## 安装

```bash
openclaw skills install safe-execution
```

或从源码安装:

```bash
git clone https://github.com/openclaw/skills/safe-execution
openclaw skills install ./safe-execution
```

## 快速验证

安装后,向你的 agent 发出任意会失败多次的工具调用,观察是否在第 3 次重试时主动停止并询问你。

## 许可证

MIT