# SOLIDWORKS API 模式速查（SW2022 / pywin32 早绑定）

所有几何 API 单位：**米 / 弧度**。`sm`=`ISketchManager`，`fm`=`IFeatureManager`，`ext`=`IModelDocExtension`。

## 目录

- 草图绘制
- 特征：旋转 / 拉伸 / 扫描 / 圆角
- 打开 / 保存 / 批量导出
- 选择标记（SelectByID2 Mark）
- 已知坑

## 草图绘制

```python
plane.Select2(False, 0); sm.InsertSketch(True)      # 进入草图
sm.CreateLine(x1, y1, z1, x2, y2, z2)               # 直线（草图坐标，米）
sm.CreateArc(xc, yc, zc, x1, y1, z1, x2, y2, z2, dir)  # dir=±1，方向容易错
sm.Create3PointArc(x1,y1,z1, x2,y2,z2, x3,y3,z3)    # 起点/终点/弧上一点，方向明确，优先用
sm.CreateCircle(xc, yc, zc, xp, yp, zp)             # 圆心+圆上一点
sm.CreateCenterLine(x1, y1, z1, x2, y2, z2)         # 中心线（旋转轴用）
sm.InsertSketch(True)                                # 退出草图
```

注意：草图内坐标系各基准面不同——前视(XY)：x=模型X, y=模型Y；右视：纵轴=模型Y，横轴≈±Z；上视：横轴=X，纵轴≈∓Z。对称零件方向画反通常无碍，画完用 PNG 自查。

## 特征

生成特征前必须先选中草图特征：`sketch_feat = last_feature(model); sketch_feat.Select2(False, 0)`。

```python
# 旋转凸台（20 参）：SingleDir, IsSolid, IsThin, IsCut, ReverseDir,
#   BothDirUpToSameEntity, Dir1Type, Dir2Type, Dir1Angle(rad), Dir2Angle,
#   OffsetRev1, OffsetRev2, OffsetDist1, OffsetDist2,
#   ThinType, ThinThick1, ThinThick2, Merge, UseFeatScope, UseAutoSelect
fm.FeatureRevolve2(True, True, False, False, False, False,
                   0, 0, 6.28318530717959, 0.0,      # 360°；180°=pi
                   False, False, 0.0, 0.0, 0, 0.0, 0.0, True, True, True)

# 拉伸凸台（23 参）：Sd, Flip, Dir, T1, T2, D1(m), D2,
#   Dchk1, Dchk2, Ddir1, Ddir2, Dang1, Dang2,
#   OffsetRev1, OffsetRev2, TransSurf1, TransSurf2,
#   Merge, UseFeatScope, UseAutoSelect, T0, StartOffset, FlipStartOffset
# 终止条件 T：0=盲孔 1=完全贯穿 6=中面(对称拉伸)
fm.FeatureExtrusion2(True, False, False, 0, 0, 0.01, 0.0,      # 盲孔 10mm
                     False, False, False, False, 0.0, 0.0,
                     False, False, False, False,
                     True, True, True, 0, 0.0, False)

# 拉伸切除 FeatureCut3（26 参，比凸台少 AssemblyFeatureScope 一位、多 NormalCut）：
#   Sd, Flip, Dir, T1, T2, D1, D2, Dchk1, Dchk2, Ddir1, Ddir2, Dang1, Dang2,
#   OffsetRev1, OffsetRev2, TransSurf1, TransSurf2, NormalCut,
#   UseFeatScope, UseAutoSelect, AssemblyFeatureScope, AutoSelectComponents,
#   PropagateFeatureToParts, T0, StartOffset, FlipStartOffset
# **Dir 必须与凸台相反**（朝材料内部），否则切空返回 None
fm.FeatureCut3(True, False, True, 1, 0, 0.01, 0.0,              # 完全贯穿
               False, False, False, False, 0.0, 0.0,
               False, False, False, False,
               False, True, True, True,
               False, False, 0, 0.0, False)

# 大批量绘制草图（数百条线段，如齿轮/凸轮轮廓）：
sm.AddToDB = True      # 绕过实时求解器，速度快且不会随机拒线
for ...: sm.CreateLine(...)
sm.AddToDB = False
sm.InsertSketch(True); model.EditRebuild3()

# 拉伸切除：FeatureCut3 / FeatureExtrusionCut…，优先 fm.FeatureCut3(True,False,False,0,0,D1,0,...)
# 圆角：fm.FeatureFillet3(195, 半径, 0, 0, 0, 0, None)  需先 SelectByID2 选边线
```

