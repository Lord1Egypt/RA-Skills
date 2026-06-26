---
name: xhs-html-creator
description: 小红书图文创作技能。触发条件：用户说"生成图文"、"创作内容"、"做图文矩阵"、"生成XX的图文"时使用。功能：读取素材库 → 生成7张竖屏小红书图文 → AI专家两轮review迭代 → 用户最终确认交付。
---

# 小红书图文创作（xhs-html-creator）

## 核心能力

输入主题 → 读素材库 → 生成全套HTML → AI专家review（两轮）→ 用户确认 → 交付图片

## 六步标准流程

### 第一步：确认方向
- 用户说什么主题、什么风格
- 主代理确认：内容范围、页面数量、发布平台
- **这个skill不爬数据**，数据从素材库读（调用xhs-material-collector）
- **起点确认**：问用户从哪里开始
  - **空白新建**：根据主题和风格偏好从零创作
  - **参考模板**：从模板库选一个模板为基础（notion_v2 / baoyu_v2 / hospitalNEW / memo）
  - **基于旧版本**：提供旧HTML文件路径，在此基础上重写

### 第二步：生成全套HTML
- 根据素材库分析结果 + 用户需求写全套HTML
- **每次改版必须从零重写整个文件**，禁止find-replace
- 同时启动HTTP服务，用playwright截图
- 截图脚本：`output/screenshot.py`
- 把截图发到用户飞书（用`feishu_image.py`）

### 第三步：专家第一轮review
- **主代理用`image`工具把全套图发给AI专家**，用户不参与
- 必须问完整的5个问题：
  1. 字号够不够大？文字是否一眼可见？
  2. 布局单调不单调？
  3. 封面点击欲够不够？
  4. 手机阅读体验好不好？
  5. 行动号召明不明显？
- 专家给意见后，主代理记录问题

### 第四步：按专家意见重写
- **从零重写全套HTML**，不是find-replace，是整套重写
- 修完再截图，再发给用户

### 第五步：专家第二轮review
- 同样用image工具发专家
- 专家确认问题是否已修复

### 第六步：用户最终确认
- 专家说可以 → 发给用户确认
- 用户说行 → 交付

### 迭代规则（最多2轮review）
| 轮次 | 情况 | 处理方式 |
|------|------|---------|
| 第1轮 | 任何问题 | 自动重写，不问用户 |
| 第2轮 | 任何问题 | 自动重写，不问用户 |
| 第2轮后 | 只有次要问题 | **直接交付**（不发用户确认） |
| 第2轮后 | 仍有致命问题 | 再重写1次，然后**强制交付** |
| 最终 | 交付前 | **必须发用户确认** ✅ |

**致命问题**：内容被遮挡/截断/Tip框挡物品/底部CTA挡文字 → 必须修
**次要问题**：间距略松/颜色略淡/缺乏呼吸感 → 可保留交付

### 旧版本文件清理规则
每轮迭代完成后，清理上一轮的非最终文件：
- 保留：`output/` 目录下**最新一版**全套HTML
- 删除：所有旧版本HTML（如 `daishengbao_v2.html` 升级到 v3 后删 v2）
- 不删：模板库 `templates/` 下的历史模板（只读存档）
- 交付后：只保留最终版到 `output/`

---

## 专家review标准prompt

### 5个基本问题（每次必问）
```
请以小红书图文运营专家身份，检查这组图文：
1. 字号够不够大？文字是否一眼可见？
2. 布局单调不单调？
3. 封面点击欲够不够？
4. 手机阅读体验好不好？
5. 行动号召明不明显？
```

### 孕产类内容专用prompt（合规检查）
```
请以小红书图文运营专家的身份，帮我优化这组待产包图文：
1. 指出视觉、排版，信息密度问题！文字一定要清晰且够大，肉眼一眼可见
2. 优化标题、封面文案，内页文案！
3. 补充孕产类内容的合规注意事项（严禁医疗术语、避免制造焦虑）
4. 给出可直接修改的具体建议，不要空泛
5. 结合爆款逻辑，提供对应建议！
```

---

## HTML排版原则（必须遵守）

### 布局原则
- 内容区用 `position:absolute`，按 top/left/right 定位
- **分类标签用普通流式布局（display:block/inline-block）**，不用 `position:absolute`
- **禁止用绝对定位把元素叠加在内容上**（tip框浮在内容上是常见错误）

### 间距原则
- 每项之间留足够间距（12-14px），不要密不透风
- **tip框必须放在所有内容下方**，不能浮在内容上
- 1080×1350px 固定尺寸，内容必须在此范围内完整显示

### 字号原则
- 物品名：30-38px，加粗
- 描述文字：20-24px，颜色用**深灰或黑色**（不用浅灰，对比度要够）
- 标题：64px 加粗
- **底线：宁大勿小，肉眼一眼可见**

