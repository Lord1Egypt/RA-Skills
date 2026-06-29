---
name: dnd-campaign-manager
description: Manage D&D campaigns stored in the shared database. Use for creating, listing, selecting, archiving, saving, verifying, loading, or undoing campaigns and complete database snapshots, including campaign-scoped player-role notes synchronized with USER.md.
---

# D&D Campaign Manager

Use the deterministic JSON CLI. Do not compose SQL or call the legacy
`dnd_engine.save.io` file-save functions.

```powershell
python -m <domain-cli> <command>
```

Pass the current workspace with `--workspace <absolute-path>` when
saving, loading, or undoing. This synchronizes only the current campaign's
managed player-role block in `USER.md`; it never replaces the whole file.

## Resolve the campaign first

1. Reuse the campaign ID already established in the current conversation.
2. Otherwise list active campaigns:

   ```powershell
   python -m <domain-cli> campaign list --status active
   ```

3. If exactly one active campaign exists, select it. If multiple exist, ask the
   user which campaign to use. Never infer from save slot numbers.
4. Treat “switch campaign” as selecting another campaign ID for the current
   conversation. This version deliberately has no channel binding.

## Manage campaigns

Create only after the user asks to start a new campaign.

### 开团流程

**Step 1 — 确定模组来源。** 先检查数据库中已有哪些模组：

```
dnd_module action=status
```

然后问用户：使用已有模组，还是导入新模组？

- **使用已有模组**：跳过导入，直接 `dnd_campaign action=start` 并指定 `module_name` 匹配已有模组名。
- **导入新模组**：见下方"导入新模组"。

**Step 2 — 一键开团：**

```
dnd_campaign action=start name="战役名称" module_name="模组名称" [source_path="<path>"]
```

自动完成：创建战役 + 绑定规则 + 初始存档 (slot 1) + 可选导入模组。

### 导入新模组

用户可以提供本地路径，或上传 PDF/Markdown 文件。上传的文件路径出现在对话中为
`[Attachment: <path>]`。

**获取路径的方式：**
1. 用户直接指定：`source_path="D:\Downloads\模组.pdf"`
2. 用户上传文件：从对话中提取 `[Attachment: <完整路径>]` 作为 `source_path`
3. 用户给目录：`source_path="D:\模组文件夹\"`（会扫描目录下所有支持的格式）

**导入：**
```
dnd_module action=import campaign_id=<id> source_path="<path>" module_name="<name>"
dnd_module action=index campaign_id=<id>
dnd_module action=status campaign_id=<id>
```

导入后报告 chapter/scene/chunk/embedding 数量。

### 分步操作（维护后备）

```powershell
python -m <domain-cli> campaign create --name "战役名称" --module "模组名称"
```

**创建战役后必须立即创建初始 Snapshot**，作为第一个恢复点：

```powershell
python -m <domain-cli> save create --campaign <campaign-id> --label "初始状态" --workspace "<workspace>"
```

If a rules corpus is already installed, creation automatically pins the active
core rules release. For a campaign created before rules were indexed, bind it
once before adjudication:

```powershell
python -m <domain-cli> rules bind --campaign <campaign-id>
```

Inspect or archive (also available via `dnd_campaign show` / `set_status`):

```powershell
python -m <domain-cli> campaign show --campaign <campaign-id>
python -m <domain-cli> campaign status --campaign <campaign-id> --set archived
```

Do not save into or load an archived campaign until it is explicitly reactivated.

## Import module content

The campaign `--module` value is only a label. Before using module facts, import the supplied
chapter documents and verify the resulting chapter, scene, chunk, and embedding counts.

**Always check if the module already exists first.** Call `dnd_module action=index` or
`module list` before importing. If the campaign already has the module imported (chapters
and scenes present), use the existing data — **do not re-import or re-parse the source**.
Only import when:
- No module exists for the campaign, OR
- The user explicitly requests a re-import (delete old → import new)

Markdown is read directly; PDF, DOCX, PPTX, XLSX, HTML, and related documents are converted
through MarkItDown before storage and Dense indexing:

```powershell
# Check first
python -m <domain-cli> module list --campaign <campaign-id>

# Only if missing:
python -m <domain-cli> module import `
  --campaign <campaign-id> `
  --name "模组名称" `
  --path "<absolute-module-directory>"