扫描（Sweep）需要两个草图：轮廓(mark=1) + 路径(mark=4)，用 `ext.SelectByID2(name, "SKETCH", 0,0,0, False, mark, None, 0)` 分别选，然后 `fm.InsertProtrusionSwept4(...)`。路径/轮廓必须在不同草图、轮廓平面须垂直路径起点切线——容易失败，优先用旋转/拉伸替代；必须用扫描时先小步验证。

## 打开 / 保存 / 批量导出

```python
# 打开文件：type 1=零件 2=装配体 3=工程图
raw = sw.OpenDoc6(path, 1, 0, "", 0, 0)   # 返回(errors, warnings, doc) 元组
doc = wrap(raw[-1] if isinstance(raw, tuple) else raw, "IModelDoc2")

ext.SaveAs(path, 0, 1, None, 0, 0)        # 返回 (ok, err, warn)；option: 1=静默 2=另存副本
```

按扩展名自动识别导出格式：`.step/.stp`、`.iges/.igs`、`.stl`、`.pdf`（工程图）、`.dxf/.dwg`（工程图/平板）、`.png/.jpeg`（当前视图渲染）。装配体/工程图打开时加 `sw.DocumentVisible(True, type)` 更稳。

批量模式：遍历目录 → OpenDoc6 → 处理 → SaveAs → `sw.CloseDoc(title)`。单文件失败不影响队列，记录失败清单最后汇总。

## 选择标记（SelectByID2 的 Mark 参数）

| Mark | 用途 |
|------|------|
| 0 | 普通选择 |
| 1 | 扫描/放样轮廓 |
| 4 | 扫描路径 |
| 2 | 放样引导线 |

特征名随界面语言本地化（中文：草图1/旋转1/凸台-拉伸1），**优先用 `IFeature.Select2` + 特征树遍历定位，不要用名字**。

## 已知坑

