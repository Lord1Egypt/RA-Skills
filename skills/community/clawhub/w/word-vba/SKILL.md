---
name: word-vba
description: "Word文档读写Skill - 基于VBA和ActiveX，支持doc/docx格式，提供完整读写、批量处理、文档合并、模板填充等功能"
metadata:
  openclaw:
    emoji: 📄
---

# Word VBA 文档处理 Skill

## 🎯 一句话定义

通过Python调用Word VBA/ActiveX，实现Word文档的完整读写、批量处理、文档合并、模板填充等高级功能。

---

## 📥 如何调用 (How to use me)

**触发语句：**
- "读取Word文档"
- "写入Word文件"
- "合并多个Word文档"
- "填充Word模板"
- "批量替换Word内容"

**需要提供的信息：**
1. **必需：** 文件路径、操作类型
2. **可选：** 格式要求、输出路径

---

## 🛠️ 核心模块

### 1. word_vba_reader - 文档读取

**功能：** 读取Word文档的文本和完整格式信息

**使用示例：**
```python
from word_vba_reader import WordReader

reader = WordReader()
result = reader.read_document("D:/docs/申请书.docx")

# 查看文档统计
print(f"段落数: {result['paragraph_count']}")
print(f"词数: {result['word_count']}")
print(f"页数: {result['pages']}")

# 遍历段落
for para in result['paragraphs']:
    print(f"文本: {para['text']}")
    print(f"字体: {para['format']['font_name']}")
    print(f"大小: {para['format']['font_size']}")
    print(f"粗体: {para['format']['bold']}")
```

---

### 2. word_vba_writer - 文档写入

**功能：** 创建新Word文档并设置格式

**使用示例：**
```python
from word_vba_writer import WordWriter

writer = WordWriter()
doc = writer.create_document()

# 添加标题
writer.add_heading(doc, "一、立项依据", level=1)

# 添加格式段落
writer.add_paragraph(doc, "这是正文内容。", {
    'font_name': '宋体',
    'font_size': 12,
    'bold': False,
    'alignment': 'justify',
    'first_line_indent': 24  # 首行缩进24磅
})

# 添加表格
table_data = [
    ["姓名", "年龄", "单位"],
    ["张三", "30", "清华大学"],
    ["李四", "28", "北京大学"]
]
writer.add_table(doc, 3, 3, table_data)

# 保存
writer.save_document(doc, "D:/output/文档.docx")
writer.close()
```

---

### 3. word_vba_utils - 高级功能

#### 3.1 文档合并

**功能：** 将多个Word文档合并为一个

**使用示例：**
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

# 合并多个章节为完整申请书
file_list = [
    "D:/chapters/摘要.docx",
    "D:/chapters/立项依据.docx",
    "D:/chapters/研究内容.docx",
    "D:/chapters/研究基础.docx"
]

utils.merge_documents(
    file_list=file_list,
    output_path="D:/output/完整申请书.docx",
    add_page_breaks=True,      # 章节间添加分页符
    keep_source_format=True     # 保留源格式
)
```

---

#### 3.2 模板填充

**功能：** 根据模板和数据生成文档

**模板示例：**
```
项目名称: {{project_name}}
项目负责人: {{leader}}
研究期限: {{start_date}} 至 {{end_date}}
申请经费: {{budget}}万元
```

**使用示例：**
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

# 填充数据
data = {
    'project_name': '振动台子结构试验关键技术研究',
    'leader': '纪金豹',
    'start_date': '2026.01',
    'end_date': '2029.12',
    'budget': '50'
}

utils.fill_template(
    template_path="D:/templates/基金模板.docx",
    data=data,
    output_path="D:/output/填充后申请书.docx"
)
```

---

#### 3.3 批量替换

**功能：** 批量替换文档中的文本

**使用示例：**
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

# 定义替换规则
replacements = {
    '2025年': '2026年',
    '面上项目': '青年基金项目',
    '50万元': '30万元'
}

utils.batch_replace(
    file_path="D:/docs/旧版本.docx",
    replacements=replacements,
    output_path="D:/output/新版本.docx"
)
```

---

#### 3.4 提取标题大纲

**功能：** 提取文档的标题结构

**使用示例：**
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

headings = utils.extract_headings("D:/docs/论文.docx")

for h in headings:
    indent = "  " * (h['level'] - 1)
    print(f"{indent}{h['level']}. {h['text']}")

# 输出:
# 1. 第一章 引言
#   1.1 研究背景
#   1.2 研究意义
# 2. 第二章 文献综述
# ...
```

---

#### 3.5 生成目录

**功能：** 为文档自动生成目录

**使用示例：**
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

