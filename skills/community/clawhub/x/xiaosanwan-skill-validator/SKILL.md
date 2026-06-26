---
name: xiaosanwan-skill-validator
description: 小三万技能验证工具，自动测试新安装 Skill 的功能完整性、边界情况、潜在问题，并提供完善建议。触发词：验证skill、测试新技能、skill能用吗、检查skill功能。
version: 1.1.0
metadata:
  openclaw:
    emoji: "🧪"
    category: "utility"
    version: "1.0.0"
    author: "小帽"
---

# 🧪 Skill 功能验证工具

**一句话描述**：验证新安装 Skill 的功能是否正常，发现潜在问题，提供完善建议。

---

## 🎯 设计思路

### 验证方法论

| 方法 | 说明 | 适用场景 |
|------|------|---------|
| **举例法** | 提供正常输入，验证功能正确性 | 基础功能验证 |
| **反证法** | 提供错误/边界输入，验证容错能力 | 异常处理验证 |
| **破解法** | 提供极端/恶意输入，测试稳定性 | 安全性验证 |
| **对比法** | 与预期输出对比，评估准确性 | 质量评估 |

### 验证流程

```
┌─────────────────┐
│  读取 SKILL.md  │ ← 获取功能描述、依赖
└────────┬────────┘
         ▼
┌─────────────────┐
│  检查依赖项     │ ← bins、env、files
└────────┬────────┘
         ▼
┌─────────────────┐
│  举例法验证     │ ← 正常场景测试
└────────┬────────┘
         ▼
┌─────────────────┐
│  反证法验证     │ ← 边界/异常测试
└────────┬────────┘
         ▼
┌─────────────────┐
│  破解法验证     │ ← 压力/安全测试
└────────┬────────┘
         ▼
┌─────────────────┐
│  生成验证报告   │ ← 结果 + 建议
└─────────────────┘
```

---

## 📋 验证清单

### 1️⃣ 基础验证（举例法）

| 检查项 | 说明 | 通过标准 |
|--------|------|---------|
| 文件完整性 | SKILL.md、scripts 存在 | 文件存在 |
| 依赖可用 | bins/env 满足 | 依赖可获取 |
| 基本功能 | 核心功能正常 | 输出符合预期 |
| 文档清晰 | 用法说明完整 | 用户可理解 |

### 2️⃣ 异常验证（反证法）

| 检查项 | 说明 | 通过标准 |
|--------|------|---------|
| 空输入 | 无参数调用 | 不崩溃，有提示 |
| 错误输入 | 非法参数 | 有错误提示 |
| 边界值 | 极端值输入 | 正确处理 |
| 缺失依赖 | 未满足依赖 | 有明确提示 |

### 3️⃣ 安全验证（破解法）

| 检查项 | 说明 | 通过标准 |
|--------|------|---------|
| 注入测试 | 特殊字符输入 | 无安全漏洞 |
| 权限检查 | 敏感操作权限 | 正确拒绝 |
| 资源限制 | 大量输入 | 不耗尽资源 |
| 并发测试 | 多次调用 | 无竞态条件 |

### 4️⃣ 质量验证（对比法）

| 检查项 | 说明 | 通过标准 |
|--------|------|---------|
| 输出格式 | 结果格式一致 | 符合预期格式 |
| 性能表现 | 响应时间合理 | < 预期时间 |
| 准确性 | 结果正确率 | > 90% |

---

## 💻 使用方法

### 命令行
```bash
# 验证指定 Skill（功能 + 安全 + UX）
bash ~/.openclaw/workspace/skills/skill-validator/scripts/validate.sh <skill-name>

# UX 用户体验专项验证
bash ~/.openclaw/workspace/skills/skill-validator/scripts/validate-ux.sh <skill-name>

# 验证最近安装的 Skill
bash ~/.openclaw/workspace/skills/skill-validator/scripts/validate-recent.sh

# 验证所有 Skill
bash ~/.openclaw/workspace/skills/skill-validator/scripts/validate-all.sh
```

### 对话触发
```
用户：验证一下我新安装的 email 技能
AI：让我帮你验证 openclaw-email 技能...
    [执行验证脚本]
    
    ✅ 基础验证通过
      - SKILL.md 存在
      - Python3 可用
    
    ⚠️ 发现问题
      - EMAIL_ADDRESS 未设置
      - EMAIL_PASSWORD 未设置
    
    📋 建议
      1. 设置环境变量: export EMAIL_ADDRESS="your@email.com"
      2. 生成应用密码并设置: export EMAIL_PASSWORD="xxx"
```

---

## 📊 验证报告示例

