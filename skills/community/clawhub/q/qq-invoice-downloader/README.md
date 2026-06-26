# Openclaw Skills QQ邮箱发票自动下载器

自动登录 QQ 邮箱，搜索发票邮件，智能识别平台类型，下载 PDF 附件并生成 Excel 目录。

---

## 一键安装（Windows）

```bat
# 方法1: 一键安装脚本（推荐）
# 下载仓库后双击 install.bat

# 方法2: 命令行
git clone https://github.com/FrankFuShMomentLab/qq-invoice-downloader.git %TEMP%\qq-invoice-downloader
xcopy /e /i /y %TEMP%\qq-invoice-downloader %USERPROFILE%\.openclaw\skills\qq-invoice-downloader
```

安装后**重启 OpenClaw** 即可生效。

---

## 快速开始

```bash
# 安装依赖
pip install imap-tools pandas openpyxl requests playwright
playwright install chromium

# 运行（最新版 v8.2）
python invoice_downloader_v82.py 260201 260310

# 输出目录: Z:\OpenClaw\InvoiceOC\260201-260310_v1\
```

## 核心功能

- **IMAP 自动登录** QQ 邮箱，支持授权码
- **智能邮件分类**（A/B/C 三类分流处理）
- **多平台识别**：和运国际（上海税务）、诺诺网、百旺金穗云、飒拉商业、中国联通、中海油、12306 等
- **PDF 附件直接下载** + **ZIP 压缩包自动解压**
- **Playwright 浏览器自动化**（税务平台点击下载）
- **MD5 内容去重**，避免重复下载
- **Excel 详细报告**（成功/跳过/失败/异常分表）
- **auto 模式**：增量同步上次截止日期至今的所有发票

## ABC 三类处理架构

```
A类: 邮件直接带 PDF/ZIP 附件 → HTTP 直接下载（8线程并行）
B类: 邮件内有下载链接       → 正则提取 + HTTP 下载（5线程并行）
C类: 税务平台需浏览器点击   → Playwright 自动化（必须串行！必须加 Lock！）
```

## 发票平台支持

### Phase 1 原有平台
| 平台 | 类型 | 下载方式 |
|------|------|----------|
| 和运国际（上海税务） | C类 | 浏览器点击 |
| 诺诺网 | C类 | 浏览器点击 |
| 百旺金穗云 | C类 | 浏览器点击 |
| 飒拉商业 | B类 | PDF链接 HTTP |
| 中国联通 | A类 | 直接附件 |
| 中海油 | A/B类 | 批量ZIP |
| 通行费电子发票 | A类 | 直接附件 |
| 12306 火车票 | A类 | 直接附件 |

### Phase 2 新增平台（30+）
| 平台 | 类型 | 下载方式 |
|------|------|----------|
| 票易通 | C类 | 浏览器点击 |
| 航天信息 | C类 | 浏览器点击 |
| **顺丰速运** | C类 | 浏览器点击 |
| **中国邮政** | C类 | 浏览器点击 |
| **中通快递** | C类 | 浏览器点击 |
| **韵达快递** | C类 | 浏览器点击 |
| **圆通速递** | C类 | 浏览器点击 |
| **申通快递** | C类 | 浏览器点击 |
| **京东电子发票** | C类 | 浏览器点击 |
| **拼多多商家发票** | C类 | 多步浏览器 |
| **美团发票** | C类 | 浏览器点击 |
| **滴滴出行** | C类 | 浏览器点击 |
| **高德打车** | C类 | 浏览器点击 |
| **曹操出行** | C类 | 浏览器点击 |
| **携程发票** | C类 | 多步浏览器 |
| **同程旅行** | C类 | 多步浏览器 |
| **飞猪机票** | C类 | 多步浏览器 |
| **酒店预订** | C类 | 浏览器点击 |
| **饿了么** | C类 | 浏览器点击 |
| **大众点评** | C类 | 浏览器点击 |
| **腾讯电子发票** | C类 | 浏览器点击 |
| **阿里云发票** | C类 | 多步浏览器 |
| **华为云发票** | C类 | 多步浏览器 |
| **京东云发票** | C类 | 浏览器点击 |
| **移动电子发票** | C类 | 浏览器点击 |
| **联通电子发票** | C类 | 浏览器点击 |
| **电信电子发票** | C类 | 浏览器点击 |
| **招商银行发票** | C类 | 浏览器点击 |
| **平安银行发票** | C类 | 浏览器点击 |

## 文件结构

```
qq-invoice-downloader/
├── invoice_downloader_v82.py    # ✅ 主程序（智能自适应按钮识别）
├── browser_processor.py         # 浏览器处理核心模块
├── enhanced_browser_handler.py  # 增强浏览器处理
├── invoice_analyzer.py          # 邮件智能分析
├── smart_browser.py             # 智能浏览器工具
├── logger.py                    # 日志工具
├── error_handler.py             # 错误处理
├── SKILL.md                     # OpenClaw Skill 文档
├── CHANGELOG.md                 # 版本历史
├── PROJECT_EXPERIENCE.md        # 项目经验总结
├── COMPLETE_EXPERIENCE.md       # 完整踩坑记录
├── FINAL_TEST_REPORT.md         # 综合测试报告
├── QUICKSTART.md                # 快速启动指南
├── run_with_report.bat          # Windows 批处理启动脚本
└── test_data.json               # 测试数据
```

## 关键教训（必读）

> ⚠️ **Playwright 浏览器必须串行！多线程要加 Lock！**
>
> v7.0 曾为追求极致性能使用多线程并行 Playwright，导致 `greenlet.error: cannot switch to a different thread` 严重错误。解决方案：单浏览器串行处理，通过 `threading.Lock()` 保证线程安全。
>
> 教训：**稳定性 > 性能，不要为了速度牺牲稳定性。**

详见 [PROJECT_EXPERIENCE.md](PROJECT_EXPERIENCE.md)。

## 配置

通过环境变量配置（**不会上传到 GitHub**，保护你的隐私）：

```bash
# Windows
set QQ_EMAIL=你的QQ邮箱
set QQ_PASSWORD=你的QQ邮箱授权码
set INVOICE_BASE_DIR=Z:\OpenClaw\InvoiceOC

# macOS/Linux
export QQ_EMAIL=你的QQ邮箱
export QQ_PASSWORD=你的QQ邮箱授权码
export INVOICE_BASE_DIR=/path/to/InvoiceOC

# 运行
python invoice_downloader_v82.py 260201 260310
```

> ⚠️ 授权码不是登录密码，是 QQ 邮箱「设置 → 账户 → POP3/IMAP/SMTP」里生成的授权码。

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v8.2 | 2026-03-12 | 智能自适应按钮识别、SSL自动降级、中海油平台支持 |
| v8.1 | 2026-03-10 | 智能搜索修复、只下载PDF/图片、MD5内容去重、Excel详细报告 |
| v7.2 | 2026-03-09 | 增强稳定版：指数退避重试、结构化日志、浏览器定期重启 |
| v7.1 | 2026-03-09 | 修复 greenlet 错误，单浏览器串行处理 |

完整历史见 [CHANGELOG.md](CHANGELOG.md)。

---

**维护者**: Frank（银河漫游者）  
**License**: MIT
