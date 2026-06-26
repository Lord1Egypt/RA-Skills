#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None


TARGET_FIELDS = {
    "name": "",
    "birth_date": "",
    "category": "",
    "as_of": "",
    "actual_contribution_months": 0,
    "deemed_contribution_months": 0,
    "actual_pre_1998_07_months": 0,
    "personal_account_balance": 0.0,
    "z_actual": 1.0,
    "unemployment_benefit_months": 0,
    "employment_type": "employee",
    "is_4050_eligible": False,
    "subsidy_already_used_months": 0,
    "subsidy_insurances": "pension,medical,unemployment",
    "annual_contribution_records": [],
}
REQUIRED_FIELDS = ["birth_date", "category", "as_of"]

ALIASES = {
    "name": ["name", "姓名"],
    "birth_date": ["birth_date", "出生日期", "出生年月", "出生"],
    "category": ["category", "退休类别", "性别类别"],
    "as_of": ["as_of", "asof", "测算日期", "统计日期", "截至日期"],
    "actual_contribution_months": ["actual_contribution_months", "实际缴费月数", "累计缴费月数", "实际缴费"],
    "deemed_contribution_months": ["deemed_contribution_months", "视同缴费月数", "视同缴费"],
    "actual_pre_1998_07_months": ["actual_pre_1998_07_months", "1998前实际缴费月数", "98前实际缴费", "1998年前实际缴费"],
    "personal_account_balance": ["personal_account_balance", "个人账户余额", "个人账户累计储存额", "个人账户"],
    "z_actual": ["z_actual", "实际缴费工资指数", "z实指数", "缴费指数"],
    "unemployment_benefit_months": ["unemployment_benefit_months", "失业金月数", "领取失业保险月数", "领失业金月数"],
    "employment_type": ["employment_type", "就业类型", "参保类型"],
    "is_4050_eligible": ["is_4050_eligible", "是否4050", "是否4050人员", "是否享受4050"],
    "subsidy_already_used_months": ["subsidy_already_used_months", "补贴已享月数", "4050已享月数"],
    "subsidy_insurances": ["subsidy_insurances", "补贴险种", "补贴包含险种"],
    "annual_contribution_records": ["annual_contribution_records", "历年缴费记录", "缴费明细"],
}


def normalize_key(s: str) -> str:
    return re.sub(r"\s+", "", str(s).strip().lower())


def parse_float(v: object, default: float = 0.0) -> float:
    if v is None:
        return default
    s = str(v)
    s = s.replace(",", "")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    if not m:
        return default
    return float(m.group(0))


def parse_int(v: object, default: int = 0) -> int:
    return int(round(parse_float(v, default)))


def parse_bool(v: object, default: bool = False) -> bool:
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in {"1", "true", "yes", "y", "是", "有"}:
        return True
    if s in {"0", "false", "no", "n", "否", "无"}:
        return False
    return default


def parse_birth_date(text: str) -> str:
    text = text.strip()
    m = re.search(r"(19\d{2}|20\d{2})[-/.年](\d{1,2})[-/.月](\d{1,2})", text)
    if m:
        y, mm, dd = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y:04d}-{mm:02d}-{dd:02d}"
    m = re.search(r"(19\d{2}|20\d{2})[-/.](\d{1,2})", text)
    if m:
        y, mm = int(m.group(1)), int(m.group(2))
        return f"{y:04d}-{mm:02d}-01"
    return ""


def infer_category_by_text(text: str) -> str:
    t = text.lower()
    if "male_60" in t or "男" in text:
        return "male_60"
    if "female_55" in t or "女干部" in text or "女职工55" in text:
        return "female_55"
    if "female_50" in t or "女工人" in text or "女职工50" in text:
        return "female_50"
    return ""


def extract_by_alias_map(row: Dict[str, object]) -> Dict[str, object]:
    norm_map = {normalize_key(k): v for k, v in row.items()}
    out = dict(TARGET_FIELDS)

    for target, alias_list in ALIASES.items():
        for alias in alias_list:
            v = norm_map.get(normalize_key(alias))
            if v is not None and str(v).strip() != "":
                out[target] = v
                break

    return out


