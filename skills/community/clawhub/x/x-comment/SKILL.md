---
name: x-comment
description: >-
  在 X（Twitter/X.com）的推荐时间线（Home timeline）上自动浏览并评论技术类和 BTC 相关推文。
  用户说「去 X 时间线上找几条技术帖子评论」「在 X 首页互动几条 BTC 相关内容」
  「帮我在 X 推荐页发几条技术评论」时触发本 skill。不进行点赞，只发布评论。
---

# x-comment —— X 时间线自动评论

本 skill 固化的是我们在 `profile=openclaw` 环境下实测的一套流程：

- 浏览 X 首页推荐时间线（Home timeline）
- 筛选技术类、BTC 相关的推文
- 自动完成：打开 reply + **模拟真人慢速打字**填入评论 + **直接发送**

> 核心原则：**全自动完成互动，输入评论后直接发送，不询问用户确认。只评论不点赞。**

---

## 0. 环境约束与边界

1. **浏览器与 profile**
   - 使用托管浏览器 `profile="openclaw"`，通过 HTTP 代理访问 X；
   - 需要保证该浏览器 profile 内已经登录目标 X 账号，否则不会出现 like/reply 按钮。

2. **交互能力现状**
   - 已实测可行：
     - 能在搜索结果页/详情页获取完整 DOM（含 `data-testid="like"/"reply"`）。
     - 能点击 like / reply 按钮。
     - 能用 `browser act` + `type` + `slowly: true` 模拟真人键盘输入，让 Reply 按钮亮起。
     - 能自动点击发送按钮完成评论发布。

3. **Vision 功能限制**
   - **禁止使用 screenshot 图片识别功能**（OpenAI 组织未开启 vision）
   - 所有页面信息必须通过文本/DOM 抽取获取（evaluate/snapshot）
   - 遇到图片内容时，只能读取 alt 文本或跳过

4. **Skill 定位**
   - 这是一个 **全自动互动 skill**：
     - 自动：找内容 + 点赞 + 填评论 + **直接发送**
     - **不询问用户确认，输入完成后立即发送**

---

## 1. 使用场景与触发条件

当用户出现类似需求时使用本 skill：

- 「去 X 时间线上找几条技术帖子评论」
- 「在 X 首页互动几条 BTC 相关内容」
- 「帮我在 X 推荐页发几条技术评论」
- 「去 X 首页找些 AI/区块链/开发相关的内容评论」

默认假设：

- 话题范围：**技术类（AI、automation、开发、工具等）+ BTC/加密货币相关**；
- 条数 `N = 3`，除非用户另行指定；
- 语言策略：**根据原推文语言自动匹配**（中文推文→中文评论，其他语言→英文评论）；
- **只评论，不点赞**。

---

## 2. 高层流程

1. 确定参数
   - 话题筛选：技术类（AI、agent、automation、开发工具、编程等）+ BTC/加密货币相关；
   - 条数 `N`：默认 3；
   - 互动动作：**只评论，不点赞**；
   - 语气：
     - 默认：专业、友好、偏工程视角；
     - 对敏感话题（政治/战争等）要中立、反战、强调查证。
   - 语言策略：
     - **检测原推文主要语言**（通过文本中汉字占比、标点符号等判断）；
     - 中文推文（汉字占比 > 30%）→ 用中文回复；
     - 其他语言 → 用英文回复；
     - 技术术语始终保持英文（如 API、Docker、LLM 等）。

2. 打开 Home timeline

   ```text
   https://x.com/home
   ```

   - 使用：

     ```jsonc
     {
       "action": "open",
       "profile": "openclaw",
       "target": "host",
       "targetUrl": "https://x.com/home"
     }
     ```

