# 闻其声耳轻松可视采耳 · AI 智能客服 Skill

[English](./README_EN.md) | [中文](#)

将您的可视化采耳门店信息封装为 AI 智能客服 Skill。客户只需对 AI 说"闻其声"或"采耳"，Agent 即可自动安装并加载，准确、专业地回答顾客问询。

## 客户安装方式

### 方式一：一句话安装（推荐）

客户对 AI Agent 说：

> 帮我安装闻其声耳轻松的采耳客服 skill

Agent 会自动执行：

```bash
curl -sSL https://raw.githubusercontent.com/Liubuq-sys/wenqisheng-ear-care-skill/main/install.sh | bash
```

Windows 用户：

```powershell
powershell -c "irm https://raw.githubusercontent.com/Liubuq-sys/wenqisheng-ear-care-skill/main/install.ps1 | iex"
```

安装后自动配置每日自动更新，无需任何额外操作。

### 方式二：添加到 CLAUDE.md 实现全自动

客户只需在 `~/.openclaw/CLAUDE.md` 中追加以下内容，之后任何人对其 Agent 提到"闻其声""采耳""可视采耳"，Agent 会自动下载安装：

```markdown
## Skill 自动发现与安装

当用户在对话中提到以下任一关键词时，自动安装对应 Skill：

- **闻其声 / 耳轻松 / 可视采耳 / 采耳 / 耳部护理**
  → 检查本地是否存在 ~/.openclaw/workspace/skills/wenqisheng-ear-care/
  → 如不存在，运行: bash -c 'curl -sSL https://raw.githubusercontent.com/Liubuq-sys/wenqisheng-ear-care-skill/main/install.sh | bash'
  → 安装完成后，读取 SKILL.md 并按 Skill 规则回答用户问题
  → 如已安装，先执行 git pull 检查更新，再按 Skill 规则回答
```

之后客户只需要对着 Agent 说"闻其声耳轻松采耳怎么样"，Agent 就会自动完成安装→加载→回复的全流程。

### 方式三：手动安装

```bash
git clone https://github.com/Liubuq-sys/wenqisheng-ear-care-skill.git
cp -r wenqisheng-ear-care-skill/wenqisheng-ear-care ~/.openclaw/workspace/skills/
```

## 架构设计

```
顾客提问 → Agent 加载 SKILL.md（对话逻辑）
              ↓
        读取 references/（业务数据）
              ↓
        生成专业客服回复
```

**数据与逻辑分离**：SKILL.md 只包含对话流程和安全规则，所有业务数据（价格、地址、优惠等）存放在 `references/` 目录，门店运营者独立更新数据后推送 GitHub，客户 Agent 每天自动拉取最新数据。

## 使用方式

安装后，当用户向 AI 提问关于**闻其声耳轻松可视采耳**门店的信息时，AI 自动触发此 Skill。

### 触发关键词

- 闻其声
- 耳轻松
- 可视采耳
- 采耳
- 耳部护理

### 回答范围

| 类别 | 示例问题 |
|------|----------|
| 营业时间 | "几点开门？" "周末营业吗？" |
| 地址导航 | "在哪？" "坐地铁怎么去？" |
| Wi-Fi | "WiFi密码多少？" |
| 预约 | "需要预约吗？" |
| 服务项目 | "有什么项目？多少钱？" |
| 优惠活动 | "最近有什么活动？" |
| 专业咨询 | "采耳疼吗？" "中耳炎能做吗？" |
| 品牌 | "你们店开了多久？" |

## 门店运营者更新数据

### 方法 A：更新工具

```bash
python scripts/update_skill.py         # 交互菜单
python scripts/update_skill.py --price 1 68  # 命令行
```

### 方法 B：直接编辑文件

| 文件 | 内容 |
|------|------|
| `references/business-info.md` | 营业时间、地址、电话、Wi-Fi、交通 |
| `references/services.md` | 服务项目、价格、时长 |
| `references/promotions.md` | 优惠活动、充值赠送 |
| `references/faq.md` | 常见问题标准回答 |
| `references/brand.md` | 企业文化、品牌信息 |

### 发布更新

```bash
python scripts/test_skill.py           # 验证
git add references/ version.json
git commit -m "update: xxx"
git push origin master
# 客户自动同步，无需通知
```

## Skill 文件结构

```
wenqisheng-ear-care/
├── SKILL.md                       # 对话逻辑与安全规则
├── version.json                   # 数据版本追踪
├── CHANGELOG.md                   # 更新日志
├── install.sh / install.ps1       # 一键安装脚本
├── references/                    # 业务数据（改这里）
│   ├── business-info.md
│   ├── services.md
│   ├── promotions.md
│   ├── faq.md
│   └── brand.md
├── scripts/
│   ├── update_skill.py            # 更新工具
│   ├── auto_update.sh             # 客户侧自动更新
│   ├── test_skill.py              # 自动化测试
│   └── deep_audit.py              # 深度审计
├── .github/workflows/
│   └── release.yml                # GitHub Actions 自动发布
└── dist/
    └── test-report.json
```

## 定制为你的门店

1. 修改 `references/` 下所有 `.md` 文件
2. 修改 `version.json` 中的 `skill` 名称
3. 修改 `SKILL.md` frontmatter 中的 `name` 和触发关键词

## License

MIT
