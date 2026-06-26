# skill_fix_workflow - 工作流固化技能 V3.0

## 触发指令

用户发送以下指令时激活：
- `固化当前主题的工作流`
- `固化「XXX 主题」的工作流`
- `把这个流程固化为自动化程序`

## 核心架构

**拼接器（Workflow Joiner）** - 不内置业务，只做拼接

```
执行 1 → 执行 2 → 执行 3 → 输出
```

## 工作流程

1. **提取执行链** - 从对话里提取顺序执行的 Skill/Tool/Function
2. **识别参数** - 把用户输入过的值变成可配置参数
3. **拼接调用** - 直接拼接真实函数，不生成伪代码
4. **询问输出** - 屏幕 / 文件 / API / 网页
5. **包裹异常** - 统一三级异常装饰器

## 三级异常（统一装饰器）

| 等级 | 类型 | 处理方式 |
|------|------|----------|
| Level 1 | 临时错误（网络/超时） | 自动重试，不打扰用户 |
| Level 2 | 资源失效但可替换 | 自动搜索替换 → 汇报用户 |
| Level 3 | 无法修复/无资源 | 停止执行 → 强告警 |

## 输出方式

- **屏幕**: `output_screen()`
- **文件**: `output_file(path)`
- **API**: `output_api(url)`
- **网页**: `output_web()`

## 示例

### 用户对话
```
用户：帮我搜索 AI 相关新闻
助手：已调用 skill_search(keyword="AI", limit=10)
用户：保存到 result.csv
助手：已调用 tool_file_save(data, path="result.csv")
```

### 固化后程序
```python
params = {
    "keyword": "AI",
    "limit": 10,
    "output_file": "result.csv"
}

@level3_wrapper
def run():
    data = skill_search(keyword=params["keyword"], limit=params["limit"])
    tool_file_save(data, path=params["output_file"])
    output(data)
```

## 文件结构

```
skill_fix_workflow/
├── SKILL.md              # 本文件
├── skill_fix_workflow.py # 主入口
├── joiner.py             # 拼接器核心
├── chain_extractor.py    # 执行链提取
├── param_recognizer.py   # 参数识别
├── exception_wrapper.py  # 统一异常装饰器
└── output_handler.py     # 输出处理
```
