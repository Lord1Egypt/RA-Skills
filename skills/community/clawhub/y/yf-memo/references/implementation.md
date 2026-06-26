# 🔧 Implementation Guide: Personal Memo System

## System Architecture Overview

### Core Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Pattern Match  │───▶│ Script Execution│
│   (Natural Language)    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent Logic   │    │  Command Parse  │    │   File Update   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow
1. **User** → Speaks natural language request
2. **Agent** → Recognizes pattern & extracts parameters
3. **Script** → Executes appropriate action
4. **Files** → Updates markdown files
5. **Agent** → Returns formatted response

## Pattern Recognition Logic

### 1. Adding Todos (添加item)
**Patterns:**
- `Reminder: {content}`
- `remember{content}`
- `帮我在memo reminder里加上: {content}`
- `需要remind我: {content}`

**Regex Examples:**
```regex
Reminder: (.+)
remember(.+)
需要remind我: (.+)
```

**Agent Logic:**
```python
def handle_add_todo(user_input):
    if Reminder:  in user_input:
        content = user_input.split(Reminder: )[1].strip()
    elif remember in user_input:
        content = user_input.split(remember)[1].strip()
    # ... more patterns
    
    # Execute script
    result = exec_command(f'sh memo-helper.sh add {content}')
    
    # Format response
    return f✅ 已添加item X: {content}
```

### 2. Completing Items (completeitem)
**Patterns by Number:**
- `item{num}is done`
- `complete第{num}个item`
- `task{num}做好了`

**Patterns by Content:**
- `{content}is done`
- `{content}搞定了`
- `{content}的taskcomplete了`

**Agent Logic:**
```python
def handle_complete_item(user_input):
    # Check for number-based completion
    import re
    num_match = re.search(r'item(\d+)is done', user_input)
    if num_match:
        num = num_match.group(1)
        result = exec_command(f'sh memo-helper.sh complete-number {num}')
        return parse_completion_response(result, by_number=True)
    
    # Check for content-based completion
    if is done in user_input:
        content = user_input.split(is done)[0].strip()
        result = exec_command(f'sh memo-helper.sh complete-content {content}')
        return parse_completion_response(result, by_number=False)
```

### 3. Viewing Items (showitem)
**Simple Patterns:**
- `showpending items` → `sh memo-helper.sh show-todos`
- `showcompleted items` → `sh memo-helper.sh show-done`
- `summarize一下completed items` → `sh memo-helper.sh show-done` + formatting

## Script Implementation Details

### memo-helper.sh Core Functions

#### File Structure Management
```bash
# Base paths
# 注意：脚本内部可以使用相对路径或HOME，因为脚本会随技能一起安装
# 但AI调用脚本时需要使用动态路径查找
TODO_FILE=$HOME/.openclaw/workspace/pending-items.md
DONE_FILE=$HOME/.openclaw/workspace/completed-items.md

# Template files
create_todo_template() {
    cat > $TODO_FILE << 'EOF'
# 📝 pending items

_最后更新: {timestamp}_

## pending items

_暂无pending items_

---

## 提示
- 添加item: 使用Format `添加item: <内容>`
- completeitem: 说 `itemXis done` 或 `<内容>is done`
- show: `showpending items`
EOF
}
```

#### Auto-Numbering System
```bash
get_next_number() {
    if grep -q ^[0-9]\+\.  $TODO_FILE; then
        last_num=$(grep ^[0-9]\+\.  $TODO_FILE | tail -1 | awk -F'[. ]' '{print $1}')
        echo $((last_num + 1))
    else
        echo 1
    fi
}
```

