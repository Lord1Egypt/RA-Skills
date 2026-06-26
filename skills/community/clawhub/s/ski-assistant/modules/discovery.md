# Module 5A: Resort Discovery & DB Update — 雪场发现

**触发词**：发现新雪场、添加雪场、update-db、同步数据库、discover, add resort, update database

---

## 发现新雪场

调用：`python3 tools/resort_discovery.py discover '{"region":"中国","enrich":true,"merge":false}'`

**region 可选值**：中国、日本、韩国、欧洲、北美 等，或具体区域如 "中国-崇礼"、"日本-北海道西"。共 65 个预定义区域，覆盖 27 国。

**参数说明**：
- `enrich: true` → 自动通过 Open-Meteo 补充海拔数据
- `merge: true` → 自动合并到 `data/resorts_db.json`（标记 `_needs_review: true`）
- 默认 `merge: false`，仅预览

**数据源**：Overpass API（首选）→ Nominatim（降级）。票价/雪道数/特色等商业信息需人工补充。

## 更新数据库

调用：`python3 tools/resort_discovery.py update-db`

从 GitHub 拉取最新 `resorts_db.json`，自动备份（.bak），对比版本后覆盖。

## MUST 步骤（不可跳过，跳过须告知用户原因）

### 发现新雪场

1. 确认用户意图（发现哪个区域的雪场）
2. 运行 `python3 tools/resort_discovery.py discover '{"region":"<区域>","enrich":true,"merge":<merge值>}'`。默认 `merge: false`（仅预览），如用户要求"发现并合并"或"自动合并"，则设 `merge: true`
3. 输出结果摘要（必须包含下方"输出格式 - 场景 A"的全部字段）
4. 如用户指定了 `merge: true`，提醒用户新雪场标记了 `_needs_review: true`，建议人工校验

### 更新数据库

1. 运行 `python3 tools/resort_discovery.py update-db`
2. 输出更新结果（必须包含下方"输出格式 - 场景 B"的全部字段）
3. 告知用户备份文件位置（.bak）

## 输出格式

### 场景 A：发现新雪场

必须包含以下三部分，顺序不可变：

**1. 发现结果摘要**

| 指标 | 数量 |
|------|------|
| 总计找到 | X 个滑雪区域 |
| 已存在（匹配） | Y 个 |
| 新发现 | Z 个 |
| 错误 | N 个（如无则写 0） |

**2. 新发现雪场列表**（仅当 Z > 0 时输出，如为 0 则说明"未发现新雪场"）

| 名称 | 区域 | 坐标 | 来源 |
|------|------|------|------|
| ... | ... | lat, lon | Overpass/Nominatim |

**3. 后续建议**
- 如新发现雪场 > 0：建议用户说"补充详细信息"来人工校验票价、雪道数等
- 如 merge=true：提醒"新雪场已标记 _needs_review: true，建议人工校验后移除标记"

### 场景 B：更新数据库

必须包含以下三部分，顺序不可变。如任一项因信息不足无法提供，必须说明原因，不可省略不告知。

**1. 更新结果**
- 当前版本：`<旧版本号>` → 新版本：`<新版本号>`
- 雪场数量变化：`<旧数量>` → `<新数量>`（+/- X 个）

**2. 备份位置**
- 备份文件：`data/resorts_db.json.bak`（可通过 git diff 查看差异）

**3. 校验建议**
- 如数量变化 > 50：建议运行 `python3 tools/resort_discovery.py discover` 检查数据一致性
- 如数量变化异常（减少 > 10%）：提醒用户可能是数据源问题，建议核实

## MAY

- 对新发现雪场补充详细信息（票价、雪道数、特色等）
- 批量校验合并后的数据一致性
