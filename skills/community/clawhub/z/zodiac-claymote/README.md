# 十二生肖黏土软萌风表情包生成器 · 使用说明

> 一句话：**描述角色和情绪，脚本自动装配完整提示词；生成无字图后自动叠中文文案，导出微信规格。**

---

## 1. 它能做什么

| 能力 | 说明 |
|---|---|
| 12 生肖原创角色 | 每个生肖有固定配色、体貌、性格、招牌动作，保证成套不重样 |
| 20+ 工种人设 | 教师 / 学生 / 工程师 / 医护 / 产品 / 运营 / 销售 / 财务 / 外卖 / 法务… |
| 24 种情绪 × 26 个场景 | 从"崩溃改作业"到"周五躺平"，情绪不重复、场景有层次 |
| 提示词自动装配 | 中英别名都认（dragon / teacher / angry），输出可直接复制的英文提示词 |
| 中文文案叠加 | 生图模型画中文必错，所以文案一律后期叠加，描边白字 |
| 微信规格导出 | 自动裁正方 + 240×240 主图 + 体积检测 |

---

## 2. 目录结构（符合主流平台规范）

```
zodiac-claymote/          ← 包根目录（SKILL.md 必须在这里）
├── SKILL.md                  技能主入口【必需】
├── skill.yaml                元数据（扣子/Coze 等平台读取）
├── README.md                 本文件
├── LICENSE.md                限时免费商用授权条款
├── DISCLAIMER.md             免责声明
├── 授权证书模板.md            可填写的原创声明与商用授权凭证
├── scripts/                  可执行脚本
│   ├── build_prompt.py       提示词装配器（零依赖）
│   ├── caption_sticker.py    文案叠加 + 裁切 + 导出
│   ├── remove_watermark.py   清除生图工具水印
│   ├── wechat_pack.py        微信投稿全套素材一键生成 + 校验
│   ├── validate_pack.py      结构自检器（零依赖）
│   └── requirements.txt      依赖清单
├── references/               参考文档（按需加载，不占常驻上下文）
│   ├── style-bible.md        画风规范
│   ├── zodiac-characters.md  12 生肖原创角色卡
│   ├── professions.md        20+ 工种设定
│   ├── scenes-emotions.md    24 情绪 × 26 场景
│   ├── prompt-templates.md   中英模板 + 20 条示例
│   └── wechat-spec.md        微信表情开放平台规范 + 审核红线
└── assets/                   示例与模板资源
    └── examples/
        ├── prompts-16.md     12 生肖轮换成套示例
        ├── prompts-龙x工程师.md
        └── captions.json     文案映射模板
```

