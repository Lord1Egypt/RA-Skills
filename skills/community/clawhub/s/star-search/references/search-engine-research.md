# Search Engine Research — 实测数据汇总

**测试时间**: 2026-05-09
**测试环境**: macOS, Camoufox v135, Camofox REST API
**测试query**: "AI API token resale market"

## 全引擎测试结果

| 引擎 | URL模板 | 结果数 | 验证码 | URL类型 | 推荐 |
|------|---------|--------|---------|---------|------|
| **搜狗** | `https://www.sogou.com/web?query={q}&ie=utf8` | **10** | 无 | JS跳转链 | ✅ 主引擎 |
| **百度** | `https://www.baidu.com/s?wd={q}` | **9** | 随机 | 真实URL | ✅ 备选 |
| **360** | `https://www.so.com/s?q={q}` | **6** | 无 | JS跳转链 | ⚠️ 补充 |
| 神马 | `https://m.sm.cn/s?q={q}` | 0 | — | — | ❌ |
| Bing中国 | `https://cn.bing.com/search?q={q}` | 0 | — | — | ❌ |
| Bing国际 | `https://www.bing.com/search?q={q}` | 0 | — | — | ❌ |
| Google | `https://www.google.com/search?q={q}` | 超时 | — | — | ❌ |
| DuckDuckGo | `https://duckduckgo.com/?q={q}` | 超时 | — | — | ❌ |
| Brave | `https://search.brave.com/search?q={q}` | 超时 | — | — | ❌ |
| Startpage | `https://www.startpage.com/do/search?q={q}` | 超时 | — | — | ❌ |
| Naver | `https://search.naver.com/search.naver?query={q}` | 超时 | — | — | ❌ |
| Yandex | `https://yandex.com/search/?text={q}` | 4 | 无 | 真实URL | 仅英文 |

## URL类型说明

### 真实URL（Baidu）
```
http://www.baidu.com/link?url=xxxxxxxxxxxx
```
通过HTTP请求可直接跟踪到真实目标地址。

### JS跳转链（Sogou/360）
```
https://www.sogou.com/link?url=hedJjaC291OHSfRZxx--pdfZ45aIPvhNrynoH4S1IZp3dsjpqTIyDdYe-yQx-7HpcIz44lfNwViJLl
https://www.so.com/link?m=eQUM3VzYEL0KkrC2Th1ogvJEPne2l3da0PF74tZeJf5hvLk8G8m0ynlz7puTSlXm
```
Python `urllib.request.urlopen()` 跟踪后停在跳转页，无法获取最终地址。
在真实浏览器中点击可正常跳转。

**对搜索结果展示无影响** — 浏览器内点击不受影响，仅影响程序化URL解析。

## 验证码触发规律

| 查询类型 | 示例 | Baidu验证码概率 |
|---------|------|----------------|
| 简单通用词 | test, hello, search | 高 |
| 长尾具体词 | AI API token 转售 市场 | 低 |
| 中文+英文混合 | AI API token resale market | 中 |

**结论**: 使用具体、描述性的搜索词可显著降低验证码触发率。

## 搜狗结果质量分析

```
1. AI API token resale market的更多内容_CSDN技术社区
2. TOKEN自由-Ai Token平台|大模型Ai Token 供应与特价平台|免费TOKEN
3. API Token Authentication for Jira expand conne...| Atlassian
4. 知识 - AI应用,AI模型API,第三方整合、Token 流转之间的关系说明
5. Open AI API价格以及使用说明_知乎
6. API渠道汇总,免费Token获取指南!!
7. APIPark 新增 AI 大模型负载均衡,APIKey 资源池以及 AI Token 消耗统...
8. 什么是Token？一文看懂AI世界的"语言积木"-AI Token - 今日头条
9. 刚刚,OpenAI推出最贵o1-pro API！千倍于DeepSeek
10. 图像识别 - 通用物体和场景识别 | 百度AI开放平台
```
来源: CSDN、知乎、腾讯云、今日头条、Atlassian — 高质量中文来源为主。

## 360结果质量分析

```
1. China warns of digital AI 'token' risks - Chinadaily.com.cn
2. ai api token resale market - 360翻译
3. 智谱API涨价83%,AI的免费午餐真的结束了?
4. 最懂大模型的人也逃不过杀猪盘?API生意背后的灰产链条
5. AI大模型DeepSeek-V3 API售后调整:输出Token费用暴涨至8元
6. OpenAI图像生成模型API发布,Token计价,一张图花掉1.4元
```
来源混合: 中国日报、澎湃、腾讯 — 有内容深度。
