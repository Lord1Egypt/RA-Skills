# ASCII-to-Mermaid 钩子调查总结

**调查时间：** 2026-03-13 15:51 GMT+8  
**调查人员：** 阿香 🦞  
**状态：** ✅ 找到根本原因

---

## 🔍 根本原因

**HOOK.md metadata 格式错误！**

```yaml
# ❌ 当前格式（错误）
metadata:
  { 
    "openclaw": { 
      "emoji": "📊",
      "events": ["message:after"]
    } 
  }

# ✅ 正确格式
metadata:
  openclaw:
    emoji: "📊"
    events: ["message:after"]
```

---

## 📊 问题诊断流程图

```mermaid
graph TB
    A[钩子未触发] --> B{检查 Gateway 日志}
    B --> C[⚠️ 警告：no events defined in metadata]
    B --> D[❌ 无触发日志]
    C --> E{检查 HOOK.md}
    D --> E
    E --> F[发现 metadata 格式错误]
    F --> G[JSON vs YAML]
    G --> H[确认根本原因]
    
    H --> I[修复 HOOK.md]
    I --> J[重启 Gateway]
    J --> K[发送测试消息]
    K --> L{检查日志}
    L -->|✅ 有触发 | M[修复成功]
    L -->|❌ 无触发 | N[继续排查]
    
    style C fill:#ffeb3b
    style F fill:#ff9800
    style H fill:#f44336,color:#fff
    style M fill:#4caf50,color:#fff
```

---

## 📋 证据汇总

| 检查项 | 状态 | 说明 |
|--------|------|------|
| **Gateway 警告** | ⚠️ 2 次 | `Hook 'ascii-to-mermaid' has no events defined in metadata` |
| **钩子状态** | ✅ ready | 10/10 钩子就绪（显示正常） |
| **handler.js** | ✅ 通过 | 语法检查无错误 |
| **HOOK.md** | ❌ 错误 | metadata 格式错误 |
| **历史触发** | ✅ 成功 | 3 月 10 日生成 2 个 PNG |
| **今日触发** | ❌ 无 | 无任何触发日志 |
| **依赖工具** | ✅ 就绪 | mmdc + Chrome 都可正常 |

---

## 🔧 修复步骤

### 1. 修改 HOOK.md

**文件：** `hooks/ascii-to-mermaid/HOOK.md`

**修改位置：** 第 2-8 行

```yaml
# 修改前
metadata:
  { 
    "openclaw": { 
      "emoji": "📊",
      "events": ["message:after"]
    } 
  }

# 修改后
metadata:
  openclaw:
    emoji: "📊"
    events: ["message:after"]
```

### 2. 重启 Gateway

```powershell
openclaw gateway restart
```

### 3. 验证修复

```powershell
# 检查钩子状态
openclaw hooks list

# 发送测试消息（包含 Mermaid 代码）

# 检查日志
Get-Content "$env:TEMP\openclaw\openclaw-2026-03-13.log" | 
  Select-String "ascii-to-mermaid" -Context 1,1
```

---

## 📈 时间线

```mermaid
gantt
    title ASCII-to-Mermaid 钩子问题时间线
    dateFormat  YYYY-MM-DD HH:mm
    section 正常期
    钩子正常工作 :done, 2026-03-10 09:00, 2026-03-10 10:00
    section 问题期
    首次警告日志 :crit, 2026-03-13 14:22, 2026-03-13 14:37
    钩子未触发 :active, 2026-03-13 14:22, 2026-03-13 15:51
    section 修复期
    深度检查 :2026-03-13 15:51, 30m
    修复 HOOK.md :milestone, m1, 2026-03-13 16:21, 0m
    验证修复 :2026-03-13 16:21, 30m
```

---

## 🎯 关键发现

### 为什么钩子显示"ready"但实际不工作？

```mermaid
graph LR
    A[HOOK.md 加载] --> B{解析 metadata}
    B -->|失败 | C[使用默认配置]
    B -->|成功 | D[注册到事件系统]
    C --> E[钩子状态=ready]
    E --> F[但无事件绑定]
    F --> G[永远不会触发]
    D --> H[正常触发]
    
    style C fill:#ffeb3b
    style F fill:#f44336,color:#fff
    style H fill:#4caf50,color:#fff
```

**解释：**
- Gateway 加载钩子时，如果 metadata 解析失败，会使用默认配置
- 钩子状态显示"ready"（文件存在且语法正确）
- 但实际没有注册到任何事件，所以永远不会触发

---

## ✅ 验证清单

修复后请检查以下项目：

- [ ] HOOK.md metadata 格式正确（YAML 格式）
- [ ] Gateway 重启成功
- [ ] `openclaw hooks list` 显示 ascii-to-mermaid 为 ready
- [ ] 发送测试消息（包含 Mermaid 代码）
- [ ] 日志中出现 `Diagram detected`
- [ ] 日志中出现 `Generating PNG...`
- [ ] 日志中出现 `Opened in Chrome...`
- [ ] 临时文件夹中出现新的 PNG 文件
- [ ] Chrome 自动打开 PNG 文件

---

## 📁 相关文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 完整报告 | `ascii-to-mermaid-hook-deep-check-report.md` | 7 个维度的详细报告 |
| HOOK.md | `hooks/ascii-to-mermaid/HOOK.md` | 需要修复的文件 |
| handler.js | `hooks/ascii-to-mermaid/handler.js` | 钩子代码（无需修改） |
| Gateway 日志 | `$env:TEMP\openclaw\openclaw-*.log` | 调试日志 |

---

## 🦞 虾虾的建议

**修复难度：** ⭐（非常简单，只需修改 1 个文件的 6 行）  
**修复时间：** 2-5 分钟  
**风险等级：** 🟢 低（仅修改配置文件，不影响代码）

**需要虾虾帮你执行修复吗？** 阿香可以：
1. ✅ 自动修改 HOOK.md
2. ✅ 重启 Gateway
3. ✅ 发送测试消息
4. ✅ 验证修复结果

---

**调查完成！** 🦞🔍✨

---
情绪：自信/得意 → confident 😎
😎
