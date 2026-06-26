# 微信公众号发布技能 - 用户使用手册

**版本：** V1.1.6  
**更新日期：** 2026-03-29  
**适用平台：** Windows / macOS / Linux

---

## 📖 目录

1. [快速开始](#1-快速开始)
2. [安装 OpenClaw](#2-安装-openclaw)
3. [安装发布技能](#3-安装发布技能)
4. [配置公众号信息](#4-配置公众号信息)
5. [设置发布时间](#5-设置发布时间)
6. [购买专业版](#6-购买专业版)
7. [常见问题](#7-常见问题)

---

## 1. 快速开始

### 1.1 完整安装流程（5 分钟）

### 🆕 V1.1.6 新功能：智能去重

**每次发布前自动执行：**
1. ✅ 读取上次发布记录
2. ✅ 实时收集新闻
3. ✅ 比对去重（标题 + 内容）
4. ✅ 数量验证（≥15 条）
5. ✅ 空数据处理（换方向收集）
6. ✅ 最终验证（每条≥80 字）
7. ✅ 发布公众号

**确保每次发布都是新鲜内容，无重复！**

---

```bash
# 第 1 步：安装 OpenClaw
npm install -g openclaw

# 第 2 步：安装微信公众号发布技能
openclaw skill install wechat-publisher

# 第 3 步：配置公众号信息
openclaw skill config wechat-publisher

# 第 4 步：设置发布时间（可选）
openclaw schedule wechat-publisher 07:00

# 第 5 步：完成！
# 每天早上 7 点自动发布 15 条 AI 新闻到公众号草稿箱
```

### 1.2 系统要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 10+ / macOS 10.15+ / Linux |
| **Node.js** | 16.0+ |
| **Python** | 3.8+（技能自动安装） |
| **网络** | 可访问微信 API |
| **公众号** | 已认证的微信公众号 |

---

## 2. 安装 OpenClaw

### 2.1 Windows 系统

```bash
# 1. 以管理员身份打开 PowerShell
# 2. 安装 OpenClaw
npm install -g openclaw

# 3. 验证安装
openclaw --version

# 输出示例：
# OpenClaw 2026.3.8
```

### 2.2 macOS 系统

```bash
# 1. 打开终端
# 2. 安装 OpenClaw
npm install -g openclaw

# 3. 验证安装
openclaw --version
```

### 2.3 Linux 系统

```bash
# 1. 打开终端
# 2. 安装 Node.js（如未安装）
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# 3. 安装 OpenClaw
sudo npm install -g openclaw

# 4. 验证安装
openclaw --version
```

### 2.4 验证安装成功

```bash
# 查看 OpenClaw 状态
openclaw status

# 输出示例：
# ✅ OpenClaw 运行正常
# 版本：2026.3.8
# 工作目录：~/.openclaw/workspace
```

---

## 3. 安装发布技能

### 3.1 在线安装（推荐）

```bash
# 安装微信公众号发布技能
openclaw skill install wechat-publisher

# 输出示例：
# ✅ 技能安装成功
# 技能名称：wechat-publisher
# 版本：V1.0
# 位置：~/.agents/skills/wechat-publisher
```

### 3.2 离线安装

```bash
# 1. 下载技能包
# 从 https://clawhub.com 下载 wechat-publisher.zip

# 2. 解压到技能目录
unzip wechat-publisher.zip -d ~/.agents/skills/

# 3. 验证安装
openclaw skill list

# 输出应包含：wechat-publisher
```

### 3.3 查看已安装技能

```bash
# 列出所有技能
openclaw skill list

# 查看技能详情
openclaw skill info wechat-publisher

# 输出示例：
# 技能名称：wechat-publisher
# 版本：V1.0
# 状态：已安装
# 授权状态：试用版（剩余 2 次）
```

---

## 4. 配置公众号信息

### 4.1 获取公众号配置信息

**步骤 1：登录微信公众号后台**
```
1. 访问 https://mp.weixin.qq.com
2. 扫码登录你的公众号
```

**步骤 2：找到 AppID**
```
1. 点击左侧菜单：开发 → 基本配置
2. 找到"公众号开发信息"
3. 复制 AppID（示例：wxebff9eadface1489）
```

**步骤 3：获取 AppSecret**
```
1. 在"基本配置"页面
2. 点击"生成"或"重置"AppSecret
3. 管理员扫码验证
4. 复制 AppSecret（示例：44c10204ceb1bfb3f7ac096754976454）
5. ⚠️ 重要：AppSecret 只显示一次，请妥善保存！
```

### 4.2 配置方式一：交互式配置（推荐）

```bash
# 运行配置命令
openclaw skill config wechat-publisher

# 进入交互式配置界面：
╔════════════════════════════════════════════════════╗
║       微信公众号发布技能 - 配置向导                 ║
╠════════════════════════════════════════════════════╣
║  请选择要配置的项目：                               ║
║                                                    ║
║  1. 公众号信息（AppID/AppSecret）                  ║
║  2. 发布时间                                       ║
║  3. 发布模板                                       ║
║  4. 新闻条数                                       ║
║  5. 完成配置                                       ║
║                                                    ║
╚════════════════════════════════════════════════════╝

请输入选项 (1-5): 1

╔════════════════════════════════════════════════════╗
║       配置公众号信息                               ║
╠════════════════════════════════════════════════════╣
║  请输入公众号 AppID: wxebff9eadface1489            ║
║  请输入公众号 AppSecret: ********                  ║
║                                                    ║
║  ✅ 公众号信息已保存                               ║
╚════════════════════════════════════════════════════╝
```

### 4.3 配置方式二：命令行配置

```bash
# 一条命令完成配置
openclaw skill config wechat-publisher \
  --app-id wxebff9eadface1489 \
  --app-secret 44c10204ceb1bfb3f7ac096754976454

# 输出：
# ✅ 公众号信息已保存
```

### 4.4 配置方式三：手动编辑配置文件

```bash
# 1. 打开配置文件
# 位置：~/.agents/skills/wechat-publisher/config/config.json

# 2. 编辑文件内容：
{
  "app_id": "wxebff9eadface1489",
  "app_secret": "44c10204ceb1bfb3f7ac096754976454",
  "schedule": "06:00",
  "template": "v5-simple",
  "news_count": 15,
  "timezone": "Asia/Shanghai"
}

# 3. 保存文件
```

### 4.5 验证配置

```bash
# 查看当前配置
openclaw skill config wechat-publisher --show

# 输出示例：
╔════════════════════════════════════════════════════╗
║       微信公众号发布技能 - 当前配置                 ║
╠════════════════════════════════════════════════════╣
║  公众号 AppID: wxebff9e******1489                  ║
║  公众号 AppSecret: 44c102******6454                ║
║  发布时间：06:00（每天早上 6 点）                     ║
║  发布模板：V5 简洁版                                ║
║  新闻条数：15 条                                    ║
║  时区：Asia/Shanghai（东八区）                      ║
║  授权状态：试用版（剩余 2 次）                       ║
╚════════════════════════════════════════════════════╝
```

---

## 5. 设置发布时间

### 5.1 设置单次发布时间

```bash
# 设置每天早上 7 点发布
openclaw schedule wechat-publisher 07:00

# 输出：
# ✅ 发布时间已设置为：07:00（每天早上 7 点）
# 下次执行：2026-03-27 07:00:00
```

### 5.2 设置多次发布时间

```bash
# 设置每天发布两次（早 7 点 + 晚 6 点）
openclaw schedule wechat-publisher 07:00,18:00

# 输出：
# ✅ 发布时间已设置为：07:00, 18:00
# 下次执行：2026-03-27 07:00:00
```

### 5.3 查看当前定时设置

```bash
# 查看定时设置
openclaw schedule wechat-publisher --show

# 输出示例：
╔════════════════════════════════════════════════════╗
║       微信公众号发布技能 - 定时设置                 ║
╠════════════════════════════════════════════════════╣
║  当前定时：06:00（每天早上 6 点）                     ║
║  下次执行：2026-03-27 06:00:00                     ║
║  时区：Asia/Shanghai（东八区）                      ║
║  状态：已激活                                       ║
╚════════════════════════════════════════════════════╝
```

### 5.4 修改发布时间

```bash
# 方法 1：直接修改
openclaw schedule wechat-publisher 07:30

# 方法 2：通过配置向导
openclaw skill config wechat-publisher
# 选择"发布时间"选项
# 输入新时间：07:30
```

### 5.5 取消定时发布

```bash
# 取消定时发布
openclaw schedule wechat-publisher --disable

# 输出：
# ✅ 定时发布已取消
# 可以手动运行：openclaw skill run wechat-publisher
```

---

## 6. 购买专业版

### 6.1 查看授权状态

```bash
# 查看当前授权状态
openclaw skill status wechat-publisher

# 输出示例：
╔════════════════════════════════════════════════════╗
║       微信公众号发布技能 - 授权状态                 ║
╠════════════════════════════════════════════════════╣
║  当前状态：试用版                                  ║
║  剩余试用次数：2 次                                 ║
║  已使用：0 次                                       ║
║                                                    ║
║  💎 专业版：8.8 元 永久买断                          ║
║     运行：openclaw skill buy wechat-publisher      ║
╚════════════════════════════════════════════════════╝
```

### 6.2 购买专业版

```bash
# 运行购买命令
openclaw skill buy wechat-publisher

# 进入购买界面：
╔════════════════════════════════════════════════════╗
║       购买专业版                                    ║
╠════════════════════════════════════════════════════╣
║  价格：8.8 元（永久买断）                            ║
║                                                    ║
║  功能：                                            ║
║  ✅ 无限次使用                                     ║
║  ✅ 全部 5 套模板                                   ║
║  ✅ 自动更新支持                                   ║
║  ✅ 优先技术支持                                   ║
║                                                    ║
║  支付方式：                                        ║
║  1. 微信扫码支付                                   ║
║  2. 支付宝扫码支付                                 ║
║                                                    ║
╚════════════════════════════════════════════════════╝

[二维码图片显示]

订单号：WP202603262100001
金额：8.8 元

正在等待支付...
```

### 6.3 激活专业版

```bash
# 如果获得激活码，运行：
openclaw skill activate wechat-publisher YOUR_LICENSE_CODE

# 输出示例：
# ✅ 激活成功！
# 授权状态：专业版（永久）
# 激活时间：2026-03-26 21:00:00
```

### 6.4 查看授权信息

```bash
# 查看授权详情
openclaw skill license wechat-publisher

# 输出示例：
╔════════════════════════════════════════════════════╗
║       微信公众号发布技能 - 授权信息                 ║
╠════════════════════════════════════════════════════╣
║  授权状态：✅ 专业版（永久）                        ║
║  激活时间：2026-03-26 21:00:00                     ║
║  激活码：WP26-W12-A3F8-B9D2                        ║
║                                                    ║
║  可用模板：                                        ║
║  ✅ v1-basic.html                                 ║
║  ✅ v2-premium.html                               ║
║  ✅ v3-mainstream.html                            ║
║  ✅ v4-modules.html                               ║
║  ✅ v5-simple.html                                ║
╚════════════════════════════════════════════════════╝
```

---

## 7. 常见问题

### 7.1 安装问题

**Q1: npm 安装失败？**
```bash
# 解决方案 1：使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install -g openclaw

# 解决方案 2：使用 sudo（macOS/Linux）
sudo npm install -g openclaw
```

**Q2: openclaw 命令找不到？**
```bash
# Windows：重启 PowerShell 或添加到 PATH
# macOS/Linux：添加 npm 全局路径到 PATH
export PATH=$PATH:$(npm config get prefix)/bin
```

### 7.2 配置问题

**Q3: AppSecret 配置后不生效？**
```bash
# 检查配置文件权限
# macOS/Linux:
chmod 600 ~/.agents/skills/wechat-publisher/config/config.json

# Windows: 以管理员身份运行配置命令
```

**Q4: 如何修改已配置的 AppSecret？**
```bash
# 重新运行配置命令
openclaw skill config wechat-publisher
# 选择"公众号信息"选项
# 重新输入 AppSecret
```

### 7.3 发布问题

**Q5: 发布失败，提示 Token 无效？**
```bash
# Token 有效期为 2 小时，会自动刷新
# 如持续失败，检查：
# 1. AppID 是否正确
# 2. AppSecret 是否正确
# 3. 公众号是否已认证
```

**Q6: 封面图上传失败？**
```bash
# 检查图片要求：
# 1. 格式：JPG/PNG
# 2. 尺寸：建议 900x383px
# 3. 大小：< 2MB

# 或使用公众号已有素材：
openclaw skill config wechat-publisher
# 选择"封面图来源" → "使用公众号已有素材"
```

### 7.4 授权问题

**Q7: 试用次数用完后如何继续使用？**
```bash
# 购买专业版
openclaw skill buy wechat-publisher

# 或联系技术支持获取帮助
```

**Q8: 激活码无效？**
```bash
# 检查激活码格式：
# 正确格式：WP26-W12-A3F8-B9D2（16 位，4 组）

# 如仍无效，联系技术支持
```

---

## 📞 技术支持

- **文档：** https://docs.openclaw.ai
- **社区：** https://discord.gg/clawd
- **邮箱：** support@openclaw.ai

---

_本手册最后更新：2026-03-26_  
_技能版本：V1.0_
