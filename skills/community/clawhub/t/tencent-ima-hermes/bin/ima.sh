#!/usr/bin/env bash
# ima — Hermes skill CLI for Tencent IMA OpenAPI
# 严格按原版 ima-skills-1.1.7.zip 的 API 端点一对一映射
# 详见 ~/.hermes/skills/ima/knowledge-base/references/api.md
#      ~/.hermes/skills/ima/notes/references/api.md

set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NODE_SCRIPT="$SKILL_ROOT/ima_api.cjs"

if [[ ! -f "$NODE_SCRIPT" ]]; then
  echo '{"code":-100,"msg":"ima_api.cjs not found"}' >&2
  exit 1
fi

# 加载 ~/.hermes/.env（hermes 启动时会加载，子进程继承）
ENV_FILE="${HERMES_ENV:-$HOME/.hermes/.env}"
[[ -f "$ENV_FILE" ]] && { set -a; source "$ENV_FILE"; set +a; }

sub="$1"; shift || true

# 通用：把 CSV 转 JSON 字符串数组
csv_to_json() {
  awk -F, 'BEGIN{printf "["} {for(i=1;i<=NF;i++) printf "%s\"%s\"", (i>1?",":""), $i} END{printf "]"}' <<< "$1"
}

# 通用：把 CLI 数字参数安全注入到 JSON（只接受整数）
safe_int() { [[ "$1" =~ ^-?[0-9]+$ ]] && echo "$1" || echo 0; }

# 把内容里的双引号/反斜杠/换行转义，注入到 JSON 字符串
json_str() {
  python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$1"
}

