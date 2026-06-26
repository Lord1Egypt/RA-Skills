# 射频工程 (RF Engineering)

> 射频电路设计、无线传播、测试测量与法规认证的工程参考。

---

## 1. 电磁波与传播

### 理论

**Maxwell 方程组（简化形式）：**

| 方程 | 表达式 |
|------|--------|
| Faraday 定律 | ∇×E = -∂B/∂t |
| Ampère 定律 | ∇×H = J + ∂D/∂t |
| Gauss 电场 | ∇·D = ρ |
| Gauss 磁场 | ∇·B = 0 |

**自由空间传播损耗（Friis 公式）：**

$$P_{rx} = P_{tx} + G_{tx} + G_{rx} - L_{fs}$$

$$L_{fs} (dB) = 20\log_{10}(d) + 20\log_{10}(f) + 32.44 \quad (d \text{ in km}, f \text{ in MHz})$$

或国际单位制：

$$L_{fs} (dB) = 20\log_{10}\left(\frac{4\pi d}{\lambda}\right)$$

**多径衰落模型：**

| 模型 | 适用场景 | PDF |
|------|----------|-----|
| Rayleigh | NLOS，多径丰富无直射 | $p(r) = \frac{r}{\sigma^2} e^{-r^2/(2\sigma^2)}$ |
| Rician | LOS 为主 + 多径 | $p(r) = \frac{r}{\sigma^2} e^{-(r^2+A^2)/(2\sigma^2)} I_0\!\left(\frac{Ar}{\sigma^2}\right)$，K因子=A²/(2σ²) |
| Nakagami-m | 通用拟合，m≥0.5 | 参数化控制衰落深度 |

**大尺度衰落（路径损耗模型）：**

- **Okumura-Hata**（150-1500MHz，1-20km）:
  $L_u = 69.55 + 26.16\log f - 13.82\log h_b - a(h_m) + (44.9-6.55\log h_b)\log d$
  - 中小城市: $a(h_m) = (1.1\log f - 0.7)h_m - (1.56\log f - 0.8)$
- **COST-231 Hata**（扩展至 2GHz）: 在 Hata 基础上 + $C_m$（城市 3dB）

**小尺度衰落：**
- 多普勒扩展: $f_d = v f_c / c$，相干时间 $T_c \approx 0.423/f_d$
- 时延扩展: 功率延迟分布 PDP 的 RMS 值 $\sigma_\tau$，相干带宽 $B_c \approx 1/(5\sigma_\tau)$
- 平坦衰落 vs 频率选择性衰落: 信号带宽 $B_s$ vs $B_c$

**穿透损耗（典型值）：**

| 材料 | 损耗 (dB) @ 1GHz |
|------|-------------------|
| 玻璃窗 | 2-3 |
| 木门 | 3-5 |
| 砖墙 (12cm) | 6-10 |
| 混凝土墙 (20cm) | 15-25 |
| 金属板/电梯 | 20-40 |

**绕射损耗:** 刃形绕射近似 $J(v)$，$v = h\sqrt{2(d_1+d_2)/(\lambda d_1 d_2)}$

### 方法

- 链路预算分析: $P_{rx} = P_{tx} + G_{tx} + G_{rx} - L_{path} - L_{misc} - M_{fade}$
- 阴影衰落余量: 对数正态分布，标准差 6-10dB（室外），8-12dB（室内）
- 多径建模: 信道冲激响应 $h(t,\tau) = \sum_i a_i e^{j\theta_i} \delta(t - \tau_i)$
- Rayleigh/Rician 仿真: Clarke/Jakes 模型

### 工具

- 传播预测: ITM (Irregular Terrain Model)、Free space path loss calculator
- 信道仿真: MATLAB Communications Toolbox、Python `scipy.stats`（Rayleigh/Rician）
- 3D 射线追踪: Remcom Wireless InSite、AWR AXIEM
- 简易计算: $L_{fs} = 32.44 + 20\log_{10}(f_{MHz}) + 20\log_{10}(d_{km})$

### 标准

- ITU-R P.1411: 短距离室外传播
- ITU-R P.2040: 建筑材料穿透损耗
- ITU-R P.526: 绕射传播
- 3GPP TR 36.873: 信道模型

### 应用

