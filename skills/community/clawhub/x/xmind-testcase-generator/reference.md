# gen_xmind.py API 参考文档

## 文件结构

```
gen_xmind.py
├── 核心工具函数（不要修改）
│   ├── _mid()          — 生成唯一 ID
│   ├── topic()         — 创建 XMind 节点
│   ├── P1, P3          — 优先级常量
│   ├── steps()         — 生成步骤→预期子节点列表
│   ├── case()          — 创建测试用例
│   ├── sub_module()    — 创建子模块节点
│   ├── module()        — 创建模块节点
│   └── generate_xmind() — 生成 .xmind 文件
├── build_cases()       — 用例数据（每次只修改这部分）
└── __main__            — 执行入口
```

---

## 常量

```python
P1 = ["priority-1"]  # smoke 冒烟用例（~20%）
P3 = ["priority-3"]  # normal 普通用例（~80%）
```

---

## 核心函数

### `topic(title, children=None, markers=None, note=None, labels=None)`

创建一个 XMind 节点。这是底层函数，通常不直接调用，而是通过 `case()`、`sub_module()`、`module()` 间接使用。

| 参数 | 类型 | 说明 |
|------|------|------|
| title | str | 节点标题 |
| children | list | 子节点列表 |
| markers | list | 优先级标记，如 `["priority-1"]` |
| note | str | F4 备注（前置条件） |
| labels | list | F3 标签，如 `["ai"]` |

### `steps(steps_list)`

生成带编号的 步骤→预期 子节点列表。

| 参数 | 类型 | 说明 |
|------|------|------|
| steps_list | list[tuple] | `[(步骤文本, 预期文本), ...]`，预期为空字符串 `""` 则该步骤无预期子节点 |

**示例：**
```python
steps([
    ("点击登录按钮", "弹出登录弹窗"),        # 有预期
    ("输入账号密码", ""),                      # 无预期（前置操作）
    ("点击确认", "登录成功跳转首页"),          # 有预期
])
```

生成结构：
```
├── "1、点击登录按钮"
│     └── "1、弹出登录弹窗"
├── "2、输入账号密码"          ← 无子节点
└── "3、点击确认"
      └── "3、登录成功跳转首页"
```

### `case(title, steps_list, priority=P3, note=None, labels=None)`

创建一条测试用例（测试点节点）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | str | - | 用例标题 |
| steps_list | list[tuple] | - | `[(步骤, 预期), ...]` |
| priority | list | P3 | `P1` 或 `P3` |
| note | str | None | 前置条件（F4 备注） |
| labels | list | None | 平台标签（F3），如 `["ai"]` |

**示例：**
```python
# 最简用例
case("功能入口正常展示", [
    ("打开APP首页", "功能入口按钮可见"),
])

# 完整用例（P1 + 前置条件 + 平台标签）
case("VIP用户专属功能展示",
     [("进入个人中心", "展示VIP专属功能区"),
      ("点击专属功能", "正常进入功能页面")],
     P1,
     note="前置条件：登录VIP账号",
     labels=["ai"])

# 无预期的中间步骤
case("多步骤操作流程",
     [("打开设置页面", ""),           # 前置步骤，无预期
      ("找到目标选项", ""),           # 前置步骤，无预期
      ("点击开关", "功能状态切换")],  # 最终验证
     P3)
```

### `sub_module(name, cases_list)`

创建子模块节点。

| 参数 | 类型 | 说明 |
|------|------|------|
| name | str | 子模块名称 |
| cases_list | list | 用例列表或更深层子模块列表 |

**支持嵌套：**
```python
# 子模块直接包含用例
sub_module("基础功能", [
    case("用例1", [...]),
    case("用例2", [...]),
])

# 子模块包含更深层子 tab
sub_module("执行组件", [
    sub_module("点踩", [case(...)]),
    sub_module("复制文案", [case(...)]),
    sub_module("语音播报", [case(...)]),
])
```

### `module(name, sub_modules)`

创建模块节点。

| 参数 | 类型 | 说明 |
|------|------|------|
| name | str | 模块名称 |
| sub_modules | list | 子模块列表 |

### `generate_xmind(root_title, modules_list, output_name)`

生成 `.xmind` 文件并输出统计信息。

| 参数 | 类型 | 说明 |
|------|------|------|
| root_title | str | 根节点标题（需求名） |
| modules_list | list | 模块节点列表 |
| output_name | str | 输出文件名（不含路径，自动输出到 `~/Desktop/工作/`） |

**输出示例：**
```
生成完成: /Users/xxx/Desktop/工作/XX模块_用例.xmind
用例统计: 总计 45 条, smoke 9 条 (20.0%), normal 36 条
```

---

## build_cases() 编写模板

每次生成新用例时，**只修改 `build_cases()` 函数的内容**，核心工具函数不动。

### 基础模板

```python
def build_cases():
    """构建用例数据，返回 (根标题, 模块列表, 输出文件名)"""

    # ===== 子模块1: XXX =====
    sub1 = [
        case("用例标题1", [
            ("步骤1", "预期1"),
            ("步骤2", "预期2"),
        ], P1),

        case("用例标题2", [
            ("步骤1", ""),       # 前置操作无预期
            ("步骤2", "预期2"),
        ]),
    ]

    # ===== 子模块2: YYY =====
    sub2 = [
        case("用例标题3", [
            ("步骤1", "预期1"),
        ], note="前置条件：XXX"),
    ]

    # --- 组装 ---
    modules_list = [module("模块名", [
        sub_module("子模块1名", sub1),
        sub_module("子模块2名", sub2),
    ])]

    return "需求名-模块名", modules_list, "需求名_模块名_用例.xmind"
```

### 嵌套子模块模板

```python
def build_cases():
    # 三级子模块
    sub_a1 = [case("用例A1", [...]), case("用例A2", [...])]
    sub_a2 = [case("用例A3", [...]), case("用例A4", [...])]

    sub_a = sub_module("大子模块A", [
        sub_module("小子模块A1", sub_a1),
        sub_module("小子模块A2", sub_a2),
    ])

    sub_b = [case("用例B1", [...]), case("用例B2", [...])]

    modules_list = [module("模块名", [
        sub_a,
        sub_module("子模块B", sub_b),
    ])]

    return "需求名", modules_list, "输出文件名.xmind"
```

---

## XMind 文件格式说明

生成的 `.xmind` 文件是一个 ZIP 压缩包，内含：

| 文件 | 说明 |
|------|------|
| content.json | 思维导图内容数据（节点树） |
| metadata.json | 元数据（创建者、活跃画布 ID） |
| manifest.json | 文件清单 |

无需安装任何第三方库，仅使用 Python 标准库：`json`、`zipfile`、`os`、`uuid`。

---

## 常见问题

### Q: 中文引号导致语法错误
A: Python 字符串内部的引号必须用英文引号（单引号 `'` 或转义双引号 `\"`），不能用中文引号 `""''`。

### Q: 如何调整输出目录
A: 修改 `generate_xmind()` 函数中的 `output_path`，默认输出到 `~/Desktop/工作/`。

### Q: smoke 占比不对怎么调
A: 检查每个子模块中 P1 的分配。原则：只有最核心的链路验证点标 P1，总量控制在 ~20%。

### Q: 如何忽略某些用例
A: 在用例标题前加 `#`，如 `case("#暂不测试的功能", ...)`，该节点及子节点会被忽略。
