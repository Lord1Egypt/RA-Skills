# vRain Skill - 中文古籍刻本电子书制作工具

将 Markdown/纯文本古籍转换为古籍刻本风格的直排 PDF 电子书。

## 触发条件

用户要求制作古籍风格电子书、直排 PDF、古籍刻本时使用此 Skill。

---

## 重要声明

**本 Skill 依赖用户本地安装的 vRain 工具，不包含 vRain 代码。**

vRain 是一款面向读者的中文古籍刻本风格直排电子书制作工具。参考中文古籍雕版刻本制作过程，首先生成书叶背景图，根据行数、每行字数形成一个自右向左、自上而下的位置数组，然后把文本逐字打印到对应位置，打满一页、新建一页，直到所有文字处理完。

---

## 依赖说明

### 1.1 安装 vRain 工具

**必须先完成此步骤**：

```bash
# 克隆 vRain 仓库到本地
cd ~/GitHub
git clone https://github.com/shanleiguang/vRain.git

# 进入目录
cd vRain
```

vRain 仓库包含：
- `vrain.pl` - 主脚本
- `vrain_mr.pl` - 多栏版本（族谱、古籍字典）
- `fonts/` - 字体文件
- `canvas/` - 背景图
- `books/` - 书籍配置样例
- `tools/` - 辅助工具

### 1.2 安装 Perl 依赖

```bash
# 使用 cpanm 安装（推荐）
cpanm PDF::Builder Font::FreeType Math::Trig Image::Magick

# 或使用系统 Perl + cpan
sudo cpan PDF::Builder Font::FreeType Math::Trig Image::Magick
```

### 1.3 准备字体文件

字体文件自行下载，存入 vRain 仓库的 `fonts/` 目录中：

| 推荐字体 | 用途 |
|---------|------|
| qiji-combo.ttf | 主字体，令东奇侪体 |
| HanaMinA.ttf / HanaMinB.ttf | 辅字体，花园明朝体 |

### 1.4 准备背景图

背景图在 vRain 仓库的 `canvas/` 目录中（.jpg + .cfg 文件）。

---

## Skill 调用方式

### 调用方式

本 Skill 作为命令行包装器，调用用户本地安装的 vRain 工具。

**工作目录**：`~/GitHub/vRain/`

### 核心命令

```bash
perl vrain.pl -b <书籍ID> [-f <起始序号>] [-t <结束序号>] [-c] [-z <页数>]
```


| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `-b` | 是 | 无 | 书籍ID，对应 `books/<ID>/` 目录 |
| `-f` | 否 | 1 | 起始卷/章回号（对应 text/ 目录下的文件名编号） |
| `-t` | 否 | 最后 | 结束卷/章回号（对应 text/ 目录下的文件名编号） |
| `-z` | 否 | 无 | 测试模式，仅输出指定页数，用于调试排版参数 |
| `-c` | 否 | 自动添加 | 压缩 PDF（MacOS） |
| `-h` | 否 | 无 | 显示帮助信息 |
| `-v` | 否 | 无 | 显示更多信息 |

```bash
# 方式1: 使用 wrapper（推荐）
vrain -b 01                  # 制作整本书
vrain -b 01 -f 1 -t 10      # 制作第1~10回
vrain -b 01 -z 3            # 测试输出前3页

# 方式2: 直接调用 perl 脚本
cd ~/GitHub/vRain
perl vrain.pl -b 01 -c      # 制作整本书
perl vrain.pl -b 01 -z 10   # 测试输出前10页
perl vrain.pl -b 01 -f 11 -t 20 -c  # 制作第11~20回
perl vrain.pl -h             # 查看帮助
```

---


## 批量制作与工作流

### 标准工作流：先测试，后批量

```bash
# 第1步：查看书籍有多少回/卷
ls books/01/text/*.txt | wc -l

# 第2步：测试前几页，确认排版效果
vrain -b 01 -z 3

# 第3步：确认效果OK后，批量制作
vrain -b 01                  # 制作全部（或指定范围）
```

### 常见用法

```bash
# 制作前10回
vrain -b 01 -f 1 -t 10

# 制作第11~20回（增量追加）
vrain -b 01 -f 11 -t 20

# 重新制作某几回（覆盖已有）
vrain -b 01 -f 5 -t 8
```

### 批量制作多本书

```bash
# 顺序制作（等待完成再下一本）
for book in 聊斋志异 儒林外史 醒世恒言; do
    echo "=== 制作《$book》 ==="
    vrain -b "$book"
done
```

### 输出说明

- PDF 文件输出到 `PDF/` 目录
- 文件名格式：`《书名》文本序号.pdf`

## 书籍配置

### 目录结构

在 `books/<书籍ID>/` 目录下创建以下文件：

