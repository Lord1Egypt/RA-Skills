# Fast 模式 - Phase 1：想法明确

**模式**: Fast 快速模式（爱好者・极简）
**Phase数**: 2/5

---

## 1.1 提取核心信息

从用户输入中快速提取：

| 要素 | 提取目标 |
|------|---------|
| 类型 | 都市/玄幻/穿越/甜宠 |
| 金手指 | 系统/重生/异能/传承 |
| 核心爽点 | 打脸/升级/甜宠 |
| 主角设定 | 男频/女频 |

---

## 1.2 快速确认

```markdown
## 你的故事

🎯 类型：[类型]
🔮 金手指：[金手指]
💥 爽点：[核心爽点]

确认以上信息，或者告诉我需要修改的部分。
```

---

## 1.3 创建项目

创建 `./web-novels/{timestamp}-{小说名称}/`

创建简版 `03-写作计划.json`：

```json
{
  "version": 1,
  "mode": "fast",
  "novelName": "[小说名称]",
  "totalChapters": [待定],
  "status": "planning",
  "coreSetting": {
    "genre": "[类型]",
    "goldenFinger": "[金手指]",
    "coreTropes": "[爽点]"
  }
}
```

---

→ 进入 [Fast2_Quick_Draft.md](./Fast2_Quick_Draft.md)
