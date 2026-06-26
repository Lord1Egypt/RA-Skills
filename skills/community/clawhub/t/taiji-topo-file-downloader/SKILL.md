---
name: taiji-topo-file-downloader
description: 在太极平台 a.taiji.woa.com 工作流页面自动定位节点侧边栏、打开配置文件面板并下载文件。用于“下载太极拓扑配置文件/模型文件”“在太极页面里找到文件并保存到本地”等任务，特别适合需要先校验页面是否已正确打开、再稳定定位侧边栏与文件列表的场景。
---

# taiji-topo-file-downloader

在太极平台下载文件时，优先用“**先校验页面状态，再分层定位 UI**”的流程，避免误点和空页面操作。

## 标准流程（按顺序执行）

### 1) 先做页面预检（经验教训：先确认网址和页面是否真的打开）

1. 确认当前标签页 URL 包含：`a.taiji.woa.com`
2. 如果不在太极域名：先切到正确标签页或导航到目标链接
3. 确认页面已加载出工作流主界面（如画布、节点区、侧栏容器任一可见）
4. 若页面未加载完成：等待关键文本/组件出现后再继续

> 不做这一步，后续“找侧边栏/找文件按钮”经常会失败。

---

### 2) 定位“节点参数侧边栏”（分层定位，先语义后样式）

优先级如下：

1. **语义定位（首选）**
   - 通过可见文本找锚点：`配置文件`、`参数配置`、`文件管理`、`节点参数`
   - 从锚点向上找最近的表单区块/抽屉容器

2. **结构定位（次选）**
   - 查找常见 Ant Design 侧栏容器：`ant-drawer` / `ant-form` / 参数区块
   - 在容器内验证是否存在“配置文件输入框 + 操作按钮”组合

3. **样式定位（兜底）**
   - 用 class 模糊匹配（如 `*[class*="drawer"]`, `*[class*="config"]`）
   - 必须结合文本二次校验，避免误匹配

> 关键点：不要只依赖单个 class；太极页面改版后 class 很容易漂移。

---

### 3) 从侧边栏进入文件列表

1. 在“配置文件”字段区域点击文件管理入口（图标/按钮）
2. 等待文件管理弹窗出现（通常是 Ant Modal）
3. 校验弹窗内存在文件表格（`tr` 行 + 文件名文本）

示例（DOM 兜底思路）：

```javascript
const modal = document.querySelector('.ant-modal-wrap, .ant-modal-root');
if (!modal) throw new Error('文件管理弹窗未出现');
const rows = modal.querySelectorAll('tr');
if (!rows.length) throw new Error('未找到文件列表行');
```

---

### 4) 在文件列表里精确定位目标文件并下载

1. 遍历 `tr`，按文件名匹配（优先全名，必要时再用 includes）
2. 在命中行查找操作列链接
3. 点击第一个操作链接作为下载按钮（常见为：索引 0=下载，1=编辑）

```javascript
const target = 'model.py';
const modal = document.querySelector('.ant-modal-wrap, .ant-modal-root');
const rows = [...modal.querySelectorAll('tr')];

const hit = rows.find(r => r.textContent.includes(target));
if (!hit) throw new Error(`未找到文件: ${target}`);

const ops = hit.querySelectorAll('a,button');
if (!ops.length) throw new Error('未找到可点击下载操作');
ops[0].click();
```

---

### 5) 处理 Chrome 下载临时文件并落盘重命名（新增：目录命名规范）

落盘目录必须为：`{topo名}_{YYYYMMDD_HHMMSS}`，并放在指定基目录下。

```bash
# 指定基目录（可按任务改）
base_dir="~/Downloads"

# 输入（从页面提取或任务参数传入）
topo_name="{拓扑名}"
file_name="{文件名}"

# 清洗拓扑名，避免路径非法字符
safe_topo=$(echo "$topo_name" | tr '/:' '_' | tr -s ' ' '_' | sed 's/[^[:alnum:]_.-]/_/g')

# 当前时间（Asia/Shanghai）
now=$(TZ=Asia/Shanghai date +%Y%m%d_%H%M%S)
out_dir=$(eval echo "$base_dir")/${safe_topo}_${now}
mkdir -p "$out_dir"

# 取最新 Chrome 临时下载文件
temp_file=$(ls -t ~/Downloads/.com.google.Chrome.* 2>/dev/null | head -1)

# 安全检查
[ -z "$temp_file" ] && echo "未发现临时下载文件" && exit 1

# 移动并重命名
mv "$temp_file" "$out_dir/$file_name"
```

---

## OpenClaw 浏览器自动化模板（新增，可直接照此执行）

> 目标：减少盲点点击，稳定复现“预检→侧栏→文件弹窗→下载”流程。

1. **获取当前标签并快照**
   - `browser.tabs(profile="chrome")`
   - `browser.snapshot(profile="chrome", targetId=<taiji-tab>, refs="aria")`

2. **URL 与页面状态断言**
   - 若 `targetUrl` 不含 `a.taiji.woa.com`：`browser.navigate(...)`
   - 重新 `snapshot`，确认出现“配置文件/参数配置/节点参数”等文本锚点

3. **打开文件管理入口**
   - 在 snapshot 中定位“文件管理”按钮对应 ref
   - `browser.act(request:{kind:"click", ref:<file-manager-ref>})`
   - 再次 `snapshot`，断言弹窗/表格出现

4. **点击目标文件下载**
   - 在弹窗内找到包含目标文件名的行
   - 点击该行操作列中的“下载”控件 ref
   - 若 ref 不稳定，再退回 DOM 兜底脚本策略

5. **本地落盘校验（必要）**
   - 执行第 5 节 shell 模板
   - 只有当目标目录下出现重命名文件，才判定成功

---

## OpenClaw 浏览器自动化建议（更稳定）

1. 用 `browser.snapshot` 先抓 UI 引用，再 `browser.act` 点击，少用盲点坐标点击
2. 同一标签连续操作时，始终复用同一个 `targetId`
3. 优先通过可访问名称/可见文本定位（比 CSS class 更稳）
4. 每次关键点击后都做状态断言（弹窗是否出现、文件行是否出现）

---

## 失败恢复策略

### A. 找不到侧边栏
- 回到第 1 步重做 URL 与加载校验
- 确认是否已选中正确节点（未选中节点通常不会出现参数侧栏）
- 改用“文本锚点 + 向上回溯容器”的方式重新定位

### B. 找不到文件管理按钮
- 确认当前节点是否有“配置文件”参数
- 滚动侧边栏，避免按钮在可视区外
- 检查是否有权限/只读状态导致按钮隐藏

### C. 下载后无临时文件
- 等待 1-3 秒再查一次
- 确认 Chrome 下载路径是否仍是 `~/Downloads`
- 排除并发下载干扰（按时间戳过滤最新文件）

---

## 本次迭代沉淀（必须遵守）

1. **先确认网址和页面打开状态**，再做任何 UI 定位。
2. **侧边栏定位必须分层**：语义文本 → 结构容器 → 样式兜底。
3. **每个关键步骤都要有断言**（找到侧栏、弹窗、文件行、临时下载文件）。
4. **下载成功判定不靠“点击成功”**，而靠“本地出现临时文件并完成重命名”。
5. **落盘目录统一为 `topo名_当前时间`**，避免覆盖历史下载与并发冲突。

这几条是让流程在页面抖动、样式改版、加载波动时仍可用的核心保障。