---
name: solidworks-modeling
description: 通过 SOLIDWORKS 官方 COM API 自动操作本机安装的 SOLIDWORKS（已验证 2022/内部版本30），完成参数化建模（草图、拉伸、旋转、扫描）、打开/修改/保存零件装配体工程图（.SLDPRT/.SLDASM/.SLDDRW）、批量导出 STEP/IGES/PDF/DXF/STL、读取质量属性与特征树、渲染预览图。当用户要求"用 SOLIDWORKS 画/建模/出图/批量转换格式/修改模型"，或提到 SLDWORKS、sldprt、sldasm 文件时使用。无法实时点击 GUI，一切操作经 API 脚本完成。仅限 Windows 且本机已装 SOLIDWORKS。
---

# SOLIDWORKS 自动化建模（OpenClaw 版）

一切操作通过 COM API 脚本（Python + pywin32）完成，不操控 GUI。SOLIDWORKS 窗口保持可见，用户可实时看到结果。

## 环境与连接（已验证的关键事实，勿再试错）

**SOLIDWORKS 版本对照**（规律：内部版本号 = 年份 - 1992）：

| 年份 | 内部版本 | ProgID |
|------|---------|--------|
| 2020 | 28 | SldWorks.Application.28 |
| 2021 | 29 | SldWorks.Application.29 |
| **2022** | **30**（本机已验证） | SldWorks.Application.30 |
| 2023 | 31 | SldWorks.Application.31 |
| 2024 | 32 | SldWorks.Application.32 |
| 2025 | 33 | SldWorks.Application.33 |

通用 ProgID `SldWorks.Application` 作备选。本机版本可查：SOLIDWORKS 安装目录（如 `D:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe`）的文件版本，或注册表 `HKLM:\SOFTWARE\SolidWorks\SOLIDWORKS <年份>\Setup` 的 `SolidWorks Folder`。

- 执行脚本的 Python 环境需要 **pywin32**：先 `python -m pip install pywin32`。
- pywin32 的 `EnsureDispatch` 和 `CastTo` 对 SOLIDWORKS **均失败**；必须先 `gencache.EnsureModule` 生成类型库包装，再用 `mod.ISldWorks(obj._oleobj_)` 手动包装。2022 类型库 GUID：`{83A33D31-27C5-11CE-BFD4-00400513BB57}`（版本 30.0；其他版本从注册表 `HKCR\CLSID\<ProgID的CLSID>\TypeLib` 查）。
- COM 调用返回的对象是裸 `CDispatch`，**每个接口都要手动 wrap**：`IModelDoc2`、`IFeature`、`ISketchManager`、`IFeatureManager`、`IModelDocExtension`、`IMassProperty`。
- 部分成员在早绑定下变成**属性**而非方法（`GetTitle`、`GetTypeName2`），用 `val()` 助手兼容。
- 国标零件模板（2022 示例）：`C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2022\templates\gb_part.prtdot`。`NewPart()` 常返回 None，直接用 `NewDocument(模板路径, 0, 0.0, 0.0)`。
- `Dispatch` 会自动附加到已运行的实例；启动耗时 10–30 秒，连上后 `sw.Visible = True` 并 `sleep(3)`。
- 若 SW 首启弹窗（许可/注册），提醒用户手动关掉，弹窗会阻塞 COM。

**直接使用 `scripts/sw_api.py`**：已实现以上全部逻辑（connect / new_part / 特征遍历 / val / wrap / 保存 / PNG 导出）。写新脚本时 `sys.path.insert(0, <本技能目录>/scripts)` 后 `from sw_api import *`。不要重写连接逻辑。

## 建模核心流程

1. `connect()` → `new_part()` → 拿 `model / sm / fm / ext`（均已 wrap 好）。
2. 选基准面：`refplanes(model)` 按特征树顺序返回 `[前视, 上视, 右视]`（用 `GetTypeName2 == "RefPlane"` 过滤，**不要用名字匹配**，中文界面名字是"前视基准面"等）。
3. 进草图：`plane.Select2(False, 0)` → `sm.InsertSketch(True)`；退出也是 `sm.InsertSketch(True)`（`InsertSketch2` 在该类型库中不存在）。
4. **草图 API 一律用米**（与文档单位无关），角度用弧度。
5. 生成特征前：退草图 → `last_feature(model)` 拿到刚建的草图特征 → `Select2(False, 0)` → 调 `fm.FeatureRevolve2` / `fm.FeatureExtrusion2` 等。**避免 `SelectByID2("草图1",...)`**——特征名随语言本地化。
6. 收尾：`model.ShowNamedView2("*等轴测", 7)` + `ViewZoomtofit2()` → `save_part()` → `export_png()` 渲染预览图。

## 验证（必做）

