# 📖 模组索引

> 目标：运行模组时快速定位所需信息，减少上下文浪费。
> 模组数据存储于战役数据库，通过 `ModuleImportService` / `ModuleProgressService` 管理。

---

## 一、模组导入

模组文件（PDF/Markdown）通过 `dnd_module` 工具或 CLI 导入战役数据库：

```powershell
python -m nanobot.dnd.db.cli module import --campaign <id> --path "<path>" --name "<name>"
```

导入后自动：
- 按章节拆分（`ModuleChapter`）
- 建立场景索引（`SceneIndex`，含起止行号、子节、标签、房间标注）
- 生成检索块和 BGE-M3 Dense 向量（`ModuleChunk`）

---

## 二、场景索引

场景数据存储于 `scene_indexes` 表，可通过以下方式访问：

```powershell
# 列出所有模组和场景
python -m nanobot.dnd.db.cli module index --campaign <id>

# 导出为 scenes_index.json 兼容格式
python -m nanobot.dnd.db.cli module export-scenes --campaign <id> --output scenes.json
```

每个场景包含：标题、起止行号、子节列表（含 `type: "room"` 标注）、关键词标签。

---

## 三、场景切换与进度追踪

场景切换通过 `ModuleProgressService.set_scene()` 执行（由 `dnd_module` 工具的 `set_scene` action 调用）：

1. 验证场景存在于当前激活模组中
2. 检查章节状态（locked 章节不可进入）
3. 更新 `WorldState` 中的当前场景信息
4. 创建/更新 `SceneState`（含 `explored_percent`、`current_room`）
5. 记录 `CampaignEvent` 到审计日志

```python
# 通过工具调用
dnd_module action=set_scene campaign_id=<id> scene_id=<scene_id> [explored_percent=50]
```

---

## 四、章节过渡条件

章节过渡由存档中的 `completedNodes` 驱动。完成当前章节所有关键节点后，DM 根据规则执行：

| 步骤 | 操作 |
|:----:|------|
| 1 | 确认章节结束条件（验证节点完成 + 存档） |
| 2 | `ModuleProgressService.set_scene()` 切换到新章节首场景 |
| 3 | 新章节状态标记为 `current` |
| 4 | 开始新章节叙事 |
| 5 | 存档 |

---

## 五、玩家信息

角色状态 → 当前 `campaign_id` 的 `Party` + `Character` 聚合
世界状态 → 当前 `campaign_id` 的 `WorldState` 聚合
剧情摘要 → 当前 `campaign_id` 的 `PlotSummary` 与 `CampaignEvent` 记录

以上内容在每次对话时动态摘要，不在此硬编码。
