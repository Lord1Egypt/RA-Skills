# CodeBuddy Adaptation

## Default stance

CodeBuddy tasks often waste tokens in three places:

1. reading too many files too early
2. editing too much code before the scope is stable
3. running broader tests than the current decision actually needs

Treat CodeBuddy as a budgeted execution environment, not a default full-repo analysis environment.

## Default budgets

### Read budget

Start with:

- `1-3` most relevant files
- the smallest error trace or entrypoint slice
- the smallest code region that can answer the question

Do not scan the whole repository by default.

### Edit budget

Start with:

- one function
- one file
- one tightly scoped diff
- one smallest viable fix

Do not jump to module-wide or project-wide rewrites unless the user confirmed that scope.

### Test budget

Start with:

- no test run if the task is purely diagnostic
- the smallest validation possible if a fix was made
- related tests before broad tests

Do not default to a full test suite unless:

- the user asked for it
- the affected scope is large
- confidence would otherwise remain too low

## Default route in CodeBuddy

- bug or error with incomplete context -> Ask or Ask + CodeBuddy scope confirmation
- small explicit patch -> Craft with small read/edit budget
- multi-file refactor or architecture change -> Plan
- repeated failed fixes or deep specialist problem -> Expert recommendation

## CodeBuddy scope gate

When the code task is not yet scoped, ask the user to choose:

- `只诊断`
- `只读 1-3 文件`
- `只改一个点`
- `分阶段重构`

Default recommendation: `2` or `3`.

## CodeBuddy test gate

When execution implies testing, ask the user to choose:

- `不跑测试`
- `最小验证`
- `相关测试`
- `完整测试`

Default recommendation: `2` or `3`.

## Refactor rule

Any request like:

- `重构这个项目`
- `整理整个代码库`
- `统一改掉所有地方`

should default to:

1. need calibration
2. scope confirmation
3. staged execution

Do not default to one-shot refactoring.

## Good prompt examples

`这个代码任务先确认范围：1只诊断 2只读1-3文件 3只改一个点 4分阶段重构。默认建议 2 或 3。`

`如果需要验证，我建议先做最小验证，而不是直接跑完整测试。`