1. `NewPart()` 依赖默认模板设置，常返回 None——用 `NewDocument(模板绝对路径, 0, 0.0, 0.0)`。
2. `FeatureByPosition` / `InsertSketch2` 在早绑定包装中缺失——用 `FirstFeature`/`GetNextFeature` 遍历、`InsertSketch(True)`。
3. `GetTitle` / `GetTypeName2` 可能表现为属性——用 `val()` 兼容。
4. 弹窗（许可、欢迎页、崩溃恢复）会阻塞 COM——任务前确认 SW 能正常空手启动。
5. `sw.CloseAllDocuments(True)` 清理残留文档，避免同名草图/特征错位。
6. 导出 PNG 前务必 `ShowNamedView2 + ViewZoomtofit2`，否则视图可能空白或截断。
7. 草图欠约束不影响特征生成；但轮廓必须封闭且自相交为零，否则 Revolve/Extrude 返回 None。
8. **微小几何被拒**：弦长 ~2mm 以下的 `Create3PointArc` 会静默返回 None（实测 4mm 以上稳定）。做小特征时先放大建模再整体缩放，或加大局部尺寸。
9. **面-面贯穿导致合并随机失败**：薄板特征被已有实体的平面从中间切开（如花瓣板 98~101mm 被茎顶面 100mm 穿过）时，Merge=True 的拉伸在某些方位角上数值失败。对策：让已有实体**高出**薄板（茎顶伸出板面），或合并失败时降级重试 Merge=False（多实体也能保存/导出）。
10. **多轮廓草图慎用**：多个闭合轮廓在同一草图里若相邻轮廓的弧相交/接近容差，整个拉伸返回 None。规律造型（花瓣、齿、槽）优先**每单元独立草图+逐个拉伸合并**，也更方便单步排错。
11. 旋转成型画球：半圆轮廓 + 一条沿轴的闭合线 + 中心线（中心线必须比轮廓两端各长出一截），`FeatureRevolve2` 选整个草图即可。
12. 偏移起始拉伸：`FeatureExtrusion2(..., T0=3, StartOffset=距离, ...)` 从草图面偏移开始拉伸，免建参考面（探针验证 SW2022 可用）。
13. **程序化绘制任何多点轮廓都必须 `sm.AddToDB = True`**（不只是大批量！）：实时求解模式下有两个灾难——(a) 数百条线段时闭合处随机拒线（CreateLine 返回 None）；(b) **自动几何关系会把采样点吸附到水平/竖直方向，轮廓静默变形**（实测：48 段圆弧变成阶梯多边形，特征照样成功、体积仅差 0.07%，不渲染检查根本发现不了）。所以：所有脚本生成的草图一律 AddToDB，画完 `AddToDB = False` + `InsertSketch(True)` + `EditRebuild3()`；交付前必须渲染正视图/等轴测 PNG 用眼睛复查轮廓。
14. **生成轮廓点时去掉零长度段**：相邻重复点（如周期阵列轮廓的首尾点）产生的零长度 CreateLine 会失败，绘制前用 `math.hypot(dx,dy) < 1e-9` 跳过。
15. **切除方向与凸台相反**：同一基准面上，凸台 `FeatureExtrusion2(..., Dir=False)` 成功后，切除必须 `FeatureCut3(..., Dir=True, ...)`（朝材料内部），否则切空返回 None。
16. **复杂嵌套轮廓分两步**：复杂外轮廓 + 带凸台的内孔（如齿轮+键槽孔）放同一草图会拉伸失败；拆成"外轮廓实心拉伸 → 内轮廓 FeatureCut3 切除"两步，稳定可靠。
17. **渐开线齿轮轮廓算法**（`build_gear.py` 已实现）：r=mz/2, rb=r·cosα, ra=r+m, rf=r−1.25m；半齿厚角 η(ρ)=π/(2z)+inv(α)−inv(α_ρ)，inv(x)=tan x−x；基圆以下（rf<rb 时）用径向线段衔接。每齿 32 段折线即可，体积校验误差 <0.1%。
18. **圆形截面扫描（`build_hook.py` 已验证）**：`InsertProtrusionSwept4` 免轮廓草图，三条铁律——
    - 路径草图用 `SelectByID2(名, "SKETCH", 0,0,0, True, 4, None, 0)`（**Mark=4**，不是 1/0；用 Feature.Select2 传 mark 也一样失败）；
    - **首实体必须 Merge=False**（第 13 参；体已存在才可 True），否则返回 None；
    - **路径必须是单个草图段**：AddToDB 模式下直线+三点弧两段路径端点虽几何重合但未合并，扫描必然失败；改画**单条样条** `CreateSpline(VARIANT(VT_ARRAY|VT_R8, [x,y,z,...]))`，既相切连续又无接头问题。2D/3D 草图单直线均实测可行。
    - 20 参顺序：Propagate, Alignment, Twist, KeepTangency, AdvSmoothing, Start/EndMatching, IsThin, T1, T2, ThinType, PathAlign, Merge, FeatScope, AutoSelect, TwistAngle, MergeSmoothFaces, CircularProfile=True, 直径(米), Direction。
19. **多截面放样（`build_hook_loft.py` 已验证，10 截面变径吊钩）**：`fm.InsertProtrusionBlend` 17 参(Closed, KeepTangency, ForceNonRational, TessTol, Start/EndMatching, Start/EndTangentLen, Start/EndTangentDir, IsThin, T1, T2, ThinType, Merge, FeatScope, AutoSelect)，轮廓草图按序 `SelectByID2(..., True, 1, None, 0)`（Mark=1），首实体 Merge=False。配套套路——
    - 偏移参考面用 **`fm.InsertRefPlane(8, 距离米, 0, 0, 0, 0)`**（8=距离约束；注意是 FeatureManager 的方法，IModelDoc2 上没有），先 `SelectByID2("上视基准面","PLANE",...)` 再调；
    - **负偏移距离是隐形炸弹**：偏移面能建、圆也能画，但含负偏移面轮廓的放样必然返回 None（实测：全正高度 5 截面 OK，混入负偏移 3 截面即失败）。对策：把整体造型坐标**整体抬升**让所有偏移为正；
    - 各截面 y（偏移距离）必须互不相同，共面两轮廓会让放样折叠失败；
    - 渲染前把 `基准面N` 全部选中后 `model.BlankRefGeom()` 隐藏，否则橙色参考面刷屏。
