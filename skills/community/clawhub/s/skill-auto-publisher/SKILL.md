---
name: skill-auto-publisher
description: ClawHub 技能发布助手 — AI 全流程搞定：自动递增版本 → 智能生成 changelog → 元数据验证 → 用户确认 → 一键发布。触发词：发布技能、publish skill、ClawHub发布、发布到ClawHub、技能发布。
---

# 🚀 ClawHub 技能发布助手

一键发布技能到 ClawHub，支持版本自动递增、changelog 智能生成、元数据验证。

---

## 一、发布流程

```
用户请求发布技能
        │
        ▼
  查找技能目录
        │
        ▼
  技能名称占用检测（检查 ClawHub 是否已有同名技能）
        │
   ┌────┴────┐
   │         │
  被占用    未占用
   │         │
   ▼         ▼
 提示改名   继续流程
   │
   ▼
  元数据验证（SKILL.md 格式检查）
        │
        ▼
  读取当前版本
        │
        ▼
  分析变更内容 → 智能生成 changelog
        │
        ▼
  建议新版本号
        │
        ▼
  显示发布摘要 → 用户确认
        │
   ┌────┴────┐
   │         │
  确认      取消
   │         │
   ▼         ▼
 执行发布   退出
   │
   ▼
 更新发布历史
```

---

## 二、触发方式

**自然语言触发**：
- 「发布 xxx-skill 技能」
- 「把 xxx-skill 发布到 ClawHub」
- 「发布这个技能」

---

## 三、核心功能

### 3.1 技能名称占用检测（新增）

**检测时机**：发布前自动检测

**实现方式**：
```bash
# 使用 skillhub search 检测名称是否被占用
skillhub search <skill-name> | grep -q "<skill-name>" && echo "已被占用" || echo "可用"
```

**占用时的处理**：
1. 提示用户名称已被占用
2. 显示占用者的技能链接
3. 建议替代名称：
   - 添加前缀：`xiao-duo-<skill-name>`
   - 添加后缀：`<skill-name>-cn`
   - 使用缩写

**示例**：
```
❌ 技能名称「skill-publisher」已被占用
   占用者：/SASAMITTRRR/skill-publisher

💡 建议替代名称：
   1. xiao-duo-skill-publisher
   2. skill-publisher-cn
   3. skill-auto-publisher

请选择或输入新名称：
```

---

### 3.2 版本自动递增

**规则**：

| 变更类型 | 版本递增 | 示例 |
|---------|---------|------|
| **Patch** | x.y.z → x.y.(z+1) | Bug 修复、小改动 |
| **Minor** | x.y.z → x.(y+1).0 | 新功能、新参数 |
| **Major** | x.y.z → (x+1).0.0 | 重大变更、不兼容更新 |

**判断逻辑**：
1. 检测 SKILL.md 变更：
   - 新增 description 内容 → Minor
   - 修改 description 内容 → Patch
   - 新增/删除核心章节 → Minor
2. 检测 scripts/ 变更：
   - 新增脚本 → Minor
   - 修复脚本 bug → Patch
3. 检测 references/ 变更：
   - 新增参考文档 → Patch

**版本号来源**：
- 优先读取 `_meta.json` 中的 `version` 字段
- 如果没有，从 `package.json` 或默认 `1.0.0` 开始

---

### 3.3 Changelog 智能生成

**实现方式**：
1. 读取 `.publish_history.json` 获取上次发布的文件快照
2. 对比当前文件与快照的差异
3. AI 分析变更内容，生成简洁的 changelog

**文件快照格式**：
```json
{
  "xxx-skill": {
    "last_version": "1.0.1",
    "last_published_at": "2026-03-15T12:00:00",
    "files": {
      "SKILL.md": "hash:abc123",
      "scripts/main.sh": "hash:def456"
    },
    "changelog": "新增功能"
  }
}
```

**Changelog 生成规则**：
- 新增功能：「新增 xxx 功能」
- 修复问题：「修复 xxx 问题」
- 优化改进：「优化 xxx」
- 文档更新：「更新 xxx 文档」

---

### 3.4 元数据验证

**检查项**：

| 检查项 | 规则 | 错误级别 |
|--------|------|---------|
| **name** | 必填，小写字母+连字符 | ❌ 阻止发布 |
| **description** | 必填，至少 20 字符 | ❌ 阻止发布 |
| **YAML 格式** | 语法正确 | ❌ 阻止发布 |
| **触发词** | description 中包含「触发词」| ⚠️ 警告 |

**验证脚本**：[scripts/validate_meta.py]({baseDir}/scripts/validate_meta.py)

---

## 四、使用示例

### 示例 1：发布指定技能

```
用户：发布 xxx-skill 技能

AI：
📋 发布摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
技能名称：xxx-skill
当前版本：1.0.0
建议版本：1.0.1 (Patch)

📝 检测到变更：
- SKILL.md: 新增触发词

📄 Changelog：
"新增触发词描述"

✅ 元数据验证通过

确认发布？(y/n)
```

### 示例 2：发布当前技能（模糊匹配）

```
用户：发布这个技能

AI：
🔍 检测到最近修改的技能：xxx-skill

📋 发布摘要
...
```

---

## 五、发布历史

**历史文件**：`/root/.openclaw/workspace/skills/.publish_history.json`

**用途**：
1. 记录每次发布的版本、时间、changelog
2. 对比文件变更，智能生成 changelog
3. 避免重复发布相同版本

---

## 六、命令参考

**手动发布（跳过验证）**：
```bash
bash {baseDir}/scripts/publish.sh <skill-path> --version <version> --changelog <message> --skip-validate
```

**仅验证元数据**：
```bash
python3 {baseDir}/scripts/validate_meta.py <skill-path>
```

**查看发布历史**：
```bash
python3 {baseDir}/scripts/show_history.py <skill-name>
```

---

## 七、注意事项

1. **发布前确认**：必须用户确认后才执行发布
2. **版本号唯一**：不能发布已存在的版本号
3. **网络检查**：发布前检查网络连接
4. **登录状态**：确保 ClawHub CLI 已登录

---

## 八、故障排查

| 问题 | 解决方案 |
|------|---------|
| 「未找到技能目录」 | 检查技能路径是否正确 |
| 「元数据验证失败」 | 检查 SKILL.md 格式 |
| 「版本已存在」 | 递增版本号后重试 |
| 「网络错误」 | 检查网络连接 |
