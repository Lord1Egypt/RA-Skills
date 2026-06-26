# 知乎问答爬虫

按关键词搜索知乎问题，自动抓取高回答数的问题及其全部回答，保存为 JSON 和纯文本。

## 快速开始

```bash
# 安装依赖
pip install requests

# 运行（将 Cookie 替换为你自己的）
python zhihu_crawl.py --cookie "你的知乎Cookie" --keywords "丰川祥子" --top 100
```

## 如何获取 Cookie

1. 浏览器打开 [zhihu.com](https://www.zhihu.com) 并登录
2. 按 `F12` → **Network（网络）** 标签
3. 点击任意知乎页面请求 → **Request Headers**
4. 找到 `cookie:` 那行，复制冒号后的全部内容

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--cookie` | ✅ | — | 知乎登录 Cookie |
| `--keywords` | — | MyGO Ave Mujica 丰川祥子 | 搜索关键词，多个用空格分隔 |
| `--top` | — | 100 | 取回答数最多的前 N 个问题 |
| `--output` | — | zhihu_output | 输出目录 |
| `--search-max` | — | 200 | 每个关键词最多搜索多少候选 |

## 输出

```
zhihu_output/
├── question_{id}.json     # 每题完整数据（含全部回答）
├── _question_list.json    # 问题列表（按回答数排序）
└── _merged_all.txt        # 所有内容合并纯文本
```

## 示例

```bash
# 单关键词
python zhihu_crawl.py --cookie "abc..." --keywords "高松灯" --top 50

# 多关键词，自定义输出目录
python zhihu_crawl.py --cookie "abc..." \
  --keywords "MyGO" "Ave Mujica" "丰川祥子" \
  --top 200 \
  --output ./mygo_data

# Windows PowerShell（若有 SSL 报错先加这行）
$env:PATH = "C:\python\anaconda\Library\bin;" + $env:PATH
python zhihu_crawl.py --cookie "abc..." --keywords "丰川祥子" --top 100
```

## 工作原理

1. 对每个关键词调用知乎搜索 API，收集候选问题
2. 跨关键词去重，按回答数降序排列，取前 N 名
3. 对每个问题分页抓取全部回答
4. 保存 JSON + 合并纯文本

## 注意事项

- Cookie 有时效性，失效（HTTP 403）时需重新复制
- 抓取间隔已设置礼貌延迟（2s/题），请勿并发运行多个实例
- 仅供个人学习研究使用
