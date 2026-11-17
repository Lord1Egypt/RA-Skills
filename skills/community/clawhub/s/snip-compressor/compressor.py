#!/usr/bin/env python3
NL = chr(10)

import json, sys, re, argparse
from typing import Any

WEIGHTS = {"decision":0.95,"factual_data":0.90,"tool_result":0.60,"tool_call":0.50,"code_block":0.70,"question":0.55,"instruction":0.65,"greeting":0.10,"small_talk":0.15,"acknowledgment":0.20,"error":0.80,"summary":0.75}

DECISION_PATTERNS = [r"决策|选|用|采用|走|方案|就这|定了|ok|好的|可以|行|done|完成", r"decide|choose|use|go with|settle|done|approved|confirmed", r"那就|就这么|就这样|okay|sure|let's do"]
FACT_PATTERNS = [r"\\d+\\.?\\d*%", r"\\d{4}-\\d{2}-\\d{2}", r"价格|金额|数量|比例|市值|PE|PB|ROE|营收|利润", r"price|amount|count|ratio|market cap|revenue|profit", r"http[s]?://", r"[A-Z]{2,}\\d+"]

def score_segment(content: str) -> dict:
    scores = {}; cl = content.lower()
    for p in DECISION_PATTERNS:
        if re.search(p, content): scores["decision"] = WEIGHTS["decision"]; break
    fc = sum(len(re.findall(p, content)) for p in FACT_PATTERNS)
    if fc > 0: scores["factual_data"] = min(1.0, WEIGHTS["factual_data"]*(1+fc*0.05))
    if re.search(r"`", content): scores["code_block"] = WEIGHTS["code_block"]
    if re.search(r'"(result|output|data|response)"\\s*:', content): scores["tool_result"] = WEIGHTS["tool_result"]
    if re.search(r"error|traceback|exception|failed|失败|错误", cl): scores["error"] = WEIGHTS["error"]
    if content.strip().endswith("?") or re.search(r"^(什么|怎么|为什么|如何|哪|有没有|是不是|能否)", content): scores["question"] = WEIGHTS["question"]
    if re.search(r"^(请|帮我|给我|把|将|用|运行|执行|查|看|分析|对比|写|创建|修改|删除)", content): scores["instruction"] = WEIGHTS["instruction"]
    if re.search(r"^(你好|hi|hello|hey|早|晚上好|在吗|哈喽)", cl) and len(content)<50: scores["greeting"] = WEIGHTS["greeting"]
    if re.search(r"^(好的|收到|明白|知道了|ok|okay|got it|thanks|谢谢)", cl) and len(content)<30: scores["acknowledgment"] = WEIGHTS["acknowledgment"]
    if re.search(r"总结|综上所述|综上|总的来说|in summary|to summarize|overall", cl): scores["summary"] = WEIGHTS["summary"]
    return scores

def compute_retention_score(scores: dict) -> float:
    return max(scores.values()) if scores else 0.30

def compress_tool_result(content: str, max_chars: int = 200) -> str:
    if len(content) <= max_chars: return content
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            keys = list(data.keys())
            s = "[Tool result: " + str(len(keys)) + " keys]"
            for k in keys[:3]:
                v = str(data[k])
                if len(v) > 100: v = v[:100] + "..."
                s += NL + "  " + k + ": " + v
            if len(keys) > 3: s += NL + "  ... and " + str(len(keys)-3) + " more fields"
            return s
    except: pass
    return content[:max_chars] + NL + "... [truncated]"

def parse_conversation(data: Any) -> list:
    if isinstance(data, list): return data
    if isinstance(data, dict):
        if "messages" in data: return data["messages"]
        if "conversation" in data: return data["conversation"]
    return []

