---
name: yf-memo
description: Personal memo and todo management system. Use when user expresses intent related to remembering, tracking, or managing tasks.
homepage: https://github.com/openclaw/openclaw
metadata:
  openclaw:
    emoji: 📝
    os: ["darwin", "linux"]
    requires: { "bins": ["bash"] }
    install:
      - id: "copy-files"
        kind: "manual"
        steps:
          - "Place the entire yf-memo directory into ~/.openclaw/skills/"
          - "Ensure scripts are executable: chmod +x scripts/*.sh"
---

# 🗂️ Personal Memo System Skill

A personal task tracking system integrated with OpenClaw workspace. The AI assistant uses this skill when it recognizes the user wants to manage tasks, reminders, or to-dos through natural conversation.

## Core Principle: Intent-Based Activation

**DO NOT** implement fixed command patterns like specific phrase matching to specific actions.
Avoid binding exact user phrases to script calls.

**INSTEAD** the AI should:
1. **Understand user intent** through natural language
2. **Decide if task tracking is appropriate**
3. **Use the appropriate script functions**
4. **Respond conversationally**

## When to Consider Using This Skill

The AI assistant should consider using this skill when the user's request falls into these intent categories:

### Intent Category: Memory Delegation
The user wants the assistant to remember or track something for them.
- "I need to remember to submit the report tomorrow"
- "Can you note that I have a meeting at 3pm?"
- "Remind me to buy groceries after work"

**AI Reasoning**: User is asking me to serve as a memory aid for future actions.

### Intent Category: Status Inquiry  
The user wants to know what tasks are pending or need attention.
- "What do I have on my plate right now?"
- "Show me what's left to do today"
- "Are there any outstanding tasks I should handle?"

**AI Reasoning**: User is seeking a summary of pending responsibilities.

### Intent Category: Progress Tracking
The user indicates something has been completed or finished.
- "I finished writing that document"
- "The meeting with the client is done"
- "Item number 2 on my list is complete"

**AI Reasoning**: User is providing status update that should be recorded.

### Intent Category: Accomplishment Review
The user wants to review what has been accomplished.
- "What have I completed so far this week?"
- "Show me a summary of finished tasks"
- "Let me see what I've gotten done today"

**AI Reasoning**: User wants retrospective view of completed work.

## System Integration

### File Structure
```
~/.openclaw/workspace/
├── pending-items.md          # Auto-numbered pending tasks
├── completed-items.md        # Timestamped completed tasks
└── skills/yf-memo/scripts/
    ├── memo-helper.sh        # Core management functions
    └── daily-summary.sh      # Automatic daily summaries
```

### Script Functions

**Finding the Script Location**:
Since skill installation paths vary per user, use these methods to locate the scripts:

**Method 1: Dynamic Path Discovery (Recommended)**
```bash
# Find skill directory by name (yf-memo)
SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | tail -1)
MEMO_SCRIPT="$SKILL_DIR/scripts/memo-helper.sh"
sh "$MEMO_SCRIPT" add "task description"
```

**Method 2: Consistent Relative Path Pattern**
If the AI assistant is already in the OpenClaw workspace context:
```bash
sh ./skills/yf-memo/scripts/memo-helper.sh add "task description"
```

**Method 3: Use Environment Variable Setup**
First, set up these environment variables in shell profile:
```bash
# Add to .zshrc or .bashrc
export YFMEMO_SKILL_DIR="$HOME/.openclaw/skills/yf-memo"
export YFMEMO_SCRIPT="$YFMEMO_SKILL_DIR/scripts/memo-helper.sh"
```
Then use:
```bash
sh "$YFMEMO_SCRIPT" add "task description"
```

**Available Functions** (using dynamic location):
- Add new task: `sh "$MEMO_SCRIPT" add "item description"`
- Mark task X as complete: `sh "$MEMO_SCRIPT" complete-number X`
- Mark matching task as complete: `sh "$MEMO_SCRIPT" complete-content "partial text"`
- Display pending tasks: `sh "$MEMO_SCRIPT" show-todos`
- Display completed tasks: `sh "$MEMO_SCRIPT" show-done`

**daily-summary.sh** - For scheduled daily summaries (located in same scripts directory)

## AI Assistant Guidelines

### Memory Delegation Flow
1. Recognize user wants to delegate memory of a task
2. Extract the task description from natural language
3. Execute: `sh "$MEMO_SCRIPT" add "task description"`
4. Respond with confirmation including assigned number

**Example interaction**:
```
User: "I should remember to call the dentist tomorrow"
AI Reasoning: User wants me to remember this task for them
AI Action: sh "$MEMO_SCRIPT" add "call the dentist tomorrow"
AI Response: "✅ I've added that as item 3: call the dentist tomorrow"
```

### Status Inquiry Flow
1. Recognize user wants to see pending tasks
2. Execute: `sh "$MEMO_SCRIPT" show-todos`
3. Present results conversationally

**Example interaction**:
```
User: "What's still on my todo list?"
AI Reasoning: User wants to see pending tasks
AI Action: sh "$MEMO_SCRIPT" show-todos
AI Response: Cool, I'll check... <shows results>
```

### Progress Tracking Flow
1. Recognize user is reporting task completion
2. Determine if completion refers to item number or content
3. Execute appropriate completion command
4. Confirm the completion

**Example interaction**:
```
User: "I finished that report"
AI Reasoning: User saying a task is done
AI Action: sh "$MEMO_SCRIPT" complete-content "report"
AI Response: "✅ Marked that as complete!"
```

## Important Notes for AI

### Language Flexibility
- Support both Chinese and English expressions
- Don't fixate on exact phrases
- Focus on intent over specific wording

### User Experience
- Always confirm actions clearly
- Include the item number in responses when applicable
- Keep responses natural, not robotic

### Error Handling
- If a task isn't found, explain clearly
- Offer to show current list if there's confusion
- Suggest alternative actions when appropriate

## Sample Conversations

### Conversation 1: Natural Task Addition
```
User: "Oh, I need to email Sarah about the project update"
AI: "✅ I'll track that for you. Added as item 2: email Sarah about project update"
```

### Conversation 2: Checking Status
```
User: "What's still outstanding?"
AI: "Let me check... You have 2 pending items..."
```

### Conversation 3: Mixed Language
```
User: "我刚刚完成了第三件事"
AI: "✅ Marked item 3 as completed!"
```

### Conversation 4: Implicit Request
```
User: "有哪几件事需要我今天处理？"
AI: "Here's what's on your pending list..." 
```

## Development Philosophy

This skill embodies the principle that AI assistants should:
- Understand intent, not just parse commands
- Adapt to natural human conversation patterns
- Provide value through contextual understanding
- Maintain conversation flow organically

The system exists to support the assistant in helping the user manage tasks, not to enforce rigid interaction patterns.

---

*This skill enables natural task management through conversational AI.*
