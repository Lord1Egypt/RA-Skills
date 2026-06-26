# Word Document Creator Skill

## 🎯 技能描述
**工业级Word文档创建器** - 使用Word COM创建空白文档 + python-docx编辑内容的混合方案，包含三层编码防御、COM异常熔断、文件反读验证。

## 🔑 触发关键词
- "创建Word文档"
- "生成Word文件"  
- "写一个Word文档"
- "word文档创建"
- "word文件生成"

## 🛠️ 调用方式
```yaml
interpreter: D:\openclaw_project\venv\Scripts\python.exe
script: scripts/word_creator.py
args: ["--title", "{title}", "--content", "{content}", "--output", "{output_path}"]
```

## 📋 参数说明
- `title`: 文档标题（字符串）
- `content`: 内容段落列表（JSON数组字符串）
- `output_path`: 输出文件路径（完整路径）

## 🏗️ 架构设计

### **三层编码防御**
1. **环境变量级**: `os.environ['PYTHONIOENCODING'] = 'utf-8'`
2. **系统控制台级**: `os.system('chcp 65001 > nul')`
3. **Python输出流级**: `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`

### **COM异常熔断机制**
- Word COM初始化失败 → 立即终止程序（`sys.exit(1)`）
- 防止在基础组件失败的情况下继续执行
- 减少错误传播和资源泄漏

### **文件反读验证**
1. **物理存在性**: `os.path.exists()`
2. **文件大小合理性**: `os.path.getsize() > 0`
3. **文档结构完整性**: 重新打开读取验证段落数

## 🎨 样式配置
```python
WORD_STYLE_CONFIG = {
    'title_font_size': 18,      # 小二
    'normal_font_size': 12,     # 小四
    'line_spacing': 1.5,        # 1.5倍行距
    'paragraph_spacing': 12,    # 段前段后12磅
    'font_family': '微软雅黑',   # 默认字体
    'title_alignment': 1,       # 居中
    'normal_alignment': 0,      # 左对齐
}
```

## 📚 成功经验（存入mem9数据库）
- **数据库ID**: `l0dUoXsQPIKl1WF5yRBKF6369zaF2OPn`
- **存储时间**: 2026-03-30
- **关键经验**: 混合方案解决图标异常问题

## 🚀 使用示例
```python
# 直接调用技能
create_robust_word_doc(
    title="华为未来二十年",
    content_paragraphs=[
        "中国作为世界第二大经济体...",
        "从经济总量来看...",
        "未来二十年，随着科技创新..."
    ],
    output_path=r"E:\Desktop\华为未来二十年.docx"
)
```

## ⚠️ 注意事项
1. **必须安装Microsoft Word**（Office套件）
2. **使用专用Python环境**: `D:\openclaw_project\venv\Scripts\python.exe`
3. **路径使用raw string**: 避免转义问题
4. **文件占用释放**: Word COM必须调用`Quit()`释放文件

## 🔄 版本历史
- **v1.0** (2026-03-30): 初始版本，包含完整防御性代码
- **v1.1** (2026-03-30): 添加样式配置分离，函数封装