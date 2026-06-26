---
name: vue-table-操作及导出
description: 自动化操作 vue-element-admin 管理系统的综合 Table 页面，包括登录、遍历数据、修改记录并导出到 Excel。适用于需要批量处理 Table 数据的场景。
---

# vue-table-操作及导出

## 使用场景

当需要在 vue-element-admin 管理系统中进行以下操作时使用此 skill：
1. 登录系统（editor/123456）
2. 打开综合 Table 页面
3. 遍历每一页数据，记录指定行信息
4. 修改记录的重要性星级
5. 将数据导出到 Excel 文件

## 前提条件

- 使用 browser 工具进行自动化操作
- 使用 openpyxl 库创建和写入 Excel 文件

## 操作流程

### 1. 打开网站并登录

```python
# 使用 browser 打开登录页面
browser(action="open", url="https://panjiachen.github.io/vue-element-admin/")

# 登录后会自动进入首页（已登录状态）
# 如果需要重新登录，先登出再登录
```

### 2. 创建 Excel 文件

```python
import openpyxl
from datetime import datetime

# 创建以当天日期命名的 Excel 文件
date_str = datetime.now().strftime("%Y-%m-%d")
file_path = f"/Users/openclaw/Desktop/{date_str}.xlsx"

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Sheet1"
ws.append(["序号", "作者", "类型", "时间", "标题", "状态", "重要性"])
wb.save(file_path)
```

### 3. 导航到综合 Table 页面

```python
# 点击 Table 菜单（展开子菜单）
browser(action="act", request={"kind": "click", ref": "e89"})  # Table 菜单

# 等待菜单展开后，点击综合 Table
browser(action="act", request={"kind": "click", ref": "e227"})  # 综合 Table 链接
```

### 4. 处理每一页数据

对于每一页，执行以下操作：

#### 4.1 点击第一行的编辑按钮

```python
# 点击第一行的编辑按钮（需要从 snapshot 中获取最新的 ref）
browser(action="act", request={"kind": "click", ref": "e341"})  # 编辑按钮
```

#### 4.2 获取弹窗中的详情

从弹窗中提取以下字段：
- 类型：Japan/China/Eurozone/USA
- 时间：YYYY-MM-DD HH:MM 格式
- 标题：完整标题文本
- 状态：published/draft
- 重要性：1-5星（通过 slider 图片数量判断）

#### 4.3 保存数据到 Excel

```python
import openpyxl

wb = openpyxl.load_workbook(file_path)
ws = wb.active
ws.append([
    "序号",      # 从表格第一行获取
    "作者",      # 从表格第一行获取
    "类型",      # 从弹窗获取
    "时间",      # 从弹窗获取
    "标题",      # 从弹窗获取
    "状态",      # 从弹窗获取
    "1星"       # 修改前记录原始值
])
wb.save(file_path)
```

#### 4.4 修改重要性为 3 星

```python
# 点击 slider 组件的第三个星星图标
browser(action="act", request={"kind": "click", ref": "e902"})  # 第3个星
```

#### 4.5 关闭弹窗

```python
# 点击确定按钮保存
browser(action="act", request={"kind": "click", ref": "e911"})  # 确定按钮
```

### 5. 翻页

```python
# 点击页码按钮翻页
browser(action="act", request={"kind": "click", ref": "e849"})  # 第2页
browser(action="act", request={"kind": "click", ref": "e850"})  # 第3页
```

### 6. 重复步骤 4-5

直到处理完所有需要的页面。

### 7. 关闭浏览器

```python
browser(action="close")
```

## 注意事项

1. 编辑弹窗的 ref 可能会随着页面刷新而变化，需要从 snapshot 中获取最新的 ref
2. 重要性 slider 点击第三个星星图标可将星级改为3星
3. Excel 文件默认保存在桌面，文件名为当天日期.xlsx
4. 登录凭据为 editor/123456（系统可能已自动登录）
5. 表格每页显示20条数据，共100条（5页）
6. 弹窗关闭后需要等待页面刷新再进行下一步操作
