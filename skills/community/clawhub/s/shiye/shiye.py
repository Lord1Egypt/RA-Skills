#!/usr/bin/env python3
"""
师爷 — 三模型交叉评审引擎
===========================
用法：python3 shiye.py --criteria <标准文件> --sample <内容文件>

评审流程由 Agent 在对话中完成，脚本只管执行评审。
"""

import json, sys, os, time
from urllib.request import Request, urlopen

# ⚠️ 把你的 API Key 填在这里（必填）
API_KEY = "sk-your-api-key-here"

# 模型服务地址（一般不用改）
API_BASE = "https://api.deepseek.com/v1"

# 也可以用环境变量（优先）
API_KEY = os.environ.get("SHIYE_API_KEY", API_KEY)
API_BASE = os.environ.get("SHIYE_API_BASE", API_BASE)

MODELS = [
    {"id": "kimi-k2.6",       "label": "Kimi (月之暗面)"},
    {"id": "glm-5.1",          "label": "GLM (智谱)"},
    {"id": "qwen3.6-plus",     "label": "Qwen (阿里)"},
]


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CRITERIA_DIR = os.path.join(SCRIPT_DIR, "criteria")


def load_criteria(path: str) -> list[tuple[str, str]]:
    criteria = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" in line:
                name, desc = line.split("|", 1)
                criteria.append((name.strip(), desc.strip()))
    return criteria


