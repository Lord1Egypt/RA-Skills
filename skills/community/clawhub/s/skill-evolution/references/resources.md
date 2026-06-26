# 资源参考

回滚机制详细流程、外部文档解析工具、吞噬融合详细流程。

---

## 回滚机制：三层防护

### 触发时机

任何改动前（进化或吞噬），必须先执行备份。备份成功才能继续。

### 通用准备工作

```
1. 确保 .skill-backups/{skill-name}/ 目录存在
2. 确定目标 SKILL.md 的绝对路径
3. 记录文件大小: wc -c SKILL.md
```

### Layer 1: 文件级备份

```
1. 生成时间戳: date +%Y%m%d_%H%M%S
2. 复制: cp SKILL.md .skill-backups/{name}/SKILL.md.{timestamp}
3. 验证:
   - 备份文件存在
   - 备份文件大小 == 原文件大小 (byte-level)
   - 备份文件大小 > 0
4. 任一验证失败 -> 中止，输出错误信息，绝不继续
```

### Layer 2: Git 版本控制

```
检查 SKILL.md 是否在 git 仓库内: git rev-parse --git-dir
若在仓库内:
  1. git stash push -m "[skill-evolution] backup before {operation}" -- SKILL.md
  2. 验证 stash 成功: git stash list | grep "skill-evolution"

操作后保留:
  继续在当前状态工作 git add {SKILL.md} && git commit -m "[skill-evolution] {path}: {summary}"

操作后回滚:
  Step 1: git checkout -- SKILL.md
  Step 2: git stash pop (恢复 stash 中的其他改动）
  Step 3: 若 stash pop 冲突 -> 手动解决或 git stash drop
```

### Layer 3: 回滚验证

```
执行回滚后:
1. 读取回滚后文件
2. 读取最近的备份文件 (Layer 1)
3. diff 比对: diff SKILL.md .skill-backups/{name}/SKILL.md.{ts}
4. 无差异 -> 回滚成功
5. 有差异 -> 告警显示差异
   -> 尝试用 Layer 1 备份文件直接覆盖: cp 备份 SKILL.md
   -> 再次比对
   -> 仍有差异 -> 中止，显示所有备份路径，要求人工介入
```

### 必须遵守

- 改动前必须看备份验证结果。备份失败 = 不许改动。
- 备份文件绝不自动删除，由用户手动清理。
- 回滚后必须输出明确的对比结果（字节数是否一致）。

---

## 吞噬: 外部文档解析工具

根据文件后缀选择解析方式。以下所有工具使用前确保已安装对应 Python 包。

### .md 文件

直接使用 Read 工具读取，解析 Markdown 结构：
- 按 `## ` 和 `### ` 分割章节
- 识别代码块 ` ``` ` 和表格
- 提取每节的标题 + 正文摘要

### .docx 文件

```python
# 使用 python-docx 或直接用 docx skill 读取
# 关键: 提取段落文字 + 表格内容
from docx import Document
doc = Document(path)
for para in doc.paragraphs:
    if para.text.strip():
        print(para.text)  # 段落文本
for table in doc.tables:
    for row in table.rows:
        cells = [cell.text for cell in row.cells]
        print(' | '.join(cells))  # 表格行
```

注意: docx 中的页码、页眉页脚需单独处理。

### .pdf 文件

```python
# 方式1: pdfplumber (表格提取好)
import pdfplumber
with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()

# 方式2: PyMuPDF/fitz (文字提取好)
import fitz
doc = fitz.open(path)
for page in doc:
    text = page.get_text()
```

### .txt 文件

直接使用 Read 工具读取。按双换行分割段落。

### 提取后处理

```
1. 按段落/章节拆分为独立知识单元
2. 每个单元生成:
   - 摘要（30字内）
   - 关键词
   - 源位置（文件名+页码/行号）
