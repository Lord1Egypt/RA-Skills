# 半导体器件物理参考

> 基准来源: S.M. Sze "Physics of Semiconductor Devices" 3rd Ed, Streetman "Solid State Electronic Devices"
> 数据取典型值，具体参数以实际工艺规格为准。

## 1. 能带理论基础

### 1.1 常见半导体禁带宽度 (300K)

| 材料 | 符号 | 类型 | E_g (eV) | 晶格常数 (Å) |
|------|------|------|----------|-------------|
| 硅 | Si | 间接 | 1.12 | 5.431 |
| 锗 | Ge | 间接 | 0.66 | 5.658 |
| 砷化镓 | GaAs | 直接 | 1.42 | 5.653 |
| 氮化镓 | GaN | 直接 | 3.39 | a=3.189, c=5.185 |
| 碳化硅(4H) | 4H-SiC | 间接 | 3.26 | a=3.073, c=10.053 |
| 磷化铟 | InP | 直接 | 1.34 | 5.869 |
| 氧化镓(β) | β-Ga₂O₃ | 间接 | 4.8~4.9 | - |
| 金刚石 | Diamond | 间接 | 5.47 | 3.567 |

### 1.2 E_g 温度依赖性 (Varshni公式)

```
E_g(T) = E_g(0) - αT²/(T + β)
```

硅: E_g(0)=1.17eV, α=4.73×10⁻⁴, β=636
GaAs: E_g(0)=1.52eV, α=5.41×10⁻⁴, β=204
GaN: E_g(0)=3.47eV, α=7.7×10⁻⁴, β=600

## 2. 载流子统计

### 2.1 本征载流子浓度

```
n_i = sqrt(N_c·N_v) · exp(-E_g / 2kT)
```

硅 300K: n_i ≈ 1.0×10¹⁰ cm⁻³
GaAs 300K: n_i ≈ 2.1×10⁶ cm⁻³
4H-SiC 300K: n_i ≈ 6.7×10⁻¹¹ cm⁻³ (极低!)

### 2.2 有效态密度

硅 300K: N_c ≈ 2.8×10¹⁹ cm⁻³, N_v ≈ 1.04×10¹⁹ cm⁻³
GaAs 300K: N_c ≈ 4.7×10¹⁷ cm⁻³, N_v ≈ 7.0×10¹⁸ cm⁻³

### 2.3 费米能级

n型: E_F - E_i = kT·ln(N_d/n_i)
p型: E_i - E_F = kT·ln(N_a/n_i)

简并判定: N_d > N_c 或 N_a > N_v 时进入简并

## 3. 载流子输运

### 3.1 迁移率经验模型 (硅 300K)

电子迁移率:
```
μ_n(N) = μ_min + (μ_max - μ_min) / [1 + (N/N_ref)^α]
```
μ_max ≈ 1360 cm²/V·s, μ_min ≈ 92 cm²/V·s, N_ref = 1.3×10¹⁷, α = 0.91

空穴迁移率:
μ_max ≈ 495 cm²/V·s, μ_min ≈ 48 cm²/V·s, N_ref = 6.3×10¹⁶, α = 0.76

### 3.2 电阻率

```
ρ = 1 / (q·n·μ_n + q·p·μ_p) ≈ 1/(q·N·μ)  (单掺杂)
```

典型值: n-type Si @ 1×10¹⁵ cm⁻³ → ρ ≈ 4.6 Ω·cm

### 3.3 饱和速度

Si 电子: v_sat ≈ 1.0×10⁷ cm/s
Si 空穴: v_sat ≈ 0.7×10⁷ cm/s
GaN 电子: v_sat ≈ 2.5×10⁷ cm/s

## 4. pn结

### 4.1 内建电势

```
V_bi = (kT/q)·ln(N_a·N_d / n_i²)
```

### 4.2 耗尽层宽度

```
W_dep = sqrt[2ε_si·(V_bi - V_a)·(1/N_a + 1/N_d) / q]
```

### 4.3 结电容

```
C_j = ε_si·A / W_dep = C_j0 / sqrt(1 - V_a/V_bi)^m
```
突变结 m=1/2，线性缓变结 m=1/3

### 4.4 击穿电压

```
V_BD ∝ N^(-3/4)  (突变pn结)
```