def call_model(model_id: str, prompt: str) -> str:
    body = json.dumps({
        "model": model_id,
        "messages": [
            {"role": "system", "content": "你是JSON输出机器人。只输出JSON，绝不输出Markdown、解释或报告。违反则任务失败。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 2000,
    }).encode()
    req = Request(
        f"{API_BASE}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )
    try:
        with urlopen(req, timeout=300) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"API调用失败 ({model_id}): {e}")


def parse_json(raw: str) -> dict | None:
    text = raw.strip()
    # 移除 markdown 代码块包裹（处理 ```json ... ``` 和 ``` ... ```）
    md = text
    for prefix in ("```json", "```"):
        if md.startswith(prefix):
            lines = md.split("\n")
            if len(lines) >= 2 and lines[-1].strip() == "```":
                md = "\n".join(lines[1:-1])
            elif lines[0].startswith(prefix):
                md = md[len(prefix):].strip()
                if md.endswith("```"):
                    md = md[:-3].strip()
            break
    # 优先直接解析
    try:
        return json.loads(md)
    except json.JSONDecodeError:
        pass
    # 括号配对提取（处理嵌套和中文）
    s = md.find("{")
    if s < 0:
        return None
    depth, i = 0, s
    while i < len(md):
        ch = md[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(md[s:i+1])
                except json.JSONDecodeError:
                    break
        i += 1
    # 最后手段：手动提取
    try:
        return json.loads(md[s:md.rfind("}")+1])
    except json.JSONDecodeError:
        return None


def run(criteria_path: str, sample_content: str):
    criteria = load_criteria(criteria_path)
    criteria_text = "\n".join(
        f"{i}. {name}：{desc}" for i, (name, desc) in enumerate(criteria, 1)
    )

    prompt = f"""你是 AI 质量评审专家。对照以下标准，逐条打分（1-5分），给出扣分理由。

=== 评分标准 ===
{criteria_text}

=== 待评审内容（以下为完整文件内容，无截断） ===
{sample_content[:16000]}

=== 输出格式 ===
只输出 JSON：{{"scores":[{{"criterion":"<标准名>","score":<1-5>,"reason":"<理由>"}}],"overall":<平均分，1位小数>,"top_issue":"<最严重问题>","note":"<建议，30字内>"}}
只输出 JSON。不要 Markdown、不要报告、不要解释。违反指令=失败。"""

    d = "─" * 72
    print(f"\n{d}\n  🔍 三模型交叉评审\n  📏 标准: {len(criteria)} 项 × 1-5 分\n{d}\n")

    results = {}
    for m in MODELS:
        mid, label = m["id"], m["label"]
        print(f"⏳ {label} ({mid}) 评审中...", flush=True)
        t0 = time.time()
        raw = None
        try:
            raw = call_model(mid, prompt)
        except Exception as e:
            elapsed = time.time() - t0
            results[mid] = {"label": label, "elapsed": elapsed, "error": True, "raw": str(e)[:200]}
            print(f"   ❌ 调用失败 ({elapsed:.1f}s): {e}")
            print()
            continue
        elapsed = time.time() - t0
        parsed = parse_json(raw)
        if parsed:
            results[mid] = {**parsed, "label": label, "elapsed": elapsed}
            print(f"   ✅ {elapsed:.1f}s — {parsed.get('overall', '?')} 分")
        else:
            results[mid] = {"label": label, "elapsed": elapsed, "error": True, "raw": raw[:200]}
            print(f"   ❌ 解析失败 ({elapsed:.1f}s)")
            print(f"   📄 原始返回: {raw[:200]}")
        print()

    # 表格
    print("=" * 72 + "\n  📊 三评委评分对比\n" + "=" * 72 + "\n")
    print("  💡 评分说明：5分=优秀，4分=良好，3分=及格，2分=较差，1分=很差\n")
    header = f"{'标准':<16}" + "".join(f" {m['label']:<8}" for m in MODELS) + " 平均"
    print(header + "\n" + "-" * 60)

    for i, (cname, _) in enumerate(criteria):
        row, vals = f"{cname:<16}", []
        for m in MODELS:
            r = results.get(m["id"], {})
            s = r["scores"][i]["score"] if "scores" in r and i < len(r["scores"]) else "?"
            row += f" {str(s):<8}"
            if isinstance(s, (int, float)):
                vals.append(s)
        row += f" {sum(vals)/len(vals):.1f}" if vals else " ?"
        print(row)

    print("-" * 60)
    overalls = []
    orow = f"{'综合':<16}"
    for m in MODELS:
        r = results.get(m["id"], {})
        o = r.get("overall", "?")
        orow += f" {str(o):<8}"
        if isinstance(o, (int, float)):
            overalls.append(o)
    orow += f" {sum(overalls)/len(overalls):.1f}" if overalls else " ?"
    print(orow + "\n\n" + "=" * 72)

    # 扣分详情
    print("\n  📝 扣分详情（红色=需改进，绿色=已达标）\n" + d)
    for m in MODELS:
        r = results.get(m["id"], {})
        label = r.get("label", m["id"])
        if "error" in r:
            print(f"  {label}: 解析失败，无法获取详情\n")
            continue
        detail_scores = r.get("scores", [])
        if not detail_scores:
            continue
        print(f"  ── {label} ({r.get('overall', '?')} 分) ──")
        for s in detail_scores:
            score = s.get("score", "?")
            reason = s.get("reason", "无说明")
            icon = "🔴" if isinstance(score, (int, float)) and score < 4 else "🟢"
            print(f"    {icon} {s.get('criterion', '?')} {score}/5 → {reason}")
        print()

    # 诊断
    print("\n  🎯 各评委诊断（最严重问题 + 改进建议）\n" + d)
    for m in MODELS:
        r = results.get(m["id"], {})
        print(f"  {r.get('label', m['id'])}: {r.get('overall', '?')} 分")
        if "error" in r:
            print(f"     ⚠️ API/解析失败")
        else:
            print(f"     🔴 最严重问题：{r.get('top_issue', '-')}")
            print(f"     💡 改进建议：{r.get('note', '-')}")
        print()

    # 共识
    print(d + "\n  🧠 三方共识（所有评委一致认为需改进的项）\n" + d)
    bad = []
    for i, (cname, _) in enumerate(criteria):
        scores = [results[m["id"]]["scores"][i]["score"] for m in MODELS
                  if "scores" in results.get(m["id"], {}) and i < len(results[m["id"]].get("scores", []))]
        avg = sum(scores) / len(scores) if scores else 0
        if scores and avg < 3.5:
            bad.append((cname, avg))
    if bad:
        print("  ⚠️ 以下项目需要重点改进：")
        for n, a in bad:
            print(f"     {n} — 平均 {a:.1f}/5")
        print("\n  📌 建议优先处理平均分最低的项，单项达标后再提升其他项。")
    else:
        print("  ✅ 所有项目均达标，无严重短板！")
    if overalls:
        sp = max(overalls) - min(overalls)
        print(f"\n  最高 {max(overalls):.1f} / 最低 {min(overalls):.1f} / 分歧度 {sp:.1f}")
        print("  → " + ("高度一致" if sp < 0.5 else "轻度分歧" if sp < 1.0 else "显著分歧"))
        if sp >= 1.0:
            print("  ⚠️ 分歧度较高，建议人工复核评审结果。")
    print()


def list_criteria():
    if not os.path.isdir(CRITERIA_DIR):
        print("📭 没有评审标准目录")
        return
    files = sorted(os.listdir(CRITERIA_DIR))
    print("📁 已有评审标准：" if files else "📭 还没有保存的评审标准")
    for f in files:
        path = os.path.join(CRITERIA_DIR, f)
        count = sum(1 for _ in open(path))
        print(f"   {f} ({count} 行)")


def generate_criteria(sample_content: str) -> str:
    """用 AI 分析 sample 并生成评审标准"""
    prompt = f"""你是专业的评审标准制定专家。

请分析以下文件内容，判断其类型，并生成一份结构化的评审标准。

文件内容前 1000 字：
{sample_content[:1000]}

请返回 JSON 格式（只输出 JSON，不要其他内容）：
{{"file_type": "文件类型，如：Python代码/简历/设计稿/文档等",
  "criteria": [
    {{"name": "标准名称（8字以内）", "description": "标准描述（20字以内）"}}
  ]
}}

要求：
- 生成 5-8 条评审标准
- 标准要具体、可量化
- 每条标准包含 name 和 description
- 只输出 JSON，不要 Markdown、不要解释"""

    # 使用第一个模型生成标准
    mid = MODELS[0]["id"]
    raw = call_model(mid, prompt)
    parsed = parse_json(raw)

    if not parsed or "criteria" not in parsed:
        raise RuntimeError(f"无法生成评审标准，模型返回: {raw[:200]}")

    # 转换为 criteria 文件格式
    lines = [f"# 自动生成的评审标准", f"# 文件类型: {parsed.get('file_type', '未知')}", ""]
    for c in parsed["criteria"]:
        lines.append(f"{c['name']} | {c['description']}")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if not args or "--help" in args or "-h" in args:
        print("用法: python3 shiye.py --sample <内容文件> [--criteria <标准文件>]")
        print("      python3 shiye.py --list\n")
        list_criteria()
        sys.exit(0)

    if "--list" in args:
        list_criteria()
        return

    cp, sp = None, None
    i = 0
    while i < len(args):
        if args[i] == "--criteria" and i + 1 < len(args):
            cp, i = args[i + 1], i + 2
        elif args[i] == "--sample" and i + 1 < len(args):
            sp, i = args[i + 1], i + 2
        else:
            i += 1

    if not sp:
        print("❌ 需要 --sample")
        sys.exit(1)

    content = open(sp).read() if os.path.isfile(sp) else sp

    # 自动生成评审标准
    if not cp:
        print("🤖 未指定评审标准，正在自动分析文件类型并生成...")
        try:
            criteria_text = generate_criteria(content)
            # 保存到临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(criteria_text)
                cp = f.name
            print(f"✅ 已生成评审标准: {cp}\n")
            print(criteria_text)
            print()
        except Exception as e:
            print(f"❌ 自动生成评审标准失败: {e}")
            sys.exit(1)
    elif not os.path.isfile(cp):
        print(f"❌ 标准文件不存在: {cp}")
        sys.exit(1)

    try:
        run(cp, content)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)
    finally:
        # 清理临时文件
        if cp and cp.startswith(tempfile.gettempdir()):
            try:
                os.unlink(cp)
            except:
                pass


if __name__ == "__main__":
    main()