### 拆页原则
- 一页12项是极限，超过就拆
- 内容多的分类拆成2页，每页不超过8项
- tip框永远放页面最底部，不挡内容
- **宁可多拆一页，不要内容重叠**

### 禁止事项
- 禁止医疗术语（如"肚脐贴"→"脐部护理类（听医嘱）"）
- 禁止一套HTML用find-replace改，要从零重写每个文件

### 合规红线
- 禁用医疗术语：肚脐贴、收腹带（改为"遵医嘱"）、产妇卫生巾（改为"透气卫生巾"）
- 避免："一定会"、"必须"、"保证"等绝对化用语
- 避免：制造焦虑的文案（如"不准备就后悔"）

---

## 页面结构规范

### 标准7页结构（待产包为例）
1. 封面 — 精简入口，标题醒目
2. 证件篇 — 5项
3. 宝宝1 — 衣物类4项
4. 宝宝2 — 喂养类4项+护理类
5. 妈妈1 — 衣物+护理（各4项）
6. 妈妈2 — 喂养+日用
7. 结尾页 — 打包技巧+互动引导+CTA+话题标签

### 每页必须有的元素
- 顶部标题栏（色块+大字标题）
- 页码标注
- 分类标签（流式，不挡内容）
- 物品卡片（序号+名称+描述+数量）
- 底部tip框（可选，必须在所有内容下方）

### 结尾页特殊要求
- 打包技巧3条
- 互动引导（评论区问题）
- CTA按钮（醒目颜色）
- 话题标签（黑底白字，清晰可见）
- **CTA在上，互动引导在中，标签在下，不要重叠**

---

## 文件位置

```
skills/xhs-html-creator/
├── SKILL.md
├── output/
│   ├── shots/           ← 截图输出
│   ├── daishengbao_cover_v3.html
│   ├── daishengbao_doc_v3.html
│   └── ...
├── templates/           ← 4个确认模板（模板库位置固定）
└── scripts/
```

## HTML规范（各模板通用标准）

### 通用尺寸
- 固定尺寸：`width:1080px; height:1440px`（或 `min-height:1440px`）
- 外层容器：`body { margin:0; padding:0; width:1080px; }`
- 截图 viewport：`1080×1350px`（留出顶部状态栏高度）

### 各模板规范

#### notion_v2（现代简约+手写书法）
| 项目 | 规范 |
|------|------|
| 背景 | `#fff` 纯白 |
| 字体 | 标题用 `Ma Shan Zheng`（Google Fonts 手写体）；正文用 `Noto Sans SC` |
| 装饰 | 左侧 `1.5px` 红色竖线（`left:32px; width:1.5px; background:#cc0000`）|
| 物品列表 | notion表格样式：`border-collapse:collapse`，表头36px深灰，物品行36px手写体 |
| 字号 | 标题76px，物品名36px，描述36px灰色，字号统一 |
| 禁止 | 禁止渐变背景、禁止彩色色块、禁止阴影卡片 |

#### baoyu_v2（手绘治愈风）
| 项目 | 规范 |
|------|------|
| 背景 | `#f5f0e8` 暖米色 |
| 字体 | 标题用 `ZCOOL KuaiLe`（Google Fonts 童稚体）；正文用 `Noto Sans SC` |
| 装饰 | 左侧暖色条纹（`linear-gradient(180deg, #e8d5c4, #d4c4a8)`）；纸张纹理（`repeating-linear-gradient`） |
| 主色 | `#d4a574` 焦糖金；辅色 `#e8919a` 淡粉 |
| 卡片 | `background:#fff; border-radius:16px; border:3px solid #e8d5c4` |
| 字号 | 标题84px，物品名30px，描述26px |

#### hospitalNEW（清新母婴风）
| 项目 | 规范 |
|------|------|
| 背景 | `#FFF0F5` 极淡粉 |
| 彩虹条 | `height:18px; background:linear-gradient(90deg,#E87090,#FFB3C6,#4A90E2,#89C4F8,#52C77B)` |
| 字体 | `PingFang SC` / `Microsoft YaHei`（系统字体，无需下载） |
| 辅色 | 粉 `#E87090`、蓝 `#4A90E2`、绿 `#52C77B` |
| 数字卡片 | `background:#fff; border-radius:18px; box-shadow:0 6px 22px rgba(色,0.13); border:2px solid` |
| 分类图标 | 圆形色块（`width:50px; height:50px; border-radius:50%; background:#色`）+ emoji |
| 字号 | 标题82px 加粗，数字60px，辅文28px，物品名30px |