简单估算: V_BD ≈ 60·(E_g/1.1)^(3/2) · (N_B/10¹⁶)^(-3/4)

## 5. MOSFET基础

### 5.1 阈值电压

```
V_th = V_FB + 2φ_F + sqrt(2ε_s·q·N_sub·|2φ_F|)/C_ox

V_FB = φ_ms - Q_ox/C_ox
φ_F = (kT/q)·ln(N_sub/n_i)
C_ox = ε_ox / t_ox
```

SiO₂: ε_ox = 3.9ε₀
High-k (HfO₂): ε_ox ≈ 25ε₀

### 5.2 漏极电流 (长沟道)

线性区: I_D = μ·C_ox·(W/L)·[(V_GS-V_th)·V_DS - V_DS²/2]
饱和区: I_D,sat = (μ·C_ox/2)·(W/L)·(V_GS-V_th)²·(1+λ·V_DS)

### 5.3 亚阈值摆幅

```
SS = (kT/q)·ln(10)·(1 + C_dep/C_ox)
```

室温理论极限: SS ≈ 60 mV/dec

### 5.4 短沟道效应

- **DIBL** (Drain-Induced Barrier Lowering): ΔV_th = -η·V_DS
- **速度饱和**: I_D,sat,short = W·C_ox·(V_GS-V_th)·v_sat
- **沟道长度调制**: λ ∝ 1/L
- **GIDL** (Gate-Induced Drain Leakage): 栅/漏重叠区高场带间隧穿
- **Narrow Width Effect**: 窄沟道引起V_th增加
- **Reverse Short Channel Effect**: 源/漏注入导致反常V_th变化

## 6. 失效物理机制

### 6.1 栅氧完整性 (GOI/TDDB)

- **E模型**: ln(t_BD) ∝ γ·E_ox
- **1/E模型**: ln(t_BD) ∝ G/E_ox (Anode Hole Injection)
- **Power-law**: t_BD ∝ V^(-n), n≈38~44 for SiO₂
- 典型SiO₂击穿场强: 10~15 MV/cm
- 工作寿命要求: 10年 @ V_cc_max, T=125°C

### 6.2 热载流子注入 (HCI)

- 最坏条件: V_GS ≈ V_DS/2 (峰值衬底电流)
- NMOS HCI > PMOS HCI (电子迁移率高)
- 退化表现: V_th升高, g_m降低, I_DSAT退化

### 6.3 NBTI (Negative Bias Temperature Instability)

- 主要影响PMOS
- 应力条件: V_GS < 0 (强反型), T=125°C
- 机制: Si-H键断裂，界面态生成
- 恢复效应: 移除应力后部分恢复
- 表现: |V_th|升高, 老化加速

### 6.4 电迁移 (EM)

```
MTTF = A·J^(-n)·exp(E_a/kT)
```
Cu: E_a ≈ 0.9~1.0 eV, n ≈ 1~2
Al: E_a ≈ 0.5~0.6 eV

### 6.5 ESD保护

- **HBM** (人体模型): 100pF + 1.5kΩ, typical 2kV
- **CDM** (充电器件模型): 器件自身充放电, <1ns
- **MM** (机器模型): 200pF + 0Ω
- ESD窗口: V_HBM > V_operating + margin, V_trigger < V_oxide_BD

### 6.6 闩锁效应 (Latch-up)

- 寄生PNPN SCR结构触发
- 触发条件: I/O过冲 > V_DD+0.7V 或 下冲 < V_SS-0.7V
- 防护: 保护环(guard ring)、增加阱/sub接触间距、SOI工艺免疫

## 7. 常用物理常数

| 常数 | 符号 | 值 |
|------|------|-----|
| 电子电荷 | q | 1.602×10⁻¹⁹ C |
| 玻尔兹曼常数 | k | 1.381×10⁻²³ J/K |
| 热电压 (300K) | kT/q | 0.02585 V |
| 真空介电常数 | ε₀ | 8.854×10⁻¹⁴ F/cm |
| 硅介电常数 | ε_si | 11.7ε₀ |
| SiO₂介电常数 | ε_ox | 3.9ε₀ |
| 普朗克常数 | h | 6.626×10⁻³⁴ J·s |
| 电子质量 | m₀ | 9.109×10⁻³¹ kg |
