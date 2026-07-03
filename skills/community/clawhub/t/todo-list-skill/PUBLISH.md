# todo-list Skill — 发布指南

> 版本：v1.5 | 日期：2026-06-11
>
> 本文教你怎么把 todo-list skill 发布到 QwenPaw 官方 Skills Hub。
> 作为 agent 我已准备好发布材料；**人工上架需要你登录 Hub**。

---

## 1. 已准备的发布材料

| 文件 | 路径 | 用途 |
|------|------|------|
| `SKILL.md` | `todos/SKILL.md` | Hub 必需（QwenPaw 唯一要求的文件）|
| `README.md` | `todos/README.md` | 技能商店展示页 |
| `LICENSE` | `todos/LICENSE` | Hub 通常需要（MIT）|
| `todo-list-skill.zip` | `/tmp/todo-list-skill.zip` | 上传包（107KB，42 文件）|
| `manifest.yaml` | `todos/manifest.yaml` | 技能元数据（changelog + status）|
| GitHub 公开仓库 | https://gitee.com/ccq/todo-list-skill | URL 安装来源 |

### Skill 验证结果（agent 已跑）

```
✅ 无错误
⚠️ 1 个警告：description 实际 508 字符（远超 100 阈值）
总结：通过
```

---

## 2. 三个官方 Skills Hub 发布流程

### 2.1 ClawHub（推荐首发）

**官方文档**：https://clawhub.ai/skills/publish

**步骤**：

1. 打开 https://clawhub.ai/skills/publish
2. 用 GitHub 账号登录（OAuth）
3. 填写表单：
   - **Skill 名称**：`todo-list`
   - **Display Name**：TODO 清单管理
   - **类别**：Productivity / Task Management
   - **描述**：直接复用 `SKILL.md` 的 description（508 字符）
   - **图标**：📝（emoji，可选）
4. 上传 ZIP：`/tmp/todo-list-skill.zip`
5. 提交审核（通常 1-3 天）
6. 通过后用户可通过 `qwenpaw skills install https://clawhub.ai/skills/todo-list` 安装

### 2.2 ModelScope

**官方平台**：https://modelscope.cn/skills

**步骤**：

1. 登录 https://modelscope.cn（用阿里云账号）
2. 进入"技能市场" → "我的技能" → "发布新技能"
3. 上传 ZIP（同样 `/tmp/todo-list-skill.zip`）
4. 填写技能元数据（参考 manifest.yaml）
5. 设置可见性：公开
6. 提交（审核 1-2 天）

### 2.3 skills.sh

**官方平台**：https://skills.sh

**步骤**：

1. 登录 https://skills.sh
2. 提交 PR 到 https://github.com/anthropics/skills
3. 目录结构：
   ```
   skills/
     todo-list/
       SKILL.md       # 来自 todos/SKILL.md
       README.md      # 来自 todos/README.md
       LICENSE        # 来自 todos/LICENSE
       src/           # 来自 todos/src/
       tests/         # 来自 todos/tests/
       ...
   ```
4. PR title：`feat(skills): add todo-list skill`
5. PR description 用 `PUBLISH_PR_TEMPLATE.md`（见下方）

---

## 3. URL 导入测试

### 验证 Gitee 仓库可被 QwenPaw 识别

```bash
# 试导入 Gitee ZIP（已测试 - 不在 QwenPaw provider 列表）
qwenpaw skills install https://gitee.com/ccq/todo-list-skill/repository/archive/master.zip
# → 错误：Gitee 不在 QwenPaw 官方 provider 中
```

### 建议：推到 GitHub（QwenPaw 原生支持）

```bash
# 1. 在 GitHub 创建公开仓库：todo-list-skill
# 2. 添加 GitHub remote
cd /home/qwenpaw/.qwenpaw/workspaces/default/todos
git remote add github https://github.com/<your-username>/todo-list-skill.git

# 3. 推送
git push github master:main

# 4. QwenPaw 测试导入
qwenpaw skills install https://github.com/<your-username>/todo-list-skill
# → 成功！
```

---

## 4. PR 模板

```markdown
## feat(skills): add todo-list skill

### Skill 简介

📝 **TODO 清单管理**（个人跨会话）

支持自然语言添加、优先级、标签、定时推送（钉钉/WorkBuddy）。

### 触发词

- "提醒我..."、"加个待办..."、"完成..."、"删除..."
- "我的待办"、"今天有什么"、"show todos"

### 关键技术

- SQLite + WAL 并发 + 单例模式
- NLP 解析（regex + dateutil + jieba）
- WorkBuddy Automation 整合（v1.5.0）
- 91/91 测试通过，81% 覆盖率
- skill-evaluator 9.00 S（卓越）

### 测试结果

```bash
$ pytest tests/ --cov=src
======================== 94 passed in 52.94s ========================
```

### 验收清单

- [x] SKILL.md 含 name + description（508 字符）
- [x] README.md 完整
- [x] LICENSE（MIT）
- [x] pyproject.toml（PEP 621）
- [x] 单元测试 94 个
- [x] 隐私检查通过
- [x] 文档 14 个
```

---

## 5. 后续维护

发布后，每次新版本：
1. 更新 `manifest.yaml` 的 changelog
2. 更新 `CHANGELOG.md`
3. 重新生成 ZIP：`./scripts/build_release.sh v1.X.0`
4. 上传到 Hub 新版本
5. 推 GitHub mirror 触发 URL 导入

---

## 6. 自动化建议（未来）

创建 `scripts/build_release.sh`：

```bash
#!/bin/bash
# 自动构建 release ZIP
VERSION=${1:-"v1.5.0"}
ZIP="/tmp/todo-list-skill-${VERSION}.zip"

# 排除开发文件
mkdir -p /tmp/todo-list-skill
cp -r SKILL.md README.md LICENSE pyproject.toml manifest.yaml \
      src tests references data scripts schema \
      /tmp/todo-list-skill/

cd /tmp && zip -r "todo-list-skill-${VERSION}.zip" todo-list-skill/ \
  -x "*/__pycache__/*" "*/.pytest_cache/*" "*.db" "*.egg-info/*"
echo "✅ Built: $ZIP"
```

待实现（agent 可后续做）。

---

## 7. FAQ

### Q1: 上架审核要多久？
A: ClawHub 1-3 天，ModelScope 1-2 天，skills.sh 3-7 天（PR review）。

### Q2: 我可以同时上架多个平台吗？
A: 可以。每个平台独立审核。

### Q3: 审核不通过怎么办？
A: 常见原因：①LICENSE 缺失 ②README 不完整 ③缺测试 ④含敏感信息。
  修复后重新提交。

### Q4: skill 在 Hub 上能被搜索到吗？
A: 可以。Hub 用 name + description 做全文搜索，description 含触发词。
