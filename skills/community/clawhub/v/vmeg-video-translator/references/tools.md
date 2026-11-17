# VMEG MCP Tools Overview

This doc describes **what each** `vmeg_*` tool **does** (quick reference).

**How to call** (parameters, polling, confirmation rules) follows **MCP server instructions** injected after connecting — this Skill does not duplicate those details.

Local video/audio must be uploaded first — see [SKILL.md](../SKILL.md) and platform setup docs.

---

## Materials

| Tool | Purpose |
|------|---------|
| `vmeg_list_materials` | List uploaded video/audio in project |
| `vmeg_initiate_material_upload` | Local upload step 1: get S3 presigned PUT URL (OAuth-friendly) |
| `vmeg_complete_material_upload` | Local upload step 2: register after S3 PUT, returns materialId |
| `vmeg_delete_material` | Delete material (requires confirmation) |

## Tasks

| Tool | Purpose |
|------|---------|
| `vmeg_list_tasks` | List or check translation task progress |
| `vmeg_delete_task` | Delete task (requires confirmation) |

## Create translation

| Tool | Purpose |
|------|---------|
| `vmeg_create_video_translation_task` | Create video/audio dubbing translation |
| `vmeg_create_subtitle_translation_task` | Create subtitle translation (preview / merge / export) |

## Voices

| Tool | Purpose |
|------|---------|
| `vmeg_list_basic_voices` | System voice library |
| `vmeg_list_clone_voices` | Your cloned voices |

## Editor · Query

| Tool | Purpose |
|------|---------|
| `vmeg_query_task_scripts` | View translation scripts / lines |
| `vmeg_query_task_subtitles` | View subtitles |
| `vmeg_query_task_asr` | View ASR results |
| `vmeg_query_task_speakers` | View speakers / voice assignments |
| `vmeg_query_task_tracks` | View audio/video tracks |

## Editor · Edit & export

| Tool | Purpose |
|------|---------|
| `vmeg_save_task_draft` | Save edits (lines, subtitles, volume, etc.) |
| `vmeg_compose_task_draft` | Submit final render/export (requires confirmation) |

## Video translation · Async ops

| Tool | Purpose |
|------|---------|
| `vmeg_retranslate_task_scripts` | Retranslate entire task (requires confirmation) |
| `vmeg_get_retranslate_status` | Check retranslation progress |
| `vmeg_trigger_video_translation_all_tts` | Re-dub (requires confirmation) |
| `vmeg_get_tts_status` | Check dubbing progress |

---

## Typical flows (outline)

**New video translation:**

```
Pick material → Create task → Check progress → Optional: edit → Export
```

**Retranslate / re-dub:**

```
Retranslate → Check status → Re-dub → Check status
```

---

## Operations requiring confirmation

These modify or delete data, or may consume quota — Agent should ask first:

- Delete material / task
- Retranslate, re-dub, final render/export