- Sub-GHz IoT 链路预算（LoRa: +14dBm, 433MHz, 10km）
- Wi-Fi 室内覆盖规划（AP 部署间距、穿墙余量）
- 5G NR 覆盖与容量仿真
- 室内分布系统（DAS）设计

---

## 2. 射频电路基础

### 理论

**功率单位换算：**

$$P_{dBm} = 10\log_{10}(P_{mW})$$
$$P_{dB\mu V} = P_{dBm} + 107 \quad (\text{在 50Ω 系统中})$$
$$P_{dBu} = P_{dBm} + 107 - 20\log_{10}(f_{MHz})$$

| dBm | mW | μV (50Ω) |
|-----|-----|-----------|
| +30 | 1000 | — |
| +20 | 100 | 2.24V |
| +10 | 10 | 707mV |
| 0 | 1 | 224mV |
| -10 | 0.1 | 70.7mV |
| -30 | 0.001 | 7.07mV |
| -60 | 1μW | 224μV |
| -100 | 0.1nW | 2.24μV |
| -120 | 1pW | 0.224μV |

**阻抗匹配（L型网络）：**

给定负载 $Z_L = R_L + jX_L$ 匹配到 $Z_0 = R_0$：

$L$型（低通）: 串联电感 + 并联电容
$L$型（高通）: 串联电容 + 并联电感
$\pi$型: 两个并联支路 + 一个串联支路（Q值更高，带宽更窄）
$T$型: 两个串联支路 + 一个并联支路

Smith 圆图: 等电阻圆 + 等电抗圆，Q值圆，等 VSWR 圈

**S 参数：**

$$
\begin{bmatrix} b_1 \\ b_2 \end{bmatrix} = \begin{bmatrix} S_{11} & S_{12} \\ S_{21} & S_{22} \end{bmatrix} \begin{bmatrix} a_1 \\ a_2 \end{bmatrix}
$$

- $S_{11}$: 端口1反射系数（回波损耗 $RL = -20\log|S_{11}|$ dB）
- $S_{21}$: 正向传输（插入增益/损耗）
- $S_{12}$: 反向传输（隔离度）
- $S_{22}$: 端口2反射系数

**稳定性判据：**

Rollett 稳定条件（无条件稳定）:
$$K = \frac{1 - |S_{11}|^2 - |S_{22}|^2 + |\Delta|^2}{2|S_{12}S_{21}|} > 1$$
$$|\Delta| = |S_{11}S_{22} - S_{12}S_{21}| < 1$$

**噪声：**

$$NF (dB) = 10\log_{10}(F), \quad F = \frac{SNR_{in}}{SNR_{out}}$$

级联噪声系数（Friis 公式）:
$$F_{total} = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1 G_2} + \cdots$$

噪声温度: $T_e = T_0(F - 1)$，其中 $T_0 = 290K$

**线性度：**

- 1dB 压缩点 (P1dB): 增益下降 1dB 时的输入/输出功率
- 三阶交调 (IMD3): $f_1, f_2 \rightarrow 2f_1 - f_2, 2f_2 - f_1$
- IIP3/OIP3: $OIP3 \approx P_{out} + \frac{\Delta P}{2}$（其中 $\Delta P$ 为基波与 IMD3 的功率差）
- SFDR (无杂散动态范围): $SFDR \approx \frac{2}{3}(IIP3 - N_{floor})$

### 方法

- 阻抗匹配设计: Smith Chart 图解法 → 解析公式验证 → 仿真优化
- 稳定性设计: 在输入/输出端加电阻/铁氧体 bead
- 增益/噪声优化: 同时匹配法 vs 单向化法，LNA 用噪声圆匹配
- 线性度改善: 输出功率回退 10dB → IMD3 改善约 20dB
- 交调分析: 双音测试 → 频谱仪读基波与三阶产物功率差

### 工具

- Smith Chart: 免费 online 工具、Keysight ADS Smith Chart Utility
- 电路仿真: Keysight ADS / PathWave、AWR Microwave Office、Ansys HFSS
- 开源: Qucs、GNU Radio + PyRF
- Python: `scikit-rf`（S 参数处理、Smith Chart 绘制）

### 标准

- IEEE 145-1983: VSWR 定义
- IEC 61300-3-4: 光纤器件回波损耗测量

### 应用

- LNA 输入匹配（噪声最优 vs 功率最优折中）
- PA 输出匹配（效率 vs 线性度折中，Doherty/ET 架构）
- 滤波器/天线端口匹配调试
- 接收机链路 NF 分配与 IIP3 预算

