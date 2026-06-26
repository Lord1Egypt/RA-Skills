# 工作流引擎集成指南

## 任务信息
- **任务 ID**: JJC-20260323-003
- **状态**: ✅ 已完成
- **集成方式**: Internal Hooks（非侵入式）

---

## 📦 已创建文件

### 核心文件
1. **`/root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts/openclaw_hook.py`**
   - HTTP Hook 服务器
   - 监听 `POST /hook` 端点
   - 接收 OpenClaw inbound 消息
   - 调用工作流引擎处理
   - 返回响应或放行给 AI

2. **`/root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts/update_openclaw_config.py`**
   - 自动更新 OpenClaw 配置文件
   - 添加 hooks 配置段
   - 创建备份

3. **`/root/.openclaw/workspace-zhongshu/skills/wol-wakeup/openclaw-hook.service`**
   - systemd 服务配置
   - 自动启动 Hook 服务
   - 日志轮转

### 已有文件（工作流引擎）
- `workflow_engine.py` - 工作流引擎核心
- `state_manager.py` - 状态管理器
- `wol_workflow.py` - WoL 工作流定义
- `message_handler.py` - 消息处理器
- `wol_manager.py` - 设备管理器

---

## 🚀 快速开始

### 步骤 1：启动 Hook 服务

**临时启动（测试用）:**
```bash
cd /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts
python3 openclaw_hook.py --port 8765 --token 6fb57eb806f64da4e70b1b7a8c41f6b97a4788dc9f6b15430cdfedc0b61c75b1
```

**后台启动:**
```bash
cd /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts
nohup python3 openclaw_hook.py --port 8765 --token 6fb57eb806f64da4e70b1b7a8c41f6b97a4788dc9f6b15430cdfedc0b61c75b1 > /tmp/hook_server.log 2>&1 &
```

**systemd 服务启动（推荐生产环境）:**
```bash
# 创建日志目录
sudo mkdir -p /var/log/openclaw

# 安装服务
sudo cp /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/openclaw-hook.service /etc/systemd/system/

# 重载 systemd 并启动
sudo systemctl daemon-reload
sudo systemctl enable openclaw-hook
sudo systemctl start openclaw-hook

# 查看状态
sudo systemctl status openclaw-hook
```

### 步骤 2：更新 OpenClaw 配置

**自动更新（推荐）:**
```bash
cd /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts
python3 update_openclaw_config.py
```

**手动更新:**
编辑 `/root/.openclaw/openclaw.json`，添加:
```json
{
  "hooks": {
    "enabled": true,
    "token": "6fb57eb806f64da4e70b1b7a8c41f6b97a4788dc9f6b15430cdfedc0b61c75b1",
    "internal": {
      "enabled": true,
      "endpoint": "http://127.0.0.1:8765/hook"
    }
  }
}
```

### 步骤 3：重启 OpenClaw Gateway
```bash
openclaw gateway restart
```

### 步骤 4：测试

**健康检查:**
```bash
curl http://127.0.0.1:8765/health
# 预期输出：{"status": "healthy", "active_sessions": 0}
```

**测试 Hook 接口:**
```bash
# 测试工作流消息（应返回 handled: true）
curl -X POST http://127.0.0.1:8765/hook \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 6fb57eb806f64da4e70b1b7a8c41f6b97a4788dc9f6b15430cdfedc0b61c75b1" \
  -d '{"event":"inbound_message","channel":"openclaw-weixin","from":"test@im.wechat","text":"帮我开机"}'

# 测试非工作流消息（应返回 handled: false）
curl -X POST http://127.0.0.1:8765/hook \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 6fb57eb806f64da4e70b1b7a8c41f6b97a4788dc9f6b15430cdfedc0b61c75b1" \
  -d '{"event":"inbound_message","channel":"openclaw-weixin","from":"test@im.wechat","text":"你好"}'
```

**微信测试:**
1. 发送 `帮我开机` → 应收到设备列表
2. 发送 `添加网络唤醒` → 应收到多轮对话提示
3. 发送 `你好` → 应由 AI 正常回复（非工作流）

---

## 📊 工作流程

### 消息处理流程
```
微信用户发送消息
    ↓
OpenClaw 微信插件接收
    ↓
Internal Hook 触发
    ↓
POST http://127.0.0.1:8765/hook
    ↓
工作流引擎匹配关键词
    ├─ 匹配成功 → 返回响应 (handled: true) → OpenClaw 直接发送回复
    └─ 匹配失败 → 返回空 (handled: false) → 消息流转给 AI 处理
```

### 支持的工作流命令

| 命令 | 动作 | 示例 |
|------|------|------|
| `帮我开机` / `电脑开机` | 列出设备 | 返回设备列表 |
| `开机 - 设备名` | 唤醒设备 | `开机 - 书房电脑` |
| `添加网络唤醒` | 启动添加工作流 | 多轮对话收集信息 |
| `列表` / `设备列表` | 查看设备 | 返回设备列表 |
| `删除 - 设备名` | 删除设备 | `删除 - 旧电脑` |
| `删除设备` | 启动删除工作流 | 多轮对话确认 |

