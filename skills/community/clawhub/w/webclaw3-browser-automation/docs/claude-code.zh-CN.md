# 在 Claude Code 中使用 webclaw3

[English](./claude-code.md) | **中文**

一切都在 Claude Code 的对话框里完成——你说话，它跑命令。

**0. 两个一次性前置**（要你自己动手）：

- 装 Chrome 扩展：下载并解压 [wc3-chrome-extension-2.0.0.zip](https://github.com/fatmind/webclaw3/blob/main/dist/wc3-chrome-extension-2.0.0.zip)，打开 `chrome://extensions/` 开「开发者模式」→「加载已解压的扩展程序」→ 选刚解压后的文件夹
- 到 [webclaw3.com](https://webclaw3.com) 登录拿 Access Key——生成扣次数、拉站点经验库都靠它

**1. 安装 + 检查环境**——说一句：

```
帮我安装 webclaw3（https://github.com/fatmind/webclaw3），装好检查一下环境
```

Claude Code 会把仓库装进 `~/.claude/skills/webclaw3`、拉起本地服务，并引导你完成基本配置（填入刚拿的 Access Key、确认生成 skill 的存放目录等）。

**2. 开始使用**——之后全是对话：

- 探索：`帮我看看 https://example.com 的热榜都有什么` → 边跑边调，直到就是你要的
- 提炼：`把刚才这个提炼成 skill，我以后要每天跑`（第一次它会引导你去 [webclaw3.com](https://webclaw3.com) 拿 Access Key）
- 日常跑：`/skill名 跑一下`，或配成定时任务
- 修复：把报错甩给它，本地直接修

完整流程和示例见 [README](../README.zh-CN.md#快速上手)。
