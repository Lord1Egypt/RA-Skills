# OpenClaw -> Star-Office-UI 状态同步配置总结

## 📋 配置概述

已成功配置 OpenClaw 与 Star-Office-UI 的自动状态同步，支持 6 种状态的实时切换。

## ✅ 已完成的配置

### 1. 创建状态同步脚本

**文件**：`/usr/local/bin/star-office-state`

**功能**：
- 封装 Star-Office-UI 的 `set_state.py` 脚本
- 提供简洁的命令行接口
- 自动记录状态变更日志

**用法**：
```bash
star-office-state <state> [detail]
```

**示例**：
```bash
star-office-state writing "正在帮你整理文档"
star-office-state idle "任务完成，待命中"
star-office-state error "发现问题，正在排查"
```

### 2. 修改 SOUL.md

**文件**：`/root/.openclaw/workspace/SOUL.md`

**修改内容**：
- 新增"Star Office UI 状态同步"章节
- 定义了 6 种状态的切换规则
- 提供了使用场景说明

**状态映射**：
- **idle** (待命) → 休息区 💤
- **writing** (写作) → 办公桌 💻
- **researching** (调研) → 书架区 📚
- **executing** (执行) → 服务器区 🖥️
- **syncing** (同步) → 同步区 🔄
- **error** (错误) → Bug 区 🐛

### 3. 状态同步规则

**任务开始前**：
```bash
star-office-state writing "正在帮你整理文档"
```

**任务完成后**：
```bash
star-office-state idle "任务完成，待命中"
```

**遇到错误时**：
```bash
star-office-state error "发现问题，正在排查"
```

## 🧪 验证测试

已验证以下状态都能正常切换：

| 状态 | 测试结果 | 说明 |
|------|---------|------|
| idle | ✅ 成功 | 待命状态 |
| writing | ✅ 成功 | 写作状态 |
| researching | ✅ 成功 | 调研状态 |
| executing | ✅ 成功 | 执行状态 |
| syncing | ✅ 成功 | 同步状态 |
| error | ✅ 成功 | 错误状态 |

## 📁 修改的文件清单

### 新增文件

1. **`/usr/local/bin/star-office-state`**
   - 状态同步包装脚本
   - 权限：755 (可执行)

### 修改文件

1. **`/root/.openclaw/workspace/SOUL.md`**
   - 新增"Star Office UI 状态同步"章节
   - 添加了状态切换规则和使用说明

### 依赖的现有文件

1. **`/root/Star-Office-UI/set_state.py`**
   - Star-Office-UI 的状态设置脚本
   - 无需修改

2. **`/root/Star-Office-UI/state.json`**
   - 状态存储文件
   - 自动更新

## 🔧 环境变量

无需额外配置环境变量，所有路径都已硬编码在脚本中。

## 🌐 访问地址

**像素办公室看板**：http://115.190.250.10:19000

## 📝 使用示例

### 示例 1：开始任务

当 OpenClaw 开始执行任务时，会自动调用：
```bash
star-office-state writing "正在帮你整理产业日报"
```

### 示例 2：任务完成

任务完成后，会自动调用：
```bash
star-office-state idle "产业日报已生成完成"
```

### 示例 3：遇到错误

遇到错误时，会自动调用：
```bash
star-office-state error "搜索 API 调用失败，正在重试"
```

## 🎯 工作原理

1. **OpenClaw 执行任务** → 根据 SOUL.md 的指令调用 `star-office-state`
2. **更新 state.json** → `star-office-state` 调用 `set_state.py` 更新状态文件
3. **Star-Office-UI 读取** → 前端定期读取 `state.json` 并更新像素角色位置
4. **用户查看** → 访问 http://115.190.250.10:19000 查看实时状态

## ⚙️ 高级配置（可选）

如果需要配置远程办公室同步，可以：

1. **配置 join key**：
   ```bash
   export JOIN_KEY="ocj_example_team_01"
   export AGENT_NAME="OpenClaw Agent"
   ```

2. **运行推送服务**：
   ```bash
   cd /root/Star-Office-UI
   python3 office-agent-push.py
   ```

## 📌 注意事项

1. **状态更新频率**：每次状态变更都会立即更新 `state.json`
2. **状态持久化**：状态会保存在 `/root/Star-Office-UI/state.json`
3. **日志记录**：所有状态变更都会记录到系统日志（`logger`）
4. **访问权限**：确保 Star-Office-UI 服务正在运行

## ✅ 配置验证

运行以下命令验证配置：

```bash
# 测试状态切换
star-office-state writing "测试状态同步"

# 查看当前状态
cat /root/Star-Office-UI/state.json

# 查看系统日志
journalctl -t openclaw-state -n 10
```

## 🎉 完成！

OpenClaw 现在会自动同步状态到 Star-Office-UI，你可以在像素办公室看板中实时看到 OpenClaw 的工作状态！
