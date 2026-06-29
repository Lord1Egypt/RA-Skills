## Step 5 — 生成 HTML

### 5.1 配套资源

1. 复制本 skill 的 `assets/` 目录到当前工作目录
2. 根据用户选择，从 `templates/full-decks/` 复制对应 `style.css`：
   - A（培训演示）→ `templates/full-decks/pptx-model/style.css` 复制为 `assets/pptx-model.css`
   - B（学习分享）→ `templates/full-decks/pdf-model/style.css` 复制为 `assets/pdf-model.css`
3. 运行校验：

```bash
python scripts/check_assets.py <当前工作目录>/assets --type <pptx|pdf>
```

若校验不通过（exit 1），根据报错信息从本 skill 目录补充复制缺失文件，重新校验直至通过（exit 0）。

### 5.2 生成页数计划 → `{原始文档stem}_page-plan.md`

1. 读取 `resources/prompts/5.0_内容映射.md`，按其中映射规则和分页规则，从 5 个独立分析文件（`{原始文档stem}_4.N_*.md`）确定每页内容和标题
2. 以 Markdown 表格形式输出，落盘到 `{原始文档stem}_page-plan.md`：

```markdown
| # | 页标题 | 来源文件 | 覆盖数据点 |
|----|--------|---------|-----------|
| 1 | 封面 | — | 文档标题、发布日期、发布机构 |
| 2 | 法规定性 | `_4.2_定性.md` | 为什么、适用范围、适用对象 |
| ... | ... | ... | ... |
```

3. **覆盖度核对**：逐文件检查 5 个分析文件的全部数据点是否在 page-plan 的"覆盖数据点"列中有对应行。遗漏则补页。
4. 运行校验：

```bash
python scripts/validate.py {原始文档stem} --step page-plan
```

校验不通过则补全缺失的页。通过则继续。

### 5.3 生成布局分配计划 → `{原始文档stem}_layout-plan.md`

1. 读取 `{原始文档stem}_page-plan.md`，获取全部页数和每页内容类型
2. 读取 `resources/layouts.md`，按每页内容类型严格匹配布局
3. 以表格形式输出并落盘到 `{原始文档stem}_layout-plan.md`：

```markdown
| # | 页标题 | 布局场景 | pptx-model class | pdf-model class |
|----|--------|---------|-----------------|-----------------|
| 1 | 封面 | 封面页 | `.ts-stripe` + `.ts-alert-tag` + `.ts-h1` | `.page-dot` + `.sticker` + `.cover-title` + `.h1` |
| ... | ... | ... | ... | ... |
```

**布局约束：**
- 布局场景必须选自 `layouts.md` 的"应用场景"列
- 相邻页不得使用相同布局场景（连续同类内容的页除外）
- 内容量大的页，确保所选布局有足够容量（避免 8 行表格塞进两栏布局）
- # 列必须与 `page-plan.md` 完全对应
4. 运行校验：

```bash
python scripts/validate.py {原始文档stem} --step layout-plan
```

校验不通过则修正。通过则继续。

### 5.4 生成 HTML

根据开始时的用户选择，**仅生成对应的一个 HTML 文件**：

| 选择 | 生成文件 | 比例 |
|------|---------|------|
| A 培训演示 | `{原始文档stem}_pptx-model.html` | 16:9 |
| B 学习分享 | `{原始文档stem}_pdf-model.html` | 3:4 竖版 |

**按以下顺序读取，逐页生成：**

1. 读取 `{原始文档stem}_page-plan.md` — 确定页数、标题、数据来源
2. 读取 `{原始文档stem}_layout-plan.md` — 确定每页布局和 CSS class
3. 读取 `resources/html_spec.md` — 确定 HTML 骨架、组件格式、**class 白名单**

生成过程中，**严格只使用 `html_spec.md` 中白名单列出的 class**，禁止自行发明 class 名。

### 5.5 校验与审阅

1. 运行校验：

```bash
python scripts/validate.py {原始文档stem} --step 5
```

2. 校验通过后，**暂停并用 `present_files` 展示生成的 HTML 文件给用户审阅**：

> HTML 已生成（共 N 页），请审阅（可以在浏览器打开，或者在右侧文件栏预览，鼠标点击网页后按方向键⬅️或➡️预览对应页面）。预览后可直接回复调整意见，或回复"继续"进入 Step 6。

根据用户反馈修改并重新生成，直至用户确认满意，再继续 Step 6。