---

## 3. 射频组件

### 理论

#### 滤波器

| 类型 | 频率范围 | 特点 |
|------|----------|------|
| LC | DC-3GHz | 低成本、Q值受限 |
| Balun（平衡-不平衡转换） | — | 同时实现不平衡→平衡+滤波 |
| SAW | 50MHz-3GHz | 体积小、插入损耗 1-3dB |
| BAW (FBAR) | 1-7GHz | 高Q、温度稳定性好、成本高 |
| 腔体 | 300MHz-40GHz | 低损耗、高功率、体积大 |
| 陶瓷 | 100MHz-10GHz | 中等Q、成本低 |

滤波器响应: Butterworth（最平坦）、Chebyshev（等纹波）、Elliptic（最陡峭）、Bessel（线性相位）

#### 放大器

- **LNA**: 最低噪声优先，$NF_{min}$、$G_{max}$、IIP3、OIP1dB
- **PA**: 效率（PAE = $(P_{out}-P_{in})/P_{DC}$）与线性度权衡
  - Class A: 50% 理论效率，最线性
  - Class AB: 60-78%，常用于手持设备
  - Class D/E/F: >80%，开关型，需谐波滤波
  - Doherty: 宽范围效率提升
- **VGA**: 增益可调范围 20-60dB，步进 0.5-2dB

#### 混频器

- 上下变频: $f_{IF} = |f_{RF} \pm f_{LO}|$
- 镜像抑制混频器 (IRM): I/Q 两路混频 + 90° 移相，抑制镜像 20-35dB
- 关键指标: 变频损耗/增益、隔离度、LO-RF 泄漏、IIP3

#### 振荡器与 PLL

| 类型 | 稳定度 | 温漂 | 应用 |
|------|--------|------|------|
| XO (晶振) | ±50ppm | ±30ppm | 时钟源 |
| VCXO | ±50ppm | ±30ppm | 压控调谐 |
| TCXO | ±0.5ppm | ±0.5ppm | GPS/蜂窝 |
| OCXO | ±0.01ppm | ±0.001ppm | 基站/仪表 |

**PLL（锁相环）:**
- 环路带宽: 相位噪声低频段跟随 VCO，高频段跟随参考源
- 相位噪声: $L(f) = S_\phi(f)/2$，单位 dBc/Hz
- 整数分频: 信道步进 = 参考频率 $f_{ref}$
- 小数分频: $\Sigma-\Delta$ 调制，细步进但引入分数杂散

#### 开关

- PIN 二极管: 高功率（1-100W），切换速度 10-100ns
- GaAs FET: 低功耗，切换速度 1-10ns
- SOI/CMOS: 低压集成，趋势方向

#### 天线

| 类型 | 增益 | 特点 |
|------|------|------|
| 偶极子 (Dipole) | 2.15dBi | 全向、基础参考 |
| 单极子 (Monopole) | 5.16dBi | 地面反射增益 |
| 贴片 (Patch) | 6-9dBi | 低轮廓、易集成 |
| 八木 (Yagi) | 10-15dBi | 定向、电视/基站 |
| 对数周期 | 8-12dBi | 宽带定向 |
| 螺旋 (Helical) | 12-15dBi | 圆极化 |
| PIFA | 3-6dBi | 手机内置天线 |
| IFA | 2-5dBi | 小型化 |

#### 功率分配/合成

- Wilkinson 功分器: 等分/不等分，隔离度 >20dB，1/4λ 变换线 + 100Ω 电阻
- Lange 耦合器: 宽带 90° 耦合，3dB 耦合比

### 方法

- 滤波器设计: 查表归一化低通原型 → 频率变换 → 元件值计算 → 仿真优化
- LNA 设计: 噪声圆 + 稳定圆 → 选最佳反射系数 → 匹配网络
- PA 设计: 负载牵引 (Load-Pull) → 等功率/等效率圆 → 输出匹配
- PLL 设计: 环路滤波器参数计算（相位裕度 45-60°）
- 天线仿真: 数值方法（MoM/FEM/FDTD）

### 工具

