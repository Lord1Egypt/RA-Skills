# Shader 效果起手式

这份参考不是效果大全，而是把常见视觉需求快速映射到可落地的 shader 结构。

## 1. 流动渐变

适合：

- 背景动画
- 品牌页氛围层
- loading 背景

起手：

- 先做 UV 渐变混色
- 再用 `sin` 或低频 noise 推动颜色边界
- 不要一上来就叠很多 octave

关键词：

- `uv`
- `mix`
- `sin`
- low-frequency noise

## 2. 水波 / 径向波纹

适合：

- 点击反馈
- 能量扩散
- 科幻面板

起手：

- 先算中心点到当前像素的距离
- 用 `sin(distance * scale - time * speed)` 做波纹
- 用 `smoothstep` 控制带宽和衰减

关键词：

- radial distance
- ring mask
- falloff

## 3. 溶解

适合：

- 角色消散
- UI 显隐特效
- 材质切换

起手：

- 用 noise 生成阈值图
- 用一个进度值和 noise 比较
- 用边缘带单独上色，别只做硬切

关键词：

- threshold
- edge band
- burn color

## 4. 菲涅耳 / 边缘发光

适合：

- 护盾
- 全息材质
- 轮廓强化

起手：

- 计算视线方向和法线的点积
- 用 `1.0 - dot(viewDir, normal)` 做基础 fresnel
- 再决定是否乘颜色、强度或噪声

关键词：

- view direction
- normal
- rim light

## 5. 顶点波动 / 呼吸形变

适合：

- 旗帜
- 水面
- 有机表面

起手：

- vertex shader 里沿法线或某个轴偏移
- fragment shader 先保持简单，先确认形变本身是对的
- 位移不要和颜色问题混在一起一起查

关键词：

- vertex displacement
- normal offset
- world/object space

## 6. 扫描线 / HUD

适合：

- 监控视图
- 科幻 UI
- CRT 风格

起手：

- 用屏幕空间坐标生成重复条纹
- 叠轻微噪点和时间偏移
- 让强度可调，不要把底图盖死

关键词：

- screen-space bands
- scanline mask
- overlay

## 7. 像素化 / 马赛克

适合：

- 转场
- 复古滤镜
- 内容遮挡

起手：

- 先量化 UV 再采样纹理
- 单独控制像素格大小
- 纹理类效果先确认采样链路可用

关键词：

- quantized uv
- texel block
- nearest-style sampling

## 选型建议

- 用户只要“动态背景”：先从流动渐变或低频 noise 开始。
- 用户要“有交互反馈”：优先水波、径向扩散、扫描线。
- 用户要“模型材质更有感觉”：优先菲涅耳、溶解、顶点波动。
- 用户说“像 ShaderToy 一样炫”：先做屏幕空间版本证明视觉，再决定要不要移植成材质。
