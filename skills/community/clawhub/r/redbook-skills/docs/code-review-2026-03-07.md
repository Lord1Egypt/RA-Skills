# RedBookSkills 代码审阅报告

审阅日期：2026-03-07  
审阅范围：`scripts/account_manager.py`、`scripts/chrome_launcher.py`、`scripts/feed_explorer.py`、`scripts/image_downloader.py`、`scripts/publish_pipeline.py`、`scripts/run_lock.py`、`scripts/cdp_publish.py`

## 审阅结论

整体结构是清晰的：账号管理、Chrome 生命周期、CDP 封装、下载器、发布流水线、锁机制已经做了模块拆分，`run_lock.py` 与 `feed_explorer.py` 的边界也相对干净。  
但当前实现里仍有几处**会直接影响正确性或稳定性**的问题，尤其是：

1. 定时发布校验存在**运行时异常**，会直接中断带 `--post-time` 的流程。
2. 内容数据抓取接口的分页/筛选参数**名义支持但实际未生效**。
3. 多账号能力与 Chrome 端口复用之间存在**会串号的设计缺陷**。
4. CDP 请求与正文填充逻辑存在**挂死/内容变形**风险。

## 审阅方式

- 静态通读全部脚本实现与 CLI 入口。
- 执行 `python3 -m py_compile scripts/*.py`，结果通过。
- 执行导入级检查与纯函数调用，确认 `scripts/cdp_publish.py` 在调用 `validate_schedule_post_time()` 时抛出 `NameError`。
- 执行 `python3 -Wall` 导入，确认 `scripts/cdp_publish.py` 存在多处 `SyntaxWarning: invalid escape sequence '\s'`。

## 做得好的地方

- 模块划分合理：`publish_pipeline` 负责编排，`cdp_publish` 负责页面自动化，职责大体明确。
- `run_lock.py` 的 stale lock 清理思路不错，能避免一部分僵尸锁问题。
- `feed_explorer.py` 的 `SearchFilters` + `FeedExplorer` 抽象可复用性较好。
- 大部分 CLI 参数有说明，类型注解与 docstring 覆盖率也不错。

## 主要问题

### 1. 定时发布参数校验存在运行时异常

- 严重级别：高
- 位置：`scripts/cdp_publish.py:54`、`scripts/cdp_publish.py:206`、`scripts/cdp_publish.py:3028`
- 现象：`validate_schedule_post_time()` 中使用了 `timedelta`，但文件顶部只导入了 `datetime`，没有导入 `timedelta`。
- 实际影响：只要调用带 `post_time` 的发布流程，就会在运行期触发 `NameError`，定时发布不可用。
- 复现结果：`from scripts.cdp_publish import validate_schedule_post_time; validate_schedule_post_time('2026-03-08 10:00')` 会报 `NameError: name 'timedelta' is not defined`。
- 建议：补充 `from datetime import datetime, timedelta`，并为该纯函数补最小单元测试。

### 2. 内容数据抓取接口的分页参数没有真正生效

- 严重级别：高
- 位置：`scripts/cdp_publish.py:2513`、`scripts/cdp_publish.py:2538`、`scripts/cdp_publish.py:2616`
- 现象：`get_content_data(page_num, page_size, note_type)` 接收分页与筛选参数，但方法内部只是打开固定页面 `XHS_CONTENT_DATA_URL`，然后被动监听页面自己发出的请求。
- 实际影响：调用方传入的 `page_num`、`page_size`、`note_type` 只是“记录下来”，并不驱动真实请求；最终返回的数据取决于页面默认行为，而不是 CLI 参数。
- 证据：代码在 `2616` 行以后还专门打印 “Requested pagination/filter differs from captured page request”，说明当前实现本身也知道参数可能失效。
- 建议：要么显式通过页面脚本触发目标分页请求，要么移除这几个 CLI 参数，避免形成错误契约。

### 3. 多账号隔离会被“端口已占用”逻辑绕过

- 严重级别：高
- 位置：`scripts/chrome_launcher.py:129`、`scripts/chrome_launcher.py:133`、`scripts/chrome_launcher.py:297`
- 现象：`launch_chrome()` / `ensure_chrome()` 只要发现调试端口已打开，就直接认为 Chrome 可复用，但并不会校验当前监听该端口的实例是否就是目标账号的 `user-data-dir`。
- 实际影响：在多账号场景下，如果端口 `9222` 已被另一个账号的 Chrome 占用，新流程会静默复用错误 Profile，导致“看起来指定了账号，实际上操作到了别的账号”。
- 建议：至少在连接前校验当前标签页所属 Profile/账号标识；更稳妥的方案是按账号分配独立 CDP 端口，或在本地保存端口到账号的映射关系。

### 4. 正文填充使用 `innerHTML`，会把普通文本当 HTML 解释