- 滤波器设计: Nuhertz Filter Solutions、AADE Filter Design（免费）
- PLL 设计: ADIsimPLL（免费）、PLLatinum Sim
- 天线仿真: CST Microwave Studio、HFSS、4NEC2（免费）
- 射频前端仿真: Keysight Genesys、AWR Microwave Office

### 标准

- MIL-STD-188-124B: 天线标准
- ETSI EN 300 328: 2.4GHz 设备
- IEEE 802.15.4: Sub-GHz/WiFi/BLE 物理层

### 应用

- Sub-GHz 无线模块前端（SAW + LNA + PA + Switch）
- Wi-Fi 6E 前端模块 (FEM)
- 5G NR n77/n78/n79 滤波器组
- 汽车雷达 77GHz 天线阵列

---

## 4. PCB 射频设计

### 理论

**阻抗控制（微带线 Microstrip）：**

$$Z_0 \approx \frac{87}{\sqrt{\varepsilon_r + 1.41}} \ln\left(\frac{5.98h}{0.8w + t}\right)$$

- $h$: 介质厚度, $w$: 走线宽度, $t$: 铜厚, $\varepsilon_r$: 介电常数
- 有效介电常数: $\varepsilon_{eff} \approx \frac{\varepsilon_r + 1}{2} + \frac{\varepsilon_r - 1}{2}\frac{1}{\sqrt{1 + 12h/w}}$

**带状线 (Stripline):**

$$Z_0 \approx \frac{60}{\sqrt{\varepsilon_r}} \ln\left(\frac{4b}{\pi(0.67w + t)}\right) \quad \text{(对称)}$$

**共面波导 (CPW):**

中心导带 + 两侧地平面，适合高密度集成，减少过孔寄生。

**常用介质材料：**

| 材料 | εr | tanδ | 应用 |
|------|-----|------|------|
| FR-4 | 4.3-4.8 | 0.02 | 低成本、<3GHz |
| Rogers RO4350B | 3.48 | 0.0037 | 微波、高可靠性 |
| Rogers RO3003 | 3.0 | 0.0013 | mmWave |
| Rogers RT/duroid 5880 | 2.2 | 0.0009 | 最低损耗 |

### 方法

- 层叠设计: 
  - 4层: Top(RF信号) / GND / PWR / Bottom(控制信号)
  - 6层: Top(RF) / GND1 / Inner1(数字) / Inner2(数字) / GND2 / Bottom(电源)
  - 关键: 射频走线下方完整地平面，层间距离对称
- 接地: 射频区完整地铜皮，过孔间距 ≤ λ/20，分割地用桥接电容
- 隔离: 射频区与数字区物理分隔，电源滤波（π型 LC），金属屏蔽罩
- 过孔: 射频过孔寄生电感 ~0.5nH，背钻减少 stub

### 工具

- 阻抗计算: Saturn PCB Toolkit（免费）、KiCad 内置计算器、Polar Si9000
- PCB 设计: Altium Designer、KiCad、Cadence Allegro
- SI 仿真: HyperLynx、ADS Momentum、CST
- 有限元: HFSS、CST Microwave Studio

### 标准

- IPC-2141A: 高速/高频 PCB 设计
- IPC-6012: 刚性 PCB 规范
- IEC 61188-5: PCB 设计信号完整性

### 应用

- 2.4GHz/5GHz Wi-Fi 模块 PCB 布局
- Sub-GHz 收发器射频前端
- 汽车雷达 77GHz 层叠设计
- 射频开关矩阵板

---

## 5. 测试测量

### 理论

**频谱分析仪关键参数：**
- RBW (分辨率带宽): 越小频率分辨率越高，扫描时间越长。RBW 缩小 10 倍 → 噪底降低 10dB
- VBW (视频带宽): 平滑噪声起伏，VBW < RBW 时平均效果明显
- 检波器模式: Peak（峰值）、Average（均值）、RMS、Quasi-peak（EMC 用）
- DANL (显示平均噪声电平): 本底噪声，典型 -150~-165dBm/Hz
- 相位噪声: 偏移载波 f 处的噪声功率密度

**矢量网络分析仪 (VNA)：**
- 测量 S 参数全矩阵（S11/S21/S12/S22）
- 时域反射 (TDR): 通过 IFFT 将频域 S11 转为时域阻抗分布
- 校准: SOL（Short-Open-Load）、TRL（Thru-Reflect-Line）

**信号发生器:**
- CW（连续波）、AM/FM/PM 调制、I/Q 矢量调制
- 扫频、功率扫描

