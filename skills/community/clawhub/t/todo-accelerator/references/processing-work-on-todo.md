# Processing the work-on-todo Output

After running `work-on-todo`, the script returns a structured prompt. Follow these instructions:

1. Read the **Expected Results** — these are the outcomes the user expects
2. Read the **Unresolved Issues** — these are the requirements to work on
3. If the prompt mentions previous findings, read that section of the note before proceeding
4. Reference **Previous Results** if present
5. Work on the unresolved issues
6. While working:
   - Record new findings in the "Investigation and Problems" section of the note — keep entries concise (facts and conclusions only, no filler)
   - Add results aligned with targets to the "Target" section
7. When finished or blocked, call `commit` with the requirements you completed
