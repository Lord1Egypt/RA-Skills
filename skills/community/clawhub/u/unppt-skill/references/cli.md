# 命令行参考（unppt 0.3.2）

## 语法

```bash
unppt <输入.pptx> [-o 输出] [选项]
unppt check <输入.pptx> [--json] [字体选项]   # 只检查字体，不写文件
```

- 不写 `-o` 时，在 pptx 旁边新建同名文件夹放产物（入口 `index.html`；`data` 形式是 `deck.json`）。
- 输入只支持 .pptx（OOXML zip 格式）。老的二进制 .ppt（或加密的 pptx）会报错"这是老格式的 .ppt 文件（或加密的 pptx），暂不支持"——先在 PowerPoint 里另存为 .pptx 再转码。
- 旧写法 `unppt convert <输入.pptx>` 仍可用（0.2.0 起可省略 `convert`）。
- 退出码：0 成功；1 转码错误 / `check` 发现必须处理的问题 / 文件读不出来；2 用法错误（此时打印版本和用法）。

## 全部选项

| 选项 | 取值 | 默认值 | 说明 |
|---|---|---|---|
| `-o`, `--out <路径>` | 文件或目录 | 见上 | `single`/`data` 是输出文件；`paged`/`pages` 是输出目录 |
| `--output <形式>` | `single` `paged` `pages` `data`（`html` 是 `single` 旧名） | `paged` | 产物形式；代码里 `convert()` 默认仍是 `single` |
| `--data` | 无 | 关 | 等同 `--output data` |
| `--fonts <目录>` | 目录 | 无 | 指定字体目录（递归读 `.ttf`/`.otf`/`.ttc`），同名压过默认字体包。可写多次 |
| `--system-fonts` | 无 | 关 | 也用本机系统/Office 私有字体，用到的字嵌入产物（注意商业字体授权） |
| `--no-default-fonts` | 无 | 关 | 不用默认字体包（调试用；字宽只能估算） |
| `--no-images` | 无 | 出图 | 不输出 `pic/`、`thum/`（`prop.json` 照常） |
| `--jobs <n\|auto>` | 正整数或 `auto` | `auto` | 出图线程数。`auto` 按 CPU 配额和可用内存（每线程约 400MB）取小；`1` 主线程 |
| `--inline-limit <字节>` | 数字 | `2097152` | 小于该大小的图片内联进 HTML（仅 `single`） |
| `--stats` | 无 | 关 | 结束时打印页数、用时、峰值内存 |
| `-q`, `--quiet` | 无 | 关 | 不显示进度和结果 |
| `-v` / `-h` | 无 | — | 版本 / 用法 |

## 四种产物形式对比

| 形式 | 图片 | 字体子集 | 音视频 | 主文件 |
|---|---|---|---|---|
| `single` | 小于 `inlineLimit`（默认 2MB）内联，其余 `media/` | 内联 | `media/` | `index.html` |
| `paged` | 全部 `media/` | `fonts/<别名>.<哈希>.js` | `media/` | `index.html` + `pages/<页号>.<哈希>.js` |
| `pages` | 同 `paged` | 同 `paged` | `media/` | 同 `paged`，另加 `page-001.html`… |
| `data` | 全部 `media/` | `fonts/<别名>.woff` | `media/` | `deck.json` |

`paged`/`pages` 每页数据用 `<script>` 标签按需加载（不用 `fetch`），所以 `file://` 双击打开也能用。

## 常用组合

```bash
# 最常用：按需加载，放网站或本地双击
unppt demo.pptx -o site/demo

# 自包含单文件 HTML（附件）
unppt demo.pptx -o out/index.html --output single

# 每页一个 HTML
unppt demo.pptx -o site/demo --output pages

# 先检查字体
unppt check demo.pptx

# 服务器：自备字体目录、不出图、安静模式
unppt demo.pptx -o out/index.html --fonts /opt/fonts --no-images -q

# 内存紧张：单线程出图并显示统计
unppt demo.pptx -o out/index.html --jobs 1 --stats

# 只要数据
unppt demo.pptx --data -o out/deck.json
```

## 输出怎么读

```text
转码中 12/12 页                                   ← 进度（stderr）
统计：12 页，用时 4.2 秒，峰值内存 310 MB         ← --stats 时
完成：12 页，用时 4.2 秒 -> D:\work\out\index.html
字体：                                            ← 有字体问题时，只列 ⚠ / ✗
  ✗ Webdings   第 3 页   符号字体没有嵌入，符号会显示成字母或方框：请在 PowerPoint 里勾选"将字体嵌入文件"
提示：……                                          ← 每条警告一行
```

## 字体检查：unppt check

```bash
unppt check <输入.pptx> [--json] [--fonts 目录]... [--system-fonts] [--no-default-fonts]
```

几秒出结果，不写任何文件。示例输出：

```text
字体检查：demo.pptx（共 12 页）
  ⚠ 楷体_GB2312  第 1 页   没有这个字体，按 Microsoft YaHei 替代（字形和换行可能和作者电脑上不同）
  ✓ 等线         第 1 页   排版按原字体，显示用 思源黑体（Noto Sans SC）
结论：0 个必须处理的问题（✗），1 个提醒（⚠）
```

结论含义：✓ 正常（嵌入 / 指定 / 默认字体包接管）；⚠ 替代（`substituted`，字形换行可能不同）或有无字体可显示的字；✗ 必须处理（`symbol-missing` 符号字体未嵌入、`missing` 连替代字体都没有）。`--json` 输出结构与 `checkFonts()` 返回值相同（字段见 `references/api.md` 第 3.8 节）。

## 字体机制速记

- 播放时**不用**观看者电脑上的字体：用到的每个字都做成字体子集打包进产物。
- 字体来源优先级：PPT 嵌入的 > `--fonts` 指定的 > 默认字体包 `@unppt/fonts`（思源黑体/宋体、霞鹜文楷、Carlito、Caladea、Liberation 等开源字体 + 457 个 Windows/Office 字体的度量数据）。
- 没嵌入的字体：排版按原字体度量（换行和 PowerPoint 一致），显示用对应开源字体（微软雅黑→思源黑体、Calibri→Carlito）。
- 符号字体：Wingdings 1~3 未嵌入时由字体包接管；Webdings、Symbol 等未嵌入会显示成字母/方框，`unppt check` 会提示作者嵌入。