3. 通过 `evaluate` 抓取候选 tweets（增强版：包含互动数据）

   在 Home timeline 执行类似脚本，拿前若干条并获取互动数据：

   ```js
   () => {
     const N = 15; // 多拉一些以便筛选优质内容
     const articles = Array.from(document.querySelectorAll('article[role="article"]'));
     const picked = articles.slice(0, N);
     const tweets = picked.map(article => {
       const linkEl = article.querySelector('a[href*="/status/"]');
       const href = linkEl ? linkEl.href : null;
       const textEl = article.querySelector('div[data-testid="tweetText"]');
       const text = textEl ? textEl.innerText : '';
       const authorEl = article.querySelector('div[data-testid="User-Name"] span');
       const author = authorEl ? authorEl.innerText : '';
       
       // 获取互动数据（reply/retweet/like 计数）
       const replyEl = article.querySelector('[data-testid="reply"]');
       const retweetEl = article.querySelector('[data-testid="retweet"]');
       const likeEl = article.querySelector('[data-testid="like"]');
       const replies = replyEl?.getAttribute('aria-label')?.match(/\d+/)?.[0] || '0';
       const retweets = retweetEl?.getAttribute('aria-label')?.match(/\d+/)?.[0] || '0';
       const likes = likeEl?.getAttribute('aria-label')?.match(/\d+/)?.[0] || '0';
       
       // 获取发布时间（相对时间）
       const timeEl = article.querySelector('time');
       const timeAgo = timeEl?.getAttribute('datetime') || '';
       
       return { 
         href, text, author, 
         replies: parseInt(replies), 
         retweets: parseInt(retweets), 
         likes: parseInt(likes),
         timeAgo
       };
     }).filter(t => t.href && t.text);
     return { ok: true, tweets };
   }
   ```

   模型侧基于多维度筛选出 `N` 条**最值得互动**的推文。

   **筛选标准（优先级从高到低）：**
   
   1. **优质账号优先**：
      - 已认证账号（蓝V/金V）
      - 知名技术博主/开发者/加密 KOL
      - 粉丝量 > 1k 或互动率高的账号
   
   2. **新鲜度优先**：
      - 优先选择 < 2 小时内发布的推文
      - 次优：2-6 小时内
      - 尽量避免 > 24 小时的旧内容
   
   3. **互动起飞阶段**：
      - 理想区间：10-100 条回复，说明话题有热度但未过度拥挤
      - 点赞/转发比例合理（非刷量）
      - 避免：0 互动（冷清）或 >500 互动（已饱和）
   
   4. **话题相关性**：
      - 技术类：AI、agent、automation、OpenClaw、开发工具、编程、框架、API、cloud、DevOps 等
      - BTC 相关：Bitcoin、BTC、加密货币、区块链、DeFi、Web3 等
      - 排除：纯政治、八卦、娱乐、广告推广等无关内容

4. 为每条生成高质量评论文案

   **评论质量标准（必须满足至少一项）：**
   
   1. **提供额外价值**：
      - 补充原推文未提及的技术细节、实践经验
      - 分享相关工具/资源/文档链接
      - 提出可操作的改进建议
      - 例：「这个方案不错，如果结合 XX 工具的 YY 功能，可以进一步优化 ZZ 环节」
   
   2. **制造对立（建设性）**：
      - 提出不同观点但附带论据
      - 指出潜在问题或边界条件
      - 挑战假设但保持尊重
      - 例：「不完全同意，实际场景中 XX 可能成为瓶颈，因为……」
   
   3. **提问引导**：
      - 提出深入的技术问题
      - 请求具体细节或使用体验
      - 引导作者展开讨论
      - 例：「好奇你们是怎么处理 XX 场景的？我们遇到了 YY 问题」
   
   4. **求证验证**：
      - 对数据/结论提出验证需求
      - 分享类似场景的对比结果
      - 请求开源/文档链接
      - 例：「有相关的 benchmark 数据吗？我们测试下来 XX 指标差异较大」
   
   5. **幽默共鸣**：
      - 用梗或类比增强表达
      - 自嘲式认同（「我也踩过这个坑」）
      - 轻松但不失专业
      - 例：「哈哈这个 bug 是程序员的必经之路，上次我因为这个 debug 到凌晨三点」

   **格式与长度要求：**
   
   - **字数限制（硬约束）**：
     - **普通用户（非 Premium）：最多 280 字符**
     - 中文评论建议：50-120 字（约 150-360 字符，安全范围内）
     - **严格控制**：生成评论后必须验证字符数 ≤ 280，超过则缩减
   - **结构**：
     - 开头：直接切入观点/问题（不要「很有意思」「很棒」等空话）
     - 主体：1-2 句核心论述或具体细节
     - 结尾：可选的问句/行动号召（如「你怎么看？」「期待开源」）
   - **格式优化**：
     - 必要时用换行分段（最多 2 段）
     - 技术术语用英文或代码格式（如 `API`、`Docker`）
     - 避免过度使用 emoji（最多 1-2 个，且有实际语义）

   **互动闭环策略：**
   
   - 优先评论**有回复习惯的作者**（查看其它回复中作者是否活跃）
   - 在评论中**留钩子**：提问、@相关账号、预告后续分享
   - 例：「我们团队也在探索类似方案，改天整理个完整对比发出来 @你」
   - 如果作者回复，**在下一轮 cron job 时优先回访**（需要维护一个「待回访列表」）

   **负面示例（避免）：**
   
   ❌ 「很有意思，学习了！」（无实质内容）  
   ❌ 「666」「牛逼」（无价值的符号）  
   ❌ 「同意楼上」（重复他人观点）  
   ❌ 纯广告/自我推广（「我们的产品也能做到」）  
   ❌ 过长的技术教程（超过 150 字，应该拆成独立推文）

   **正面示例（已验证字符数 ≤ 280）：**
   
   ✅ 「这个架构的关键在于状态管理，我们之前用 Redis 做分布式锁遇到过脑裂问题，后来改用 etcd 的 lease 机制才彻底解决。你们是怎么处理的？」（62 字/约 186 字符，提供价值 + 提问）
   
   ✅ 「不完全认同"BTC 只是投机工具"，真正的价值在于抗审查和去中心化。当然现阶段 90% 的人确实只是炒币，这是两码事。」（53 字/约 159 字符，制造对立但有论据）
   
   ✅ 「哈哈上次我也因为忘了清 Docker cache 导致镜像大小暴涨到 2GB，最后发现是 node_modules 被打进去了。多阶段构建真的能救命。」（62 字/约 186 字符，幽默共鸣 + 实践经验）

