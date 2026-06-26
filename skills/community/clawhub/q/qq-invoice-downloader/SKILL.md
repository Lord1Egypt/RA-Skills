# QQ邮箱发票下载器 SKILL

## 用途
自动登录QQ邮箱，搜索指定时间段的发票邮件，下载PDF附件，处理压缩包，并生成Excel目录

## 使用方法

```bash
# v8.2 最新版 (推荐)
python invoice_downloader_v82.py 260201 260310

# 输出目录: Z:\OpenClaw\InvoiceOC\260201-260310_v1\
```

## 核心特性

| 特性 | 说明 |
|------|------|
| **智能搜索** | 修复 date_lt 参数，支持精确日期范围 |
| **智能自适应按钮识别** | 自动扫描"下载"/"批量zip下载"等关键词 |
| **只下载PDF/图片** | 跳过 OFD/XML/CSV |
| **保留原文件名** | 不添加时间戳前缀 |
| **重名处理** | MD5内容比对，不同加版本号 |
| **ZIP解压后删除** | 自动解压并删除压缩包 |
| **跳过非发票** | 过滤堂食明细、小票等 |
| **SSL自动降级** | SSL失败时自动禁用验证重试 |
| **Excel详细报告** | 成功/跳过/失败/异常分表显示 |

### 发票处理策略

| 发票类型 | 处理方式 |
|----------|----------|
| 直接附件 | HTTP直接下载 |
| 诺诺网 | 浏览器点击下载按钮 |
| 税务平台(预览) | 浏览器点击PDF下载 |
| 税务平台(直链) | HTTP直接下载 |
| 飒拉商业 | 筛选PDF链接+HTTP下载 |
| 中海油/批量下载 | 识别"批量zip下载"按钮 |
| 通行费发票 | ZIP解压 |

### 支持平台

- 和运国际 (上海税务)
- 诺诺网
- 百旺金穗云
- 飒拉商业
- 中国联通
- 中海油(批量zip下载)
- 通行费电子发票
- 所有PDF/ZIP/PNG/JPG附件

### 输出文件

```
260201-260310_vX/
├── attachments/          # 发票文件
├── 发票目录.xlsx        # Excel报告
│   ├── 全部记录         # 所有邮件处理记录
│   ├── 成功            # 成功下载
│   ├── 跳过_重复       # 内容重复跳过的
│   ├── 失败            # 下载失败
│   └── 处理异常        # 处理异常
└── detailed_results.json # 详细JSON日志
```

## 关键教训

> ⚠️ Playwright 浏览器必须串行！多线程要加 Lock！
>
> greenlet.error: cannot switch to a different thread — 这是多线程并行 Playwright 导致。解决方案：单浏览器串行，通过 threading.Lock() 保证线程安全。

---

## Phase 1.5 - LLM 增强分析（invoice_analyzer_v9）

### LLM 触发条件

`InvoiceAnalyzerWithLLM` 在以下情况自动调用 MiniMax LLM：

| 条件 | 说明 |
|------|------|
| `confidence < 0.7` | 硬编码置信度不足 |
| `invoice_type == "unknown"` | 平台不在已知列表中 |

策略：硬编码优先 → 置信度不足或类型未知 → LLM fallback → 取置信度更高者

### MINIMAX_API_KEY 配置

```bash
# 设置环境变量（Windows PowerShell）
$env:MINIMAX_API_KEY = "your-api-key-here"

# 或在 Python 中直接传入
from invoice_analyzer_v9 import InvoiceAnalyzerWithLLM
analyzer = InvoiceAnalyzerWithLLM(api_key="your-api-key-here")

# 不设置 → 纯硬编码模式（v8.2 兼容行为）
```

### 测试方法

```bash
cd qq-invoice-downloader

# 语法检查
python -m py_compile invoice_downloader_v82.py
python -m py_compile invoice_analyzer_v9.py

# 导入验证
python -c "from invoice_analyzer_v9 import InvoiceAnalyzerWithLLM; print('import OK')"

# 运行集成测试（使用 unittest，pytest 可选）
python test/test_analyzer.py

# 或用 pytest
python -m pytest test/test_analyzer.py -v
```

### 测试覆盖

| 测试类 | 验证点 |
|--------|--------|
| `TestKnownPlatforms` | 和运国际/诺诺网/中海油 → 置信度 ≥ 0.7，不触发 LLM |
| `TestUnknownPlatformTriggersLLM` | 未知平台 → LLM 被调用并胜出 |
| `TestLLMWinsWhenBetter` | LLM 置信度 > 硬编码 → 使用 LLM |
| `TestFallbackPreservesBaseResult` | LLM 异常 → 保留硬编码结果 |
| `TestNonInvoiceSkip` | 非发票邮件 → unknown 类型 |
