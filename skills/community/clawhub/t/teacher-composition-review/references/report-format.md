# 打印报告协议与命令

报告生成器只把模型已完成、老师需要交付的批改结果排版，不识别作文、不评分、不判断是否掌握，也不自动写成长档案。默认学生版不含教师诊断和练习参考答案；老师要求教师版时用不同文件名并加 `--teacher-copy`。

## 输入 ReportRequest

JSON 必须包含下列全部字段，不允许未知字段。没有亮点、明确问题或二稿时相应列表为空，不为了填表编造内容。只需短评的任务直接聊天交付，不强迫构造整份报告。

| 字段 | 内容 |
| --- | --- |
| `title` | 作文题目，未提供时写“题目未提供” |
| `grade_level` | 已确认整数 3～6，不允许猜测 |
| `composition_type` | 文体或“暂不确定” |
| `rating` | 固定四级之一；总体暂不能判断时为 `null` |
| `rating_reason` | 总体依据或暂不评级的原因 |
| `dimensions` | 按内容、结构、语言、规范顺序的四项，每项 `{name, rating, evidence}`；未判 `rating=null`，依据须说明限制 |
| `highlights` | `[{quote, reason}]`，原句与好在哪里 |
| `annotations` | `[{id, kind, location, quote, problem, revision, reason}]`；编号从 1 连续，类别为 correction 或 suggestion，提升建议最多五条 |
| `student_comment` | 面向学生的具体评语 |
| `focus` | 本次一至两个修改重点 |
| `exercise` | `{minutes, task, hint, success_criteria, teacher_reference}`，minutes 为整数 3～5，完成标准为非空文字数组 |
| `teacher_reference` | 教师诊断和教学建议，仅教师版包含 |
| `second_draft` | `[{goal, status, evidence, authorship}]`；状态和来源使用反馈与订正参考中的固定表述，无复查时为空 |

`ReportRequest` 与 `ReviewRecord` 是两种用途的协议，不能把报告整体写入档案。报告允许引用原句，是交付材料；即使输出在临时目录，也不保证平台不会保留，应只放用户本次要求的教学内容、不加入姓名学号等无关信息。

真实可运行的合成请求见 [report-request.json](../examples/report-request.json)。不要用合成样例替代老师提供的作文。坐标渲染与文档报告共用编号，但报告脚本不嵌入作文原图；实际逐页批注图与报告分别交付。

## 运行方式

**当前目录为本 Skill 所在目录**，使用环境允许写入的输出目录，报告请求和输出不能同名、符号链接别名或硬链接别名。以下为明确标注的合成样例演示：

```bash
# 默认 Markdown 学生版，只依赖 Python 标准库。
python3 scripts/build_report.py --request examples/report-request.json --output /tmp/composition-student.md
# A4 Word 学生版，只有用户需要 Word 且允许安装依赖时才安装 python-docx。
python3 scripts/build_report.py --request examples/report-request.json --output /tmp/composition-student.docx
# 教师专用版另用文件名，避免误把诊断和参考答案发给孩子。
python3 scripts/build_report.py --request examples/report-request.json --output /tmp/composition-teacher.docx --teacher-copy
```

Word 缺少 `python-docx` 时，生成同名 `.md` 文件并在 JSON 中给出 warning，不能用 `.docx` 后缀伪装 Markdown。其他生成错误返回 `status=error`、退出码 1；失败不覆盖旧文件。显式 `--format md|docx` 时，以实际格式修正输出后缀。

调用后检查退出码、JSON 的 `status`、实际文件与格式。只有成功且文件存在才交付 `[下载学生版批改报告](实际绝对路径)`；warning 非空时同步说明降级。无脚本执行能力则在聊天里给可复制文本，不能说已生成 Word。

A4 报告按内容自动分页，不保证一页内装下全部错误；Word 字体使用系统宋体，目标设备无该字体会由 Word 替代。老师可打开打印预览后调整，不捆绑字体。需要 PDF 时另用可用转换工具，不能把 Word 文件直接改后缀。