def parse_special_contribution_table_df(df: pd.DataFrame) -> List[Dict[str, object]]:
    cols = {normalize_key(c): c for c in df.columns}
    c_period = cols.get(normalize_key("缴费起止年月"))
    c_months = cols.get(normalize_key("月数"))
    c_annual = cols.get(normalize_key("年缴费基数"))
    if not (c_period and c_months and c_annual):
        return []

    records: List[Dict[str, object]] = []
    for _, r in df.iterrows():
        period = str(r.get(c_period, "")).strip()
        if not period:
            continue
        y_hits = re.findall(r"((?:19|20)\d{2})", period)
        if not y_hits:
            continue
        year = int(y_hits[0])
        months = parse_int(r.get(c_months, 0), 0)
        annual_base = parse_float(r.get(c_annual, 0.0), 0.0)
        if year < 1990 or year > 2090 or months <= 0 or annual_base <= 0:
            continue
        records.append(
            {
                "year": year,
                "months": months,
                "avg_contribution_base_monthly": round(annual_base / months, 2),
                "unemployment_benefit_months": 0,
            }
        )

    # 去重按年
    by_year: Dict[int, Dict[str, object]] = {}
    for rec in records:
        by_year[int(rec["year"])] = rec
    return [by_year[y] for y in sorted(by_year.keys())]


def table_to_record(df: pd.DataFrame) -> Tuple[Dict[str, object], List[str]]:
    warnings: List[str] = []
    if df.empty:
        return dict(TARGET_FIELDS), ["表格为空，未提取到数据"]

    special_records = parse_special_contribution_table_df(df)
    if special_records:
        out = dict(TARGET_FIELDS)
        out["annual_contribution_records"] = special_records
        out["actual_contribution_months"] = sum(int(x["months"]) for x in special_records)
        warnings.append(f"已按专用模板(表格)识别历年缴费记录{len(special_records)}条")
        return out, warnings

    # 形式A: 单行宽表
    if df.shape[0] >= 1 and df.shape[1] >= 4:
        row = df.iloc[0].to_dict()
        record = extract_by_alias_map(row)
        return record, warnings

    # 形式B: 两列 key-value
    if df.shape[1] >= 2:
        row = {}
        for _, r in df.iterrows():
            k = str(r.iloc[0]).strip()
            v = r.iloc[1]
            if k:
                row[k] = v
        record = extract_by_alias_map(row)
        return record, warnings

    return dict(TARGET_FIELDS), ["无法识别的表格结构，请使用单行宽表或两列键值表"]


def ocr_image_text(path: Path) -> str:
    if shutil.which("tesseract") is None:
        raise RuntimeError(
            "未找到 tesseract 可执行文件。请先安装 tesseract-ocr 和中文语言包 chi_sim 后重试。"
        )
    cmd = ["tesseract", str(path), "stdout", "-l", "chi_sim+eng", "--psm", "6"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "OCR失败")
    return proc.stdout


