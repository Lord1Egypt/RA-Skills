#!/usr/bin/env python3
"""
新闻流事件驱动选股分析引擎
使用百度千帆 API 对财经新闻进行深度分析，输出结构化选股信号。

用法:
    echo '新闻内容' | python3 news_analyzer.py
    python3 news_analyzer.py -t "新闻内容"
    python3 news_analyzer.py -f news.txt
    python3 news_analyzer.py -t "新闻内容" -m deepseek-v4-pro
    python3 news_analyzer.py -t "新闻内容" --raw  # 输出原始API响应
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# ─── 百度千帆 API 配置 ───
QIANFAN_API_KEY = os.environ.get("QIANFAN_API_KEY")
if not QIANFAN_API_KEY:
    print("错误：请设置环境变量 QIANFAN_API_KEY（百度千帆 API Key）", file=sys.stderr)
    sys.exit(1)
QIANFAN_BASE_URL = "https://qianfan.baidubce.com/v2/chat/completions"
DEFAULT_MODEL = os.environ.get("QIANFAN_MODEL", "ernie-4.5-turbo-128k")

# ─── 系统提示词 ───
SYSTEM_PROMPT = """你是一位专业的A股事件驱动选股分析师。你的任务是对输入的财经新闻进行深度分析，输出结构化的选股信号。

## 分析框架

### 第一步：事件分类
将新闻归入以下类别之一：
- policy（政策类）：货币政策、财政政策、产业政策、监管新规
- earnings（财报类）：业绩超预期/不及预期、预告修正、分红方案
- industry（行业类）：供需变化、价格异动、技术突破、产能调整
- company（公司类）：并购重组、股权变动、高管变更、重大合同
- macro（宏观类）：GDP/CPI/PMI数据、国际经贸、汇率利率

### 第二步：影响判断
- 判断事件对市场整体的影响方向（利好/利空/中性）
- 判断影响的持续时间（短期情绪/中期趋势/长期逻辑）

### 第三步：受益标的匹配
按照以下逻辑筛选受益标的：
1. 直接受益（强信号）：公司主营业务与事件直接相关，收入占比>30%
2. 间接受益（中信号）：供应链上下游关联，或业务有部分涉及
3. 情绪受益（弱信号）：概念相关性，市场情绪可能炒作

对每个标的，说明：
- 股票代码和名称
- 受益逻辑（为什么受益）
- 信号强度（strong/medium/weak）
- 关注要点（需要验证的关键信息）

### 第四步：风险提示
- 列出主要风险因素
- 标注分析的不确定性来源

## 输出格式

严格输出以下JSON格式，不要添加其他文本：

```json
{
  "event_type": "policy|earnings|industry|company|macro",
  "event_title": "事件标题（一句话概括）",
  "event_summary": "事件摘要（2-3句话）",
  "market_impact": {
    "direction": "利好|利空|中性",
    "duration": "短期情绪|中期趋势|长期逻辑",
    "intensity": "high|medium|low"
  },
  "affected_sectors": [
    {"sector": "板块名称", "impact": "利好|利空", "reason": "原因"}
  ],
  "beneficiary_stocks": [
    {
      "code": "600000",
      "name": "股票名称",
      "signal": "strong|medium|weak",
      "logic": "受益逻辑说明",
      "key_point": "关注要点"
    }
  ],
  "risk_factors": ["风险因素1", "风险因素2"],
  "signal_summary": "综合信号评级：综合判断事件对市场的整体影响和操作建议（2-3句话）",
  "confidence": "high|medium|low",
  "disclaimer": "本分析由AI生成，仅供参考，不构成投资建议。投资有风险，入市需谨慎。"
}
```

## 注意事项
- 只输出JSON，不要输出其他内容
- 如果新闻内容不够明确，在event_summary中说明不确定性
- 受益标的尽量给出具体的A股代码和名称
- 如果无法确定具体标的，给出板块方向判断
- confidence反映对分析结论的把握程度"""


def call_qianfan_api(news_text: str, model: str = DEFAULT_MODEL, max_tokens: int = 8192) -> dict:
    """调用百度千帆 API 进行新闻分析"""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请分析以下财经新闻：\n\n{news_text}"}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        QIANFAN_BASE_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {QIANFAN_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}", "detail": error_body}
    except Exception as e:
        return {"error": str(e)}


def extract_analysis(api_response: dict) -> dict:
    """从API响应中提取分析结果"""
    if "error" in api_response:
        return api_response

    choices = api_response.get("choices", [])
    if not choices:
        return {"error": "No choices in response", "raw": api_response}

    message = choices[0].get("message", {})
    content = message.get("content", "")

    # Some models put everything in reasoning_content
    if not content and message.get("reasoning_content"):
        content = message.get("reasoning_content", "")

    # Try to parse JSON from content
    # Remove markdown code fences if present
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        analysis = json.loads(content)
    except json.JSONDecodeError:
        # If JSON parse fails, return raw content
        analysis = {
            "error": "Failed to parse JSON from model response",
            "raw_content": content[:2000],
        }

    # Add metadata
    if "error" not in analysis:
        analysis["_meta"] = {
            "model": api_response.get("model", "unknown"),
            "usage": api_response.get("usage", {}),
            "finish_reason": choices[0].get("finish_reason", "unknown"),
        }

    return analysis


def main():
    parser = argparse.ArgumentParser(description="新闻流事件驱动选股分析引擎")
    parser.add_argument("-t", "--text", help="新闻文本（直接传入）")
    parser.add_argument("-f", "--file", help="从文件读取新闻文本")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"模型名称（默认: {DEFAULT_MODEL}）")
    parser.add_argument("--max-tokens", type=int, default=8192, help="最大输出token数")
    parser.add_argument("--raw", action="store_true", help="输出原始API响应")
    args = parser.parse_args()

    # 获取新闻文本
    if args.text:
        news_text = args.text
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            news_text = f.read()
    elif not sys.stdin.isatty():
        news_text = sys.stdin.read()
    else:
        print("错误：请通过 -t、-f 或 stdin 提供新闻文本", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    news_text = news_text.strip()
    if not news_text:
        print("错误：新闻文本为空", file=sys.stderr)
        sys.exit(1)

    # 调用API
    api_response = call_qianfan_api(news_text, args.model, args.max_tokens)

    if args.raw:
        print(json.dumps(api_response, ensure_ascii=False, indent=2))
    else:
        analysis = extract_analysis(api_response)
        print(json.dumps(analysis, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
