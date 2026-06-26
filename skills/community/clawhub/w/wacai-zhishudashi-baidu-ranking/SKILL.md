---
name: zhishudashi-baidu-ranking
description: 抓取百度搜索关键词“指数大师”的搜索结果标题，并按从前到后的顺序整理成编号列表，再通过企业微信机器人 webhook 推送。用于日报、定时巡检、品牌词/关键词排名观察、搜索结果快照汇报，尤其适合需要“打开浏览器→搜索→提取标题→推送消息”这一固定流程时。
---

# 指数大师百度排名日报

## 概览

执行固定流程：打开百度，搜索“指数大师”，提取结果页主结果标题，生成编号列表，并发送到企业微信机器人。

## 工作流

1. 用 `browser` 打开 `https://www.baidu.com/`。
2. 在搜索框输入 `指数大师` 并提交搜索。
3. 从结果页顶部到底部，提取每条主结果的标题。
4. 用 `scripts/push_wecom.py` 发送推送。
5. 向用户返回已抓取的标题列表；若已推送，说明推送成功。

## 浏览器执行规则

- 优先用 `browser` 工具，不要改用人工描述。
- 若用户明确要求使用现有 Chrome 标签页、Browser Relay 或工具栏接管，使用 `profile: "chrome"`；否则可以使用隔离浏览器。
- 搜索后等待结果页稳定再提取。
- 只提取“主结果标题”：
  - 包含清晰可点击标题的结果卡片。
  - 按页面视觉顺序从上到下。
  - 跳过搜索框、分页、相关搜索、热榜、推荐视频、问答摘要等非主结果区域。
- 若页面顶部存在带明确标题的广告位，默认跳过；除非用户明确要求“连广告一起统计”。

## 提取方式

按以下顺序执行：

1. `browser.snapshot` 查看结果页结构。
2. 若 snapshot 已清楚给出结果标题，直接整理。
3. 若结构复杂，用 `browser.act` 的 `evaluate` 读取页面上的结果标题文本。
4. 若标题重复，按页面出现顺序保留，不去重。

## 输出格式

发送到 webhook 的正文固定为：

```text
标题的列表：
1. 标题1
2. 标题2
3. 标题3
```

不要把额外解释写进 webhook 文本。

## 推送

优先使用脚本：

```bash
python3 scripts/push_wecom.py --title "标题1" --title "标题2"
```

或从 stdin 逐行读取：

```bash
printf '%s\n' "标题1" "标题2" | python3 scripts/push_wecom.py --stdin
```

如需直接发 HTTP，可使用：

```bash
curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0e41994e-9e62-4713-ad69-fddeaaba8e9a' \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "百度首页主标题列表：\n1. 标题1\n2. 标题2\n3. 标题3"
    }
  }'
```

## 失败处理

- 如果百度首页未正常加载：重试一次，再报告失败原因。
- 如果结果页没有可提取标题：截图或快照后报告“未提取到结果标题”，不要发送空推送。
- 如果 webhook 返回非 `errcode: 0`：把响应摘要给用户。
- 如果只提取到部分标题：按已提取内容继续生成列表，并说明是部分结果。

## 资源

### scripts/push_wecom.py

发送企业微信机器人文本消息。

- 默认 webhook 已内置为本技能使用的地址。
- 支持 `--title` 重复传参。
- 支持 `--stdin` 从标准输入逐行读取标题。
- 支持 `--dry-run` 仅打印 payload，不实际发送。