def parse_special_contribution_table_records(text: str) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        prefix = line[:48]
        year_hits = re.findall(r"((?:19|20)\d{2})", prefix)
        year_hits = [int(y) for y in year_hits if 1990 <= int(y) <= 2090]
        if len(year_hits) < 2:
            continue
        y1 = int(year_hits[0])
        y2 = int(year_hits[1])
        year = y1 if y1 == y2 else y2

        # 取第二个“年-月”之后的尾部，尝试解析：月数、年缴费基数、个人缴费
        m_tail = re.search(
            r"(?:19|20)\d{2}\D*\d{1,2}.*?(?:19|20)\d{2}\D*\d{1,2}(.*)$",
            line,
        )
        if not m_tail:
            continue
        tail = m_tail.group(1)
        nums = re.findall(r"\d+(?:\.\d+)?", tail)
        if len(nums) < 2:
            continue

        months = 0
        annual_base = 0.0

        if len(nums) >= 3:
            m0 = int(float(nums[0]))
            if 1 <= m0 <= 12:
                months = m0
                annual_base = parse_float(nums[1], 0.0)
            else:
                token = nums[0]
                if len(token) >= 5:
                    m_guess = int(token[:2])
                    if 1 <= m_guess <= 12:
                        months = m_guess
                        annual_base = parse_float(token[2:], 0.0)
        else:
            # 典型粘连：1248000（12 + 48000）
            token = nums[0]
            if len(token) >= 5:
                m_guess = int(token[:2])
                if 1 <= m_guess <= 12:
                    months = m_guess
                    annual_base = parse_float(token[2:], 0.0)

        if months <= 0 or annual_base <= 0:
            continue

        avg_base_monthly = annual_base / months
        records.append(
            {
                "year": year,
                "months": months,
                "avg_contribution_base_monthly": round(avg_base_monthly, 2),
                "unemployment_benefit_months": 0,
            }
        )

    # 去重（同一年取最后一条）
    by_year: Dict[int, Dict[str, object]] = {}
    for r in records:
        y = int(r["year"])
        if 1990 <= y <= 2090:
            by_year[y] = r
    return [by_year[y] for y in sorted(by_year.keys())]


def extract_from_ocr_text(text: str) -> Tuple[Dict[str, object], List[str]]:
    warnings: List[str] = []
    out = {k: "" for k in TARGET_FIELDS}
    out["annual_contribution_records"] = []

    # 姓名（可选）
    m_name = re.search(r"姓名[:：\s]*([\u4e00-\u9fa5A-Za-z·]{2,20})", text)
    if m_name:
        out["name"] = m_name.group(1).strip()

    # 出生日期
    m_birth_line = re.search(r"(出生(?:日期|年月)?[:：\s]*[^\n]+)", text)
    if m_birth_line:
        out["birth_date"] = parse_birth_date(m_birth_line.group(1))
    if not out["birth_date"]:
        m_birth_any = re.search(r"(19\d{2}|20\d{2})[-/.年](\d{1,2})[-/.月](\d{1,2})", text)
        if m_birth_any:
            out["birth_date"] = f"{int(m_birth_any.group(1)):04d}-{int(m_birth_any.group(2)):02d}-{int(m_birth_any.group(3)):02d}"

    out["category"] = infer_category_by_text(text)

    # 截止日期
    m_asof = re.search(r"(截至|统计|测算|as[_\s-]?of)日期?[:：\s]*(20\d{2}[-/.年]\d{1,2}(?:[-/.月]\d{1,2})?)", text, flags=re.IGNORECASE)
    if m_asof:
        out["as_of"] = parse_birth_date(m_asof.group(2))

    patterns = {
        "actual_contribution_months": [
            r"实际缴费月数[:：\s]*([0-9]+)",
            r"累计缴费月数[:：\s]*([0-9]+)",
            r"actual[_\s-]?contribution[_\s-]?months[:：\s]*([0-9]+)",
        ],
        "deemed_contribution_months": [
            r"视同缴费月数[:：\s]*([0-9]+)",
            r"deemed[_\s-]?contribution[_\s-]?months[:：\s]*([0-9]+)",
        ],
        "actual_pre_1998_07_months": [
            r"(?:1998年前|98前).*?实际缴费月数[:：\s]*([0-9]+)",
            r"actual[_\s-]?pre[_\s-]?1998[_\s-]?07[_\s-]?months[:：\s]*([0-9]+)",
        ],
        "unemployment_benefit_months": [
            r"(?:失业金|失业保险).{0,6}月数[:：\s]*([0-9]+)",
            r"领取失业保险.{0,6}([0-9]+)个月",
            r"unemployment[_\s-]?benefit[_\s-]?months[:：\s]*([0-9]+)",
        ],
        "z_actual": [
            r"(?:z实指数|实际缴费工资指数|缴费指数)[:：\s]*([0-9]+(?:\.[0-9]+)?)",
            r"z[_\s-]?actual[:：\s]*([0-9]+(?:\.[0-9]+)?)",
        ],
        "personal_account_balance": [
            r"(?:个人账户(?:累计储存额|余额|金额)?)[:：\s]*([0-9,]+(?:\.[0-9]+)?)",
            r"personal[_\s-]?account[_\s-]?balance[:：\s]*([0-9,]+(?:\.[0-9]+)?)",
        ],
    }

    for k, ps in patterns.items():
        for p in ps:
            m = re.search(p, text, flags=re.IGNORECASE)
            if m:
                out[k] = m.group(1)
                break

    # 专用模板：缴费起止年月 + 月数 + 年缴费基数 + 个人缴费
    annual_records = parse_special_contribution_table_records(text)

    if annual_records:
        out["annual_contribution_records"] = annual_records
        if not str(out.get("actual_contribution_months", "")).strip():
            out["actual_contribution_months"] = sum(int(r["months"]) for r in annual_records)
        warnings.append(f"已按专用模板识别历年缴费记录{len(annual_records)}条")

    return out, warnings


