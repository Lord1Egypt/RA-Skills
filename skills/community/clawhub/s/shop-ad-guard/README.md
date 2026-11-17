# 电商广告合规护栏 (shop-ad-guard)

在商品标题、详情页、直播话术、促销文案**发布前**，实时检测高频违规用语，按风险分级
输出命中与整改建议。纯本地运行，零网络请求。

## 快速开始

```bash
# 检测一段文案
python3 scripts/guard.py --text "本产品是国家级最佳减肥神器，销量第一"

# 从标准输入读取
echo "全网最低价限时特惠最后一天" | python3 scripts/guard.py --stdin

# 结构化 JSON 输出
python3 scripts/guard.py --text "..." --format json

# 列出违规类别与依据
python3 scripts/guard.py --list-categories
```

## 检测类别

| 类别 | 风险 | 主要依据 |
|------|------|----------|
| 绝对化用语 | high | 广告法第九条（罚款 20 万起） |
| 医疗功效违规宣称 | high | 广告法第十七条 |
| 虚假/夸大宣传 | medium | 广告法第四条 |
| 虚假促销用语 | medium | 价格法 / 反不正当竞争法 |
| 比较/贬低用语 | medium | 广告法第十三条 |
| 迷信/诱导用语 | low | 广告法导向要求 |

## 与 shop-ad-check-pro 的关系

本护栏是**免费、实时**的高频拦截；`shop-ad-check-pro` 是**付费、深度**的四大模块
22 项审计。日常发文用 guard，上架前大促用 audit，组合即"轻 guard + 重 audit"。

## 扩展规则

编辑 `scripts/rules/terms.py`，在 `TERMS` 中按 `(term, category, severity, suggestion)`
追加即可，内核无需改动。

## 声明

本工具仅供合规自查辅助，**不构成法律建议**。详见 `SKILL.md` 法律声明。
