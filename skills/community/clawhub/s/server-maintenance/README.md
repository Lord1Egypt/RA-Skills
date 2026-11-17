# Server Maintenance Skill

自动化服务器维护工具，支持磁盘检查、缓存清理、资源优化。

## 快速开始

### 检查单个服务器
```bash
bash ~/.openclaw/skills/server-maintenance/check.sh localhost 硅谷
bash ~/.openclaw/skills/server-maintenance/check.sh 43.163.225.27 中央
```

### 清理单个服务器
```bash
bash ~/.openclaw/skills/server-maintenance/cleanup.sh localhost 硅谷
bash ~/.openclaw/skills/server-maintenance/cleanup.sh 43.163.225.27 中央
```

### 批量维护所有服务器
```bash
bash ~/.openclaw/skills/server-maintenance/maintain-all.sh
```

## 实战案例

2026-03-03 首次使用，清理三台服务器：

| 服务器 | 清理前 | 清理后 | 释放空间 |
|--------|--------|--------|----------|
| 硅谷   | 79%    | 69%    | 4.7GB    |
| 中央   | 88%    | 78%    | 5.0GB    |
| 东京   | 71%    | 63%    | 4.0GB    |

**总计释放：13.7GB**

## 记忆蒸馏

这个 Skill 是从实际维护经验中蒸馏出来的：

1. **原始上下文**：17K tokens（完整对话历史）
2. **蒸馏后**：~2K tokens（核心步骤 + 脚本）
3. **Token 节省**：88%

### 蒸馏过程
1. 提取关键步骤（检查 → 清理 → 验证）
2. 固化为可执行脚本
3. 添加配置文件支持多服务器
4. 文档化使用方法

### 效果
- 未来维护不需要重新思考流程
- 直接调用脚本，节省 token
- 可复用、可扩展、可定时

## 配置

编辑 `servers.json` 添加更多服务器：
```json
{
  "name": "新服务器",
  "host": "1.2.3.4",
  "type": "ssh",
  "description": "描述"
}
```

## 定时任务

在 OpenClaw 中设置每周自动维护：
```bash
openclaw cron add "0 2 * * 0" "bash ~/.openclaw/skills/server-maintenance/maintain-all.sh"
```

## 版本历史

- v1.0.0 (2026-03-03): 初始版本，支持磁盘检查和缓存清理