def cast_record(record: Dict[str, object]) -> Dict[str, object]:
    out = dict(TARGET_FIELDS)

    out["name"] = str(record.get("name", "")).strip()
    out["birth_date"] = parse_birth_date(str(record.get("birth_date", "")))

    category = str(record.get("category", "")).strip()
    out["category"] = category if category in {"male_60", "female_55", "female_50"} else infer_category_by_text(category)

    as_of = parse_birth_date(str(record.get("as_of", "")))
    out["as_of"] = as_of

    out["actual_contribution_months"] = parse_int(record.get("actual_contribution_months", 0), 0)
    out["deemed_contribution_months"] = parse_int(record.get("deemed_contribution_months", 0), 0)
    out["actual_pre_1998_07_months"] = parse_int(record.get("actual_pre_1998_07_months", 0), 0)
    out["unemployment_benefit_months"] = parse_int(record.get("unemployment_benefit_months", 0), 0)
    out["personal_account_balance"] = round(parse_float(record.get("personal_account_balance", 0.0), 0.0), 2)
    out["z_actual"] = round(parse_float(record.get("z_actual", 1.0), 1.0), 4)
    et = str(record.get("employment_type", "employee")).strip().lower()
    out["employment_type"] = "flexible" if et in {"flexible", "灵活就业"} else "employee"
    out["is_4050_eligible"] = parse_bool(record.get("is_4050_eligible", False), False)
    out["subsidy_already_used_months"] = parse_int(record.get("subsidy_already_used_months", 0), 0)
    out["subsidy_insurances"] = str(record.get("subsidy_insurances", "pension,medical,unemployment")).strip() or "pension,medical,unemployment"
    arr = record.get("annual_contribution_records", [])
    if isinstance(arr, list):
        normalized = []
        for r in arr:
            try:
                year = int(r.get("year"))
                months = parse_int(r.get("months", 0), 0)
                avg_base = parse_float(r.get("avg_contribution_base_monthly", 0), 0.0)
                unemp = parse_int(r.get("unemployment_benefit_months", 0), 0)
                if year > 1900 and months > 0 and avg_base > 0:
                    normalized.append(
                        {
                            "year": year,
                            "months": months,
                            "avg_contribution_base_monthly": round(avg_base, 2),
                            "unemployment_benefit_months": unemp,
                        }
                    )
            except Exception:
                continue
        out["annual_contribution_records"] = sorted(normalized, key=lambda x: x["year"])
    else:
        out["annual_contribution_records"] = []

    return out


def infer_format(path: Path, fmt: str) -> str:
    if fmt != "auto":
        return fmt
    ext = path.suffix.lower()
    if ext in {".json"}:
        return "json"
    if ext in {".csv"}:
        return "csv"
    if ext in {".xlsx", ".xls"}:
        return "xlsx"
    if ext in {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}:
        return "image"
    raise ValueError(f"无法识别格式: {path}")


