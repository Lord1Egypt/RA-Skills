#!/bin/bash
# Personal Memo Helper Script
# For managing pending and completed items

TODO_FILE="$HOME/.openclaw/workspace/pending-items.md"
DONE_FILE="$HOME/.openclaw/workspace/completed-items.md"

# Update last updated timestamp
update_timestamp() {
    local current_time=$(date '+%Y-%m-%d %H:%M')
    sed -i '' "1,/Last updated:/s/Last updated: .*/Last updated: $current_time/" "$TODO_FILE"
}

# Get next item number
get_next_number() {
    if grep -q "^[0-9]\+\. " "$TODO_FILE"; then
        local last_num=$(grep "^[0-9]\+\. " "$TODO_FILE" | tail -1 | awk -F'[. ]' '{print $1}')
        echo $((last_num + 1))
    else
        echo 1
    fi
}

# Add item
add_todo() {
    local content="$1"
    local next_num=$(get_next_number)
    
    # Insert into pending items section
    if grep -q "_No pending items_" "$TODO_FILE"; then
        # Replace "No pending items" with first item
        sed -i '' "/_No pending items_/d" "$TODO_FILE"
        sed -i '' "s/## Pending items/## Pending items\n\n$next_num\. $content/" "$TODO_FILE"
    else
        # Add at the end of pending items list
        sed -i '' "/## Pending items/a\\
$next_num\. $content" "$TODO_FILE"
    fi
    
    update_timestamp
    echo "✅ Added item $next_num: $content"
}

# Complete item by number
complete_by_number() {
    local num="$1"
    local line=$(grep -n "^$num\. " "$TODO_FILE" | cut -d: -f1)
    
    if [ -z "$line" ]; then
        echo "❌ Item $num not found"
        return 1
    fi
    
    local content=$(grep "^$num\. " "$TODO_FILE" | sed 's/^[0-9]\+\. //')
    local completed_time=$(date '+%Y-%m-%d %H:%M')
    
    # Remove from pending items
    sed -i '' "${line}d" "$TODO_FILE"
    
    # If pending items is empty, add "No pending items"
    if ! grep -q "^[0-9]\+\. " "$TODO_FILE"; then
        sed -i '' "/## Pending items/a\\
\\
_No pending items_" "$TODO_FILE"
    fi
    
    # Add to completed items
    if grep -q "_No completed items yet_" "$DONE_FILE"; then
        sed -i '' "/_No completed items yet_/d" "$DONE_FILE"
    fi
    
    sed -i '' "/## Completed Items List/a\\
\\
### $completed_time\\
$num\. $content" "$DONE_FILE"
    
    update_timestamp
    echo "✅ Item $num is done: $content"
}

# Complete item by content
complete_by_content() {
    local content="$1"
    local line=$(grep -n "\. $content$" "$TODO_FILE" | cut -d: -f1)
    
    if [ -z "$line" ]; then
        echo "❌ No item found containing '$content'"
        return 1
    fi
    
    local num=$(grep "\. $content$" "$TODO_FILE" | awk -F'[. ]' '{print $1}')
    complete_by_number "$num"
}

# Show pending items
show_todos() {
    echo "📋 Pending items:"
    if grep -q "_No pending items_" "$TODO_FILE"; then
        echo "    - No pending items"
    else
        grep "^[0-9]\+\. " "$TODO_FILE" | sed 's/^/    - /'
    fi
}

# Show completed items
show_done() {
    echo "✅ Completed items:"
    if grep -q "_No completed items yet_" "$DONE_FILE"; then
        echo "    - No completed items yet"
    else
        grep -A1 "### [0-9]" "$DONE_FILE" | grep -v "^--$" | sed 's/^/    - /' | sed 's/###/Completed at: /'
    fi
}

# Clean up empty lines and format
cleanup_format() {
    # Clean excess blank lines in pending file
    sed -i '' '/^[[:space:]]*$/N;/^\n$/D' "$TODO_FILE"
    
    # Clean excess blank lines in completed file
    sed -i '' '/^[[:space:]]*$/N;/^\n$/D' "$DONE_FILE"
}

# Main function
main() {
    case "$1" in
        "add")
            shift
            add_todo "$*"
            ;;
        "complete-number")
            shift
            complete_by_number "$1"
            ;;
        "complete-content")
            shift
            complete_by_content "$*"
            ;;
        "show-todos")
            show_todos
            ;;
        "show-done")
            show_done
            ;;
        "cleanup")
            cleanup_format
            echo "✅ Format cleanup complete"
            ;;
        "help")
            echo "Usage:"
            echo "  memo-helper.sh add <item content>"
            echo "  memo-helper.sh complete-number <number>"
            echo "  memo-helper.sh complete-content <item content>"
            echo "  memo-helper.sh show-todos"
            echo "  memo-helper.sh show-done"
            echo "  memo-helper.sh cleanup"
            ;;
        *)
            echo "Invalid command, use 'help' for usage"
            ;;
    esac
}

main "$@"