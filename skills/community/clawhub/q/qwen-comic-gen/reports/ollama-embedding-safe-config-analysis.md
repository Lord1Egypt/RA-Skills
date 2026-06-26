# Ollama Embedding 向量模型安全配置方案分析报告

**分析时间：** 2026-03-12 15:00  
**分析执行者：** 阿福（OpenClaw 助手）  
**任务来源：** 用户早上询问 Ollama mxbai-embed-large 模型配置问题

---

## 1. 当前状态评估表

| 条件 | 状态 | 说明 |
|------|------|------|
| Ollama 安装 | ✅ | 版本 0.17.7（客户端） |
| mxbai-embed-large 下载 | ✅ | 669 MB，5 小时前下载完成 |
| Ollama 服务运行 | ⚠️ | 客户端可访问模型列表，但连接警告（可能间歇性） |
| OpenClaw 支持 Embedding | ✅ | 版本 2026.3.8，支持 `tools.embedding` 配置 |
| 配置方式 | `tools.embedding` | **关键：必须在 tools 下配置，不能在根级别** |

---

## 2. 问题根因分析

### 之前失败的原因

用户之前尝试在 `openclaw.json` **根级别**添加 `embedding` 字段：

```json
// ❌ 错误做法 - 会导致配置验证失败
{
  "embedding": {
    "provider": "ollama",
    "model": "mxbai-embed-large",
    "base_url": "http://127.0.0.1:11434/v1",
    "dimension": 1024
  }
}
```

### 正确的配置位置

根据 OpenClaw 2026.3.8 的 schema 定义，embedding 配置必须在 `tools.embedding` 下：

```typescript
// 来自 types.tools.d.ts
export type MemoryIndexConfig = {
  /** Embedding provider mode. */
  provider?: "openai" | "gemini" | "local" | "voyage" | "mistral" | "ollama";
  model?: string;
  remote?: {
    baseUrl?: string;
    apiKey?: SecretInput;
    // ...
  };
  // ...
};
```

---

## 3. 安全操作步骤（按顺序）

### 步骤 1：备份当前配置（已完成）
```powershell
# 已有备份：openclaw.json.bak (2026-03-12 09:45:37)
# 建议再创建一个新的备份
Copy-Item "C:\Users\Xiabi\.openclaw\openclaw.json" `
          "C:\Users\Xiabi\.openclaw\openclaw.json.before-embedding"
```

### 步骤 2：验证当前配置
```powershell
openclaw config validate
# 预期输出：Config valid: ~\.openclaw\openclaw.json
```

### 步骤 3：修改 openclaw.json（使用正确结构）

**方法 A：使用 openclaw config set 命令（推荐）**
```powershell
# 设置 embedding provider
openclaw config set tools.embedding.provider "ollama"

# 设置 embedding model
openclaw config set tools.embedding.model "mxbai-embed-large"

# 设置 remote baseUrl
openclaw config set tools.embedding.remote.baseUrl "http://127.0.0.1:11434/v1"

# 设置 remote apiKey
openclaw config set tools.embedding.remote.apiKey "ollama-local"
```

**方法 B：手动编辑 openclaw.json**

找到现有的 `tools` 段，修改为：
```json
{
  "tools": {
    "profile": "full",
    "embedding": {
      "provider": "ollama",
      "model": "mxbai-embed-large",
      "remote": {
        "baseUrl": "http://127.0.0.1:11434/v1",
        "apiKey": "ollama-local"
      }
    }
  }
}
```

### 步骤 4：验证新配置
```powershell
openclaw config validate
# 预期输出：Config valid: ~\.openclaw\openclaw.json
```

### 步骤 5：重启 Gateway（如果正在运行）
```powershell
# 检查 Gateway 状态
openclaw gateway status

# 如果正在运行，重启
openclaw gateway restart

# 或者停止后重新启动
openclaw gateway stop
openclaw gateway start
```

### 步骤 6：验证 Embedding 功能
```powershell
# 检查 Gateway 日志
openclaw logs

# 或测试 memory 索引功能
openclaw memory search --query "测试"
```

---

## 4. 验证方法

### 确认配置成功

1. **配置验证**
   ```powershell
   openclaw config validate
   # 输出：Config valid
   ```

2. **Gateway 状态检查**
   ```powershell
   openclaw gateway status
   # 输出：Listening: 127.0.0.1:18789
   #       RPC probe: ok
   ```

3. **检查配置内容**
   ```powershell
   Get-Content "C:\Users\Xiabi\.openclaw\openclaw.json" | ConvertFrom-Json | `
     Select-Object -ExpandProperty tools | `
     Select-Object -ExpandProperty embedding
   ```

### 测试 Embedding 功能

1. **测试 Memory 搜索**
   ```powershell
   openclaw memory search --query "测试查询"
   ```

2. **检查日志**
   ```powershell
   Get-Content "C:\Users\Xiabi\AppData\Local\Temp\openclaw\openclaw-2026-03-12.log" -Tail 50
   ```

3. **观察 Ollama 连接**
   ```powershell
   # 检查 Ollama 是否收到请求
   Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing | `
     ConvertFrom-Json | Select-Object -ExpandProperty models
   ```

