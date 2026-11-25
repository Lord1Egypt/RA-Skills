# 环境与常见问题

## TOKEN

环境变量名是 `GUAIKEI_API_TOKEN`。16-256 位，只含字母、数字、下划线和连字符。在 https://www.guaikei.com 开通微博热搜、微博搜索、微博评论后再跑对应命令。

未配置时命令直接 `AUTH_REQUIRED`，不会发请求。

## 工作目录

技能根是含 `SKILL.md` 和 `package.json` 的目录。Agent 用绝对路径：

```bat
node "D:\Git\weibo-skill\scripts\weibo\search-cli.js" --keyword "AI"
```

已经 `cd` 到技能根时，`node scripts\weibo\search-cli.js` 也可以。

## Windows 引号

cmd 包住带空格或中文的参数时只用双引号。仍然被拆开时，改用 `--json-args`，并且不要再混其它 flag。

PowerShell：

```powershell
node scripts/weibo/search-cli.js --json-args '{"keyword":"AI 教程","search_type":1,"limit":10}'
```

## 要等多久

三条命令都是先创建任务再查询。查询返回「处理中」会继续等，大约 20 次，间隔从 2 秒翻倍，单次最长 60 秒。大约 100 条搜索或评论通常几分钟；大约 1000 条要更久。热搜通常更快，仍可能要几分钟。进程没退出就还在等。

次数用尽仍在处理 → `TIMEOUT`。用完全相同的参数再跑一次是续等，不是新开一份不同的任务。

## 结果存在哪

默认只打到 stdout。`--save` 或 `GUAIKEI_ENABLE_LOG=1` 时，完整 JSON 写到系统临时目录下的 `weibo-guaikei/logs/当天日期/`。

## 和抖音技能的差别

本技能只有热搜、搜索、评论。没有用户主页作品列表，也没有单条详情。微博热搜是异步任务，必须等进程结束。搜索类型是 1-7，评论排序是 0 热度、1 时间。
