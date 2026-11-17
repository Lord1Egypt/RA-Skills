# 3D 增强通道（方案 A）· Blender → three.js 完整管线

> 状态：经两个完整项目实战验证——「心脏解剖」（blenderkit 写实模型 → GLB 交互幕，D:\coding2026\课件-心脏解剖\）与「欧姆定律」（从零建模 → 仿真视频+静帧内嵌，D:\coding2026\课件-欧姆定律\，D:\coding2026\欧姆定律3D\）。
> 目标：让交互课件在 SVG 之上获得"可旋转的真实 3D"与"物理仿真动画"能力，**仍是单文件零外链、离线可用**；3D 资产体积宽松（总体几十 MB 内均可），但必须落实大体积 HTML 的离线打开体验保障（第六节清单）。

## 一、通道选择矩阵（第零·五步的展开）

| 通道 | 内容物 | 适用知识形态 | 典型例子 | 体积代价 |
|---|---|---|---|---|
| A. three.js 交互幕 | GLB 模型 base64 内嵌 + OrbitControls + 点选标注 + 动画 mixer | 需要"绕看"的空间结构 | 心脏四腔、发动机、分子、地形 | GLB 不设硬上限（几十 MB 内均可），须落实体验保障清单 |
| B. 仿真视频/静帧 | mp4 / JPEG base64 内嵌 | 动态过程实景、装饰性高质量渲染 | 电流流动、天体运行、流体 | mp4 高清几十 MB 亦可，jpg 30–60KB |
| A+B | 两者组合 | 结构 + 过程并重 | 心脏（GLB+顶点色分色）＋欧姆定律（滑块仿真+视频） | 总体积几十 MB 内均可 |
| D. 纯 SVG | 无 | 平面流程/参数依赖/叙事 | 晨昏线、时间轴 | 0 |

判定要点：
- **写实级复杂结构**（器官、文物、机械）：手写 SVG 有天花板 → 首选 A，模型优先从 blenderkit 素材库拉（写实度远超程序化），特殊/抽象结构才从零建。
- **抽象但需要交互的装置**（电路、光具座、单摆）：SVG 滑块仿真已够精准，3D 作 B 通道点缀（渲染视频/静帧）增强质感——欧姆定律即此路线。
- **参数依赖类**（I=U/R、凸透镜）：公式联动交互放 SVG 幕（拾取/计算/联动零延迟），3D 幕只做"实景欣赏/空间认知"，不要把数值交互塞进 3D。

## 二、从零建模铁律（用户指令级规范，严禁跳步）

```
① 设计 → ② 参考图（必要时搜图/AI 生成）→ ③ 高质量 .py（零件逐个函数 → 组装）
→ ④ 交给 Blender 执行 → ⑤ 渲染验证（不达标回③）→ ⑥ 导出 GLB / 渲染序列
```

### ① 设计（`设计.md` 落盘，先写后建）
必含四节：
- **教学目标**：这个 3D 模型服务于什么知识点、学生要看懂什么。
- **视觉编码表**：物理量/结构 → 3D 载体 → 颜色/尺寸/动画语义（如 电压V→电池红正黑负、电流I→橙光粒子流速∝I、电阻R→色环密度）。
- **零件清单**：每个零件一行（名称 + 几何构成 + 关键尺寸），这就是③的函数清单。
- **动画与渲染方案**：动画参数（速度/周期/关键物理量映射）、引擎（EEVEE 快/Cycles 真）、相机机位（3/4 等距优先）。

### ② 参考图（必要时）
- 优先 WebSearch 教材/科普实物图确认**物理正确性**（拓扑、比例、颜色语义）。
- 美术方向不明时用 ImageGen 生成 1 张场景参考图（提示词含构图/光/风格，"no text, no labels"）。
- **红线**：AI 生成图的物理/解剖拓扑不作准，建模以教材知识为准；参考图只定构图与美术。

### ③ 高质量 .py（结构模板，已在欧姆定律项目验证）
```python
# ohms_law_3d.py 的结构范式
import bpy, math, os, argparse
from mathutils import Vector
OUT = os.path.dirname(os.path.abspath(__file__))
BUILD_LOG = []

def new_mat(name, base, metallic=0., rough=.5, emis=None, emis_s=0.):
    """按 n.type=='BSDF_PRINCIPLED' 过滤取节点；base/emis 必须 RGBA 4 元组"""
    ...
def make_battery():   ...  # 零件1：圆柱壳+端子+标签
def make_resistor():  ...  # 零件2：陶瓷柱+色环+引线
def make_wire():      ...  # 零件3：贝塞尔曲线放样成管
def make_gauge():     ...  # 零件4：表盘+指针+刻度
def make_current_particles(): ...  # 零件5：沿路径运动的小球
def make_formula_text():      ...  # 零件6：3D 文字
def make_base():      ...  # 零件7：地台
def assemble():       # 逐个调用 + BUILD_LOG 记录 + 相机 + 灯光 + world
    ...
# 每个 make_*() 必须：清同名旧物 → 建几何 → 配材质 → 打印 BUILD_LOG
def main():
    assemble()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'xxx.blend'))
    # --anim 参数：动画帧序列渲染；否则静帧
```
质量要求：零零件间穿插破面、材质命名语义化、`--anim` 可重跑、BUILD_LOG 全程可追溯。

