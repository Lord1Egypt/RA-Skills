# 脚本文件模板

> 复制下方"脚本正文"段（第 5 行起）到自己的 `outputs/` 目录，按占位符填入即可。
> 本文件下面的"字段说明"和"命名规范"段不参与复制。

## 脚本正文（从这里开始复制）

## 短视频脚本：{title}

> 素材来源：{source}
> 素材编号：{material_id}
> 预估时长：{duration} 秒
> 平台建议：{platform}
> 画面建议：{visual_style}

---

### 钩子句（{hook_duration} 秒）

{hook_text}

### 展开（{body_duration} 秒）

{body_text}

### 收束 + 引流（{ending_duration} 秒）

{ending_text}

---

### 制作备注

- 钩子句类型：{hook_type}
- 同批轮换检查：{batch_hook_types}
- 需要画面素材：{visual_assets}
- 脱敏检查：{privacy_check}
- {creator_name} 已替换：{yes_no}

---

## 脚本正文结束（不复制以下内容）

## 字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `title` | 脚本标题 | "AI 帮我数口癖" |
| `source` | 素材来源 | "直播 2 01:10:37" |
| `material_id` | 素材库 ID | "material-shock-data" |
| `duration` | 预估总时长（秒） | 90 |
| `platform` | 目标平台 | "抖音" / "视频号" / "小红书" / "全平台" |
| `visual_style` | 画面风格 | "纯口播" / "配截图" / "配数据卡片" / "配 PPT" |
| `hook_duration` | 钩子句时长（秒） | 3-5 |
| `body_duration` | 展开段时长（秒） | 30-150 |
| `ending_duration` | 收束段时长（秒） | 5-10 |
| `hook_type` | 钩子类型 | "反直觉结论" / "炸弹数字" / "场景悬念" / "提问" / "对比冲突" |
| `batch_hook_types` | 本批已用钩子 | "反直觉结论、炸弹数字" |
| `visual_assets` | 需要的素材 | "数据卡片 ×3、口播字幕" |
| `privacy_check` | 脱敏检查 | "无第三方产品引用" / "需脱敏为有人做了 XX" |
| `creator_name` | 作者署名（替换占位符） | "你的名字" |

## 命名规范

- 文件名：`{material_id}-{title_slug}.md`
- 标题 slug：取核心关键词的拼音或英文短横线连接
- 编号必须与素材库对应，不能跳过
- 同一素材的备选角度脚本：追加 `-a` / `-b` / `-c` 后缀

**示例**：

```
material-shock-data-ai-tongue-count.md
material-method-min-loop-a.md
material-method-min-loop-b.md
```