5. ~~对选中 tweets 自动点赞~~（本版本取消点赞）

   **不再执行点赞动作，直接进入评论流程。**

6. 进入详情页 + 打开回复框 + 填入评论

   对每条选中的 tweet：

   1. 使用 `browser.navigate` 进入详情页：

      ```jsonc
      {
        "action": "navigate",
        "targetId": "<page-id>",
        "url": "https://x.com/<user>/status/<id>"
      }
      ```

   2. 使用 `evaluate` 在详情页：
      - 找到 `article[role="article"]`；
      - 点击 `[data-testid="reply"]` 打开回复弹窗；
      - 等待 `div[role="dialog"] div[role="textbox"][contenteditable="true"]` 出现。

   3. 在文本框内**使用 browser 原生 type 动作 + slowly: true** 输入评论内容：

      **⚠️ 重要：必须使用 browser 的原生 `type` 动作配合 `slowly: true`，而不是 evaluate 里的 JS 模拟输入！**

      X 的 Draft.js 编辑器会校验输入事件的来源，只有通过 Playwright/CDP 的真实键盘输入才能让 Reply 按钮亮起。

      **正确做法：**

      1. 先用 `snapshot` 获取回复对话框中 textbox 的 ref：
         ```
         browser snapshot labels=false targetId=<page-id>
         ```
         找到 `textbox "Post text" [ref=eXXX]`

      2. 用 `browser act` 的 `type` 动作，**必须带 `slowly: true`**：
         ```jsonc
         {
           "action": "act",
           "profile": "openclaw",
           "targetId": "<page-id>",
           "request": {
             "kind": "type",
             "ref": "eXXX",
             "text": "你的评论内容",
             "slowly": true
           }
         }
         ```

      **错误做法（Reply 按钮会保持灰色）：**
      - 用 `evaluate` + `execCommand('insertText', ...)`
      - 用 `evaluate` + 手动 dispatch KeyboardEvent/InputEvent
      - 用 `type` 但不带 `slowly: true`

      **验证按钮状态：**
      输入完成后，可以用 evaluate 检查 Reply 按钮是否亮起：
      ```js
      (() => {
        const dialog = document.querySelector('div[role="dialog"]');
        const btns = dialog?.querySelectorAll('button');
        for (const btn of btns || []) {
          if (btn.innerText?.trim() === 'Reply') {
            return { disabled: btn.disabled, ariaDisabled: btn.getAttribute('aria-disabled') };
          }
        }
        return { found: false };
      })()
      ```
      当 `disabled: false` 且 `ariaDisabled: null` 时，按钮可点击。

   4. **输入后直接发送（默认行为）**：

      使用 `slowly: true` 输入后，Reply 按钮应该已经亮起。**默认直接点击发送，不询问用户确认。**

      发送方式：用 `evaluate` 点击 Reply 按钮：
      ```js
      (() => {
        const dialog = document.querySelector('div[role="dialog"]');
        const btns = dialog?.querySelectorAll('button');
        for (const btn of btns || []) {
          if (btn.innerText?.trim() === 'Reply' && !btn.disabled) {
            btn.click();
            return 'clicked Reply';
          }
        }
        return 'not found or disabled';
      })()
      ```

      发送后等待 2 秒，检查对话框是否关闭（`dialogExists: false`）来确认发送成功。