### ④ 交给 Blender 执行
```bash
# 冒烟测试先行（15s 确认引擎/输出链路，再跑正式，避免白跑）
BLENDER --background --factory-startup --python-expr "<渲染320x180一张PNG>"
# 正式构建（静帧）
BLENDER --background --python xxx.py 2>&1 | grep -E "零件合计|ALL_DONE|Error|Traceback"
# 动画序列
BLENDER --background --python xxx.py -- --anim
```

### ⑤ 渲染验证
- 静帧必须**肉眼 Read 查看**，按"背景/过曝/构图裁切/固有色对比/粒子颜色"清单逐项过——欧姆定律项目循环了 4 轮才达标。
- 动画用帧 md5 抽查（不同帧指纹不同 = 确实在动，防关键帧静默失效）。

## 三、方案 A：GLB → three.js 单文件内嵌（心脏项目验证）

### 3.1 Blender 侧导出
```python
bpy.ops.export_scene.gltf(filepath=OUT+'/model.glb',
    export_format='GLB', use_selection=True,
    export_animations=True, export_morph=True,   # shape key 动画
    export_colors=True,                          # 顶点色图层 COLOR_0..N
    export_yup=True)
```
- **归一化**：模型整体缩放到包围盒 ~2 单位（OrbitControls 相机距离 1.2–7 才舒适），中心移到原点。
- **教学分色**：需要图层切换时，在 Blender 里写顶点色层（如四腔分色/动静脉血/循环蒙版，各一层），导出后 GLB 的 `primitives[0].attributes` 里即 COLOR_0..N，three.js 侧交换 `geometry.attributes.color` 引用即可秒切。
- GLB 自检（防"导出了但没导对"）：
```python
import struct, json
data=open('model.glb','rb').read()
clen,_=struct.unpack('<II',data[12:20]); j=json.loads(data[20:20+clen])
prim=j['meshes'][0]['primitives'][0]   # ⚠️ 是 primitives[0].attributes，不是 mesh.attributes
print(list(prim['attributes'].keys()), [a['name'] for a in j.get('animations',[])])
```

### 3.2 three.js 内嵌单文件方案（⚠️ v1.2.2 起废弃 Blob 链，改静态打包）
**沙箱 iframe / 部分 file:// 环境会拦截 `import(blobUrl)`（报 Failed to fetch）——伯努利项目实测。** 现行方案：
1. **打包脚本已随技能分发：`scripts/bundle_3d.py`**。把 `three.module.min.js` + `orbit-controls.js` + `bufferutils.js` + `gltfloader.js`（three r169 官方构建，自行下载放入工作目录）打成单 IIFE 挂 `window.ThreeBundle = {THREE, OrbitControls, GLTFLoader}`，作为普通 `<script>` 内联课件；
2. 打包三步关键（脚本已内置）：①剥 `export {..}` 块前先剥具名 `export function/const` 声明 ②import 剥除覆盖 `from 'three'` 和 `from '../utils/BufferGeometryUtils.js'` 两种 ③剥完插 `const {Ray,Plane,...} = THREE;` 解构注入（从原 import 语句解析名字），否则 body 裸用类名 ReferenceError；
3. 页面侧 `const {THREE, OrbitControls, GLTFLoader} = window.ThreeBundle;` 同步取用，零 fetch；
4. GLB 装载用 `GLTFLoader.parse(arrayBuffer, '', onLoad, onError)` 直接吃 ArrayBuffer，**不要** `URL.createObjectURL` + `.load(url)`（同为 fetch 拦截点）；
5. 交付前三道关：`node --check` 语法 → node `require()` 冒烟（mock `global.window={}`，验证 THREE.REVISION/类实例化）→ 浏览器 file:// 协议实机打开验证模型渲染。
6. 顶点色图层切换（材质 `vertexColors=true` 常开，交换 color attribute 引用 + `needsUpdate`）。
7. 发光脉冲特效：RAF 循环改 `material.emissive` 颜色与 `emissiveIntensity` 正弦脉动（startPulse/stopPulse 封装）。

