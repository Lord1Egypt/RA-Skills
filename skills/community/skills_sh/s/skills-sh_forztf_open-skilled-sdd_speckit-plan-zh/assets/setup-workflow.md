# 设置工作流程

## 初始设置步骤

### 1. 环境设置
从仓库根目录运行：
```powershell
.speckit/scripts/powershell/setup-plan.ps1 -Json
```

### 2. JSON 解析
解析 JSON 输出以获取：
- FEATURE_SPEC
- IMPL_PLAN
- SPECS_DIR
- BRANCH

### 3. 参数处理
对于参数中的单引号（如 "I'm Groot"），使用转义语法：
- 例如：'I'\\''m Groot'
- 或者尽可能使用双引号："I'm Groot"

### 4. 上下文加载
读取 FEATURE_SPEC 和 `.specify/memory/constitution.md`
加载已复制的 IMPL_PLAN 模板