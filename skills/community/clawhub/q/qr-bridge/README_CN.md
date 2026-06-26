> English version: [README.md](README.md)

# qr-bridge

**扫码、追链、诊断——一步到位。**

专为 AI 编程 Agent 设计的二维码入口侦察技能。不止于扫码——自动追踪重定向链路，识别微信/企微/淘宝/抖音/小红书等国内平台的封闭网关，并诊断链接打不开的真正原因。

## 为什么需要它

AI Agent 可以"看到"图片里的二维码，但无法解码。即使拿到了 URL，短链跳转、平台网关、登录拦截又会层层阻断。qr-bridge 把完整链路打通：

```
图片 → 二维码解码 → URL → 重定向追踪 → 网关识别 → 诊断建议
```

来源于真实场景：想通过一张海报图片报名北京 AI 线下活动，结果链接跳到微信内才能打开的表单——再怎么 `curl` 也打不开。

## 核心能力

| 功能 | 说明 |
|------|------|
| **解码 (Decode)** | 利用 macOS CoreImage 从图片中提取二维码，零依赖，约 10ms |
| **追链 (Trace)** | 逐跳追踪短链的完整重定向路径 |
| **识别 (Inspect)** | 检测微信、企微、淘宝、抖音、小红书等国内平台网关，精准识别"打不开"的根因 |
| **诊断 (Diagnose)** | 解释链接为什么打不开，并给出可操作的解决建议 |
| **生成 (Generate)** | 将文本或 URL 生成为二维码图片 |

## 快速开始

### 作为 Claude Code 技能使用
```bash
# 复制到技能目录
cp -r . ~/.claude/skills/qr-bridge/

# 编译 Swift 解码器
bash scripts/setup.sh
```

然后自然语言调用即可：*"扫一下这张图里的二维码"* 或 *"这个短链最终跳到哪里？"*

### 独立命令行使用
```bash
# 编译
swiftc scripts/qr-decode.swift -o scripts/qr-decode -O

# 解码
./scripts/qr-decode /path/to/image.png
```

输出：
```json
{
  "ok": true,
  "count": 1,
  "results": [
    {
      "message": "https://example.com",
      "symbology": "QRCode",
      "bounds": { "x": 40, "y": 40, "width": 290, "height": 290 }
    }
  ]
}
```

## 技术细节

- **主解码器**：macOS CoreImage (`CIDetectorTypeQRCode`) —— 系统原生，零外部依赖
- **备用方案**：pyzbar（当 CoreImage 不可用时）
- **二维码生成**：Python `qrcode` 库
- **网关识别**：基于域名、响应头和页面内容的模式匹配
- **重定向追踪**：`curl -sIL` 逐跳记录

### 支持识别的网关类型

这是 qr-bridge 对国内用户最核心的价值——**自动识别中国互联网生态中常见的封闭网关**，精准定位"为什么打不开"：

| 网关 | 识别方式 | 解决方法 |
|------|----------|----------|
| 微信 | `weixin.qq.com` 域名、MicroMessenger UA 检测 | 需在微信内打开 |
| 企业微信 | `work.weixin.qq.com`、企业认证 | 需为组织成员 |
| 淘宝 | `tb.cn`、`tbopen://` 深度链接 | 需在淘宝 App 内打开 |
| 抖音 | `douyin.com`、`snssdk://` | 需在抖音 App 内打开 |
| 小红书 | `xhslink.com` | 需在小红书 App 内打开 |
| 登录拦截 | 401/403 状态码、`/login` 重定向 | 需先登录 |

## 环境要求

- macOS（CoreImage 解码器依赖）
- Python 3 + `qrcode[pil]`（用于二维码生成）
- 可选：`pyzbar` + `zbar`（备用解码器）

## 诞生故事

这个技能诞生于 Claude Code 和 OpenClaw（觉）的一次协作。我们发现：
1. AI 视觉模型能"看到"二维码，但无法"解读"
2. 真正的难点不在解码，而在于应对解码之后的各种平台网关
3. macOS CoreImage 可以原生解码二维码，完全不需要第三方库

关键灵感来自 OpenClaw 使用 CoreImage 解码，而 Claude Code 还在苦苦安装 Python 库。不同的工具，同一个团队。

## 许可证

MIT
