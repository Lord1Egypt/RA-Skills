# SAW滤波器参考文献 — 详细笔记

---

## 1. Abbott (2016) — Piston Mode 原理性文献

**文件：** `Abbott2016-piston mode原理性文献.pdf` + 5张LDV图片页

### 核心贡献
提出了 SAW 横向模抑制的 **Piston Mode** 设计方法。

### 问题
普通 SAW 的横向能量分布为 cosine 型，激发出多个横向模式（spurious modes），导致：
- 频响中产生 ripple 和杂散峰
- Q 值下降
- 滤波器选择性降低

### 解决方案：横向速度剖面（Velocity Profiling）

```
区域划分：
┌─────────────────────────────────────────┐
│ Busbar (low v)  │ Gap (high v) │ Aperture │ Gap (high v) │ Busbar │
└─────────────────────────────────────────┘

Δv/v = (v_g - v_c) / v_c  → 控制piston模态质量
```

### Piston Mode 条件
- 中心孔径区域：ky → 0（横向wavenumber趋近于零）
- 过渡区：evanescent decay 速率匹配
- 设计目标：平坦位移分布，|u(y)| ≈ const（对于 |y| < Wa/2）

### 关键公式
**Tiersten 方程（横向模式）：**
```
(∂²/∂x² + (1-γ)·∂²/∂y² + k²) · ψ(x,y) = 0
```

**Piston 条件：**
```
横向wavenumber ky → 0
→ 中心区域为平面波传播
→ 高阶横向模式被截止
```

### 几何参数
```
Wa : 孔径宽度（15λ–40λ）
Wg : gap宽度（高速度区域）
Δv/v : 速度对比度（通常 1%–5%）
γ : 各向异性因子
```

### 实现方式
1. **Dummy Electrodes**：两侧虚拟指增大局部声速
2. **Hammerhead 结构**：边缘加厚金属→局部慢速→piston效应
3. **Lithium Tantalate 42° YX切向**：最大化各向异性
4. **多节groove结构**（TCSAW常用）

---

## 2. After 60 years — Q因子新公式

**文件：** `After_60_years_A_new_formula_for_computing_quality_factor_is_warranted_text.txt`

### 核心问题
传统 BVD Q公式的局限性：
- 只考虑 Rs（动态电阻）
- 忽略 R0（漏电导）和贴片质量 Γ 的频率依赖性
- 对高Q谐振器误差可达 20–50%

### 传统公式
```
Qm = 1/Rs · √(L/C)
```

### 新公式（动态质量法）
```
Qm = 2π · fR · Γ · Cm² / (Γ²·Rs + Γ·Rm)

其中：
  Γ  = 有效机械质量（Load Mass，含声辐射）
  Cm = 动态电容
  Rs = 动态电阻（导带+电极损耗）
  Rm = 其他损耗（贴片质量损耗等）
```

### 实测 Q 值
```
Q = fR / f_-3dB

其中 f_-3dB = 阻抗幅度从最大值下降3dB的带宽
```

---

## 3. Iwamoto (2018) — IHPSAW（Murata）

**文件：** `Iwamoto-2018-IHPSAW.pdf` + FEM仿真图片

### 核心技术：I-HP SAW（Inverted High-Performance SAW）

**结构（自上而下）：**
```
第1层：LiTaO₃ 压电薄膜 + IDT金属电极
第2层：SiO₂ 热补偿层
第3层：High-velocity Si 衬底（声速>压电层，声波无法泄漏）
```

### 核心性能
| 参数 | 传统SAW | TCSAW | IHPSAW |
|------|---------|-------|--------|
| Q | ~1000 | ~2000 | **>3000** |
| TCF | -40 ppm/°C | ≈0 | **≈0** |
| 插入损耗 | -2dB | -1.5dB | **<-1dB** |
| k² | 0.5% | 0.3% | 0.8% |
| 适用频段 | <2GHz | <2.5GHz | **1–5GHz** |

### 关键公式
```
机电耦合：
  k² ≈ (π/2) · (fR/fA) · tan((π/2)·(fA-fR)/fA)

Q因子：
  Q = ω · (存储能量) / (每周期耗散能量)
  IHPSAW: Q > 3000 @ 2GHz

TCF补偿：
  TCF_total = α·TCF_LiTaO3 + β·TCF_SiO2 ≈ 0
```

---

## 4. Modified BVD — FBAR/SAW 等效电路

**文件：** `Modified_Butterworth-Van_Dyke_circuit_for_FBAR_resonators_and_automated_measurement_system_text.txt`

### MBVD 扩展项
在标准 BVD 基础上新增：
- `R0`：静态电容 C0 的分流电阻（漏电导 Go = 1/R0）
- `Rm`：其他损耗来源
- `Cp`：封装/探头寄生电容

### 导纳公式
```
Y(ω) = j·ω·C0 + 1/R0 + 1/[Rs + j·ω·Lm + 1/(j·ω·Cm)]
```

### 参数提取方法（自动化）
- 最小二乘法优化测量阻抗曲线
- 分离 fR（串联）和 fA（并联）区域
- 从 fR 附近数据提取 Rs, Lm, Cm
- 从 fA 附近数据提取 R0, C0

---

## 5. TCSAW — 温度补偿 SAW

**文件：** `TCSAW-_text.txt`

### 两种主流结构
**（1）Filled TCSAW（在LiNbO₃上直接沉积SiO₂）**
- 工艺简单，与标准SAW兼容
- SiO₂厚度：0.5–2λ

**（2）Grooved TCSAW（刻蚀LiNbO₃形成沟槽再填充SiO₂）**
- TCF补偿效果更好
- 需要额外刻蚀工艺

### TCF补偿机制
```
TCF_LiNbO₃ ≈ -75 ppm/°C（负）
TCF_SiO₂ ≈ +35 ppm/°C（正）

通过调节SiO₂厚度实现零TCF：
  h_SiO2 / h_total ≈ TCF_LiNbO3 / (TCF_LiNbO3 - TCF_SiO2)
```

---

## 6. Layered SAW — 双共振近零TCF

**文件：** `Layered_SAW_Resonators_with_Near_Zero_TCF_at_Both_Resonance_and_Anti-resonance_text.txt`

### 目标
在 fR（串联谐振）和 fA（并联谐振）两个频率点同时实现近零TCF。

### 技术路线
```
POI (Piezoelectric on Insulator) 技术：
  顶层：SiO₂（热补偿）
  中层：薄层压电材料
  底层：高声速衬底

→ fR和fA的TCF同时接近0
```

---

## 7. Sin加权 (1992)

**文件：** `sin加权原始文献-1992.pdf`

### 核心方法
对 IDT 的指重叠长度（aperture）施加 sin 加权函数：
```
A_n = sin(n·π·W_a / L)   （n为第n个电极对）
```

### 效果
- 降低IDT的频谱旁瓣（sidelobe suppression）
- 减小衍射效应
- 主要用于频谱整形滤波器设计

---

## 8. Tanski (1979) — 横向模谐振

**文件：** `tanski1979-横向模谐振.pdf`

### 核心研究
SAW 横向模式（transverse mode resonance）的早期理论分析。

### 关键发现
- IDT 电极边缘的反射导致横向谐振
- 谐振频率与孔径宽度直接相关
- 提出了横向模式的简化模型

---

## 9. US20210313961A1 — 高通栅格

**文件：** `US20210313961A1_高通栅格_text.txt`

### 技术内容
SAW 高通滤波器的栅格结构专利设计。

### 核心特点
- 利用高声速栅格结构实现高通特性
- 抑制低频横向模式
- 适用于射频前端高通滤波应用
