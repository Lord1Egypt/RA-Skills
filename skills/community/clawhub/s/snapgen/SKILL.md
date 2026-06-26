---
name: snapgen
slug: snapgen
description: Use this skill when the user asks to open, run, or automate a specific desktop application. It manages the full lifecycle of automation scripts within dedicated application folders, handling class-based automation execution. This skill relies on the Python environment and the `clicknium` package.
metadata: {"clawdbot":{"os":["win32"],"requires":{"bins": ["python","pip"]},"install":{"python -m pip install clicknium>=0.2.9"}}}
---

# Program Automator Skill

This skill is a router and manager. It ensures every application has its own dedicated folder containing both its automation class file and its capability documentation.

## Bundled Python Environment

This skill relies exclusively on the **Python environment** (accessible via the `python` command) rather than a bundled setup.

### Dynamic Recorder Resolution
Because we use the global Python environment, the `Clicknium.Recorder.exe` is located inside the system's `site-packages`.
To dynamically resolve its location (referred to below as `{RECORDER_EXE}`), use this command:
`python -c "import clicknium, os; print(os.path.join(os.path.dirname(clicknium.__file__), '.lib', 'automation', 'Clicknium.Recorder.exe'))"`

## Context Directory Structure
All resources are organized by process name in the `.\apps\` directory:
- **Folder**: `{WORKSPACE_PATH}\skills\snapgen\apps\{PROCESS_NAME}\`
- **Class File**: `...\{PROCESS_NAME}\{PROCESS_NAME}.py` (Contains a Python class with action methods)
- **Docs**: `...\{PROCESS_NAME}\{PROCESS_NAME}.md`

## Workflow

### Step 1: Identify & Normalize
Extract the program name from the user's request (e.g., "Firefox") and standardize it to a lowercase process name (e.g., `firefox`).

### Step 2: Check Existence
Check for: `apps/{PROCESS_NAME}/{PROCESS_NAME}.md` AND `apps/{PROCESS_NAME}/{PROCESS_NAME}.py`

- **IF** both exist -> Go to **Step 3: Capability Audit**.
- **IF** either is missing -> Go to **Scenario B: Creation Protocol**.

### Step 3: Capability Audit
Read `apps/{PROCESS_NAME}/{PROCESS_NAME}.md`. Compare the user's request against the "Supported Actions".

- **IF** supported -> Go to **Scenario A: Dynamic Execution**.
- **IF** NOT supported -> Go to **Scenario C: Extension Protocol**.


## Scenarios

### Scenario A: Dynamic Execution (Function Call Strategy)
Since the Python file contains a Class, we must instantiate it and call the correct method.

1.  **Analyze Source Code**:
    - Read `{WORKSPACE_PATH}\skills\snapgen\apps\{PROCESS_NAME}\{PROCESS_NAME}.py`.
    - Identify the **Class Name** (usually matches the process name, e.g., `class FirefoxAutomator`).
    - Identify the **Method Name** that matches the user's intent (e.g., `def open_url(self, url):`).

2.  **Extract Parameters**:
    - If the target method requires arguments (e.g., `url`, `text`, `filepath`), extract these values from the user's prompt.

3.  **Generate Driver Script**:
    Create a temporary Python script (e.g., `run_temp.py`) **inside the application folder** `{WORKSPACE_PATH}\skills\snapgen\apps\{PROCESS_NAME}` with the following logic. **If the executed method has a return value, it must be captured and printed directly as a Python object.**

    ```python
    import sys
    import os
    
    # Ensure Current Working Directory matches the script location
    os.chdir(r"{WORKSPACE_PATH}\skills\snapgen\apps\{PROCESS_NAME}")
    
    # Import the Specific Module from the current directory
    from {PROCESS_NAME} import {CLASS_NAME} 
    
    # Instantiate and Run
    bot = {CLASS_NAME}()
    result = bot.{METHOD_NAME}({PARAMETERS}) 
    
    # Capture output. The return value is expected to be a Python list (array) object.  
    if result is not None:  
        print(result)  
    ```

4.  **Execute (CRITICAL)**:
    Run the generated `run_temp.py` using the **global** system Python environment.
    
    **IMPORTANT:** The execution process (subprocess/terminal) **MUST set the Current Working Directory (CWD)** to the application folder. The total execution time $T$ will depend strictly on the complexity of the execution script.
    - **Command**: `python run_temp.py`
    - **Working Directory (cwd)**: `{WORKSPACE_PATH}\skills\snapgen\apps\{PROCESS_NAME}`
    
    *Failure to set the execution directory correctly will result in module import errors or missing resource failures.*

    **Error Handling - Login Required**: 
    If an execution error occurs and the error message implies that the user needs to log in:
    - Execute the command `"{RECORDER_EXE}" replay` to bring up the recorder interface.
    - Instruct the user to manually perform the login operations within the opened window and close it once finished.
    - Do **not** perform any additional operations or retries automatically after giving this instruction.

5.  **Output Processing Format**:   
    If the executed function returns a value, **it will be a Python list (array) object**. The JSON block below is *only used to illustrate the expected object's structure*:  
    ```json  
    [  
      {  
        "element": "", // corresponding locatorid
        "value": ""    // fetched value during execution, content to be output
      }  
    ]  
    ```  
    When interpreting the output, you must iterate through this array in the exact order, extract the `"value"` field from each element, and inform the user of these output values sequentially.  

6.  **Cleanup**:
    Delete `run_temp.py` from the application folder.

### Scenario B: Creation Protocol (Brand New App)
Initiate this when the application folder does not exist.

1. **Notify**: "I don't have a configuration for <Program> yet. Initiating generation..."
2. **Define Paths**:
   - `PROCESS_SKILL_PATH`: `{WORKSPACE_PATH}\skills\snapgen\apps\{PROCESS_NAME}`
   - `PYTHON_CODE_FILE`: `{PROCESS_SKILL_PATH}\{PROCESS_NAME}.py`
   - `DOC_FILE`: `{PROCESS_SKILL_PATH}\{PROCESS_NAME}.md`
   - `META_JSON_FILE`: `{PROCESS_SKILL_PATH}\meta.json`

3. **Record & Generate**:
   - Create the directory `{PROCESS_SKILL_PATH}` if it doesn't exist.
   - Run the recorder command using the `{RECORDER_EXE}` path resolved in dependencies:
     ```bash
     "{RECORDER_EXE}" replayAndGencode -p "{PROCESS_SKILL_PATH}" -o "{PYTHON_CODE_FILE}"
     ```

4. **Extract and Generate Documentation & Meta**:
   - **READ** the generated `{PYTHON_CODE_FILE}`.
   - **ANALYZE** the Python code to understand what actions were just recorded and identify properties.
   - **CREATE** `{DOC_FILE}`. Include:
     - `# {PROCESS_NAME} Automation`
     - `## Supported Actions`: List the intents realized by the code.
     - `## Automatable Elements`: List the properties (with `@property`) defined in the Python class.
   - **CREATE** `{META_JSON_FILE}` with the following structure:
     ```json
     {
       "Name": "{PROCESS_NAME}",
       "Description": "Automation for the {PROCESS_NAME} application, supporting actions such as [List of Supported Actions]."
     }
     ```
     *(Note: The automation name should be adjusted to be more user-friendly if needed. The description should be a concise summary of the skill's capabilities.)*

### Scenario C: Extension Protocol (Adding Methods)
Initiate this when the app folder exists, but the specific action is missing from the documentation.

1. **Notify**: "I know <Program>, but I need to learn this new specific action. Recording new steps..."
2. **Define Paths**:
   - `PROCESS_SKILL_PATH`: `{WORKSPACE_PATH}\skills\snapgen\apps\{PROCESS_NAME}`
   - `EXISTING_CODE`: `{PROCESS_SKILL_PATH}\{PROCESS_NAME}.py`
   - `TEMP_NEW_CODE`: `{PROCESS_SKILL_PATH}\{PROCESS_NAME}_new_feature.py`
   - `DOC_FILE`: `{PROCESS_SKILL_PATH}\{PROCESS_NAME}.md`
   - `META_JSON_FILE`: `{PROCESS_SKILL_PATH}\meta.json`

3. **Record (New Features Only)**:
   Run the recorder, saving only the new steps to the temporary file:
   ```
   "{RECORDER_EXE}" replayAndGencode -p "{PROCESS_SKILL_PATH}" -o "{TEMP_NEW_CODE}"
   ```

4. **Merge Code**:
   - **READ** both `EXISTING_CODE` and `TEMP_NEW_CODE`.
   - **MERGE** them logically:
     - Combine imports.
     - Append the new functions/logic from `TEMP_NEW_CODE` into `EXISTING_CODE`.
     - *Ensure the old logic remains intact.*
   - **SAVE** the merged content back to `EXISTING_CODE`.

5. **Update Documentation and Meta**:
   - **READ** the new content of `EXISTING_CODE` (or the diff).
   - **UPDATE** `{DOC_FILE}`:
     - Add the new capability to the "Supported Actions" list.
     - Add the newly defined properties to the "Automatable Elements" list.
     - Ensure the file accurately describes the *combined* capabilities of the script.
   - **UPDATE** `{META_JSON_FILE}`:
     - Update the "Description" to reflect the new capabilities.

6. **Cleanup & Execute**:
   - Delete `TEMP_NEW_CODE`.
   - Proceed to **Scenario A** to run the newly added method immediately (respecting the CWD requirement).