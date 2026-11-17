# NotebookLM CLI Quick Reference

## Setup
```bash
pip install notebooklm
notebooklm login
```

## Common Commands

```bash
notebooklm list                              # List notebooks
notebooklm create "Title"                    # Create notebook
notebooklm use <id>                         # Set active notebook
notebooklm status                           # Show current context
notebooklm summary                          # Get summary
notebooklm ask "question"                    # Chat
notebooklm ask "question" --json             # With citations
notebooklm source add "https://..."         # Add URL
notebooklm source list                       # List sources
notebooklm generate slide-deck "prompt"     # Generate slides
notebooklm generate quiz "prompt"           # Generate quiz
notebooklm artifact list                     # List artifacts
notebooklm artifact poll <id>               # Poll artifact status
notebooklm download slide-deck --format pptx  # Download
```

## Artifact Types
slide-deck, quiz, flashcards, infographic, report, audio, video, mind-map, data-table

## Poll Loop (for generation)
```bash
for i in 1 2 3 4 5 6 7 8 9 10; do
  status=$(notebooklm artifact poll <id> | grep -oP "status='\K[^']+")
  echo "[$i] $status"
  [ "$status" = "completed" ] && break
  sleep 15
done
```