### 多轮对话示例
```
用户：添加网络唤醒
助手：📝 第一步：请输入设备名称（如：书房电脑）

用户：书房电脑
助手：📝 第二步：请输入 MAC 地址
      格式：00:11:22:33:44:55

用户：00:11:22:33:44:55
助手：📝 第三步：请输入备注信息（可选）
      直接回车可跳过

用户：我的台式机
助手：✅ 设备添加成功！
      名称：书房电脑
      MAC: 00:11:22:33:44:55
      备注：我的台式机
      
      现在可以使用 '开机 - 书房电脑' 唤醒设备
```

---

## 🔧 配置说明

### Hook 服务配置

**命令行参数:**
- `--port`: 监听端口（默认：8765）
- `--token`: 认证 token（必需，与 OpenClaw 配置一致）
- `--generate-token`: 生成新 token

**环境变量:**
- `HOOK_TOKEN`: 从环境变量读取 token

### OpenClaw 配置

**hooks 字段说明:**
```json
{
  "hooks": {
    "enabled": true,           // 启用 hooks
    "token": "<安全 token>",    // 认证 token（建议 32+ 字符）
    "internal": {
      "enabled": true,         // 启用 internal hooks
      "endpoint": "http://..." // Hook 服务地址
    }
  }
}
```

**安全建议:**
1. 使用强随机 token（至少 32 字符）
2. Hook 服务仅监听 localhost（127.0.0.1）
3. 定期更新 token
4. 限制文件权限（`chmod 600 openclaw.json`）

---

## 📁 数据持久化

### 会话状态
- **路径**: `~/.openclaw/wol/workflows/sessions.json`
- **内容**: 活跃工作流会话（多轮对话状态）
- **格式**: JSON
- **超时**: 60 秒无活动自动清理

### 设备配置
- **路径**: `~/.openclaw/wol/devices.json`
- **内容**: 已保存的 WoL 设备
- **格式**: JSON
- **字段**: name, mac, note, id

---

## 🐛 故障排查

### Hook 服务未启动
```bash
# 检查进程
ps aux | grep openclaw_hook

# 查看日志
cat /tmp/hook_server.log

# 手动启动测试
python3 openclaw_hook.py --port 8765 --token <token>
```

### 消息未触发工作流
1. 检查 Hook 服务是否运行：`curl http://127.0.0.1:8765/health`
2. 检查 OpenClaw 配置：`cat ~/.openclaw/openclaw.json | grep -A 10 hooks`
3. 查看 OpenClaw 日志：`openclaw logs`
4. 测试 Hook 接口（见上方 curl 命令）

### Token 验证失败
- 确保 Hook 服务的 `--token` 与 OpenClaw 配置的 `hooks.token` 一致
- 检查 Authorization header 格式：`Bearer <token>`

### 会话状态丢失
- 检查状态文件权限：`ls -la ~/.openclaw/wol/workflows/`
- 确保磁盘空间充足
- 避免同时运行多个 Hook 服务实例

---

## 📈 监控与运维

### 健康检查端点
```bash
curl http://127.0.0.1:8765/health
# 返回：{"status": "healthy", "active_sessions": <数量>}
```

### 查看活跃会话
```bash
cd /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts
python3 wol_workflow.py list-sessions
```

### 清理超时会话
```bash
python3 wol_workflow.py check-timeouts
```

### 日志位置
- **Hook 服务**: `/tmp/hook_server.log` 或 `/var/log/openclaw/hook-server.log`
- **工作流状态**: `~/.openclaw/wol/workflows/sessions.json`

---

## 🔄 扩展开发

### 添加新工作流

1. **定义工作流** (`wol_workflow.py`):
```python
def create_my_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        workflow_type="my_workflow",
        name="我的工作流",
        steps=[...],
    )

def init_wol_workflows():
    engine.register_workflow(create_my_workflow())
```

2. **添加消息匹配** (`message_handler.py`):
```python
if text in ['触发关键词']:
    return 'start_my_workflow', {}
```

3. **重启 Hook 服务**

### 集成其他技能

工作流引擎是通用的，可用于任何多轮对话场景：
- 问卷调研
- 订单创建
- 预约登记
- 信息收集

只需定义新的 `WorkflowDefinition` 并注册到引擎。

---

## ✅ 验收标准

- [x] Hook 服务可启动并监听端口
- [x] OpenClaw 配置可更新
- [x] 工作流消息正确匹配并处理（handled: true）
- [x] 非工作流消息正确放行（handled: false）
- [x] 多轮对话状态保持正常
- [x] 会话超时自动清理
- [x] 设备持久化保存
- [x] 健康检查端点可用

---

## 📝 版本信息

- **集成日期**: 2026-03-23
- **OpenClaw 版本**: 2026.3.2
- **Python 版本**: 3.x
- **Hook 端口**: 8765

---

## 🆘 支持

遇到问题请查看：
1. 本集成指南
2. Hook 服务日志
3. OpenClaw 日志
4. 工作流引擎测试工具

**快速诊断命令:**
```bash
# 1. 检查 Hook 服务
curl http://127.0.0.1:8765/health

# 2. 检查 OpenClaw 配置
python3 update_openclaw_config.py --dry-run

# 3. 测试工作流
python3 message_handler.py "帮我开机" test_user

# 4. 查看活跃会话
python3 wol_workflow.py list-sessions
```
