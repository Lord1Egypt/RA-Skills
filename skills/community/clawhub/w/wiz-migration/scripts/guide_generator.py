#!/usr/bin/env python3
"""
为知笔记导出指南生成器
将导出要求转换为 Markdown 模板
"""

from pathlib import Path
from datetime import datetime


def generate_export_guide(export_dir, output_file=None):
    """
    生成导出操作指南 Markdown 文件
    
    Args:
        export_dir: 导出目录路径
        output_file: 输出文件路径，默认使用当前时间戳
        
    Returns:
        str: 生成的指南文件路径
    """
    export_path = Path(export_dir)
    
    # 生成文件名
    if output_file:
        guide_path = Path(output_file)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        guide_path = Path(f"wiz_export_guide_{timestamp}.md")
    
    guide_path = guide_path.resolve()
    
    # 生成 Markdown 内容
    content = f"""# 为知笔记导出操作指南

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 导出目录: {export_path}

## ⚠️  重要提醒

**这一步是为迁移做准备，请务必在迁移前完成！**

## 📋 导出前准备

### 1. 整理笔记

在开始导出前，建议先将为知笔记中要迁移的所有目录和文档
移动到同一个父目录下，这样可以在一次导出中完成所有内容的转换。

步骤：
1. 在左侧笔记本列表中，右键要导出的笔记本
2. 选择"移动到" → 选择目标笔记本或创建新笔记本
3. 重复直到所有要迁移的笔记都在同一父目录下

### 2. 确认导出设置

**必须选择正确的导出格式**，否则附件会被内嵌或丢失！

---

## 🚀 导出操作步骤

### 步骤一：选中要导出的内容

1. 在左侧笔记本列表中，选中要导出的笔记本
2. 如果要导出多个笔记本，可以按住 Ctrl 多选
3. 或选中父目录下的所有子笔记本

### 步骤二：开始导出

1. 右键点击选中的笔记本
2. 在右键菜单中选择 **"导出文件"**
3. 选择 **"导出 HTML"** 选项

### 步骤三：配置导出选项（关键！）

在弹出的导出对话框中，**必须** 设置以下选项：

#### ✅ 必须选择的选项

- **"导出为多个网页文件（含附件）"**
  - ⚠️  **不要**选择"单个 HTML 文件"！  
     否则附件会被 base64 内嵌到 HTML 中，难以分离
  
- **"保持目录结构"**（如果可用）
  - 这样导出后能保留笔记本的层级关系

#### ❌ 不要勾选的选项

- ~~"渲染 Markdown 笔记"~~
  - 这会丢失原始结构，笔记可能格式错乱
  
- ~~"导出为单个 HTML 文件"~~
  - 附件会内嵌，无法单独使用

#### 📁 导出位置

**目标文件夹：**

```
{export_path}
```

- 点击"浏览"按钮
- 选择或创建导出文件夹
- **建议使用空文件夹**，避免文件冲突

### 步骤四：开始导出

1. 确认选项无误后，点击 **"确定"** 或 **"导出"**
2. 等待导出完成（时间取决于笔记数量）
3. 如果导出中断，可以重新导出相同内容，会覆盖已有的

---

## 🔍 导出后检查

导出完成后，请按照以下清单检查：

### 目录结构检查

你的导出文件夹应该有这样的结构：

```
{export_path.name}/
├── 笔记本1/
│   ├── 笔记1.html
│   ├── 笔记1_files/
│   │   ├── 图片1.png
│   │   ├── 图片2.jpg
│   │   └── 附件.pdf
│   └── 笔记2.html
├── 笔记本2/
│   ├── 笔记3.html
│   └── 笔记3_files/
└── ...
```

**检查要点：**

1. ✅ 每个 `.html` 文件旁边都有一个同名 `_files` 文件夹
2. ✅ `_files` 文件夹中包含实际的图片和附件文件
3. ✅ 附件文件不是空的（检查文件大小）

### 内容检查

1. 随便打开一个 `.html` 文件
2. 检查图片是否能正常显示
3. 检查附件链接是否正常（如果是超链接）
4. 检查格式是否基本正常

### 路径检查

在浏览器中打开的 HTML 文件，其附件路径应该是相对路径，例如：

```html
<img src="笔记1_files/图片1.png">
```

**如果看到类似这样的路径，说明导出正确：**
- ✅ `笔记1_files/xxx.png` （正确，相对路径）
- ✅ `./笔记1_files/xxx.png` （正确）

**如果看到这些，说明有问题：**
- ❌ `file:///C:/Users/...` （绝对路径，可能无法在其他电脑使用）
- ❌ 长串的 `data:image/png;base64,...` （附件被内嵌了，选错选项）

---

## ⚠️  常见问题

### Q1: 没有看到"导出为多个网页文件"选项？

A: 为知笔记不同版本界面不同：
- PC 客户端：右键 → 导出文件 → 选择"HTML" → 在对话框中选"多个网页文件"
- 网页版：可能导出功能有限，建议使用客户端
- Mac 版：选项可能略有不同，但原理相同

### Q2: 导出的 HTML 文件打不开？

A: 
1. 检查是否用浏览器打开（不是用记事本）
2. 如果双击打不开，右键选择"打开方式" → 浏览器
3. 检查文件是否损坏（大小是否过小）

### Q3: 图片显示为空白或破损图标？

可能原因：
1. 导出时没有选择"含附件"选项
2. `_files` 文件夹和 `.html` 不在同一目录
3. 文件路径被修改过
4. 浏览器安全限制：有些浏览器会阻止本地文件访问

**解决方法：**
1. 确认 `_files` 文件夹存在且不为空
2. 确保没有移动 `.html` 或 `_files` 的位置
3. 尝试使用 Chrome/Edge 浏览器打开
4. 可以尝试将整个导出文件夹放到 Web 服务器下测试

### Q4: 附件链接不可用？

为知笔记导出的 HTML 中，附件可能是：
- 图片：嵌入在 HTML 中（显示正常）
- 文件：作为超链接存在（需要点击下载）

如果附件链接无效：
1. 检查 `_files` 文件夹中是否有对应文件
2. 检查文件名是否匹配（大小写敏感）
3. 如果是外部链接，可能需要网络连接

---

## ✅ 导出完成检查清单

完成检查后，打勾 ✅ 确认：

- [ ] 已在为知笔记中完成 HTML 导出（多个网页文件）
- [ ] 导出到指定文件夹（或已告知迁移人员）
- [ ] 文件夹中有多个子文件夹（笔记本名称）
- [ ] 每个子文件夹中有 `.html` 文件和 `_files` 文件夹
- [ ] 至少打开了 3 个 HTML 文件，图片/附件都能正常显示
- [ ] 附件文件大小正常（不是 0 字节）
- [ ] 已关闭为知笔记（避免文件被占用）

---

## 📞 需要帮助？

如果遇到问题：
1. 仔细阅读本指南的常见问题部分
2. 检查导出选项是否正确（这是最常见的问题）
3. 确认是否为最新版为知笔记
4. 截取导出对话框和目录结构的截图

---

## 🎯 下一步

导出完成后，请返回迁移向导，选择"自动迁移附件"或"手动迁移附件"。

迁移向导会：
- ✅ 自动复制所有 `_Attachments` 目录
- ✅ 智能跳过已存在的文件
- ✅ 保持目录结构不变
- ✅ 提供详细的进度和统计

祝你迁移顺利！

---

*本指南由为知笔记迁移向导自动生成*
"""
    
    # 写入文件
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(guide_path)


def append_migration_log(export_dir, status, notes=""):
    """
    记录导出操作日志
    
    Args:
        export_dir: 导出目录
        status: 状态（completed/failed/partial）
        notes: 备注信息
    """
    log_path = Path("migration_log.json")
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "export_dir": export_dir,
        "status": status,
        "notes": notes
    }
    
    if log_path.exists():
        import json
        with open(log_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(log_entry)
    
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    
    return str(log_path)


if __name__ == "__main__":
    # 测试
    test_dir = input("测试导出目录路径: ").strip() or r"C:\Wiz_Export"
    output = generate_export_guide(test_dir)
    print(f"指南已生成: {output}")