case "$sub" in
  # ═══════════════════════════════════════════════════════════════
  # 笔记模块 — 完全对应 openapi/note/v1/*
  # ═══════════════════════════════════════════════════════════════
  list-notebook)
    # openapi/note/v1/list_notebook  cursor + limit(必填)
    api="openapi/note/v1/list_notebook"
    body=$(printf '{"cursor":"%s","limit":%s}' "${1:-0}" "$(safe_int "${2:-50}")")
    ;;
  list-note)
    # openapi/note/v1/list_note  folder_id(可选) + sort_type + cursor + limit
    api="openapi/note/v1/list_note"
    fid=$(json_str "${1:-}")
    body=$(printf '{"folder_id":%s,"sort_type":%s,"cursor":"%s","limit":%s}' \
      "$fid" "$(safe_int "${2:-1}")" "${3:-}" "$(safe_int "${4:-50}")")
    ;;
  search-note)
    # openapi/note/v1/search_note  真实字段（按 references/api.md §SearchNoteReq）：
    #   search_type: 0=标题(默认) 1=正文
    #   sort_type:   0=修改时间(默认)
    #   query_info:  { title?: string, content?: string }  ← 注意不是 query
    #   start:       int64 (必填)  翻页起始
    #   end:         int64 (必填)  翻页终止，end-start ≤ 20
    api="openapi/note/v1/search_note"
    q=$(json_str "${1:-}")
    # 全部按默认搜索类型（标题）；start=0, end=20 拿首屏
    body=$(printf '{"search_type":0,"sort_type":0,"query_info":{"title":%s},"start":0,"end":20}' "$q")
    ;;
  get-doc)
    # openapi/note/v1/get_doc_content  note_id + target_content_format(必填)
    api="openapi/note/v1/get_doc_content"
    nid=$(json_str "${1:-}")
    fmt=$(safe_int "${2:-0}")
    body=$(printf '{"note_id":%s,"target_content_format":%s}' "$nid" "$fmt")
    ;;
  new-doc)
    # openapi/note/v1/import_doc  content + content_format(必填=1) + folder_id(可选) + title(可选)
    api="openapi/note/v1/import_doc"
    content=$(json_str "${1:-}")
    fid=$(json_str "${2:-}")
    title=$(json_str "${3:-}")
    body=$(printf '{"content":%s,"content_format":1,"folder_id":%s,"title":%s}' \
      "$content" "$fid" "$title")
    ;;
  append-doc)
    # openapi/note/v1/append_doc  note_id + content + content_format(必填=1)
    api="openapi/note/v1/append_doc"
    nid=$(json_str "${1:-}")
    content=$(json_str "${2:-}")
    body=$(printf '{"note_id":%s,"content":%s,"content_format":1}' "$nid" "$content")
    ;;

  # ═══════════════════════════════════════════════════════════════
  # 知识库模块 — 完全对应 openapi/wiki/v1/*
  # ═══════════════════════════════════════════════════════════════
  list-kb)
    # openapi/wiki/v1/search_knowledge_base  query(可选) + cursor + limit
    api="openapi/wiki/v1/search_knowledge_base"
    q=$(json_str "${1:-}")
    body=$(printf '{"query":%s,"cursor":"%s","limit":%s}' "$q" "${2:-}" "$(safe_int "${3:-20}")")
    ;;
  addable-kb)
    # openapi/wiki/v1/get_addable_knowledge_base_list  cursor + limit
    api="openapi/wiki/v1/get_addable_knowledge_base_list"
    body=$(printf '{"cursor":"%s","limit":%s}' "${1:-0}" "$(safe_int "${2:-50}")")
    ;;
  get-kb)
    # openapi/wiki/v1/get_knowledge_base  ids[](1-20)
    api="openapi/wiki/v1/get_knowledge_base"
    ids=$(csv_to_json "${1:-}")
    body=$(printf '{"ids":%s}' "$ids")
    ;;
  browse-kb)
    # openapi/wiki/v1/get_knowledge_list  knowledge_base_id + folder_id(可选) + cursor + limit
    api="openapi/wiki/v1/get_knowledge_list"
    kbid=$(json_str "${1:-}")
    fid=$(json_str "${2:-}")
    body=$(printf '{"knowledge_base_id":%s,"folder_id":%s,"cursor":"%s","limit":%s}' \
      "$kbid" "$fid" "${3:-0}" "$(safe_int "${4:-50}")")
    ;;
  search-kb)
    # openapi/wiki/v1/search_knowledge  knowledge_base_id + query + cursor + limit
    api="openapi/wiki/v1/search_knowledge"
    kbid=$(json_str "${1:-}")
    q=$(json_str "${2:-}")
    body=$(printf '{"knowledge_base_id":%s,"query":%s,"cursor":"%s","limit":%s}' \
      "$kbid" "$q" "${3:-}" "$(safe_int "${4:-10}")")
    ;;
  add-url)
    # openapi/wiki/v1/import_urls  knowledge_base_id + urls[](1-10) + folder_id(可选)
    api="openapi/wiki/v1/import_urls"
    kbid=$(json_str "${1:-}")
    urls=$(csv_to_json "${2:-}")
    fid=$(json_str "${3:-}")
    body=$(printf '{"knowledge_base_id":%s,"urls":%s,"folder_id":%s}' "$kbid" "$urls" "$fid")
    ;;
  get-media)
    # openapi/wiki/v1/get_media_info  media_id
    # 字段实测：media_id（不是 id、不是 MediaId 首字母大写）
    # 错误信息 "GetMediaInfoReq.MediaId" 是腾讯内部 proto 字段名，CLI 序列化时要全小写
    api="openapi/wiki/v1/get_media_info"
    mid=$(json_str "${1:-}")
    body=$(printf '{"media_id":%s}' "$mid")
    ;;
  check-name)
    # openapi/wiki/v1/check_repeated_names  knowledge_base_id + folder_id(可选) + params[]
    # 原 SKILL.md: params 元素 {name, media_type}，最多 2000
    # CLI: check-name <kb_id> <name> <media_type> [folder_id]
    api="openapi/wiki/v1/check_repeated_names"
    kbid=$(json_str "${1:-}")
    name=$(json_str "${2:-}")
    mt=$(safe_int "${3:-1}")
    fid=$(json_str "${4:-}")
    if [[ -n "${4:-}" ]]; then
      body=$(printf '{"knowledge_base_id":%s,"folder_id":%s,"params":[{"name":%s,"media_type":%s}]}' \
        "$kbid" "$fid" "$name" "$mt")
    else
      body=$(printf '{"knowledge_base_id":%s,"params":[{"name":%s,"media_type":%s}]}' \
        "$kbid" "$name" "$mt")
    fi
    ;;
  create-media)
    # openapi/wiki/v1/create_media  file_name + file_size + content_type + knowledge_base_id + file_ext
    # CLI: create-media <kb_id> <file_name> <file_size> <file_ext> [content_type]
    api="openapi/wiki/v1/create_media"
    kbid=$(json_str "${1:-}")
    fname=$(json_str "${2:-}")
    fsize=$(safe_int "${3:-0}")
    fext=$(json_str "${4:-}")
    ct=$(json_str "${5:-application/octet-stream}")
    body=$(printf '{"file_name":%s,"file_size":%s,"content_type":%s,"knowledge_base_id":%s,"file_ext":%s}' \
      "$fname" "$fsize" "$ct" "$kbid" "$fext")
    ;;
  add-knowledge)
    # openapi/wiki/v1/add_knowledge
    # - 文件入知识库: media_type + media_id + title + knowledge_base_id + file_info
    # - 笔记入知识库: media_type=11 + note_info.content_id + title + knowledge_base_id
    # CLI 提供两种模式：
    #   模式 A（文件）: add-knowledge <kb_id> <media_id> <title> <media_type> <file_name> <file_size>
    #   模式 B（笔记）: add-knowledge --note <kb_id> <note_id> <title>
    api="openapi/wiki/v1/add_knowledge"
    if [[ "${1:-}" == "--note" ]]; then
      kbid=$(json_str "${2:-}")
      nid=$(json_str "${3:-}")
      title=$(json_str "${4:-}")
      body=$(printf '{"media_type":11,"note_info":{"content_id":%s},"title":%s,"knowledge_base_id":%s}' \
        "$nid" "$title" "$kbid")
    else
      kbid=$(json_str "${1:-}")
      mid=$(json_str "${2:-}")
      title=$(json_str "${3:-}")
      mt=$(safe_int "${4:-1}")
      fname=$(json_str "${5:-$3}")
      fsize=$(safe_int "${6:-0}")
      body=$(printf '{"media_type":%s,"media_id":%s,"title":%s,"knowledge_base_id":%s,"file_info":{"cos_key":"","file_size":%s,"file_name":%s}}' \
        "$mt" "$mid" "$title" "$kbid" "$fsize" "$fname")
    fi
    ;;

  # ═══════════════════════════════════════════════════════════════
  # 未文档化但真实存在的端点（经探针验证）：
  #   - openapi/wiki/v1/create_folder         （原版 SKILL.md 未列）
  #   - openapi/wiki/v1/create_knowledge_base  （原版 SKILL.md 未列）
  #   - openapi/wiki/v1/move_knowledge        （原版 SKILL.md 未列）
  #   - openapi/note/v1/add_notebook          （原版 SKILL.md 未列）
  #   - openapi/note/v1/rename_notebook       （原版 SKILL.md 未列）
  # 字段结构按探针实际响应反推，未经腾讯官方文档背书；后续若腾讯
  # 调整字段名，update 这五个 case 即可。
  # ═══════════════════════════════════════════════════════════════
  create-folder)
    # openapi/wiki/v1/create_folder  knowledge_base_id + name [+ folder_id]
    # 探针验证: 返回 { code:0, data:{ media_id:"folder_..." } }
    # 实测 2026-06-04：字段 knowledge_base_id 对（kb_id 会报 51 "value length must be at least 1 runes"）
    # 实测 2026-06-04 v8 探针：父目录字段名是 folder_id（不是 parent_folder_id / parent_id / dst_folder_id）
    # 副作用：默认 parent=KB 根；指定第 3 参数 folder_id 可建在任意子目录下
    # 用法: ima create-folder <kb_id> <name> [parent_folder_id]
    api="openapi/wiki/v1/create_folder"
    kbid=$(json_str "${1:-}")
    name=$(json_str "${2:-}")
    parent=$(json_str "${3:-}")
    if [ -n "${3:-}" ]; then
      body=$(printf '{"knowledge_base_id":%s,"name":%s,"folder_id":%s}' "$kbid" "$name" "$parent")
    else
      body=$(printf '{"knowledge_base_id":%s,"name":%s}' "$kbid" "$name")
    fi
    ;;
  create-kb)
    # openapi/wiki/v1/create_knowledge_base  type + name
    # type 枚举: "KBT_MINE_KB"（个人知识库）| "KBT_SHARED_KB"（共享知识库）
    # 探针验证: 返回 { code:0, data:{ id, name } }
    # 实测 2026-06-04：type=KBT_MINE_KB 真创建，name 入 list-kb 第一项
    api="openapi/wiki/v1/create_knowledge_base"
    type_v=$(json_str "${1:-KBT_MINE_KB}")
    name=$(json_str "${2:-}")
    body=$(printf '{"type":%s,"name":%s}' "$type_v" "$name")
    ;;
  move-kb-item)
    # openapi/wiki/v1/move_knowledge  src_knowledge_base_id + media_id + dst_knowledge_base_id + dst_folder_id
    # 探针验证: 端点存在，body 接受，code:0 返回 move_results: {}
    # 实测 2026-06-04：3 种场景全无效 —
    #   (a) KB 内文件夹间移动 file/folder  → code:0 但文件位置不变
    #   (b) 跨 KB 移动 file                → code:0 但文件位置不变
    #   (c) 跨 KB 移动 + dst_folder_id     → code:0 但文件位置不变
    # 结论：端点存在但**不实现"移动文件"语义**。可能是腾讯内部占位/未实现。
    #     OpenAPI 整体不开放 KB 内文件夹移动能力 → 走 ima 客户端 UI
    api="openapi/wiki/v1/move_knowledge"
    src=$(json_str "${1:-}")
    mid=$(json_str "${2:-}")
    dst=$(json_str "${3:-}")
    dfid=$(json_str "${4:-}")
    body=$(printf '{"src_knowledge_base_id":%s,"media_id":%s,"dst_knowledge_base_id":%s,"dst_folder_id":%s}' \
      "$src" "$mid" "$dst" "$dfid")
    ;;
  create-notebook)
    # openapi/note/v1/add_notebook  folder_name
    # ⚠️ 字段名是 folder_name（不是 name / title / notebook_name）
    # 探针验证: 返回 { code:0, data:{ folder_id, folder_name } }
    api="openapi/note/v1/add_notebook"
    fname=$(json_str "${1:-}")
    body=$(printf '{"folder_name":%s}' "$fname")
    ;;
  rename-notebook)
    # openapi/note/v1/rename_notebook  folder_id + folder_name
    # 探针验证: 端点存在；2026-06-04 早期返回 310001 "folder not owner"
    # 实测 2026-06-04：现在返回 code:0 + data:{}（改名"成功"），但 list-notebook 实际**未生效**
    # 真实行为: 改名任意 → 100030 "名称已被占用"（即便是新笔记本 + 全新名）
    # 结论：腾讯对系统默认笔记本 (folder_type=0) 不允许改名；用户自建笔记本改名也频繁冲突
    #     OpenAPI 整体不开放稳定的改名能力 → 走 ima 客户端 UI
    api="openapi/note/v1/rename_notebook"
    fid=$(json_str "${1:-}")
    fname=$(json_str "${2:-}")
    body=$(printf '{"folder_id":%s,"folder_name":%s}' "$fid" "$fname")
    ;;
  rename-note)
    # openapi/note/v1/rename_note  note_id + title
    # 探针 v8 (2026-06-04) 发现：端点真存在，code:0 success
    # 字段实测：
    #   {note_id, title}           → code:0 success ✅（已通过 search-note 验证标题真改了）
    #   {note_id, new_title}       → code:210001 "noteId or title is empty"
    #   {note_id, name}            → code:210001 "noteId or title is empty"
    # 错误信息命名是 camelCase (noteId/title) 但 body 实际用 snake_case
    # 用法: ima rename-note <note_id> <new_title>
    api="openapi/note/v1/rename_note"
    nid=$(json_str "${1:-}")
    ntitle=$(json_str "${2:-}")
    body=$(printf '{"note_id":%s,"title":%s}' "$nid" "$ntitle")
    ;;

  # ═══════════════════════════════════════════════════════════════
  # 便利封装 — 不发明接口，只是把多步流水线合成一个调用
  # 内部严格按 SKILL.md 章节顺序：preflight → check → create_media → cos-upload → add
  # ═══════════════════════════════════════════════════════════════
  upload-file)
    # 把"上传文件到知识库"的四步流水线合成一条命令
    # 用法: ima upload-file <kb_id> <file_path> [folder_id] [--force]
    #  --force: 遇到同名文件时不询问，自动加时间戳后缀保留两者
    kbid=""
    fpath=""
    fid=""
    force="false"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --force) force="true"; shift ;;
        --kb=*) kbid="${1#--kb=}"; shift ;;
        --folder=*) fid="${1#--folder=}"; shift ;;
        *)
          if [[ -z "$kbid" ]]; then kbid="$1"; shift
          elif [[ -z "$fpath" ]]; then fpath="$1"; shift
          elif [[ -z "$fid" ]]; then fid="$1"; shift
          else shift
          fi
          ;;
      esac
    done
    if [[ -z "$kbid" || -z "$fpath" ]]; then
      echo '{"code":-100,"msg":"usage: ima upload-file <kb_id> <file_path> [folder_id] [--force]"}' >&2; exit 1
    fi
    if [[ ! -f "$fpath" ]]; then
      echo "{\"code\":-100,\"msg\":\"file not found: $fpath\"}" >&2; exit 1
    fi

    # ── GATE 1: preflight-check
    PREFLIGHT_JSON=$(node "$SKILL_ROOT/knowledge-base/scripts/preflight-check.cjs" \
      --file "$fpath" 2>/dev/null || echo '{"pass":false}')
    PASS=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print('true' if d.get('pass') else 'false')" "$PREFLIGHT_JSON")
    if [[ "$PASS" != "true" ]]; then
      REASON=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print(d.get('reason','preflight failed'))" "$PREFLIGHT_JSON")
      echo "{\"code\":-100,\"msg\":\"GATE 1 failed: $REASON\"}" >&2
      exit 1
    fi
    FNAME=$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['file_name'])" "$PREFLIGHT_JSON")
    FEXT=$(python3  -c "import json,sys; print(json.loads(sys.argv[1])['file_ext'])"   "$PREFLIGHT_JSON")
    FSIZE=$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['file_size'])" "$PREFLIGHT_JSON")
    MTYPE=$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['media_type'])" "$PREFLIGHT_JSON")
    CTYPE=$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['content_type'])" "$PREFLIGHT_JSON")
    echo "✓ preflight pass: $FNAME ($FSIZE bytes, media_type=$MTYPE)"

    # ── GATE 3: check_repeated_names
    CHECK_BODY=$(printf '{"knowledge_base_id":%s,"folder_id":%s,"params":[{"name":%s,"media_type":%s}]}' \
      "$(python3 -c "import json; print(json.dumps('$kbid'))")" \
      "$(python3 -c "import json; print(json.dumps('$fid'))")" \
      "$(python3 -c "import json; print(json.dumps('$FNAME'))")" \
      "$MTYPE")
    CHECK_RESP=$(node "$NODE_SCRIPT" "openapi/wiki/v1/check_repeated_names" "$CHECK_BODY" "{}")
    IS_REPEATED=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); r=d.get('data',{}).get('results') or d.get('data',{}).get('params') or []; print('true' if (r and r[0].get('is_repeated')) else 'false')" "$CHECK_RESP")
    if [[ "$IS_REPEATED" == "true" ]]; then
      if [[ "$force" != "true" ]]; then
        echo '{"code":-100,"msg":"GATE 3: 同名文件已存在。请加 --force 自动加时间戳后缀保留两者，或手动改名。"}' >&2
        exit 1
      fi
      # 加时间戳后缀
      TS=$(date +%Y%m%d%H%M%S)
      base="${FNAME%.*}"; ext="${FNAME##*.}"
      FNAME="${base}_${TS}.${ext}"
      FEXT="$ext"
      echo "⚠ 同名文件，已加时间戳: $FNAME"
    fi

    # ── GATE create_media
    CREATE_BODY=$(printf '{"file_name":%s,"file_size":%s,"content_type":%s,"knowledge_base_id":%s,"file_ext":%s}' \
      "$(python3 -c "import json; print(json.dumps('$FNAME'))")" \
      "$FSIZE" \
      "$(python3 -c "import json; print(json.dumps('$CTYPE'))")" \
      "$(python3 -c "import json; print(json.dumps('$kbid'))")" \
      "$(python3 -c "import json; print(json.dumps('$FEXT'))")")
    CREATE_RESP=$(node "$NODE_SCRIPT" "openapi/wiki/v1/create_media" "$CREATE_BODY" "{}")
    # ⚠️ 注意：create_media 响应里 cos 相关字段全部嵌套在 data.cos_credential.*
    # 顶层只有 media_id；cos_key/secret_id/secret_key/token/bucket_name/region/
    # start_time/expired_time 都在 data.cos_credential.<字段>
    MEDIA_ID=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('media_id',''))" "$CREATE_RESP")
    CC=$(printf '%s' "$CREATE_RESP")
    COS_KEY=$(python3    -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('cos_key',''))" "$CC")
    COS_BUCKET=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('bucket_name',''))" "$CC")
    COS_REGION=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('region',''))" "$CC")
    COS_SID=$(python3    -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('secret_id',''))" "$CC")
    COS_SKEY=$(python3   -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('secret_key',''))" "$CC")
    COS_TOK=$(python3    -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('token',''))" "$CC")
    COS_ST=$(python3     -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('start_time',''))" "$CC")
    COS_ET=$(python3     -c "import json,sys; d=json.loads(sys.argv[1]); print((d.get('data') or {}).get('cos_credential',{}).get('expired_time',''))" "$CC")
    if [[ -z "$MEDIA_ID" ]]; then
      echo "{\"code\":-100,\"msg\":\"create_media failed: $CREATE_RESP\"}" >&2; exit 1
    fi
    echo "✓ create_media: media_id=$MEDIA_ID, cos_key=${COS_KEY:0:40}..."

    # ── GATE 5: cos-upload
    UPLOAD_EXIT=0
    node "$SKILL_ROOT/knowledge-base/scripts/cos-upload.cjs" \
      --file "$fpath" \
      --secret-id "$COS_SID" \
      --secret-key "$COS_SKEY" \
      --token "$COS_TOK" \
      --bucket "$COS_BUCKET" \
      --region "$COS_REGION" \
      --cos-key "$COS_KEY" \
      --content-type "$CTYPE" \
      --start-time "$COS_ST" \
      --expired-time "$COS_ET" \
      --timeout 300000 || UPLOAD_EXIT=$?
    if [[ $UPLOAD_EXIT -ne 0 ]]; then
      echo "{\"code\":-100,\"msg\":\"GATE 5: COS upload failed (exit $UPLOAD_EXIT). STOP, do NOT add_knowledge.\"}" >&2
      exit $UPLOAD_EXIT
    fi
    echo "✓ cos-upload done"

    # ── GATE 2: add_knowledge (title 必须 = file_name)
    # 2026-06-04 fix: 传入 $fid（CLI 第 3 参数 folder_id）→ 落到指定子文件夹。
    #   历史 bug: body 没有 folder_id 字段，CLI 接受参数但 add_knowledge 永远落 KB 根。
    #   命名空间遵循 create_folder v9 探针结论：纯数字 (e.g. YOUR_TARGET_FOLDER_ID)，不要 folder_ 前缀。
    #   空字符串表示不指定（落 KB 根，保持原行为）。
    if [[ -n "$fid" ]]; then
      ADD_BODY=$(printf '{"media_type":%s,"media_id":%s,"title":%s,"knowledge_base_id":%s,"folder_id":%s,"file_info":{"cos_key":%s,"file_size":%s,"file_name":%s}}' \
        "$MTYPE" \
        "$(python3 -c "import json; print(json.dumps('$MEDIA_ID'))")" \
        "$(python3 -c "import json; print(json.dumps('$FNAME'))")" \
        "$(python3 -c "import json; print(json.dumps('$kbid'))")" \
        "$(python3 -c "import json; print(json.dumps('$fid'))")" \
        "$(python3 -c "import json; print(json.dumps('$COS_KEY'))")" \
        "$FSIZE" \
        "$(python3 -c "import json; print(json.dumps('$FNAME'))")")
    else
      ADD_BODY=$(printf '{"media_type":%s,"media_id":%s,"title":%s,"knowledge_base_id":%s,"file_info":{"cos_key":%s,"file_size":%s,"file_name":%s}}' \
        "$MTYPE" \
        "$(python3 -c "import json; print(json.dumps('$MEDIA_ID'))")" \
        "$(python3 -c "import json; print(json.dumps('$FNAME'))")" \
        "$(python3 -c "import json; print(json.dumps('$kbid'))")" \
        "$(python3 -c "import json; print(json.dumps('$COS_KEY'))")" \
        "$FSIZE" \
        "$(python3 -c "import json; print(json.dumps('$FNAME'))")")
    fi
    exec node "$NODE_SCRIPT" "openapi/wiki/v1/add_knowledge" "$ADD_BODY" "{}"
    ;;

  # ═══════════════════════════════════════════════════════════════
  # 元信息
  # ═══════════════════════════════════════════════════════════════
  -h|--help|help|"")
    cat <<'USAGE'
