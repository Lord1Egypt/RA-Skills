---
name: testagent-browser-testing
version: 1.4.0
description: 使用 Playwright MCP、browser-use CLI 和 openclaw 内置浏览器对 Web 产品进行功能测试，包含完整的测试 SOP：制定计划、执行测试、记录 bug 并截图，最终输出报告并录入 Coding。当用户说「去测」「测试一下」「帮我测」「QA」某个 URL 或功能时触发。
---

# Browser Testing

## ⚠️ 铁律（每次测试前必须确认，不得跳过）

**1. 截图必须用 Playwright MCP，绝不用内置浏览器截图**
内置浏览器 `browser screenshot` 只返回 AI 分析文本，`MEDIA:` 无法渲染，用户看不到图片。
截图唯一正确方式：`playwright__browser_take_screenshot` → 存文件 → `MEDIA:<路径>`

**2. 使用内置浏览器前，先检查 ssrfPolicy 白名单**
目标域名和登录域名（Auth0 等）必须在 `~/.openclaw/openclaw.json` 的 `allowedHostnames` 中，否则导航报 `blocked by policy`。
配置改完必须执行完整重启序列：`browser stop` → `gateway restart` → 等 15 秒 → `browser start`

**3. 字体/环境问题，先检查 browser-setup 是否跑过，不要手动折腾**
中文乱码、浏览器启动超时等环境问题，优先运行 `bash testagent-browser-setup/scripts/setup.sh`，不要手动装字体或逐步排查。

---

## 测试 SOP

### 阶段一：收集启动信息

收到测试指令后，只询问登录前无法自行获取的信息：

1. **目标 URL**（若用户未提供）
2. **测试账号和密码**（登录用）
3. **测试目标描述**（如「测试创建团队功能」）

不要在看到产品之前提任何关于产品细节的问题（字段格式、必填项、二级账号等），这些登录后自己看。

### 阶段二：探索产品，制定测试计划（需用户确认）

1. 按 [REFERENCE.md 工具选择](REFERENCE.md#工具选择) 选定主用工具
2. **若使用内置浏览器**，导航前先确认 `~/.openclaw/openclaw.json` 的 `browser.ssrfPolicy.allowedHostnames` 已包含目标域名和登录域名；若未包含，先添加并执行完整重启序列（见 [REFERENCE.md 踩坑](REFERENCE.md#踩坑)），再导航
3. 导航到目标 URL，自动登录
4. **Viewport 检查（必做，自主判断）**：用 Playwright MCP 截图，自行判断页面是否适合测试：
   - 若内容拥挤、元素重叠、按钮被遮挡、侧边栏挤压主内容区 → 执行 `playwright__browser_resize → width=1440, height=900`，再截图确认
   - 若页面显示正常 → 直接继续
   - 不需要询问用户，自主决定是否调整
5. 浏览目标功能区域，了解实际页面结构和交互
6. **基于真实页面**，输出 3-5 个测试点，**等用户确认或修改后再开始执行**

```
（登录并查看产品后）我计划测试以下场景，确认后开始：
1. 创建团队 — 填写名称和必要字段，验证创建成功
2. 表单校验 — 必填项为空时是否有提示
3. 团队内发送消息 — 消息是否正常显示
4. 边界输入 — 团队名称超长时的处理
```

**只有在探索后发现确实需要额外信息时**（如：测试场景需要第二个账号、需要特定测试数据），才在此阶段向用户追问。

### 阶段三：执行测试（全程自主，不打断用户）

- 逐一执行每个测试点
- **发现 bug 立刻截图**，不要攒到最后（页面状态随时可能变化）
- 截图命名：`/root/.openclaw/workspace/bug_<序号>_<简短描述>.png`
- 同一操作失败 2-3 次后，立即切换工具或策略（见 [REFERENCE.md 踩坑](REFERENCE.md#踩坑)）

### 阶段四：输出测试报告

所有测试点完成后，聊天内输出完整报告（格式见 [REFERENCE.md 报告格式](REFERENCE.md#报告格式)）。

### 阶段五：确认录入 Coding（需用户确认）

报告输出后询问：

```
以上 N 个 Bug 是否录入 Coding？
可修改建议的优先级、assignee、工期后回复「录入」，或指定修改某条。
```

用户确认后，调用 **coding-net skill** 的 `create_issue` 批量录入：
- `issue_type="DEFECT"`
- `priority`：按优先级规则（见 [REFERENCE.md](REFERENCE.md#优先级规则)）
- `due_date`：今日日期 + 建议修复工期（天）
- `assignee_id`：按 AGENTS.md 分工规则查成员 ID（用 `get_team_members_id_and_name` 或 `extract_members_from_issue_list`）

录入完成后输出每条 bug 的 Coding issue 编号。

---

详细工具对比、截图流程、报告模板见 [REFERENCE.md](REFERENCE.md)
