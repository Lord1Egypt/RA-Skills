---
name: xhs-note-gen
description: 小红书笔记生成服务，当用户要求"生成小红书笔记/小红书文案/笔记"并希望通过 小念AI来 生成结果而不是手动编写时使用。
---

# xhs-note-gen

Use this skill to generate XiaoHongShu (小红书) notes via external API.

## Prereqs

1) The service is running on:
- `https://xiaonian.cc/employee-console/dashboard/v2/api`

2) Endpoint
- Uses **one-shot** endpoint: `POST /content/quick-note/generate`
- **No auth required**

## Workflow

1) Convert the user request into:
- `task_description`: the user’s requirement (keep it verbatim, add constraints if provided)
- Defaults (unless user specifies):
  - `audience`: 小红书用户
  - `tone`: 友好自然
  - `character`: 专业分享者
  - `generate_num`: 默认 1（只生成 1 篇笔记；如需多版备选再改成 2/3）

2) Run the script (calls quick-note; `--generate-num` 表示生成“多篇不同版本的文案备选”；
图片数量用 `--image-num` 控制，不需要用 generate-num 来换图片张数):

```bash
python3 skills/local/xhs-note-gen/scripts/xhs_note_gen.py \
  --task-description "<task_description>" \
  --audience "<audience>" \
  --tone "<tone>" \
  --character "<character>" \
  --generate-num 3
```

Optional controls:
- Disable images: `--no-generate-image`
- Change image count (default 1): `--image-num 3`
- Set note type explicitly (optional): `--note-type "工具测评类"`

3) The script prints JSON containing:
- `notes[]` with `title`, `content`, `tags`, `image_urls`, `note_type`

4) Return to the user:
- A clean, readable list of generated notes
- Include hashtags if available

## Troubleshooting

- Task FAILED / `success: false`:
  - Surface `message` from response.

- Want field details:
  - Read `references/content-marketing-dashboard-api.md`.
