# 模组运行结构

> 本文件是通用模组弧线参考模板；实际章节与节点状态存储于当前战役数据库。
> 模组导入后由 `ModuleImportService` 自动建立章节结构与场景索引。

---

## 章节加载序列

章节结构由模组导入时自动建立，通过 `ModuleChapter` 表管理：

| 字段 | 说明 |
|------|------|
| `chapter_key` | 章节标识（`ch.1`, `ch.2`, `appendix.a` 等） |
| `status` | `current` / `locked` / `reference` |
| `order_index` | 章节排序 |

切换当前章节通过 `ModuleProgressService.set_scene()` 自动更新章节状态。

---

## 关键节点清单

关键节点由 DM 在运行中通过 `CampaignEvent` 记录，不在本文件硬编码。

---

## 事件流程图

事件由 `CampaignEventService` 管理，存储于 `campaign_events` 表。
每次存档时完整保留。

---

## 等级与升级里程碑

角色等级与经验值存储于 `Character` 表的 `sheet_json` 和 `xp` 字段，
通过 `CharacterService` 管理。

---

## 跨章节NPC命运

NPC 状态由当前 `campaign_id` 的 `WorldState.state_json` 维护。
存档时完整捕获。

---

## 存档剧情快照

通过 `CampaignSnapshotService` 管理。每次存档时调用 `save create`：
```powershell
python -m nanobot.dnd.db.cli save create --campaign <id> --label "<描述>"
```
