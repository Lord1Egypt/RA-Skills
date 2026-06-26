# 示例文章：AutoClaw 测评

## BREAKING
- strikethrough: 各种折腾装龙虾
- bold: 智谱亲自下场
- highlight: 3分钟装好龙虾
- subtitle: 养虾不求人
- date: 2026.03

👉 滑动查看更多

## PART 01 精装满血版

AutoClaw 相当于精装交付，龙虾本体的能力一个没少，智谱还帮你预装了 50+ 热门 Skill：浏览器自动化、深度调研、联网搜索、AI 生图……装完直接能干活，相当于是满血增强版。

> [警告] 迁移完之后别同时开两只龙虾——两者默认用同一个本地网关端口 18789，会互相打架导致飞书消息收不到。

> [技术] 把原版龙虾端口改成 19001，让龙虾帮你改，一行配置的事。不双开就完全不用管这个。

## PART 02 快速上手

### STEP 01 安装

下载 AutoClaw → 打开 → 注册登录 → 就这么简单。

没有终端、没有命令行、没有环境配置。AutoClaw 是个启动器，所有运行环境它帮你自动配好。就像给手机装 app 一样简单。

### STEP 02 飞书对接

这是我觉得最惊喜的地方。以前对接飞书是最折腾的一步，大概要十几步操作，中间任何一步出错都可能配不通，现在呢？

点一下 接入飞书 → 登录二维码 → 飞书扫一下 → 全自动配置。再也不需要去折腾各种飞书配置了，所有这些 AutoClaw 全部帮你自动搞定。

## 配置示例

```
# 龙虾配置文件示例
server:
  port: 19001
  gateway: 18789

model:
  name: "Pony-Alpha-2"
  provider: "zhipu"
  temperature: 0.7

skills:
  - AutoGLM-Browser-Agent
  - AutoGLM-DeepResearch
  - AI-Image-Generation
```

## PART 03 总结

先上车，再慢慢折腾。方向是对的，谁能把门槛降到最低就很重要。

