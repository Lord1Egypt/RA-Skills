---
name: zhongshan-lesson-plan
description: 中专教案模板填充——分析docx模板表格结构，生成教案内容，用直接XML操作填充模板文件
category: productivity
---

# 中专教案模板填充技能

基于中专教案模板（.docx），自动生成并填写教案内容。

## 触发条件

用户提供 docx 模板文件 + 教案主题 + 课时数，要求填表生成教案。

**可选参数：** 授课教师、授课班级、授课教材。缺失时按默认规则填充。

## 默认填充规则

| 字段 | 默认值 | 说明 |
|------|--------|------|
| 授课教师 | 刘某某 | 用户未提供时自动填充 |
| 课程名称 | 根据教案主题推断 | 从主题关键词匹配课程名，见下方映射表 |
| 授课班级 | 22级电子信息1班 | 用户未提供时的默认班级 |
| 授课教材 | 《模拟电子技术基础》（第5版） | 默认教材 |

## 技术原理

**核心挑战：** Microsoft Word .docx 文件使用 XML 格式存储内容，其中表格的纵向合并单元格（vMerge）是一个特殊属性。`python-docx` 库在读写时会**破坏 vMerge 属性**，导致合并单元格变成独立单元格。

**解决方案：** 使用 `zipfile` + `lxml` 直接操作 .docx 文件的 XML 底层结构，完全绕过 python-docx，确保 vMerge 和其他表格格式零损坏。

## 工作流程

### 第一步：分析模板结构

在编写教案内容之前，必须先分析模板的表格结构。

```bash
# 从docx中提取document.xml
python3 -c "
import zipfile
docx_path = r'模板文件路径'
with zipfile.ZipFile(docx_path) as z:
    with z.open('word/document.xml') as f:
        print(f.read().decode('utf-8'))
"
```

然后检查 `document.xml` 中的 `<w:tbl>` 部分，统计每一行（`<w:tr>`）的单元格数、gridSpan 和 vMerge 属性。

### 第二步：中专教案模板结构详解

**模板：中专教案模板.docx**

| XML行索引 | 原始行号 | 字段 | 单元格数 | 说明 |
|-----------|---------|------|---------|------|
| 0 | R1 | 授课教师/课程名称 | 4 | ci1内容区gridSpan=2, ci3内容区gridSpan=6 |
| 1 | R2 | 授课教材 | 2 | ci1内容区gridSpan=9 |
| 2 | R3 | 授课班级 | 2 | ci1内容区gridSpan=9 |
| 3 | R4 | 授课内容/授课时长 | 4 | ci1内容区gridSpan=7, ci3=授课时长标签, ci4空 |
| 4 | R5 | 教学目标+知识目标 | 3 | ci0 vMerge=restart, ci1标签, ci2内容区gridSpan=8 |
| 5 | R6 | (vMerge续)+能力目标 | 3 | ci0 vMerge, ci1标签, ci2内容区gridSpan=8 |
| 6 | R7 | (vMerge续)+素质目标 | 3 | ci0 vMerge, ci1标签, ci2内容区gridSpan=8 |
| 7 | R8 | 思政元素 | 2 | ci0标签, ci1内容区gridSpan=9 |
| 8 | R9 | 教学重点与难点 | 2 | ci0标签, ci1内容区gridSpan=9 |
| 9 | R10 | 教法和学法 | 2 | ci0标签, ci1内容区gridSpan=9 |
| 10 | R11 | 教学过程（标题） | 1 | 全行合并gridSpan=10 |
| 11 | R12 | 三列表头 | 3 | ci0(6列), ci1(3列), ci2(1列) |
| 12 | R13 | **主教学内容区** | 3 | ci0=教学环节内容, ci1=教师活动, ci2=学生活动 |
| 13 | R14 | 课后作业/评价方式 | 4 | ci0标签, ci1内容区gridSpan=4, ci2标签gridSpan=2, ci3内容区gridSpan=3 |
| 14 | R15 | 教学反思与改进建议 | 2 | ci0标签, ci1内容区gridSpan=9 |

**总行数：15行**

### 第三步：使用直接XML操作填充内容

**完整代码模板：**