### 方法

- 回波损耗测量: VNA → 校准 → 测 S11 → 检查 < -10dB（VSWR < 2:1）
- 插入损耗测量: VNA → 测 S21 → 2-port thru 校准
- 增益压缩: 信号源 + 频谱仪 → 功率扫描 → 找 -1dB 点
- IMD3 测量: 双音信号 → 频谱仪读基波与 3 阶交调产物
- 相位噪声: 频谱仪相位噪声模式或专用相位噪声分析仪
- 近场 EMI 排查: 近场探头 + 频谱仪 → 定位干扰源（时钟谐波、电源纹波）
- OTA 测试: 暗室 + 标准天线 → 测 TRP/TIS/EIRP

### 工具

- 频谱仪: Keysight N9030B (PXAI)、R&S FSW、Tektronix RSA 系列
- VNA: Keysight PNA 系列、R&S ZNB、Copper Mountain
- 信号源: Keysight E8257D、R&S SMA100B
- 近场探头: Beehive、Langer EMV、Com-Power
- 功率计: Keysight N1914A（热电偶/二极管检波）
- 免费工具: Python + pyrtlsdr (SDR)、GNU Radio

### 标准

- CISPR 16-1-1: EMC 测量接收机规范
- ANSI C63.4: 美国 EMC 测量方法
- 3GPP TS 38.521: 5G NR UE 射频测试

### 应用

- 天线端口 VSWR 调试
- 接收机灵敏度与动态范围测试
- EMI 预认证排查
- 产线射频校准

---

## 6. 法规认证

### 理论

**主要认证体系：**

| 认证 | 地区 | 频段 | 关键限值 |
|------|------|------|----------|
| FCC Part 15 | 美国 | ISM/Unlicensed | EIRP ≤ 36dBm (5.8GHz), ≤ 30dBm (2.4GHz) |
| FCC Part 22/24/27 | 美国 | 蜂窝 | SAR ≤ 1.6W/kg |
| CE/RED | 欧洲 | 全频段 | ETSI EN 标准 |
| SRRC | 中国 | 全频段 | 需核准，功率/频谱/杂散限值 |
| MIC | 日本 | 全频段 | 电波法 |
| IC | 加拿大 | 类似 FCC | RSS 标准 |
| SAR | 全球 | 蜂窝/手机 | 1.6W/kg(美)/2.0W/kg(欧) |

**SAR (比吸收率):**
$$SAR = \frac{\sigma |E|^2}{\rho} = \frac{C \Delta T}{\Delta t}$$
- 美国 FCC: ≤ 1.6W/kg (1g 均方)
- 欧洲 EN: ≤ 2.0W/kg (10g 均方)

**EMC 发射限值（CISPR 32 / FCC Part 15）：**
- 辐射发射: 30MHz-1GHz，准峰值检波
- 传导发射: 150kHz-30MHz，LISN 测量
- 谐波发射: IEC 61000-3-2
- 闪烁: IEC 61000-3-3

### 方法

- 预认证测试: 3m 半电波暗室（预扫）→ GTEM cell → 近场探排查
- EMC 整改: 屏蔽、滤波、接地、布局优化
- SAR 仿真: SEMCAD X、Sim4Life（头部/身体模型）
- 认证流程: 样机 → 预测试 → 整改 → 正式测试 → 报告 → 获证

### 工具

- EMC 暗室: 3m/10m 半电波暗室 (SAC)
- GTEM cell: 小设备快速预测试
- LISN: 传导发射测量
- SAR 测试系统: DASY（SPEAG）
- 仿真: CST Studio Suite（EMC + SAR）

### 标准

- FCC Part 15.247: 跳频/DSSS 2.4GHz
- FCC Part 15.249: 2.4GHz 通用
- FCC Part 15.209: 杂散发射限值
- ETSI EN 300 328: 2.4GHz
- ETSI EN 301 893: 5GHz
- ETSI EN 300 220: Sub-GHz
- YD/T 1484-2006 (SRRC): 中国无线电设备

### 应用

- Sub-GHz 模块 SRRC 核准
- Wi-Fi 产品 FCC/CE 认证
- 5G 手机 SAR 测试
- 车载电子产品 EMC 认证

---

## 7. 常用频段

### 理论

