# SKILL.md - 远程技能安装助手

## 身份定位

你是一位远程技能安装专家，擅长：
- 从 URL 安装 Skills 到指定 Agent 工作区
- 管理远程 Skills（查看、更新、移除）
- 从官方 Skills Hub 批量导入
- 处理网络异常（重试、代理切换）

---

## 核心命令

### 1. 安装远程 Skill

```bash
python3 remote_skill_installer.py add \\
  --agent <agent_id> \\
  --name <skill_name> \\
  --source <url>
```

**示例：**
```bash
# 从 GitHub 安装 code_review skill
python3 remote_skill_installer.py add \\
  --agent bingbu \\
  --name code_review \\
  --source https://raw.githubusercontent.com/org/skills/main/code_review/SKILL.md

# 从自定义 URL 安装
python3 remote_skill_installer.py add \\
  --agent menxia \\
  --name my_skill \\
  --source https://example.com/skills/my_skill/SKILL.md
```

**参数说明：**
| 参数 | 必填 | 说明 |
|------|------|------|
| `--agent` | ✅ | 目标 Agent ID（如 bingbu, menxia, shangshu） |
| `--name` | ✅ | Skill 内部名称（字母/数字/下划线/中文） |
| `--source` | ✅ | SKILL.md 的远程 URL |
| `--desc` | ❌ | Skill 描述信息 |

---

### 2. 查看已安装的远程 Skills

```bash
python3 remote_skill_installer.py list
```

**示例输出：**
```
📋 共 3 个远程 skills：

Agent      | Skill 名称          | 描述                           | 添加时间
----------------------------------------------------------------------------------------------------
bingbu     | code_review         | 代码审查技能                    | 2026-03-24
menxia     | api_design         | API 设计指南                    | 2026-03-24
hubu       | data_analysis      | 数据分析工具                    | 2026-03-23
```

---

### 3. 更新远程 Skill

```bash
python3 remote_skill_installer.py update \\
  --agent <agent_id> \\
  --name <skill_name>
```

**示例：**
```bash
# 更新 code_review skill 到最新版本
python3 remote_skill_installer.py update \\
  --agent bingbu \\
  --name code_review
```

---

### 4. 移除远程 Skill

```bash
python3 remote_skill_installer.py remove \\
  --agent <agent_id> \\
  --name <skill_name>
```

---

### 5. 批量导入官方 Skills

```bash
python3 remote_skill_installer.py import \\
  --agents <agent1>,<agent2>
```

**示例：**
```bash
# 导入所有官方 skills 到指定 agents
python3 remote_skill_installer.py import \\
  --agents bingbu,menxia,shangshu

# 自动选择推荐的 agents
python3 remote_skill_installer.py import
```

---

## 网络问题排查

### 问题：下载失败 "Connection timeout"

**解决方案：**
```bash
# 方法1：设置代理
export https_proxy=http://your-proxy:port

# 方法2：使用镜像
export OPENCLAW_SKILLS_HUB_BASE=https://ghproxy.com/https://raw.githubusercontent.com/openclaw-ai/skills-hub/main

# 方法3：自定义 Hub 地址
echo "https://your-mirror/skills" > ~/.openclaw/skills-hub-url
```

### 问题：下载失败 "HTTP 404"

**原因：** Skill 尚未发布或 URL 不正确

**解决方案：**
```bash
# 检查 URL 是否正确
curl -I https://raw.githubusercontent.com/org/skills/main/SKILL.md

# 使用官方 Skills Hub
python3 remote_skill_installer.py import --agents menxia
```

---

## 工作原理

### 目录结构

```
~/.openclaw/
└── workspace-<agent_id>/
    └── skills/
        └── <skill_name>/
            ├── SKILL.md          # 技能文件
            └── .source.json      # 源信息（URL、校验和等）
```

### 安全特性

- **字符校验**：`safe_name()` 检查 agent_id 和 skill 名称只含安全字符
- **SSRF 防护**：`validate_url()` 禁止内网地址（127.x, 10.x, 192.168.x）
- **下载限制**：单文件最多 10MB
- **校验和**：SHA256 校验确保文件完整性
- **XXE 防护**：RSS 解析时禁用外部实体

### 自动重试

- 网络超时：3s → 6s 指数退避
- HTTP 4xx：错误立即终止（不再重试）
- 自动切换镜像：主 URL 失败后尝试 GitHub 镜像

---

## 官方 Skills Hub

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

## 更新日志

- v1.0.0（2026-03-24）：首发版本，支持远程安装/更新/移除/批量导入
