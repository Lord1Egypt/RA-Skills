---
name: text-cleaner-cli
description: 清理文本中的多余空格、空行和行尾空白。
category: text-processing
source_template: skillsmp_download/1/SKILL.md
---

# text-cleaner-cli

## 能力边界
- 只处理当前命令输入指定的数据，不做额外隐式操作。
- 不依赖交互式界面，全部通过命令行完成。

## 输入参数
- 按命令行参数传入，参数格式见下方步骤命令。

## 输出结果
- 生成命令输出（stdout）和对应输出文件（JSON/TXT）。

## 执行步骤（具体操作）
1. 在 skill 目录准备输入文件，例如 input.txt、data.json。
2. 运行命令： python main.py --input <file> --output <file>
3. 若命令失败，先执行 --help 查看参数，再修正参数重新执行。
4. 查看输出文件内容，确认字段和行数符合预期。
5. 记录本次命令和输出路径，便于后续复现。

## 验证命令
python main.py --input <file> --output <file> --help
