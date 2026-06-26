---
name: skill-install-manager
version: 1.1.0
description: 安全技能安装管理器 - 按照用户要求，所有技能安装前必须通过Skill vetter检测，如果发现需要修改配置的直接拒绝并上报，所有指令以用户为准。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["clawhub"] },
        "scripts": { "safe-install": "scripts/safe-install.sh" }
      },
  }
---

# 安全技能安装管理器 🔒

## 安装流程规范（更新版）

### 核心规则
1. **安全检测强制**：所有技能安装前必须通过Skill Vetter检测
2. **配置修改禁止**：如果发现需要修改配置，直接拒绝并上报
3. **用户指令最高**：所有操作以用户的具体指令为准

### 简化流程
```
1. 找到技能（通过任何来源：Clawhub、GitHub、其他）
   ↓
2. 使用Skill Vetter进行安全检测（强制）
   ↓
3. 检查是否需要配置修改
   ↓
4. 安装技能（仅当安全检测通过且无需配置修改）
```

### 详细步骤

#### 步骤1：找到技能
- 可以通过任何来源寻找技能（Clawhub、GitHub、直接提供等）
- 不需要特定的搜索顺序

#### 步骤2：使用Skill Vetter进行安全检测（强制）
- 对技能进行全面的安全检测
- 按照skill-vetter技能的要求生成安全报告
- 只有检测通过（✅ SAFE TO INSTALL）才能继续

#### 步骤3：检查配置修改
- 检查技能安装是否需要修改任何系统配置
- 如果发现需要修改配置，立即停止并上报

#### 步骤4：安装技能
- 使用适当的命令安装技能
- 不修改任何系统配置
- 所有操作以用户指令为准

## 使用示例

```bash
# 搜索"天气"相关技能
# 1. 先通过Composio搜索
curl -X POST "$COMPOSIO_BASE/tools/execute/COMPOSIO_SEARCH_TOOLS" \
  -H "x-api-key: $COMPOSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "queries": [{"use_case": "weather forecast skill for AI agent"}],
      "session": {"generate_id": true}
    }
  }'

# 2. 如果未找到，通过Clawhub搜索
clawhub search "weather"

# 3. 使用Skill Vetter检测
# 按照skill-vetter技能的要求进行安全检测

# 4. 安装（如果安全检测通过）
clawhub install weather-skill
```

## 安全规则

1. **绝不修改配置**：如果安装过程需要修改任何配置文件，立即停止并上报
2. **用户指令优先**：所有操作必须严格遵循用户的具体指令
3. **安全第一**：没有通过安全检测的技能绝不安装
4. **流程不可跳过**：必须按照1-4的顺序执行，不能跳过任何步骤

## 上报格式

当需要拒绝配置修改时，使用以下格式上报：

```
⚠️ 配置修改请求被拒绝
────────────────────────────
技能名称: [技能名称]
需要修改的配置: [配置项]
原因: 用户要求不修改任何配置
建议: [建议用户手动检查或提供具体指令]
────────────────────────────
已停止安装流程，等待用户进一步指示。
```

## 注意事项

- 确保Composio API密钥已正确设置
- 确保clawhub CLI已安装并可用
- 确保skill-vetter技能已安装并可用
- 所有搜索和安装操作都要记录日志