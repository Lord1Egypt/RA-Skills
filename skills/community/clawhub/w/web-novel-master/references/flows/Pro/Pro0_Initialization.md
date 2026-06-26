# Professional 模式 - Phase 0：初始化

**模式**: Professional 专业模式（作者・完整但不繁琐）
**Phase数**: 1/8

---

## 0.1 偏好加载

检查 `user-preferences.json`：
- 存在 → 加载偏好数据，选项排序+标记常用
- 不存在 → 使用默认值

---

## 0.2 中断续写检测

扫描 `./web-novels/`：

**如有未完成项目**：
- 展示：小说名称，完成进度
- 提供选项：
  - `继续上次创作` → 进入 Pro4_Full_Draft_Writing
  - `开始新作品` → 进入 Phase 1

---

## 0.3 目录初始化

确保 `./web-novels/` 目录存在

---

## 0.4 欢迎确认

```
🎯 Professional 专业创作模式启动！

请选择：
- 【快速开始】告诉我你想写什么小说
- 【详细问答】一步步完成所有创作配置
```

---

→ 进入 [Pro1_Core_Clarify.md](./Pro1_Core_Clarify.md)
