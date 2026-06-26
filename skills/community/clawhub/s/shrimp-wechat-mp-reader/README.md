# wechat-mp-reader

## 产品定位
一个**可直接安装、可直接运行、已验证能读出公众号正文**的微信公众号读取 skill。

### 一句话卖点
直接安装、直接运行、直接读出公众号正文。不是只给方法，而是已经把 setup、run 和验证成功的提取链都做好了。

### 和同类 skill 相比，这个 skill 多做了什么
- 不只给方法
- 不只给 prompt
- 不只告诉你“可以用 Playwright”
- 而是直接带：
  - setup 脚本
  - run 入口
  - 提取脚本
  - 已验证成功的读取链
  - 可直接复现的安装与运行路径

### 为什么值得装
- 很多同类 skill 只告诉你怎么做
- 这个 skill 已经把“装上就能跑”的链路做完了
- 已在真实公众号文章上验证成功读出标题和正文

### CTA
如果你要的是结果，不是教程，这个 skill 值得直接装上。

## 产物
- `SKILL.md`：skill 说明
- `_meta.json`：skill 元数据
- `package.json`：依赖定义
- `run.sh`：统一执行入口
- `scripts/setup.sh`：安装脚本
- `scripts/extract.js`：正文提取脚本

## 当前验证结果
### 已验证成功的直接脚本链
命令：
```bash
node /home/baiwan/.openclaw/workspace-assistant-shrimp/tmp/wechat-mp-crawler/extract.js https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw
```

结果：
- 成功读到标题：`分享6个我觉得应该必装的Skills。`
- 成功读到正文文本前段

### 当前 skill 包装入口验证（第一次）
命令：
```bash
/home/baiwan/.openclaw/workspace-assistant-shrimp/skills/wechat-mp-reader/run.sh https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw
```

结果：
```json
{
  "title": "Weixin Official Accounts Platform",
  "bodyText": ""
}
```

### 当前 skill 包装入口验证（修正后）
命令：
```bash
/home/baiwan/.openclaw/workspace-assistant-shrimp/skills/wechat-mp-reader/run.sh https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw
```

结果：
- 已成功输出与直接脚本链一致的正文长文本
- 已读到文章标题与正文主体

说明：
- skill 目录和可执行入口已封装完成
- `run.sh` 已修正浏览器缓存路径问题
- 当前 skill 入口已能复现直接脚本链结果