这个结构同时满足 WorkBuddy / CodeBuddy、扣子 Coze（豆包同生态）、Claude / Claude Code 的技能包约定：**根目录一份 SKILL.md + 可选的 scripts/ references/ assets/**。

---

## 3. 各平台安装方式

| 平台 | 安装方式 |
|---|---|
| **WorkBuddy / CodeBuddy** | 把整个文件夹放到 `~/.workbuddy/skills/` 下即可自动识别；或在技能管理里选择导入本地文件夹 |
| **扣子 Coze / 豆包** | 扣子编程 → 技能 → 附件 → 上传技能包（ZIP）。**注意：压缩文件夹内部的内容，不要连外层文件夹一起压** |
| **Claude（网页/桌面）** | 设置 → 自定义技能 → 添加技能，上传 ZIP 包 |
| **Claude Code** | 放到 `~/.claude/skills/` 或项目 `.claude/skills/` 目录 |
| **其他支持 Agent Skills 的平台** | 绝大多数沿用同一约定，放对目录即可；若平台要求 `skill.yaml` 元数据，本包已提供 |

> 平台差异兜底：SKILL.md 放在根目录这一条最关键。少数平台会自动做结构转换，只要根目录有 SKILL.md 就能识别。

---

## 4. 环境准备

### 依赖说明

- `build_prompt.py`、`validate_pack.py`：**零依赖**，任意 Python 3.8+ 直接跑
- `caption_sticker.py`：需要 Pillow（文案叠加用）

```bash
pip install -r scripts/requirements.txt
```

本机（Windows + WorkBuddy 托管环境）示例：
```powershell
C:\Users\peisenzhang\.workbuddy\binaries\python\envs\default\Scripts\pip.exe install Pillow
```
> 不想装 Pillow 也能用：提示词生成无需依赖，只是不能用自动加文案，可手动在设计软件里加字。

### 命令写法

下文所有命令都假设**当前目录是技能包根目录**，用相对路径：

```bash
python scripts/build_prompt.py --list
```
Windows PowerShell 里把 `python` 换成你的解释器路径即可。

---

## 5. 三步出图（最快路径）

### 第 1 步 · 生成提示词

```bash
python scripts/build_prompt.py --set 16 --mix --out prompts.md
```
- `--set 16`：16 张一套（可选 24）
- `--mix`：12 生肖轮换；去掉则固定单一生肖
- 打开 `prompts.md`，每张都有「场景 / 配色 / 服装 / 道具 / 文案 / 英文提示词」

> 懒得跑脚本？直接看 `assets/examples/prompts-16.md`，抄里面的提示词即可。

### 第 2 步 · 生成图片

把每段代码块内的英文提示词逐张喂给生图工具，**参数一律 1:1 正方形**。
文末的负向提示词每张都要带上（整套一致，画风才不漂移）。

### 第 3 步 · 加文案 + 出图

```bash
python scripts/caption_sticker.py --input ./raw --captions "好耶,无语,我裂开,摸了" --size 240
```
自动完成：居中裁方 → 叠加白字描边 → 导出 `01.png…16.png` → 超 100KB 会告警。

---

## 6. 命令速查

### 查看所有可选项
```bash
python scripts/build_prompt.py --list
```

### 单张定制
```bash
python scripts/build_prompt.py --zodiac 龙 --job 工程师 --emotion 崩溃 --scene 线上出Bug --text 线上炸了
```
中英文参数都行，终端编码有问题的机器上用英文更稳：
```bash
python scripts/build_prompt.py -z dragon -j engineer -e crash -t "线上炸了"
```

### 成套生成
```bash
# 12 生肖轮换 × 各自推荐职业（最丰富）
python scripts/build_prompt.py --set 16 --mix --out out/全套16.md

# 单一角色深挖：鸡 × 教师，24 张
python scripts/build_prompt.py --set 24 --zodiac 鸡 --job 教师 --out out/教师鸡24.md

# 指定统一职业
python scripts/build_prompt.py --set 16 --mix --job 工程师 --out out/工程师16.md

# 导出 JSON 给程序用
python scripts/build_prompt.py --set 16 --mix --json --out out/prompts.json
```

### 文案叠加进阶
```bash
# 用映射文件，顺序完全可控（模板见 assets/examples/captions.json）
python scripts/caption_sticker.py --input ./raw --caption-map assets/examples/captions.json --size 240

# 只裁切导出，不加文字
python scripts/caption_sticker.py --input ./raw --no-text --size 512

# 字放顶部 / 改颜色
python scripts/caption_sticker.py --input ./raw --position top --color "#FFE45C" --stroke "#7A3B00"

# 导出微信缩略图
python scripts/caption_sticker.py --input ./raw --size 120 --output ./thumb
```

---

## 6.5 清水印 + 一键生成微信投稿素材包

### 清除生图工具水印（投稿硬要求：画面不得有水印）

```bash
# 1) 先生成红框预览，确认框住水印
python scripts/remove_watermark.py --input ./raw --corner br --area "0.35,0.08" --preview

# 2) 确认后正式清除（fill 零依赖；装了 opencv-python 可用 --method inpaint）
python scripts/remove_watermark.py --input ./raw --corner br --area "0.35,0.08" --method fill

# 3) 位置不对就用像素坐标精确指定
python scripts/remove_watermark.py --input ./raw --region "900,1010,180,60" --method inpaint
```
定位方式三选一：`--region "x,y,w,h"`（最准）/ `--corner br --area "宽比,高比"` / `--auto` 自动检测。

### 一键产出全套投稿素材

```bash
python scripts/wechat_pack.py --input ./sticker_out --raw-src ./cleaned --banner-src ./cleaned \
  --cover 01.png --icon 09.png --with-tips --zip --name "生肖打工人"
```

一条命令产出并逐项校验：

```
wechat_submit/
├── 表情图/01.png…        240×240 PNG ≤500KB（自动压体积，默认保留原始背景）
├── 缩略图/01.png…        120×120 PNG
├── 表情封面图.png         240×240 PNG 圆外透明（圆形徽章+描边环）
├── 聊天面板图标.png        50×50  PNG 圆外透明（头部徽章+描边环）
├── 详情页横幅.jpg         750×400 渐变底+徽章排列+装饰（无文字、非白底）
├── 赞赏引导图/致谢图       750×560 / 750×750（--with-tips）
├── 投稿清单.md            逐项校验结果 + 提交前自查清单
└── {专辑名}-微信投稿素材.zip
```

**关键参数**：
- `--raw-src` 封面/图标用的**无文字原图**目录；`--banner-src` 横幅与赞赏图用——官方要求横幅避免文字、图标去除文字与装饰
- `--showcase-style circle`（默认）：封面/图标/横幅/赞赏图用**圆形徽章**——奶白黏土主体与浅色背景色距过近，抠图必然掏洞，徽章方案零风险且暗夜模式必然可见
- `--outline auto`（默认）：封面/图标过浅（亮度 >185）自动加**同色系深色描边**
- **主图默认保留背景，不要加 `--transparent`**（浅色主体抠图会掏洞=审核驳回"没有填充颜色"）；高对比素材才用 `--transparent --showcase-style cutout`
- `--cover / --icon` 指定用哪张图；图标自动裁头部徽章，`--icon-span 0.44 --icon-cy 0.30` 微调取景
- 数量不在 8~24 会警告；每张超体积自动降色压缩
- 只校验不生成：`python scripts/wechat_pack.py --check ./wechat_submit`

**实测驳回案例 → 已内置的对策**（2026-09 真实审核反馈）：
| 驳回理由 | 对策 |
|---|---|
| 角色类型选错（"人物角色"→应选"宠物动物角色-兔"） | 投稿清单自查项第一条 |
| "角色形象没有填充颜色，暗夜模式下无法清晰辨识" | 根因=浅色主体抠图掏洞（白底看不出）→ 主图保留背景 + 封面/图标圆形徽章 + `--outline auto` |
| "聊天页图标展示位置小，去除不必要的文字信息和装饰" | 图标强制从无字原图生成、头部徽章放大占满、无装饰 |

---

## 7. 微信表情包投稿规格（官方，2026-09 核对）

| 素材 | 尺寸 | 格式 | 大小 | 特殊要求 |
|---|---|---|---|---|
| 表情主图 ×8~24 | 240×240 | PNG/JPG/GIF | ≤ 500KB/张 | 全套统一动/静态，各图情绪不重复 |
| 表情缩略图 | 120×120 | PNG | ≤ 500KB | — |
| 表情封面图 | 240×240 | PNG | ≤ 500KB | **必须透明底**，无白边无锯齿，避免文字 |
| 聊天面板图标 | 50×50 | PNG | ≤ 100KB | **必须透明底**，建议头部正面 |
| 详情页横幅 | 750×400 | JPG/PNG | ≤ 500KB | **避免任何文字**，避免白底与透明底，要有主题元素 |
| 赞赏引导图（可选） | 750×560 | GIF/PNG | ≤ 500KB | 色调活泼，元素不变形 |
| 赞赏致谢图（可选） | 750×750 | GIF/PNG | ≤ 500KB | 风格与表情一致 |

⚠️ 最常见的错误是把主图上限记成 100KB——官方是 **500KB**，只有聊天面板图标才是 100KB。
超出会被平台自动压缩裁剪，画质不可控。文件名 `01.png` … `24.png`，顺序即展示顺序。
完整审核红线见 [references/wechat-spec.md](references/wechat-spec.md)。

---

## 8. 成套排布经验（决定好不好用）

- **情绪配比**：正面 30% / 负面宣泄 40% / 摆烂摸鱼 20% / 节日祝福 10%。全做崩溃没人收藏。
- **前 3 张最关键**：商店按前几张决定是否下载，把最通用的"开心 / 无语 / 崩溃"放前面。
- **文案要短**：2–4 字最佳，`好耶`、`无语`、`摸了`、`在吗`。超过 6 字缩略图就看不清。
- **画风锁死**：整套的材质、打光、镜头、负向词四段必须逐字一致，一张改了整套就散。
- **一次只生成一只**：两只角色的对戏图会串味，分两次生成再拼。

---

## 9. 常见翻车与修法

| 症状 | 修法 |
|---|---|
| 手指变形 / 多出一只手 | 提示词已锁 `round mitten hands without visible fingers`；道具改"抱在怀里 / 夹在腋下" |
| 画风在套内漂移 | 检查材质/打光/镜头/负向词四段是否逐字一致 |
| 表情不到位 | 情绪描述扩成"眉 + 眼 + 嘴"三句分写 |
| 出现中文乱码字 | 提示词里绝不写文字需求，文案一律后期叠加 |
| 背景太乱 | 加 `simple clean solid color background, nothing else`，删多余场景词 |
| 太写实不够萌 | 提高 `chibi`、`toy-like` 权重，删掉写实材质词 |
| 缩到 48px 看不清 | 主体占比提到 80%，减少小道具 |

---

## 10. 打包与上传前自检

### 一键结构自检
```bash
python scripts/validate_pack.py
python scripts/validate_pack.py --zip ./zodiac-claymote.zip
```
会检查 10 类项目：SKILL.md 位置、frontmatter 必需字段、name 字符集与保留字、description 长度、正文行数、标准目录、文档引用完整性、无缓存文件、脚本语法、ZIP 是否多套一层目录。

### 打包注意事项（上传失败的头号原因）

1. **压缩文件夹内部的内容**，不是压缩文件夹本身 —— ZIP 打开后第一层就应该是 `SKILL.md`
2. 打包前删除 `__pycache__`、`.DS_Store`、临时文件
3. 跨平台请用 UTF-8 编码保存，ZIP 内文件名不要有乱码

PowerShell 打包示例：
```powershell
Compress-Archive -Path "zodiac-claymote\*" -DestinationPath "zodiac-claymote.zip" -Force
```

---

## 11. 不侵权自检（商用前必跑）

1. 提示词里**没有**任何在售 IP 名、角色名、作者名
2. 配色 / 五官 / 道具是原创设定，不是某个已知角色的招牌特征
3. 文案原创，没搬他人台词、歌词、影视梗
4. 画面无商标、无 Logo、无水印、无签名
5. 相似度三问：① 去掉生肖物种后还像某个 IP 吗？② 有某 IP 的招牌道具/动作吗？③ 陌生人会叫出某个已有 IP 的名字吗？
6. 中国商标网检索拟用角色名是否已注册

完整条款见 [LICENSE.md](LICENSE.md) 与 [DISCLAIMER.md](DISCLAIMER.md)。

---

## 12. 版本与授权

- 版本：v1.1.0（新增：水印清除、微信投稿素材一键生成、官方规范核对）
- 授权：限时免费商用，期限与范围见 [LICENSE.md](LICENSE.md)
- 免责：AI 生成内容需人工审核，风险由使用者承担，见 [DISCLAIMER.md](DISCLAIMER.md)
- 凭证：向平台/客户出示的原创声明模板见 [授权证书模板.md](授权证书模板.md)