utils.generate_toc(
    file_path="D:/docs/论文.docx",
    output_path="D:/output/论文_含目录.docx"
)
```

---

#### 3.6 文档比较

**功能：** 比较两个文档的差异

**使用示例：**
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

utils.compare_documents(
    doc1_path="D:/docs/初稿.docx",
    doc2_path="D:/docs/修改稿.docx",
    output_path="D:/output/差异比较.docx"
)
```

---

#### 3.7 批量处理

**功能：** 对多个文档执行相同操作

**使用示例：**
```python
from word_vba_utils import WordVBAUtils
from word_vba_writer import WordWriter

utils = WordVBAUtils()

# 定义处理函数：添加页眉
def add_header(doc):
    header = doc.Sections(1).Headers(1)
    header.Range.Text = "机密文件"
    header.Range.Font.Name = "宋体"
    header.Range.Font.Size = 10

# 批量处理
file_list = ["D:/docs/1.docx", "D:/docs/2.docx", "D:/docs/3.docx"]

utils.batch_process(
    file_list=file_list,
    processor=add_header,
    output_dir="D:/output/processed/"
)
```

---

## 💡 典型应用场景

### 场景1: 基金申请书整合
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

# 合并各章节
sections = [
    "摘要.docx",
    "一、立项依据与研究内容.docx",
    "二、研究方案.docx",
    "三、创新点.docx",
    "四、研究基础.docx"
]

utils.merge_documents(
    file_list=[f"D:/fund/{s}" for s in sections],
    output_path="D:/fund/NSFC申请书_完整版.docx",
    add_page_breaks=True
)
```

### 场景2: 批量生成证书
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

# 获奖名单
winners = [
    {'name': '张三', 'award': '一等奖', 'date': '2026-03-04'},
    {'name': '李四', 'award': '二等奖', 'date': '2026-03-04'},
    {'name': '王五', 'award': '三等奖', 'date': '2026-03-04'}
]

# 批量生成
for i, person in enumerate(winners, 1):
    utils.fill_template(
        template_path="D:/templates/证书模板.docx",
        data=person,
        output_path=f"D:/output/证书_{i}_{person['name']}.docx"
    )
```

### 场景3: 论文格式统一
```python
from word_vba_utils import WordVBAUtils

utils = WordVBAUtils()

# 统一替换期刊名称缩写
replacements = {
    'Earthquake Engineering and Structural Dynamics': 'Earthq. Eng. Struct. Dyn.',
    'Journal of Structural Engineering': 'J. Struct. Eng.',
    'Mechanical Systems and Signal Processing': 'Mech. Syst. Signal Process.'
}

utils.batch_replace(
    file_path="D:/papers/参考文献.docx",
    replacements=replacements,
    output_path="D:/papers/参考文献_缩写版.docx"
)
```

---

## ⚙️ 依赖要求

- **操作系统**: Windows（必需）
- **Microsoft Word**: 2010或更高版本（必需）
- **Python**: 3.8+
- **Python库**: `pip install pywin32`

---

## 🔧 与 docx-tools 的区别

| 特性 | word-vba | docx-tools |
|------|----------|------------|
| **依赖** | 需要Microsoft Word | 纯Python |
| **平台** | 仅Windows | 跨平台 |
| **功能** | 完整（VBA所有功能） | 基础功能 |
| **速度** | 较慢（启动Word） | 快 |
| **格式支持** | 100%（包括复杂样式） | 基本格式 |
| **批量处理** | ✅ 支持 | ✅ 支持 |
| **模板填充** | ✅ 支持 | ❌ 不支持 |
| **文档合并** | ✅ 保留格式 | ⚠️ 有限支持 |
| **目录生成** | ✅ 支持 | ❌ 不支持 |

**选择建议：**
- 需要精确格式控制、复杂操作 → **word-vba**
- 快速批量处理、跨平台需求 → **docx-tools**

---

## 🐛 故障排除

### 问题："无法创建Word应用对象"
**原因**: Word未安装或COM接口未注册
**解决**: 
1. 确保已安装Microsoft Word
2. 尝试修复Office安装
3. 以管理员身份运行

### 问题：文档被占用无法打开
**解决**: 关闭Word中已打开的该文档，或重启Word进程

### 问题：格式信息读取不完整
**解决**: 检查文档是否使用了特殊样式或模板

### 问题："ImportError: No module named 'win32com'"
**解决**: `pip install pywin32`

---

## 📝 最佳实践

1. **使用后及时关闭**: 调用 `writer.close()` 或 `utils._close_word()` 释放资源
2. **设置 visible=False**: 后台运行提高速度
3. **批量处理**: 使用 `batch_process` 而不是循环打开单个文件
4. **异常处理**: 使用 try-except 包裹代码，确保Word进程能正常关闭

---

_技能版本: v2.0_
_更新日期: 2026-03-04_
_更新说明: 添加高级功能模块（合并、模板、批量处理等）_