20. **圆角（sw_api.fillet_circle_edge 已封装，`build_hook_loft.py` 全流程复现）**：`fm.FeatureFillet3(Options, R1, R2, Rho, Ftyp, Overflow, ConicRhoType, 7个None数组)`，等半径圆角 **Ftyp=0**（Simple；1 是变半径，不给 Radii 数组必败）、**Options=2**（UniformRadius；0 会静默失败）、Overflow=0。
    - **棱边不要用坐标点选**：`SelectByID2("","EDGE",x,y,z,...)` 按"最近边+容差"匹配，偏十几毫米也能选中别的边（实测想点凸缘顶圈 y=97 却倒了 y=85 的边），且倒过角的边消失后同一点位直接选空。可靠做法：**遍历几何** `part.GetBodies2(0,True)→GetFaces→GetEdges→IsCircle→CircleParams[圆心,轴,半径]`，按（圆心高度+半径）匹配，`IEntity.Select4(True, None)` 选中；
    - `GetFaces`/`GetEdges`/`CircleParams` 又是属性/方法二义成员，用 `call0()` 兼容（sw_api 已加）；
    - 文档已打开时用 `model.Save3(1,0,0)` 覆盖保存，`save_part()` 的 os.remove 会撞文件锁（WinError 32）；
    - 偏移面上拉伸凸台 `Dir=True` 实际朝 -Y（包住已有体），倒角目标边高度要按实测几何读，别按设计意图猜。
21. **抽壳（`build_cup_shell.py` 已验证）**：`model.InsertFeatureShell(厚度米, Outward)`（**IModelDoc2 的方法**，IFeatureManager 上没有；先选中要移除的开口面）——**返回值恒为 None，成功也返 None**（与 AddComponent5 同类）！验证三连：特征树出现「抽壳N」+ `feat.GetErrorCode2(False)==0` + 体积比对（开口壳体积 ≈ π(R²−r²)L + πr²t，与实测偏差应 <3%）。
    - 同类型"假失败"API 备忘：AddComponent5、InsertFeatureShell——**凡返回 None 先查特征树再下结论**；
    - 反向拉伸实心体后顶面高度别猜，用 circle_edges 实测（如本例 Dir=True 实际朝 -Y，顶面在 y=0）。
22. **螺旋线+弹簧（`build_spring.py` 一次通过）**：画圆草图选中后 `model.InsertHelix(Reversed, Clockwise, Tapered, Outward, Helixdef=0[螺距+圈数], Height, Pitch, Revolution, TaperAngle, StartAngle)`（**IModelDoc2 的方法**）；生成「螺旋线/涡状线N」特征后，用 **`SelectByID2(名, "REFERENCECURVES", 0,0,0, True, 4, None, 0)`** 选中作路径，接 CircularProfile 扫描即成弹簧/螺纹坯（Mark=4、Merge=False 铁律同坑18）。体积校验公式：V = π·(d/2)²·圈数·π·D。
    - 渲染前把螺旋线特征选中后 `BlankRefGeom()` 隐藏，否则蓝色线框刷屏。