def load_record(path: Path, fmt: str) -> Tuple[Dict[str, object], List[str], str]:
    warnings: List[str] = []
    raw_excerpt = ""

    if fmt == "json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if "person" in data and "current" in data:
            # 已是目标结构，直接回传
            return {
                "name": data.get("person", {}).get("name", ""),
                "birth_date": data.get("person", {}).get("birth_date", ""),
                "category": data.get("person", {}).get("category", ""),
                "as_of": data.get("current", {}).get("as_of", ""),
                "actual_contribution_months": data.get("current", {}).get("actual_contribution_months", 0),
                "deemed_contribution_months": data.get("current", {}).get("deemed_contribution_months", 0),
                "actual_pre_1998_07_months": data.get("current", {}).get("actual_pre_1998_07_months", 0),
                "personal_account_balance": data.get("current", {}).get("personal_account_balance", 0),
                "z_actual": data.get("current", {}).get("z_actual", 1),
                "unemployment_benefit_months": data.get("current", {}).get("unemployment_benefit_months", 0),
                "employment_type": data.get("current", {}).get("employment_type", "employee"),
                "is_4050_eligible": data.get("current", {}).get("is_4050_eligible", False),
                "subsidy_already_used_months": data.get("current", {}).get("subsidy_already_used_months", 0),
                "subsidy_insurances": ",".join(data.get("current", {}).get("subsidy_insurances", ["pension", "medical", "unemployment"])),
                "annual_contribution_records": data.get("current", {}).get("annual_contribution_records", []),
            }, warnings, raw_excerpt
        return data, warnings, raw_excerpt

    if fmt == "csv":
        if pd is None:
            raise RuntimeError(
                "缺少依赖 pandas。请执行: python3 -m pip install -r requirements.txt"
            )
        df = pd.read_csv(path)
        rec, w = table_to_record(df)
        return rec, w, raw_excerpt

    if fmt == "xlsx":
        if pd is None:
            raise RuntimeError(
                "缺少依赖 pandas/openpyxl。请执行: python3 -m pip install -r requirements.txt"
            )
        df = pd.read_excel(path)
        rec, w = table_to_record(df)
        return rec, w, raw_excerpt

    if fmt == "image":
        txt = ocr_image_text(path)
        raw_excerpt = txt[:500]
        rec, w = extract_from_ocr_text(txt)
        return rec, w, raw_excerpt

    raise ValueError(f"不支持格式: {fmt}")


def build_target_payload(casted: Dict[str, object], strategy_indices: List[float], assumptions: Dict[str, float]) -> Dict[str, object]:
    subsidy_insurances = [x.strip() for x in str(casted["subsidy_insurances"]).split(",") if x.strip()]
    return {
        "person": {
            "name": casted["name"],
            "birth_date": casted["birth_date"],
            "category": casted["category"],
        },
        "current": {
            "as_of": casted["as_of"],
            "actual_contribution_months": casted["actual_contribution_months"],
            "deemed_contribution_months": casted["deemed_contribution_months"],
            "actual_pre_1998_07_months": casted["actual_pre_1998_07_months"],
            "personal_account_balance": casted["personal_account_balance"],
            "z_actual": casted["z_actual"],
            "unemployment_benefit_months": casted["unemployment_benefit_months"],
            "employment_type": casted["employment_type"],
            "is_4050_eligible": casted["is_4050_eligible"],
            "subsidy_already_used_months": casted["subsidy_already_used_months"],
            "subsidy_insurances": subsidy_insurances,
            "annual_contribution_records": casted.get("annual_contribution_records", []),
        },
        "assumptions": assumptions,
        "optimization": {
            "strategy_contribution_indices": strategy_indices,
        },
    }


