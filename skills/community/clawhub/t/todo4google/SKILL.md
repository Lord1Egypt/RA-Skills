---
name: todo4google
description: 管理todo事项，记录工作日志，并与Google Task同步。根据本地ToDo创建Goole Task，并根据完成情况更新Google Task状态。上传todo文件到Google Drive进行归档。
metadata: {"openclaw":{"emoji":"✅","requires":{"bins":["gog"]}}}

---
# Todo Manager

## 默认设置
- 基本设置
  - `GOOGLETASKLIST="openclaw"`  # 可通过用户指令自定义
  - `TODODIR="archive/todos"`  # 相对于agent工作目录
  - 默认一个todo文件包含一周的内容，每天以一级标题 `# YYYY-MM-DD` 开始
  - `FILENAME="todos-{YYYYMMDD}.md"` 其中 `YYYYMMDD` 是**当周周一的日期**，文件路径为 `{TODODIR}/{FILENAME}`

- 默认md文件模版:
  ```markdown
  # YYYY-MM-DD
  ## ToDos
  - [ ] **[{priority}] {title}**
    - taskId: xxx
    - due: yyyy-mm-dd （默认当天）
    - 第一行notes
    第二行notes（续）
    第三行notes（续）

  - [ ] **下一个任务**
    ...

  ## Works
  [一般由用户自己填写]
  ## Summary
  [可由agent根据todo和works自动生成总结]
  
  ---

  # YYYY-MM-DD+1
  ## ToDos
  ## Works
  ## Summary

  ---

  # YYYY-MM-DD+2
  ...
  ```
  **模版注意事项**：
  - 一个todo-xxx.md文件**默认包含一周**的内容，每一天的内容以一级标题 `# YYYY-MM-DD` 开始
  - 每一天的内容包括: ToDos (计划todo) → Works (实际工作内容) → Summary (总结)

## 本地操作
### FUNC-00: 确定目标md文件
- 当周周一日期为文件名，例如2026-04-19（周日），则使用2026-04-13的日期对应文件名 `todos-20260413.md`

### FUNC-01: 添加本地todo
- FUNC-00 确定目标md文件，如无则创建
- 总结用户需求，提取todo标题、优先级、截止日期、notes等信息，添加到当天的todo文件中

### FUNC-02: 解析当天todo事项
- FUNC-00 确定目标md文件，提取当天的内容
- 只解析当天的 todo 项，忽略其他内容。

**解析规则**：
1. 任务标题行 `- [ ] **[{priority}] {title}**` 依次提取:
    完成状态:status 
    优先级:priority（p0 > p1 > p2，默认p1）如无则自动添加p1
    任务标题:title 
    
2. 子行 `- taskId: xxx` → 提取 taskId
3. 子行 `- due: YYYY-MM-DD` → 提取 截止日期:due （默认当天）
4. 子行 `- xxx`（非 taskId/due/priority）→ 归入 notes
5. **多行 notes**：从第一条 notes 行开始，所有后续不包含 `taskId:`、`due:` 的行都属于该任务的 notes，直到下一个任务

### FUNC-03: 编辑当天Works
**需要用户主动触发**
- FUNC-00 确定目标md文件，提取当天的内容
- 根据用户输入，编辑当天的Works内容

### FUNC-04: 总结今日完成情况-Summary
- FUNC-00 确定目标md文件，提取当天的内容
- 根据当天的todo和works内容，自动生成当天的Summary总结
在**当天内容末尾**添加完成情况小结，格式如下：

```
---
## Summary
**已完成（N/M）**：
1. ✅ 第一项任务
2. ✅ 第二项任务

**未完成（M/N）**：
1. ❌ 第一项任务
2. ❌ 第二项任务
```

### FUNC-05: 生成下一天 todo 
- FUNC-00 确定目标md文件，提取当天的内容
- 根据当天的todo完成情况，自动生成下一天的todo计划
- **如果下一天是下周一**，则生成新的md文件  
- **注意**：如果未完成任务中包含 **taskId，due**，则保留以便后续同步
格式参照上文的 todo 任务模版。  

## Google 云端同步
### FUNC-06: 新建google task
根据当天todo创建新的google task，**仅针对本地todo中没有taskId的任务（无论是否已经标记完成）**，并将生成的taskId回写到本地todo文件中。

1. FUNC-00 确定目标md文件，提取**当天**的内容

2. 向Google Task创建新任务
对于本地todo中**没有任务id**的任务（**无论是否已经标记完成**）执行如下：
  ```bash
  gog task add {GOOGLETASKLIST} --title "[{priority}] {title}" --notes "$(printf notes)" --due {due}
  ```
**注意：并发提起tool_use, notes 注意 $(printf ...) 语法**  

3. 回写入本地todo
等待所有任务均创建完毕，更新todo文件对应内容，**并按照priority排序**, **priority要用方括号包裹**

### FUNC-07: 更新google task完成情况
根据当天todo完成情况，更新Google Task中对应任务的完成状态。**仅针对本地todo中，当天的，有taskId的任务**。

FUNC-00 确定目标md文件，提取**当天**的内容，**当天任务中，有任务id且任务已完成**的执行如下：  
  ```bash
  gog task update {GOOGLETASKLIST} {taskId} --notes "$(printf notes)" --due {due} --status "completed" 
  ```
**注意：并发提起tool_use, notes 注意 $(printf ...) 语法** 

### FUNC-08: 归档todo文件
**需要用户主动触发**
将目标文件上传到云端google drive, 默认转成Google Doc格式
```bash
gog drive upload {filePath} --convert-to doc
```