def compress(conversation: list, token_budget: int = 3000) -> dict:
    segments = []
    for i, msg in enumerate(conversation):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        tc = msg.get("tool_calls", []); tr = msg.get("tool_results", [])
        combined = content
        for t in tc: combined += NL + "[Tool: " + t.get("name","unknown") + "]"
        for t in tr:
            rs = json.dumps(t) if isinstance(t,dict) else str(t)
            combined += NL + "[Result: " + compress_tool_result(rs) + "]"
        scores = score_segment(combined)
        retention = compute_retention_score(scores)
        segments.append({"index":i,"role":role,"content":content,"tool_calls":tc,"tool_results":tr,"scores":scores,"retention":retention,"token_estimate":len(combined)//2})
    for seg in segments:
        seg["action"] = "keep"
        if seg["retention"] < 0.25: seg["action"] = "drop"
        elif seg["retention"] < 0.40: seg["action"] = "condense"
    for i, seg in enumerate(segments):
        if seg["action"] == "drop":
            for j in range(i+1, min(i+5, len(segments))):
                later = segments[j]
                if later["retention"] >= 0.70:
                    refs = [r"如上|上述|前面|之前|刚才|之前说的|刚才说的", r"above|previous|earlier|before|as mentioned", rf"#{i+1}|第{i+1}条|第{i+1}步"]
                    for p in refs:
                        if re.search(p, later["content"]): seg["action"] = "condense"; break
    droppable = sorted([s for s in segments if s["action"]=="drop"], key=lambda s:s["retention"])
    total_tokens = sum(s["token_estimate"] for s in segments if s["action"]!="drop")
    for seg in droppable:
        if total_tokens <= token_budget: break
        seg["action"] = "dropped"; total_tokens -= seg["token_estimate"]
    key_decisions = []; active_context = []; compressed_lines = []
    for seg in segments:
        if seg["action"] == "dropped": continue
        rl = {"user":"**User**","assistant":"**Assistant**","system":"**System**"}.get(seg["role"],"**"+seg["role"]+"**")
        if seg["action"] == "condense":
            c = seg["content"]
            if len(c) > 100:
                sentences = re.split(r"[。！？"+NL+".!?]", c)
                c = sentences[0].strip()
                if len(c) > 150: c = c[:150] + "..."
            compressed_lines.append(rl + ": " + c + " [condensed]")
        else:
            compressed_lines.append(rl + ": " + seg["content"])
            if seg["tool_calls"]:
                for t in seg["tool_calls"]: compressed_lines.append("  "+chr(0x2514)+chr(0x2500)+" Tool: "+t.get("name","unknown"))
            if seg["tool_results"]:
                for t in seg["tool_results"]:
                    rs = json.dumps(t) if isinstance(t,dict) else str(t)
                    compressed_lines.append("  "+chr(0x2514)+chr(0x2500)+" Result: "+compress_tool_result(rs))
        if "decision" in seg["scores"]: key_decisions.append(seg["content"][:200])
        if seg["role"]=="user" and seg["retention"]>=0.50: active_context.append(seg["content"][:150])
    active_context = active_context[-3:]
    total_msgs = len(conversation)
    kept_msgs = sum(1 for s in segments if s["action"] not in ("dropped",))
    summary_parts = ["Conversation compressed: "+str(total_msgs)+" -> "+str(kept_msgs)+" segments", "Participants: "+", ".join(set(s["role"] for s in segments))]
    if key_decisions: summary_parts.append("Key decisions identified: "+str(len(key_decisions)))
    return {"summary":NL.join(summary_parts),"key_decisions":key_decisions[:5],"active_context":active_context,"compressed_transcript":NL.join(compressed_lines),"stats":{"original_segments":total_msgs,"kept_segments":kept_msgs,"dropped_segments":total_msgs-kept_msgs,"condensed_segments":sum(1 for s in segments if s["action"]=="condense"),"estimated_tokens":total_tokens}}

def format_output(result: dict) -> str:
    lines = ["# Snip Compression Report","","## Summary",result["summary"],""]
    if result["key_decisions"]:
        lines.append("## Key Decisions")
        for i,d in enumerate(result["key_decisions"],1): lines.append(str(i)+". "+d)
        lines.append("")
    if result["active_context"]:
        lines.append("## Active Context")
        for ctx in result["active_context"]: lines.append("- "+ctx)
        lines.append("")
    lines.append("## Compressed Transcript")
    lines.append(result["compressed_transcript"])
    lines.append(""); lines.append("---")
    s = result["stats"]
    lines.append("*Stats: "+str(s["original_segments"])+"->"+str(s["kept_segments"])+" segments | ~"+str(s["estimated_tokens"])+" tokens | "+str(s["dropped_segments"])+" dropped, "+str(s["condensed_segments"])+" condensed*")
    return NL.join(lines)

def main():
    parser = argparse.ArgumentParser(description="Snip Compressor")
    parser.add_argument("--input","-i",help="Input JSON file")
    parser.add_argument("--output","-o",help="Output file")
    parser.add_argument("--budget","-b",type=int,default=3000,help="Token budget")
    args = parser.parse_args()
    if args.input:
        with open(args.input,"r",encoding="utf-8") as f: data = json.load(f)
    else: data = json.load(sys.stdin)
    conversation = parse_conversation(data)
    if not conversation:
        print("Error: No conversation data found.",file=sys.stderr); sys.exit(1)
    result = compress(conversation, token_budget=args.budget)
    output = format_output(result)
    if args.output:
        with open(args.output,"w",encoding="utf-8") as f: f.write(output)
        print("Compressed to "+args.output)
    else: print(output)

if __name__ == "__main__": main()