ima — Hermes skill CLI for Tencent IMA OpenAPI
严格对应 ima-skills-1.1.7.zip 的 16 个 API 端点 + 5 个未文档化但真实存在的端点

笔记 (openapi/note/v1/*)
  ima list-notebook [cursor] [limit]
  ima list-note [folder_id] [sort_type] [cursor] [limit]
  ima search-note <query> [limit]
  ima get-doc <note_id> [format]            # format 0=text
  ima new-doc <content> [folder_id] [title]
  ima append-doc <note_id> <content>
  # 未文档化但真实存在（探针验证）
  ima create-notebook <folder_name>         # 字段名是 folder_name
  ima rename-notebook <folder_id> <new_folder_name>
  ima rename-note <note_id> <new_title>            # 探针 v8 发现：真存在 + 真生效

知识库 (openapi/wiki/v1/*)
  ima list-kb [query] [cursor] [limit]              # search_knowledge_base
  ima addable-kb [cursor] [limit]                   # get_addable_knowledge_base_list
  ima get-kb <id1,id2,...>                          # get_knowledge_base
  ima browse-kb <kb_id> [folder_id] [cursor] [limit]# get_knowledge_list
  ima search-kb <kb_id> <query> [cursor] [limit]    # search_knowledge
  ima add-url <kb_id> <url1,url2,...> [folder_id]   # import_urls
  ima get-media <media_id>                          # get_media_info
  ima check-name <kb_id> <name> <media_type> [folder_id]  # check_repeated_names
  ima create-media <kb_id> <file_name> <size> <file_ext> [content_type]  # create_media
  ima add-knowledge <kb_id> <media_id> <title> <media_type> <file_name> <file_size>
  ima add-knowledge --note <kb_id> <note_id> <title>
  # 未文档化但真实存在（探针验证）
  ima create-folder <kb_id> <name> [parent_folder_id]  # create_folder
                                            # 第 3 参数可选，指定 folder_id 建在子目录
  ima create-kb <type> <name>                       # create_knowledge_base，type: KBT_MINE_KB | KBT_SHARED_KB
  ima move-kb-item <src_kb> <media_id> <dst_kb> [dst_folder_id]  # move_knowledge

便利封装（不发明接口，串多个原版 API）
  ima upload-file <kb_id> <file_path> [folder_id] [--force]
    # 严格按 SKILL.md 写入类工作流：
    #   preflight → check_repeated_names → create_media → cos-upload → add_knowledge

凭证
  从 ~/.hermes/.env 自动加载 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY

关于未文档化端点
  5 个新增子命令对应的端点未经腾讯官方 SKILL.md / api.md 文档化，
  是通过主动探针（POST 21+ 候选端点，观察 RAW 响应长度）发现的。
  字段结构按探针实际响应反推。腾讯可能后续调整字段名。
USAGE
    exit 0
    ;;

  *)
    echo "{\"code\":-100,\"msg\":\"unknown subcommand: $sub. Run ima --help for usage.\"}" >&2
    exit 1
    ;;
esac

# 默认 options
options="{}"
for arg in "$@"; do
  [[ "$arg" == "--force-update-check" ]] && options='{"forceCheck":true}'
done

exec node "$NODE_SCRIPT" "$api" "$body" "$options"
