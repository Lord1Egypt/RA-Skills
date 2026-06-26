# Template-based Image Generation

Generate images using ShortArt templates for posters, social media graphics, and marketing materials.

**IMPORTANT:** Ensure `SHORTART_API_KEY` is set in your environment. After setting it in `~/.zshrc`, restart your terminal or run `source ~/.zshrc`.

## Workflow

### Step 1: Recommend Templates

1. **Extract keywords** from user input:
   - Read `assets/keywords.json` for available keywords
   - Match user input (case-insensitive, partial match)
   - Select 3-5 most relevant keywords

2. **List templates**:
```bash
python3 scripts/template-image/impl.py --list-templates {keyword1} {keyword2} --count 6
```

3. **Show top 3** templates with numbered descriptions
4. **If unsatisfied**, show next 3, then cycle back

### Step 2: Get Template Details

After user selects (e.g., "第1个"), get full definition:

```bash
python3 scripts/template-image/impl.py --get-template {template_slug}
```

### Step 3: Collect Parameters

Prompt based on `template.args`:
- `type: "image"` → Ask for image path
- `type: "input"` → Ask for text
- `type: "select"` → Show options, ask user to choose
- `type: "radio"` → Show options, ask user to choose

**CRITICAL**: Keep complete parameter structure. Only update `default` field.

### Step 4: Upload Images

For each image parameter:

```bash
python3 scripts/template-image/impl.py --upload-image "/path/to/image.jpg"
```

Extract `path` from response and set to parameter's `default` field.

### Step 5: Generate Image

```bash
python3 scripts/template-image/impl.py \
  --template-id "{template_id}" \
  --args '[{complete_args_with_ALL_params}]' \
  --image "{uploaded_path_1}" \
  --image "{uploaded_path_2}" \
  --wait
```

**CRITICAL**:
- Use template ID (not slug)
- Include ALL parameters in args
- Preserve complete structure from get-template
- Update only `default` values
- Duplicate image paths in both args and `--image` flags

### Step 6-10: Poll and Download

Same as other modes:
6. Ask user to wait
7. Poll: `--poll {project_id} --args '{json_args}'`
8. Handle result
9. Download: `--download '{json_result}'`
10. Inform user of local paths