```python
import zipfile
import os
from lxml import etree

# ===== 配置 =====
src = r'模板文件路径'    # 原始模板
out = r'输出文件路径'     # 生成的教案

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

# ===== 读入XML =====
with zipfile.ZipFile(src, 'r') as zin:
    doc_xml = zin.read('word/document.xml')
root = etree.fromstring(doc_xml)

# 找到表格
body = root.find(W + 'body')
tbl = body.find(W + 'tbl')
rows = tbl.findall(W + 'tr')

# ===== 创建格式化段落 =====
def make_paragraph(text, alignment='left'):
    """创建带格式的段落元素"""
    p = etree.SubElement(etree.Element('dummy'), W + 'p')
    pPr = etree.SubElement(p, W + 'pPr')
    
    # 对齐方式
    jc = etree.SubElement(pPr, W + 'jc')
    jc.set(W + 'val', alignment)
    
    # 行间距
    sp = etree.SubElement(pPr, W + 'spacing')
    sp.set(W + 'before', '20')
    sp.set(W + 'after', '20')
    sp.set(W + 'line', '320')
    sp.set(W + 'lineRule', 'auto')
    
    # 运行（Run）
    r = etree.SubElement(p, W + 'r')
    rPr = etree.SubElement(r, W + 'rPr')
    
    # 字体设置
    rf = etree.SubElement(rPr, W + 'rFonts')
    rf.set(W + 'ascii', '宋体')
    rf.set(W + 'hAnsi', '宋体')
    rf.set(W + 'eastAsia', '宋体')
    
    # 字号（21 = 10.5pt）
    sz = etree.SubElement(rPr, W + 'sz')
    sz.set(W + 'val', '21')
    szCs = etree.SubElement(rPr, W + 'szCs')
    szCs.set(W + 'val', '21')
    
    # 文本内容
    t = etree.SubElement(r, W + 't')
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return p

# ===== 填充单元格内容 =====
# 清除单元格中的所有段落
cell = rows[row_index].findall(W + 'tc')[cell_index]
for p in cell.findall(W + 'p'):
    cell.remove(p)

# 写入新内容（支持多段落）
if isinstance(content, str):
    if content.strip():
        cell.append(make_paragraph(content))
else:
    for line in content:
        if line.strip():
            cell.append(make_paragraph(line))

# ===== 写回文件 =====
new_doc_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
if os.path.exists(out):
    os.remove(out)
with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, new_doc_xml)
            else:
                zout.writestr(item, zin.read(item.filename))

print(f'✅ 教案已生成: {out}')
```

### 第四步：验证

填写完成后必须验证以下项：

```python
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
with zipfile.ZipFile(output_path, 'r') as z:
    doc_xml = z.read('word/document.xml')
root = etree.fromstring(doc_xml)
rows = root.findall('.//' + W + 'tr')

# 1. 行数检查
assert len(rows) == 15, f"行数错误: 期望15, 实际{len(rows)}"

# 2. 每行单元格数检查
expected_cells = [4, 2, 2, 4, 3, 3, 3, 2, 2, 2, 1, 3, 3, 4, 2]
for i, row in enumerate(rows):
    cells = row.findall(W + 'tc')
    assert len(cells) == expected_cells[i], \
        f"R{i+1} 单元格数错误: 期望{expected_cells[i]}, 实际{len(cells)}"

# 3. vMerge检查
r5_vm = rows[4].findall(W + 'tc')[0].find(W + 'tcPr').find(W + 'vMerge')
assert r5_vm is not None and r5_vm.get(W + 'val') == 'restart', "R5 vMerge错误"
r6_vm = rows[5].findall(W + 'tc')[0].find(W + 'tcPr').find(W + 'vMerge')
assert r6_vm is not None and 'val' not in r6_vm.attrib, "R6 vMerge错误"

print('✅ 所有验证通过！')
```

### 单元格索引映射速查

| 位置 | 索引 (行, 列) | 字段 | 说明 |
|------|-------------|------|------|
| 基本信息 | (0, 0) | 授课教师标签 | 不要修改 |
| 基本信息 | (0, 1) | 授课教师内容 | 填入姓名 |
| 基本信息 | (0, 2) | 课程名称标签 | 不要修改 |
| 基本信息 | (0, 3) | 课程名称内容 | 填入课程名 |
| 基本信息 | (1, 1) | 授课教材 | 填入教材 |
| 基本信息 | (2, 1) | 授课班级 | 填入班级 |
| 基本信息 | (3, 1) | 授课内容 | 填入教学内容 |
| 基本信息 | (3, 3) | 授课时长 | 填入课时数 |
| 目标 | (4, 2) | 知识目标 | 多段落列表 |
| 目标 | (5, 2) | 能力目标 | 多段落列表 |
| 目标 | (6, 2) | 素质目标 | 多段落列表 |
| 思政 | (7, 1) | 思政元素 | 多段落列表 |
| 重点难点 | (8, 1) | 教学重点与难点 | 多段落列表 |
| 教法学法 | (9, 1) | 教法和学法 | 多段落列表 |
| 教学过程 | (12, 0) | 教学环节与内容 | 多段落列表 |
| 教学过程 | (12, 1) | 教师活动 | 多段落列表 |
| 教学过程 | (12, 2) | 学生活动 | 多段落列表 |
| 作业 | (13, 1) | 课后作业 | 多段落列表 |
| 作业 | (13, 3) | 评价方式 | 多段落列表 |
| 反思 | (14, 1) | 教学反思与改进 | 多段落列表 |

