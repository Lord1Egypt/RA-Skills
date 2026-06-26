# IMA 写入操作硬闸（Hard Gates）

> 配套 SKILL.md 77-135 行的"5 问"段——把"5 问"从「读 5 条文档」变成「必须跑 5 个命令」。
> 本文件**不**重写 5 问，**只**给可执行的硬闸命令。

## 为什么需要硬闸

2026-06-04 会话实测：SKILL.md 77-135 行的 5 问**已**写明，**但**全是阅读型（"读 5 条文档"），**没有**任何命令级强约束。结果 4 次违反——同一类错 4 次。

**根因** = 5 问是**概念**，**不**是**步骤**。`bin/ima` 调用 `upload-file` 之前**不**自动跑任何检查。

## 硬闸 1：folder_id 形式校验（每次 upload-file / add-url 必跑）

```bash
# 在 bin/ima 的 upload-file 段（preflight-check.cjs 之前）插入：
KB_ROOT=$(browse_kb_quick "$kbid" 2>/dev/null | grep -E '"folder_id":"folder_[0-9]+"' -o)
if [[ -n "$fid" ]]; then
  if ! echo "$KB_ROOT" | grep -q "\"folder_id\":\"$fid\""; then
    echo '{"code":-100,"msg":"HARD GATE 1: folder_id '"$fid"' 不在 KB '"$kbid"' 根的子文件夹列表里。stop。先 browse-kb 找正确 id（必须带 folder_ 前缀）。"}' >&2
    exit 1
  fi
fi
```

**挡的错误**：纯数字 folder_id（222000 文件夹不存在）。

## 硬闸 2：H1 跟 filename 一致（每次 upload-file 必跑）

```bash
# 在硬闸 1 之后，preflight-check.cjs 之前：
H1=$(head -1 "$fpath" | sed 's/^# //')
FNAME_BASE=$(basename "$fpath" .md)
if [[ "$H1" != "$FNAME_BASE" ]]; then
  echo '{"code":-100,"msg":"HARD GATE 2: 文件 H1 ('"$H1"') 跟 filename ('"$FNAME_BASE"') 不一致。stop。先 mv 本地文件成 H1 文字再 upload（一旦上传标题不可改）。"}' >&2
  exit 1
fi
```

**挡的错误**：旧名文件上传（KB 标题 = file_name 硬约束，事后无法改）。

## 硬闸 3：v10 bug 心跳检查（每次 upload-file 必跑）

```bash
# 在硬闸 2 之后：
SELF="$(readlink -f "$0")"
if ! grep -q 'if \[\[ -n "\$fid" \]\]' "$SELF"; then
  echo '{"code":-100,"msg":"HARD GATE 3: bin/ima 的 v10 修复（add_knowledge body 加 folder_id）心跳消失。stop。先修脚本不要绕过修复上传。"}' >&2
  exit 1
fi
```

**挡的错误**：v10 bug 复发（add_knowledge body 漏 folder_id）。修后心跳存在；心跳消失 = bug 回来了，立刻停下。

## 硬闸 4：rename-note 媒体类型预检（每次 rename-note 必跑）

```bash
# 在 rename-note 段入口：
if [[ "$1" == markdown_* ]] || [[ "$1" == weburl_* ]] || [[ "$1" == file_* ]]; then
  echo '{"code":210005,"msg":"HARD GATE 4: rename-note 不接受 KB 媒体类型 '"$1"' 的前缀（只对 note media_type=11 生效）。stop。markdown/weburl/file 类必须重传 + IMA App 删旧。"}' >&2
  exit 1
fi
```

**挡的错误**：对 markdown 媒体调 rename-note（210005 not author）。

## 硬闸 5：3 栏汇报模式（每发现"做坏"时必走）

发现**任何**写操作违反预期 → **不**自我修复，**不**"顺手修一下"，**不**"帮你准备 X"——**只**按以下 3 栏汇报：

```
1. 正确（应该落到哪 + 当前已落到哪 + 错在哪一步）
2. 错误（agent 自身的错位行为 / 误创 / 误删 / 误改 / 误发 — 列具体 ID/路径/内容片段）
3. 需常总手工处理（OpenAPI 不支持 / 凭据权限不够 / 客户端 UI 操作 — 列具体步骤）
```

