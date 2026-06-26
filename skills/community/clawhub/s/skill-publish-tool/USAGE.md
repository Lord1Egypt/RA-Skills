# skill-publish-tool 使用指南

## 快速开始

### 1. 安装 skill

```bash
npx clawhub@latest install skill-publish-tool
```

### 2. 基本用法

```bash
# 进入 skill 目录
cd ~/.jvs/.openclaw/workspace/skills/skill-publish-tool

# 发布其他 skill
python3 scripts/publish_skill.py <要发布的 skill 目录> \
  --slug <clawhub-slug> \
  --changelog "<更新日志>"
```

## 完整示例

### 示例 1: 发布补丁版本（默认）

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/cn-stock-volume \
  --slug cn-stock-volume \
  --changelog "修复数据获取错误"
```

**效果：**
- 版本号：1.0.0 → 1.0.1
- 更新 package.json 和 _meta.json
- 更新 README.md 更新日志
- Git 提交并推送
- 发布到 ClawHub

### 示例 2: 发布集合仓库中的 skill（Monorepo）

```bash
# 从 skill 集合仓库发布单个 skill
python3 scripts/publish_skill.py \
  ~/.jvs/.openclaw/workspace/skills/cn-stock-volume/cn-stock-volume \
  --slug cn-stock-volume \
  --changelog "新增功能" \
  --collection-root ~/.jvs/.openclaw/workspace/skills/cn-stock-volume
```

**说明：**
- `path`: 单个 skill 的目录
- `collection-root`: 集合仓库根目录（Git 仓库位置）
- Git 提交会在集合根目录进行
- 适合 monorepo 结构

### 示例 3: 发布小版本更新

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/my-skill \
  --slug my-skill \
  --bump minor \
  --changelog "新增 XX 功能"
```

**效果：**
- 版本号：1.0.0 → 1.1.0

### 示例 3: 发布大版本更新

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/my-skill \
  --slug my-skill \
  --bump major \
  --changelog "重构核心架构，不兼容旧版本"
```

**效果：**
- 版本号：1.0.0 → 2.0.0

### 示例 4: 仅更新本地文件（不发布）

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/my-skill \
  --slug my-skill \
  --changelog "本地测试" \
  --skip-clawhub
```

### 示例 5: 仅发布到 ClawHub（不推送 Git）

```bash
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/my-skill \
  --slug my-skill \
  --changelog "仅发布" \
  --skip-git
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `path` | ✅ | - | 要发布的 skill 目录路径 |
| `--slug` | ✅ | - | ClawHub 上的 skill slug |
| `--name` | ❌ | - | Display name（当前未使用） |
| `--bump` | ❌ | patch | 版本号递增类型：major/minor/patch |
| `--changelog` | ✅ | - | 更新日志内容 |
| `--skip-git` | ❌ | false | 跳过 Git 操作 |
| `--skip-clawhub` | ❌ | false | 跳过 ClawHub 发布 |

## 输出示例

```
============================================================
  📦 Skill Publisher
  路径：/Users/xxx/skills/cn-stock-volume
  Slug: cn-stock-volume
============================================================

📋 当前版本：v1.0.0
📋 新版本：v1.0.1

━━━ 步骤 1: 更新版本号 ━━━
✅ 已更新：package.json → v1.0.1
✅ 已更新：_meta.json → v1.0.1

━━━ 步骤 2: 更新 README.md ━━━
✅ 已更新 README.md 更新日志 → v1.0.1

━━━ 步骤 3: Git 提交和推送 ━━━
✅ Git 推送成功

━━━ 步骤 4: 发布到 ClawHub ━━━
🚀 发布到 ClawHub: cn-stock-volume@1.0.1
✅ ClawHub 发布成功!
📦 Skill ID: k974z4a6pc4bv3gverd92c935s83anr6
🔗 链接：https://clawhub.ai/k974z4a6pc4bv3gverd92c935s83anr6/cn-stock-volume

============================================================
  ✅ 发布完成!
  版本：v1.0.1
============================================================
```

## 常见问题

### Q: 提示"Version already exists"
**原因**: 该版本已发布过
**解决**: 使用 `--bump` 参数自动递增版本号

### Q: 提示"Slug is already taken"
**原因**: slug 已被其他 skill 使用
**解决**: 更换唯一的 slug 名称

### Q: Git 推送失败 - 未配置远程仓库
**原因**: 未配置远程仓库
**解决**: 
```bash
cd <skill 目录>
git remote add origin <github-repo-url>
git push -u origin main
```

### Q: Git 推送失败 - 远程仓库已有内容
**原因**: 远程仓库有独立的历史记录
**解决**: 
```bash
cd <skill 目录>
# 方法 1: 强制推送（覆盖远程）
git push -u origin main --force

# 方法 2: 合并远程历史
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Q: Git 认证失败
**原因**: 未配置 Git 凭证或 SSH 密钥
**解决**: 
- HTTPS: `git config --global credential.helper store` 然后重新输入密码
- SSH: 配置 SSH 密钥 `ssh-keygen` 并添加到 GitHub

### Q: ClawHub 发布失败
**原因**: 未登录或网络问题
**解决**: 确保已登录 ClawHub，检查网络连接

## 最佳实践

1. **提交前测试**: 发布前确保 skill 能正常工作
2. **语义化版本**: 
   - patch: 修复 bug
   - minor: 新增功能（向后兼容）
   - major: 破坏性变更
3. **清晰的更新日志**: 简要说明做了什么改动
4. **Git 标签**: 可以手动添加 Git 标签标记版本

## 自动化工作流

可以将此 skill 集成到 CI/CD 流程中：

```bash
# GitHub Actions 示例
- name: Publish Skill
  run: |
    python3 scripts/publish_skill.py ./my-skill \
      --slug my-skill \
      --changelog "${{ github.event.head_commit.message }}" \
      --skip-git
```

## 许可证

MIT License
