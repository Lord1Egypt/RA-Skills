# OpenClaw 集成指南

## 快速开始

### 1. 安装压缩技能
```bash
# 将压缩代理移动到技能目录
cp -r context-compactor ~/.agents/skills/

# 或者使用软链接
ln -s $(pwd)/context-compactor ~/.agents/skills/context-compactor
```

### 2. 在OpenClaw中启动压缩代理

#### 方法一：直接启动
```bash
# 启动压缩代理
sessions_spawn(
  runtime: "subagent",
  task: "启动上下文压缩代理，采用分层压缩策略，基于内存使用触发机制。监控对话历史，自动优化token使用。",
  label: "context-compactor",
  model: "deepseek-chat"
)
```

#### 方法二：通过技能启动
```bash
# 使用技能启动
exec("cd ~/.agents/skills/context-compactor && ./start.sh")
```

### 3. 配置自动触发

#### 定时检查内存使用
```bash
# 每5分钟检查一次
cron(
  action: "add",
  job: {
    name: "定期检查内存使用",
    schedule: { kind: "every", everyMs: 300000 },
    sessionTarget: "main",
    payload: {
      kind: "systemEvent",
      text: "检查当前token使用情况，如需压缩则触发压缩代理"
    }
  }
)
```

#### 基于消息数量触发
```bash
# 每50条消息触发一次
cron(
  action: "add",
  job: {
    name: "消息数量触发压缩",
    schedule: { kind: "every", everyMs: 60000 },  # 每分钟检查
    sessionTarget: "isolated",
    payload: {
      kind: "agentTurn",
      message: "检查最近消息数量，如果超过50条则触发压缩"
    }
  }
)
```

## 使用示例

### 1. 手动触发压缩
```bash
# 发送压缩请求
sessions_send(
  sessionKey: "context-compactor",
  message: "压缩当前上下文，token使用率85%，消息数量120条"
)

# 或者通过API
exec("curl -X POST http://127.0.0.1:8081/api/compact -H 'Content-Type: application/json' -d '{\"token_usage\": 0.85}'")
```

### 2. 获取压缩统计
```bash
# 获取统计信息
sessions_send(
  sessionKey: "context-compactor",
  message: "报告当前压缩统计和内存使用情况"
)

# 或者通过API
exec("curl http://127.0.0.1:8081/api/stats")
```

### 3. 更新压缩配置
```bash
# 更新配置
sessions_send(
  sessionKey: "context-compactor",
  message: "更新压缩配置：token阈值调整为80%，HOT层消息数量调整为15条"
)

# 或者通过API
exec("curl -X POST http://127.0.0.1:8081/api/config -H 'Content-Type: application/json' -d '{\"token_threshold\": 0.8, \"hot_threshold\": 15}'")
```

## 集成到心跳检查

### 1. 修改 HEARTBEAT.md
```markdown
# HEARTBEAT.md - 压缩代理监控

## 定期检查
1. 检查压缩代理运行状态
2. 检查token使用情况
3. 检查压缩统计
4. 必要时触发压缩

## 检查脚本
```bash
# 检查压缩代理状态
if curl -s http://127.0.0.1:8081/api/health | grep -q "healthy"; then
  echo "压缩代理运行正常"
  
  # 获取当前统计
  stats=$(curl -s http://127.0.0.1:8081/api/stats)
  token_usage=$(echo $stats | jq '.current_stats.current_token_usage')
  
  # 如果token使用超过阈值，触发压缩
  if (( $(echo "$token_usage > 0.7" | bc -l) )); then
    echo "token使用率过高 ($token_usage)，触发压缩"
    curl -X POST http://127.0.0.1:8081/api/compact \
      -H "Content-Type: application/json" \
      -d "{\"token_usage\": $token_usage}"
  fi
else
  echo "压缩代理未运行，尝试启动..."
  sessions_spawn(
    runtime: "subagent",
    task: "启动上下文压缩代理",
    label: "context-compactor",
    model: "deepseek-chat"
  )
fi
```

## 与记忆技能集成

### 1. 集成 memory-management
```bash
# 压缩代理可以读取记忆管理技能的输出
sessions_send(
  sessionKey: "context-compactor",
  message: "从memory-management技能获取记忆数据，进行智能压缩"
)
```

### 2. 集成 agent-memory-store
```bash
# 将压缩结果存储到共享记忆
sessions_send(
  sessionKey: "context-compactor",
  message: "将压缩总结存储到agent-memory-store，供其他代理使用"
)
```

## 监控和告警

### 1. 创建监控面板
```bash
# 创建监控脚本
cat > monitor_compactor.sh << 'EOF'
#!/bin/bash
echo "=== 压缩代理监控面板 ==="
echo "时间: $(date)"
echo ""

# 健康状态
echo "健康状态:"
curl -s http://127.0.0.1:8081/api/health | jq -r '.status'

echo ""
echo "统计信息:"
curl -s http://127.0.0.1:8081/api/stats | jq '{
  total_compactions: .history_stats.total_compactions,
  total_tokens_saved: .history_stats.total_tokens_saved,
  current_token_usage: .current_stats.current_token_usage,
  avg_compression_ratio: .history_stats.avg_compression_ratio
}'
EOF

