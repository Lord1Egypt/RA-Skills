# 写盘后验证与沉淀教训（2026-06-05 实战）

IMA skill 写盘后**必跑**的 5 个验证动作 + 沉淀到 skill 的工作流教训。

## 写盘后 5 个验证动作

### 1. browse-kb 分页拿全（硬闸 6）

**问题**：`browse-kb` 单次 `Limit` 硬上限 50，传 >50 触发 `code:51`。只看首页 50 条可能跟预期对不上就误报"上传失败"。

**正确姿势**（分页循环）：

```bash
KB_ID="..."  # 替换
SUBFOLDER="folder_..."  # 替换

# 第 1 页
RESP1=$(~/.hermes/skills/ima/bin/ima browse-kb "$KB_ID" "$SUBFOLDER" 2>&1 | tail -1)
TOTAL=$(echo "$RESP1" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['data']['knowledge_list']))")
CURSOR=$(echo "$RESP1" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['next_cursor'])")
IS_END=$(echo "$RESP1" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['is_end'])")

# 后续页循环
PAGE=1
while [ "$IS_END" != "True" ] && [ -n "$CURSOR" ]; do
  PAGE=$((PAGE+1))
  RESP=$(~/.hermes/skills/ima/bin/ima browse-kb "$KB_ID" "$SUBFOLDER" "$CURSOR" 50 2>&1 | tail -1)
  PAGE_LEN=$(echo "$RESP" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['data']['knowledge_list']))")
  CURSOR=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['next_cursor'])")
  IS_END=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['is_end'])")
  TOTAL=$((TOTAL + PAGE_LEN))
done

echo "子文件夹真实文件数 = $TOTAL (is_end=$IS_END, 翻了 $PAGE 页)"
```

### 2. 14 篇新传逐一核验（跟 upload 清点对比）

```python
import json, subprocess
from pathlib import Path

KB_ID = "YOUR_KB_ID"
SUBFOLDER = "YOUR_FOLDER_ID"
IMA = "/home/jerome/.hermes/skills/ima/bin/ima"

def get_all_titles():
    r1 = subprocess.run([IMA, "browse-kb", KB_ID, SUBFOLDER], capture_output=True, text=True, timeout=60)
    j1 = json.loads([l for l in r1.stdout.split("\n") if l.startswith("{")][-1])
    titles = [it["title"] for it in j1["data"]["knowledge_list"]]
    cursor = j1["data"].get("next_cursor", "")
    if cursor and not j1["data"].get("is_end"):
        r2 = subprocess.run([IMA, "browse-kb", KB_ID, SUBFOLDER, cursor, "50"], capture_output=True, text=True, timeout=60)
        j2 = json.loads([l for l in r2.stdout.split("\n") if l.startswith("{")][-1])
        titles += [it["title"] for it in j2["data"].get("knowledge_list", [])]
    return titles

new_14 = [...]  # 你这次上传的 14 篇清单
all_titles = get_all_titles()
missing = [t for t in new_14 if t not in all_titles]
print(f"✅ 核验：{len(new_14)-len(missing)}/{len(new_14)} 入库")
for m in missing: print(f"  ❌ 缺失：{m}")
```

### 3. 重复项检查

```python
from collections import Counter
dups = {t: c for t, c in Counter(all_titles).items() if c > 1}
if dups: print(f"⚠️ 重复：{dups}")
```

### 4. 旧残留识别（6/4 收尾时的 `multi-channel-assistant_zh.md` 是典型）

找出"6/4 收尾时传的旧 slug 文件"——**应该**被 H1 中文重传覆盖，**但** OpenAPI 不支持删除导致它还在。

### 5. obsidian / IMA 双向链接一致性

- vault 端 frontmatter 的 `ima: kb:.../folder:.../<file>.md` 跟 KB 端 `parent_folder_id` + `title` 一致
- vault 文件数（不含 index.md）= KB 子文件夹文件数 - 旧残留

---

## 沉淀到 skill 的工作流教训

### 沉淀前必查（避免重复造轮子）

每次发现新坑想沉淀到 ima skill，**先**：

```bash
# 1. 主 SKILL.md 是否有 vN+1 段
grep -nE "^## v" ~/.hermes/skills/ima/SKILL.md

# 2. api-quirks.md 是否有 vN+1 段
grep -nE "^## v" ~/.hermes/skills/ima/references/api-quirks.md

# 3. hard-gates.md 是否有硬闸 N+1
grep -nE "^## 硬闸 [0-9]" ~/.hermes/skills/ima/references/ima-write-hard-gates.md
```

**有就在原处 patch，没有才新建**。**反模式**（2026-06-05 踩过）：直接加 `api-quirks.md` v14 段，没 grep 主 SKILL.md，结果重复了"分页坑"发现 1。

### 沉淀"硬闸 N+1"判定标准

`ima-write-hard-gates.md` 加新硬闸要满足：

- ✅ **可命令化**（`cat | bash` 能跑）
- ✅ **挡的是可重复错的模式**
- ❌ **不**加"验证姿势"类（这些进 api-quirks.md 的 vN 段）
- ❌ **不**加"概念讲解"类（这些进 SKILL.md 的 5 问段）

### "已中文仓库"硬规则

`*-zh` / `中文` / `cn-` 仓库**整篇就是中文**——**不**走 mmx text chat 翻译（会"把中文翻成中文"造成退化）；走"原文已经是译文"流程（仅做内容质量校验 + H1 名映射 + GATE 3 + upload）。

**判断方法**（3 步，5 秒）：

```bash
# 1. 仓库 README 头部找语言信号
head -10 <repo>/README.md

# 2. 抽 1 个 .md 头 30 行
head -30 <repo>/usecases/<slug>.md
# 中文字符比例 > 80% = 已中文

# 3. 看 H1 是英文还是中文
grep -h "^# " <repo>/usecases/*.md | head -10
```

**真实案例**（2026-06-05）：`AlexAnys/awesome-openclaw-usecases-zh` 50 篇，H1 全是中文。**详见 ima-kb-curation SKILL.md** 的"已中文仓库 vs 英文仓库"段。

---

## 错误码 51 触发场景表

| 端点 | 错误码 51 触发场景 | 来源 |
|---|---|---|
| `list-notebook` / `list-note` | limit=0 / 不传 limit | 旧规则 |
| `browse-kb` | limit > 50（**硬上限 50**）| v14 实战 |
| 其他 browse/list 端点 | 推测同上 | **未验证** |

**含义**：所有 browse/list 类端点的 limit 上限推测都是 50（v14 实战只验过 browse-kb，其他按同样规则处理）。