---

## 3. 对用户的反馈格式

完成互动后，向用户做一个结构化汇报，例如：

- 本轮使用 `profile=openclaw`，已在托管浏览器中登录 X；
- 已自动执行：
  - 筛选范围：X 首页推荐时间线（Home timeline）
  - 筛选策略：优质账号 + 最新发布（< 2h）+ 互动起飞阶段（10-100 回复）
  - 筛选标准：技术类（AI/agent/开发工具等）+ BTC/加密货币相关
  - 评论质量：每条评论附带价值类型标签（提供价值/制造对立/提问/求证/幽默共鸣）
- 发送状态：
  - 以「对话框是否关闭」作为发送成功的判断依据；
  - 如果对话框关闭，视为发送成功。

示例（自然语言）：

> 本轮在 X 首页完成了 2 条高质量互动：
> 
> 1. **@某 AI 开发者**（1 小时前，35 回复）  
>    话题：LangChain vs Semantic Kernel  
>    评论：「这两个框架的定位其实不同，LangChain 偏快速原型，SK 更适合企业级。我们项目里混用，用 LC 做 POC，SK 做生产。你们有考虑过混合方案吗？」  
>    类型：**提供价值 + 提问**（110 字）
> 
> 2. **@某加密分析师**（30 分钟前，18 回复）  
>    话题：BTC 短期波动分析  
>    评论：「技术分析在加密市场作用有限，尤其是链上数据和宏观政策更有预测力。上次 ETF 通过前夕就是典型案例，TA 根本没捕捉到。」  
>    类型：**制造对立**（68 字）

---

## 4. 互动闭环跟踪（可选增强功能）

为了实现真正的互动闭环，可以在 workspace 中维护一个状态文件：

**文件路径**：`~/.openclaw/workspace/skills/x-comment/interaction-state.json`

**结构示例**：

```json
{
  "pendingReplies": [
    {
      "tweetUrl": "https://x.com/user/status/123456",
      "myCommentTime": 1773533956000,
      "author": "@某开发者",
      "topic": "AI agent 框架",
      "checkCount": 0,
      "lastChecked": null
    }
  ],
  "completedThreads": [
    {
      "tweetUrl": "https://x.com/user/status/789012",
      "rounds": 3,
      "finalStatus": "author-replied-back"
    }
  ]
}
```

**跟踪策略**：

1. 每次发送评论后，将 tweet 加入 `pendingReplies`
2. 在后续 cron job 中：
   - 检查 `pendingReplies` 中是否有作者回复（通过访问 tweet 详情页，检查作者是否回复了我的评论）
   - 如果有回复，**优先对这些内容进行二次互动**
   - 如果 3 次检查后仍无回复，移入 `completedThreads` 标记为 `no-author-reply`
3. 二次互动评论同样遵循「高质量」标准，避免简单的「感谢回复」

---

## 5. 清理与关闭

完成所有评论后，**关闭浏览器 tab**：

```jsonc
{
  "action": "close",
  "targetId": "<page-id>"
}
```

这样可以释放资源，避免后台累积过多标签页。

---

## 6. 技术要点总结

- **输入方式**：必须用 `browser act` + `type` + `slowly: true`，不能用 evaluate 脚本注入
- **发送方式**：用 evaluate 点击 Reply 按钮（`btn.click()`）
- **成功判断**：对话框关闭（`dialogExists: false`）即为发送成功
- **默认行为**：全自动，输入完成后直接发送，不询问用户确认
- **质量优先**：宁可少评论，也要保证每条都是高质量（50-150 字，有实质内容）
- **互动闭环**：维护状态文件跟踪作者回复，优先二次互动形成对话
- **任务结束**：所有评论完成后关闭浏览器 tab，释放资源