### 3.3 3D 幕与 SVG 幕的"无缝一体"（关键工程约定）
- **共用外壳**：3D 幕就是普通 `<section class="scene">`，内部放 `<canvas>` 替代 `<svg class="main">`；左导航/顶栏/大纲树/底部控制条/幕切换引擎 `go()` 完全复用，NAMES 数组照常注册。
- **按需渲染**：主循环里 `if(cur===N3D) { controls.update(); renderer.render(); }`——非激活幕不渲染，省 CPU。
- **暂停联动**：全局暂停时冻结 `AnimationMixer` 与粒子推进（`mixer.update(0)`、跳过自定义步进），SVG 的 `.paused` 类与 3D 的暂停走同一开关。
- **镜头语言**：进 3D 幕时相机 position/target lerp 补间（等价 SVG 的 flyCamera），每幕配 `cam:[x,y,z], target:[x,y,z]`。
- **点选联动**：Raycaster 拾取 mesh → 弹标注 div（复用 SVG 幕的浮动卡样式）→ 同步右侧大纲 `.hl`，与 SVG region 点选行为一致。
- **漫游冲突**：canvas 的 OrbitControls 自带右键平移/滚轮缩放，**不要**给 canvas 挂 SVG 漫游引擎的 mousedown/wheel；SVG 漫游只绑 `svg.main`。
- HUD 提示条注明 3D 幕操作（"左键旋转 · 滚轮缩放 · 右键平移 · 点击部件看名称"）。

## 四、方案 B：仿真视频 / 渲染静帧内嵌（欧姆定律项目验证）

1. **动画序列**：Blender 出 PNG 序列（`--anim` 参数，如 48 帧 @12fps=4s）。
2. **合成 mp4**：本 Blender 构建无 FFMPEG 输出 → 系统 ffmpeg：
```bash
ffmpeg -y -framerate 12 -i "anim2/s_%04d.png" -c:v libx264 -pix_fmt yuv420p -movflags +faststart out.mp4
# ⚠️ ffmpeg 8.x 不支持 -pattern_type glob：先重编号 s_0001.png 连续序列
```
3. **静帧压缩**：`ffmpeg -i still.png -vf scale=960:-1 -q:v 3 still.jpg`（1.4MB PNG → 29KB JPEG）。
4. **内嵌**：mp4 → `<video src="data:video/mp4;base64,..." controls muted loop playsinline>`；jpg → SVG `<image href="data:image/jpeg;base64,...">`（SVG 内嵌位图时 audit 的无障碍项要配 `aria-label`）。

## 五、Blender 5.2 兼容坑清单（全部实测踩过，禁再踩）

| # | 坑 | 正确做法 |
|---|---|---|
| 1 | 中文 UI 下按名字找不到节点 | 一律 `next(n for n in nodes if n.type=='BSDF_PRINCIPLED'/'BACKGROUND')` 按 type 过滤 |
| 2 | 材质颜色传 3 元组报错 | Base Color / Emission Color 必须 RGBA 4 元组（封装 `rgba()` 归一化） |
| 3 | 无 `light_add_sun` 等 operator | `bpy.data.lights.new(type='SUN'/'AREA')` + `bpy.data.objects.new` 挂载 |
| 4 | 遍历 `action.fcurves` 不存在 | 多打关键帧近似匀速；或导 GLB 后用 three.js AnimationMixer 接管 |
| 5 | 无 FFMPEG 视频输出 | PNG 序列 + 系统 ffmpeg 合成（glob 不支持，先重编号） |
| 6 | 元球 `evaluated_get` 无头求值失败 | 放弃元球建模；写实结构走 blenderkit，抽象结构走常规网格 |
| 11 | **GLB 在 three.js 里"看不见"（实测伯努利项目）**：渲染循环正常（draw calls/tris 都在跑）但模型暗到融入深色背景。根因：three r155+ 物理光照单位下，EEVEE 导出的 Standard 材质用 "Ambient 1.1 + Directional 2.2" 强度严重欠亮 | 灯光全面加强（Ambient 2.6 + Hemisphere 2.2 + Key 4.5 + Rim 2.6 + Fill 1.6）+ `renderer.toneMapping = ACESFilmicToneMapping` + `toneMappingExposure=1.35`；GLB 装载后再对关键件加青色 emissive（0.3~0.4）提轮廓，地台压暗防抢戏。诊断手法：swap `MeshBasicMaterial` 纯色 + 全画面扫像素，先区分"没渲染"与"渲染了但太暗" |
| 12 | **`svg.viewBox.baseVal` 恒读 0**（Chromium 特定环境实测）：baseVal 宽高全为 0，基于它算缩放会得 NaN | 漫游引擎一律用 `getAttribute('viewBox')` 解析 + `setAttribute` 回写（封装 vbRead/vbWrite），不碰 `.baseVal` |
| 7 | 构建可能只有 EEVEE（无 Cycles/Workbench） | 先冒烟测试枚举 `RenderSettings.engine.enum_items`，按实际可用引擎写脚本 |
| 8 | 新 world 背景按名字取不到 → 背景深灰 | Background 节点按 type=='BACKGROUND' 过滤（同坑 1） |
| 9 | 灯光/世界强度过高 → Standard 变换下过曝 | 逐轮降能量降曝光，Read 渲染图肉眼验证对比度 |
| 10 | blenderkit 无头下载：操作符层不触发 | 调内部 `sys.modules['bl_ext.user_default.blenderkit.download'].start_download(asset_data, model_location=, replace=False)`，完成后从 `~/blenderkit_data/models/<slug>/<uuid>.blend` append |

