#!/usr/bin/env bash
# onedrive-files.sh — OneDrive file & folder operations via Microsoft Graph
#
# Usage: onedrive-files.sh <command> [args]
# Run without args to print full help.

set -euo pipefail

CONFIG_DIR="${ONEDRIVE_MCP_CONFIG_DIR:-$HOME/.onedrive-mcp}"
CREDS_FILE="$CONFIG_DIR/credentials.json"
GRAPH="${ONEDRIVE_GRAPH_BASE:-https://graph.microsoft.com/v1.0}"
DRIVE_PREFIX="${ONEDRIVE_DRIVE_PREFIX:-/me/drive}"  # override to e.g. /drives/{id} or /sites/{id}/drive

get_token() {
    if [ -n "${ONEDRIVE_ACCESS_TOKEN:-}" ]; then echo "$ONEDRIVE_ACCESS_TOKEN"; return; fi
    [ -f "$CREDS_FILE" ] || { echo "Error: no token. Run onedrive-setup.sh or set ONEDRIVE_ACCESS_TOKEN" >&2; exit 1; }
    local t; t=$(jq -r '.access_token // empty' "$CREDS_FILE")
    [ -n "$t" ] || { echo "Error: empty access_token in $CREDS_FILE" >&2; exit 1; }
    echo "$t"
}

# URL-encode a string segment (paths)
url_encode_path() {
    # Encode each path segment but keep '/' separators
    python3 -c '
import sys, urllib.parse
p = sys.argv[1].strip("/")
print("/".join(urllib.parse.quote(seg, safe="") for seg in p.split("/")))
' "$1" 2>/dev/null || echo "$1"
}

# Build a Graph URL for an item by path or by ID.
# Input: either "01ABC..." (id) or "Documents/Reports/q4.xlsx" (path)
# Optional suffix: ":/content", "/children", "/createUploadSession", etc.
item_url() {
    local target="$1" suffix="${2:-}"
    if [[ "$target" =~ ^[A-Za-z0-9!_-]{8,}$ ]] && [[ "$target" != */* ]]; then
        # Treat as item ID
        echo "$GRAPH$DRIVE_PREFIX/items/$target$suffix"
    else
        # Treat as path
        local enc
        enc=$(url_encode_path "$target")
        if [ -z "$suffix" ]; then
            echo "$GRAPH$DRIVE_PREFIX/root:/$enc"
        else
            echo "$GRAPH$DRIVE_PREFIX/root:/$enc:$suffix"
        fi
    fi
}

# Resolve a path-or-id input to a full item ID
resolve_id() {
    local target="$1"
    if [[ "$target" =~ ^[A-Za-z0-9!_-]{8,}$ ]] && [[ "$target" != */* ]]; then
        echo "$target"; return
    fi
    local token; token=$(get_token)
    local url; url=$(item_url "$target")
    curl -fsS -H "Authorization: Bearer $token" "$url?\$select=id" | jq -r '.id'
}

graph_get() {
    local path="$1"
    local token; token=$(get_token)
    curl -fsS "$GRAPH$path" -H "Authorization: Bearer $token"
}

# ===== Commands =====

cmd_list() {
    # list [path]
    local path="${1:-}"
    local url
    if [ -z "$path" ]; then
        url="$GRAPH$DRIVE_PREFIX/root/children"
    else
        url=$(item_url "$path" "/children")
    fi
    url="$url?\$top=200&\$select=id,name,size,folder,file,lastModifiedDateTime,webUrl,parentReference"
    local token; token=$(get_token)
    curl -fsS "$url" -H "Authorization: Bearer $token" \
      | jq '.value[] | {
            kind: (if .folder then "dir" else "file" end),
            name,
            size,
            modified: .lastModifiedDateTime,
            id,
            mime: .file.mimeType,
            children: .folder.childCount
        }'
}

cmd_list_id() {
    local id="${1:?usage: list-id <item-id>}"
    local token; token=$(get_token)
    curl -fsS "$GRAPH$DRIVE_PREFIX/items/$id/children?\$top=200" \
        -H "Authorization: Bearer $token" \
      | jq '.value[] | {kind:(if .folder then "dir" else "file" end), name, size, id}'
}

cmd_list_special() {
    local name="${1:?usage: list-special <documents|photos|cameraroll|approot|music>}"
    local token; token=$(get_token)
    curl -fsS "$GRAPH$DRIVE_PREFIX/special/$name/children?\$top=200" \
        -H "Authorization: Bearer $token" \
      | jq '.value[] | {kind:(if .folder then "dir" else "file" end), name, size, id}'
}