def estimate_confidence(
    record: Dict[str, object],
    casted: Dict[str, object],
    fmt: str,
    used_default_asof: bool,
) -> Dict[str, float]:
    confidence: Dict[str, float] = {}
    for k in TARGET_FIELDS:
        raw = record.get(k)
        has_raw = raw is not None and str(raw).strip() != ""
        has_casted = casted.get(k) is not None and str(casted.get(k)).strip() != ""

        if not has_casted:
            confidence[k] = 0.0
            continue

        if fmt in {"csv", "xlsx", "json"}:
            confidence[k] = 0.95 if has_raw else 0.6
        else:
            # image OCR: conservative confidence
            confidence[k] = 0.78 if has_raw else 0.45

        if k == "category" and has_raw and str(raw).strip() not in {"male_60", "female_55", "female_50"}:
            confidence[k] = min(confidence[k], 0.6)
        if k == "as_of" and used_default_asof:
            confidence[k] = 0.0

    return confidence


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest user data from json/csv/xlsx/image and output calculator JSON.")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--format", default="auto", choices=["auto", "json", "csv", "xlsx", "image"], help="Input format")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument("--as-of-default", default="2026-03-01", help="Fallback as_of when missing")
    parser.add_argument("--name", default="", help="Override name")
    parser.add_argument("--birth-date", default="", help="Override birth_date (YYYY-MM-DD)")
    parser.add_argument("--category", default="", choices=["", "male_60", "female_55", "female_50"], help="Override retirement category")
    parser.add_argument("--employment-type", default="", choices=["", "employee", "flexible"], help="Override employment type")
    parser.add_argument("--is-4050-eligible", default="", choices=["", "true", "false"], help="Override 4050 eligibility")
    parser.add_argument("--assumption-wage-growth", type=float, default=0.04)
    parser.add_argument("--assumption-book-rate", type=float, default=0.03)
    parser.add_argument("--assumption-personal-rate", type=float, default=0.08)
    parser.add_argument("--strategy-indices", default="0.6,1.0,1.5,2.0,3.0")
    args = parser.parse_args()

    in_path = Path(args.input)
    fmt = infer_format(in_path, args.format)

    record, warnings, raw_excerpt = load_record(in_path, fmt)
    casted = cast_record(record)

    if args.name:
        casted["name"] = args.name
    if args.birth_date:
        casted["birth_date"] = parse_birth_date(args.birth_date)
    if args.category:
        casted["category"] = args.category
    if args.employment_type:
        casted["employment_type"] = args.employment_type
    if args.is_4050_eligible:
        casted["is_4050_eligible"] = args.is_4050_eligible.lower() == "true"

    used_default_asof = False
    if not casted["as_of"]:
        casted["as_of"] = parse_birth_date(args.as_of_default)
        warnings.append("缺少as_of，已使用默认值")
        used_default_asof = True

    missing = [k for k in REQUIRED_FIELDS if not casted[k]]
    if missing:
        raise ValueError(f"关键字段缺失: {missing}")

    strategy_indices = [float(x.strip()) for x in args.strategy_indices.split(",") if x.strip()]
    assumptions = {
        "avg_wage_growth_rate": float(args.assumption_wage_growth),
        "personal_account_bookkeeping_rate": float(args.assumption_book_rate),
        "personal_contribution_rate": float(args.assumption_personal_rate),
    }

    payload = build_target_payload(casted, strategy_indices, assumptions)
    confidence = estimate_confidence(record, casted, fmt, used_default_asof)
    low_confidence = [k for k, v in confidence.items() if v < 0.75]

    output = {
        "source": {
            "input_file": str(in_path),
            "input_format": fmt,
        },
        "warnings": warnings,
        "raw_text_excerpt": raw_excerpt,
        "review": {
            "required_fields": REQUIRED_FIELDS,
            "missing_required_fields": [],
            "field_confidence": confidence,
            "low_confidence_fields": low_confidence,
            "needs_manual_confirmation": len(low_confidence) > 0,
        },
        "payload": payload,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(out_path), "warnings": warnings}, ensure_ascii=False))


if __name__ == "__main__":
    main()
