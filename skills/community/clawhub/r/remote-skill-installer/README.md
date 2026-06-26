# 🛠️ 远程技能安装助手

> 从 URL 远程安装、管理 OpenClaw Skills，支持官方 Hub 批量导入

---

## ✨ 功能特色

- **远程安装** - 从任意 URL 安装 SKILL.md 到指定 Agent 工作区
- **批量导入** - 一键从官方 Skills Hub 导入全套技能
- **智能重试** - 网络失败自动指数退避，支持代理切换
- **安全防护** - SSRF 防护、字符校验、校验和验证
- **镜像切换** - GitHub 访问不稳定时自动切换备用镜像

---

## 🚀 快速开始

### 安装

```bash
# 方式1：复制到本地
cp -r remote-skill-installer/ ~/.openclaw/skills/

# 方式2：直接运行（无需安装）
python3 remote_skill_installer.py --help
```

### 基本使用

```bash
# 安装远程 skill
python3 remote_skill_installer.py add \
  --agent bingbu \
  --name code_review \
  --source https://example.com/skills/code_review/SKILL.md

# 查看已安装的远程 skills
python3 remote_skill_installer.py list

# 更新 skill 到最新版本
python3 remote_skill_installer.py update --agent bingbu --name code_review

# 移除 skill
python3 remote_skill_installer.py remove --agent bingbu --name code_review

# 批量导入官方 skills
python3 remote_skill_installer.py import --agents bingbu,menxia,shangshu
```

---

## 📖 使用示例

### 示例1：从 GitHub 安装 Skill

```bash
python3 remote_skill_installer.py add \
  --agent bingbu \
  --name code_review \
  --source https://raw.githubusercontent.com/org/skills/main/code_review/SKILL.md \
  --desc "代码审查专家"
```

**输出：**
```
⏳ 正在从 https://raw.githubusercontent.com/... 下载...
✅ 技能 code_review 已添加到 bingbu
   路径: /home/user/.openclaw/workspace-bingbu/skills/code_review/SKILL.md
   大小: 4521 字节
```

### 示例2：批量导入官方 Skills

```bash
python3 remote_skill_installer.py import --agents bingbu,menxia,shangshu
```

**输出：**
```
📦 自动选择推荐 agents: bingbu, menxia, shangshu

📥 正在导入 skill: code_review
   目标 agents: bingbu, menxia, shangshu
✅ 技能 code_review 已添加到 bingbu
✅ 技能 code_review 已添加到 menxia
✅ 技能 code_review 已添加到 shangshu

📥 正在导入 skill: api_design
...

📊 导入完成：18/18 个 skills 成功
```

### 示例3：查看已安装的 Skills

```bash
python3 remote_skill_installer.py list
```

**输出：**
```
📋 共 5 个远程 skills：

Agent      | Skill 名称          | 描述                           | 添加时间
----------------------------------------------------------------------------------------------------
bingbu     | code_review         | 代码审查专家                    | 2026-03-24
bingbu     | security_audit     | 安全审计专家                    | 2026-03-24
menxia     | api_design         | API 设计指南                    | 2026-03-24
hubu       | data_analysis      | 数据分析工具                    | 2026-03-23
libu       | doc_generation     | 文档生成器                      | 2026-03-23
```

---

## 🔧 高级配置

### 设置代理

```bash
# 环境变量
export https_proxy=http://your-proxy:port

# 或自定义 Hub 地址
export OPENCLAW_SKILLS_HUB_BASE=https://ghproxy.com/https://raw.githubusercontent.com/openclaw-ai/skills-hub/main
```

### 自定义镜像源

```bash
echo "https://your-mirror/skills" > ~/.openclaw/skills-hub-url
```

---

## 🏛️ 官方 Skills Hub

| Skill | 说明 |
|-------|------|
| code_review | 代码审查：自动扫描常见漏洞、代码规范问题 |
| api_design | API 设计：RESTful 规范、接口文档、版本管理 |
| security_audit | 安全审计：SQL注入、XSS、CSRF 等常见威胁检测 |
| data_analysis | 数据分析：数据清洗、统计建模、可视化报表 |
| doc_generation | 文档生成：自动生成技术文档、API 文档、README |
| test_framework | 测试框架：单元测试、集成测试、自动化测试用例 |

> 💡 使用 `import` 命令可一键安装所有官方 Skills

---

## 🔒 安全特性

- **SSRF 防护** - 禁止访问内网地址（127.x, 10.x, 192.168.x）
- **字符校验** - agent_id 和 skill 名称只允许安全字符
- **下载限制** - 单文件最多 10MB
- **校验和** - SHA256 校验确保文件完整性

---

## 📁 目录结构

```
~/.openclaw/
└── workspace-<agent_id>/
    └── skills/
        └── <skill_name>/
            ├── SKILL.md          # 技能文件
            └── .source.json      # 源信息
```

---

## 📝 更新日志

- v1.0.0（2026-03-24）：首发版本，支持 add/list/update/remove/import 命令

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

*🛠️ OpenClaw Skills 生态成员*
