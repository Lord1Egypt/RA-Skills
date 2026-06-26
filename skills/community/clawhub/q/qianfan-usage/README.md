# Qianfan Usage

查询百度千帆 Coding Plan 用量和额度。

## 功能

- 🔍 自动检测 cookie 状态，失效时自动登录
- 📊 查询 Coding Plan 三级用量（5小时/周/月）
- 💾 保存登录状态，避免重复登录
- 🎨 彩色显示使用率和重置时间

## 安装

```bash
# 克隆仓库
git clone https://github.com/wsjwoods/qianfan-usage.git
cd qianfan-usage
```

## 使用方法

### 快速查询（推荐）

```bash
python3 qianfan_usage.py
```

自动检测 cookie 状态：
- ✅ 如果 cookie 有效，直接显示用量
- 🔑 如果 cookie 失效，自动打开登录页面，输入验证码即可

### 简化版（仅查询，需已登录）

```bash
python3 qianfan.py
```

### 完整版（带颜色和建议）

```bash
python3 check_quota_v2.py
```

## 配置

### 环境变量（可选）

设置手机号，避免每次输入：

```bash
export QIANFAN_PHONE=你的手机号
```

### Cookie 文件

登录成功后，cookie 自动保存到：
```
~/.baidu-qianfan-auth.json
```

## API 端点

```
GET https://console.bce.baidu.com/api/qianfan/charge/codingPlan/quota
```

返回格式：
```json
{
  "success": true,
  "result": {
    "quota": {
      "fiveHour": { "used": 25, "limit": 1200, "resetAt": "..." },
      "week": { "used": 2355, "limit": 9000, "resetAt": "..." },
      "month": { "used": 2355, "limit": 18000, "resetAt": "..." }
    }
  }
}
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `qianfan_usage.py` | ⭐ 主程序，自动检测 cookie + 自动登录 |
| `qianfan.py` | 简化版，仅查询（需已登录） |
| `check_quota_v2.py` | 完整版，带颜色和建议 |
| `SKILL.md` | OpenClaw 技能描述 |

## 项目结构

```
qianfan-usage/
├── qianfan_usage.py      # ⭐ 主程序
├── qianfan.py            # 简化版
├── check_quota_v2.py     # 完整版
├── README.md             # 文档
├── SKILL.md              # OpenClaw 技能描述
├── LICENSE               # MIT
└── .gitignore            # 忽略敏感文件
```

## 依赖

- Python 3.8+
- curl
- [agent-browser](https://github.com/nicepkg/agent-browser)（用于自动登录）

## 输出示例

```
🔍 检查登录状态...
✓ Cookie 有效，直接查询用量

╔══════════════════════════════════════════════════════════╗
║          📊 百度千帆 · Coding Plan 用量详情              ║
╚══════════════════════════════════════════════════════════╝

⏱️  5小时周期:
   已用: 25 / 1200 (2.1%)
   剩余: 1175
   重置: 03月13日 01:50

📅 本周用量:
   已用: 2355 / 9000 (26.2%)
   剩余: 6645
   重置: 03月16日 00:00

📆 本月用量:
   已用: 2355 / 18000 (13.1%)
   剩余: 15645
   重置: 04月09日 16:39

══════════════════════════════════════════════════════════

💡 使用建议：
   • 用量正常 (2.1%)，可以继续使用
   • 月度额度剩余 86.9%
```

## License

MIT
