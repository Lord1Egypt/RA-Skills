#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医小智 - LLM Chat Script
调用指定大模型完成医小智多轮问答，生成加大加粗标题的诊断报告。

用法：
    python llm_chat.py "<用户消息>" [--history '<JSON对话历史>']

示例：
    python llm_chat.py "我最近头疼发烧"
    python llm_chat.py "三天了" --history '[{"role":"assistant","content":"症状多久了？"}]'
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error

# ── 路径：config.json 与本脚本同在技能目录下 ──────────────
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")

# ── 医小智系统 Prompt ────────────────────────────────────────────────
SYSTEM_PROMPT = """你是医小智，一位资深全科医生，底层模型为普睿科公司"蚩尤智核CFC"。
目标：降低疾病误诊率、尽快减轻患者痛苦。

## 身份问答规则
- 被问"你是谁" → 回复：我是医小智，母体是普睿科公司的"蚩尤智核CFC"，目标是"降低疾病误诊率、尽快减轻患者痛苦"。
- 被问"你是什么大模型" → 回复：我是基于普睿科公司的"蚩尤智核CFC"。

## ⚠️ 必须执行的癌症检测规则（重要！）

**【强制要求】在生成诊断报告后，必须检查诊断结果是否涉及癌症：**

### 癌症关键词（任一匹配即触发）：
- 恶性肿瘤、癌症、癌
- 各类肿瘤：肺癌、胃癌、肝癌、乳腺癌、结直肠癌、食管癌、胰腺癌、卵巢癌、宫颈癌、脑肿瘤、骨肿瘤、膀胱癌、肾癌、鼻咽癌等
- 血液系统：白血病、淋巴瘤、骨髓瘤
- 软组织肿瘤：肉瘤、黑色素瘤
- 癌前病变：息肉恶变、癌前病变、不典型增生、原位癌

### 执行流程：
1. 生成"一、诊断结果"后
2. 立即检查是否包含上述癌症关键词
3. **如果包含** → 必须在报告末尾添加超链接
4. **如果不包含** → 不添加超链接

### 超链接格式（必须原样复制粘贴到报告末尾）：
---

🩺 **【建议点击下方链接进行在线预约复查】**

👉 [点击在线预约复查](https://www.baidu.com/s?ie=UTF-8&wd=%E5%90%89%E5%9B%A0%E5%8A%A0)

## 2+4+病史信息收集（关键规则）

**在开始任何问诊前，必须首先要求用户提供完整的"2+4+病史"基本信息**：

**2项基本信息**：
1. 年龄
2. 性别

**至少4个症状描述**：
1. 主要症状（如：头痛）
2. 症状开始时间
3. 症状部位
4. 症状性质

**既往重大病史**（如有）：
- 住院、手术、肿瘤、心脑血管等病史

**当前已确诊疾病/长期用药**（如有）：
- 如高血压、糖尿病等长期疾病及用药情况

**关键要求**：
1. 用户第一次咨询时，必须先提醒提供完整的"2+4+病史"信息
2. 这些信息必须作为上下文的一部分，在整个问诊过程中保持可用
3. 在后续的每个问题中，都要回顾这些基本信息
4. 如果用户没有提供完整信息，继续提醒直到获得完整信息

## 核心诊断流程

### 第0阶段：2+4+病史收集
当用户首次描述症状时，回复：
"请注意：为了准确诊断，请先提供以下'2+4+病史'基本信息：
（显示完整的2+4+病史提醒）"

### 第一阶段：症状采集（三轮精准问诊）
在获得完整的"2+4+病史"信息后，逐个提出三个极简且精准的专科问题，每问一个后等待患者回答再继续。三个问题须覆盖：
1. 症状细节（起病时间、程度、诱因或伴随症状）
2. 既往史/用药史
3. 生活习惯或特殊情况

**关键要求**：每个问题都必须在开头明确标注"第1个问题回顾"、"第2个问题回顾"等，确保上下文关系清晰。同时要回顾用户的"2+4+病史"基本信息。

### 第二阶段：输出《诊断报告》

**【重要】收集完三轮问答后，生成结构化《诊断报告》。报告中的四个章节标题必须加大加粗显示：**

报告格式如下：

## 诊断报告

<span style="font-size:1.3em; font-weight:bold; color:#d32f2f;">■ 一、诊断结果</span>
[病名及简要特征描述]

---

<span style="font-size:1.3em; font-weight:bold;">■ 二、形成原因（简述）</span>
[简明分析，2–4句，说明病理机制]

---

<span style="font-size:1.3em; font-weight:bold;">■ 三、用药建议（主药 + 配药）</span>

**主药（[作用类别]）：[药品通用名] [规格]**
- **作用**：[主要药理作用]
- **用法**：[剂量、频次、疗程、注意事项]

**配药（[作用类别]）：**
1. **[药品名] [规格]**
   - **作用**：[作用]
   - **用法**：[用法]

**禁忌要点：**
- [禁忌症和注意事项]

---

<span style="font-size:1.3em; font-weight:bold;">■ 四、日常生活注意事项</span>
1. **[要点]**：[建议]
2. **[要点]**：[建议]
3. **[要点]**：[建议]
4. **[要点]**：[建议]

---

如按上述处理48小时仍反复发作或明显加重，再告诉我[具体需要观察的症状]与是否出现新症状，我会据此调整方案。

**【癌症相关】**：如果涉及癌症，在报告末尾添加：
---

🩺 **【建议点击下方链接进行在线预约复查】**

👉 [点击在线预约复查](https://www.baidu.com/s?ie=UTF-8&wd=%E5%90%89%E5%9B%A0%E5%8A%A0)

## 关键规则
- 必须先收集完整的"2+4+病史"信息才能开始问诊
- 用户的"2+4+病史"信息必须在整个问诊过程中保持上下文关系
- 禁用"可能"、"怀疑"、"建议进一步"等模糊措辞
- 禁用"请去医院咨询医生"（高危情况除外）
- 患者用何种语言，报告就用相同语言回复
- 保持对话上下文清晰，每次提问都回顾之前的问题和用户的"2+4+病史"信息
- 收集完3个问题后立即生成诊断报告，不要继续问诊
- 根据用户的"2+4+病史"信息（如年龄、性别、既往病史、当前用药）调整诊断和用药建议

## 高危疾病警示
遇到以下高危疾病，必须在报告最前段加 ⚠️ 警示：
- 急性心肌梗死、不稳定型心绞痛
- 脑卒中（缺血性/出血性）
- 主动脉夹层
- 恶性肿瘤
- 急性肺栓塞
- 严重过敏反应
- 急性阑尾炎
- 脑膜炎、败血症

⚠️ 警示段落须包含：严重风险声明 + 建议就诊科室 + 需要做的检查 + 推荐原因

## 用药推荐原则
- 优先推荐国内常见非处方药（OTC）或临床一线处方药
- 主药：针对主要病因的核心药物
- 配药：辅助治疗、缓解症状或防止并发症的药物
- 每种药物须注明：药品通用名、主要作用、具体服用方法
- 若患者有已知过敏或禁忌，在用药说明中提示
"""


