---
name: resume-review
description: "秋招简历毒舌测评,生成 JOJO 替身面板图。"
version: 2.0.0
author: padepa
license: MIT
platforms: [linux, macos, windows]
tags: [resume, 秋招, jojo, meme, image]
---

# 简历评测 (Qiuzhao Resume Roast)

把一份简历测评成「JOJO 替身面板」:六维能力值雷达图(排版/教育/实习/项目/技能/
亮点)+ 评级字母(A-E)+ 毒舌替身名 + 替身能力判词,渲染成一张 1200×1600 PNG,
适合发社交媒体。

本 skill 是**通用流程**,任何 AI 助手、任何用户、任何平台都能执行:不依赖特定
agent 系统、不依赖特定操作系统。测评由 AI 完成,渲染脚本只需要 Python + Pillow。

## When to Use

- 用户说「测评一下我的简历 / 秋招简历帮我看看 / 把我的简历做成替身面板」
- 用户想发「简历测评」类社交媒体内容(面板图轻量,可直接发图)

Don't use for: 正经简历改写/求职文档(那是 `resume-development` 的活);
不涉及面板图的单纯简历问答(直接答即可)。

## Prerequisites

- Python 3.10+ 与 [uv](https://docs.astral.sh/uv/)(脚本经 `uv run --with pillow` 运行;
  无 uv 时 `pip install pillow` 后直接 `python scripts/render_stand.py` 也可)
- 系统 CJK 字体(脚本自动按平台查找 macOS/Windows/Linux 字体;失败用 `--font` 指定)
- 无需网络(除了 AI 测评那一步)

## How to Run

```bash
# 渲染(测评数据 JSON -> 面板图 PNG)
uv run --with pillow python scripts/render_stand.py panel.json 面板.png [--font 字体]
```

输入格式见 `templates/panel_template.json` 与 `references/roast-prompt.md`。

## Procedure

1. **读简历。** 读取用户提供的简历文件(PDF/DOCX/TXT)。外部用户可用
   `scripts/extract_resume.py` 提取文本(需要 pymupdf/python-docx):
   `uv run --with pymupdf --with python-docx python scripts/extract_resume.py 简历.pdf -o resume.txt`
2. **匿名化(发社交媒体的硬性前提)。** 姓名→花名,手机/邮箱/微信/身份证→删除,
   具体公司名→「某厂」,学校→「某985/某双非/某本科」。写入 JSON 前完成。
3. **按维度打分。** 读 `references/humor-style.md` 的评分表与梗库
   (排版/教育/实习/项目/技能/亮点,满分 100),记下每个维度的**真实**槽点。
4. **写测评数据 JSON。** 参考 `templates/panel_template.json`:persona(花名·身份)、
   stand_name(毒舌替身名,≤8字)、total_score、verdict(判词)、ability(替身能力
   描述:毒舌+一条建议,≤50字)、dimensions(6 维 score/max)。
   规则见 `references/humor-style.md`;也可用 `references/roast-prompt.md` 的提示词
   让任何 LLM 生成 JSON。用文件写入工具存盘。
5. **渲染。** 运行 `render_stand.py`,输出 PNG。
6. **验证。** 打开图片确认:六边形雷达图完整、文字无溢出、评级字母正确。
   发现问题就回到第 4 步改 JSON 再渲染。
7. **交付。** 把 PNG 文件给用户(以文件形式发送),附 2-3 句「真·修改建议」摘要。

## Quick Reference

- 渲染:`uv run --with pillow python scripts/render_stand.py <panel.json> <out.png>`
- 提取文本:`uv run --with pymupdf --with python-docx python scripts/extract_resume.py <简历> -o resume.txt`
- 评级规则:A(90+) B(75-89) C(60-74) D(45-59) E(<45)
- 无 uv 的替代:`pip install pillow && python scripts/render_stand.py panel.json out.png`

## Pitfalls

- **PYTHONPATH 污染(部分桌面 agent 环境):** 某些 AI 桌面应用会向子进程注入
  PYTHONPATH,导致 `uv run` 加载到错误环境的 PIL。出现 `OSError: cannot open
  resource` 时,用 `env -u PYTHONPATH uv run --with pillow ...` 重跑即可。
- **字体:** 自动查找链覆盖 macOS(STHeiti/PingFang/Songti)、Windows(msyh/simhei)、
  Linux(Noto/wqy);找不到时 `--font` 指定任意 CJK TTF/TTC。
- **文字溢出:** ability ≤50 字、stand_name ≤8 字、verdict ≤10 字是排版安全线,
  超了文字会挤或截断。
- **隐私红线:** 不匿名就发图 = 事故。姓名/联系方式/公司名必须处理。脚本不自动打码。
- **dimensions 必须 6 项**,顺序固定(排版/教育/实习/项目/技能/亮点),否则报错。

## Verification

- 渲染脚本 exit 0 且打印 `完成: <out.png> 1200x1600 评级 X`
- 打开 PNG:米黄底、顶部黑条 STAND STATS、红色六边形雷达图、评级字母、底部判词
- 六维顶点标签与分数与 JSON 一致
