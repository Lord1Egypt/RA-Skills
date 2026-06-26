# XHS 运行规则（引用自技能主文）

## 0.1 低 token 与快照约束

- 优先 `evaluate`，减少无意义 dump 与重复抓取。
- 只在关键节点做快照：登录确认、到发布页、填写完成、发布前停顿。
- 避免 `fullPage`（除用户要求整页归档）；重复调用优先复用同一 `targetId`。
- 每个动作最多重试 1 次；第二次失败改稳健路径并汇报。
- 记录关键证据：账号名、页面状态、按钮可见、字数等，返回可执行信号。

## 0.2 浏览器稳定规则（最高优先）

- 默认仅用内置浏览器：`profile="openclaw"`。
- 每次动作前先确认会话目标 tab（`browser.start --profile openclaw` 后再 `open/snapshot`）。
- 若出现 `no tab is connected`、`profile "chrome"` 等异常，立刻切回 `openclaw` 并重试。
- 连续 2 次点击/导航失败后改稳健路径（如直达点击改为 evaluate+定位），不做盲重试。

## 3.5 搜索并浏览（核心约束）

1. 仅从搜索结果页点击进入帖子，禁止直接 `navigate` 到 `/explore/<id>`。
2. 默认跳过本账号作者内容（避免自刷）。
3. 进入后先校验：不是 404、可见评论/互动信息、可识别标题或作者。
4. 进入方式优先点卡片本体，避免点头像/作者名导致跳错。
5. 若评论控件为 `contenteditable` 或 `p.content-input`，需先触发输入事件再发送。
6. 两条点击失败或 404 后返回搜索页换下一条，不对同链接直跳重试。

## 5.0 轮播图与评论区输入规则

### 5.1 轮播图抓取

只取当前活跃帧，排除 Swiper 克隆节点（避免重复抓取）：

```js
// 正确做法：过滤掉 duplicate 帧
const slides = document.querySelectorAll(
  '.swiper-slide-active:not(.swiper-slide-duplicate)'
);
```

- 不要用 `.swiper-slide` 全量选取，会包含无效的克隆帧
- 轮播图图片 URL 在 `img[src]` 或 `[data-src]`（懒加载时取 data-src）

### 5.2 评论区 contenteditable 输入

小红书评论框为 `contenteditable`，需触发 input 事件才能让平台识别文字：

```js
// 正确做法：execCommand + InputEvent
const el = document.querySelector('[contenteditable="true"]');
el.focus();
document.execCommand('insertText', false, '回复内容');
el.dispatchEvent(new InputEvent('input', { bubbles: true }));
```

- 禁止直接赋值 `el.textContent = '...'`（平台无法识别，发送按钮不激活）
- 禁止用 `act(kind=type)` 操作富文本评论框（已知失败）
- 若上述方法仍不激活发送按钮，改为手动：产出回复文案，通知老板粘贴

## 6.0 回放与降级

- 若搜索结构变化先 snapshot 更新 selector 再继续，不盲跑旧路径。
- 关键页（创作页、探索页、用户页）尽量复用已打开 tab，不重复 `open`。
- 先告诉用户“已达异常节点”，避免无意义继续操作导致误发。
