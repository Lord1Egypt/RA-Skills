# 🔧 分页撕裂问题修复

**修复时间：** 2026-03-14 18:24  
**问题：** Excel 太宽、HTML 分页撕裂

---

## 📊 问题分析

### 问题 1：Excel PDF 撕裂

**原因：**
1. ❌ 列宽太宽（25+25+25+25 = 100 字符）
2. ❌ 页边距太小（0.3 英寸）
3. ❌ A4 宽度装不下

**表现：**
- PDF 内容被压缩
- 表格列被切断
- 格式错乱

---

### 问题 2：HTML PDF 撕裂

**原因：**
1. ❌ 没有优化分页 CSS
2. ❌ 表格行高太大
3. ❌ 没有避免在表格内部分页

**表现：**
- 产品行被切成两半
- 表头和产品分离
- 内容跨页断裂

---

### 对比：Word 为什么正常？

**Word 设置：**
```python
# 合理的页边距
section.left_margin = Cm(2.5)   # 2.5cm
section.right_margin = Cm(2.5)  # 2.5cm
section.top_margin = Cm(2)      # 2cm
section.bottom_margin = Cm(2)   # 2cm
```

**特点：**
- ✅ 边距合理
- ✅ 表格自动适配
- ✅ 分页智能

---

## ✅ 修复方案

### Excel 修复

**修改前：**
```python
# 列宽太宽
ws.column_dimensions['A'].width = 25
ws.column_dimensions['B'].width = 25
ws.column_dimensions['C'].width = 25
ws.column_dimensions['D'].width = 25

# 边距太小
ws.page_margins.left = 0.3
ws.page_margins.right = 0.3
```

**修改后：**
```python
# 缩小列宽（适应 A4）
ws.column_dimensions['A'].width = 12   # Item
ws.column_dimensions['B'].width = 20   # Description
ws.column_dimensions['C'].width = 12   # Qty
ws.column_dimensions['D'].width = 20   # 条款

# 增加边距（参考 Word）
ws.page_margins.left = 0.7    # ≈ 1.8cm
ws.page_margins.right = 0.7   # ≈ 1.8cm
ws.page_margins.top = 0.8     # ≈ 2cm
ws.page_margins.bottom = 0.8  # ≈ 2cm
```

**效果：**
- ✅ A4 宽度刚好装下
- ✅ 不再撕裂
- ✅ 格式工整

---

### HTML 修复

**修改前：**
```css
@media print {
    .a4-container {
        padding: 15mm;
    }
    table, .grid, .flex {
        page-break-inside: avoid;
    }
}
```

**修改后：**
```css
@media print {
    body {
        margin: 0;
        padding: 0;
    }
    .a4-container {
        padding: 15mm 15mm 10mm 15mm;  /* 底部减少 */
    }
    
    /* 表格整体不分页 */
    table {
        page-break-inside: avoid;
    }
    
    /* 每行不分页 */
    tr {
        page-break-inside: avoid;
        page-break-after: auto;
    }
    
    /* 标题后不分页 */
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
    }
    
    /* 区块不分页 */
    .grid {
        page-break-inside: avoid;
    }
    
    /* 确保颜色 */
    .bg-slate-900 {
        background-color: #0f172a !important;
        color: white !important;
    }
}
```

**产品行优化：**
```html
<!-- 修改前：padding 太大 -->
<td class="p-4">

<!-- 修改后：缩小 padding -->
<td class="p-3 py-2">
    <p class="text-sm">...</p>  <!-- 字体略小 -->
</td>
```

**效果：**
- ✅ 表格整体在一页
- ✅ 产品行不切断
- ✅ 标题后不分页
- ✅ 2 页完美分页

---

## 📊 修复对比

### Excel

| 项目 | 修复前 | 修复后 |
|------|--------|--------|
| **列宽** | 25+25+25+25 | 12+20+12+20 ✅ |
| **边距** | 0.3 英寸 | 0.7 英寸 ✅ |
| **A4 适配** | ❌ 太宽 | ✅ 刚好 |
| **PDF 撕裂** | 严重 | 无 ✅ |

### HTML

| 项目 | 修复前 | 修复后 |
|------|--------|--------|
| **分页控制** | 基础 | 完整 ✅ |
| **表格分页** | 会切断 | 避免 ✅ |
| **行内分页** | 会切断 | 避免 ✅ |
| **标题分页** | 会分离 | 避免 ✅ |
| **PDF 撕裂** | 严重 | 无 ✅ |

---

## 🎯 测试文件

**生成文件：**
```
QT-20260314-020-Fixed/
├── QT-20260314-020-Fixed.xlsx        (6.9KB)
├── QT-20260314-020-Fixed.docx        (37KB)
├── QT-20260314-020-Fixed.html        (15KB)
├── QT-20260314-020-Fixed-HTML.pdf    (289KB) ✅ 优化后
└── QT-20260314-020-Fixed-Excel.pdf   (161KB) ✅ 优化后
```

**对比旧版：**
```
QT-20260314-019-Complete/
├── QT-20260314-019-Complete-HTML.pdf    (290KB) ❌ 有撕裂
└── QT-20260314-019-Complete-Excel.pdf   (161KB) ❌ 有撕裂
```

---

## 📝 验收清单

### Excel PDF

- [x] 所有列在一页内
- [x] 无内容被切断
- [x] 左右边距合理
- [x] 表格工整
- [x] 2 页完成

### HTML PDF

- [x] 产品行完整（不切断）
- [x] 表头和产品同页
- [x] 区块完整（不切断）
- [x] 背景色正确
- [x] 2 页完成

### Word PDF（参考标准）

- [x] 格式标准
- [x] 分页合理
- [x] 作为对比基准

---

## 🚀 使用方法

```bash
# 一键生成（已包含修复）
./generate-all.sh data.json QT-001

# 生成文件：
# - QT-001-HTML.pdf ✅ 优化后
# - QT-001-Excel.pdf ✅ 优化后
```

---

## 💡 经验总结

### Excel 优化要点

1. **列宽总和要小于 A4 可用宽度**
   - A4 宽度：210mm
   - 左右边距：2×18mm = 36mm
   - 可用宽度：174mm ≈ 65 字符
   - 列宽总和：12+20+12+20 = 64 ✅

2. **边距不能太小**
   - 太小会导致打印时内容被切
   - 参考 Word：左右 2.5cm

3. **使用 fitToWidth**
   - 强制所有列 fit 到一页宽度

### HTML 优化要点

1. **避免表格内部分页**
   ```css
   table, tr {
       page-break-inside: avoid;
   }
   ```

2. **标题后不分页**
   ```css
   h1, h2, h3 {
       page-break-after: avoid;
   }
   ```

3. **减少 padding 和字体**
   - 表格行：`p-4` → `p-3 py-2`
   - 字体：默认 → `text-sm`

4. **底部 padding 减少**
   - `15mm 15mm 15mm 15mm` → `15mm 15mm 10mm 15mm`
   - 给第二页留更多空间

---

**修复完成！** ✅

**最后更新：** 2026-03-14 18:24  
**维护者：** WILSON
