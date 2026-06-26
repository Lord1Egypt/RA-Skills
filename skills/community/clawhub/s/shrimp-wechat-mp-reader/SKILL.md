---
name: wechat-mp-reader
description: 直接读取微信公众号文章正文的可执行 skill。适用于用户提供 mp.weixin.qq.com 链接，并明确要你读正文、摘录内容、提取标题、做总结的场景。与很多只给方法或提示词的同类 skill 不同，这个 skill 自带 setup、run 和 Playwright 提取脚本，已经在真实文章上验证能读出标题和正文，不是停留在思路层。
---

# WeChat MP Reader

## 这是什么
这是一个**能直接安装、直接运行、直接读出公众号正文**的微信公众号读取 skill。

## 推荐标题
- 直接读出公众号正文｜可安装可运行版
- 微信公众号正文读取器｜装上就能跑
- WeChat Article Reader That Actually Runs

当用户提供 `mp.weixin.qq.com` 文章链接，并要求：
- 读取正文
- 提取标题
- 摘录内容
- 总结公众号文章

优先使用这条 skill。

## 这个 skill 的优势
- 不只是告诉你“可以用 Playwright”
- 不只是给一段方法说明
- 不只是一个 prompt 型 skill
- **而是已经把 setup、run、提取脚本都做完了**
- **并且已经在真实公众号文章上验证成功读出标题和正文**

## 为什么值得装
很多同类微信公众号 skill 会停在：
- 给思路
- 给方法
- 给 prompt
- 让你自己补环境
- 装完也不一定本地能跑

这个 skill 解决的是另一件事：
> **把“公众号文章读取”从一种方法，变成一个可执行、可验证、可复用的本地能力。**

## 你真正会得到什么
- 直接安装
- 直接运行
- 直接读出公众号文章标题和正文
- 不再停在“方法我懂了，但本地还是跑不起来”

## CTA
如果你要的不是教程，而是现在就把公众号正文读出来，这个 skill 值得直接装上。

## 目标
通过 Playwright 模拟真实浏览器渲染公众号文章页，提取：
- 标题
- 正文纯文本

## 使用条件
- 本地 Node 可用
- Playwright 可安装/可运行
- skill 目录可独立安装依赖并独立运行

## 标准目录
- `SKILL.md`
- `_meta.json`
- `package.json`
- `run.sh`
- `scripts/setup.sh`
- `scripts/extract.js`
- `README.md`

## 执行步骤
1. 进入 skill 目录：
   - `/home/baiwan/.openclaw/workspace-assistant-shrimp/skills/wechat-mp-reader`
2. 初始化环境：
   - `bash scripts/setup.sh`
3. 执行读取：
   - `bash run.sh <mp.weixin.qq.com文章链接>`
4. 从 JSON 输出中读取：
   - `title`
   - `bodyText`

## 产物路径
- skill 目录：`/home/baiwan/.openclaw/workspace-assistant-shrimp/skills/wechat-mp-reader`
- 提取脚本：`/home/baiwan/.openclaw/workspace-assistant-shrimp/skills/wechat-mp-reader/scripts/extract.js`
- 安装脚本：`/home/baiwan/.openclaw/workspace-assistant-shrimp/skills/wechat-mp-reader/scripts/setup.sh`
- 执行入口：`/home/baiwan/.openclaw/workspace-assistant-shrimp/skills/wechat-mp-reader/run.sh`

## 成功判定
满足以下任一条件可视为成功：
- 读到公众号文章标题和正文前 1000+ 字
- 输出 JSON 中包含有效 `title` 和明显属于正文内容的 `bodyText`

## 失败判定
以下情况视为失败：
- 微信风控页（环境异常 / 滑块）
- Playwright 浏览器未安装且安装失败
- 页面只返回壳内容，无正文

## 结果汇报格式
只汇报：
1. 产物路径
2. 执行命令
3. 结果是否成功
4. 标题
5. 正文摘录

不要把查资料、看文档、搜索方向算作结果。