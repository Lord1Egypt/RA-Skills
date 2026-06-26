cmd_list() {
  local filter_status="" filter_parent="" filter_project="" format_chat=0 filter_tag=""

  while [ $# -gt 0 ]; do
    case "$1" in
      --status=*)  filter_status="${1#*=}" ;;
      --parent=*)  filter_parent="${1#*=}" ;;
      --project=*) filter_project="${1#*=}" ;;
      --tag=*)     filter_tag="${1#*=}" ;;
      --format=chat) format_chat=1 ;;
      -*)          die "Unknown flag: $1" ;;
    esac
    shift
  done

  local where="WHERE 1=1"

  if [ -n "$filter_status" ]; then
    case "$filter_status" in
      pending|in_progress|blocked|done) ;;
      *) die "Unknown status: '$filter_status'. Use: pending, in_progress, blocked, done" ;;
    esac
    where="$where AND status = '$filter_status'"
  fi

  if [ -n "$filter_parent" ]; then
    require_int "$filter_parent" "--parent"
    where="$where AND parent_id = $filter_parent"
  fi

  if [ -n "$filter_project" ]; then
    local safe_proj
    safe_proj=$(printf '%s' "$filter_project" | sed "s/'/''/g")
    where="$where AND project = '$safe_proj'"
  fi
  
  if [ -n "$filter_tag" ]; then
    local safe_tag
    safe_tag=$(printf '%s' "$filter_tag" | sed "s/'/''/g")
    where="$where AND (tags LIKE '%$safe_tag%' OR tags = '$safe_tag')"
  fi

  if [ "$format_chat" -eq 1 ]; then
    # Bypass ASCII tables and construct pure GitHub Markdown
    local list_data
    list_data=$(sqlite3 -batch "$DB" "
    SELECT 
      CASE WHEN status = 'done' THEN '- [x] '
           WHEN status = 'in_progress' THEN '- [/] '
           WHEN status = 'blocked' THEN '- [!] '
           ELSE '- [ ] ' END ||
      '**#' || id || ': ' || request_text || '** ' ||
      '(Priority: ' || priority || ')' ||
      CASE WHEN project IS NOT NULL THEN ' [' || project || ']' ELSE '' END ||
      CASE WHEN assignee IS NOT NULL THEN ' (@' || assignee || ')' ELSE '' END ||
      CASE WHEN due_date IS NOT NULL THEN ' (Due: ' || due_date || ')' ELSE '' END ||
      CASE WHEN tags IS NOT NULL THEN ' (Tags: ' || tags || ')' ELSE '' END
    FROM tasks
    $where
    ORDER BY status = 'done', due_date IS NULL ASC, due_date ASC, priority DESC, created_at ASC;
    ")
    
    if [ -z "$list_data" ]; then
      echo "_No tasks found matching criteria._"
    else
      echo "$list_data"
    fi
    exit 0
  fi

  # Default ASCII table mode
  local q="
  SELECT
    id,
    CASE
      WHEN status = 'done' THEN '✔ '
      WHEN status = 'in_progress' THEN '▶ '
      WHEN status = 'blocked' THEN '⛔ '
      ELSE '  '
    END || substr(request_text, 1, 50) AS task,
    status,
    priority,
    IFNULL(project, '-') AS project,
    IFNULL(assignee, '-') AS assignee,
    IFNULL(due_date, '-') AS due_date,
    IFNULL(tags, '-') AS tags
  FROM tasks
  $where
  ORDER BY status = 'done', due_date IS NULL ASC, due_date ASC, priority DESC, created_at ASC;
  "

  sql_table "4 42 12 8 13 13 10 15" "$q"
}