```
╔══════════════════════════════════════════════════════════╗
║           🧪 Skill 验证报告: openclaw-email            ║
╚══════════════════════════════════════════════════════════╝

📅 验证时间: 2026-03-19 20:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 基础验证 (4/4 通过)
  ✓ SKILL.md 文件存在
  ✓ scripts/ 目录存在  
  ✓ Python3 可用
  ✓ IMAP 连接正常

⚠️ 配置验证 (2/4 通过)
  ✓ EMAIL_ADDRESS 已设置
  ✓ EMAIL_IMAP_SERVER 已设置
  ✗ EMAIL_PASSWORD 未设置
  ✗ EMAIL_SMTP_SERVER 未设置

❌ 功能验证 (0/2 通过)
  ✗ 发送邮件失败（缺少密码）
  ✗ 接收邮件失败（缺少密码）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 完善建议

1. [必须] 设置邮箱应用密码
   export EMAIL_PASSWORD="your_app_password"

2. [建议] 设置 SMTP 服务器
   export EMAIL_SMTP_SERVER="smtp.gmail.com"

3. [优化] 添加错误重试机制

4. [文档] 补充常见错误码说明

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

总体评分: 60/100
状态: ⚠️ 部分可用（需配置）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 验证脚本结构

```
skill-validator/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── validate.sh             # 主验证脚本
│   ├── validate-recent.sh      # 验证最近安装
│   ├── validate-all.sh         # 验证所有 Skill
│   ├── test-basic.sh           # 基础验证
│   ├── test-edge.sh            # 边界验证
│   └── test-security.sh        # 安全验证
└── templates/
    ├── report.md               # 报告模板
    └── suggestions.md          # 建议模板