python -m <domain-cli> module index --campaign <campaign-id>
```

Channel attachments are downloaded to local media paths and appear in the turn as
`[Attachment: <path>]`. When the user explicitly identifies an attachment as module source,
**first check `module list`** to see if the module is already imported. If already present,
skip import and report the existing chapter/scene counts. Only call `dnd_module action=import`
when the module is genuinely missing. Do not treat every uploaded document as a module.
The CLI above is the maintenance fallback, not the normal Agent path.

PDF imports use the dedicated structured converter rather than MarkItDown's flat PDF text:
page boundaries and bookmarks are retained, repeated margins are removed, wrapped CJK text is
reflowed, chapter/appendix duplicates from the table of contents are discarded, and room headings
become retrieval boundaries. Reject the import when bookmark coverage is below 95% or no headings
can be recovered. Every stored chunk must retain its source page range.

Never reconstruct a published module from model memory. If source documents are absent, report
that the campaign has only a module label and ask for a lawful local source directory.

Imported module documents, chapter metadata, and scene indexes are static database content.
Snapshots store only mutable progress such as scene state; restoring a snapshot must not delete,
replace, or duplicate imported module content.

Load only the scene required for the current turn, using the scene ID returned by `module index`:

```powershell
python -m <domain-cli> module scene `
  --campaign <campaign-id> `
  --scene <scene-id>
```

For discovery, search the active module with the resident `dnd_module` tool (`action=search`),
which combines lexical and BGE-M3 Dense retrieval. Expand the selected chunk before relying on
the complete scene. Use the CLI only for maintenance:

```powershell
python -m <domain-cli> module search --campaign <campaign-id> `
  --query "<地点、NPC、事件或线索>" --top-k 5
```

## Run module progress

At the start of a campaign turn call `dnd_module action=current`. If no current scene exists,
use `action=index` to select the first unlocked scene, expand it, then persist entry with
`action=set_scene`. During play:

1. `search` locates candidate module facts without loading a chapter.
2. `expand` loads the complete selected scene before narration or adjudication.
3. `set_scene` persists the current scene, room, explored percentage, and confirmed scene facts.
4. Scene entry automatically updates world state, writes audit, and appends a campaign event.
5. A later snapshot captures scene/world/event progress but never duplicates module documents or
   Dense vectors.

Never call `set_scene` for a locked chapter or merely planned player movement.

## Save a complete snapshot

Prefer the native `dnd_save` tool. Use a short label describing the decision point.
Every save creates a new slot; never overwrite an earlier slot. Restore auto-saves
current state before loading. Archived campaigns are rejected.

```
dnd_save action=create campaign_id=<id> label="进入地城前"
dnd_save action=list campaign_id=<id>
dnd_save action=verify campaign_id=<id> slot=1
dnd_save action=restore campaign_id=<id> slot=1 [auto_save=true]
dnd_save action=delete campaign_id=<id> slot=3
dnd_save action=export campaign_id=<id> slot=1 output="save.json"
```

Before a save whose label or surrounding conversation claims that character creation is
complete, run `character list` for the campaign. If an expected character is absent, stop
and persist it using the character-creation procedure; never create a misleading empty save.

The CLI below is the maintenance fallback:

```powershell
python -m <domain-cli> save create `
  --campaign <campaign-id> `
  --label "进入地城前" `
  --workspace "<workspace>"
```

Report the returned campaign ID, slot, label, chapter, location, and hash prefix.

## List and verify saves

```powershell
python -m <domain-cli> save list --campaign <campaign-id>
python -m <domain-cli> save verify --campaign <campaign-id> --slot <slot>
```

Slots are campaign-local. Campaign A slot 1 and Campaign B slot 1 are unrelated.

## Load a save

Loading replaces the selected campaign's current database state. If the user did
not specify a slot, list saves and ask. If they explicitly named a slot, load it
without an extra confirmation.

```powershell
python -m <domain-cli> save load `
  --campaign <campaign-id> `
  --slot <slot> `
  --workspace "<workspace>"
```

The CLI validates the database record, embedded campaign ID, snapshot format,
schema version, and SHA-256 checksum. Never bypass a validation error or retry
against a different campaign. After success, report the restored slot and audit ID.

## Undo

Undo restores the state that existed before the latest audited mutation,
including a snapshot load. Respect the configured audit limit.

```powershell
python -m <domain-cli> undo `
  --campaign <campaign-id> `
  --count 1 `
  --workspace "<workspace>"
```

Do not interpret undo as deleting a save. Snapshot rows remain immutable history.

## USER.md player roles

Maintain only this campaign-scoped block when the user assigns player names to
characters:

```markdown
<!-- dnd-campaign:<campaign-id>:players:start -->
## 战役玩家角色

- 玩家甲：角色甲
- 玩家乙：角色乙
<!-- dnd-campaign:<campaign-id>:players:end -->
```

The save command imports the block into campaign configuration before capturing
the snapshot. Load and undo project the restored value back into the same block.
Never place channel IDs or authentication claims here.

Read [references/database-contract.md](references/database-contract.md) only when
debugging a validation failure, explaining snapshot coverage, or extending the CLI.