```
books/<书籍ID>/
├── book.cfg          # 书籍配置文件（必需）
├── cover.jpg         # 封面图（可选）
└── text/
    ├── 01.txt        # 第1回
    ├── 02.txt        # 第2回
    └── ...
    # 或多位数如 001.txt, 002.txt ... 10.txt, 11.txt ...
```

### book.cfg 配置项

```ini
# 基础信息
title=书名
author=作者

# 背景图 ID（对应 canvas/ 目录）
canvas_id=24_paper
row_num=30           # 每列字数
row_delta_y=10       # 列末到边框距离

# 字体配置
font1=qiji-combo.ttf
font2=HanaMinA.ttf
font3=HanaMinB.ttf

# 正文字体大小
text_fonts_array=123
text_font1_size=60
text_font2_size=42
text_font3_size=42
text_font_color=black

# 封面配置
cover_title_font_size=120
cover_title_y=200
cover_author_font_size=60
cover_author_y=600
cover_font_color=black

# 版心标题
title_font_size=80
title_y=1200
title_postfix=卷X   # 卷号后缀，置空则不显示

# 页码
pager_font_size=35
pager_y=500

# 标点处理
if_onlyperiod=1     # 归一化为句号
```

---

## vRain 功能特性

- **书叶背景图**：书房名、尺寸、列数、框线粗细及颜色均可配置。支持单双、顺对、黑白鱼尾。
- **风格背景图**：支持生成宣纸做旧风格、竹简风格的背景图。
- **批注文字**：支持小字双排。正文、批注文字的字体、大小、颜色、位置可配置。
- **位置微调**：正文文字、批注文字、标点符号的上、下、左、右位置均可微调。
- **多字体支持**：一主多辅字体，主字体不支持时自动采用辅助字体补字。
- **标点处理**：标点符号替换规则、过滤规则可配置。标点符号可归一化为句号。
- **书名号**：书名号、单双引号直排旋转九十度。可调整为侧边线。
- **目录生成**：根据文本序号自动生成 PDF 目录，如第x回、卷x。
- **保留字符**：
  - `@` - 代表空格
  - `【】` - 内代表双排批注文字
  - `%` - 换叶符
  - `&` - 换页符（半叶）
  - `&` - 下行文字居叶末
  - `S+数字` - 文本行首代表整段缩几个字符

---

## 背景图制作

生成古籍刻本风格的背景图（书叶边框、鱼尾、宣纸纹理等）。

### 触发条件

用户要求制作古籍背景图、生成书叶边框、创建宣纸风格背景时使用此功能。

### 背景图脚本

背景图脚本位于 `canvas/` 目录：
- `canvas.pl` - 主要背景图生成脚本
- `vintage.pl` - 宣纸做旧风格背景图脚本
- `bamboo.pl` - 竹简风格背景图脚本

### 工作目录

**工作目录**：`~/GitHub/vRain/canvas/`

### 核心命令

```bash
perl canvas.pl -c <背景图ID>
perl vintage.pl -c <背景图ID>
perl bamboo.pl -c <背景图ID>
```


| 参数 | 必填 | 说明 |
|------|------|------|
| `-c` | 是 | 背景图ID，对应配置文件名（不含.cfg后缀） |
| `-h` | 否 | 显示帮助信息 |

### 背景图配置

#### 配置目录结构

在 `canvas/` 目录下创建配置文件（.cfg）和输出文件：

```
canvas/
├── <背景图ID>.cfg       # 配置文件（必需）
├── <背景图ID>.jpg       # 生成的背景图（输出）
└── ...
```

#### 基础配置项 (canvas.cfg)

```ini
# 画布尺寸
canvas_width=1485
canvas_height=2100
canvas_color=#f5f5dc    # 背景颜色（如米色）

# 页边距
margins_top=150
margins_bottom=150
margins_left=150
margins_right=150

# 版心配置
leaf_col=2              # 列数（1=单栏，2=双栏）
leaf_center_width=80    # 中间框线宽度

# 外框线
outline_width=8
outline_color=#333333

# 内框线
inline_width=2
inline_color=#666666

# 框线边距
outline_hmargin=30
outline_vmargin=30
```

#### 鱼尾配置项

```ini
# 鱼尾类型
fish_top_y=200              # 上鱼尾Y坐标
fish_top_color=#333333      # 上鱼尾颜色
fish_top_rectheight=80      # 上鱼尾身长
fish_top_triaheight=40      # 上鱼尾尾长
fish_top_linewidth=3        # 上鱼尾线宽

fish_btm_y=1900             # 下鱼尾Y坐标
fish_btm_color=#333333      # 下鱼尾颜色
fish_btm_direction=0        # 0=顺鱼尾，1=对鱼尾
fish_btm_rectheight=80      # 下鱼尾身长
fish_btm_triaheight=40      # 下鱼尾尾长
fish_btm_linewidth=3        # 下鱼尾线宽
```

#### 花鱼尾配置项

```ini
# 花鱼尾（装饰性鱼尾）
if_fishflower=1
fish_flower_image=cloud.png  # 花鱼尾装饰图（正方形，内容居中）
```