cmd_recent() {
    local top="${1:-25}"
    local token; token=$(get_token)
    curl -fsS "$GRAPH$DRIVE_PREFIX/recent?\$top=$top" \
        -H "Authorization: Bearer $token" \
      | jq '.value[] | {name, size, modified: .lastModifiedDateTime, id, parent: .parentReference.path}'
}

cmd_shared() {
    local top="${1:-25}"
    local token; token=$(get_token)
    curl -fsS "$GRAPH$DRIVE_PREFIX/sharedWithMe?\$top=$top" \
        -H "Authorization: Bearer $token" \
      | jq '.value[] | {name, size, owner: .remoteItem.shared.owner.user.displayName, id: .remoteItem.id, driveId: .remoteItem.parentReference.driveId, url: .webUrl}'
}

cmd_info() {
    local target="${1:?usage: info <path-or-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target")
    curl -fsS "$url" -H "Authorization: Bearer $token" | jq
}

cmd_stat() {
    local target="${1:?usage: stat <path-or-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target")
    curl -fsS "$url?\$select=id,name,size,file,folder,createdDateTime,lastModifiedDateTime" \
        -H "Authorization: Bearer $token" \
      | jq '{name, size, mime: .file.mimeType, created: .createdDateTime, modified: .lastModifiedDateTime, id}'
}

cmd_thumbnail() {
    # thumbnail <id-or-path> [small|medium|large]
    local target="${1:?usage: thumbnail <path-or-id> [size]}"
    local size="${2:-medium}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/thumbnails")
    curl -fsS "$url" -H "Authorization: Bearer $token" \
      | jq --arg size "$size" '.value[0][$size] // .value[0]'
}

cmd_preview() {
    local target="${1:?usage: preview <path-or-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/preview")
    curl -fsS -X POST "$url" -H "Authorization: Bearer $token" -H "Content-Length: 0" | jq
}

cmd_versions() {
    local target="${1:?usage: versions <path-or-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/versions")
    curl -fsS "$url" -H "Authorization: Bearer $token" \
      | jq '.value[] | {id, size, modified: .lastModifiedDateTime, by: .lastModifiedBy.user.displayName}'
}

