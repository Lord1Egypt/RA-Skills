# 安全技能安装管理器

## 概述

这是一个严格按照用户要求实现的技能安装管理器，确保所有技能安装都遵循安全流程：

1. **必须通过Skill Vetter检测** - 所有技能安装前必须进行全面的安全检测
2. **配置修改禁止** - 如果发现需要修改配置，直接拒绝并上报
3. **用户指令最高** - 所有操作以用户的具体指令为准
4. **灵活的技能来源** - 可以从任何来源获取技能（Clawhub、GitHub、本地等）

## 安装

```bash
# 确保clawhub已安装
npm i -g clawhub

# 设置Composio API密钥（可选）
export COMPOSIO_API_KEY="your_api_key_here"
```

## 使用方法

### 通过脚本安装

```bash
# 运行安全安装脚本
cd ~/.openclaw/workspace/skills/skill-install-manager-1.0.0
./scripts/safe-install.sh "技能名称"
```

### 手动流程

如果你想要手动控制每个步骤：

1. **搜索技能**:
   ```bash
   # 先尝试Composio搜索
   # 需要设置COMPOSIO_API_KEY环境变量
   
   # 如果未找到，使用Clawhub搜索
   clawhub search "技能关键词"
   ```

2. **安全检测**:
   ```bash
   # 使用skill-vetter技能进行安全检测
   # 确保skill-vetter技能已安装
   ```

3. **安装技能**:
   ```bash
   # 只有安全检测通过后才能安装
   clawhub install 技能名称
   ```

## 安全规则

### 必须遵守的规则

1. **安全检测强制**：所有技能必须通过skill-vetter检测
2. **配置修改禁止**：如果安装需要修改配置，直接拒绝并上报
3. **用户指令最高**：所有操作必须严格遵循用户的具体要求
4. **灵活来源**：可以从任何可信来源获取技能

### 上报格式

当需要拒绝配置修改时，使用以下格式：

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

## 示例

### 安装天气技能

```bash
# 完整流程示例
./scripts/safe-install.sh "weather"

# 输出示例:
# [INFO] 开始安全安装流程: weather
# [INFO] 检查依赖...
# [SUCCESS] 依赖检查完成
# [INFO] 步骤1: 通过Composio搜索技能 'weather'...
# [WARNING] 跳过Composio搜索 (API密钥未设置)
# [INFO] 未在Composio中找到，尝试Clawhub搜索
# [INFO] 步骤2: 通过Clawhub搜索技能 'weather'...
# [INFO] 执行: clawhub search "weather"
# 模拟clawhub搜索结果:
# 1. weather-skill - 天气技能 v1.0.0
# 2. calendar-skill - 日历技能 v2.1.0
# 3. notes-skill - 笔记技能 v1.5.0
# 请输入要安装的技能编号 (或输入'skip'跳过): 1
# [SUCCESS] 选择技能: weather-skill
# [INFO] 步骤3: 使用Skill Vetter检测技能 'weather-skill'...
# [SUCCESS] 安全检测通过，准备安装
# [INFO] 步骤4: 安装技能 'weather-skill'...
# [INFO] 检查是否需要配置修改...
# [SUCCESS] 未发现需要修改的配置
# [INFO] 执行: clawhub install weather-skill
# [SUCCESS] 技能 'weather-skill' 安装成功！
# [SUCCESS] 安装流程完成
```

## 依赖

- `clawhub` CLI (必须)
- `COMPOSIO_API_KEY` 环境变量 (可选，用于Composio搜索)
- `skill-vetter` 技能 (必须，用于安全检测)

## 故障排除

### 1. clawhub未安装
```bash
错误: clawhub CLI未安装
解决: npm i -g clawhub
```

### 2. Composio API密钥未设置
```bash
警告: COMPOSIO_API_KEY未设置
解决: export COMPOSIO_API_KEY='your_api_key'
注意: 这只是警告，安装流程会继续使用Clawhub搜索
```

### 3. skill-vetter技能未安装
```bash
错误: skill-vetter技能未安装
解决: 先安装skill-vetter技能
```

### 4. 需要配置修改
```bash
错误: 发现需要修改配置
解决: 立即停止安装，上报给用户
```

## 开发说明

这个技能管理器是为了满足特定的安全要求而创建的：

1. **不可修改性**：脚本不会修改任何系统配置
2. **可审计性**：所有步骤都有明确的日志记录
3. **安全性**：强制性的安全检测流程
4. **用户控制**：所有决策点都需要用户确认

如果你需要修改这个技能，请确保不违反上述核心原则。