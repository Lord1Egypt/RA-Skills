#!/bin/bash
# 自动统计与提升脚本
# 每日 00:00 自动执行，遍历所有智能体

set -e

# 获取共享学习目录
SHARED_LEARNING_DIR="${SHARED_LEARNING_DIR:-/root/.openclaw/shared-learning}"

# 获取当前 agent ID（用于日志记录）
CURRENT_AGENT_ID="${AGENT_ID:-main}"

# 工作区基础路径
WORKSPACE_BASE="/root/.openclaw"

# 是否启用自动提升（默认启用）
AUTO_PROMOTE_ENABLED="${AUTO_PROMOTE_ENABLED:-true}"

# 日志输出
log() {
    echo "$1"
}

# 获取所有智能体列表及其工作区
get_all_agents() {
    local agents=()
    
    if command -v openclaw &> /dev/null; then
        while IFS= read -r line; do
            if [[ $line =~ ^([a-zA-Z0-9_-]+)\ -\>\ (.+)$ ]]; then
                agents+=("${BASH_REMATCH[1]}:${BASH_REMATCH[2]}")
            fi
        done < <(openclaw config get agents.list 2>&1 | jq -r '.[] | "\(.id) -> \(.workspace)"' 2>/dev/null)
    fi
    
    # 如果没有找到，使用默认值
    if [ ${#agents[@]} -eq 0 ]; then
        agents=("main:$WORKSPACE_BASE/workspace-ql")
    fi
    
    echo "${agents[@]}"
}

# 检测学习目录路径
get_learning_dir() {
    local workspace="$1"
    local learnings_path="$workspace/.learnings"
    
    # 检查 .learnings 是否存在
    if [ ! -e "$learnings_path" ]; then
        echo "$SHARED_LEARNING_DIR"
        return
    fi
    
    # 检查是否是软连接
    if [ -L "$learnings_path" ]; then
        local target_path=$(readlink -f "$learnings_path")
        echo "$target_path"
        return
    fi
    
    # 如果是独立文件夹
    if [ -d "$learnings_path" ]; then
        echo "$learnings_path"
        return
    fi
    
    echo "$SHARED_LEARNING_DIR"
}

# 统计并更新 Recurrence-Count
update_recurrence_counts() {
    local learning_dir="$1"
    local errors_file="$learning_dir/ERRORS.md"
    local learnings_file="$learning_dir/LEARNINGS.md"
    
    # 临时文件用于存储 Pattern-Key 统计
    local temp_file=$(mktemp)
    
    # 提取所有 Pattern-Key 及其出现次数
    grep -oh "- Pattern-Key: [^$]*" "$errors_file" "$learnings_file" 2>/dev/null | \
        sed 's/- Pattern-Key: //' | \
        grep -v "^$" | \
        grep -v "^|" | \
        grep -v "^)" | \
        grep -v "^(" | \
        grep -v "^uniq" | \
        grep -v "^sort" | \
        grep -v "^grep" | \
        grep -v "^sed" | \
        grep -v "^awk" | \
        grep -v "^cut" | \
        grep -v "^自动生成" | \
        grep -v "^  " | \
        sort | uniq -c | \
        while read count key; do
            echo "$key:$count" >> "$temp_file"
        done
    
    # 对每个 Pattern-Key 更新记录
    if [ -f "$temp_file" ]; then
        while IFS=: read -r key count; do
            # 找到所有包含此 Pattern-Key 的记录
            local files=$(grep -l "- Pattern-Key: $key" "$errors_file" "$learnings_file" 2>/dev/null || true)
            
            if [ -n "$files" ]; then
                # 找到最早和最晚日期
                local first_seen=$(grep -B20 "- Pattern-Key: $key" $files 2>/dev/null | grep "Logged:" | head -1 | sed 's/.*Logged: //' | cut -d'T' -f1)
                local last_seen=$(grep -B20 "- Pattern-Key: $key" $files 2>/dev/null | grep "Logged:" | tail -1 | sed 's/.*Logged: //' | cut -d'T' -f1)
                
                # 更新所有相关记录
                for file in $files; do
                    # 使用 awk 更新特定 Pattern-Key 的 Recurrence-Count
                    awk -v key="$key" -v count="$count" -v first="$first_seen" -v last="$last_seen" '
                    BEGIN { in_record = 0; found_key = 0; updated = 0 }
                    /^## \[/ {
                        if (in_record && found_key && !updated) {
                            # 上一个记录有 Pattern-Key 但未更新，插入
                            print "- Recurrence-Count: " count
                            print "- First-Seen: " first
                            print "- Last-Seen: " last
                        }
                        in_record = 1
                        found_key = 0
                        updated = 0
                    }
                    in_record && /- Pattern-Key: / {
                        if ($0 ~ "- Pattern-Key: " key) {
                            found_key = 1
                        }
                    }
                    in_record && /Recurrence-Count:/ && found_key && !updated {
                        sub(/Recurrence-Count: [0-9]+/, "Recurrence-Count: " count)
                        updated = 1
                    }
                    in_record && /First-Seen:/ && found_key {
                        sub(/First-Seen: .*/, "First-Seen: " first)
                    }
                    in_record && /Last-Seen:/ && found_key {
                        sub(/Last-Seen: .*/, "Last-Seen: " last)
                    }
                    { print }
                    END {
                        if (in_record && found_key && !updated) {
                            print "- Recurrence-Count: " count
                            print "- First-Seen: " first
                            print "- Last-Seen: " last
                        }
                    }
                    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
                done
            fi
        done < "$temp_file"
        rm -f "$temp_file"
    fi
}

# 自动提升
auto_promote() {
    local learning_dir="$1"
    local agent_id="$2"
    local workspace_dir="$3"
    local soul_file="$workspace_dir/SOUL.md"
    
    local errors_file="$learning_dir/ERRORS.md"
    local learnings_file="$learning_dir/LEARNINGS.md"
    
    local promoted_count=0
    
    # 查找候选项（Recurrence-Count >= 3）
    local candidates=$(grep -l "Recurrence-Count: [3-9]" "$errors_file" "$learnings_file" 2>/dev/null || true)
    
    if [ -z "$candidates" ]; then
        return 0
    fi
    
    for file in $candidates; do
        # 提取所有候选项的 Pattern-Key（去重）
        local pattern_keys=$(awk '/^## \[/ { in_record = 1 }
 in_record && /- Pattern-Key: / { 
    match($0, /- Pattern-Key: [^$]*/)
    key = substr($0, RSTART + 15, RLENGTH - 15)
    print key
    in_record = 0
 }
 /^---/ { in_record = 0 }' "$file" | sort -u)
        
        if [ -z "$pattern_keys" ]; then
            continue
        fi
        
        # 对每个 Pattern-Key 进行提升
        for pattern_key in $pattern_keys; do
        
        # 检查是否已提升（检查该 Pattern-Key 下是否有记录已提升）
        local promoted_by=$(awk -v pattern="$pattern_key" '
        BEGIN { in_record = 0; found = 0 }
        /^## \[/ {
            if (in_record && found) {
                exit
            }
            in_record = 1
            found = 0
        }
        in_record && /- Pattern-Key: / {
            if ($0 ~ "- Pattern-Key: " pattern) {
                found = 1
            }
        }
        in_record && /Promoted-By:/ && found {
            print $0
            exit
        }
        ' "$file" | sed 's/.*Promoted-By: //')
        
        if [ -n "$promoted_by" ] && echo "$promoted_by" | grep -q "$agent_id"; then
            # 当前 agent 已提升，跳过
            continue
        fi
        
        # 提取该 Pattern-Key 下第一条记录的摘要和建议行动
        local summary=$(awk -v pattern="$pattern_key" '
        BEGIN { in_record = 0; found = 0; in_summary = 0 }
        /^## \[/ {
            if (in_record && found) {
                exit
            }
            in_record = 1
            found = 0
        }
        in_record && /- Pattern-Key: / {
            if ($0 ~ "- Pattern-Key: " pattern) {
                found = 1
            }
        }
        in_record && /### 摘要/ {
            in_summary = 1
            next
        }
        in_summary && /^###/ {
            in_summary = 0
        }
        in_summary {
            print
        }
        ' "$file")
        
        local action=$(awk -v pattern="$pattern_key" '
        BEGIN { in_record = 0; found = 0; in_action = 0 }
        /^## \[/ {
            if (in_record && found) {
                exit
            }
            in_record = 1
            found = 0
        }
        in_record && /- Pattern-Key: / {
            if ($0 ~ "- Pattern-Key: " pattern) {
                found = 1
            }
        }
        in_record && /### 建议行动/ {
            in_action = 1
            next
        }
        in_action && /^###/ {
            in_action = 0
        }
        in_action {
            print
        }
        ' "$file")
        
        # 提取 Area 字段
        local area=$(awk -v pattern="$pattern_key" '
        BEGIN { in_record = 0; found = 0 }
        /^## \[/ {
            if (in_record && found) {
                exit
            }
            in_record = 1
            found = 0
        }
        in_record && /^- Area: / {
            area = $0
        }
        in_record && /- Pattern-Key: / {
            if ($0 ~ "- Pattern-Key: " pattern) {
                found = 1
                print area
                exit
            }
        }
        ' "$file" | sed 's/.*Area: //')
        
        if [ -z "$summary" ]; then
            summary="自动提升的规则"
        fi
        
        if [ -z "$area" ]; then
            area="其他"
        fi
        
        # 检查是否启用自动提升
        if [ "$AUTO_PROMOTE_ENABLED" != "true" ]; then
            log "    跳过提升（AUTO_PROMOTE_ENABLED=$AUTO_PROMOTE_ENABLED）"
            continue
        fi
        
        # 根据 Area 映射到二级标题
        local section_header=""
        case "$area" in
            "行为准则"|"行为模式"|"交互规范")
                section_header="## Core Truths（核心准则）"
                ;;
            "工作流"|"工作流改进"|"任务分发")
                section_header="## 工作流程"
                ;;
            "工具"|"配置"|"工具问题")
                section_header="## 工具使用"
                ;;
            "边界"|"安全")
                section_header="## Boundaries（边界）"
                ;;
            "风格"|"气质")
                section_header="## Vibe（风格气质）"
                ;;
            "连续性"|"偏好")
                section_header="## Continuity（连续性）"
                ;;
            *)
                section_header="## 其他"
                ;;
        esac
        
        # 生成规则内容
        local rule_content="