#### 宣纸背景配置项

```ini
# 宣纸背景图（可选，使用背景图替代纯色）
canvas_background_image=../images/paper texture.jpg
```

#### Logo/印章配置项

```ini
# 版心底部书房名
logo_text=兀雨书屋
logo_y=2000
logo_color=#333333
logo_font=...
logo_font_size=36

# 或使用印章图片
logo_image=../images/seal.png
```

#### 多栏模式配置项（族谱/字典）

```ini
# 多栏模式
if_multirows=1
multirows_num=4             # 栏数
multirows_linewidth=1       # 分栏线宽
multirows_colcolor=#cccccc  # 栏线颜色
```

### 预设背景图

vRain 仓库提供预设背景图：

| ID | 风格 | 说明 |
|----|------|------|
| `simple` | 极简 | 简约无框线 |
| `24_paper` | 宣纸 | 24cm 宣纸做旧风格 |
| `20_paper` | 宣纸 | 20cm 宣纸风格 |
| `28_paper` | 宣纸 | 28cm 大幅宣纸 |
| `vintage` | 做旧 | 复古宣纸纹理 |
| `bamboo` | 竹简 | 竹简风格 |
| `18_blue` | 蓝框 | 18cm 蓝框单栏 |
| `18_red` | 红框 | 18cm 红框单栏 |
| `24_black` | 黑框 | 24cm 黑框双栏 |
| `mr_4` | 多栏 | 4栏族谱模式 |
| `mr_5` | 多栏 | 5栏族谱模式 |

### 背景图使用示例

#### 1. 使用预设背景图

```bash
cd ~/GitHub/vRain/canvas

# 查看预设背景图
ls -la *.jpg *.cfg

# 使用宣纸背景
perl canvas.pl -c 24_paper
```

#### 2. 创建自定义背景图

```bash
# 1. 复制预设配置作为模板
cp 24_paper.cfg mybook.cfg

# 2. 编辑配置
vim mybook.cfg

# 3. 生成背景图
perl canvas.pl -c mybook
```

#### 3. 使用宣纸做旧风格

```bash
# 使用 vintage.pl 生成宣纸做旧背景
perl vintage.pl -c 24_paper
```

#### 4. 使用竹简风格

```bash
# 使用 bamboo.pl 生成竹简背景
perl bamboo.pl -c bamboo
```

### 常见问题

#### Q: 背景图尺寸如何选择？

- **A5尺寸（18cm）**：适合短篇、单本书
- **A4尺寸（24cm）**：适合普通古籍
- **A3尺寸（28cm）**：适合大幅展示或长篇巨著

#### Q: 如何制作宣纸效果？

```ini
# 选项1：使用预设
canvas_id=24_paper

# 选项2：自定义宣纸背景
canvas_background_image=../images/paper_texture.jpg
```

#### Q: 鱼尾是什么？

鱼尾是古籍版心中间的装饰性线条，形状像鱼尾。有：
- **顺鱼尾**：上下鱼尾方向一致
- **对鱼尾**：上下鱼尾方向相对
- **花鱼尾**：带装饰图案的鱼尾

---

## 辅助工具

### 添加印章

使用 `addyin.pl` 添加电子印章：

```bash
# 复制到书籍目录
cp tools/addyin.pl books/01/

# 运行
cd books/01
perl addyin.pl

# 参数说明
# -s 藏书章位置（左上/右上）
# -p 页码印章（默认启用）
```
---

## 错误处理

### 常见错误及解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `未发现该书籍目录'books/xxx'` | 书籍ID不存在 | 确认 `books/<ID>/` 目录存在 |
| `未发现该书籍文本目录` | text/ 目录不存在 | 创建 `books/<ID>/text/` 目录 |
| `未发现该书籍排版配置文件` | book.cfg 不存在 | 创建 `books/<ID>/book.cfg` |
| `未发现字体'fonts/xxx'` | 字体文件缺失 | 将字体文件放入 fonts/ 目录 |
| `未发现背景图jpg图片文件` | 背景图缺失 | 将 canvas/*.jpg 和 *.cfg 放入 canvas/ |
| `Can't locate XXX.pm` | Perl 模块未安装 | `cpanm PDF::Builder Font::FreeType Math::Trig Image::Magick` |


## 相关项目

| 项目 | 说明 | 仓库 |
|------|------|------|
| vRain | 古籍刻本电子书制作 | https://github.com/shanleiguang/vRain |
| vYinn | 古籍印章制作 | https://github.com/shanleiguang/vYinn |
| vQi | 围棋棋谱转古棋谱图 | https://github.com/shanleiguang/vQi |
| vModou | 古籍扫描图像变形纠正 | https://github.com/shanleiguang/vModou |
| vBorder | 摄影作品边框 | https://github.com/shanleiguang/vBorder |

---