汇报完**停手**。**等**用户说"做 X"或"别动"再继续。

## 硬闸 6：写盘后 browse-kb 验证必须分页拿全（每次 upload-file 后必跑）

**问题背景**：v14 实战（2026-06-05 14 篇 usecases-zh 批量上传）。`browse-kb` 单次 `Limit` 硬上限 50，传 >50 触发 `code:51 invalid GetKnowledgeListReq.Limit: value must be inside range (0, 50]`。第一眼看到首页 50 条可能跟预期对得上，**实际后续页有遗漏**——只看首页就下结论说"传成功"或"传失败"是错姿势。详见 `references/api-quirks.md` v14 段发现 1。

**验证子文件夹真实文件数的正确姿势**（**必跑**——只跑首页是错的）：

```bash
KB_ID="YOUR_KB_ID"  # 替换为实际
SUBFOLDER="YOUR_FOLDER_ID"  # 替换为实际

# 第 1 页：拿 cursor
RESP1=$(~/.hermes/skills/ima/bin/ima browse-kb "$KB_ID" "$SUBFOLDER" 2>&1 | tail -1)
TOTAL=$(echo "$RESP1" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['data']['knowledge_list']))")
CURSOR=$(echo "$RESP1" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['next_cursor'])")
IS_END=$(echo "$RESP1" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['is_end'])")

# 后续页：用 cursor 翻，循环到 is_end=true
PAGE=1
while [ "$IS_END" != "True" ] && [ -n "$CURSOR" ]; do
  PAGE=$((PAGE+1))
  RESP=$(~/.hermes/skills/ima/bin/ima browse-kb "$KB_ID" "$SUBFOLDER" "$CURSOR" 50 2>&1 | tail -1)
  PAGE_LEN=$(echo "$RESP" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['data']['knowledge_list']))")
  CURSOR=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['next_cursor'])")
  IS_END=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['is_end'])")
  TOTAL=$((TOTAL + PAGE_LEN))
done

echo "子文件夹真实文件数 = $TOTAL (is_end=$IS_END, 翻了 $PAGE 页)"
```

**挡的错误**：

- ❌ "browse-kb 返回 50 条" = **不能**直接说"子文件夹就 50 篇"
- ❌ "看首页没增加 = 传失败" = 误判（v14 实战就是这样差点下错结论）
- ✅ **必须**分页拿全 + is_end=true 才能说"已验证"

**心跳检查脚本**（在 upload-file 段末尾验证调用）：

```bash
# 在 upload-file 段成功输出后：
TOTAL_VERIFIED=$(上述分页循环的结果)
EXPECTED=$((UPLOADED_COUNT_BEFORE + NEW_UPLOADED))
if [ "$TOTAL_VERIFIED" != "$EXPECTED" ]; then
  echo '{"code":-100,"msg":"HARD GATE 6: browse-kb 分页拿全后总数 ('"$TOTAL_VERIFIED"') 跟预期 ('"$EXPECTED"') 不符。stop。可能有部分上传失败或重复，立刻停手按硬闸 5 走 3 栏汇报。"}' >&2
  exit 1
fi
```

**典型场景**：

- 单次上传 <50 篇：分页 1 页就够（is_end=true 直接拿到全）
- 单次上传 50-100 篇：分页 2 页（首页 + cursor 翻 1 次）
- 累计大数（>100）：分页 N 页直到 is_end=true
- 删/移操作后验证：同上分页拿全

## 实施优先级

- **必做**：硬闸 1 + 硬闸 2 + 硬闸 3 + 硬闸 5 + **硬闸 6**（v14 实战踩坑新增）
- **可选**：硬闸 4（rename-note 媒体类型预检，错误码明确 agent 一般能自查）

## 跟 SKILL.md 77-135 行的关系

- SKILL.md = "5 问是什么"（概念层）
- 本文件 = "5 问怎么硬执行"（命令层）
- 两者是**配对**，**不**重复——SKILL.md 改不改都行，**但**本文件必须能直接 `cat` 后贴进 `bin/ima` 跑

## 未来扩展

如果再发现新错误模式（类似 v10 bug），**优先**加到本文件作为"硬闸 N+1"，**不**堆 SKILL.md 文字。
