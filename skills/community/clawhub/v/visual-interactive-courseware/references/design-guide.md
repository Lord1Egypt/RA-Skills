# 视觉与交互设计规范（专业级）

> 品质基准：三张标杆截图——①医学软件级应用外壳与图层化解剖（Visible Body 类）
> ②电影感 3D 地形叙事（历史地理动画）③暗色科技风爆炸图+步骤标注流（原理拆解视频）。
> 达不到这三张图的水准，就不叫"高水平的可视化交互课件"。

## 设计总原则

**双主题路线，按学科气质选**：
- **浅色医学插图主题**（生物/人体/解剖类首选）：淡青底 `#E8F2F0` + 医学青强调 `#0E9888` + 动脉红 `#C43B2E` / 静脉蓝 `#2E6DA8`。对标"生命寻动"类全身解剖插画：器官用多段 C 曲线 + 径向渐变塑真实形态，血管树由粗到细有锥度，白胶囊标注 + 引线。
- **深色电影感主题**（物理/天文/科技类首选）：`#070D1A` 底 + 青蓝 `#38BDF8` 强调 + 辉光效果。
- 两者共同底线：主视觉用 SVG 渐变（radialGradient/linearGradient）+ 滤镜营造质感，**拒绝平面色块**；生物结构必须"类解剖"形态（心尖朝向、沟回纹理、大血管空间关系），**拒绝爱心形卡通心脏**。

### 浅色医学插图主题要点（生物类标杆配置）

| 元素 | 规范 |
|------|------|
| 应用外壳 | 同深色版四区结构，但面板纯白 `#FFFFFF`，背景淡青，强调色医学青 |
| 器官渲染 | radialGradient（高光偏移 40%/32%）+ 深色描边 + feDropShadow；肝/肾/肠用棕红系（#A85A48→#6E3325） |
| 血管树 | 由粗到细（主动脉 8px → 末梢 3px）+ dash 流动动画 + 圆角线帽；动/静两套颜色与速度 |
| 毛细血管网 | `<pattern>` 散点模拟（红蓝交替小圆点），填充在手足末端、脑部椭圆区域 |
| **白胶囊标注** | HTML absolute 定位 div：白底 95% 不透明 + 圆角 10px + 阴影；标题行 = 色点 + 器官名（用器官色），描述 11.5px 灰 |
| **标注引线** | JS 动态生成 SVG polyline：胶囊边缘中点 → 水平拐点 → 器官目标点 + r=4 端点圆。用 `getScreenCTM().inverse()` 把屏幕坐标转 viewBox 坐标，resize 时重算。引线组置于 SVG 最顶层 |
| **分段时间轴** | 底部控制条：段名标签行 + 比例分段条（JS 按 dur 比例生成 `.tl-seg`，段间白色分隔线）+ 段内进度填充 + 圆形旋钮 + 速度组 0.75×/1×/1.5×/2× + 总时长计时器 |
| 全身比例 | viewBox 高度 ≥ 1080 容纳站姿全身；头顶预留 ≥ 100px 给提示条；人体宽度占 viewBox 约 45% 居中 |

⚠️ **人体比例三坑（实测踩过）**：
1. 头顶与提示条重叠 → 整体 `<g transform="translate(0,N)">` 下移，顶部留白
2. 手足毛细血管网椭圆脱离肢体末端 → 椭圆圆心必须压在肢体末端路径坐标上
3. 心脏顶到颈部/肺过宽 → 心脏上缘不高于肺中线，肺内缘与心脏留 8px+ 呼吸空隙

## 应用级外壳（必备）

课件外壳必须像专业软件，不是网页幻灯片。四区结构：

| 区域 | 内容 | 对标 |
|------|------|------|
| 左侧导航栏 | 图标+文字的垂直幕导航（56px 按钮，激活态辉光）、底部教师模式/全屏开关 | 医学软件工具栏 |
| 顶栏 | 课程名+教材版本（左）、**模式切换 Tab 组**（中右，如"全循环/肺循环/体循环"图层切换）、图例（右） | 3D 软件模式条 |
| 右侧面板 | **知识大纲树**：每幕展开子知识点，可点击跳幕；SVG 点选部件与大纲条目双向高亮联动；底部教师提示卡（教师模式显示） | 知识大纲/图层树 |
| 底部控制条 | 上一幕/播放暂停（主按钮 52px 辉光）/下一幕、**可点击进度条**、幕序号指示、速度切换（0.5×/1×/2×） | 视频播放器 |