**注意：** 所有索引均为 0-based。

## 课程名称推断规则

根据教案主题关键词自动推断课程名称：

| 主题关键词 | 推断课程名称 |
|-----------|-------------|
| MOS/MOSFET/NMOS/PMOS/CMOS/半导体/JFET | 模拟电子技术基础 |
| 51单片机/定时器/中断/Keil/AT89S51/PWM | 单片机原理与应用 |
| C语言/指针/数组/结构体/链表 | C程序设计 |
| 数字电路/逻辑门/触发器/Karnaugh/布尔 | 数字电子技术基础 |
| 传感器/ADC/DAC/滤波/运算放大器 | 传感器与检测技术 |
| 自动控制/PID/传递函数/频域/根轨迹 | 自动控制原理 |
| 通信原理/调制解调/香农/信道编码 | 通信原理 |
| 微机原理/汇编/总线/中断/接口 | 微机原理与接口技术 |
| 信号与系统/傅里叶/拉普拉斯/Z变换 | 信号与系统 |
| 电机/变压器/电力电子/逆变器 | 电力电子技术 |
| PLC/梯形图/步进电机/伺服 | PLC应用技术 |
| PCB/Altium/布线/封装/EDA | EDA技术与PCB设计 |
| 嵌入式/Linux/ARM/RTOS/STM32 | 嵌入式系统设计 |
| 无线/WIFI/BLE/LoRa/NB-IoT/物联网 | 物联网技术概论 |
| 人工智能/深度学习/神经网络/卷积 | 人工智能基础 |
| 数据库/SQL/ER图/事务/索引 | 数据库原理与应用 |
| 计算机网络/TCP/IP/OSI/路由协议 | 计算机网络 |
| 其他未匹配 | 根据主题自行推断合理课程名 |

**推断逻辑：** 提取主题中的核心技术词，对照关键词表匹配课程名。

## 教案内容编写指南

### 教学环节应覆盖

1. **导入新课**（5-10% 课时）— 情境创设、问题引入、激发兴趣
2. **知识讲授**（30-40% 课时）— 分小节讲解核心知识点
3. **原理分析**（15-20% 课时）— 深入讲解原理
4. **实例演示**（10-15% 课时）— 结合案例或代码演示
5. **课堂练习**（10-15% 课时）— 学生动手实践
6. **课堂小结**（5分钟）— 知识梳理、重点回顾
7. **布置作业**（5分钟）— 课后巩固、预习引导

### 教师活动要素

展示（PPT/实物/图片/视频）→ 讲授（板书/讲解/推导）→ 演示（操作/编程/实验）→ 提问（引导思考/检查理解）→ 指导（巡视/答疑/点评）→ 总结（归纳/思维导图）

### 学生活动要素

观察（看演示/看图片/看动画）→ 思考（回答问题/分析案例）→ 记录（笔记/公式/流程图）→ 操作（编程/实验/计算）→ 讨论（小组交流/互助）→ 练习（独立完成/互评）

## 注意事项（重要！）

- ⛔ **禁止使用 python-docx 写入内容**（会破坏 vMerge 纵向合并单元格）
- ✅ 必须使用 zipfile + lxml 直接操作 XML
- ⚠️ lxml 的 `element.set(namespace, key, value)` 三个参数用逗号分隔，不是嵌套括号
- 字体统一为宋体，字号 10.5pt（XML 中 sz=21）
- 教学环节与教学内容列的段落用左对齐，表头用居中
- 所有单元格索引用 0-based：`(row_index, cell_index)`
- 不要修改原有标签单元格的内容（如"授课教师"、"1.4教学目标"等）
- 写完后**务必验证** vMerge 是否完整、行数是否正确
- 长文本使用列表格式：`['段落1', '段落2', '', '段落3']`，空字符串表示分段

## 常见问题

### Q: 为什么不用 python-docx？

A: python-docx 在处理 .docx 时会重新生成 XML，过程中丢失 vMerge 属性。vMerge 是 Word 表格纵向合并单元格的标记，丢失后合并单元格会展开为独立单元格，整个表格结构崩溃。使用 zipfile+lxml 直接操作 XML 可以完全保留原始格式。

### Q: 如果模板不是中专教案模板版本怎么办？

A: 本技能专为中专教案模板（15行表格）设计。如使用其他模板，需先分析模板结构，调整行索引和单元格索引映射。

### Q: 如何添加新的主题课程？

A: 在课程名称推断规则表中添加新的关键词映射即可。