---

## 5. 回滚方案

### 如果配置失败

**方案 A：恢复备份**
```powershell
# 恢复之前的备份
Copy-Item "C:\Users\Xiabi\.openclaw\openclaw.json.before-embedding" `
          "C:\Users\Xiabi\.openclaw\openclaw.json" -Force

# 或使用更早的备份
Copy-Item "C:\Users\Xiabi\.openclaw\openclaw.json.bak" `
          "C:\Users\Xiabi\.openclaw\openclaw.json" -Force
```

**方案 B：删除 embedding 配置**
```powershell
# 使用 openclaw config unset 删除配置
openclaw config unset tools.embedding
```

**方案 C：手动编辑恢复**
```powershell
# 打开配置文件
notepad "C:\Users\Xiabi\.openclaw\openclaw.json"

# 删除 tools.embedding 段，保留 tools.profile
```

### 如果 Gateway 无法启动

```powershell
# 1. 检查配置
openclaw config validate

# 2. 查看错误日志
Get-Content "C:\Users\Xiabi\AppData\Local\Temp\openclaw\openclaw-2026-03-12.log" -Tail 100

# 3. 强制重启
openclaw gateway stop --force
openclaw gateway start

# 4. 如果还不行，恢复备份后重启
Copy-Item "C:\Users\Xiabi\.openclaw\openclaw.json.bak" `
          "C:\Users\Xiabi\.openclaw\openclaw.json" -Force
openclaw gateway restart
```

---

## 6. 最终建议

### 推荐操作：**立即配置（使用正确结构）**

**理由：**
1. ✅ 所有必要条件已满足（Ollama 安装、模型下载、OpenClaw 支持）
2. ✅ 已知正确的配置方式（`tools.embedding` 而非根级别）
3. ✅ 有完整的备份和回滚方案
4. ✅ 配置验证工具可用（`openclaw config validate`）

### 风险评估：**低**

| 风险项 | 风险等级 | 缓解措施 |
|--------|----------|----------|
| 配置错误导致 Gateway 无法启动 | 低 | 使用 `openclaw config validate` 预先验证 |
| Ollama 连接失败 | 低 | 模型已下载，服务可访问 |
| Embedding 功能不工作 | 低 | 有完整的日志和调试工具 |
| 配置丢失 | 低 | 已有备份文件 |

### 关键注意事项

1. **配置位置**：必须在 `tools.embedding` 下，**不能在根级别**
2. **配置字段**：使用 `remote.baseUrl` 和 `remote.apiKey`，不是 `base_url`
3. **验证优先**：修改后先用 `openclaw config validate` 验证
4. **备份习惯**：修改前创建备份
5. **日志监控**：修改后检查 Gateway 日志

---

## 7. 配置示例（完整参考）

### 正确的 openclaw.json 结构（相关部分）

```json
{
  "meta": {
    "lastTouchedVersion": "2026.3.8",
    "lastTouchedAt": "2026-03-12T07:00:00.000Z"
  },
  "env": {
    "DASHSCOPE_API_KEY": "sk-xxx"
  },
  "models": {
    "mode": "merge",
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434/v1",
        "apiKey": "ollama-local",
        "api": "openai-completions",
        "models": [...]
      }
    }
  },
  "tools": {
    "profile": "full",
    "embedding": {
      "provider": "ollama",
      "model": "mxbai-embed-large",
      "remote": {
        "baseUrl": "http://127.0.0.1:11434/v1",
        "apiKey": "ollama-local"
      },
      "cache": {
        "enabled": true
      }
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local"
  }
}
```

---

## 8. 快速命令参考

```powershell
# 验证配置
openclaw config validate

# 设置 embedding 配置
openclaw config set tools.embedding.provider "ollama"
openclaw config set tools.embedding.model "mxbai-embed-large"
openclaw config set tools.embedding.remote.baseUrl "http://127.0.0.1:11434/v1"
openclaw config set tools.embedding.remote.apiKey "ollama-local"

# 删除 embedding 配置（回滚）
openclaw config unset tools.embedding

# 查看配置
openclaw config get tools.embedding

# Gateway 控制
openclaw gateway status
openclaw gateway restart
openclaw logs

# 测试功能
openclaw memory search --query "测试"
```

---

**报告生成完成** ✅  
**下一步：** 按步骤 3 执行配置，然后验证
