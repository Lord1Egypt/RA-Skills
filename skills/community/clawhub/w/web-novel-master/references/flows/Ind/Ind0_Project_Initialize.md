# Industrial 模式 - Phase 0：项目初始化

**模式**: Industrial 工业模式（团队・最完整・可流水线）
**Phase数**: 1/10

---

## 0.1 系统检查

### 检查项

| 检查项 | 说明 |
|--------|------|
| 目录结构 | 确保 `./web-novels/` 存在 |
| 偏好系统 | 检查 `user-preferences.json` |
| 脚本可用性 | `scripts/check_chapter_wordcount.py` |
| Agent权限 | TaskCreate / TeamCreate 权限 |

---

## 0.2 项目初始化

### 创建项目文件夹

`./web-novels/{YYYYMMDD-HHmmss}-{项目名称}/`

### 创建项目配置

```json
{
  "version": 1,
  "mode": "industrial",
  "projectName": "[项目名称]",
  "projectPath": "./web-novels/{timestamp}-[项目名称]",
  "createdAt": "[ISO时间]",
  "status": "initializing",
  "team": {
    "size": null,
    "members": []
  }
}
```

---

## 0.3 中断续写检测

扫描 `./web-novels/`：

**如有未完成项目**：
- 展示：项目名称、状态、完成进度
- 提供选项：
  - `继续项目` → 从中断阶段继续
  - `新建项目` → 初始化新项目

---

## 0.4 团队配置（如需要）

```
Question: 本项目是否使用团队协作？
Options:
- 【单人创作】我自己完成
- 【小团队】2-3人协作
- 【大团队】4人以上，可流水线
```

---

## 0.5 项目初始化确认

```markdown
## 项目初始化完成

项目名称：[名称]
项目路径：[路径]
模式：Industrial 工业模式
团队：[单人/小团队/大团队]

下一步：进入 Phase 1 市场调研
```

---

→ 进入 [Ind1_Market_Research.md](./Ind1_Market_Research.md)