| 频段 | 范围 | 波长 | 应用 |
|------|------|------|------|
| VLF | 3-30kHz | 100-10km | 潜艇通信、导航 |
| LF | 30-300kHz | 10-1km | 长波广播、时钟同步 |
| HF | 3-30MHz | 100-10m | 短波广播、业余无线电 |
| VHF | 30-300MHz | 10-1m | FM 广播、对讲机 |
| UHF | 300-3000MHz | 1m-10cm | 电视、蜂窝 |
| SHF | 3-30GHz | 10-1cm | 卫星、5G、雷达 |
| EHF (mmWave) | 30-300GHz | 10-1mm | 5G FR2、汽车雷达 |

**ISM 频段：**

| 频段 | 区域 | 功率限制 | 典型应用 |
|------|------|----------|----------|
| 315MHz | 中国/日本 | 10mW (EIRP) | 遥控、汽车钥匙 |
| 433MHz | 欧洲/中国 | 10mW | LoRa、智能家居 |
| 470-510MHz | 中国 | 10-50mW | 智能电表 |
| 868MHz | 欧洲 | 10-25mW | LoRaWAN、Sigfox |
| 915MHz | 美洲 | 30mW (FCC) | LoRa、ZigBee |
| 2.4GHz | 全球 | 100mW (EIRP) | Wi-Fi、BLE、ZigBee |
| 5.15-5.825GHz | 全球 | 200-1000mW | Wi-Fi 5/6/7 |
| 24GHz | 全球 | — | ISM/雷达 |
| 60GHz | 全球 | — | WiGig |
| 77GHz | 全球 | — | 汽车雷达 |

**蜂窝频段：**

| 频段 | 范围 | 制式 |
|------|------|------|
| n28 | 700MHz | 5G |
| B5/B8 | 850/900MHz | 4G |
| B1/B3 | 2100/1800MHz | 3G/4G |
| B7/B41 | 2.6GHz | 4G |
| n77/n78 | 3.3-4.2GHz | 5G |
| n79 | 4.4-5.0GHz | 5G (中国) |
| n257/n258 | 26-28GHz | 5G FR2 |

### 方法

- 频段选择: 覆盖距离 vs 数据速率 vs 穿透能力 权衡
- 干扰分析: 频谱仪扫描 → 同频/邻频干扰评估
- 信道规划: 蜂窝复用、Wi-Fi 信道分配（1/6/11）

### 工具

- 频谱管理: ITU 频率数据库
- 在线查询: 频谱地图、各国频率分配表
- SDR: HackRF/BladeRF/USRP → 实时频谱监测

### 标准

- ITU Radio Regulations: 全球频率分配
- 3GPP TS 36.101/38.101: LTE/NR UE 射频要求

### 应用

- IoT 设备频段选型（LoRa 433/868/915MHz）
- Wi-Fi 频道规划（2.4GHz 1/6/11，5GHz DFS 信道）
- 5G 基站部署频段选择
- 雷达频段分配（24GHz ISM → 77GHz automotive）

---

## 8. 常用公式速查

### 功率与电压

$$dBm = 10\log(P_{mW})$$
$$V_{rms} = \sqrt{P \times Z}$$
$$V_{rms}(dB\mu V) = P(dBm) + 107 \quad (Z=50\Omega)$$

### VSWR 与回波损耗

$$\Gamma = \frac{VSWR - 1}{VSWR + 1}$$
$$RL (dB) = -20\log|\Gamma|$$
$$VSWR = \frac{1 + |\Gamma|}{1 - |\Gamma|}$$

| VSWR | RL (dB) | |Γ| | 功率反射% |
|------|---------|-----|-----------|
| 1.0 | ∞ | 0 | 0% |
| 1.5 | -13.98 | 0.20 | 4% |
| 2.0 | -9.54 | 0.33 | 11% |
| 3.0 | -6.02 | 0.50 | 25% |

### 噪声

$$NF_{total} = NF_1 + \frac{NF_2-1}{G_1} + \frac{NF_3-1}{G_1 G_2}$$
$$SNR_{dB} = P_{sig,dBm} - (-174 + 10\log(B_{Hz}) + NF_{dB})$$

### 传播

$$L_{fs} (dB) = 32.44 + 20\log(f_{MHz}) + 20\log(d_{km})$$
$$\lambda (m) = \frac{300}{f_{MHz}}$$
