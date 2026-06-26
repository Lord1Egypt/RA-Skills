#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复诊病历生成：从复诊病历文本中抽取并规范化为细粒度字段 JSON.
LLM 调用使用公司内部医疗大模型.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_ROOT = SCRIPT_DIR.parents[3]
PREPROCESS_DIR = SKILLS_ROOT / "_shared" / "doc-preprocess" / "scripts"
if str(PREPROCESS_DIR) not in sys.path:
    sys.path.insert(0, str(PREPROCESS_DIR))

from preprocess import (
    PreprocessError,
    SUPPORTED_FILE_TYPES,
    detect_input_type,
    load_input_artifact,
)


DEFAULT_LLM_BASE = "https://maas-api.hivoice.cn/v1"
DEFAULT_LLM_MODEL = "u1-insuremed"

# 标准输出字段顺序
FIELDS_PART1 = [
    "现病史.病情概述",
    "现病史.药物",
    "现病史.其他治疗措施",
    "现病史.病情转归",
    "现病史.一般情况",
    "既往史.疾病",
    "既往史.其他信息",
    "既往史.手术史",
    "既往史.过敏史",
    "既往史.输血史",
    "婚育史",
    "月经史",
    "个人史",
    "家族史",
    "查体",
    "辅助检查",
    "诊断",
]

FIELDS_PART2 = [
    "处理意见.药物",
    "处理意见.其他建议",
]


def _read_json(path: Path) -> dict[str, Any]:
    """读取 JSON 文件并验证结构."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("输入 JSON 必须是对象")
    return payload


def extract_text(path: Path, input_type: str, encoding: str, sheet: str) -> str:
    """从任意格式文件中提取纯文本."""
    artifact = load_input_artifact(
        path, input_type, encoding, sheet, pdf_as_single_text=True
    )
    kind = artifact["kind"]
    if kind == "text":
        return str(artifact.get("text") or "")
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            for key in ("record", "text", "content"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value
            return json.dumps(data, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)
    if kind == "tables":
        rows_text: list[str] = []
        for table in artifact.get("tables", []):
            for row in table.get("rows", []):
                rows_text.append("\t".join(str(cell) for cell in row))
        return "\n".join(rows_text)
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def build_payload_from_input(
    path: Path,
    *,
    input_type: str,
    encoding: str,
    sheet: str,
) -> dict[str, Any]:
    """根据输入构建 API 请求体."""
    resolved_type = detect_input_type(path, input_type)

    # 尝试直接读取 JSON
    if resolved_type == "json":
        try:
            payload = _read_json(path)
            # 检查是否包含 record 字段
            if payload.get("record"):
                return payload
        except Exception:
            pass

    # 从文件提取文本
    text = extract_text(path, resolved_type, encoding, sheet)
    if not text.strip():
        raise PreprocessError("预处理后病历文本为空")

    # 尝试解析 JSON 文本
    try:
        data = json.loads(text)
        if isinstance(data, dict) and data.get("record"):
            return data
    except json.JSONDecodeError:
        pass

    # 默认为纯文本病历
    return {"record": text}


def _http_post(
    url: str, payload: dict[str, Any], headers: dict[str, str], *, timeout: int = 0
) -> Any:
    """发送 HTTP POST 请求."""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            **{key: value for key, value in headers.items() if value},
        },
    )
    try:
        opener = (
            urllib.request.urlopen(req)
            if not timeout
            else urllib.request.urlopen(req, timeout=timeout)
        )
        with opener as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def call_llm(prompt: str, *, base: str, model: str, appkey: str, timeout: int) -> str:
    """调用内部医疗大模型."""
    url = f"{base.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {appkey}"} if appkey else {}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    response = _http_post(url, payload, headers, timeout=timeout)
    try:
        return str(response["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected LLM response: {response}") from exc


def build_prompt(payload: dict[str, Any]) -> tuple[str, str]:
    """构建 LLM 提示词，返回 (part1_prompt, part2_prompt)."""
    record = payload.get("record") or payload.get("text") or payload.get("content") or ""

    if not record.strip():
        raise ValueError("输入缺少 record 字段")

    # 第一步：分块 - 将病历分为"患者的情况"和"医生的处理意见"
    chunk_prompt = """给定下面的病历文本，请抽取出两部分
1.患者的情况
2.医生的处理意见

输入：
{}

