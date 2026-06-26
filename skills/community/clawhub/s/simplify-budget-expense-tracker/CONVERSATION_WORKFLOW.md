# Simplify Budget Conversation Workflow

This file is the visual source of truth for the budget conversation layer.

OpenClaw handles orchestration natively through its active conversation model and conversation context. No external state machine is required.

```mermaid
flowchart TD
    IN["Incoming message"] --> INTENT{"Budget intent?"}

    INTENT -- "No" --> IGNORE["Ignore or route elsewhere"]
    INTENT -- "Yes" --> PARSE["Parse: what does the user want?"]

    PARSE --> KIND{"Kind?"}

    KIND -- "Log expense" --> PREVIEW["Run log.sh --preview"]
    KIND -- "Find / inspect" --> FIND["Run find_expenses.sh or find_income.sh"]
    KIND -- "Update / delete" --> RESOLVE["Resolve target from sheet first"]
    KIND -- "Recurring question" --> RECURRING["Run find_recurring.sh"]
    KIND -- "Monthly totals" --> SUMMARY["Run find_summary.sh"]
    KIND -- "Log income" --> INCOME["Run write_income.sh"]

    PREVIEW --> EXPLICIT{"Explicit category?"}
    EXPLICIT -- "Yes" --> WRITE_DIRECT["Run log.sh --category X"]
    EXPLICIT -- "No" --> CONFIDENCE{"Strong match?"}

    CONFIDENCE -- "builtin / learned" --> ASK_CONFIRM["Relay question, wait for reply"]
    CONFIDENCE -- "No match" --> ASK_CATEGORY["Relay best-guess question, wait for reply"]

    ASK_CONFIRM --> REPLY{"User reply?"}
    ASK_CATEGORY --> REPLY

    REPLY -- "yes" --> WRITE_PROPOSED["Run log.sh --category proposed"]
    REPLY -- "category name" --> WRITE_OVERRIDE["Run log.sh --category chosen"]
    REPLY -- "cancel" --> DONE["Done"]

    WRITE_DIRECT --> DUP{"Duplicate?"}
    WRITE_PROPOSED --> DUP
    WRITE_OVERRIDE --> DUP

    DUP -- "Yes" --> ASK_DUP["Ask: log anyway?"]
    DUP -- "No" --> SUCCESS["Relay REPLY line"]

    ASK_DUP --> DUP_REPLY{"User reply?"}
    DUP_REPLY -- "yes" --> WRITE_FORCE["Run log.sh --skip-duplicate-check"]
    DUP_REPLY -- "no" --> DONE

    WRITE_FORCE --> SUCCESS

    SUCCESS --> LEARN{"Alias learning?"}
    LEARN -- "Yes" --> DO_LEARN["Run learn_category_alias.sh"]
    LEARN -- "No" --> DONE
    DO_LEARN --> DONE
```

## How State Works

The active OpenClaw conversation model's conversation context is the state. No external storage is needed.

When OpenClaw asks "Log mcdonalds under Dining Out?" and the user replies "yes", the current conversation model resolves what "yes" refers to from the conversation history. No classify-reply script, no pending state file, and no session keys are required.

## Rules

- Script output is the only source of truth. Never answer from memory.
- Relay `REPLY:` lines verbatim.
- User-facing confirmations come from the `question` field in preview output.
- If context is lost (session restart), re-run the preview and ask again.
