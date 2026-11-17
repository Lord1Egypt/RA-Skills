# 真题试卷转题库（exam-bank-convert）v1.4.0

把历年真题原卷（PDF / 图片）转成 **17 列表头**的题库 Excel：OCR → 语义抽取 → 写表 → 漏题自检。

## 一、安装

把 `exam-bank-convert/` 整个目录拷进你的 AI 客户端技能目录即可，例如：

| 客户端 | 技能目录 |
|---|---|
| WorkBuddy | `~/.workbuddy/skills/exam-bank-convert/` |
| Cursor | `~/.cursor/skills/exam-bank-convert/` |
| Trae | `~/.trae-cn/skills/exam-bank-convert/` |
| CodeBuddy | `~/.codebuddy/skills/exam-bank-convert/` |
| 其它 | 任意位置，调用脚本时写全路径 |

## 二、准备（两件事，都必须有）

1. **OCR 服务地址**：本技能需要一个 exam-ocr 服务（提供 `/parse-async`、`/task/{id}`、`/write-excel` 接口）。
   设置环境变量指向它（**按你自己的服务地址填，本包不含默认地址**）：

   ```bash
   export EXAM_OCR_URL="http://<你的服务IP>:8000"
   ```

2. **Python**：3.6+ 即可，脚本只用标准库（`auto_run.py` 需要额外 `pip install requests`）。

## 三、归档目录（可选，自己决定）

**本技能不内置任何固定归档路径。** 想归档就给路径，不想归档就不给（自动跳过，不影响主流程）：

```bash
# 方式1：每次调用时指定
python archive.py 题库.xlsx 原卷.pdf --to "<你的归档目录>" --subject "15044马克思主义基本原理"

# 方式2：设一次环境变量，之后省略 --to
export EXAM_BANK_ARCHIVE_DIR="<你的归档目录>"
```

归档目录可以是本地文件夹、NAS 挂载盘、网盘同步目录、项目目录——随便哪里。

## 四、使用

- **方式 A（推荐）**：让 AI 自己读 OCR 文本做抽取，不需要任何 LLM key。见 `SKILL.md` 的「方式 A」。
- **方式 B（一键脚本）**：需要 DeepSeek key（用你自己的）：

  ```bash
  DEEPSEEK_API_KEY=sk-xxx python auto_run.py <试卷.pdf> <输出.xlsx> \
      --course 马克思主义基本原理 --year 2026 --month 4 \
      --url "$EXAM_OCR_URL"
  ```

  年份列会写成 `2026年4月` 格式（同课程同年 4 月 / 10 月两套卷能区分）。

## 五、输出表头（17 列，与题库系统模板一致）

```
课程 | 知识点 | 题型 | 题目内容 | 选项A | 选项B | 选项C | 选项D | 选项E
正确答案 | 难度 | 状态 | 是否真题 | 是否模拟试卷 | 是否考前押题 | 年份 | 解析
```

- **年份**：填具体考期 `2026年4月`
- **解析**：必填，客观题写正确项依据 + 干扰项错因，主观题写得分要点
- **知识点**：必填

## 六、文件清单

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 技能说明（AI 读这个） |
| `parse_ocr.py` | 调 OCR 服务出 Markdown（异步排队，`--owner` 区分调用方，`--sync` 可退回同步） |
| `write_excel.py` | 把抽取 JSON 写成 17 列 xlsx |
| `check_missing.py` | 漏题自检（题号连续性校验，退出码 1 = 缺题） |
| `auto_run.py` | 一键跑（可选，需 DeepSeek key） |
| `archive.py` | 产物归档（可选，路径自己给） |