### $summary
$action

---
"
        
        # 查找或创建二级标题，然后追加内容
        if grep -q "^$section_header" "$soul_file"; then
            # 找到二级标题，追加内容
            # 使用临时文件传递多行内容
            echo "$rule_content" > /tmp/rule_content.txt
            awk -v section="$section_header" '
            BEGIN { in_section = 0; found = 0 }
            /^## / {
                if (in_section) {
                    # 找到下一个二级标题，在之前插入
                    while ((getline line < "/tmp/rule_content.txt") > 0) {
                        print line
                    }
                    close("/tmp/rule_content.txt")
                    print $0
                    exit
                }
                if ($0 == section) {
                    in_section = 1
                }
            }
            { print }
            END {
                if (in_section) {
                    # 没有找到下一个二级标题，追加到文件末尾
                    while ((getline line < "/tmp/rule_content.txt") > 0) {
                        print line
                    }
                    close("/tmp/rule_content.txt")
                }
            }
            ' "$soul_file" > "$soul_file.tmp" && mv "$soul_file.tmp" "$soul_file"
            rm -f /tmp/rule_content.txt
        else
            # 没有找到二级标题，创建新的
            echo "" >> "$soul_file"
            echo "$section_header" >> "$soul_file"
            echo "$rule_content" >> "$soul_file"
        fi
        
        # 更新该 Pattern-Key 下所有记录的状态
        awk -v pattern="$pattern_key" -v agent_id="$agent_id" '
        BEGIN { in_record = 0; found = 0; in_metadata = 0 }
        /^## \[/ {
            if (in_record && found && in_metadata) {
                # 记录结束，检查是否需要添加 Promoted 字段
                if (!has_promoted) {
                    print "- Promoted: SOUL.md"
                }
                if (!has_promoted_by) {
                    print "- Promoted-By: " agent_id
                }
            }
            in_record = 1
            found = 0
            in_metadata = 0
            has_promoted = 0
            has_promoted_by = 0
        }
        in_record && /- Pattern-Key: / {
            if ($0 ~ "- Pattern-Key: " pattern) {
                found = 1
            }
        }
        in_record && found && /^###/ {
            # 进入内容部分，元数据结束
            in_metadata = 0
        }
        in_record && found && /^---/ {
            # 记录结束
            if (!has_promoted) {
                print "- Promoted: SOUL.md"
            }
            if (!has_promoted_by) {
                print "- Promoted-By: " agent_id
            }
            in_record = 0
        }
        in_record && found && /^-/ {
            # 元数据行
            in_metadata = 1
            if (/^- Status: pending/) {
                sub(/Status: pending/, "Status: promoted")
            }
            if (/^- Promoted:/) {
                has_promoted = 1
            }
            if (/^- Promoted-By:/) {
                has_promoted_by = 1
                if ($0 !~ /Promoted-By:.*'" agent_id "'/) {
                    sub(/Promoted-By: /, "Promoted-By: " agent_id ", ")
                }
            }
        }
        { print }
        END {
            if (in_record && found && in_metadata) {
                if (!has_promoted) {
                    print "- Promoted: SOUL.md"
                }
                if (!has_promoted_by) {
                    print "- Promoted-By: " agent_id
                }
            }
        }
        ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        
        promoted_count=$((promoted_count + 1))
        done  # 结束内层循环（for pattern_key）
    done  # 结束外层循环（for file）
    
    echo "$promoted_count"
}