23. **圆周阵列（`build_flange.py` 已验证）**：`fm.FeatureCircularPattern4(数量, 总角rad, FlipDir, "", GeometryPattern=False, EqualSpacing=True, VaryInstance=False)`。选择顺序与标记：先选**要阵列的特征 `feat.Select2(False, 4)`（Mark=4，Mark=0 失败）**，再 `SelectByID2("","FACE",圆柱侧面上一点,..., True, 1, None, 0)` 选**圆柱面作旋转轴（Mark=1，追加选择）**。EqualSpacing=True 时 Spacing 给 2π（整周均布）。体积校验：V = V母体 − N·V单元。
24. **工程图（`build_drawing.py` 已验证）**：模板 `C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2022\templates\gb_a4.drwdot`（A0~A4 都有），NewDocument 后 `wrap(raw, "IDrawingDoc")`。
    - 插视图：`draw.CreateDrawViewFromModelView3(零件绝对路径, "*前视", LocX, LocY, 0)`，**视图名随界面语言本地化**（"*前视"/"*上视"/"*等轴测"），坐标单位米、原点在图纸左下角；
    - GB 第一角投影：俯视图放主视图**下方**；A4 横向右下约 180×56mm 是标题栏，视图坐标别压上去（实测俯视中心 y≥92mm 安全）；
    - 标题栏材质/质量/比例自动从零件带出；
    - `InsertModelAnnotations3` 导入模型尺寸：零件没有"为工程图标记"的尺寸时静默返回 None（尺寸标注自动化是后续课题）；
    - 导出 PDF：`ext.SaveAs("xxx.pdf", 0, 1, None, 0, 0)` 直接成；验证渲染用 pypdfium2 `PdfDocument(pdf)[0].render(scale=2.0).to_pil()`。

## 装配体（build_assembly.py 已验证全流程）

```python
raw = sw.NewDocument(r"C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2022\templates\gb_assembly.asmdot", 0, 0.0, 0.0)
asm    = wrap(raw, "IAssemblyDoc")
amodel = wrap(raw, "IModelDoc2")
aext   = wrap(amodel.Extension, "IModelDocExtension")   # 必须从 .Extension 属性取!

# 插入组件（官方套路：先开零件再切回装配体，否则第二个起插入静默失败）
sw.OpenDoc6(path, 1, 1, "", 0, 0)              # type 1=零件 2=装配体, options=1 静默
sw.ActivateDoc3(asm_title, False, 0, 0)
asm.AddComponent5(path, 0, "", False, "", 0.0, 0.0, 0.0)   # 8参, 末三位是插入点 xyz(米)
# 验证靠 GetComponents(False) 数量变化, 不要信返回值(常返回 None)

# 基准面配合: 选组件内基准面用装配限定名
aext.SelectByID2("前视基准面@齿轮-1@装配体1", "PLANE", 0.0, 0.0, 0.0, False, 0, None, 0)
aext.SelectByID2("前视基准面@传动轴-1@装配体1", "PLANE", 0.0, 0.0, 0.0, True, 0, None, 0)
r = asm.AddMate3(0, 0, False, 0.0, 0.0, 0.0, 1, 1, 0.0, 0.0, 0.0, False, 0)  # 14参
# MateType: 0=重合 1=同心 3=平行; Align: 0=同向 1=反向 2=最近; 返回末位 ErrorStatus=1 成功
```

**设计技巧**：零件建模时让"原点/基准面即配合基准"（如齿轮前面在 z=0、轴肩顶面在 z=0），装配时原点重合即就位，配合只负责锁定，免去变换矩阵。

**装配体坑（实测）**：

18. **第二个组件起插入静默失败**：`AddComponent5/AddComponent2` 返回 None 且组件数不变。解法：插入前 `OpenDoc6` 打开零件 → `ActivateDoc3(装配体标题)` 切回 → 再插入。第一个组件不受此限。
19. **`GetComponents(False)` 返回顺序是特征树顺序**，不是插入顺序——找组件按 `Name2`（如"齿轮-1"）或 `GetPathName()` 匹配。
20. **接口包装必须包正确的对象**：`wrap(doc, "IModelDocExtension")` 是错的（dispid 对不上会报"无效的参数数目"），必须 `wrap(doc.Extension, "IModelDocExtension")`。sw_api 的 `new_part` 里就是这么做的，自己写装配代码时照此办理。
21. `AddMate3` 在 SW2022 是 **14 参**（末位 ErrorStatus 出参，=1 成功）；基准面选择用 `"PLANE"` 类型 + 装配限定名 `基准面名@组件名@装配体名`（名字本地化但稳定，中文界面就是"前视基准面"）。
22. 查配合/组件常量：swconst 常量库 GUID `{4687F359-55D0-4CD3-B6CF-2EB42C11F989}`（版本 30.0），`EnsureModule` 后从 `win32com.client.constants` 按名取（`dir()` 枚举不出来）。
