# 元阁复杂场景走查

## 走查 1：新智能体初始化

目标：在一台新机器上为 Codex 安装元阁家族。

1. 查看清单：

```bash
npx -y @yottameta/yotta-skills --list
```

2. 安装到默认目录：

```bash
npx -y @yottameta/yotta-skills --agent codex
```

3. 核对结果：输出应包含安装路径与成功 / 跳过 / 失败汇总。

4. 重启会话后输入“列出已装技能”，确认注册表能读取到新技能。

## 走查 2：版本漂移更新

背景：本机已装 27 个技能，其中 5 个版本落后。

1. 只读检查：

```bash
npx -y @yottameta/yotta-skills update --check --agent codex
```

2. 如果由后台调度执行，改用周检入口：

```bash
npx -y @yottameta/yotta-skills update --check --scheduled --agent codex
```

未到期时不联网；到期只检查一次并把结果写入 `~/.yottaskills/update-check.json`。

3. 根据输出确认可更新清单。

4. 执行增量更新：

```bash
npx -y @yottameta/yotta-skills update --agent codex
```

5. 复核：已最新的技能应显示跳过，落后的技能显示更新；失败项单独重装。

## 走查 3：按路由安装单个技能

用户需求：“帮我做发布前质量检查。”

1. 路由：

```bash
npx -y @yottameta/yotta-skills --route "发布前质量检查"
```

2. 输出建议组合与缺失技能。

3. 只安装缺失技能：

```bash
npx -y @yottameta/yotta-skills install yotta-code-quality yotta-anti-shallow --agent codex
```

4. 重新执行路由，确认缺失技能已补齐。