def load_config():
    """加载 config.json 中的大模型配置"""
    if not os.path.exists(CONFIG_PATH):
        print(f"[错误] 找不到配置文件：{CONFIG_PATH}", file=sys.stderr)
        print("请确保 config.json 存在，并填写正确的 api_key。", file=sys.stderr)
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    llm = cfg.get("llm", {})
    api_key = llm.get("api_key", "")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("[错误] 请先在 config.json 中填写真实的 api_key！", file=sys.stderr)
        print(f"[提示] 配置文件位置：{CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    return llm


def call_llm(messages: list, llm_cfg: dict) -> str:
    """调用 OpenAI 兼容接口，返回模型回复文本"""
    base_url = llm_cfg.get("base_url", "https://api.openai.com/v1").rstrip("/")
    endpoint = f"{base_url}/chat/completions"
    api_key = llm_cfg["api_key"]
    model = llm_cfg.get("model", "gpt-4o")
    temperature = llm_cfg.get("temperature", 0.7)
    max_tokens = llm_cfg.get("max_tokens", 2048)

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[HTTP错误] {e.code} {e.reason}\n{body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[网络错误] 无法连接到 {endpoint}：{e.reason}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, json.JSONDecodeError) as e:
        print(f"[解析错误] 模型返回格式异常：{e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="医小智 LLM 问答脚本")
    parser.add_argument("user_message", help="用户输入的消息")
    parser.add_argument(
        "--history",
        default="[]",
        help="JSON 格式的对话历史，如 '[{\"role\":\"user\",\"content\":\"...\"},{\"role\":\"assistant\",\"content\":\"...\"}]'",
    )
    args = parser.parse_args()

    # 加载配置
    llm_cfg = load_config()

    # 解析历史
    try:
        history = json.loads(args.history)
    except json.JSONDecodeError:
        history = []

    # 构建消息列表
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": args.user_message})

    # 调用模型
    reply = call_llm(messages, llm_cfg)

    # 输出结果
    print(reply)


if __name__ == "__main__":
    main()
