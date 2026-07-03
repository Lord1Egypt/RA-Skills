---
name: sketch2cad
description: 手绘草图转CAD DXF文件。Use when user sends a hand-drawn sketch with dimensions and wants to convert it to an editable CAD (DXF) file. Automatically recognizes shape and dimensions from photos, generates standard AutoCAD-compatible DXF. 手绘转CAD、草图转DXF、拍照生成图纸。
version: 1.0.0
author: cdszeyao
price: 0
pricingModel: one-time  # one-time / subscription / free
license: MIT-0
metadata: {"openclaw": {"emoji": "📐", "requires": {"bins": ["python3"], "files": ["scripts/convert.py"]}, "primaryFile": "scripts/convert.py"}}
---

# Sketch2CAD - 手绘草图转CAD

拍照上传手绘草图，自动识别尺寸和形状，生成标准AutoCAD兼容的DXF文件。

## 适用场景

| 场景 | 示例 |
|------|------|
| 快速建模 | 随手画个平面轮廓，直接进CAD编辑 |
| 现场量房 | 拍照手绘尺寸 → DXF → 深化 |
| 方案推敲 | 草图阶段快速生成电子底图 |
| 尺寸标注图 | 手绘标注 → 精确CAD线稿 |

## Trigger Conditions

- "手绘转CAD" / "草图转DXF"
- "帮我画个CAD"（附手绘图片）
- "把这个转成图纸"
- "sketch2cad"
- 用户发送手绘图片并提到CAD、DXF、图纸

---

## 工作流程

### Step 1: 接收手绘图片

用户发送手绘照片，需包含：
- ✅ 清晰的线条轮廓
- ✅ 关键尺寸标注（数字尽量大且清晰）
- ✅ 尽量正拍，减少透视变形

### Step 2: AI识别图形

分析图片，提取：
- 轮廓形状（直线段组成的闭合多边形）
- 关键顶点坐标（基于尺寸标注推算比例）
- 图形类型判断（矩形、L形、T形、自定义等）

### Step 3: 生成DXF

调用脚本生成标准R2010格式DXF：

```bash
python3 ~/.openclaw/workspace/skills/sketch2cad/scripts/convert.py \
  <output.dxf> \
  <x1,y1> <x2,y2> <x3,y3> ...
```

**示例 — L形轮廓（宽8，高10，内凹5×5）：**
```bash
python3 scripts/convert.py handdrawn.dxf \
  0,5 5,5 5,0 8,0 8,10 0,10
```

### Step 4: 发送文件

通过飞书文件消息发送DXF，用户下载后用AutoCAD打开。

---

## 坐标点约定

- 所有坐标单位为**毫米（mm）**
- 第一个点为起点，按轮廓顺序依次连接
- 脚本自动闭合最后一个点到第一个点
- 坐标系：X向右，Y向上，Z=0

### 常见图形速查

| 图形 | 坐标点序列 |
|------|-----------|
| 矩形 10×8 | `0,0 10,0 10,8 0,8` |
| L形（本技能测试图） | `0,5 5,5 5,0 8,0 8,10 0,10` |
| T形 | `0,8 3,8 3,10 5,10 5,8 8,8 8,0 0,0` |

---

## 脚本说明

`scripts/convert.py`

- **自动管理依赖**：首次运行自动创建venv并安装ezdxf
- **标准格式**：生成AutoCAD R2010兼容的DXF
- **使用LINE实体**：兼容性最佳，所有版本CAD均可打开
- **参数简单**：`输出路径` + `空格分隔的x,y坐标`

---

## 注意事项

1. **图片质量影响识别**：模糊、反光、歪斜会导致尺寸识别偏差
2. **复杂曲线暂不支持**：目前仅支持直线段组成的轮廓（圆弧需手动加）
3. **单位默认毫米**：如需要米或其他单位，在CAD里用SCALE命令缩放
4. **图层**：默认在0图层，进入CAD后可自行调整线型、颜色、图层

---

## 使用示例

**用户发送手绘图：**
> [图片：手绘L形轮廓，标注尺寸]

**助手执行：**
1. 识别为L形，尺寸8×10，内凹5×5
2. 提取顶点序列：`0,5 5,5 5,0 8,0 8,10 0,10`
3. 运行脚本生成DXF
4. 飞书发送文件

---

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| CAD报错"DXF输入无效" | 手写DXF格式不标准 | 确保使用本技能的convert.py脚本生成 |
| 打开后看不到图 | 视图范围不在图形区域 | CAD里双击中键或输入`Z`→`E`全图缩放 |
| 坐标比例不对 | 图片识别偏差 | 用户确认关键尺寸，手动修正坐标 |

---

## 技术栈

- **DXF生成**：ezdxf (Python)
- **CAD兼容**：AutoCAD R2010+、天正、中望CAD等
- **依赖管理**：Python3 venv（自动创建）