**blenderkit 程序化 API 速查**（写实模型首选通道）：
```python
bpy.ops.view3d.blenderkit_search(keywords='human heart anatomy', force_clear=True)
results = sys.modules['bl_ext.user_default.blenderkit.search'].get_search_results()
# 登录：prefs.addons['bl_ext.user_default.blenderkit'].preferences.api_key = '<key>'
# 下载进度在 download_tasks；asset_data 取 results[0]（校验 name/description 匹配度）
```

## 六、质量红线（3D 通道附加验收）

1. **GLB 自检**：`primitives[0].attributes` 含预期 COLOR_N/POSITION/NORMAL；animations 数组含预期 clip。
2. **体积基调（宽松）**：3D 模型与视频**不必苛刻压缩，课件总体积几十 MB 以内均可接受**——保细节优先，不做损伤观感的极限压贴图/降帧。允许的上限内把质量做足：GLB 贴图 2–4K、视频 720p/24fps 也随意。但**硬约束只有一条：维持好的离线 HTML 使用体验**，见下方"大体积体验保障清单"。
3. **大体积体验保障清单（>5MB 时逐项落实）**：
   - **加载遮罩**：`<div id="boot">` 全屏遮罩（logo + "课件加载中…"），`window.load` 或 3D 就绪后淡出——防止大 base64 解析期间白屏让学生以为死机；
   - **视频 faststart**：ffmpeg 加 `-movflags +faststart`（moov 前置），data URI 内嵌时同样受益于顺序解析；
   - **视频懒挂载**：多个大视频时，非当前幕的 `<video>` 用 `preload="none"` + 进幕才设 `src`（或 IntersectionObserver），切换幕即 `pause()`，杜绝多视频同时解码卡顿；
   - **GLB 贴图适压**：不极限压缩，但 >4K 贴图降到 2K；`renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` 防 4K 屏 GPU 过载；
   - **canvas 占位**：3D 幕 canvas 先给 CSS 背景/骨架，模型异步装载完成前显示"模型加载中"，装载失败显示 SVG 替代图（WebGL 探测降级，见 skill-card 风险项）；
   - **逐幕按需渲染**：3D 幕离开视口立即停止 render loop（性能红线，模型越大越关键）；
   - **测试大文件打开**：交付前用本机 Chrome/Edge 实际打开一次 ≥30MB 的成品确认加载流畅（file:// 协议下 data URI 解析无报错）。
4. **3D 幕回归 7 项**：旋转/缩放/平移、点选出标注、暂停冻结动画、进幕镜头补间、退出幕停止渲染（性能）、控制台 0 报错、与 SVG 漫游互不干扰。
5. **视频/静帧**：mp4 可播放（muted+loop+playsinline）、帧 md5 验证非静帧、jpg 有 aria-label。
6. **物理正确性**：模型结构/颜色语义/动画参数与教材核对（视觉编码表逐条过），AI 参考图带来的错误不得带入成品。
7. audit_courseware.py 仍须 ≥90 分（base64 内嵌满足 P0 单文件/内嵌图检查）。

## 七、实作范例索引

| 项目 | 路径 | 看点 |
|---|---|---|
| 心脏解剖（A 通道） | `D:\coding2026\课件-心脏解剖\` | build_courseware.py：three.js Blob URL 链、GLB base64、顶点色 5 图层切换、AnimationMixer 心跳、Raycaster 点选、脉冲特效、8 模式镜头联动 |
| 欧姆定律（B 通道） | `D:\coding2026\课件-欧姆定律\` | 课件.html 第④幕：mp4/jpg base64 内嵌 + SVG 滑块仿真并存 |
| 欧姆定律建模工程 | `D:\coding2026\欧姆定律3D\` | ohms_law_3d.py：从零建模铁律完整范式（设计.md → ImageGen 参考图 → 7 零件函数 → 组装 → 静帧/动画渲染） |