cmd_mkdir() {
    # mkdir <path>   — creates all missing parents
    local path="${1:?usage: mkdir <path>}"
    local token; token=$(get_token)
    # Split into segments and create each one if missing
    local IFS='/' parts; read -r -a parts <<< "$path"
    local parent_id=""
    for seg in "${parts[@]}"; do
        [ -z "$seg" ] && continue
        # Look up under parent
        local list_url
        if [ -z "$parent_id" ]; then
            list_url="$GRAPH$DRIVE_PREFIX/root/children"
        else
            list_url="$GRAPH$DRIVE_PREFIX/items/$parent_id/children"
        fi
        local existing
        existing=$(curl -fsS "$list_url?\$select=id,name,folder&\$top=200" \
            -H "Authorization: Bearer $token" \
            | jq -r --arg n "$seg" '.value[] | select(.name == $n and .folder != null) | .id')
        if [ -n "$existing" ]; then
            parent_id="$existing"
            continue
        fi
        # Create
        local create_url
        if [ -z "$parent_id" ]; then
            create_url="$GRAPH$DRIVE_PREFIX/root/children"
        else
            create_url="$GRAPH$DRIVE_PREFIX/items/$parent_id/children"
        fi
        local body new_id
        body=$(jq -n --arg n "$seg" '{name:$n, folder:{}, "@microsoft.graph.conflictBehavior":"fail"}')
        new_id=$(curl -fsS -X POST "$create_url" \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/json" \
            -d "$body" | jq -r '.id')
        parent_id="$new_id"
    done
    echo "{\"status\":\"created\",\"path\":\"$path\",\"id\":\"$parent_id\"}"
}

cmd_upload() {
    # upload <local-file> <remote-path>
    local local_file="${1:?usage: upload <local-file> <remote-path>}"
    local remote_path="${2:?usage: upload <local-file> <remote-path>}"
    [ -f "$local_file" ] || { echo "Error: file not found: $local_file" >&2; exit 1; }
    local token; token=$(get_token)
    local size
    size=$(stat -c%s "$local_file" 2>/dev/null || stat -f%z "$local_file")
    local enc; enc=$(url_encode_path "$remote_path")

    if [ "$size" -le 4000000 ]; then
        # Simple PUT
        local url="$GRAPH$DRIVE_PREFIX/root:/$enc:/content?@microsoft.graph.conflictBehavior=replace"
        curl -fsS -X PUT "$url" \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/octet-stream" \
            --data-binary "@$local_file" \
          | jq '{status:"uploaded", name, size, id, url: .webUrl}'
    else
        # Resumable
        local session_url="$GRAPH$DRIVE_PREFIX/root:/$enc:/createUploadSession"
        local session
        session=$(curl -fsS -X POST "$session_url" \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/json" \
            -d '{"item":{"@microsoft.graph.conflictBehavior":"replace"}}')
        local upload_url
        upload_url=$(echo "$session" | jq -r '.uploadUrl')
        if [ -z "$upload_url" ] || [ "$upload_url" = "null" ]; then
            echo "$session" | jq '.error // .' >&2; exit 1
        fi
        # Stream chunks of 10 MiB (10485760 = 32 * 327680, multiple of 320 KiB)
        local chunk=10485760
        local offset=0 last result
        while [ "$offset" -lt "$size" ]; do
            local end=$((offset + chunk - 1))
            [ "$end" -ge "$size" ] && end=$((size - 1))
            local len=$((end - offset + 1))
            result=$(dd if="$local_file" bs=1 skip="$offset" count="$len" 2>/dev/null \
                | curl -fsS -X PUT "$upload_url" \
                    -H "Content-Length: $len" \
                    -H "Content-Range: bytes $offset-$end/$size" \
                    --data-binary @-)
            offset=$((end + 1))
            echo "$result" | jq -c '{nextExpectedRanges, id, name, size, status:"chunk"}' >&2 || true
            last="$result"
        done
        echo "$last" | jq '{status:"uploaded", name, size, id, url: .webUrl}'
    fi
}

cmd_upload_stream() {
    # upload-stream <remote-path>   — reads stdin
    local remote_path="${1:?usage: upload-stream <remote-path>}"
    local token; token=$(get_token)
    local enc; enc=$(url_encode_path "$remote_path")
    local url="$GRAPH$DRIVE_PREFIX/root:/$enc:/content?@microsoft.graph.conflictBehavior=replace"
    curl -fsS -X PUT "$url" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/octet-stream" \
        --data-binary @- \
      | jq '{status:"uploaded", name, size, id, url: .webUrl}'
}

cmd_download() {
    # download <remote> [local]
    local remote="${1:?usage: download <remote-path-or-id> [local-path]}"
    local local_path="${2:-}"
    local token; token=$(get_token)
    # Get download URL from item metadata
    local info_url; info_url=$(item_url "$remote")
    local info
    info=$(curl -fsS "$info_url?\$select=id,name,@microsoft.graph.downloadUrl" \
        -H "Authorization: Bearer $token")
    local name dl
    name=$(echo "$info" | jq -r '.name')
    dl=$(echo "$info" | jq -r '."@microsoft.graph.downloadUrl"')
    [ -z "$local_path" ] && local_path="$name"
    # downloadUrl is pre-authenticated — no auth header
    curl -fsS -L "$dl" -o "$local_path"
    local size
    size=$(stat -c%s "$local_path" 2>/dev/null || stat -f%z "$local_path")
    echo "{\"status\":\"downloaded\",\"file\":\"$local_path\",\"size\":$size}"
}

cmd_cat() {
    local remote="${1:?usage: cat <path-or-id>}"
    local token; token=$(get_token)
    local info_url; info_url=$(item_url "$remote")
    local dl
    dl=$(curl -fsS "$info_url?\$select=@microsoft.graph.downloadUrl" \
        -H "Authorization: Bearer $token" | jq -r '."@microsoft.graph.downloadUrl"')
    curl -fsS -L "$dl"
}

cmd_url() {
    local remote="${1:?usage: url <path-or-id>}"
    local token; token=$(get_token)
    local info_url; info_url=$(item_url "$remote")
    curl -fsS "$info_url?\$select=@microsoft.graph.downloadUrl,webUrl,name" \
        -H "Authorization: Bearer $token" \
      | jq '{name, downloadUrl: ."@microsoft.graph.downloadUrl", webUrl}'
}

cmd_rename() {
    local target="${1:?usage: rename <path-or-id> <new-name>}"
    local newname="${2:?usage: rename <path-or-id> <new-name>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target")
    curl -fsS -X PATCH "$url" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg n "$newname" '{name:$n}')" \
      | jq '{status:"renamed", name, id, url: .webUrl}'
}

