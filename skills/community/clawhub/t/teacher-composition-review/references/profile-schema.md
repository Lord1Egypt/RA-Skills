# 批注与成长档案协议

本文件定义跨平台共用的数据协议。后续脚本、测试和便携档案必须使用完全相同的字段名；日期使用 `YYYY-MM-DD`，数组顺序保持输入或显示顺序。`AnnotationRequest.source_image`、`output_image` 与可选 `font_path` 使用绝对路径；档案 CLI 的 JSON 文件参数可使用 `store_dir` 内的相对路径。

## AnnotationRequest

`AnnotationRequest` 是单页批注渲染请求。仅在已获得可靠坐标时创建；`items` 按全篇连续编号排序。

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `source_image` | string | 原始作文图片的绝对路径。 |
| `output_image` | string | 批注输出图片的绝对路径；解析后不得与原图相同，也不得是指向原图的符号链接或文件别名。 |
| `font_path` | string（可选） | 需指定字体时使用；必须是已存在、可加载且支持中文字形的字体文件绝对路径。显式字体无效或不支持中文时直接拒绝，不回退到其他字体。仅当不指定时，才由脚本从 macOS、Linux 和 Windows 常见系统字体中安全选择；Skill 不捆绑版权字体。 |
| `items` | AnnotationItem[] | 当前页待绘制的批注项目。 |

JPEG 先按 EXIF orientation 归一化为人眼所见方向，然后再校验尺寸和绘制。平台视觉识别、OCR 及 `bbox` 必须使用同一个 **EXIF 归一化后的视觉坐标系**，不得使用 JPEG 底层未旋转存储坐标。RGBA PNG 的原图区域保留 RGBA 像素与 alpha，批注以可见覆盖层正确合成；输出仍统一为 PNG。

## AnnotationItem

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `id` | integer | 全篇唯一、从 1 起连续的编号。 |
| `kind` | string | 问题类别；至少可使用 `correction`（明确纠错）与 `suggestion`（提升建议）。 |
| `bbox` | integer[4] | `[left, top, right, bottom]` 像素坐标；必须在原图边界内，且 `right > left`、`bottom > top`。 |
| `message` | string | 面向老师的简明说明；不覆盖原图文字。 |
| `confidence` | number | `0` 至 `1` 的坐标与识别综合置信度；不足可靠阈值时不渲染，改为文字清单。 |

## TeacherSettings

`TeacherSettings` 保存教师长期偏好。单次批改覆盖项不写回本结构。

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `grade_levels` | integer[] | 任教年级，可选值仅为 `3`、`4`、`5`、`6`。 |
| `revision_level` | string | `minimal`、`moderate` 或 `developmental`。 |
| `comment_style` | string | `gentle`、`professional`、`humorous` 或 `concise`。 |
| `ratings` | string[] | 固定为 `["优秀", "良好", "合格", "待提高"]`。 |
| `profile_enabled` | boolean | 是否启用学生成长档案。 |
| `privacy_notice_confirmed` | boolean | 是否已告知档案内容、确认机制和默认隐私规则。 |

`profile_enabled=false` 时，调用方必须完全跳过历史读取、学生建档、档案摘要确认、写入及便携导入/导出；每次调用 `create`、`append`、`update-review`、`import` 或 `export` 前都应重新检查该值。

## ReviewRecord

`ReviewRecord` 是一篇作文最终确认后的教学摘要。未确认的草稿不得写入 `StudentProfile.review_records`。

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `review_id` | string | 唯一批改编号，如 `2026-08-13-001`。 |
| `date` | string | 批改日期，格式 `YYYY-MM-DD`。 |
| `title` | string | 作文题目；不明时先确认。 |
| `composition_type` | string | 作文类型，如“记事”。 |
| `grade_level` | integer | 本篇所属年级，只能为 `3`、`4`、`5`、`6`。 |
| `rating` | string | `优秀`、`良好`、`合格`、`待提高`之一。 |
| `dimension_ratings` | object | 必需且只能包含 `content`、`structure`、`language`、`conventions`；每个值都是固定四级之一。 |
| `strengths` | string[] | 本次可记录的优点或进步。 |
| `recurring_issues` | string[] | 本次仍出现的高频或持续问题。 |
| `next_goals` | string[] | 下一篇重点目标，通常 1～2 项。 |

## StageSummary

`StageSummary` 是详细记录超过 10 条时形成的结构化教学摘要。它不保存题目、日期、原文或图片路径，也不把数组拼成展示文本，避免合法标点改变数据边界。

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `rating` | string | `优秀`、`良好`、`合格`、`待提高`之一。 |
| `strengths` | string[] | 被压缩记录中的优点或进步，逐项原文保留。 |
| `recurring_issues` | string[] | 被压缩记录中的持续问题，逐项原文保留。 |
| `next_goals` | string[] | 被压缩记录中的下一步目标，逐项原文保留。 |

## StudentProfile

