# 共享机制

本文件定义跨阶段共享的机制和规则。

---

## 三大黄金法则

1. **展示而非讲述** - 用动作和对话表现，不要直接陈述。修炼突破要写出身体感受
2. **爽点驱动剧情** - 每章必须有爽点或爽点铺垫
3. **悬念承上启下** - 每章结尾必须留下钩子

---

## 工作路径系统

### 核心概念

Skill 的所有产出文件（配置、设定、章节等）均基于**用户确认的工作路径** + Skill 定义的子路径。

| 变量 | 含义 | 示例 |
|------|------|------|
| `{workspace}` | 用户确认的工作根目录 | `/Users/me/projects/我的小说` |
| `{base}` | Skill 的基础输出目录 | `{workspace}/xuanhuan-novelist` |
| `{projectPath}` | 单个项目的目录 | `{base}/20260605-逆天邪神` |

### 路径解析规则

- 所有流程文档中的 `./xuanhuan-novelist/` 均等价于 `{base}/`
- `user-preferences.json` 存储在 `{workspace}/` 下（跨项目共享）
- `.pending-title` 存储在 `{base}/` 下
- 项目文件存储在 `{projectPath}/` 下

### 工作路径如何确定

Phase 0 启动时引导用户确认工作路径（详见 `phase0-initialization.md` 步骤 0）。确认后整个会话期间复用该路径，不重复询问。

---

## 用户偏好系统

### 存储文件

`user-preferences.json`（项目根目录，首次使用后自动创建）

### 数据结构

```json
{
  "version": 1,
  "updatedAt": "2026-06-05",
  "preferences": {
    "favoriteSubGenres": [],
    "preferredProtagonist": "",
    "preferredGoldenFinger": "",
    "preferredPerspective": "",
    "preferredTone": "",
    "typicalChapterCount": null,
    "styleReferences": [],
    "cultivationPreference": "",
    "dislikes": [],
    "creationHistory": []
  }
}
```

### 偏好更新规则

| 时机 | 行为 |
|------|------|
| 每完成一层问答 | 静默将本层回答同步到偏好文件（追加/更新，不删除历史） |
| 用户说"记住我的偏好" | 保存当前所有配置到偏好 |
| 用户说"忘记XX偏好" | 清除指定维度的偏好 |
| 用户说"重置偏好" | 清空所有偏好数据 |
| 一部长篇创作完成 | 将作品信息追加到 `creationHistory` |

### 偏好如何影响交互

1. **启动欢迎语**：有偏好时显示"欢迎回来！" + 个性化提示
2. **选项排序**：Q1中将 `favoriteSubGenres` 匹配项排前面
3. **常用标记**：Q5/Q8中对应用⭐标记"你的常用"/"上次选择"
4. **随机生成**：优先从偏好范围内随机选取，保持一致性
5. **风格参考追问**：优先推荐 `styleReferences` 中的作者/作品

### 错误恢复

- **回退修改**：用户随时可说"回到QX"、"修改XX"，AI 回退到指定问题重新询问
- **中途暂存**：通过 `02-写作计划.json` 实现自动暂存
- **偏好文件损坏**：JSON解析失败时忽略偏好，使用默认值

---

## 标题传递机制

### 传递方式

标题通过**对话上下文**在阶段间传递，同时通过临时文件防中断。

**传递链路**：
1. Phase 1 Layer 3：用户选择/确认标题 → 标题存入对话上下文 + 写入 `{base}/.pending-title` 临时文件
2. Phase 2：从上下文读取标题 → 写入项目目录名、`02-写作计划.json`、`01-大纲.md` → 删除 `.pending-title` 临时文件

**中断恢复**：若 Phase 1 Layer 3 完成后中断，Phase 0 读取 `.pending-title` 文件，允许用户直接跳到 Phase 2

---

## 写作计划系统

### 存储文件

`02-写作计划.json`（项目文件夹内，Phase 2 创建）

### 作用

- **进度跟踪**：记录每章创作状态（pending/in_progress/completed/failed）
- **写作模式**：记录用户选择的写作模式（serial/subagent-parallel/agent-teams）
- **修炼体系**：记录修炼体系设定，供创作时参照
- **势力地图**：记录势力和地图信息
- **创作规则**：`writingRules` 字段记录用户选择的创作规则配置（内容量/风格/体系），Phase 3 动态参照执行。如果字段不存在（旧项目），自动 fallback 到默认推荐方案
- **中断续写**：Phase 0 读取 JSON 检测未完成项目
- **校验依据**：Phase 4 基于 JSON 校验章节完成度和字数

### 与大纲的关系

- `01-大纲.md`：章节规划 + 章节摘要 + 修炼体系 + 势力地图 + 爽点分布
- `02-写作计划.json`：章节状态、字数、修炼体系结构化数据（机器可读）
- Phase 3 创作每章时必须同时读取两者

---

## 字数检查脚本

使用 `scripts/check_chapter_wordcount.py` 检查章节字数：

```bash
# 检查单个章节
python scripts/check_chapter_wordcount.py {base}/项目文件夹/第01章.md

# 检查所有章节
python scripts/check_chapter_wordcount.py --all {base}/项目文件夹/

# 自定义最小字数
python scripts/check_chapter_wordcount.py {base}/项目文件夹/第01章.md 3500
```

### 使用场景

| 阶段 | 用途 |
|------|------|
| Phase 3（逐章创作） | 撰写后检查单章字数，低于配置的 min 值必须扩充 |
| Phase 4（自动校验） | 批量检查所有章节字数，不合格章节自动重写 |

低于配置的 min 值的章节必须使用 [content-expansion.md](../guides/content-expansion.md) 的扩充技巧进行扩充。
