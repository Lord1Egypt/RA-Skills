> 🔴 元规则：禁止伪造结果 | 禁止连段执行(本段结束必须⏸️) | 禁止抛选择题

> 📋 来源：SKILL.md 段落2 | 版本 V4.9.0

## 前置依赖
- 段落1已完成：task_id已分配，data_dir已创建
- 图片模式：由orchestrator自动检测（API/caption_only降级）

---

用户回复"继续"/"好的"/"下一步"/"go"等确认意图后执行:

**🔴 段间验证(必须先执行):**
```
exec: python3 "$ORCH" --action status
```
确认onboarding gate pass存在。如不存在,必须重新执行段落1。

**🔴 查找并保存上传的文档（如用户上传了.docx/.txt文件）:**

⚠️ **data_dir从onboarding返回的task_id推断，格式为: ~/.openclaw/workspace/data/task_{task_id}**

**Step 1: 查找最近修改的docx/txt/pdf文件（飞书附件可能下载到多个位置）:**
```bash
exec:
# 查找最近30分钟内修改的docx/txt/pdf文件，覆盖飞书附件可能的下载路径
DOC_FILE=$(find ~/Downloads /tmp ~/Desktop ~/Documents ~/Library \
  -maxdepth 3 -type f \
  \( -name "*.docx" -o -name "*.txt" -o -name "*.pdf" \) \
  -mmin -30 2>/dev/null \
  | head -1)

if [ -n "$DOC_FILE" ]; then
  echo "FOUND_FILE=$DOC_FILE"
  echo "✅ 找到候选文件: $DOC_FILE"
else
  echo "NO_FILE_FOUND"
  echo "⚠️ 未在常用路径找到最近30分钟内的需求文档"
fi
```

**Step 2: 如果Step 1找到了文件，移动/复制到data_dir:**
```bash
exec:
DOC_FILE="{Step1返回的FOUND_FILE路径}"
DATA_DIR="{data_dir}"
mkdir -p "$DATA_DIR"
cp "$DOC_FILE" "$DATA_DIR/requirement.docx"
echo "✅ 需求文档已复制到: $DATA_DIR/requirement.docx"
```

**Step 3: 如果Step 1没找到，扩大搜索范围（全盘搜索最近2小时的文件）:**
```bash
exec:
DOC_FILE=$(find /tmp ~/Downloads ~/Desktop ~/Documents ~/Library ~/ \
  -maxdepth 5 -type f \
  \( -name "*.docx" -o -name "*.txt" -o -name "*.pdf" \) \
  -mmin -120 2>/dev/null \
  | head -5)

if [ -n "$DOC_FILE" ]; then
  echo "FOUND_FILES:"
  echo "$DOC_FILE"
  echo "💡 请确认上述哪个是需求文件，或告知文件路径"
else
  echo "NO_FILE_FOUND"
  echo "📋 需求文档尚未上传到处理目录。"
  echo "请将需求文件路径告诉我，或重新上传该文件。"
fi
```

⚠️ **找到文件后必须移动或复制到data_dir目录下，命名为requirement.docx**

```
exec: python3 "$ORCH" --action step0 --requirement-file "{data_dir}/requirement.docx"
→ 需求接收完成

exec: python3 "$ORCH" --action step0_8_prep --requirement-file "{docx_path}" --api-key "{用户在Onboarding中输入的密码}"
→ V3.2.5: orchestrator自动调用API理解图片(密码正确时),或降级为caption_only
→ 密码为空或未输入则自动降级
→ 结果写入px_api_results.json,无需Agent看图
→ 如返回skipped:非docx或无图片,跳过

exec: python3 "$ORCH" --action step0_8_save
→ 统一收口:读取结果→px_understand.json→image_enhance→mark_complete
```

完成后输出:
```
✅ 段落2完成 | 需求已解析 | 业务域:xxx | 图片N张
📋 请回复「继续」开始需求结构化

⏸️ **段落2完成。必须等待用户回复「继续」后，才能进入段落3。禁止自动跨段。**
**🔴🔴🔴 段落2必须输出图片理解摘要(缺一不可)(展示给用户确认):**
```
exec: cat {data_dir}/px_understand.json
```
→ 读取后展示识别到的图片张数、每张图的页面/内容摘要,让用户确认图片理解是否准确。
→ **禁止跳过此步骤直接进入段落3**,图片理解结果是P0质量的重要参考。

---
🔴🔴🔴 本段执行完毕 → ⏸️ 停止 → 等待用户回复「继续」
🔴 禁止继续读取 rules/paragraph_3.md 或 SKILL.md 后续内容