外加"幕内叠加层"：左上角电影式字幕标题（`01` 编号 + 标题 + 副标）、左下角浮动观察任务卡、右侧步骤序列器（见下）。

## 电影感镜头语言

- **viewBox 补间运镜**：进幕时用 `flyCamera(svg, from, to, dur)` 对 viewBox 做缓动插值，实现"镜头推近"（如从全景推进到肺泡）。缓动函数用 easeInOutQuad。
- **步骤聚光**：序列器走到某步时，非当前路径/区域降为 opacity .16-.30，当前路径加粗（stroke-width 6→10）+ 辉光滤镜，模拟聚光灯。
- **微动效营造生命感**：心脏持续 beat 脉动（scale 1→1.055 双峰波形）、心率仪表随机微跳（72±6 bpm）、血流 dash 流动（art/ven 两套速度错开形成层次）。

## 画布漫游 + 全局镜头联动（课件级必备模式）

知识型课件必须支持"自由探索 + 引导镜头"双通道，二者共享同一 viewBox 状态：

### 1. 拖动平移 + 滚轮缩放引擎
```js
const HOME_VIEW = { x:0, y:0, w:1080, h:1086 };   // 记录初始 viewBox
let pan = null, panMovedAt = 0;
svg.addEventListener('mousedown', e=>{            // 开始拖动：打断镜头补间
  if(vbAnim) cancelAnimationFrame(vbAnim);
  const vb = svg.viewBox.baseVal;
  pan = { sx:e.clientX, sy:e.clientY, x:vb.x, y:vb.y, w:vb.width, h:vb.height, moved:false };
});
window.addEventListener('mousemove', e=>{
  if(!pan) return;
  const ctm = svg.getScreenCTM();                 // ⚠️ 用 getScreenCTM 精确换算，勿用 rect 宽高比
  const dx = (e.clientX-pan.sx)/(ctm?ctm.a:1), dy = (e.clientY-pan.sy)/(ctm?ctm.a:1);
  if(Math.abs(e.clientX-pan.sx)+Math.abs(e.clientY-pan.sy) > 3) pan.moved = true;
  svg.setAttribute('viewBox', (pan.x-dx)+' '+(pan.y-dy)+' '+pan.w+' '+pan.h);
});
window.addEventListener('mouseup', ()=>{ if(pan){ panMovedAt = pan.moved ? Date.now() : 0; pan=null; } });
svg.addEventListener('wheel', e=>{                // 滚轮：以光标为锚点缩放
  e.preventDefault();
  const vb = svg.viewBox.baseVal, ZOOM = e.deltaY<0 ? 0.86 : 1.16;
  const w = Math.max(120, Math.min(HOME_VIEW.w*1.6, vb.width*ZOOM));   // 边界钳制
  const h = w/HOME_VIEW.w*HOME_VIEW.h;
  const p = svgPoint(e);                          // 光标 → viewBox 坐标
  svg.setAttribute('viewBox', (p.x-(p.x-vb.x)/vb.width*w)+' '+(p.y-(p.y-vb.y)/vb.height*h)+' '+w+' '+h);
}, { passive:false });
```

### 2. 点击目标联动镜头（知识点/环节 → 推近）
- 维护坐标表：`ORGAN_CAM = { brain:{x,y,w}, heart:{...}, ... }`、`SEG_CAM = { 0:HOME_VIEW, 1:..., ... }`
- 点击大纲知识点 / 课程环节 / 器官热点 → `tweenViewBox(cam, 700-900ms)` 推近到对应区域
- 模式切换（MODE_MAP）也应携带 `cam` 字段，切 Tab 即推镜头

### 3. 三个必须处理的冲突（血泪教训）
- **拖动误点击**：`mouseup` 时记录 `panMovedAt = Date.now()`；点击处理器开头 `if(Date.now()-panMovedAt < 300) return;`
- **双击复位 vs 单击开面板**：单击动作延迟 240ms 执行（`setTimeout`），`dblclick` 时 `clearTimeout` 全部待发动作——否则双击复位的第一次点击会先弹开器官面板
- **播放状态同步**：任何 `playing = false` 的地方必须同步 `stage.classList.add('paused')`，否则动画停了但 UI 显示未暂停，播放按钮行为错乱

