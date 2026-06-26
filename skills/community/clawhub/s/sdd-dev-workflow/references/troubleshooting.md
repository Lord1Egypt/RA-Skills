# 问题排查指南

## 常见问题 FAQ

### Q1: specify init 失败？
**原因**：网络问题或 GitHub 限流
**解决方案**：
1. 使用 `--force` 跳过确认
2. 设置 GitHub Token：`export GH_TOKEN=xxx`
3. 使用代理或更换网络

### Q2: specify init 卡住？
**原因**：交互式确认等待输入
**解决方案**：
```bash
# 使用 --here --force 跳过确认
specify init . --here --force --ai claude --no-git
```

### Q3: 需求澄清不完怎么办？
采用**分阶段、小粒度**拆分，每个迭代只做 MVP。

### Q4: 上下文丢失怎么办？
规范文档是锚点，不依赖对话历史。重要阶段提醒关键约束。

### Q5: 实现一半发现需求错了？
放弃当前迭代，git 回滚，重新开始。

### Q6: 前端开发怎么做？
借助组件库（shadcn、heroui），让 Agent 使用现成组件。

### Q7: Claude Code 连接失败？
**错误**：`Unhandled stop reason: network_error`
**原因**：Gateway 网络问题
**解决方案**：
```bash
# 检查 gateway 状态
openclaw gateway status

# 重启 gateway
openclaw gateway restart
```

### Q8: 项目初始化超时？
**原因**：Speckit 模板下载慢
**解决方案**：脚本已内置 60 秒超时和降级方案

### Q9: `python` vs `python3` 问题？
**原因**：Claude Code 生成的代码使用 `python3`，但系统只有 `python3`
**解决方案**：
1. 在测试时使用 `python3` 而非 `python`
2. 或在代码中添加 shebang：`#!/usr/bin/env python3`

### Q10: 外部 API 网络不可达？
**原因**：某些 API（如 wttr.in）国内被 GFW 限制
**解决方案**：设置代理环境变量
```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
python3 src/weather.py 北京
```

### Q11: 交互式确认太多？
**原因**：Claude Code 默认每个命令都需要确认
**解决方案**：使用 `--permission-mode` 参数
```bash
# 方案 A：自动接受编辑操作（推荐）
claude --permission-mode acceptEdits

# 方案 B：跳过所有权限检查（仅限沙箱环境）
claude --dangerously-skip-permissions

# 在脚本中使用
./claude-code-helper.sh start my-project /path/to/project acceptEdits
```

### Q12: sessions_spawn 返回 forbidden？
**原因**：agent ID 未在 allowAgents 中配置
**解决方案**：
```javascript
// 检查当前配置
agents_list()

// 添加 agent ID
gateway({
  action: "config.patch",
  raw: {
    agents: {
      list: [{
        id: "main",
        subagents: {
          allowAgents: ["dev-agent", "research-agent", "test-agent"]
        }
      }]
    }
  }
})
```

### Q13: 子 agent 任务超时？
**原因**：任务执行时间超过 runTimeoutSeconds
**解决方案**：
1. 增加 runTimeoutSeconds（如 7200 = 2小时）
2. 优化任务粒度，拆分成更小的子任务

### Q14: 子 agent 无法启动 Claude Code？
**原因**：tmux 会话权限或环境变量问题
**解决方案**：
```bash
# 检查 tmux socket 权限
ls -la /tmp/openclaw-tmux-sockets/

# 检查 Claude Code 路径
which claude

# 手动测试启动
claude --permission-mode acceptEdits
```

## 问题排查清单

遇到问题时按此顺序检查：

```
1. [ ] Gateway 是否正常运行？
   → openclaw gateway status

2. [ ] 大模型 API 是否可用？
   → 测试简单对话

3. [ ] 环境依赖是否满足？
   → ~/.openclaw/skills/sdd-dev-workflow/scripts/check-environment.sh

4. [ ] Speckit 是否可用？
   → specify --help

5. [ ] 网络是否通畅？
   → curl -s https://api.github.com | head -5

6. [ ] tmux 会话是否正常？
   → tmux -S /tmp/openclaw-tmux-sockets/claude-code.sock ls

7. [ ] 子 agent 是否配置？
   → agents_list()

8. [ ] 项目进度文件是否存在？
   → cat projects/your-project/.task-context/progress.json
```

## 错误恢复策略

### 网络错误
```bash
# 重试 3 次
for i in {1..3}; do
  if claude --permission-mode acceptEdits; then
    break
  fi
  sleep 5
done
```

### API 限流
```bash
# 指数退避
wait_time=10
for i in {1..5}; do
  if python3 test.py; then
    break
  fi
  sleep $wait_time
  wait_time=$((wait_time * 2))
done
```

### 任务卡住
```bash
# 检查进度文件
cat .task-context/checkpoint.md

# 手动恢复
# 发送恢复指令给 agent
```

## 日志查看

### Gateway 日志
```bash
# 实时查看
journalctl --user -u openclaw-gateway -f

# 查看最近 100 行
journalctl --user -u openclaw-gateway -n 100
```

### 子 agent 日志
```bash
# 查看特定 session
cat /home/admin/.openclaw/agents/dev-agent/sessions/<session-id>.jsonl | tail -50

# 查看所有子 agent session
sessions_list({ kinds: ["isolated"] })
```

### 项目日志
```bash
# 查看项目进度
cat projects/your-project/.task-context/session-log.md

# 查看错误记录
cat projects/your-project/.task-context/error.log
```