`StudentProfile` 以 `class_name` 与 `student_name` 共同识别，不得因同名自动合并。默认不保存原图、完整正文、未确认 OCR 内容或无关个人信息。

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `student_name` | string | 已由老师确认的学生姓名。 |
| `class_name` | string | 已由老师确认的班级。 |
| `current_grade_level` | integer | 当前年级，只能为 `3`、`4`、`5`、`6`；追加或修正后更新为最新详细记录的 `grade_level`。 |
| `created_date` | string | 建档日期，格式 `YYYY-MM-DD`。 |
| `feedback_preferences` | string[] | 个性化反馈偏好，例如更多鼓励或更简洁。 |
| `review_records` | ReviewRecord[] | 最近最多 10 次详细、已确认的批改摘要。 |
| `used_review_id_hashes` | string[] | 所有已使用 `review_id` 的 SHA-256 指纹；详细记录压缩或删除后仍保留，用于防止编号重用，不保存原始编号。 |
| `stage_summaries` | StageSummary[] | 超过 10 次详细记录后按时间顺序形成的结构化阶段总结；字符串旧格式视为不兼容或损坏。 |
| `dimension_trends` | object | 且仅含 `content`、`structure`、`language`、`conventions`；每维是最近 10 个 `{date, rating}` 对象的有序列表。 |
| `recurring_issues` | string[] | 跨记录仍反复出现的问题。 |
| `documented_progress` | string[] | 相对历史记录已体现的进步。 |
| `current_goals` | string[] | 最新剩余详细记录的 `next_goals`，稳定去重后最多 2 项；没有任何详细记录时，才回退到最新 `StageSummary.next_goals`。 |

详细记录压缩为 `StageSummary` 时不复制四维评级；`dimension_trends` 单独保留最近 10 次。缺少 `dimension_ratings`、使用 `basic_norms` 或使用字符串趋势的早期开发分支档案明确拒绝，不猜测或自动补值。v1.1.0 保留正式版档案字段和格式，二稿结果以教学摘要写入既有字段，不增加正文、练习答案或图片路径。

## 规范示例

以下示例固定展示 `annotation_request` 与 `review_record` 的字段形状：

```json
{
  "annotation_request": {
    "source_image": "绝对图片路径",
    "output_image": "绝对输出路径",
    "items": [
      {
        "id": 1,
        "kind": "correction",
        "bbox": [100, 120, 220, 160],
        "message": "‘的’改为‘地’",
        "confidence": 0.98
      }
    ]
  },
  "review_record": {
    "review_id": "2026-08-13-001",
    "date": "2026-08-13",
    "title": "难忘的一天",
    "composition_type": "记事",
    "grade_level": 4,
    "rating": "良好",
    "dimension_ratings": {
      "content": "良好",
      "structure": "良好",
      "language": "合格",
      "conventions": "合格"
    },
    "strengths": ["事情经过完整"],
    "recurring_issues": ["的地得混用"],
    "next_goals": ["增加动作细节"]
  }
}
```

## 写入与便携档案

仅在老师确认摘要后写入档案。长期存储不可用或写入失败时，导出包含 `schema_version`、`teacher_settings` 和 `student_profile` 的便携档案文件；已确认记录位于 `student_profile.review_records`，顶层**不**存在 `review_record`。导入与导出均以便携对象、`TeacherSettings`、`StudentProfile`、`ReviewRecord` 和 `StageSummary` 各层的严格字段白名单与类型校验作为隐私边界；`source_image`、`output_image`、`full_text`、`path` 等未知字段都因 schema 被拒绝。题目、优点、问题、目标和反馈偏好等已允许自然语言字段不按其文字是否像本地路径而拒绝，并必须原文保留。任何校验失败均不覆盖既有导出文件；明确告知老师保存该文件并在下次上传。仅当 `profile_enabled=true` 才能导出或导入。

## 本地档案 CLI 协议

档案脚本为 `python3 scripts/manage_profiles.py --store-dir STORE_DIR <子命令>`。`STORE_DIR` 是唯一的本地数据边界；`settings-set` 的 `--settings`、`create` 的可选 `--feedback-preferences`、`append` 与 `update-review` 的 `--review` 以及 `import` 的 `--input` 都必须指向其中的 JSON 对象文件。不要使用不存在的 `--review-file` 参数，也不要从存储目录外读取 JSON。

| 子命令 | 必要参数 | 确认门槛与结果 |
| --- | --- | --- |
| `settings-set` | `--settings SETTINGS_JSON` | 设置必须包含本协议规定的六个 `TeacherSettings` 字段，且 `privacy_notice_confirmed` 为 `true`。 |
| `settings-get` | 无 | 返回当前完整教师设置。 |
| `create` | `--class-name`、`--student-name`、`--grade-level` | 必须加 `--confirmed`，才创建新档案。 |
| `get` | `--class-name`、`--student-name` | 返回指定班级与姓名的档案。 |
| `append` | `--class-name`、`--student-name`、`--review REVIEW_JSON` | 必须加 `--confirmed`，只写入已确认的 `ReviewRecord`。 |
| `update-review` | `--class-name`、`--student-name`、`--review-id`、`--review REVIEW_JSON` | 必须加 `--confirmed`；`review_id` 必须精确存在于详细记录，替换对象的 `review_id` 必须与目标一致，已压缩记录不可修正。保留全部已用 ID 指纹并原子重建派生字段。 |
| `delete-review` | `--class-name`、`--student-name`、`--review-id` | 仅接受精确存在的 `review_id`；删除后该编号仍不可重用。 |
| `delete-profile` | `--class-name`、`--student-name` | 必须加 `--confirm-delete`，才删除整份档案。 |
| `export` | `--class-name`、`--student-name`、`--output` | 输出路径同样必须位于 `STORE_DIR` 内；导出 JSON 含 `schema_version`、`teacher_settings` 和 `student_profile`。 |
| `import` | `--input PORTABLE_JSON` | 必须加 `--confirmed`；完整校验便携 JSON、设置和档案后恢复。若同名档案存在，默认拒绝；仅 `--confirmed --overwrite` 才会原子覆盖。 |

`render_annotations.py` 的唯一 CLI 参数是 `--request REQUEST_JSON`。请求中的 `source_image` 与 `output_image` 均为绝对路径且不得指向同一文件；原图仅支持 PNG、JPG、JPEG，输出必须为 PNG。`confidence` 低于 `0.80` 或视觉坐标越界时，不调用渲染器，改用编号文字清单。