### 4. 透明热区必须有可见锚点
透明 `<ellipse>` 热区学生"看不见摸不着"。标配：每个热区配一个 `.organ-pin`（脉冲圆点 + 悬停显示器官名白胶囊）。标记层 `pointer-events:none`，点击仍由热区接。

### 5. 交付前回归测试清单（playwright 实测 14 项）
滚轮缩放 ✓ 拖动平移 ✓ 双击复位 ✓ 知识点→推近 ✓ 环节→推近 ✓ 模式Tab→推近 ✓ 热区高亮 ✓ 热区→深读面板 ✓ 拖后无误触 ✓ 缩放边界 ✓ 暂停切换 ✓ 播放状态同步 ✓ 器官标记数量 ✓ 键盘翻页 ✓

## 步骤序列器（对标"①-⑥"标注流）

过程/流程类知识（血液循环、有丝分裂、工艺流程）的最后一幕**必须**配备右侧步骤流：
- 每步一张 chip：圆形序号 + 加粗小标题 + 一句描述
- 自动步进（约 2.6s/步 × 速度系数），点击 chip 可手动跳步
- 当前 chip 高亮（青色描边+辉光+左移 6px），已走过的序号变淡青
- 与 SVG 联动：每步对应 SVG 内 `data-s` 路径/区域的显隐与加粗

## SVG 质感规范（重要工程约束）

- **每个 `<svg>` 必须自带完整 `<defs>`，渐变/滤镜 ID 全局唯一**（后缀 `-2`/`-3` 区分）。
  ⚠️ 血泪教训：Chromium/Edge 下**跨 SVG 引用 `url(#id)`，若被引用元素位于 `display:none` 的 SVG 内则解析失败**，导致整个 stroke 不渲染（路径凭空消失）。同名 ID 重复时只认文档第一个——同样会炸。
- **写实组织纹理（最大写实度核心手法）**：`feTurbulence` + `feDiffuseLighting` 叠加凹凸光照，再 `feComposite(arithmetic k1≈1.15)` 与源图相乘、`feComposite(in)` 裁剪到 SourceAlpha、末接 feDropShadow。三种预设：
  - 心肌 `fHeartTex`：`baseFrequency="0.09 0.012"`（横向拉伸模拟肌纤维）+ surfaceScale 1.5
  - 肺 `fLungTex`：`fractalNoise baseFrequency="0.82"`（细密蜂窝感）
  - 肝/肾通用 `fOrgan`：`fractalNoise 0.5` + surfaceScale 1.5
- **解剖学结构红线**（结构类课件必须达标，否则即"卡通"）：
  - 心脏：心尖朝患者左下（画面右下）、冠状沟 + 前室间沟、LAD/RCA 冠状动脉走行、右心房暗紫色区分（`gRA`）、主动脉弓深红渐变
  - 肺：右肺三叶（斜裂+水平裂）、左肺两叶（斜裂+心切迹）、气管+左右支气管、肺门血管纹理
  - 肝：镰状韧带分左右叶 + 胆囊（绿色梨形）
  - 肠：结肠袋横痕 + 小肠盘曲 + 升/横/降结肠框
  - 脑：大脑沟回多段曲线 + 小脑（独立椭圆+纹） + 脑干
  - 肾：肾门凹陷 + 输尿管