- 特征对象非 None，日志记录每个特征名。
- `save_part()` 返回 `(True, 0, 0)` 且文件存在、大小合理。
- 体积校验：`ext.CreateMassProperty` 的 `Volume` 与理论计算对比（误差 <5%）。
- **用 `export_png()` 渲染图自查模型形状**，再用 OpenClaw 的文件/图片读取工具（`read`）打开 PNG 确认无误后交付。
- 不要关闭 SOLIDWORKS，让用户接着看/改。

## 参考与示例

- 常用特征 API 参数（含 FeatureCut3 切除、AddToDB 批量绘制）、选择标记、批量导出代码、**已知坑清单（24 条，全部实测）**：见 [references/api-patterns.md](references/api-patterns.md)。
- 完整可运行示例：
  - `scripts/build_mug.py` — 马克杯（旋转杯体 + 拉伸把手 + 保存 + 渲染 + 体积校验）
  - `scripts/build_flower.py` — 花朵（多瓣独立草图逐个拉伸合并 + 偏移起始拉伸 + 不合并降级重试 + 旋转球）
  - `scripts/build_gear.py` — 渐开线齿轮（数学轮廓 660 段折线 + AddToDB 批量绘制 + 键槽孔 FeatureCut3 切除）
  - `scripts/build_assembly.py` — 装配体（建轴 → OpenDoc6 预热插入组件 → 基准面重合配合 ×3）
  - `scripts/build_hook.py` — 起重吊钩（样条单段路径 + InsertProtrusionSwept4 圆形截面扫描 + 顶部凸缘）
  - `scripts/build_hook_loft.py` — 锻造变径吊钩（11 站位偏移参考面圆轮廓 + InsertProtrusionBlend 放样 + 几何遍历棱边 FeatureFillet3 圆角 + BlankRefGeom 隐藏参考面）
  - `scripts/build_cup_shell.py` — 薄壁水杯（实心圆柱 + InsertFeatureShell 开口抽壳 + 杯口圆角；含"返回值假失败"树验证法）
  - `scripts/build_spring.py` — 弹簧（InsertHelix 螺旋线 + REFERENCECURVES 选路径 + CircularProfile 扫描）
  - `scripts/build_flange.py` — 法兰盘（圆盘拉伸 + 单孔切除 + FeatureCircularPattern4 圆周阵列 6 孔）
  - `scripts/build_drawing.py` — 工程图（gb_a4 模板 + CreateDrawViewFromModelView3 三视图 + SLDDRW/PDF 导出）

## 排错方法（实测有效的调试套路）

特征返回 None 时不要盲猜，按这个顺序隔离变量：

1. **写最小探针脚本**：新开零件，只复现失败的那一步（一个草图 + 一个特征），确认能否独立复现。
2. **给每步加日志**：草图实体创建返回值（`Create3PointArc` 失败返回 None）、`Select2` 返回值、特征对象是否为 None——多数失败能在日志里一眼定位（例：花瓣 2 失败就是靠逐瓣日志锁定到 120°/300° 两个方位）。
3. **变量对照**：换参数矩阵（尺寸/角度/合并开关/偏移开关）逐个试，找出触发边界（例：弦长 2mm 被拒、4mm 通过）。
4. **确认是几何问题还是调用问题**：同一草图换特征参数能成 → 参数问题；同一参数换草图能成 → 草图轮廓问题。
5. 修复后把结论写回 `references/api-patterns.md` 的"已知坑"。

## 批量任务模式

遍历文件夹找 `.SLDPRT/.SLDASM`，逐个 `sw.OpenDoc6` → 操作 → `ext.SaveAs` → `sw.CloseDoc`。每步 try/except 并记录失败清单，最后汇总。导出 STEP/PDF 等的参数见 api-patterns.md。

## 安装与迁移（OpenClaw）

把 `solidworks-modeling` 文件夹整体复制到 OpenClaw 技能目录之一：

```bash
# 工作区技能（优先级最高，推荐）
~/.openclaw/workspace/skills/solidworks-modeling/

# 或全局技能目录
~/.openclaw/skills/solidworks-modeling/
```

然后：

1. 装 COM 依赖（用 OpenClaw 执行脚本的那个 Python）：`python -m pip install pywin32`。
2. 验证加载：`openclaw skills list`；若未出现，新开会话（`/new`）或 `openclaw gateway restart`。
3. 若 SOLIDWORKS 版本不是 2022：改 `scripts/sw_api.py` 顶部的 `SW_VERSION`（2023=31, 2024=32…），并在 `TYPELIB_GUIDS` 加入对应 GUID（注册表查：先 `HKCR\SldWorks.Application.<版本>\CLSID` 取 CLSID，再查 `HKCR\CLSID\<CLSID>\TypeLib`），模板路径也要核对。

**平台限制**：仅 Windows + 本机安装 SOLIDWORKS 可用；云部署 / Linux / macOS 容器无法使用（COM API 不存在）。
