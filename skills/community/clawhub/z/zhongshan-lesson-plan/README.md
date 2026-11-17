# zhongshan-lesson-plan — 中专教案模板填充技能

> 基于中专教案模板（.docx），自动生成并填写教案内容。

## 快速开始

### 1. 安装依赖

```bash
pip install lxml
```

### 2. 准备文件

将 `中专教案模板.docx` 放在项目目录中，准备好教案主题和课时数。

### 3. 运行

```bash
python fill_lesson_plan.py \
  --template 中专教案模板.docx \
  --topic "51单片机的定时器T0工作原理及编程" \
  --hours 2 \
  --teacher "张老师" \
  --output 生成的教案.docx
```

### 4. 验证

```bash
python verify_output.py 生成的教案.docx
```

## 技能说明

本技能解决的核心问题是：**如何在保持 .docx 模板表格结构完全不变的前提下，自动填充教案内容。**

### 关键技术点

1. **不使用 python-docx** — 因为它会破坏 vMerge（纵向合并单元格）属性
2. **使用 zipfile + lxml** — 直接操作 .docx 的底层 XML 结构
3. **自动课程名称推断** — 根据教案主题关键词匹配课程名
4. **完整验证机制** — 确保行数、单元格数、vMerge、标签全部正确

## 文件结构

```
zhongshan-lesson-plan/
├── SKILL.md              # 技能说明文档
├── README.md             # 本文件 — 详细使用指南
├── fill_lesson_plan.py   # 教案生成脚本
├── verify_output.py      # 验证脚本
├── templates/
│   └── 中专教案模板.docx  # 模板文件
└── examples/
    ├── example_fill.py   # 使用示例
    └── sample_output.docx  # 示例输出
```

## 模板结构

| 行号 | 字段 | 单元格数 | 说明 |
|------|------|---------|------|
| R1 | 授课教师/课程名称 | 4 | gridSpan 合并 |
| R2 | 授课教材 | 2 | gridSpan=9 |
| R3 | 授课班级 | 2 | gridSpan=9 |
| R4 | 授课内容/时长 | 4 | gridSpan 合并 |
| R5-R7 | 教学目标 | 3× | vMerge 纵向合并 |
| R8 | 思政元素 | 2 | gridSpan=9 |
| R9 | 重点难点 | 2 | gridSpan=9 |
| R10 | 教法学法 | 2 | gridSpan=9 |
| R11 | 教学过程 | 1 | 全行合并 |
| R12 | 三列表头 | 3 | 6列/3列/1列 |
| R13 | 教学内容 | 3 | 主内容区 |
| R14 | 作业/评价 | 4 | gridSpan 合并 |
| R15 | 教学反思 | 2 | gridSpan=9 |

## 课程名称推断

| 关键词 | 课程名 |
|--------|--------|
| MOS/MOSFET/半导体 | 模拟电子技术基础 |
| 51单片机/定时器/Keil | 单片机原理与应用 |
| C语言/指针/数组 | C程序设计 |
| 数字电路/逻辑门 | 数字电子技术基础 |
| PLC/梯形图 | PLC应用技术 |
| 嵌入式/Linux/STM32 | 嵌入式系统设计 |
| 数据库/SQL | 数据库原理与应用 |
| 计算机网络/TCP/IP | 计算机网络 |

## 许可证

MIT License