- **血管颜色精准（教学红线）**：肺动脉画蓝（流静脉血）、**肺静脉画红（流动脉血——七年级最大易错点）**、肝门静脉入肝、血管用"渐变粗干 + 半透明高光细线"双层模拟圆柱体积
- 人体皮肤：径向渐变 `gSkin`（暖白→肤色边缘）替代平涂半透明 + 锁骨/胸肌/腹肌暗示线
- 辉光滤镜模板：`feGaussianBlur stdDeviation=2.6 → feMerge(blur + SourceGraphic)`，区域 x/y -40% width/height 180% 防裁切。
- 血管管线：粗线（6-10px）+ `stroke-dasharray:10 7` + dashoffset 动画 + 线帽 round + 渐变描边（如 #FF7B8C→#E11D48）。
- 有机形体（心、肺、肾）用多段 C 曲线拼真实轮廓，叠 1-2 条半透明白弧线当"高光/沟回"，禁止单个 path 敷衍。
- 微观场景（肺泡、细胞）放大呈现：主体圆 + 缠绕毛细血管（紫色 #A855F7）+ animateMotion 红细胞单行通过 + O₂（绿）/CO₂（红）粒子沿路径迁移。
- 人体/地貌剪影：低透明度（.3）勾环境，别抢主视觉。
- **特写运镜验证**：验收时用 `setAttribute('viewBox', 'x y w h')` 推近主器官截图检查纹理细节——远景合格不代表特写合格。

## 语义色（深色主题版）

| 含义 | 色 | 辉光 |
|------|-----|------|
| 动脉血/含氧 | #FF4D5E 系渐变 | 0 0 12px rgba(255,77,94,.75) |
| 静脉血/缺氧 | #3B82F6 系渐变 | 0 0 12px rgba(59,130,246,.75) |
| 毛细血管/交换 | #A855F7 | — |
| O₂/养料 | #34D399 | — |
| CO₂/废物 | #F87171 | — |
| UI 强调 | #38BDF8（青蓝） | 0 0 14px rgba(14,165,233,.4) |

## 字号（投影最低标准）

| 元素 | 最小字号 |
|------|---------|
| SVG 内关键标注 | 13px（1200 viewBox 下）≈ 投影 20px+ |
| 幕标题 | 22px（叠加字幕式，带 text-shadow） |
| 浮动卡/大纲树 | 13px |
| 底部指示器 | 13px |

## 布局

- CSS Grid 三栏：`76px 导航 | 1fr 舞台 | 316px 大纲`，行高 `56px 顶栏 / 1fr / 64px 控制`。
- viewBox 统一 `0 0 1200 760`，`preserveAspectRatio="xMidYMid meet"`。
- 全屏模式：body.fs 类把侧栏宽归零并隐藏，舞台自动放大。
- 键盘/翻页笔：←→ 翻幕、空格播放暂停（PageUp/PageDown 兼容翻页笔）。

## 交互控件规范

| 控件 | 适用 | 深色主题样式 |
|------|------|------|
| 模式 Tab 组 | 图层切换（全循环/肺循环/体循环） | 圆角容器内胶囊按钮，激活态渐变+辉光 |
| 命中区 | 全部可点元素 | ≥ 44×44px |
| 区域点选 | SVG 结构部件 | hover 提亮，点击高亮 + 大纲树条目同步 `.hl` |
| 进度条 | 幕切换 | 5px 高圆角条，可点击跳幕，填充渐变+辉光 |
| 速度切换 | 演示节奏 | 0.5×/1×/2× 循环 |

## 教师模式

左侧栏 🎓 开关 → body.teacher-mode → 右下角显示琥珀色教学提示卡（导入提问/易错点/互动建议/追问）。

## 验收清单（每幕必过）

1. 三种视口截图检查：1600×900 / 1366×768 / 1024×768；1024 下检查 `document.documentElement.scrollWidth` 无横向溢出（控制条控件需媒体查询收缩）
2. 每个渐变引用的路径在**其他幕激活时**依然渲染（跨 SVG 引用陷阱）
3. **特写检查**：viewBox 推近主器官截图，确认纹理滤镜/沟回/血管走行在放大后依然精致
4. 步骤序列器自动步进 + 点击跳步 + 与 SVG 联动正常
5. 播放暂停对 dash 动画、beat 动画、序列器同时生效
6. 功能回归（完整 14 项清单见上文「5. 交付前回归测试清单」）：暂停、速度、时间轴跳转、键盘翻页、点选联动、标注引线数量、模式循环无 JS 错
7. **画布漫游回归**（playwright 页面级事件，勿用 `locator.dblclick`——会被遮挡元素拦截超时）：滚轮缩放以光标为锚、拖动平移与 `getScreenCTM` 换算一致、双击复位、拖动结束 300ms 内不触发点击、知识点/环节/模式Tab 均联动镜头
8. 控制台 0 报错（favicon 404 可忽略）