```

---

## 🎨 验证策略（按 Skill 类型）

### API 类 Skill
- 测试 API 连接
- 验证认证流程
- 检查错误处理
- 测试限流处理

### 工具类 Skill
- 测试核心命令
- 验证参数解析
- 检查输出格式
- 测试异常情况

### 内容生成类 Skill
- 测试生成质量
- 验证格式正确
- 检查多样性
- 评估准确性

### 自动化类 Skill
- 测试触发条件
- 验证执行流程
- 检查状态管理
- 测试并发情况

---

## 📝 验证结果状态

| 状态 | 图标 | 说明 |
|------|------|------|
| 通过 | ✅ | 功能正常 |
| 警告 | ⚠️ | 部分问题，可使用 |
| 失败 | ❌ | 无法使用，需修复 |
| 跳过 | ⊘ | 无法验证（如需外部服务） |

---

## 🔄 与其他 Skill 配合

| 配合技能 | 场景 |
|---------|------|
| `config-diagnose` | 验证后诊断配置问题 |
| `clawhub` | 验证新安装的 Skill |
| `healthcheck` | 系统健康 + Skill 验证 |

---

## 📈 评分标准

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100 | 🌟 优秀 | 功能完整，文档清晰 |
| 70-89 | ✅ 良好 | 核心功能正常，小问题 |
| 50-69 | ⚠️ 可用 | 需配置或有改进空间 |
| 0-49 | ❌ 不可用 | 需修复或重写 |

---

## 🎨 用户体验验证（UX Testing）

### 验证维度

| 维度 | 检查项 | 通过标准 |
|------|--------|---------|
| **可视化** | 输出格式清晰 | 有颜色/表格/图标 |
| **时区** | 时间处理正确 | 使用 UTC 或明确时区 |
| **语言** | 多语言支持 | 无硬编码文本 |
| **交互** | 用户引导清晰 | 有提示和帮助 |
| **错误** | 错误信息友好 | 无技术术语 |

---

## 🌍 国际化验证

### 时区检查

```bash
# 检查是否正确处理时区
check_timezone() {
    local skill_path=$1
    
    echo "🌍 时区处理检查..."
    
    # 检查是否使用 TZ 环境变量
    if grep -rq "TZ=" "$skill_path"; then
        echo "✅ 使用 TZ 环境变量"
    fi
    
    # 检查是否使用 UTC
    if grep -rq "UTC\|utc\|ISO 8601" "$skill_path"; then
        echo "✅ 使用 UTC 或 ISO 8601 格式"
    fi
    
    # 检查是否硬编码时区
    if grep -rqE "CST|PST|EST|GMT\+[0-9]" "$skill_path" 2>/dev/null; then
        echo "⚠️ 发现硬编码时区，建议使用用户本地时区"
    fi
    
    # 检查时间格式化
    if grep -rq "date.*format\|strftime\|moment\|dayjs" "$skill_path"; then
        echo "✅ 使用时间格式化库"
    fi
}
```

### 多语言检查

```bash
# 检查国际化支持
check_i18n() {
    local skill_path=$1
    
    echo "🗣️ 多语言支持检查..."
    
    # 检查是否有语言配置
    if [ -f "$skill_path/locales" ] || [ -d "$skill_path/i18n" ]; then
        echo "✅ 包含语言资源目录"
    fi
    
    # 检查硬编码文本
    local hardcoded=$(grep -rE "(错误|成功|失败|提示|Error|Success|Failed)" "$skill_path"/*.md 2>/dev/null | wc -l)
    if [ $hardcoded -gt 5 ]; then
        echo "⚠️ 发现 $hardcoded 处硬编码文本"
        echo "   建议：使用 i18n 函数或语言文件"
    fi
    
    # 检查字符编码
    if grep -rq "UTF-8\|utf8" "$skill_path"; then
        echo "✅ 声明 UTF-8 编码"
    fi
}
```

---

## 🎯 可视化验证

### 输出格式检查

```bash
# 检查输出可读性
check_visualization() {
    local skill_path=$1
    
    echo "🎨 可视化检查..."
    
    local scripts="$skill_path/scripts"
    local score=0
    
    # 检查颜色输出
    if grep -rq "\\033\[" "$scripts" 2>/dev/null; then
        echo "✅ 使用颜色输出"
        ((score+=20))
    else
        echo "⚠️ 无颜色输出"
    fi
    
    # 检查表格格式
    if grep -rqE "\|.*\||printf.*%|column" "$scripts" 2>/dev/null; then
        echo "✅ 使用表格格式"
        ((score+=20))
    fi
    
    # 检查图标/Emoji
    if grep -rqE "✅|❌|⚠️|🔴|🟢|📋|🔍" "$scripts" 2>/dev/null; then
        echo "✅ 使用图标/Emoji"
        ((score+=20))
    fi
    
    # 检查进度指示
    if grep -rq "spinner\|progress\|loading" "$scripts" 2>/dev/null; then
        echo "✅ 包含进度指示"
        ((score+=20))
    fi
    
    # 检查分隔线
    if grep -rqE "^[-=]{10,}|━|─" "$scripts" 2>/dev/null; then
        echo "✅ 使用分隔线"
        ((score+=20))
    fi
    
    echo ""
    echo "可视化评分: $score/100"
}
```

---

## 💡 最佳实践建议生成

### 建议规则引擎

```bash
# 根据验证结果生成建议
generate_best_practices() {
    local skill_path=$1
    local results=$2
    
    echo "💡 最佳实践建议"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 时区建议
    echo ""
    echo "【时区处理】"
    if grep -rq "date" "$skill_path" 2>/dev/null; then
        echo "  ✅ 建议：所有时间使用 ISO 8601 格式 (YYYY-MM-DDTHH:mm:ssZ)"
        echo "  ✅ 建议：显示时转换为用户本地时区"
        echo "  ✅ 示例：date -u +%Y-%m-%dT%H:%M:%SZ"
    fi
    
    # 多语言建议
    echo ""
    echo "【国际化】"
    echo "  ✅ 建议：将文本提取到语言文件"
    echo "  ✅ 建议：支持环境变量 LANG 或 LOCALE"
    echo "  ✅ 示例："
    echo "     # en_US.json"
    echo '     { "error": "Configuration not found" }'
    echo "     # zh_CN.json"
    echo '     { "error": "配置未找到" }'
    
    # 用户体验建议
    echo ""
    echo "【用户体验】"
    echo "  ✅ 建议：提供 --help 参数"
    echo "  ✅ 建议：错误信息包含解决方法"
    echo "  ✅ 建议：长时间操作显示进度"
    echo "  ✅ 建议：输出使用颜色区分状态"
    
    # 安全建议
    echo ""
    echo "【安全最佳实践】"
    echo "  ✅ 建议：敏感信息使用环境变量"
    echo "  ✅ 建议：不记录密码/token 到日志"
    echo "  ✅ 建议：输入验证和过滤"
    echo "  ✅ 建议：使用 timeout 限制外部调用"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}
```

---

## 📊 UX 验证报告示例

```
╔══════════════════════════════════════════════════════════╗
║           🎨 UX 验证报告: config-diagnose               ║
╚══════════════════════════════════════════════════════════╝

📅 验证时间: 2026-03-19 20:50

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 可视化 (80/100)
  ✅ 使用颜色输出
  ✅ 使用表格格式
  ✅ 使用图标/Emoji
  ✅ 使用分隔线
  ⚠️ 无进度指示

🌍 时区处理 (60/100)
  ✅ 使用 UTC 时间
  ⚠️ 发现硬编码时区 "CST"
  建议：改用 TZ 环境变量

🗣️ 多语言 (40/100)
  ⚠️ 发现 15 处硬编码中文
  ✅ 声明 UTF-8 编码
  建议：添加英文支持

🎯 用户引导 (70/100)
  ✅ 有使用帮助
  ✅ 错误信息清晰
  ⚠️ 缺少示例输出

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 UX 综合评分: 62/100

💡 改进建议
1. [高优先] 添加英文语言支持
2. [中优先] 修复时区硬编码问题
3. [低优先] 添加进度指示器

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 👤 作者

小帽 (OpenClaw)

## 📅 创建时间

2026-03-19

## 📜 许可证

MIT