输出：
""".strip().format(record)

    return chunk_prompt, None


def extract_chunk_result(text: str) -> tuple[str, str]:
    """从模型输出中提取"患者的情况"和"医生的处理意见"两部分."""
    # 匹配输出格式：1.患者的情况\n{}\n\n2.医生的处理意见\n{}
    pattern = r"1\.患者的情况\s*\n([^2]*)\n\n2\.医生的处理意见\s*\n(.*)"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        record1 = match.group(1).strip()
        record2 = match.group(2).strip()
        return record1, record2
    
    # 如果无法匹配，返回原始文本
    return text, ""


def build_extract_prompts(record1: str, record2: str) -> tuple[str, str]:
    """构建抽取提示词."""
    # 第一部分：病史相关
    part1_prompt = f"""
给定患者病历中病史相关内容，请按要求抽取出其中对应的部分

1.基本原则：忠实于原文，只做拆解，不要加工
2.抽取以下字段，如果没有对应内容，请回答"未提及"
{chr(10).join(FIELDS_PART1)}

病史相关内容如下：
{record1}
""".strip()

    # 第二部分：处理意见相关
    part2_prompt = f"""
给定患者病历中处理意见和随诊相关内容，请按要求抽取出其中对应的部分

1.基本原则：忠实于原文，只做拆解，不要加工
2."本人就诊"不用抽取
3.抽取以下字段，如果没有对应内容，请回答"未提及"
{chr(10).join(FIELDS_PART2)}

