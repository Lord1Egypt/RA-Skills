# 番茄导出（MD→TXT）｜export-fanqie

> 脚本来自你本地的 `AI小说/tools/export_fanqie.py`，已适配本套件 `novels/书名/` 落盘结构。

## 何时用

章节已是 MD，要贴进番茄作家助手后台（只收纯文本）时。

## 命令

在项目根（或 skill 目录外、能指到 novels 的位置）：

```bash
python skillhub-wangwen-author-suite/scripts/export_fanqie.py --src novels/书名 --as-chapter
```

自定义输出与字数预警：

```bash
python …/export_fanqie.py --src novels/书名 --out novels/书名/番茄导出 --min-chars 1000
```

## 行为

- 去掉 `#` `**` `---` 等 MD 标记  
- `「」` → `“”`  
- 跳过 `00-大纲` / `01-人物` / `02-情绪` / `03-黄金开篇` / `000-进度`  
- 生成 `目录.txt` + 每章一个 txt  
- 不足 `--min-chars`（默认 1000）打印预警，不阻断导出  

## 与套件衔接（助手话术）

用户说「导出番茄」「MD转TXT」时：

1. 确认书目录 `novels/书名/`  
2. 给出上面命令（或代为执行，若环境有 Python）  
3. 指引：txt 粘贴正文，目录.txt 填章节标题  

## 不要放进 skill 包的

`tools/fix_punctuation.py` 等标点修复脚本——只服务你某次正文抢救，不是通用上架能力。
