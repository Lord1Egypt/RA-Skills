# 易店上货

> 闲鱼商品批量上传工具，基于 Playwright 自动化控制易店后台（ed.weeeg.com），实现从批量商品清单解析到自动上架的全流程自动化。

## 适合谁

- 闲鱼卖家，每天需要上架多个商品
- 使用易店后台（ekadmin）管理闲鱼店铺
- 商品是虚拟资源类（软件、教程、资料等），需配置百度网盘自动发货
- 想实现"每周整理一次，自动排队上架"

## 怎么用

### 在 WorkBuddy 里装

跟 AI 说一句 **「安装易店上货 Skill」** 就行，AI 会一步步引导你配好。

> 💡 **省流量小技巧**：用 WorkBuddy 的 **DSFlash** 模型来跑这个工具，速度快、省流量，日常上货完全够用。

### 自己跑脚本（不用 WorkBuddy 也行）

#### 环境准备

```bash
# 1. 安装 Python 3.10+
# 2. 安装 Playwright
pip install playwright
playwright install chromium

# 3. 启动 Edge 调试模式
# 关闭所有 Edge 窗口后，运行：
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222
```

#### 使用方式

```bash
# 方式1：飞书模式（推荐，从飞书多维表格读取商品清单）
python scripts/auto_publish.py --feishu

# 方式2：飞书预览模式
python scripts/auto_publish.py --feishu --dry-run

# 方式3：本地模式（从总上货.txt 读取）
python scripts/auto_publish.py

# 方式4：预览模式（不实际上架）
python scripts/auto_publish.py --dry-run

# 方式5：解析总上货.txt 并拆分到 day 目录
python scripts/batch_parser.py --apply
```

#### 总上货.txt 格式

**新版格式（推荐）：**

```
一、发布时间：6.23
二、商品文案：
商品标题
商品描述内容...
三、店铺：二号店铺名
四、网盘发货文案：
通过网盘分享的文件：xxx
链接：https://pan.baidu.com/s/xxx
提取码：abcd
```

**旧版格式（向后兼容）：**

```
以下为二号店铺名未来一周要上货的货品：
1.商品标题
描述内容...

通过网盘分享的文件：xxx
链接: https://... 提取码: xxxx

2.商品标题
描述内容...

通过网盘分享的文件：xxx
链接: https://... 提取码: xxxx
```

## 功能特性

### v3.4 新功能
- ✅ **CDP 直连方案** — Python websockets 直连 Edge CDP，绕过 Playwright 兼容性问题
- ✅ **每步自检重试** — 每步操作后自检，失败自动重试3次
- ✅ **Vue 响应式兼容** — nativeInputValueSetter + 多种事件触发，支持 Element UI 输入框
- ✅ **自动发货二次触发** — 保存后开关未变蓝 → 自动再点开关 + 重新保存
- ✅ **飞书多维表格同步** — 从飞书读取商品清单，上架后自动回写状态
- ✅ **表单校验** — 发布前自动检查表单错误，发布后等待跳转确认
- ✅ **飞书文档同步** — SKILL.md 变更自动同步到飞书对外展示文档

### v3.3 基础功能
- ✅ **日期过滤** — 只上架当天日期的商品
- ✅ **已发布标记** — 上架后自动标记，防重复
- ✅ **多格式支持** — 自动识别新旧两种格式
- ✅ **商品级店铺** — 每个商品可独立指定店铺
- ✅ **dispatchEvent选店铺** — 绕过Element UI teleport不可见
- ✅ **getComputedStyle检测弹窗** — 更可靠的弹窗检测

## 目录结构

```
.
├── README.md
├── CHANGELOG.md
├── SKILL.md              ← WorkBuddy 技能定义
└── scripts/
    ├── publisher.py      ← 发布函数模块 v3.4（CDP直连+每步自检+飞书融合）
    ├── feishu_reader.py  ← 飞书多维表格商品清单读取器（v3.4新增）
    ├── auto_publish.py   ← 自动上货主控（v3.4，支持--feishu模式）
    ├── batch_parser.py   ← 总txt解析+按天拆分（旧版）
    ├── full_flow.py      ← 单商品发布
    └── product_parser.py ← 单商品解析器（遗留）
```