#### memo（简约备忘录风）
| 项目 | 规范 |
|------|------|
| 背景 | `#fff` 纯白 |
| 字体 | 系统默认无衬线（`PingFang SC` / `Microsoft YaHei`） |
| 点缀色 | `#F7B521` 金黄；`#EF8F31` 橙色；`#7CA9CF` 淡蓝 |
| 列表标记 | 圆形金黄背景 `width:36px; height:36px; background:#F7B521; border-radius:50%` + 打钩符号 |
| 标签 | 淡蓝底 `background:#F0F7FF; border-radius:6px; padding:2px 8px; color:#7CA9CF` |
| 字号 | 标题32px加粗800，物品名30px，标签26px |

### 通用禁止事项
- 禁止医疗术语（肚脐贴→脐部护理类（听医嘱）；收腹带→遵医嘱）
- 禁止绝对化用语（"必须"、"保证"、"一定"）
- 禁止用 `position:absolute` 把 tip 框叠加在内容上
- 禁止内容溢出 `1440px` 高度（底部被截断）

## 模板库（4个确认模板）

模板库路径：`skills/xhs-html-creator/templates/`

| 模板 | 风格 | 文件 | 页数 |
|------|------|------|------|
| **notion_v2** | 现代简约+手写书法，黑白灰+红色点缀 | notion_v2_01.html（宝宝物品）<br>notion_v2_02.html（封面）<br>notion_v2_03.html（证件物品） | 3页 |
| **baoyu_v2** | 手绘治愈风，暖米+焦糖金+ZCOOL字体 | baoyu_v2_01.html ~ 04.html | 4页 |
| **hospitalNEW** | 清新母婴风，彩虹条+粉蓝绿圆角白卡 | 封面.html<br>妈妈用品篇.html<br>妈妈衣物篇.html<br>宝宝护理篇.html<br>宝宝衣物篇.html | 5页 |
| **memo** | 简约备忘录风，纯白+金黄+emoji清单 | memo_01.html（v1）<br>memo_02.html（v2） | 2个版本 |

**选模板规则**：根据主题和目标受众推荐，不是让用户自己选。

---

## 截图脚本模板

路径使用相对路径或环境变量，禁止硬编码用户目录：

```python
# screenshot.py
import os, sys
from pathlib import Path

# 相对路径：相对于 workspace 根目录
WORKSPACE = Path(r'C:\Users\95116\.openclaw\workspace')
shots_dir = WORKSPACE / 'skills' / 'xhs-html-creator' / 'output' / 'shots'
shots_dir.mkdir(parents=True, exist_ok=True)

pages = [
    ('daishengbao_cover_v3.html', 'cover_v3'),
    ('daishengbao_doc_v3.html',    'doc_v3'),
    # ...
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 1350})
    for html, name in pages:
        url = f'http://127.0.0.1:8899/{html}'
        page.goto(url, wait_until='networkidle', timeout=15000)
        page.wait_for_timeout(1500)
        page.screenshot(path=shots_dir / f'{name}.png')
        print(f'Saved {name}')
    browser.close()
```

## 发飞书脚本模板

```python
# send_images.py
import subprocess, os, time
from pathlib import Path

WORKSPACE = Path(r'C:\Users\95116\.openclaw\workspace')
script = WORKSPACE / 'skills' / 'feishu-image' / 'scripts' / 'feishu_image.py'
user_id = 'ou_620fceb1cd2bccee9363926691161a2d'
shots_dir = WORKSPACE / 'skills' / 'xhs-html-creator' / 'output' / 'shots'
images = ['cover_v3.png', 'doc_v3.png', ...]
for img in images:
    path = shots_dir / img
    result = subprocess.run(['python', str(script), str(path), user_id], capture_output=True)
    print(result.stdout.decode())
    time.sleep(1.5)
```

## HTTP服务

截图前需启动HTTP服务：
```bash
cd skills/xhs-html-creator/output
python -m http.server 8899
```

---

## 填充率标准

在写代码之前，先评估内容是否够满：

```
页面可用高度 ≈ 1100px
每行卡片高度 ≈ 60-80px
每段间距 ≈ 12-16px

预估总高度 = (每行高度 × 行数) + (间距 × 段数)
填充率 = 预估总高度 / 1100px

合格线：填充率 > 60%
```

填充率不足时：
1. 增加物品数量
2. 增加描述文字长度
3. 增加tips内容

---

## 教训（踩过的坑）

1. **不要用find-replace改HTML** — 不同版本结构可能不同，必须从零重写
2. **tip框不要用absolute** — 会浮在内容上方挡住东西，必须放最底部
3. **分类标签不要用absolute** — 会和物品行重叠，用流式布局
4. **描述文字颜色不能太淡** — 深灰或黑色，确保手机屏幕也能看清
5. **超过12项必须拆页** — 不要硬挤在一页里
6. **肚脐贴是医疗术语** — 改为"脐部护理类（听医嘱）"
