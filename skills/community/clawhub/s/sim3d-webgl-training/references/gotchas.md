# gotchas.md — 弱模型防呆机制清单（写代码前通读）

> 全部来自真实项目的踩坑记录。每一条都对应过一个实际的 bug。

## 🔴 致命项（犯了必返工）

### 1. 视口宽高变量遮蔽
**症状**：2D 引线标签全部消失，或高度计算错乱。
**原因**：视口高命名 `h`，与热点遍历 `for (const h of hotspots)` 冲突。
**铁律**：视口尺寸**永远命名 `viewW` / `viewH`**；热点循环变量用 `hs` / `item`，禁用单字母。

### 2. 外部 CDN 引用
**症状**：离线打开白屏，控制台 `net::ERR_INTERNET_DISCONNECTED`。
**铁律**：全文搜索 `http://`、`https://`、`cdn`、`three`、`import`——**不允许出现任何网络资源引用**。字体用系统字体栈（见 core-engine.md §1）。

### 3. 一次性直出超长代码被截断
**症状**：HTML 尾部 `</script></body></html>` 缺失，或函数写一半断掉，浏览器静默失败。
**铁律**：预计 >1500 行时，用 **Python 脚本分模块拼接**（见 SKILL.md 第 2 步），每模块是独立字符串，最后写单文件；或分多次输出再合并。
**自检**：文件末尾必须是 `</script>\n</body>\n</html>`；所有 `function` 定义数与调用数大致匹配。

### 4. 半透明外壳挡死内部结构
**症状**：透明壳内零件看不清，或透视模式下出现浑浊双层叠加。
**原因**：半透明件写深度缓冲，遮挡后画的内部件。
**铁律**：Pass1 不透明（`depthMask(true)`）→ Pass2 半透明+粒子（`depthMask(false)`）；且外壳必须是**中空侧板/剖面结构**（弧段 tube / lofted 侧面），不封整体端盖。

### 5. 拖拽旋转误触选中零件
**症状**：转个视角就弹出零件详情，无法正常观察。
**铁律**：mouseup 里判断 `Math.hypot(e.clientX - startX, e.clientY - startY) < 5` 才触发拾取（渲染规则 §4 已内置）。

### 6. 人物穿模
**症状**：3D 技师卡进举升机立柱/舱壁/机身。
**铁律**：技师朝向用 `Math.atan2(dx, dz)` 固化公式；**工位坐标一律设在设备包围盒外侧**（与设备中心距离 ≥ 包围半径 + 0.4）。人物移动用插值（0.08 系数），瞬移会穿模。

## 🟡 高频项（犯了明显降质）

### 7. 非均匀缩放导致法线畸变、死黑高光
**症状**：拉伸过的圆柱/压扁的球体表面一片死黑或高光怪异。
**原因**：`mat3(uModel)` 含缩放因子，法线未归一化。
**铁律**：顶点着色器必须用法线矩阵重归一化写法（core-engine.md §3 PBR_VS，**不可删改**）。

### 8. 着色器编译错误静默失败
**症状**：整个 3D 区域全黑。
**铁律**：`createShaderProgram` 里必须有 `getShaderParameter` 检查 + `console.error`（core-engine.md §3 已内置）。开发期打开控制台看一眼。

### 9. Uint16 索引溢出
**症状**：部件数量多时网格显示残缺、顶点乱飞。
**原因**：`Uint16Array` 最多 65535 顶点。
**铁律**：MeshBuilder.compile 用 `Uint32Array`（需 WebGL2）；场景型 unit 网格复用（uploadMesh 版）顶点少可用 Uint16。

### 10. 爆炸视图后引线锚点不跟随
**症状**：爆炸时标签飘在空中不贴部件。
**铁律**：leaderAnchors3D 的 pos 计算里叠加爆炸位移（参照内燃机样本：`pos: [0.12, 3.55 + expSpark[1], zOffset]`），且每帧重填 `leaderAnchors3D.length = 0` 再 push。

### 11. Canvas 未处理 devicePixelRatio → 高分屏模糊
**铁律**：每帧检查 `canvas.width !== clientWidth * dpr` 并 resize（core-engine.md §4 主循环已内置）；2D 画布 `ctx.scale(dpr, dpr)` 后按 CSS 像素绘制。

### 12. 音效在首次交互前创建 AudioContext 被浏览器拦截
**铁律**：AudioContext 惰性创建 + 首次点击时 `resume()`（core-engine.md §6 已内置）。默认 `soundEnabled: false`，用户手动开启。

## 🟢 质感项（决定"高逼真"观感）

### 13. 只会方块拼积木（Minecraft 感）
**对策**：旋转体一律 `addCylinder`/`addTubeSection`（≥32 段）；机壳加散热孔阵列（循环 addBox/extruded）；板金件加倒角与分缝线；线缆用 `buildTubeMesh` 弯管；弹簧用 `addHelicalSpring`。参考 cad-library.md §4 五个范例。