# 主流程
main() {
    log "=== 自动统计与提升（所有智能体） ==="
    log ""
    
    # 获取所有智能体
    local agents=$(get_all_agents)
    
    # 分类：共享目录组和独立目录组
    declare -A shared_agents
    declare -A independent_agents
    
    for agent_entry in $agents; do
        local agent_id=$(echo "$agent_entry" | cut -d: -f1)
        local workspace=$(echo "$agent_entry" | cut -d: -f2-)
        local learning_dir=$(get_learning_dir "$workspace")
        
        if [ "$learning_dir" = "$SHARED_LEARNING_DIR" ]; then
            shared_agents["$agent_id"]="$workspace"
        else
            independent_agents["$agent_id"]="$workspace:$learning_dir"
        fi
    done
    
    # 处理共享目录
    if [ ${#shared_agents[@]} -gt 0 ]; then
        log "共享目录："
        
        # 统计共享目录
        update_recurrence_counts "$SHARED_LEARNING_DIR"
        
        # 找出候选项
        local shared_candidates=$(grep -l "Recurrence-Count: [3-9]" "$SHARED_LEARNING_DIR"/*.md 2>/dev/null || true)
        local shared_candidate_count=0
        if [ -n "$shared_candidates" ]; then
            shared_candidate_count=$(echo "$shared_candidates" | xargs grep -c "Recurrence-Count: [3-9]" 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
        fi
        
        log "  发现候选项：$shared_candidate_count 条"
        log "  需要提升的智能体：${!shared_agents[*]}"
        
        # 依次提升
        for agent_id in "${!shared_agents[@]}"; do
            local workspace="${shared_agents[$agent_id]}"
            local promoted=$(auto_promote "$SHARED_LEARNING_DIR" "$agent_id" "$workspace")
            log "  提升 $agent_id：$promoted 条"
        done
        
        log ""
    fi
    
    # 处理独立目录
    if [ ${#independent_agents[@]} -gt 0 ]; then
        log "独立目录："
        
        for agent_id in "${!independent_agents[@]}"; do
            local entry="${independent_agents[$agent_id]}"
            local workspace=$(echo "$entry" | cut -d: -f1)
            local learning_dir=$(echo "$entry" | cut -d: -f2)
            
            log "  $agent_id："
            
            # 统计
            update_recurrence_counts "$learning_dir"
            
            # 找出候选项
            local ind_candidates=$(grep -l "Recurrence-Count: [3-9]" "$learning_dir"/*.md 2>/dev/null || true)
            local ind_candidate_count=0
            if [ -n "$ind_candidates" ]; then
                ind_candidate_count=$(echo "$ind_candidates" | xargs grep -c "Recurrence-Count: [3-9]" 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
            fi
            
            # 提升
            local promoted=$(auto_promote "$learning_dir" "$agent_id" "$workspace")
            log "    发现候选项：$ind_candidate_count 条"
            log "    提升：$promoted 条"
        done
        
        log ""
    fi
    
    log "完成"
}

# 执行
main
