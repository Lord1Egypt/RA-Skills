---
name: skill-preflight-checker
description: 技能预检检查器。在安装任何技能前进行安全检查，验证作者声誉、检查恶意脚本、分析权限需求，防止安装恶意技能。
---

# Skill Preflight Checker - 技能预检检查器

## 核心功能

### 1. 🔍 作者声誉检查
- 检查技能作者在 npm/ClawHub 的声誉
- 查看下载量、星标数、用户评价
- 检查是否有其他可信技能

### 2. 📦 代码安全检查
- 读取 package.json 的 scripts 部分
- 检查是否有可疑的 postinstall 脚本
- 搜索网络调用（curl/wget）
- 搜索危险函数（eval/exec）

### 3. 🔐 权限分析
- 分析技能需要的文件访问权限
- 检查是否访问敏感目录（~/.ssh, ~/.env）
- 检查是否需要网络访问
- 检查是否需要提权

### 4. 🧪 隔离环境测试
- 在 Docker 容器中先安装测试
- 监控安装过程中创建/修改的文件
- 检查是否有异常行为

### 5. 📋 生成检查报告
- 生成详细的安全检查报告
- 标记红旗警告
- 给出安装建议（安全/谨慎/拒绝）

---

## 使用方式

### 安装前检查
```
用户：帮我检查这个技能是否安全
助手：运行预检检查流程，生成报告
```

### 批量检查
```
用户：检查我准备安装的 5 个技能
助手：逐个检查，汇总报告
```

---

## 预检清单

### Step 1：检查作者
```bash
# 查看作者信息
npm view package-name author

# 查看下载量
npm view package-name downloads

# 查看星标
npm view package-name stargazers_count
```

### Step 2：检查 scripts
```bash
# 读取 package.json
jq '.scripts' package.json

# 检查可疑脚本
grep -E "postinstall|preinstall" package.json
```

### Step 3：搜索危险模式
```bash
# 搜索网络调用
grep -r "curl\|wget\|axios\|request" node_modules/

# 搜索危险函数
grep -r "eval\|exec\|spawn" node_modules/

# 搜索敏感文件访问
grep -r "\.ssh\|\.env\|credentials" node_modules/
```

### Step 4：容器测试
```bash
# 在 Docker 中安装测试
docker run --rm -v $(pwd):/app node:alpine npm install package-name

# 监控文件变化
docker run --rm -v $(pwd):/app node:alpine ls -la
```

---

## 红旗警告 🚨

**立即拒绝安装的信号：**

| 红旗 | 说明 | 风险等级 |
|------|------|----------|
| postinstall 脚本 | 安装时自动执行代码 | 🔴 高危 |
| 网络调用 | 安装时访问外部服务器 | 🔴 高危 |
| 读取敏感文件 | 访问 ~/.ssh, ~/.env, 凭证文件 | 🔴 高危 |
| 使用 eval/exec | 动态执行代码 | 🔴 高危 |
| 未知作者 | 首次发布，无历史记录 | 🟡 中危 |
| 代码混淆 | 压缩、编码、混淆 | 🔴 高危 |
| 请求提权 | 需要 sudo/管理员权限 | 🔴 高危 |
| 访问浏览器 | 读取 cookie、session | 🔴 高危 |

---

## 风险等级分类

| 等级 | 标志 | 操作 |
|------|------|------|
| 🟢 低风险 | 无红旗，作者可信 | 可以直接安装 |
| 🟡 中风险 | 有警告但可解释 | 需要人工审查 |
| 🔴 高风险 | 有严重红旗 | 拒绝安装 |
| ⛔ 极高风险 | 多个严重红旗 | 举报给社区 |

---

## 检查报告模板

```
SKILL PREFLIGHT REPORT
═══════════════════════════
技能：[技能名称]
来源：[ClawHub / GitHub / npm]
作者：[作者名]
版本：[版本号]
───────────────────────────
指标：
• 下载量：[数字]
• 星标数：[数字]
• 最后更新：[日期]
• 文件审查：[数字] 个
───────────────────────────
红旗警告：[无 / 列表]

权限需求：
• 文件：[列表或"无"]
• 网络：[列表或"无"]
• 命令：[列表或"无"]
───────────────────────────
风险等级：[🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]

建议：[✅ 安全 / ⚠️ 谨慎 / ❌ 拒绝]

备注：[任何观察]
═══════════════════════════
```

---

## 信任层级

1. **官方 OpenClaw 技能** → 较低审查（仍需检查）
2. **高星标仓库（1000+）** → 中等审查
3. **知名作者** → 中等审查
4. **新/未知来源** → 最大审查
5. **请求凭证的技能** → 必须人工批准

---

## 自动化脚本

### preflight_check.sh
```bash
#!/bin/bash

SKILL_NAME=$1

echo "🔍 Preflight Check: $SKILL_NAME"
echo "═══════════════════════"

# 1. Check author
echo "1. Checking author..."
npm view $SKILL_NAME author

# 2. Check scripts
echo "2. Checking scripts..."
npm view $SKILL_NAME scripts

# 3. Download and scan
echo "3. Scanning for red flags..."
npm pack $SKILL_NAME
tar -xzf *.tgz
grep -r "curl\|wget\|eval" package/

# 4. Clean up
rm -rf package *.tgz

echo "═══════════════════════"
echo "✅ Preflight complete"
```

---

## 成功指标

- [ ] 100% 的技能经过预检检查
- [ ] 零恶意技能被安装
- [ ] 维护检查记录（runbook）
- [ ] 社区共享红旗技能列表

---

## 使用场景

### 场景 1：安装 ClawHub 技能
```
用户：clawhub install xxx-skill

助手：
1. 暂停安装
2. 运行预检检查
3. 生成报告
4. 如果安全，继续安装
5. 如果有红旗，警告用户
```

### 场景 2：安装 GitHub 技能
```
用户：从 GitHub 安装技能

助手：
1. 检查仓库星标和 fork 数
2. 检查作者其他项目
3. 审查 SKILL.md 和代码
4. 生成报告
5. 给出建议
```

### 场景 3：批量检查
```
用户：我要安装这 10 个技能

助手：
1. 逐个检查
2. 汇总报告
3. 分类（安全/谨慎/拒绝）
4. 给出优先级建议
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 无法获取作者信息 | 手动检查 GitHub/npm 页面 |
| 容器测试失败 | 检查 Docker 配置和网络 |
| 误报红旗 | 调整检查规则，添加白名单 |
| 检查时间太长 | 优化脚本，缓存结果 |

---

## 道德使用

- 不要仅因作者身份拒绝技能
- 给新作者公平机会
- 分享红旗发现帮助社区
- 保持检查规则透明

---

## 好处

- ✅ 避免安装恶意技能
- ✅ 保护敏感数据和凭证
- ✅ 减少安全事故响应时间
- ✅ 建立社区信任
- ✅ 90 秒预检避免数小时事故响应

---

## 相关资源

- `scripts/preflight_check.sh` - 预检脚本
- `scripts/scan_package.py` - 包扫描脚本
- `references/red-flags.md` - 红旗模式库
- `references/trusted-authors.md` - 可信作者白名单
- `references/checklist-template.md` - 检查清单模板
