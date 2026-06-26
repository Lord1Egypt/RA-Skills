---
name: safe-terminal-runner
description: Forces the AI to use a "temporary file + environment variable isolation" workflow for script execution, completely resolving terminal freezes and escaping errors in Windows PowerShell/Bash.
tags: [terminal, robust, backend, windows-fix]
---

# Terminal & Script Execution Rules

When executing scripts or database operations that contain complex logic, environment variables, or special characters (such as single/double quotes, parentheses, `%`, `$`, etc.) in Node.js or Python, you MUST strictly adhere to the following rules:

## 🚫 PROHIBITED
- **NEVER** use inline single-line scripts like `node -e "..."` or `python -c "..."` to execute complex logic.
- **NEVER** construct complex strings containing SQL queries, JSON parsing, or intricate regular expressions directly within terminal commands. This prevents escaping errors and command alias conflicts in environments like Windows PowerShell or Bash (e.g., misinterpreting `%` as `ForEach-Object`).

## ✅ MANDATORY PROCESS
When you need to run one-off scripts (e.g., updating database schemas, migrating data, testing APIs), you must follow this workflow:

1. **Create a Temporary File**: Generate a complete, standalone script file (e.g., `temp_update_db.js` or `temp_task.ts`) in an appropriate directory (like `scripts/` or the current working directory).
2. **Write Complete Code**: Clearly write all logic inside the file, including imports, environment variable loading, execution, and robust error handling. The script must explicitly load environment variables at the top of the file, rather than relying on external environment injection:
    ```javascript
    import 'dotenv/config'; // For ESM
    // OR
    require('dotenv').config(); // For CJS
    ```
3. **Execute the File**: Run the file in the terminal using standard commands, such as `node temp_update_db.js` or `npx tsx temp_task.ts`.
4. **Clean Up**: Regardless of whether the execution succeeds or fails, once the result is confirmed, you must immediately delete the temporary file to keep the project workspace clean.

> **NOTE**: All temporary scripts must be prefixed with `temp_`. Ensure `temp_*` is added to `.gitignore` to prevent accidental commits.

## ⚠️ ERROR HANDLING
If the terminal hangs, freezes, or displays an unexpected prompt (like waiting for user input) during execution, you must immediately stop the current operation. Assume the script triggered special escaping rules in the terminal environment, and retry using the standalone file execution method described above.