3. 去重: 与目标 skill 已有内容比较，相似度 >80% 的标记为"可能重复"
4. 排序: 按与目标 skill 相关性降序
5. 最多展示 30 个候选，超过时按相关性截断
```

---

## 吞噬: 融合规则

### 标注来源

每个融入的知识块末尾加注释:
```markdown
<!-- 吞噬自: [源名称] 日期: YYYY-MM-DD 操作: [进化方向/吞噬类型] -->
```

### 冲突处理

融合前检查:
```
1. 与目标已有的每个章节做文本相似度比较
2. 相似度 > 80% -> 标记为"可能重复"
3. 语义矛盾检测:
   - 若源说"A 应该做 X"，目标说"A 应该做 Y"
   - 标记冲突，展示双方原文，让用户裁决
4. 用户裁决选项:
   - 采用源的版本 -> 替换
   - 保留目标版本 -> 跳过
   - 合并（用户描述如何合并）
```

### 体积控制

```
融合前估算目标 skill 文件大小
融合后预估大小 > 原文件 * 2.0 -> 警告
显示哪些吞噬项贡献了最多的体积
让用户决定: 继续/减少吞噬项/取消
```

---

## 日志格式

### evolution.log

```
=== 进化记录 ===
时间: 2026-06-07 07:30:00
目标: tianchuan-audit-perspective
类型: 领域知识
方向: 精准
改动: 在 Phase 3 增加交叉核验步骤，添加准则引用
结果: 保留
分数变化: 无 (未使用评分系统)
```

### phagocytosis.log

```
=== 吞噬记录 ===
时间: 2026-06-07 07:45:00
目标: tianchuan-audit-perspective
来源: 增值税法2026.pdf
吞噬项数: 3
项1: [摘要] 融入 Phase 2.1
项2: [摘要] 融入 Phase 2.3
项3: [摘要] 融入 Phase 3
结果: 用户测试满意，已保留
```

---

## 吞噬: 会话经验提取模板 (B2.3 详细指引)

### 提取步骤

```
1. 回顾本次对话中所有涉及目标 skill 的交互
2. 按以下三类分类：
   A. 逻辑纠正 — 用户指出 skill 的结论/判断有误
   B. 格式偏好 — 用户调整了输出格式/结构
   C. 知识补充 — 用户补充了 skill 未覆盖的专业知识点
3. 为每类生成候选吞噬项（见下方模板）
4. 展示为 Phase B3 的候选列表
```

### 提取模板

每项用以下结构呈现：

```
# 提取项 {序号}
类型: {逻辑纠正 / 格式偏好 / 知识补充}
触发轮次: 用户在第{2}轮对话时
原始输出: [skill 的原输出关键句]
用户反馈: [用户的纠正/补充原文]
提炼规则: [可嵌入 SKILL.md 的一条指令]
融入建议: 替换/追加到 [目标 skill] 的 Phase {X}.{Y}
```

### 示例

```
# 提取项 1
类型: 逻辑纠正
触发轮次: 用户在第3轮对话时
原始输出: "底稿复核完成，未发现异常"
用户反馈: "你漏了关联方交易的核查，附注21明确说了要查"
提炼规则: "底稿复核完成后，必须额外检查关联方交易披露（附注21），
           逐项核对关联方清单与底稿中相关科目的金额一致性"
融入建议: 追加到 tianchuan-audit-perspective 的 Phase 3
```

```
# 提取项 2
类型: 格式偏好
触发轮次: 用户在第5轮对话时
原始输出: 一大段文字描述问题
用户反馈: "给我表格，左边问题类型，右边具体问题和建议"
提炼规则: "发现异常时以表格输出，列: 问题类型 | 具体问题 | 准则依据 | 修复建议"
融入建议: 替换 tianchuan-audit-perspective 输出格式章节
```

### 过滤规则

以下情况不生成候选：
- 用户仅要求重新执行某步骤（非纠正）
- 临时性的一次性要求（如"这次只要前3页"）
- 与 skill 功能无关的闲聊

---

在 Skill 执行过程中，以下 MCP 连接器可能被用到：

| 连接器 | 用途 |
|--------|------|
| **kdocs** | 读取/操作金山文档（若用户提供云端文档路径） |
| **tencent-docs** | 读取/操作腾讯文档（若用户提供云端文档路径） |
| **ima-mcp** | 搜索知识库中的文档（若用户想从知识库吞噬） |

使用前先确认相应 connector 已连接。
