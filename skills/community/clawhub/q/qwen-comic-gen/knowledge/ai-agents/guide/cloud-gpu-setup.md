# 🖥️ 云端 GPU 设置指南

**作者**: Xiabi  
**日期**: 2026-03-03  
**目标**: 快速搭建云端 AI 视频生成环境

---

## 📍 **为什么需要云端 GPU？**

你的电脑配置（MX450, 2GB 显存）不足以运行大型 AI 模型（如 SadTalker、Stable Video Diffusion），这些模型需要至少 6-8GB 显存才能流畅运行。

**解决方案**：租用云端 GPU 实例，按小时付费，灵活又便宜！

---

## 🔧 **推荐平台对比**

| 平台 | 价格 | GPU 型号 | 优点 | 缺点 | 推荐指数 |
|------|------|---------|------|------|----------|
| **AutoDL** | ¥0.5-2/小时 | A100/T4 | 中文界面，国内速度，可备案 | 需实名认证 | ⭐⭐⭐⭐⭐ |
| Google Colab Pro | $10/月 | T4/P100 | 简单易用，有免费版 | 连接不稳定 | ⭐⭐⭐⭐ |
| Kaggle Kernels | 免费 | P100 | 完全免费 | 每日 30h 限制 | ⭐⭐⭐⭐ |
| Paperspace | $0.29/小时 | V100/A100 | 专业稳定 | 美元结算 | ⭐⭐⭐ |

**最终推荐**: **AutoDL**

---

## 🚀 **AutoDL 完整教程**

### **Step 1: 注册账号**

1. 访问 https://www.autodl.com
2. 点击右上角"注册"
3. 用手机/邮箱验证
4. 完成实名认证（需要身份证）

### **Step 2: 充值费用**

- 最低充值：¥30
- 支付方式：微信/支付宝
- 余额可用于所有实例

### **Step 3: 创建实例**

1. 点击"新建实例"
2. 选择配置：
   ```
   GPU: Tesla T4 x1  ← 性价比高，够用
   系统盘：50GB SSD
   内存：16GB
   带宽：按需（下载模型时开高速，平时关小）
   ```
3. 镜像选择：
   ```
   Deep Learning → Ubuntu 20.04 + PyTorch 2.x
   OR
   Search: "SadTalker" → 可能有预装好的模板
   ```
4. 时长设置：先选"按量付费"（用完即停）

### **Step 4: 连接并操作**

#### **方式 A: Jupyter Lab（最简单）**

- AutoDL 会自动生成一个 Jupyter Lab 地址
- 浏览器打开 → 直接拖拽上传文件 → 运行脚本

#### **方式 B: VS Code Remote**

```bash
# 在本地安装 VS Code + Remote SSH 插件
# 然后连接到远程实例进行开发
```

### **Step 5: 克隆 SadTalker**

在 Jupyter Lab 的终端里执行：

```bash
# 进入工作目录
cd ~/Autodl_Task

# 克隆 SadTalker 仓库
git clone https://github.com/Winfain-Sam/SadTalker.git
cd SadTalker

# 自动安装依赖
pip install -r requirements.txt

# 下载模型权重（第一次运行时会提示）
python inference.py --source_image path/to/photo.jpg --driven_audio path/to/audio.mp3
```

### **Step 6: 生成视频**

准备两个文件：
- `photo.jpg`：你的人像照片
- `audio.mp3`：AI 生成的台词音频

然后在 Jupyter Lab 里运行：

```python
from IPython.display import Audio, Image
!python inference.py \
    --source_image ./inputs/photo.jpg \
    --driven_audio ./inputs/audio.mp3 \
    --result_dir ./outputs \
    --enhancer codeformer
```

等待 5-10 分钟，完成后可以在 `./outputs` 看到生成的视频！

### **Step 7: 下载成果 & 关机**

1. 在 Jupyter Lab 右键 `./outputs/*` → Download
2. 回到 AutoDL 控制台 → 关闭实例（停止计费）
3. 下次需要时再开机（重启后数据保留）

---

## 💰 **费用估算**

### **学习阶段（第 1 个月）**

- 每天调试 1 小时 × 30 天 = 30 小时
- ¥1/小时 × 30 = **¥30**

### **制作阶段（每天 1 条视频）**

- 每次生成约 10 分钟
- 每天 1 次 × ¥0.2 = **¥6/月**

**总预算**: **¥100 以内** / 第一个月

---

## 🔗 **其他有用工具**

### **ElevenLabs（AI 语音合成）**
- 网址：https://elevenlabs.io
- 费用：$5/月（免费版有限制）
- 用途：把剧本台词转成真人配音

### **FFmpeg（视频剪辑）**
- 安装：`winget install Gyan.FFmpeg`
- 用途：合并片段、加字幕、调色

示例命令：
```bash
ffmpeg -i output.mp4 -vf subtitles=subtitle.srt final.mp4
```

---

## ✅ **总结**

1. **先申请 AutoDL 账号并完成实名认证**
2. **充值 ¥30**
3. **创建一个 T4 GPU 实例**
4. **用 Jupyter Lab 上传 SadTalker 代码和素材**
5. **运行脚本生成视频**
6. **下载成果后立即关机停止计费**

整个过程熟练后，**一条视频的生成成本只要 ¥0.2 左右**！

---

_持续更新中..._
_Last updated: 2026-03-03_
