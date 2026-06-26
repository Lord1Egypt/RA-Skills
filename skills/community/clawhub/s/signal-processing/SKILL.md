# Signal Processing — 信号处理

> 通信工程专业研究生级别知识体系。每个子领域按 **理论 → 方法 → 工具 → 应用** 组织。

---

## 目录

1. [时域与频域分析](#1-时域与频域分析)
2. [数字滤波器](#2-数字滤波器)
3. [估计与检测](#3-估计与检测)
4. [多载波与扩频](#4-多载波与扩频)
5. [空时信号处理](#5-空时信号处理)
6. [通信中的信号处理](#6-通信中的信号处理)
7. [实际工程实现](#7-实际工程实现)

---

## 1. 时域与频域分析

### 1.1 信号分类与基本运算

**分类维度：** 时间（连续/离散）、幅度（连续/量化）、周期性、确定性/随机、能量/功率。

**基本信号：** $\delta(t), u(t), e^{j\omega_0 t}, \text{rect}(t/T), \text{sinc}(t)$

**能量与功率：**

$$E = \int_{-\infty}^{\infty}|x(t)|^2 dt, \quad P = \lim_{T\to\infty}\frac{1}{2T}\int_{-T}^{T}|x(t)|^2 dt$$

$$E_{dt} = \sum_{n=-\infty}^{\infty}|x[n]|^2, \quad P_{dt} = \lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}|x[n]|^2$$

### 1.2 LTI 系统分析

**理论：** LTI 系统由冲激响应 $h(t)$ 完全描述，$y(t) = (x*h)(t) = \int x(\tau)h(t-\tau)d\tau$。

因果性：$h(t)=0, \forall t<0$。BIBO 稳定：$\int|h(t)|dt<\infty$。

频率响应：$H(j\omega) = \int h(t)e^{-j\omega t}dt = |H(j\omega)|e^{j\angle H(j\omega)}$

群延迟：$\tau_g(\omega) = -\frac{d}{d\omega}\angle H(j\omega)$

**方法：** 卷积计算、传递函数分析、零极点分析。

**应用：** 系统级联/并联组合分析、反馈系统稳定性（Nyquist 判据）。

### 1.3 傅里叶分析

#### CTFS（连续时间傅里叶级数）

周期 $T_0$，$\Omega_0 = 2\pi/T_0$：

$$x(t) = \sum_{k=-\infty}^{\infty} a_k e^{jk\Omega_0 t}, \quad a_k = \frac{1}{T_0}\int_{T_0} x(t) e^{-jk\Omega_0 t} dt$$

Parseval：$\frac{1}{T_0}\int_{T_0}|x(t)|^2 dt = \sum_{k=-\infty}^{\infty}|a_k|^2$

#### CTFT（连续时间傅里叶变换）

$$X(j\Omega) = \int_{-\infty}^{\infty} x(t) e^{-j\Omega t} dt, \quad x(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty} X(j\Omega) e^{j\Omega t} d\Omega$$

**关键性质：** 时移→相移 $e^{-j\Omega t_0}$；频移→调制 $e^{j\Omega_0 t}$；卷积定理 $XH$；时域微分→$\j\Omega X$；尺度变换→$\frac{1}{|a|}X(\Omega/a)$。

#### DTFS & DTFT

DTFT（非周期序列）：$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$，以 $2\pi$ 为周期。

数字频率 $\omega$ 与模拟频率 $\Omega$ 的关系：$\omega = \Omega T_s = \Omega/f_s$。

#### DFT & FFT

$N$ 点 DFT：$X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\frac{2\pi}{N}kn}$，$W_N = e^{-j2\pi/N}$

圆周卷积定理：$\text{DFT}\{x \circledast_N y\} = X[k] \cdot Y[k]$

线性卷积用 DFT：补零到 $N \geq L_1 + L_2 - 1$。

**Cooley-Tukey 基-2 FFT：**

$$X[k] = \underbrace{\sum_{m=0}^{N/2-1} x[2m] W_N^{2mk}}_{\text{偶数项}} + W_N^k \underbrace{\sum_{m=0}^{N/2-1} x[2m+1] W_N^{2mk}}_{\text{奇数项}}$$

复杂度：$O(N\log_2 N)$。

```python
import numpy as np
X = np.fft.fft(x)                  # FFT
x_rec = np.fft.ifft(X)             # IFFT
# 长序列滤波：overlap-add
# 零填充提高频率插值分辨率（不增加真实分辨率）
```

### 1.4 时频分析

#### STFT

$$X(\tau, \omega) = \int_{-\infty}^{\infty} x(t) w(t-\tau) e^{-j\omega t} dt$$

Heisenberg 不确定性：$\Delta t \cdot \Delta \omega \geq 1/2$，短窗时间分辨率高，长窗频率分辨率高。

```python
import scipy.signal as signal
f, t, Zxx = signal.stft(x, fs=fs, window='hann', nperseg=1024, noverlap=768)
x_rec = signal.istft(Zxx, fs=fs, window='hann', nperseg=1024, noverlap=768)[0]
```

#### 小波变换 (WT)

**CWT：** $W_x(a,b) = \frac{1}{\sqrt{a}}\int x(t)\psi^*((t-b)/a)dt$，$a$ 为尺度，$b$ 为平移。

**DWT (Mallat 算法)：** 多分辨率分析，交替通过 LPF $h[n]$ 和 HPF $g[n]$ 并下采样。

```
x[n] → h[n] → ↓2 → cA1 (近似)
     → g[n] → ↓2 → cD1 (细节)
```

**常用母小波：** Haar（最简单）、Daubechies dbN（紧支撑正交）、Morlet（连续分析）、Symlet（近对称）。

```python
import pywt
coeffs = pywt.wavedec(x, 'db4', level=5)     # DWT 分解
# Donoho-Johnstone 阈值去噪
sigma = np.median(np.abs(coeffs[-1])) / 0.6745
thr = sigma * np.sqrt(2 * np.log(len(x)))
coeffs_d = [pywt.threshold(c, thr, mode='soft') for c in coeffs]
x_dn = pywt.waverec(coeffs_d, 'db4')
# CWT
cwtm, freqs = pywt.cwt(x, np.arange(1, 128), 'cmor1.5-1.0', sampling_period=1/fs)
```

### 1.5 z 变换与拉普拉斯变换

**z 变换：** $X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$，$z=re^{j\omega}$

关键性质：时移 $z^{-n_0}X(z)$、z 域尺度 $X(z/a)$、卷积 $X(z)H(z)$。

因果 ⟺ ROC 为圆外且含 $\infty$。稳定 ⟺ ROC 含单位圆。

**拉普拉斯变换：** $X(s) = \int x(t)e^{-st}dt$，$s=\sigma+j\Omega$。通过 $z=e^{sT_s}$ 与 z 变换关联。

部分分式展开求逆变换：$X(z) = \sum_i \frac{A_i}{1-p_iz^{-1}} \Rightarrow x[n] = \sum_i A_i p_i^n u[n]$

### 1.6 采样定理与量化

**Nyquist 采样定理：** $f_s \geq 2f_{\max}$，理想重建 $x(t) = \sum x[nT_s]\text{sinc}((t-nT_s)/T_s)$。

混叠：$f_s < 2f_{\max}$ 时频谱折叠。抗混叠滤波器截止于 $f_s/2$。

过采样好处：降低抗混叠滤波器阶数、提高 SQNR。

**量化噪声：** 均匀量化步长 $\Delta = V_{pp}/2^B$，$P_q = \Delta^2/12$。

$$\text{SQNR} \approx 6.02B + 1.76 \text{ dB}$$

$\Sigma\Delta$ 调制噪声整形：$\text{SQNR}_{\Sigma\Delta} \approx 6.02B + 1.76 + (2L+1)\cdot 10\log_{10}(OSR)$ dB（$L$ 阶）。

### 1.7 随机信号分析

**理论：** 自相关 $r_{xx}[m] = E\{x[n]x^*[n+m]\}$，PSD（Wiener-Khinchin）：$S_{xx}(e^{j\omega}) = \mathcal{F}\{r_{xx}[m]\}$

互相关 $r_{xy}[m]$，互谱 $S_{xy}(e^{j\omega})$，相干函数 $\gamma^2_{xy} = |S_{xy}|^2/(S_{xx}S_{yy})$。

白噪声：$r_{ww}[m]=\sigma_w^2\delta[m]$，$S_{ww}=\sigma_w^2$。有色噪声：白噪声通过 $H(z)$，$S_{xx}=\sigma_w^2|H|^2$。

**方法：** 周期图法估计 PSD，Welch 法（分段平均加窗）。

```python
# PSD 估计
f, Pxx = signal.welch(x, fs=fs, window='hann', nperseg=1024, noverlap=512)
```

### 1.8 维纳滤波与卡尔曼滤波

**维纳滤波：** Wiener-Hopf 方程 $\mathbf{R}\mathbf{w} = \mathbf{r}$，$\mathbf{w}_{opt} = \mathbf{R}^{-1}\mathbf{r}$。

频域最优滤波器：$H_{opt}(e^{j\omega}) = S_{dx}(e^{j\omega})/S_{xx}(e^{j\omega})$。

最小 MSE：$\xi_{min} = r_{dd}[0] - \mathbf{r}^H\mathbf{R}^{-1}\mathbf{r}$。

**卡尔曼滤波：** 状态空间模型

$$\mathbf{x}[n] = \mathbf{F}\mathbf{x}[n-1] + \mathbf{w}[n], \quad \mathbf{z}[n] = \mathbf{H}\mathbf{x}[n] + \mathbf{v}[n]$$

```
预测: x̂⁻ = F x̂, P⁻ = F P Fᵀ + Q
更新: K = P⁻ Hᵀ (H P⁻ Hᵀ + R)⁻¹
      x̂ = x̂⁻ + K (z - H x̂⁻)
      P = (I - K H) P⁻
```

**扩展：** EKF（Jacobian 线性化）、UKF（sigma 点，无需 Jacobian）。

**应用：** 目标跟踪、GPS 定位、通信信道跟踪、雷达信号处理。

---

## 2. 数字滤波器

### 2.1 FIR 滤波器设计

**理论：** $H(z) = \sum_{n=0}^{M} h[n]z^{-n}$。线性相位条件 $h[n] = \pm h[M-n]$，群延迟 $\tau = M/2$。

四种线性相位：I 型（偶对称奇数长）、II 型（偶对称偶数长）、III 型（奇对称奇数长）、IV 型（奇对称偶数长）。

#### 窗函数法

$$h[n] = h_d[n] \cdot w[n], \quad h_d[n] = \frac{\sin(\omega_c(n-M/2))}{\pi(n-M/2)}$$

| 窗 | 主瓣宽 | 旁瓣 | 阻带衰减 |
|----|--------|------|----------|
| Rectangular | $4\pi/N$ | -13 dB | -21 dB |
| Hamming | $8\pi/N$ | -41 dB | -53 dB |
| Blackman | $12\pi/N$ | -57 dB | -74 dB |
| Kaiser ($\beta$) | 可调 | 可调 | 可调 |

#### Parks-McClellan (Remez)

等波纹 Chebyshev 最优逼近：$\min_h \max_\omega |W(\omega)[H_d - H]|$。

#### 其他方法

频率采样法（指定 $H_d[k]$，IDFT）、最小二乘法（$L_2$ 最优）。

```python
import scipy.signal as signal

# 窗函数法
h = signal.firwin(101, 12000, window='hamming', fs=48000)

# Kaiser 窗
N, beta = signal.kaiserord(60, 1000/(48000/2))
h = signal.firwin(N, 12000, window=('kaiser', beta), fs=48000)

# Remez 算法
h = signal.remez(101, [0, 12000, 13000, 24000], [1, 0], fs=48000)

# 最小二乘
h = signal.firls(101, [0, 12000, 13000, 24000], [1, 1, 0, 0], fs=48000)
```

### 2.2 IIR 滤波器设计

**理论：** $H(z) = B(z)/A(z)$。低阶实现高选择度，但非线性和潜在不稳定。

**模拟原型：** Butterworth（最大平坦 $|H|^2 = 1/(1+(\Omega/\Omega_c)^{2N})$）、Chebyshev I（通带等波纹）、Chebyshev II（阻带等波纹）、Elliptic（通带+阻带等波纹，过渡带最窄）。

#### 双线性变换

$$s = \frac{2}{T_s}\frac{1-z^{-1}}{1+z^{-1}}, \quad \Omega = \frac{2}{T_s}\tan\frac{\omega}{2}$$

频率预畸变：$\omega_c \to \Omega_c = \frac{2}{T_s}\tan(\omega_c/2)$。无混叠但频率轴非线性。

#### 脉冲响应不变法

$h[n] = T_s h_a(nT_s)$，保持时域形状但有频率混叠，仅适合低通/带通。

```python
b, a = signal.butter(6, 8000, fs=48000)         # Butterworth
b, a = signal.cheby1(6, 0.5, 8000, fs=48000)     # Chebyshev I
b, a = signal.ellip(6, 0.5, 60, 8000, fs=48000)  # Elliptic
z, p, k = signal.tf2zpk(b, a)                    # 零极点分析
```

### 2.3 滤波器结构

**FIR 结构：** 直接型、线性相位（利用对称性减半乘法）、级联型（二阶节级联）、频率采样型。

**IIR 结构：**

- **直接 I 型：** FIR + 反馈分开
- **直接 II 型（典范型）：** 合并延迟线，最少存储 $N$ 个
- **级联型：** $H(z) = k \prod_i (b_{0i}+b_{1i}z^{-1}+b_{2i}z^{-2})/(1+a_{1i}z^{-1}+a_{2i}z^{-2})$
- **并联型：** 部分分式展开，各节并联

**格型结构 (Lattice)：** 反射系数 $k_m$ 参数化，数值稳定性好，广泛用于预测编码和自适应滤波。

$$f_m[n] = f_{m-1}[n] + k_m b_{m-1}[n-1], \quad b_m[n] = k_m f_{m-1}[n] + b_{m-1}[n-1]$$

### 2.4 多采样率处理

#### 抽取 (Decimation)

降低采样率：$y[m] = x[mD]$，$D$ 为抽取因子。

需先低通滤波（截止 $f_s/(2D)$）防混叠。频谱展宽 $D$ 倍。

#### 插值 (Interpolation)

提高采样率：$y[m] = \sum_k x[k] h_I[m - kI]$，$I$ 为插值因子。

先零值上采样再滤波（抗镜像滤波器）。

#### 多相分解

$$H(z) = \sum_{l=0}^{D-1} z^{-l} E_l(z^D), \quad E_l(z) = \sum_n h[nD+l] z^{-n}$$

将滤波器分解为 $D$ 个子滤波器，计算量降低约 $1/D$。

#### 滤波器组

**分析滤波器组：** $H_k(z)$，将信号分解为子带。
**综合滤波器组：** $G_k(z)$，重建信号。

**正交镜像滤波器组 (QMF)：** $H_1(z) = H_0(-z)$，设计条件 $|H_0(e^{j\omega})|^2 + |H_1(e^{j\omega})|^2 = 1$。

**应用：** 子带编码、音频压缩（MP3/AAC 的 MDCT）、图像压缩（JPEG2000 小波）、软件无线电。

### 2.5 自适应滤波

**理论：** 滤波器系数随输入信号统计特性自动调整。

#### LMS (Least Mean Squares)

$$\mathbf{w}[n+1] = \mathbf{w}[n] + \mu e[n] \mathbf{x}[n], \quad e[n] = d[n] - \mathbf{w}^T[n]\mathbf{x}[n]$$

收敛条件：$0 < \mu < 2/(\lambda_{max}) = 2/(\text{tr}(\mathbf{R}))$

失调 (misadjustment)：$\mathcal{M} = \mu \cdot \text{tr}(\mathbf{R})/2$

#### NLMS (Normalized LMS)

$$\mathbf{w}[n+1] = \mathbf{w}[n] + \frac{\mu}{\epsilon + \|\mathbf{x}[n]\|^2} e[n] \mathbf{x}[n]$$

自动归一化步长，收敛更稳健。

#### RLS (Recursive Least Squares)

$$\mathbf{k}[n] = \frac{\mathbf{P}[n-1]\mathbf{x}[n]}{\lambda + \mathbf{x}^T[n]\mathbf{P}[n-1]\mathbf{x}[n]}$$
$$\mathbf{w}[n] = \mathbf{w}[n-1] + \mathbf{k}[n] e[n]$$
$$\mathbf{P}[n] = \frac{1}{\lambda}(\mathbf{P}[n-1] - \mathbf{k}[n]\mathbf{x}^T[n]\mathbf{P}[n-1])$$

复杂度 $O(N^2)$（vs LMS $O(N)$），但收敛快一个数量级。遗忘因子 $\lambda \approx 0.99$。

#### AP (Affine Projection)

LMS 和 RLS 的折中：使用最近 $P$ 个输入向量构成投影矩阵，复杂度 $O(NP)$。

```python
def lms_filter(x, d, M, mu=0.01):
    """LMS 自适应滤波"""
    N = len(x)
    w = np.zeros(M)
    y = np.zeros(N)
    e = np.zeros(N)
    for n in range(M, N):
        x_vec = x[n-M:n][::-1]
        y[n] = w @ x_vec
        e[n] = d[n] - y[n]
        w += mu * e[n] * x_vec
    return y, e, w

def nlms_filter(x, d, M, mu=0.5, eps=1e-8):
    """NLMS 自适应滤波"""
    N = len(x)
    w = np.zeros(M)
    y = np.zeros(N)
    for n in range(M, N):
        x_vec = x[n-M:n][::-1]
        y[n] = w @ x_vec
        e = d[n] - y[n]
        w += (mu / (eps + np.dot(x_vec, x_vec))) * e * x_vec
    return y, w
```

**应用：** 回声消除、主动降噪 (ANC)、信道均衡、干扰对消、系统辨识。

---

## 3. 估计与检测

### 3.1 参数估计

**理论：** 从含噪观测 $y[n] = s[n;\boldsymbol{\theta}] + w[n]$ 估计参数 $\boldsymbol{\theta}$。

#### 最大似然估计 (MLE)

$$\hat{\boldsymbol{\theta}}_{ML} = \arg\max_{\boldsymbol{\theta}} p(\mathbf{y}|\boldsymbol{\theta})$$

**性质：** 一致性、渐近无偏、渐近有效（达到 CRLB）、渐近正态。

#### 最大后验估计 (MAP)

$$\hat{\boldsymbol{\theta}}_{MAP} = \arg\max_{\boldsymbol{\theta}} p(\boldsymbol{\theta}|\mathbf{y}) = \arg\max_{\boldsymbol{\theta}} [p(\mathbf{y}|\boldsymbol{\theta}) \cdot p(\boldsymbol{\theta})]$$

当先验 $p(\boldsymbol{\theta})$ 为均匀分布时退化为 MLE。

#### 矩估计

令样本矩等于理论矩，求解参数。简单但不一定有效。

#### Cramér-Rao 下界 (CRLB)

$$\text{Var}(\hat{\theta}) \geq \frac{1}{I(\theta)} = \left(-E\left[\frac{\partial^2 \ln p(\mathbf{y}|\theta)}{\partial\theta^2}\right]\right)^{-1}$$

达到 CRLB 的估计量为有效估计量。

Fisher 信息矩阵（多参数）：$\mathbf{I}(\boldsymbol{\theta})_{ij} = -E[\partial^2\ln p/\partial\theta_i\partial\theta_j]$。

### 3.2 谱估计

#### 非参数法

**周期图 (Periodogram)：** $\hat{S}_{xx}(e^{j\omega}) = \frac{1}{N}|\sum_{n=0}^{N-1} x[n]e^{-j\omega n}|^2$

渐近无偏但方差大（不一致估计）。

**Bartlett 法：** 分 $K$ 段不重叠，每段 $M = N/K$ 点，取平均。方差降 $1/K$，频率分辨率降。

**Welch 法：** 加窗 + 重叠分段（通常 50%），更实用。

**Blackman-Tukey 法：** 估计自相关后加窗做 FFT。

#### 参数法

假设信号由白噪声驱动的线性系统产生（AR/MA/ARMA 模型），通过模型参数求 PSD。

$$S_{xx}(e^{j\omega}) = \sigma_w^2 \frac{|B(e^{j\omega})|^2}{|A(e^{j\omega})|^2}$$

**AR 模型谱估计（Yule-Walker）：**

$$\hat{r}_{xx}[m] = -\sum_{k=1}^{p} a_k \hat{r}_{xx}[m-k], \quad m=1,\ldots,p$$

Levinson-Durbin 算法 $O(p^2)$ 求解 Toeplitz 方程组。

```python
# 参数法谱估计
# AR 模型
ar_coeffs, sigma2 = signal.arburg(x, order=20)  # Burg 算法
f, Pxx = signal.arma2psd(ar_coeffs, sigma2, fs=fs)

# 非参数法
f, Pxx = signal.welch(x, fs=fs, nperseg=1024, noverlap=512)
f, Pxx = signal.periodogram(x, fs=fs)
```

#### 子空间法

**MUSIC (Multiple Signal Classification)：** 对自相关矩阵做特征分解，信号子空间 vs 噪声子空间。

$$P_{MUSIC}(\omega) = \frac{1}{\mathbf{a}^H(\omega)\mathbf{E}_N\mathbf{E}_N^H\mathbf{a}(\omega)}$$

$\mathbf{E}_N$ 为噪声特征向量矩阵，$\mathbf{a}(\omega)$ 为导向向量。峰值对应信号频率。

**ESPRIT (Estimation of Signal Parameters via Rotational Invariance)：**

利用信号子空间的旋转不变性估计频率，无需谱峰搜索，计算效率高于 MUSIC。

```python
# MUSIC 算法伪代码
R = x @ x.conj().T / N              # 自相关矩阵
eigvals, eigvecs = np.linalg.eigh(R) # 特征分解
# 按特征值排序，选小特征值对应向量为噪声子空间
idx = np.argsort(eigvals)
En = eigvecs[:, idx[:N-M]]           # 噪声子空间
# 扫描 MUSIC 谱
for w in freqs:
    a = np.exp(-1j * w * np.arange(N))  # 导向向量
    P[w] = 1 / (a.conj() @ En @ En.conj().T @ a)
```

### 3.3 信号检测理论

#### 假设检验

$H_0$: 仅有噪声，$H_1$: 信号+噪声。

**检测概率 vs 虚警概率：** $P_D = P(\text{判 } H_1 | H_1)$，$P_{FA} = P(\text{判 } H_1 | H_0)$。

#### Neyman-Pearson (NP) 准则

在约束 $P_{FA} \leq \alpha$ 下最大化 $P_D$。

似然比检验 (LRT)：

$$L(\mathbf{y}) = \frac{p(\mathbf{y}|H_1)}{p(\mathbf{y}|H_0)} \underset{H_0}{\overset{H_1}{\gtrless}} \gamma$$

对数似然比 (LLRT)：$\ln L(\mathbf{y}) \gtrless \ln\gamma$。

高斯白噪声下，LLRT 简化为能量检测：$\sum|y[n]|^2 \gtrless \gamma$。

#### 匹配滤波器

**理论：** AWGN 下使输出 SNR 最大的线性滤波器。

$$h_{opt}(t) = s^*(T-t)$$

即在 $t=T$ 时刻与已知信号 $s(t)$ 匹配（时间反转共轭）。

**最大输出 SNR：** $\text{SNR}_{max} = 2E/N_0$，$E = \int|s(t)|^2dt$。

**频域：** $H_{opt}(f) = S^*(f)e^{-j2\pi fT}$，即频域幅度匹配 + 线性相位补偿。

**离散形式：** $h[n] = s^*[M-n]$，实现为 FIR 滤波器或相关器。

```python
# 匹配滤波器
s = np.array([...])          # 已知信号模板
h = s[::-1].conj()           # 匹配滤波器冲激响应
y = np.convolve(x_noisy, h)  # 输出
peak_idx = np.argmax(np.abs(y))
# SNR = 2 * np.sum(np.abs(s)**2) / noise_var
```

#### ROC 曲线

接收机操作特性曲线：$P_D$ vs $P_{FA}$，不同门限 $\gamma$ 的轨迹。AUC (Area Under Curve) 衡量检测器整体性能。

### 3.4 时间序列分析

#### AR 模型 (自回归)

$$x[n] = \sum_{k=1}^p a_k x[n-k] + w[n]$$

传递函数：$H(z) = 1/A(z) = 1/(1+\sum a_k z^{-k})$

PSD：$S_{xx}(e^{j\omega}) = \sigma_w^2 / |A(e^{j\omega})|^2$

#### MA 模型 (滑动平均)

$$x[n] = \sum_{k=0}^q b_k w[n-k]$$

传递函数：$H(z) = B(z)$，PSD：$S_{xx} = \sigma_w^2 |B|^2$

#### ARMA 模型

$$x[n] = \sum_{k=1}^p a_k x[n-k] + \sum_{k=0}^q b_k w[n-k]$$

**模型定阶：** AIC $= 2K - 2\ln\hat{L}$，BIC $= K\ln N - 2\ln\hat{L}$（BIC 对过拟合惩罚更强）。

**应用：** 语音编码 (LPC)、预测编码、谱估计、金融时间序列、传感器数据建模。

---

## 4. 多载波与扩频

### 4.1 OFDM

**理论：** 将高速数据流分成 $N$ 个低速子流，在正交子载波上并行传输。

$$x(t) = \sum_{k=0}^{N-1} X[k] e^{j2\pi f_k t}, \quad f_k = f_0 + \frac{k}{T}$$

正交性：$\int_0^T e^{j2\pi f_k t}e^{-j2\pi f_l t}dt = T\delta[k-l]$

**FFT 实现：** OFDM 调制 = IFFT，解调 = FFT。效率极高。

#### 循环前缀 (CP)

在 IFFT 输出前插入 $N_{cp}$ 个样本（复制尾部），消除 ISI 和 ICI。

CP 长度要求：$T_{cp} \geq \tau_{max}$（最大多径时延）。

**效率损失：** $\eta = N/(N+N_{cp})$，典型 $N=1024, N_{cp}=64 \Rightarrow \eta \approx 94\%$。

#### OFDM 系统设计

```
比特流 → 信道编码 → 交织 → QAM 映射 → IFFT → 加 CP → DAC → 上变频 → 天线
                                                                              ↓
接收端 ← 均衡 ← QAM 解映射 ← 解交织 ← 信道解码 ← FFT ← 去 CP ← ADC ← 下变频 ← 天线
```

#### OFDM 同步

**载波频率同步：** 利用 CP 相关性、导频子载波。

**符号定时同步：** Schmidl-Cox 算法、Minn 算法、Park 算法。

```python
# Schmidl-Cox 粗同步
# 训练符号结构: [A, A] (前后两半相同)
def schmidl_cox_sync(y, N):
    N_half = N // 2
    P = np.zeros(len(y) - N)
    R = np.zeros(len(y) - N)
    for m in range(len(y) - N):
        P[m] = np.sum(y[m:m+N_half] * y[m+N_half:m+N].conj())
        R[m] = np.sum(np.abs(y[m:m+N_half])**2)
    M = np.abs(P) / R
    peak = np.argmax(M)
    return peak  # 符号起始位置
```

#### 信道估计

**导频辅助：** 在特定子载波插入已知导频（块状/梳状导频）。

**LS 估计：** $\hat{H}[k] = Y[k]/X[k]$（简单但对噪声敏感）。

**MMSE 估计：** $\hat{H}_{MMSE} = \mathbf{R}_{HH}(\mathbf{R}_{HH} + \sigma_w^2\mathbf{I})^{-1}\hat{H}_{LS}$

**应用：** Wi-Fi (802.11a/g/n/ax)、LTE/LTE-Advanced (下行)、DVB-T、5G NR。

### 4.2 扩频通信

#### DS-SS (直接序列扩频)

$$x_{ss}(t) = s(t) \cdot c(t)$$

$s(t)$ 为数据信号（比特周期 $T_b$），$c(t)$ 为 PN 码（码片周期 $T_c$），处理增益 $G_p = T_b/T_c = B_{ss}/B$。

**抗窄带干扰：** 干扰功率被扩展 $G_p$ 倍，SNR 改善 $G_p$。

**Rake 接收机：** 利用多径分集，对多个时延路径的相关输出加权合并。

```python
# PN 码生成 (m-sequence)
def m_sequence(taps, length):
    """生成 m 序列, taps 为反馈抽头 (如 [5,3])"""
    L = taps[0]
    reg = np.ones(L, dtype=int)
    seq = np.zeros(2**L - 1, dtype=int)
    for i in range(len(seq)):
        seq[i] = reg[-1]
        fb = np.sum(reg[taps - 1]) % 2
        reg = np.roll(reg, 1)
        reg[0] = fb
    return seq
```

#### FH-SS (跳频扩频)

载波频率在 PN 码控制下跳变。快跳频（每符号多次跳变）/慢跳频（多符号一次跳变）。

**应用：** 蓝牙、军事通信、抗干扰。

#### CDMA

每个用户分配独特码字，同时同频传输。

**Walsh-Hadamard 码（正交码）：** $H_{2n} = \begin{pmatrix} H_n & H_n \\ H_n & -H_n \end{pmatrix}$

**Gold 码：** 两个 m 序列的优选对异或，具有良好的互相关特性。

**远近效应 (Near-Far Problem)：** 需要精确功率控制。

### 4.3 DFT-s-OFDM / SC-FDMA

**理论：** 发射端先 DFT（预编码），再映射到子载波，再做 IFFT。本质上等价于单载波传输。

$$x[n] = \text{IDFT}\{\text{DFT}\{s[n]\} \cdot \text{子载波映射}\}$$

**优点：** PAPR（峰均比）比 OFDM 低约 2-4 dB，适合上行链路（终端功率受限）。

**应用：** LTE 上行 (SC-FDMA)、5G NR 上行 (DFT-s-OFDM)。

---

## 5. 空时信号处理

### 5.1 阵列信号处理

#### 均匀线
## 5. 空时信号处理

### 5.1 阵列信号处理

#### 均匀线阵 (ULA)

$M$ 个阵元，间距 $d$，入射角 $\theta$，导向向量：

$$\mathbf{a}(\theta) = [1, e^{-j2\pi d\sin\theta/\lambda}, \ldots, e^{-j2\pi(M-1)d\sin\theta/\lambda}]^T$$

阵列输出：$\mathbf{y}[n] = \mathbf{A}(\boldsymbol{\theta})\mathbf{s}[n] + \mathbf{w}[n]$

#### 波束成形 (Beamforming)

**延时求和波束成形：** $\mathbf{w}^H\mathbf{y}$，$\mathbf{w} = \mathbf{a}(\theta_0)/M$

**MVDR (Capon) 波束成形：** 在期望方向无失真，最小化输出功率。

$$\mathbf{w}_{MVDR} = \frac{\mathbf{R}^{-1}\mathbf{a}(\theta_0)}{\mathbf{a}^H(\theta_0)\mathbf{R}^{-1}\mathbf{a}(\theta_0)}$$

**LCMV (线性约束最小方差)：** 多约束条件，$\min \mathbf{w}^H\mathbf{R}\mathbf{w}$，s.t. $\mathbf{C}^H\mathbf{w} = \mathbf{f}$。

$$\mathbf{w}_{LCMV} = \mathbf{R}^{-1}\mathbf{C}(\mathbf{C}^H\mathbf{R}^{-1}\mathbf{C})^{-1}\mathbf{f}$$

#### MUSIC 算法

对空间自相关矩阵 $\mathbf{R} = E[\mathbf{y}\mathbf{y}^H]$ 特征分解，噪声子空间 $\mathbf{E}_N$。

$$P_{MUSIC}(\theta) = \frac{1}{\mathbf{a}^H(\theta)\mathbf{E}_N\mathbf{E}_N^H\mathbf{a}(\theta)}$$

谱峰对应 DOA 估计。分辨率优于 FFT 方法，但需要信号源数已知。

#### ESPRIT 算法

利用旋转不变性：两个平移子阵 $\mathbf{J}_1, \mathbf{J}_2$。

$$\mathbf{J}_1\mathbf{E}_S\boldsymbol{\Phi} = \mathbf{J}_2\mathbf{E}_S$$

对 $\mathbf{J}_2\mathbf{E}_S(\mathbf{J}_1\mathbf{E}_S)^+$ 做 SVD，对角元素 $\phi_k = e^{j2\pi d\sin\theta_k/\lambda}$。

**优点：** 无需谱峰搜索，自动配对，计算量小于 MUSIC。

```python
def esprit_doa(R, M, d, wavelength):
    """ESPRIT DOA 估计"""
    # 信号子空间
    eigvals, eigvecs = np.linalg.eigh(R)
    Es = eigvecs[:, -M:]  # 取 M 个大特征值对应向量
    # 旋转算子
    J1 = Es[:-1, :]  # 前M-1阵元
    J2 = Es[1:, :]   # 后M-1阵元
    Phi = np.linalg.lstsq(J1, J2, rcond=None)[0]
    angles = -np.angle(np.diag(Phi)) * wavelength / (2 * np.pi * d)
    return np.degrees(np.arcsin(angles))
```

### 5.2 MIMO 信号处理

**理论：** $N_t$ 发射天线，$N_r$ 接收天线，信道矩阵 $\mathbf{H} \in \mathbb{C}^{N_r \times N_t}$。

$$\mathbf{y} = \mathbf{H}\mathbf{x} + \mathbf{n}$$

**信道容量：**

$$C = \log_2\det\left(\mathbf{I}_{N_r} + \frac{\text{SNR}}{N_t}\mathbf{H}\mathbf{H}^H\right) \text{ bps/Hz}$$

当 $N_t = N_r = N$，富散射环境下容量近似线性增长：$C \approx N\log_2(1+\text{SNR})$。

**SVD 分解：** $\mathbf{H} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^H$，预编码 $\mathbf{V}$ + 接收成形 $\mathbf{U}^H$，将 MIMO 信道分解为 $r$ 个并行 SISO 信道（$r = \text{rank}(\mathbf{H})$）。

**预编码方案：**

- **ZF 预编码：** $\mathbf{W} = \mathbf{H}^H(\mathbf{H}\mathbf{H}^H)^{-1}$，消除干扰但放大噪声
- **MMSE 预编码：** $\mathbf{W} = \mathbf{H}^H(\mathbf{H}\mathbf{H}^H + \alpha\mathbf{I})^{-1}$，SNR 与干扰的折中

### 5.3 空时编码

#### STBC (Alamouti)

2 发 1 收，传输矩阵：

$$\mathbf{C} = \begin{pmatrix} s_1 & -s_2^* \\ s_2 & s_1^* \end{pmatrix}$$

接收端线性解码，获得满分集增益 $N_t N_r$，速率 $R=1$（2Tx）。

#### SFBC (空频分组码)

在 OFDM 子载波维度上编码，结合频率分集。结构类似 STBC 但跨子载波。

#### 空间复用 (V-BLAST)

独立数据流从不同天线发射，接收端通过 ZF/MMSE/SIC（串行干扰消除）检测。

$$\mathbf{y} = \mathbf{H}\mathbf{x} + \mathbf{n} \Rightarrow \hat{\mathbf{x}} = (\mathbf{H}^H\mathbf{H})^{-1}\mathbf{H}^H\mathbf{y} \text{ (ZF)}$$

**应用：** 802.11n/ac/ax (Wi-Fi)、LTE/5G NR (MIMO)、Massive MIMO (5G)。

---

## 6. 通信中的信号处理

### 6.1 同步

#### 载波同步

**理论：** 载波频率偏移 (CFO) $\Delta f$ 导致相位旋转 $e^{j2\pi\Delta f \cdot nT_s}$。

**方法：**
- **PLL (锁相环)：** 鉴相器 → 环路滤波器 → VCO，经典模拟/数字实现
- **Costas 环：** 适用于 BPSK/QPSK 载波恢复
- **ML 估计：** $\hat{\Delta f} = \arg\max_\phi \sum_n |y[n]e^{-j\phi n}|^2$
- **OFDM CFO 估计：** 利用 CP：$\hat{\epsilon} = \frac{1}{2\pi}\angle\left(\sum_{n=0}^{N_{cp}-1} y[n]^* y[n+N]\right)$

#### 符号同步

**早迟门 (Early-Late Gate)：** 比较超前和滞后采样点的相关值。

**Gardner 算法：** $e[n] = \text{Re}\{(y[2k] - y[2k-2])y^*[2k-1]\}$，每个符号 2 个采样即可。

**Mueller-Müller 算法：** 1 个采样/符号，基于判决反馈。

#### 帧同步

**相关检测：** 用已知前导码/同步字做匹配滤波。

$$\Lambda = \sum_{n} y[n] p^*[n] \gtrless \gamma$$

**Barker 码：** 13 位 Barker 码自相关旁瓣 $\leq 1$。

### 6.2 信道估计与均衡

#### 信道模型

**线性时变信道：** $y[n] = \sum_l h_l[n] x[n-l] + w[n]$

**频率选择性衰落：** 时延扩展 $\sigma_\tau > T_s$，信道有频率选择性。

**平坦衰落：** $\sigma_\tau \ll T_s$，信道只引起幅度和相位变化。

**衰落模型：** Rayleigh（无 LOS）、Rician（有 LOS）、Nakagami-$m$。

#### 信道估计

**训练序列法：** LS $\hat{H} = Y/X$，MMSE $\hat{H}_{MMSE} = \mathbf{R}_{HH}(\mathbf{R}_{HH}+\sigma^2\mathbf{I})^{-1}\hat{H}_{LS}$

**导频辅助：** 梳状导频 + 插值（线性/样条/维纳）。

**盲估计：** 利用信号的统计特性（二阶/高阶统计量、子空间方法）。

#### 均衡器

**ZF 均衡器：** $\mathbf{w}_{ZF} = \mathbf{H}^H(\mathbf{H}\mathbf{H}^H)^{-1}$，完全消除 ISI 但放大噪声。

$$\text{SNR}_{ZF,k} = \frac{\text{SNR}}{N_t} \cdot \frac{1}{[\mathbf{H}^H\mathbf{H}]^{-1}_{kk}}$$

**MMSE 均衡器：** $\mathbf{w}_{MMSE} = (\mathbf{H}^H\mathbf{H} + \sigma_w^2\mathbf{I})^{-1}\mathbf{H}^H$

**DFE (判决反馈均衡器)：** 前馈滤波器消除前导 ISI + 反馈滤波器消除后尾 ISI（基于已判决符号）。

**MLSE (最大似然序列估计)：** Viterbi 算法，在状态图中搜索最小距离路径，最优但复杂度 $O(S^L)$（$S$ 为星座点数，$L$ 为信道记忆长度）。

```python
# ZF/MMSE 均衡器
H = np.array([...])  # 信道矩阵
sigma2 = 0.01         # 噪声方差

# ZF
w_zf = np.linalg.pinv(H)

# MMSE
w_mmse = np.linalg.inv(H.conj().T @ H + sigma2 * np.eye(H.shape[1])) @ H.conj().T
```

### 6.3 信道编码与交织

#### 线性分组码

$(n, k)$ 码：$n$ 位码字，$k$ 位信息。$\mathbf{c} = \mathbf{m}\mathbf{G}$，校验 $\mathbf{H}\mathbf{c}^T = \mathbf{0}$。

**Hamming 码：** $(2^r-1, 2^r-1-r)$，最小距离 3，可纠 1 位错误。

**LDPC 码：** 稀疏校验矩阵，BP (Belief Propagation) 译码，接近容量。

$$P(\mathbf{c}|\mathbf{y}) \propto \prod_i P(c_i|y_i) \prod_j \delta(\mathbf{H}\mathbf{c}^T = \mathbf{0})$$

**Polar 码：** 信道极化，信息位在可靠子信道上。5G NR 控制信道。

#### 卷积码

编码：$\mathbf{c}[n] = \sum_k \mathbf{g}_k \mathbf{m}[n-k]$

**Viterbi 译码：** 最大似然序列检测，复杂度 $O(2^K)$（$K$ 为约束长度）。

**Turbo 码：** 并行级联卷积码 + 迭代译码（SISO 译码器交换外信息）。3G/4G 标准。

#### 交织

将突发错误随机化为随机错误，提高纠错能力。

**块交织：** 按行写入按列读出。**卷积交织：** 延迟线实现，无固定交织深度。

### 6.4 调制解调

#### 线性调制

**PSK (相移键控)：** $s_i = \sqrt{E_s} e^{j\phi_i}$

- BPSK：2 相，$\phi \in \{0, \pi\}$，1 bps/Hz
- QPSK：4 相，$\phi \in \{\pi/4, 3\pi/4, 5\pi/4, 7\pi/4\}$，2 bps/Hz
- 8PSK：8 相，3 bps/Hz

**QAM (正交幅度调制)：** 幅度和相位同时调制。

- 16-QAM：4×4 星座，4 bps/Hz
- 64-QAM：8×8 星座，6 bps/Hz
- 256-QAM：16×16 星座，8 bps/Hz

**星座图最小距离：** $d_{min} = \sqrt{\frac{3E_s}{M-1}}$（方形 QAM）

**误码率 (AWGN, 相干检测)：**

$$P_e \approx 2\left(1-\frac{1}{\sqrt{M}}\right)Q\left(\sqrt{\frac{3\log_2 M}{M-1}\frac{E_b}{N_0}}\right)$$

```python
# QAM 调制/解调
def qam_mod(bits, M=16):
    k = int(np.log2(M))
    symbols = np.arange(-np.sqrt(M)+1, np.sqrt(M), 2)
    constellation = np.array([(x + 1j*y) for x in symbols for y in symbols])
    # Gray 映射
    bits_reshaped = bits.reshape(-1, k)
    indices = np.array([int(''.join(map(str, b)), 2) for b in bits_reshaped])
    return constellation[indices] / np.sqrt(np.mean(np.abs(constellation)**2))

def qam_demod(symbols, M=16):
    # 最近邻判决
    k = int(np.log2(M))
    symbols_up = symbols * np.sqrt(M-1)/np.sqrt(2)
    real_part = np.clip(np.round((symbols_up.real + 1) / 2 - 1), 
                        -np.sqrt(M)/2+1, np.sqrt(M)/2-1).astype(int)
    imag_part = np.clip(np.round((symbols_up.imag + 1) / 2 - 1),
                        -np.sqrt(M)/2+1, np.sqrt(M)/2-1).astype(int)
    # 映射回比特...
```

#### 恒包络调制

**GMSK (高斯最小频移键控)：**

MSK 调制前通过高斯低通滤波器（$BT = 0.3$ 典型值），相位连续变化。

$$\phi(t) = \pi \sum_n a_n \int_{-\infty}^{t-nT} g(\tau) d\tau, \quad g(t) = \frac{1}{2T}\text{rect}\left(\frac{t}{T}\right) * h_{gauss}(t)$$

**应用：** GSM、AIS（船舶自动识别）、卫星通信。

#### OFDM 调制解调

见 4.1 节。发射端 IFFT + CP，接收端去 CP + FFT。

**应用：** Wi-Fi (OFDM)、LTE (下行 OFDM/上行 SC-FDMA)、5G NR (CP-OFDM/DFT-s-OFDM)。

---

## 7. 实际工程实现

### 7.1 Python/NumPy/SciPy 工具链

**核心工具：**

```python
import numpy as np                # 数值计算
import scipy.signal as signal     # 信号处理
import scipy.fft as fft           # FFT
import matplotlib.pyplot as plt   # 可视化

# 常用操作
signal.convolve(x, h, mode='full')       # 线性卷积
signal.fftconvolve(x, h)                 # FFT 加速卷积（长序列）
signal.resample(x, new_fs, fs)           # 重采样
signal.resample_poly(x, up, down)        # 有理数倍重采样
signal.decimate(x, q, ftype='fir')       # 抽取（含抗混叠滤波）
signal.upfirdn(h, x, up, down)           # 多采样率处理（多相分解）

# 滤波器设计
signal.butter / cheby1 / cheby2 / ellip  # IIR 设计
signal.firwin / firls / remez            # FIR 设计
signal.iirnotch / iirpeak                # 陷波/峰值滤波器

# 频谱分析
signal.welch / periodogram / csd         # PSD 估计
signal.stft / istft                      # 短时傅里叶变换
signal.spectrogram                       # 频谱图
signal.hilbert                           # 解析信号/Hilbert 变换

# 滤波
signal.lfilter(b, a, x)                  # IIR 滤波（直接 II 型）
signal.filtfilt(b, a, x)                 # 零相位滤波（前向+后向）
signal.sosfilt(sos, x)                   # 二阶节滤波（数值稳定）
signal.lfilter_zi(b, a)                  # 初始条件

# 窗函数
signal.windows.hann / hamming / blackman / kaiser / dpss
```

**MATLAB 对照：** `scipy.signal` 大部分函数与 MATLAB `signal processing toolbox` 命名一致。

### 7.2 嵌入式 DSP 实现

#### 定点数运算

**Q 格式：** Qm.n 表示 $m$ 位整数，$n$ 位小数，总 $m+n+1$ 位（含符号位）。

Q15 范围：$[-32768, 32767]$，表示 $[-1, 1-2^{-15}]$。

**乘法溢出处理：** Q15×Q15 → Q30，右移 15 位得 Q15，需舍入处理。

```c
// Q15 乘法 (ARM CMSIS-DSP 风格)
int16_t q15_mul(int16_t a, int16_t b) {
    int32_t prod = (int32_t)a * b;
    // 舍入
    prod += 1 << 14;
    return (int16_t)(prod >> 15);
}
```

**数值范围与精度权衡：** Q 格式 vs 浮点 vs 块浮点。

#### 查表法 (LUT)

**正弦/余弦查表：** 存储 $1/4$ 周期，利用对称性。

```c
// 正弦查表 (256 点, Q15)
const int16_t sin_table[64] = { 0, 804, 1608, ... };
int16_t sin_lut(uint16_t phase) {
    uint16_t index = phase & 0x3FFF;  // 14-bit, 0~16383
    uint16_t quadrant = (phase >> 14) & 0x3;
    uint16_t lut_idx = index >> 8;    // 6-bit lookup
    int16_t val = sin_table[lut_idx];
    if (quadrant == 1) val = sin_table[63 - lut_idx];
    else if (quadrant == 2) val = -val;
    else if (quadrant == 3) val = -sin_table[63 - lut_idx];
    return val;
}
```

**CORDIC 算法：** 仅用移位和加法计算三角函数/幅度/相位，无需乘法器。

#### 循环缓冲 (Circular Buffer)

FIR 滤波器高效实现：

```c
#define TAP 64
int16_t buffer[TAP];
int head = 0;

int16_t fir_circular(int16_t x_new) {
    buffer[head] = x_new;
    int32_t acc = 0;
    for (int i = 0; i < TAP; i++) {
        acc += (int32_t)coeffs[i] * buffer[(head - i + TAP) % TAP];
    }
    head = (head + 1) % TAP;
    return (int16_t)(acc >> 15);  // Q15 舍入
}
```

#### DSP 处理器架构

**常用平台：**

| 平台 | 特点 | 典型应用 |
|------|------|----------|
| TI C6000 | VLIW, 高性能 | 基站、雷达 |
| TI C5000 | 低功耗 | 便携音频 |
| ARM Cortex-M4/M7 | DSP 指令集, SIMD | IoT, 可穿戴 |
| FPGA (Xilinx/Intel) | 并行, 可定制 | SDR, 雷达, 高速 |
| ADSP-21xx | 经典定点 DSP | 音频/电机控制 |

**关键指令：** MAC (乘累加)、SIMD (单指令多数据)、饱和运算、环形寻址。

### 7.3 实时性约束与优化

#### 计算复杂度

**FIR 滤波：** 每输出样本 $M$ 次 MAC → 每秒 $M \cdot f_s$ 次 MAC。

**FFT：** $N\log_2 N$ 次复数乘法。1024 点 FFT ≈ 10K MAC。

**实时约束：** 处理时间 $< T_s = 1/f_s$。例如 $f_s = 48$ kHz → 预算 20.8 μs/样本。

#### 优化策略

1. **算法级：** 多相分解降低多采样率计算量、快速卷积（FFT）替代线性卷积、对称 FIR 减半乘法
2. **实现级：** SIMD 向量化、循环展开、DMA 减少数据搬运、内存对齐
3. **定点优化：** Q 格式选择避免溢出、块浮点、饱和运算

**FFT 长度选择：** 选择 2 的幂或小素因子组合以利用高效 FFT 算法。

**SIMD 优化示例 (ARM NEON)：**

```c
// 4 个 Q15 样本同时处理
int16x4_t x_vec = vld1_s16(&x[n]);    // 加载 4 个样本
int16x4_t h_vec = vld1_s16(&h[k]);    // 加载 4 个系数
int32x4_t prod = vmull_s16(x_vec, h_vec); // 4 次并行乘法
acc = vpadalq_s16(acc, vreinterpretq_s16_s32(prod)); // 累加
```

#### SDR (软件定义无线电) 框架

**GNU Radio：** 开源信号处理框架，模块化流程图。

**关键模块：** Signal Source → Filter → Modulator → UHD Sink (USRP)

```python
# GNU Radio 流程图（概念）
import gnuradio.gr as gr
import gnuradio.filter as filter
import gnuradio.analog as analog
import gnuradio.uhd as uhd

# OFDM 接收链
tb = gr.top_block()
src = uhd.usrp_source(device_addr="addr=192.168.10.2", ...)
src.set_samp_rate(20e6)
src.set_center_freq(2.4e9)
src.set_gain(30)
# → FFT → CP 去除 → 信道估计 → QAM 解映射 → 解码 → Sink
```

**嵌入式 SDR：** AD9361 (Analog Devices) + FPGA，支持 1×1 到 4×4 MIMO，带宽 2.56 MHz - 56 MHz。

---

## 附录

### A. 常用数学公式速查

| 公式 | 表达式 |
|------|--------|
| Parseval (DTFT) | $\sum|x[n]|^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi}\|X(e^{j\omega})\|^2 d\omega$ |
| Parseval (DFT) | $\sum_{n=0}^{N-1}\|x[n]\|^2 = \frac{1}{N}\sum_{k=0}^{N-1}\|X[k]\|^2$ |
| Wiener-Khinchin | $S_{xx}(e^{j\omega}) = \mathcal{F}\{r_{xx}[m]\}$ |
| CRLB | $\text{Var}(\hat{\theta}) \geq 1/I(\theta)$ |
| 匹配滤波器 SNR | $\text{SNR}_{max} = 2E/N_0$ |
| Shannon 容量 | $C = B\log_2(1+\text{SNR})$ bps |
| SQNR | $\approx 6.02B + 1.76$ dB |

### B. 典型应用场景

| 场景 | 核心技术 |
|------|----------|
| 音频处理 | FFT/STFT、FIR/IIR 滤波、自适应降噪 |
| 5G NR | OFDM、MIMO、LDPC/Polar、波束成形 |
| Wi-Fi 6/7 | OFDMA、MU-MIMO、1024/4096-QAM |
| 雷达 | 匹配滤波、CFAR、MTI、MUSIC/ESPRIT |
| 声纳 | 波束成形、匹配滤波、多普勒处理 |
| 医学信号 (ECG/EEG) | 小波去噪、自适应滤波、谱分析 |
| 图像处理 | DCT、小波变换、滤波器组 |
| 金融 | ARIMA/GARCH 时间序列、谱分析 |
| 语音编码 | LPC (AR 建模)、CELP、CELP 编码 |

### C. 学习路径建议

1. **基础：** 信号与系统 → 数字信号处理 (Oppenheim) → 概率论与随机过程
2. **进阶：** 统计信号处理 (Kay) → 自适应滤波 (Haykin) → 通信原理 (Proakis)
3. **专题：** 阵列信号处理 → MIMO 通信 → 信息论与编码
4. **实践：** MATLAB/Python 仿真 → SDR 实现 → 嵌入式 DSP 部署