### 14. 场景空旷没有车间氛围
**对策**：地面用 `uIsFloor=1` 程序化网格 + 暗角；必配设备：举升机/工具车/剪叉台（车间）、值机岛/传送带（安检）、登机桥/廊桥（空港）；安全元素：黄黑警示桩链、警示牌（emissive 微光）。

### 15. 材质单一塑料感
**对策**：按渲染规则 §6 材质速查表分层设置 metallic/roughness；关键件加 `uSurfaceType`（珩磨网纹/车削纹/铸造颗粒）；安全件（高压线/警示）加 `uEmissive 0.1~0.25` 微光。

### 16. 动态过程没有"生命感"
**对策**：至少 2 种粒子流（如气流+火花）；运动部件（轮转/曲轴/传送带）与参数联动；状态灯闪烁（`Math.sin(t*8) > 0 ? emissive : 0`）；相机预设位切换有阻尼过渡。

### 17. 教学闭环是摆设
**症状**：有 SOP 面板但点不点都一样。
**铁律**：每步必须 `checkFn` 实时校验 + 操作函数末尾调 `renderSopSteps()`；考核模式隐藏一键按钮；安全红线扣分必须联动弹窗+日志+仪表。

### 18. 术语不专业
**对策**：教学文案用行业术语（预位/验电/互锁/珩磨/凸轮升程…），参数带真实量纲（kN/°CA/bar/K/mm/V/Ω）；对照 teaching-modes.md §9 规范表。不确定的规程先搜索再写。

## ✅ 交付前 Checklist

- [ ] 文件完整：末尾 `</script></body></html>` 齐全，无 `TODO`/占位符
- [ ] 无任何外部网络引用（http/cdn/import）
- [ ] 控制台 0 ERROR（含着色器编译）
- [ ] `viewW`/`viewH` 命名检查：grep 无 `const h =`、`let h =` 与视口相关
- [ ] 双通道渲染：depthMask 切换存在
- [ ] 5px 拾取阈值存在
- [ ] 技师工位在设备包围盒外（如有技师）
- [ ] 拖拽旋转/缩放/点击拾取/相机预设 全部可用
- [ ] SOP 步骤：至少 1 个模块 3 步以上，checkFn 可真实触发
- [ ] 考核：扣分函数 + 评价单弹窗存在（考核型）
- [ ] 运行 `python scripts/audit_sim3d.py <成品.html>` ≥ 85 分

## §19 数据驱动架构防呆（SIM_CONFIG，火箭/irb_6700 实战验证）

1. **🔴 `renderFaultPanel` 必须生成完整面板**：注入按钮组 + `diagSelect` 诊断下拉 + 提交按钮都要在这个函数里 innerHTML 出来。只写"故障详情"会导致 `diagnoseFault()` 读 `diagSelect.value` 时 null 报错（火箭项目实战坑）。
2. **🔴 配置与渲染器的字段名必须一一对应**：`SIM_CONFIG.components[i].explodeVec / pos / leaderOffset / testPoints / specs` 少一个字段，渲染循环里就是 `undefined * exp = NaN` 矩阵，整机消失。写完数据先过一遍 §8 数据量自检清单。
3. **🟡 步骤校验函数命名统一**：教学模块用 `check` 还是 `checkFn` 全文件只能有一种；无头验证脚本按实际命名调用（火箭项目因此返工一次）。
4. **🟡 `_livePos` 动态坐标**：HUD 引线/相机飞跃/技师朝向都读 `comp._livePos`，每帧渲染时必须 `setLivePos(id, worldPt)` 更新；静态 `pos` 只是初始锚点。
5. **🟡 事件边沿触发**：飞行剖面/工况切换的状态提示（MaxQ、MECO…）用 `if (cond && !flags[key]) { flags[key]=true; ... }` 边沿锁，禁止每帧重复 logAction。
6. **🟡 断电态一致性**：`powerOff` 时必须同时抑制——关节动画、波形采样、遥测电流/电压（读 0）、激光束；但编码器电池回路（vNorm=5V）可保留，这是真实电气常识。
7. **🟢 万用表微抖动**：读数加 `Math.sin(simTime*5.3)*0.02` 量级抖动，避免数值"死板"像假数据；异常判定用 |fault-norm| 阈值（V:1/Ω:5/MΩ:10/A:3）。
8. **🟢 考核模式隐藏一键按钮**：exam 模式下 `.step-action-btn` 不渲染（学生必须手动操作），teach 模式才显示。

## §20 交付前 Checklist（新增内容密度项）

- [ ] `SIM_CONFIG` 单源数据：components≥8（specs≥4行+testPoints 8值）/sopSteps≥5/faults≥4（含quiz）
- [ ] 万用表≥3档位+表笔选择；示波器/雷达二选一以上；遥测条≥3项 `tele-` id
- [ ] 工况≥2种；关节限位表（机械臂）；标准引用≥1个真实标准号
- [ ] `renderFaultPanel` 完整面板（注入+诊断+提交）；`check`/`checkFn` 命名统一
- [ ] 运行 `python scripts/audit_sim3d.py <成品.html>` ≥ 85 分且"内容密度块"全过