- 严重级别：中
- 位置：`scripts/cdp_publish.py:2886`、`scripts/cdp_publish.py:2899`
- 现象：`_fill_content()` 把用户正文拆成段落后直接拼接到 HTML，再赋值给 `el.innerHTML`。
- 实际影响：如果正文包含 `<`, `>`, `&` 或类似 HTML 片段，最终写入编辑器的内容可能被浏览器解析成标签，而不是原始文本；这会造成内容变形，甚至直接丢字。
- 建议：改为基于 `textContent` / `createTextNode` 逐段写入，或复用已有的逐字输入/粘贴模拟逻辑，避免 HTML 注入式赋值。

### 5. CDP 收包没有超时控制，流程可能无限挂起

- 严重级别：中
- 位置：`scripts/cdp_publish.py:548`、`scripts/cdp_publish.py:552`
- 现象：`_send()` 发送 CDP 命令后直接 `self.ws.recv()` 阻塞等待匹配响应，没有总超时，也没有连接中断恢复策略。
- 实际影响：一旦 Chrome 没返回响应、WebSocket 状态异常、或页面事件流干扰导致响应丢失，整个进程会无限等待；结合 `run_lock.py`，还可能把后续发布任务一并卡死。
- 建议：为 `_send()` 增加命令级超时和更清晰的异常包装，超时后主动断开并提示重连。

### 6. 账号配置损坏时会静默回退默认配置，存在数据覆盖风险

- 严重级别：中
- 位置：`scripts/account_manager.py:43`、`scripts/account_manager.py:47`、`scripts/account_manager.py:62`
- 现象：`_load_accounts()` 在 JSON 解析失败时直接 `pass`，然后返回默认结构；之后任意一次 `_save_accounts()` 都可能把原本损坏但可人工恢复的配置覆盖掉。
- 实际影响：配置文件一旦被部分写坏或手工编辑出错，工具不会显式报警，反而会悄悄“重置”为默认账号，造成难以察觉的数据丢失。
- 建议：对损坏配置直接报错并停止写入，或者先备份损坏文件再生成新文件。

### 7. 账号名未做约束，Profile 路径可逃逸基目录

- 严重级别：中
- 位置：`scripts/account_manager.py:138`、`scripts/account_manager.py:153`
- 现象：`add_account()` 直接把用户提供的 `name` 拼到 `PROFILES_BASE` 下，没有限制 `..`、路径分隔符或绝对路径片段。
- 实际影响：恶意或误操作输入如 `../../other-dir` 时，Profile 目录可能被创建到预期目录之外，破坏多账号目录边界。
- 建议：限制账号名字符集，例如仅允许字母、数字、`-`、`_`，并在保存前做规范化校验。

### 8. 图片批量下载会吞掉部分失败，发布结果可能“少图但继续发”

- 严重级别：中
- 位置：`scripts/image_downloader.py:152`、`scripts/image_downloader.py:163`、`scripts/publish_pipeline.py:547`、`scripts/publish_pipeline.py:550`
- 现象：`download_all()` 对单张下载失败只记录日志继续执行；流水线只检查“是否全部失败”，不检查“是否部分失败”。
- 实际影响：用户传 9 张图时，只要下载成功 1 张，流程就会继续发布，最终内容与调用者预期不一致，而且没有强失败信号。
- 建议：提供严格模式（默认严格），当任意下载失败时直接终止；或至少返回成功/失败明细并在流水线中强提示。

### 9. 多处内嵌 JS 字符串触发 `invalid escape sequence` 警告

- 严重级别：低
- 位置：`scripts/cdp_publish.py:775`、`scripts/cdp_publish.py:1243`
- 现象：Python 普通字符串里直接写了 JS 正则 `/\s+/` 的未转义版本，导入时触发 `SyntaxWarning`。
- 实际影响：当前版本通常仍可运行，但这类警告会增加维护噪音，也会掩盖真正的导入问题。
- 建议：把相关 JS 片段改成原始字符串，或统一使用 `\s` 转义。

## 次要观察

- `scripts/publish_pipeline.py:591` 直接调用 `publisher._click_publish()` 私有方法，接口层次有些泄漏；后续可考虑提供公开方法。
- `scripts/publish_pipeline.py:462` 提取话题标签后没有再次校验正文是否为空；如果正文只剩标签行，流程仍会继续。
- `scripts/chrome_launcher.py:155` 启动 Chrome 时把 `stdout/stderr` 全部重定向到 `DEVNULL`，排障成本较高。

## 优先修复建议

建议按下面顺序处理：

1. 先修 `timedelta` 缺失与 `get_content_data()` 参数失效。
2. 再修多账号端口复用问题，避免串号。
3. 然后处理 `_send()` 超时和 `_fill_content()` 文本写入方式。
4. 最后补账号名校验、配置损坏保护、下载失败策略。

## 总体评价

这个仓库已经具备“能跑通”的工程骨架，但当前更像是**高耦合的自动化脚本集合**，距离“稳定的技能包”还差一层可靠性治理。  
如果只做一次性个人使用，问题还可控；如果要长期运行、跨账号运行或接入更多自动化场景，以上高优问题建议尽快处理。