处理意见相关内容如下：
{record2}
""".strip()

    return part1_prompt, part2_prompt


def normalize_text(text: str) -> str:
    """病历文本预处理：统一标点符号."""
    if not text:
        return text
    # 替换中文标点为英文标点
    text = text.replace("：", ":").replace("，", ",").replace("；", ";").replace("（", "(").replace("）", ")").replace("？", "?")
    return text


def postprocess_result(text: str, llm_base: str, llm_model: str, appkey: str, timeout: int) -> str:
    """结果后处理：规范化输出格式."""
    text = normalize_text(text)
    
    # 规范化历史相关字段
    history_rules = {
        "既往史.输血史": {"无输血史", "否认输血史", "未见输血史"},
        "既往史.过敏史": {"无过敏史", "否认过敏史", "未见过敏史"},
        "既往史.手术史": {"无手术史", "否认手术史", "未见手术史"},
        "婚育史": {"无婚育史", "否认婚育史"},
        "月经史": {"无月经史", "否认月经史"},
        "个人史": {"无个人史", "否认个人史"},
        "家族史": {"无家族史", "否认家族史"},
    }
    
    # 规范化处理意见字段
    treatment_rules = {
        "现病史.药物": {"自服", "服用", "口服"},
        "现病史.一般情况": {"可", "尚可", "一般", "尚好"},
        "现病史.病情转归": {"首诊", "初诊", "复诊", "初诊患者", "初诊病人"},
    }
    
    lines = text.split("\n")
    normalized_lines = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # 检查是否包含字段名
        is_normalized = False
        for field, patterns in history_rules.items():
            if line.startswith(f"{field}:"):
                value = line[len(field) + 1:].strip()
                if value in patterns:
                    line = f"{field}:无"
                    is_normalized = True
                    break
        
        if not is_normalized:
            for field, prefixes in treatment_rules.items():
                if line.startswith(f"{field}:"):
                    value = line[len(field) + 1:].strip()
                    # 规范化一般情况
                    if field == "现病史.一般情况":
                        for pattern in ["可", "尚可", "一般", "尚好"]:
                            if value == pattern:
                                value = "良好"
                                break
                    # 规范化病情转归
                    elif field == "现病史.病情转归":
                        for pattern in ["首诊", "初诊", "复诊", "初诊患者", "初诊病人"]:
                            if pattern in value:
                                value = "未提及"
                                break
                    # 规范化药物前缀
                    elif field == "现病史.药物":
                        for prefix in ["自服", "服用", "口服"]:
                            if value.startswith(prefix):
                                value = value[len(prefix):].strip()
                                break
                    line = f"{field}:{value}"
                    is_normalized = True
                    break
        
        normalized_lines.append(line)
    
    return "\n".join(normalized_lines)


def run(
    payload: dict[str, Any], *, base: str, model: str, appkey: str, timeout: int
) -> str:
    """执行复诊病历生成."""
    chunk_prompt, _ = build_prompt(payload)
    
    # 第一步：分块
    chunk_result = call_llm(chunk_prompt, base=base, model=model, appkey=appkey, timeout=timeout)
    
    # 提取两部分内容
    record1, record2 = extract_chunk_result(chunk_result)
    
    # 第二步：分别抽取
    part1_prompt, part2_prompt = build_extract_prompts(record1, record2)
    
    part1_result = call_llm(part1_prompt, base=base, model=model, appkey=appkey, timeout=timeout)
    part2_result = call_llm(part2_prompt, base=base, model=model, appkey=appkey, timeout=timeout)
    
    # 合并结果
    final_result = part1_result + "\n" + part2_result
    
    # 后处理
    final_result = postprocess_result(final_result, llm_base=base, llm_model=model, appkey=appkey, timeout=timeout)
    
    return final_result


def save_prepared(payload: dict[str, Any], output_path: str, input_path: Path) -> None:
    """保存预处理后的数据，便于调试."""
    save_dir = (
        Path(output_path).parent
        if output_path
        else SCRIPT_DIR.parents[1] / "runs" / "followup-record"
    )
    save_dir.mkdir(parents=True, exist_ok=True)
    prepared_path = save_dir / f"{input_path.stem}.prepared.json"
    prepared_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"Prepared data saved to: {prepared_path}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="复诊病历生成统一入口：支持 pdf/doc/docx/xls/xlsx/csv/txt/json 输入."
    )
    parser.add_argument("--input", required=True, help="输入病历文件路径.")
    parser.add_argument(
        "--input-type",
        default="auto",
        choices=["auto", *sorted(SUPPORTED_FILE_TYPES)],
        help="输入类型；默认 auto.",
    )
    parser.add_argument("--sheet", default="", help="读取 Excel 时指定 sheet（可选）.")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv 编码（默认：utf-8）.")
    parser.add_argument(
        "--base",
        default=DEFAULT_LLM_BASE,
        help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）.",
    )
    parser.add_argument(
        "--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）."
    )
    parser.add_argument(
        "--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）."
    )
    parser.add_argument(
        "--appkey",
        required=True,
        help="必须传入。内部医疗大模型鉴权 key，使用 Bearer 方式认证。",
    )
    parser.add_argument("--output-json", default="", help="输出 JSON 文件路径（可选）.")
    parser.add_argument("--output", default="", help="输出病历文本文件路径（可选）.")
    parser.add_argument("--save-prepared", action="store_true", help="保存预处理后的数据，便于调试.")
    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        payload = build_payload_from_input(
            input_path,
            input_type=args.input_type,
            encoding=args.encoding,
            sheet=args.sheet,
        )
        if args.save_prepared:
            save_prepared(payload, args.output, input_path)
        response = run(
            payload,
            base=args.base,
            model=args.model,
            appkey=args.appkey,
            timeout=args.timeout,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_path = args.output or args.output_json
    if output_path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(response, encoding="utf-8")
    print(response)
    return 0





def standardize_drug_info(text: str, llm_base: str, llm_model: str, appkey: str, timeout: int) -> str:
    """标准化药物信息：简化药物使用方法，删除不必要的内容.

    特别说明:
    1. 不要遗漏任何药物
    2. 只删除，不补充和转换任何信息
    3. 回答结果中不包含"简化后"等字样
    4. 如果输入是"未提及"，则直接返回"未提及药物"
    """
    # 提取"处理意见。药物"的值
    lines = text.split("\n")
    drug_line = None
    drug_line_idx = -1

    for i, line in enumerate(lines):
        if line.startswith("处理意见。药物"):
            drug_line = line
            drug_line_idx = i
            break

    if drug_line is None:
        return text

    # 提取药物文本
    drug_text = drug_line[len("处理意见。药物") + 1:].strip()

    if not drug_text or drug_text == "未提及":
        return text

    # 调用 LLM 进行药物标准化
    drug_prompt = f"""
简化药物使用方法，删除不必要的内容 (药品总量、总共使用时间、商品名等无用信息),整理后每种药物独立一行.
特别说明:
1. 不要遗漏任何药物
2. 只删除，不补充和转换任何信息
3. 回答结果当中不包含"简化后"等字样。如果输入是"未提及",则直接返回"未提及药物".

药物使用方法如下:
{drug_text}
""".strip()

    try:
        standardized_drug = call_llm(
            drug_prompt,
            base=llm_base,
            model=llm_model,
            appkey=appkey,
            timeout=timeout
        )

        # 替换原文本中的药物信息
        lines[drug_line_idx] = f"处理意见。药物:{standardized_drug}"

        return "\n".join(lines)
    except Exception:
        # 如果标准化失败，返回原文本
        return text


if __name__ == "__main__":
    raise SystemExit(main())