cmd_move() {
    # move <source> <dest-folder>
    local src="${1:?usage: move <source-path-or-id> <dest-folder-path-or-id>}"
    local dst="${2:?usage: move <source-path-or-id> <dest-folder-path-or-id>}"
    local token; token=$(get_token)
    local src_url; src_url=$(item_url "$src")
    local dst_id; dst_id=$(resolve_id "$dst")
    curl -fsS -X PATCH "$src_url" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg id "$dst_id" '{parentReference:{id:$id}}')" \
      | jq '{status:"moved", name, id, parent:.parentReference.path}'
}

cmd_copy() {
    # copy <source> <dest-folder> [new-name]
    local src="${1:?usage: copy <source-path-or-id> <dest-folder-path-or-id> [new-name]}"
    local dst="${2:?usage: copy <source-path-or-id> <dest-folder-path-or-id> [new-name]}"
    local newname="${3:-}"
    local token; token=$(get_token)
    local src_url; src_url=$(item_url "$src" "/copy")
    local dst_id; dst_id=$(resolve_id "$dst")
    local body
    if [ -n "$newname" ]; then
        body=$(jq -n --arg id "$dst_id" --arg n "$newname" '{parentReference:{id:$id}, name:$n}')
    else
        body=$(jq -n --arg id "$dst_id" '{parentReference:{id:$id}}')
    fi
    # Returns 202 Accepted with Location header for monitoring
    local resp
    resp=$(curl -fsS -X POST "$src_url" -D /tmp/.onedrive-copy-headers \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$body" || true)
    local monitor
    monitor=$(grep -i '^location:' /tmp/.onedrive-copy-headers | awk '{print $2}' | tr -d '\r\n' || true)
    rm -f /tmp/.onedrive-copy-headers
    echo "{\"status\":\"copy_queued\",\"monitor\":\"$monitor\"}"
}

cmd_delete() {
    local target="${1:?usage: delete <path-or-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target")
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$url" \
        -H "Authorization: Bearer $token")
    if [ "$code" = "204" ]; then
        echo "{\"status\":\"deleted\",\"target\":\"$target\"}"
    else
        echo "{\"status\":\"failed\",\"http_code\":$code}" >&2
        exit 1
    fi
}

cmd_search() {
    local q="${1:?usage: search <query> [top]}"
    local top="${2:-25}"
    local token; token=$(get_token)
    local q_enc; q_enc=$(jq -nr --arg v "$q" '$v|@uri')
    curl -fsS "$GRAPH$DRIVE_PREFIX/root/search(q='$q_enc')?\$top=$top&\$select=id,name,size,file,folder,webUrl,parentReference" \
        -H "Authorization: Bearer $token" \
      | jq '.value[] | {kind:(if .folder then "dir" else "file" end), name, size, id, path: .parentReference.path, url: .webUrl}'
}

cmd_tree() {
    # tree [path] [max-depth]
    local path="${1:-}"
    local maxdepth="${2:-3}"
    local token; token=$(get_token)
    _tree_recurse() {
        local p="$1" d="$2" indent="$3"
        [ "$d" -gt "$maxdepth" ] && return
        local url
        if [ -z "$p" ]; then
            url="$GRAPH$DRIVE_PREFIX/root/children?\$top=200&\$select=id,name,folder,file"
        else
            url=$(item_url "$p" "/children?\$top=200&\$select=id,name,folder,file")
        fi
        local items
        items=$(curl -fsS "$url" -H "Authorization: Bearer $token")
        echo "$items" | jq -r '.value[] | "\(if .folder then "D" else "F" end)\t\(.name)\t\(.id)"' \
            | while IFS=$'\t' read -r kind name id; do
                echo "${indent}${kind} ${name}"
                if [ "$kind" = "D" ]; then
                    local child="$p/$name"; child="${child#/}"
                    _tree_recurse "$child" "$((d + 1))" "$indent  "
                fi
            done
    }
    _tree_recurse "$path" 1 ""
}

cmd_delta() {
    # delta [token]
    local token; token=$(get_token)
    local delta_arg="${1:-}"
    local url
    if [ -n "$delta_arg" ]; then
        url="$GRAPH$DRIVE_PREFIX/root/delta?token=$delta_arg"
    else
        url="$GRAPH$DRIVE_PREFIX/root/delta"
    fi
    curl -fsS "$url" -H "Authorization: Bearer $token" | jq
}