chmod +x monitor_compactor.sh
```

### 2. 设置告警
```bash
# 创建告警脚本
cat > alert_compactor.sh << 'EOF'
#!/bin/bash
THRESHOLD=0.8
STATS=$(curl -s http://127.0.0.1:8081/api/stats)
TOKEN_USAGE=$(echo $STATS | jq '.current_stats.current_token_usage')

if (( $(echo "$TOKEN_USAGE > $THRESHOLD" | bc -l) )); then
  echo "⚠️  告警：token使用率过高 ($TOKEN_USAGE)"
  
  # 发送通知（可根据需要集成到iMessage、邮件等）
  imsg send --to +8613501662537 --text "OpenClaw压缩代理告警：token使用率${TOKEN_USAGE}超过阈值${THRESHOLD}"
fi
EOF

chmod +x alert_compactor.sh
```

## 性能优化建议

### 1. 调整压缩参数
```json
{
  "针对长对话": {
    "hot_threshold": 20,
    "warm_threshold": 100,
    "cold_threshold": 500,
    "token_threshold": 0.75
  },
  "针对短对话": {
    "hot_threshold": 5,
    "warm_threshold": 25,
    "cold_threshold": 50,
    "token_threshold": 0.8
  }
}
```

### 2. 缓存优化
```bash
# 启用缓存
curl -X POST http://127.0.0.1:8081/api/config \
  -d '{"enable_cache": true, "cache_size": 1000}'
```

### 3. 并行处理
```bash
# 启用并行压缩
curl -X POST http://127.0.0.1:8081/api/config \
  -d '{"parallel_processing": true, "max_workers": 4}'
```

## 故障恢复

### 1. 代理重启
```bash
# 检查并重启代理
if ! curl -s http://127.0.0.1:8081/api/health > /dev/null; then
  echo "压缩代理异常，尝试重启..."
  pkill -f "python3 compactor.py"
  cd ~/.agents/skills/context-compactor
  ./start.sh
fi
```

### 2. 数据恢复
```bash
# 备份和恢复数据库
cp context_compactor.db context_compactor.db.backup.$(date +%Y%m%d)
sqlite3 context_compactor.db ".backup recovery.db"
```

## 扩展开发

### 1. 添加Web界面
```bash
# 创建简单的Web界面
cat > web_interface.py << 'EOF'
from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

@app.route('/')
def dashboard():
    stats = requests.get('http://127.0.0.1:8081/api/stats').json()
    return render_template('dashboard.html', stats=stats)

if __name__ == '__main__':
    app.run(port=8082)
EOF
```

### 2. 集成机器学习
```python
# 使用机器学习优化压缩算法
from sklearn.feature_extraction.text import TfidfVectorizer

class MLCompressor:
    """机器学习压缩器"""
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def train(self, messages):
        """训练模型"""
        texts = [msg['content'] for msg in messages]
        self.vectorizer.fit(texts)
    
    def compress(self, messages):
        """智能压缩"""
        # 使用TF-IDF识别重要内容
        pass
```

## 最佳实践

### 1. 定期维护
```bash
# 每周清理旧数据
0 2 * * 0 sqlite3 context_compactor.db "DELETE FROM compaction_history WHERE timestamp < datetime('now', '-90 days')"

# 每月优化数据库
0 3 1 * * sqlite3 context_compactor.db "VACUUM"
```

### 2. 监控日志
```bash
# 设置日志轮转
cat > /etc/logrotate.d/context-compactor << 'EOF'
/Users/shantian/.agents/skills/context-compactor/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 shantian staff
}
EOF
```

### 3. 安全配置
```bash
# 设置API密钥
export COMPACTOR_API_KEY="your-secret-key"

# 更新配置启用认证
curl -X POST http://127.0.0.1:8081/api/config \
  -H "X-API-Key: $COMPACTOR_API_KEY" \
  -d '{"require_auth": true}'
```

## 支持与反馈

### 问题报告
1. 检查日志：`tail -f logs/compactor.log`
2. 查看统计：`curl http://127.0.0.1:8081/api/stats`
3. 测试API：`curl http://127.0.0.1:8081/api/health`

### 性能问题
1. 调整压缩阈值
2. 优化数据库索引
3. 增加缓存大小
4. 启用并行处理

### 功能请求
1. 新的压缩算法
2. 额外的触发条件
3. 集成其他系统
4. 监控和告警功能