**Numbering Rules:**
1. Start at 1 for empty list
2. Increment sequentially
3. Keep number even if items completed (numbers don't reorder)
4. Numbers are persistent reference points

#### Completion Tracking
```bash
complete_by_number() {
    local num=$1
    
    # Find and extract the item
    local line=$(grep -n ^$num\.  $TODO_FILE | cut -d: -f1)
    local content=$(grep ^$num\.  $TODO_FILE | sed 's/^[0-9]\+\. //')
    
    # Remove from TODO file
    sed -i '' ${line}d $TODO_FILE
    
    # Add to DONE file with timestamp
    local completed_time=$(date '+%Y-%m-%d %H:%M')
    sed -i '' /## completed items列表/a\\
\\
### $completed_time\\
$num\. $content $DONE_FILE
}
```

### Error Handling

#### File Existence Checks
```bash
check_files_exist() {
    for file in $TODO_FILE $DONE_FILE; do
        if [ ! -f $file ]; then
            create_template $file
        fi
    done
}
```

#### Input Validation
```bash
validate_number() {
    local num=$1
    if ! [[ $num =~ ^[0-9]+$ ]]; then
        echo ❌ 无效的序号Format: '$num'
        return 1
    fi
    
    if ! grep -q ^$num\.  $TODO_FILE; then
        echo ❌ 未找到item $num
        return 1
    fi
    
    return 0
}
```

## Agent Integration Patterns

### Response Formatting

#### Successful Add
```python
def format_add_response(script_output, content):
    # script_outputExample: ✅ 已添加item 3: 明天要交报告
    return script_output  # 直接使用脚本输出
```

#### Successful Completion  
```python
def format_completion_response(script_output, item_info):
    # script_outputExample: ✅ item 3 is done: 明天要交报告
    return script_output  # 直接使用脚本输出
```

#### Todo List Display
```python
def format_todo_list(script_output):
    # script_outputExample: 📋 pending items: \n1. 明天要交报告\n2. 下午3点开会
    lines = script_output.split('\n')
    
    # 如果是空列表
    if 暂无pending items in script_output:
        return 📋 pending items: \n    - 暂无pending items
    
    return script_output
```

### State Management

#### Check Current State
```bash
# Agent can quickly check if there are pending todos
check_todo_count() {
    count=$(grep -c ^[0-9]\+\.  $TODO_FILE 2>/dev/null || echo 0)
    echo $count
}
```

#### Get Next Action Suggestions
```python
def suggest_next_actions():
    todo_count = check_todo_count()
    
    if todo_count == 0:
        return 当前没有pending items。需要我帮你记点什么吗？
    elif todo_count == 1:
        return f当前有1项pending items。可以说'showpending items'show具体内容。
    else:
        return f当前有{todo_count}项pending items。需要我帮你summarize一下吗？
```

## Extension Points

### Adding New Features

#### 1. Priority System
```bash
# Add priority tagging
add_todo_with_priority() {
    local content=$1
    local priority=$2  # high/medium/low
    
    # Add to todo with emoji
    local emoji=
    case $priority in
        high) emoji=🔥  ;;
        medium) emoji=⚡  ;;
        low) emoji=📝  ;;
    esac
    
    # Rest of add logic...
}
```

#### 2. Categories/Tags
```bash
# Support for categories
add_todo_with_category() {
    local content=$1
    local category=$2  # work/personal/errands
    
    # Add metadata line
    sed -i '' /## pending items/a\\
$next_num\. $content [@$category] $TODO_FILE
}
```

#### 3. Due Dates
```bash
# Support for due dates
add_todo_with_due_date() {
    local content=$1
    local due_date=$2  # YYYY-MM-DD
    
    # Store due date in a separate metadata file
    echo $next_num|$due_date >> $TODO_FILE.meta
}
```

### Integration with Other Skills

#### Apple Notes Integration
```python
def add_to_apple_notes(content):
    # Use existing apple-notes skill
    result = exec_command('memo notes -a Todo: {content}')
    return result
```

#### Calendar Integration  
```python
def add_to_calendar(content, datetime):
    # Use calendar skill if available
    result = exec_command(f'calendar add {content} --time {datetime}')
    return result
```

#### Reminder Integration
```python
def add_to_reminders(content):
    # Use apple-reminders skill
    result = exec_command(f'remindctl add {content} --list Todo')
    return result
```

## Testing Strategy

### Unit Tests for Scripts
```bash
# Test adding items
test_add_item() {
    # Setup clean state
    cp empty_todo.md $TODO_FILE
    
    # Execute add
    sh memo-helper.sh add testitem
    
    # Verify
    if grep -q testitem $TODO_FILE; then
        echo ✓ Add test passed
    else
        echo ✗ Add test failed
    fi
}
```

### Integration Tests
```python
def test_agent_recognition():
    test_cases = [
        (Reminder: test, [Remember this for me: , test]),
        (item1is done, [item, 1, is done]),
        (showpending items, [showpending items]),
    ]
    
    for input_text, expected_parse in test_cases:
        result = parse_user_input(input_text)
        assert result == expected_parse, fFailed for: {input_text}
```

### Performance Considerations

#### File I/O Optimization
- Batch updates when possible
- Use in-place editing (sed -i) instead of rewrite
- Cache file state in agent memory for quick checks

#### Memory Usage
- Todo files should stay small (100 items max recommendation)
- Clean up old completed items periodically
- Consider archival for very old completed items

## Deployment Checklist

### ✅ Pre-Deployment
- [ ] All scripts are executable (`chmod +x`)
- [ ] Required directories exist (`mkdir -p`)
- [ ] Template files are in place
- [ ] File paths are correct for workspace
- [ ] Backup existing todo files (if migrating)

### ✅ Skill Installation  
- [ ] SKILL.md follows OpenClaw format
- [ ] _meta.json has correct metadata
- [ ] References documents are complete
- [ ] Assets (if any) are included

### ✅ Agent Training
- [ ] Agent understands natural language patterns
- [ ] Response formatting is consistent
- [ ] Error messages are user-friendly
- [ ] Fallback behaviors are defined

### ✅ User Experience
- [ ] Clear examples in user guide
- [ ] Common scenarios covered
- [ ] Troubleshooting guide available
- [ ] Performance is acceptable

---

*Implementation notes updated: 2026-03-14*