cmd_drives() {
    local token; token=$(get_token)
    curl -fsS "$GRAPH/me/drives" -H "Authorization: Bearer $token" \
      | jq '.value[] | {id, name, driveType, owner: .owner.user.displayName, total: .quota.total, used: .quota.used}'
}

cmd_drive() {
    local drive_id="${1:-}"
    local token; token=$(get_token)
    local url
    if [ -z "$drive_id" ]; then
        url="$GRAPH$DRIVE_PREFIX"
    else
        url="$GRAPH/drives/$drive_id"
    fi
    curl -fsS "$url" -H "Authorization: Bearer $token" | jq
}

cmd_quota() {
    local token; token=$(get_token)
    curl -fsS "$GRAPH$DRIVE_PREFIX" -H "Authorization: Bearer $token" \
      | jq '.quota | {state, total, used, remaining, deleted}'
}

cmd_help() {
    cat <<EOF
Usage: onedrive-files.sh <command> [args]

LISTING
  list [path]                List children of root (or path)
  list-id <item-id>          List children by item ID
  list-special <name>        Special folder children (documents|photos|cameraroll|approot|music)
  recent [count]             Recently used files
  shared [count]             Items shared with me
  tree [path] [max-depth=3]  Recursive tree view

INSPECT
  info <path-or-id>          Full metadata (JSON)
  stat <path-or-id>          Compact metadata
  thumbnail <id> [size]      Thumbnail URL (small|medium|large)
  preview <id>               Embeddable preview URL
  versions <id>              Version history

CREATE
  mkdir <path>               Create folder (creates parents)
  upload <local> <remote>    Upload (auto: simple if ≤4MB, else resumable in 10MiB chunks)
  upload-stream <remote>     Pipe stdin to a remote file

READ / DOWNLOAD
  download <remote> [local]  Save to local (default: basename)
  cat <path>                 Stream content to stdout
  url <path>                 Print pre-auth downloadUrl + webUrl

MODIFY
  rename <id-or-path> <new>
  move   <src> <dest-folder>
  copy   <src> <dest-folder> [new-name]
  delete <id-or-path>        Move to recycle bin

SEARCH / SYNC
  search "<query>" [top]
  delta [token]              Initial or incremental changes

DRIVES
  drives                     List accessible drives
  drive [drive-id]           Drive metadata (default: yours)
  quota                      Storage usage

Env overrides:
  ONEDRIVE_ACCESS_TOKEN      Use this token directly (skip credentials file)
  ONEDRIVE_DRIVE_PREFIX      Default '/me/drive'; override with '/drives/{id}' or '/sites/{id}/drive'
  ONEDRIVE_GRAPH_BASE        Default 'https://graph.microsoft.com/v1.0'
  ONEDRIVE_MCP_CONFIG_DIR        Default '~/.onedrive-mcp'
EOF
}

case "${1:-help}" in
    list)          shift; cmd_list "$@" ;;
    list-id)       shift; cmd_list_id "$@" ;;
    list-special)  shift; cmd_list_special "$@" ;;
    recent)        shift; cmd_recent "$@" ;;
    shared)        shift; cmd_shared "$@" ;;
    tree)          shift; cmd_tree "$@" ;;
    info)          shift; cmd_info "$@" ;;
    stat)          shift; cmd_stat "$@" ;;
    thumbnail)     shift; cmd_thumbnail "$@" ;;
    preview)       shift; cmd_preview "$@" ;;
    versions)      shift; cmd_versions "$@" ;;
    mkdir)         shift; cmd_mkdir "$@" ;;
    upload)        shift; cmd_upload "$@" ;;
    upload-stream) shift; cmd_upload_stream "$@" ;;
    download)      shift; cmd_download "$@" ;;
    cat)           shift; cmd_cat "$@" ;;
    url)           shift; cmd_url "$@" ;;
    rename)        shift; cmd_rename "$@" ;;
    move)          shift; cmd_move "$@" ;;
    copy)          shift; cmd_copy "$@" ;;
    delete|rm)     shift; cmd_delete "$@" ;;
    search)        shift; cmd_search "$@" ;;
    delta)         shift; cmd_delta "$@" ;;
    drives)        shift; cmd_drives "$@" ;;
    drive)         shift; cmd_drive "$@" ;;
    quota)         shift; cmd_quota "$@" ;;
    help|--help|-h|"") cmd_help ;;
    *) echo "Unknown command: $1"; cmd_help; exit 1 ;;
esac
