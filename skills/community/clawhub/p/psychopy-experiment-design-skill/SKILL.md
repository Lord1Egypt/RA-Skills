# PsychoPy Experiment Design Skill

## Purpose

This skill helps users design, build, troubleshoot, and document experimental tasks using PsychoPy, PsychoJS, Pavlovia, or similar online psychology experiment platforms. It is especially suitable for psychology, cognitive neuroscience, rehabilitation, and behavioral experiments.

The skill focuses on practical implementation, clear trial structure, reliable data recording, and participant-friendly task design.

## When to Use

Use this skill when the user needs help with:

- Designing a PsychoPy Builder experiment
- Creating a trial-by-trial task structure
- Setting up blocks, mini-blocks, and practice trials
- Writing instruction pages
- Creating condition files in Excel or CSV format
- Designing tasks such as Stroop, CPT, n-back, oddball, SRTT, Go/No-Go, or reaction-time tasks
- Checking whether output data look correct
- Troubleshooting PsychoPy or PsychoJS errors
- Adapting a task for children, older adults, or clinical populations
- Making the task suitable for online deployment
- Explaining experiment timing, response rules, and data columns
- Writing a task procedure for a thesis, proposal, or ethics application

## Typical User Inputs

The user may provide:

- A task name or paradigm
- A flowchart or screenshot
- Trial timing requirements
- Number of trials, blocks, or mini-blocks
- Stimulus materials
- Response keys
- Target and non-target definitions
- PsychoPy screenshots
- Error messages
- Data files such as CSV or Excel files
- Requirements for online deployment

If the user provides screenshots, infer the likely PsychoPy Builder structure and explain concrete steps.

## Core Workflow

### 1. Define the Experimental Logic

Identify:

- What the participant sees or hears
- What the participant needs to do
- What counts as a correct response
- What variables need to be recorded
- How many trials are needed
- How trials are grouped into blocks or mini-blocks
- Whether practice and feedback are needed

### 2. Build the Trial Timeline

Represent each trial clearly, for example:

```text
Fixation: 500 ms
Stimulus: 1000 ms
Response window: 2000 ms
Blank screen / ITI: 500 ms
```

For clinical or child participants, avoid overly fast presentation and provide adequate practice.

### 3. Design the Builder Structure

Translate the task into PsychoPy Builder components:

```text
instructions
practice_trials loop
practice_feedback
formal_instructions
block_loop
trial_loop
break_screen
ending
```

Explain what each routine and loop should contain.

### 4. Prepare the Condition File

Condition files should usually include columns such as:

```text
trial_index
block
mini_block
stimulus
condition
correct_answer
is_target
duration
feedback_text
```

For reaction-time tasks, include correct response keys and target labels.

### 5. Check Data Recording

Important data columns may include:

- stimulus identity
- condition
- correct response
- actual response
- accuracy
- reaction time
- block number
- trial number
- target / non-target label
- missed response

For online studies, ensure that resources are uploaded and paths are compatible with PsychoJS.

### 6. Troubleshoot Errors

Common problems include:

- Missing resource files
- Incorrect file paths
- Components starting at the wrong time
- Loops not connected correctly
- Conditions file not selected
- Unsupported Python code in PsychoJS
- Wrong variable names
- Response component not saving data
- Stimuli appearing only after a click
- Practice loop not ending
- Formal trials not starting

When diagnosing errors, prioritize the likely Builder structure and timing settings before suggesting complex code changes.

## Output Requirements

The output should be practical and step-by-step. When possible, provide:

- Recommended Builder routines
- Loop nesting structure
- Component settings
- Example condition-file columns
- Example code snippets if needed
- Data-checking logic
- A concise description suitable for a research proposal

Use clear headings such as:

```text
1. Overall Task Structure
2. Builder Setup
3. Condition File Design
4. Timing Settings
5. Response Recording
6. Data Output Check
7. Common Problems
```

## Special Considerations

### For Clinical Participants

Tasks should be:

- Simple to understand
- Not too fast
- Not too long
- Divided into blocks with breaks
- Supported by practice trials
- Designed with clear instructions
- Tolerant of slower reaction times

### For Online Deployment

Check:

- Whether all files are in the resources folder
- Whether image/audio file paths are relative paths
- Whether code components are compatible with JavaScript
- Whether the experiment works in the browser before formal data collection

### For Data Quality

Recommend excluding or flagging trials with:

- No response
- Extremely fast responses
- Extremely slow responses
- Incorrect key presses
- Technical interruptions

Do not claim data are valid based only on file existence. Check trial counts, target counts, missing responses, accuracy pattern, and reaction-time distribution.

## Example Prompts

```text
我需要用 PsychoPy 做一个 oddball 程序，请告诉我 Builder 里每一步怎么设置。
```

```text
请帮我把这个 CPT 表格拆分成两个 block。
```

```text
这个 PsychoPy 数据对吗？请帮我检查 target 数量、反应和正确率。
```

```text
我的任务上传到 Pavlovia 后图片不显示，可能是什么原因？
```

```text
请帮我写一段实验流程，用于开题报告或伦理申请。
```

## Example Output Style

For a task design request, use a concrete structure:

```text
Routine 1: instruction
- Text component: task instructions
- Keyboard component: press space to continue

Routine 2: fixation
- Text component: +
- Duration: 0.5 s

Routine 3: stimulus
- Image or text component: $stimulus
- Keyboard component: record response
- Duration: 2 s

Loop: trials
- Conditions file: conditions.xlsx
- Number of repetitions: 1
```

For data checking, summarize clearly:

```text
The data file contains 40 formal trials. There are 8 target trials and 32 non-target trials. No missing responses were found. The target count matches the task design, so the basic structure appears correct.
```
