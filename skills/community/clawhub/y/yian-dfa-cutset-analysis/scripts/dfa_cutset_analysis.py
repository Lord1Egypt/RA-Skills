#!/usr/bin/env python3
"""
DFA Cut-Set Analysis updater  (v3 — format + H/O auto-draft).

Updates the target "DFA Analysis-CutSet" sheet based on the source
"Cut-Set List" sheet within the same Excel workbook.

Target-sheet structure (per user "毅安" screenshots):
  * Each cut-set occupies a 7-row block.
  * A/B/C/D are merged across the 7 rows.
  * E is merged in pairs: rows 0-1, 2-3, 4-5 of the block; row 6 E is single.
  * F holds 7 standard DFA coupling-factor labels (1 per row).
  * G..O are the DFA analysis columns (root cause / reference example /
    possible root cause / fault type before / SM before / fault type after /
    update required / SM after / remark).

Key rules:
  * Source sheet selection: among sheets whose title contains "Cut-Set List",
    PREFER the one that does NOT contain "old" (case-insensitive).
  * ONLY cut-sets whose Order (source column E) is 2 or 3 are processed.
  * On the target sheet, only cut-sets whose order is 2/3 are ever touched.
  * Existing Order-2/3 blocks are refreshed (A/B/C/D/E/F); their human-filled
    G..O are left intact.
  * Genuinely new Order-2/3 cutsets are appended as 7-row blocks at the bottom,
    with the cutset name in D shown in RED.  For these NEW blocks we also
    auto-draft G..O by re-using the exact per-(component, coupling-factor)
    patterns observed in the existing (already human-filled) blocks, and we
    copy the cell formatting (border / font / alignment / fill) from a donor
    normal block so the new rows look identical to the existing ones.

Usage:
    dfa_cutset_analysis.py <excel_path> [--backup] [--source-sheet NAME]
                           [--target-sheet NAME] [--order 2 3]
"""

import argparse
import copy
import re
import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, Color

# ---------------------------------------------------------------------------
# Column mappings (1-indexed, matching the Excel header A..O)
# ---------------------------------------------------------------------------
SRC_COL = {
    "no": 1,        # A
    "top_event": 2, # B
    "asil": 3,      # C
    "cutset": 4,    # D
    "order": 5,     # E  (Order of the cut-set)
    "desc": 6,      # F
}

TGT_COL = {
    "no": 1,            # A  编号
    "top_event": 2,     # B  顶级事件ID
    "asil": 3,          # C  汽车安全完整性等级
    "cutset": 4,        # D  Minimum最小割集(或2/3)
    "coupling": 5,      # E  EV 说明
    "source": 6,        # F  DFA 耦合因素
    "root_cause": 7,    # G  共因和级联失效的来源
    "ref_example": 8,   # H  相关项级/系统级DFA的参考示例
    "possible_root": 9, # I  可能的根本原因(共因或级联失效)
    "fault_before": 10, # J  DFA分析前定义的故障类型
    "sm_before": 11,    # K  DFA分析前定义安全措施
    "fault_after": 12,  # L  DFA分析后所需的故障类型
    "update_required": 13, # M 是否需要更新安全措施
    "sm_after": 14,     # N  DFA分析后的新安全措施
    "remark": 15,       # O  备注
}

ASIL_RE = re.compile(r"ASIL\s+[A-Z]+(?:/[A-Z]+)?", re.IGNORECASE)
SM_MARKERS = ["Implemented SMs", "Implemented SM", "SM_"]

RED_FONT = Font(color="FF0000")

DEFAULT_ORDERS = (2, 3)
BLOCK_HEIGHT = 7

# Standard DFA coupling-factor labels in column F, one per row of the 7-row block.
COUPLING_FACTOR_LABELS = [
    "共享资源/ Shared resourse",
    "共享信息输入/ Shared Information Inputs",
    "环境抗干扰能力不足/ Insufficient Environmental Immunity",
    "系统耦合 / Systematic Coupling",
    "同类型组件/  Component of Identical Type",
    "通讯/ Communication",
    "非预期接口/ Unintended Interface",
]

# ---------------------------------------------------------------------------
# Fixed G / H text per coupling-factor label (verified identical across all
# existing blocks in the workbook — these are definitions, safe to auto-fill).
# ---------------------------------------------------------------------------
G_TEXT = {
    0: "a) random hardware failures\ng) failures of common external resources or information",
    1: "a) random hardware failures",
    2: "f) environmental factors \nh) stress due to specific situation",
    3: "b) development faults\nc) manufacturing faults\nd) installation faults\ne) service faults\nh) stress due to specific situation",
    4: "a) random hardware failures\nb) development faults",
    5: "a) random hardware failures\nb) development faults\nd) installation faults\ne) repair faults\ni) ageing and wear",
    6: "a) random hardware failures\nb) development faults\nd) installation faults\nh) stress due to specific situation",
}
H_TEXT = {
    0: "— Power supply (see also Insufficient Environmental Immunity)\n— Wiring harness\n— Data and communication busses\n— Powerstage",
    1: "— External messages (e.g. CAN, Flexray, or AUTOSAR\nRTE messages)\n— External physical signals (e.g. magnetic fields,\nremote/radio signals)\n— Readings detected by capacitive/radar/optical\nsensors",
    2: "— Mechanical coupling\n— Flammable material",
    3: "— 用于多个要素的相同生产过程/ Identical production processes used for multiple elements\n— 用于多个要素的相同维修过程/  Identical repair processes used for multiple elements.",
    4: "— Same type of actuator/ power stage e.g. motor\n— Same type of sensors",
    5: "— CAN connection between two ECUs of the same\nsystem\n— Communication between two microcontrollers within the same ECU",
    6: "— One functionality overruling the other because of missing",
}

# ---------------------------------------------------------------------------
# Component-aware I-text (col I, "可能的根本原因") per (component, label).
# These strings are taken VERBATIM from the existing, already-reviewed blocks
# (including the original spelling), so the auto-draft reuses real content.
# ---------------------------------------------------------------------------
ITEXT = {
    "TMR sensor": {
        0: "Same power supply KL30 input for  TMR Sensor Component  and  SMs in PMIC IC TLF35584, Power supply failure-e.g. Over-voltage, etc. are possible cause both failure, will possible violate the SG",
        1: "No shared information inputs for TMR Sensor Component power supply  and  SMs in PMIC IC TLF35584",
        2: "Vibration, Pressure, Humidity, Condensation, Corrosion, EMC-ESD, Mechanical stress, Wear, Aging, Dust (coating), Water and other fluids intrusion affects both TMR Sensor Component power supply  and  SMs in PMIC IC TLF35584",
        3: "TMR sensor component  and EPS ECU are developed by different company, no common systematic human, or tool error",
        4: "Not apply identical type TMR sensor component and EPS ECU",
        5: "No communication interface between  TMR Sensor Component power supply and  SMs in PMIC IC TLF35584",
        6: "Thermal may imapct TMR Sensor Component power supply and  SMs in PMIC IC TLF35584 damage",
    },
    "TAS sensor": {
        0: "Same power supply KL30 input for  TAS Sensor Component  and  SMs in PMIC IC TLF35584, Power supply failure-e.g. Over-voltage, etc. are possible cause both failure, will possible violate the SG",
        1: "No shared information inputs for TAS Sensor Component power supply  and  SMs in PMIC IC TLF35584",
        2: "Vibration, Pressure, Humidity, Condensation, Corrosion, EMC-ESD, Mechanical stress, Wear, Aging, Dust (coating), Water and other fluids intrusion affects both TAS Sensor Component power supply  and  SMs in PMIC IC TLF35584",
        3: "TAS sensor component  and EPS ECU are developed by different company, no common systematic human, or tool error",
        4: "Not apply identical type TAS sensor component and EPS ECU",
        5: "No communication interface between  TAS Sensor Component power supply and  SMs in PMIC IC TLF35584",
        6: "Thermal may imapct TAS Sensor Component power supply and  SMs in PMIC IC TLF35584 damage",
    },
    "current sensor": {
        0: "No shared resourse for current sensor component  function and SMs in EPS ECU to detect current sensor fault(e.g. SM_CH1_CS_01: Sum of IA/IB/IC)",
        1: "No shared information inputs for Read phase A/B/C current and process Id/Iq signal and SM_CH1_CS_01/02",
        2: "Vibration, Pressure, Humidity, Condensation, Corrosion, EMC-ESD, Mechanical stress, Wear, Aging, Dust (coating), Water and other fluids intrusion affects both Read phase A/B/C current and process Id/Iq signal and SM_CH1_CS_01/02",
        3: "Current sensor component  and EPS ECU are developed by different company, no common systematic human, or tool error",
        4: "Not apply identical type current sensor component and EPS ECU",
        5: "No communication interface between Read phase A/B/C current and process Id/Iq signal and SM_CH1_CS_01/02",
        6: "Thermal may imapct Read phase A/B/C current and process Id/Iq signal and SM_CH1_CS_01/02",
    },
    "ECU power supply": {
        0: "Same power supply KL30 input for ECU power supply module and SMs in PMIC IC TLF35584/EPS ECU, Power supply failure-e.g. Over-voltage, etc. are possible cause both failure, will possible violate the SG",
        1: "No shared information inputs for ECU power supply module and SMs in PMIC IC TLF35584/EPS ECU",
        2: "Vibration, Pressure, Humidity, Condensation, Corrosion, EMC-ESD, Mechanical stress, Wear, Aging, Dust (coating), Water and other fluids intrusion affects both ECU power supply module and SMs in PMIC IC TLF35584/EPS ECU",
        3: "ECU power supply  and  SMs in PMIC IC TLF35584 are developed by different compancy",
        4: "Not apply identical type for ECU power supply module and SMs in PMIC IC TLF35584/EPS ECU, and integrated the SM from IC safety manual",
        5: "No communication interface between  ECU power supply module and SMs in PMIC IC TLF35584/EPS ECU",
        6: "Thermal may imapct ECU power supply module and SMs in PMIC IC TLF35584/EPS ECU",
    },
    "Vcore": {
        0: "Same power supply KL30 input for  Voltage Convert Vcore(12v->3.3v)  and  SMs in PMIC IC TLF35584, Power supply failure-e.g. Over-voltage, etc. are possible cause both failure, will possible violate the SG",
        1: "No shared information inputs for Voltage Convert Vcore(12v->3.3v)  and  SMs in PMIC IC TLF35584",
        2: "Vibration, Pressure, Humidity, Condensation, Corrosion, EMC-ESD, Mechanical stress, Wear, Aging, Dust (coating), Water and other fluids intrusion affects both Voltage Convert Vcore(12v->3.3v)  and  SMs in PMIC IC TLF35584",
        3: "Voltage Convert Vcore(12v->3.3v)  and  SMs in PMIC IC TLF35584 are developed by IC supplier, integrated the SM from IC safety manual",
        4: "Not apply identical type for Voltage Convert Vcore(12v->3.3v)  and  SMs in PMIC IC TLF35584, and integrated the SM from IC safety manual",
        5: "No communication interface between  Voltage Convert Vcore(12v->3.3v)  and  SMs in PMIC IC TLF35584",
        6: "Thermal may imapct Voltage Convert Vcore(12v->3.3v)  and  SMs in PMIC IC TLF35584 damage",
    },
    # EPS ECU internal functions (motor control / torque / angle / output / temp ...).
    # Drafted by analogy with the sensor/power templates; to be refined by the engineer.
    "EPS ECU": {
        0: "Same power supply KL30 input for EPS ECU and SMs in EPS ECU, Power supply failure-e.g. Over-voltage, etc. are possible cause both failure, will possible violate the SG",
        1: "No shared information inputs for EPS ECU function and SMs in EPS ECU",
        2: "Vibration, Pressure, Humidity, Condensation, Corrosion, EMC-ESD, Mechanical stress, Wear, Aging, Dust (coating), Water and other fluids intrusion affects both EPS ECU function and SMs in EPS ECU",
        3: "EPS ECU function and SMs in EPS ECU are developed by same company, common systematic human, or tool error should be considered",
        4: "Not apply identical type for EPS ECU function and SMs in EPS ECU",
        5: "No communication interface between EPS ECU function and SMs in EPS ECU",
        6: "Thermal may imapct EPS ECU function and SMs in EPS ECU damage",
    },
}

# Component detection: keyword (substring, case-insensitive) -> canonical label.
COMPONENT_KEYWORDS = [
    ("TMR", "TMR sensor"),
    ("TAS", "TAS sensor"),
    ("current", "current sensor"),
    ("Id/Iq", "current sensor"),
    ("IA/IB/IC", "current sensor"),
    ("Vcore", "Vcore"),
    ("Voltage Convert", "Vcore"),
    ("KL30", "ECU power supply"),
    ("Power supply", "ECU power supply"),
    ("PMIC", "ECU power supply"),
    ("TLF", "ECU power supply"),
    ("Pre-driver", "ECU power supply"),
    ("A4918", "ECU power supply"),
]
# EPS ECU internal functions (motor control / torque / angle / output / temp ...)
# are the fallback element when no specific sensor/power component matches.
EPS_ECU_KEYWORDS = ["EPS_ECU", "MOTOR", "ROTOR", "TORQUE", "ANGLE", "MRA", "SENT",
                    "SPI", "MOSFET", "SWCL", "OUTPUT", "TEMP", "VS_SIG", "LONGIACC",
                    "FS_", "CCMOTORVEL", "CCTORQUE", "CCVS", "SAFE_REQ", "APP_FUN",
                    "TORQUE_ALGO", "PROVIDE", "STEERING", "ECU", "EPS", "CH1", "CH2"]
# Priority order used when several components match (first wins for the I-text).
COMPONENT_PRIORITY = ["TMR sensor", "TAS sensor", "current sensor", "Vcore", "ECU power supply", "EPS ECU"]

# J/K/L/M/N/O draft constants per coupling-factor label.
# These follow the dominant pattern observed in the existing blocks and the
# DFA methodology (e.g. environmental / thermal coupling => CCF + NO; absence of
# coupling => N.A.).  They are DRAFTS for the engineer to confirm.
ENV_TEST_K = ("Implemented Vibration test, Pressure test, Humidity test, Condensation test, "
              "Corrosion test, EMC-ESD test, Mechanical stress test, Wear test, Aging test, "
              "Dust (coating) test, Water and other fluids intrusion test.\n"
              "--See DV/PV test report: Links: ")
THERMAL_K = ("To implement Thermal simulation experiment\n"
             "--See Thermal simulation experiment test report: Links: ")

def jo_constants(label_idx, components):
    """Return (J, K, L, M, N, O) draft for a coupling-factor label + components."""
    na = "N.A."
    if label_idx == 0:  # 共享资源
        if "current sensor" in components:
            return (na, na, na, na, na, na)
        return ("CCF", na, "CCF", "NO", na, na)
    if label_idx == 1:  # 共享信息输入
        return (na, na, na, na, na, na)
    if label_idx == 2:  # 环境抗干扰
        return ("CCF", ENV_TEST_K, "CCF", "NO", na, na)
    if label_idx == 3:  # 系统耦合
        return (na, na, na, na, na, na)
    if label_idx == 4:  # 同类型组件
        return (na, na, na, na, na, na)
    if label_idx == 5:  # 通讯
        return (na, na, na, na, na, na)
    if label_idx == 6:  # 非预期接口
        return ("CCF", THERMAL_K, "CCF", "NO", na, na)
    return (na, na, na, na, na, na)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_source_sheet(workbook, keyword, exclude="old"):
    keyword_l = keyword.lower()
    exclude_l = exclude.lower()
    matches = [n for n in workbook.sheetnames if keyword_l in n.lower()]
    if not matches:
        return None
    non_excluded = [n for n in matches if exclude_l not in n.lower()]
    return workbook[(non_excluded or matches)[0]]


def find_target_sheet(workbook, keyword):
    keyword_l = keyword.lower()
    for name in workbook.sheetnames:
        if keyword_l in name.lower():
            return workbook[name]
    return None


def compute_order_from_name(name):
    if not name:
        return None
    parts = re.split(r"[.+]", name)
    parts = [p for p in parts if p.strip()]
    return len(parts) if parts else 1


def build_order_map(workbook, keyword="Cut-Set List"):
    keyword_l = keyword.lower()
    order_map = {}
    for name in workbook.sheetnames:
        if keyword_l in name.lower():
            ws = workbook[name]
            for row in ws.iter_rows(min_row=4, values_only=True):
                nm = row[SRC_COL["cutset"] - 1]
                od = row[SRC_COL["order"] - 1]
                if nm is None or str(nm).strip() == "":
                    continue
                nm = str(nm).strip()
                if nm not in order_map and od is not None:
                    try:
                        order_map[nm] = int(od)
                    except (ValueError, TypeError):
                        pass
    return order_map


def split_description(text):
    if not text:
        return "", ""
    text = str(text).strip()
    match = ASIL_RE.search(text)
    if match:
        start, end = match.span()
        return text[:start].strip(), text[end:].strip()
    for marker in SM_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx].strip(), text[idx:].strip()
    return text, ""


def build_e_failure_text(failure):
    return f"DFA Coupling Factor\nSource of Common Causes and Coupling Factors\n{failure}"


def build_e_safety_text(safety):
    return safety


def detect_components(text, name=""):
    """Detect the DFA element(s) from the source description and cutset name."""
    if not text and not name:
        return []
    t = str(text) + " " + str(name)
    tl = t.lower()
    found = []
    for kw, label in COMPONENT_KEYWORDS:
        if kw.lower() in tl:
            found.append(label)
    if not found:
        if any(k.lower() in tl for k in EPS_ECU_KEYWORDS):
            found.append("EPS ECU")
    # de-duplicate preserving priority order
    seen = set()
    ordered = []
    for c in COMPONENT_PRIORITY:
        if c in found and c not in seen:
            ordered.append(c)
            seen.add(c)
    return ordered


def get_block_end_row(target_ws, start_row, col=TGT_COL["cutset"]):
    for rng in target_ws.merged_cells.ranges:
        if rng.min_row == start_row and rng.min_col == col and rng.max_col == col:
            return rng.max_row
    return start_row


def iter_blocks(target_ws):
    """Yield (start_row, end_row, cutset_name) for each real 7-row cut-set block.

    A real block is identified by its D column being merged vertically (the
    sheet's header rows have an unmerged D and are skipped).
    """
    r = 2
    while r <= target_ws.max_row:
        cell_d = target_ws.cell(row=r, column=TGT_COL["cutset"])
        name = str(cell_d.value).strip() if cell_d.value else ""
        if not name:
            r += 1
            continue
        end = get_block_end_row(target_ws, r)
        if end <= r:
            # Not a merged block-start -> header / stray row; skip.
            r += 1
            continue
        yield r, end, name
        r = end + 1


def find_first_normal_block(target_ws):
    """Return the start row of the first non-strikethrough, black-font 7-row block.

    Skips the sheet header rows (whose D is not vertically merged).
    """
    r = 2
    while r <= target_ws.max_row:
        cell_d = target_ws.cell(row=r, column=TGT_COL["cutset"])
        name = str(cell_d.value).strip() if cell_d.value else ""
        if not name:
            r += 1
            continue
        end = get_block_end_row(target_ws, r)
        if end <= r:
            r += 1
            continue
        fnt = cell_d.font
        if getattr(fnt, "strike", False):
            r = end + 1
            continue
        col = fnt.color.rgb if fnt.color else None
        if col in (None, "000000", "FF000000"):
            return r
        r = end + 1
    return None


def copy_cell_style(src_cell, dst_cell):
    """Copy border/font/alignment/fill/number_format (color excluded)."""
    dst_cell.border = copy.copy(src_cell.border)
    f = copy.copy(src_cell.font)
    dst_cell.font = f  # color handled by caller
    dst_cell.alignment = copy.copy(src_cell.alignment)
    dst_cell.fill = copy.copy(src_cell.fill)
    dst_cell.number_format = src_cell.number_format


def read_source_rows(source_ws, orders=DEFAULT_ORDERS):
    rows = []
    for row in source_ws.iter_rows(min_row=2, values_only=True):
        cutset = row[SRC_COL["cutset"] - 1]
        if cutset is None or str(cutset).strip() == "":
            continue
        order_val = row[SRC_COL["order"] - 1]
        try:
            order = int(order_val) if order_val is not None else None
        except (ValueError, TypeError):
            order = None
        if order not in orders:
            continue
        rows.append({
            "no": row[SRC_COL["no"] - 1],
            "top_event": row[SRC_COL["top_event"] - 1],
            "asil": row[SRC_COL["asil"] - 1],
            "cutset": str(cutset).strip(),
            "order": order,
            "desc": row[SRC_COL["desc"] - 1],
        })
    return rows


def group_by_cutset(rows):
    grouped = {}
    for r in rows:
        grouped.setdefault(r["cutset"], []).append(r)
    return grouped


def merge_values(values, dedupe=True):
    cleaned = [str(v).strip() for v in values if v is not None and str(v).strip()]
    if dedupe:
        seen = []
        for v in cleaned:
            if v not in seen:
                seen.append(v)
        cleaned = seen
    return " ".join(cleaned)


def update_target(grouped, target_ws, order_map, orders=DEFAULT_ORDERS):
    source_names = set(grouped.keys())

    # Pass 1: refresh existing Order-2/3 blocks; strike obsolete ones.
    existing_names = set()
    for start_row, end_row, name in iter_blocks(target_ws):
        order = order_map.get(name)
        if order is None:
            order = compute_order_from_name(name)
        if order not in orders:
            continue

        if name in source_names:
            existing_names.add(name)
            group = grouped[name]
            for col in (TGT_COL["no"], TGT_COL["top_event"], TGT_COL["asil"], TGT_COL["cutset"]):
                cell = target_ws.cell(row=start_row, column=col)
                f = copy.copy(cell.font)
                f.strike = False
                f.color = None
                cell.font = f
            target_ws.cell(row=start_row, column=TGT_COL["no"], value=merge_values([r["no"] for r in group]))
            target_ws.cell(row=start_row, column=TGT_COL["top_event"], value=merge_values([r["top_event"] for r in group]))
            target_ws.cell(row=start_row, column=TGT_COL["asil"], value=merge_values([r["asil"] for r in group], dedupe=True))
            target_ws.cell(row=start_row, column=TGT_COL["cutset"], value=name)
            failure, safety = split_description(group[0]["desc"])
            target_ws.cell(row=start_row, column=TGT_COL["coupling"], value=build_e_failure_text(failure))
            target_ws.cell(row=start_row + 2, column=TGT_COL["coupling"], value=build_e_safety_text(safety))
        else:
            for col in (TGT_COL["no"], TGT_COL["top_event"], TGT_COL["asil"], TGT_COL["cutset"]):
                cell = target_ws.cell(row=start_row, column=col)
                f = copy.copy(cell.font)
                f.strike = True
                cell.font = f

    # Pass 2: append genuinely new cutsets as 7-row blocks with H/O draft.
    new_names = source_names - existing_names
    if not new_names:
        return

    donor_start = find_first_normal_block(target_ws)

    for name in sorted(new_names, key=lambda n: min((r["no"] for r in grouped[n] if r["no"] is not None), default=0)):
        group = grouped[name]
        start_row = target_ws.max_row + 1
        end_row = start_row + BLOCK_HEIGHT - 1
        is_ch2 = "CH2" in str(group[0]["desc"]).upper()

        # A/B/C/D (top-left cells before merging).
        target_ws.cell(row=start_row, column=TGT_COL["no"], value=merge_values([r["no"] for r in group]))
        target_ws.cell(row=start_row, column=TGT_COL["top_event"], value=merge_values([r["top_event"] for r in group]))
        target_ws.cell(row=start_row, column=TGT_COL["asil"], value=merge_values([r["asil"] for r in group], dedupe=True))
        cell_d = target_ws.cell(row=start_row, column=TGT_COL["cutset"], value=name)
        cell_d.font = RED_FONT

        # E narrative.
        failure, safety = split_description(group[0]["desc"])
        target_ws.cell(row=start_row, column=TGT_COL["coupling"], value=build_e_failure_text(failure))
        target_ws.cell(row=start_row + 2, column=TGT_COL["coupling"], value=build_e_safety_text(safety))

        # Detect components for H/O drafting (use both description and cutset name).
        components = detect_components(group[0]["desc"], name)
        primary = components[0] if components else None

        # Fill every cell of the 7-row block.
        for i in range(BLOCK_HEIGHT):
            rr = start_row + i
            label_idx = i
            flabel = COUPLING_FACTOR_LABELS[label_idx]

            target_ws.cell(row=rr, column=TGT_COL["source"], value=flabel)
            target_ws.cell(row=rr, column=TGT_COL["root_cause"], value=G_TEXT[label_idx])
            target_ws.cell(row=rr, column=TGT_COL["ref_example"], value=H_TEXT[label_idx])

            # I (possible root cause) — component-aware draft.
            if primary is not None:
                itext = ITEXT[primary][label_idx]
            else:
                itext = "【待确认】未自动识别组件，请补充共因/级联失效分析"
            target_ws.cell(row=rr, column=TGT_COL["possible_root"], value=itext)

            # J/K/L/M/N/O draft.
            j, k, l, m, n, o = jo_constants(label_idx, components)
            target_ws.cell(row=rr, column=TGT_COL["fault_before"], value=j)
            target_ws.cell(row=rr, column=TGT_COL["sm_before"], value=k)
            target_ws.cell(row=rr, column=TGT_COL["fault_after"], value=l)
            target_ws.cell(row=rr, column=TGT_COL["update_required"], value=m)
            target_ws.cell(row=rr, column=TGT_COL["sm_after"], value=n)
            target_ws.cell(row=rr, column=TGT_COL["remark"], value=o)

            # Copy formatting from donor block (if available).
            if donor_start is not None:
                for c in range(1, TGT_COL["remark"] + 1):
                    src = target_ws.cell(row=donor_start + i, column=c)
                    dst = target_ws.cell(row=rr, column=c)
                    copy_cell_style(src, dst)
                # Restore red D, preserving donor font name/size (only color changes).
                dst_d = target_ws.cell(row=rr, column=TGT_COL["cutset"])
                fd = copy.copy(dst_d.font)
                fd.color = Color(rgb="FFFF0000")
                dst_d.font = fd
                # Row height match.
                target_ws.row_dimensions[rr].height = target_ws.row_dimensions[donor_start + i].height

        # CH2 channel substitution in I/J/K/L/M/N/O text (best-effort).
        if is_ch2:
            for i in range(BLOCK_HEIGHT):
                rr = start_row + i
                for c in (TGT_COL["possible_root"], TGT_COL["sm_before"]):
                    v = target_ws.cell(row=rr, column=c).value
                    if isinstance(v, str) and "CH1" in v:
                        target_ws.cell(row=rr, column=c, value=v.replace("CH1", "CH2"))

        # Create merges for the new block.
        for col in (TGT_COL["no"], TGT_COL["top_event"], TGT_COL["asil"], TGT_COL["cutset"]):
            target_ws.merge_cells(start_row=start_row, start_column=col,
                                  end_row=end_row, end_column=col)
        target_ws.merge_cells(start_row=start_row, start_column=TGT_COL["coupling"],
                              end_row=start_row + 1, end_column=TGT_COL["coupling"])
        target_ws.merge_cells(start_row=start_row + 2, start_column=TGT_COL["coupling"],
                              end_row=start_row + 3, end_column=TGT_COL["coupling"])
        target_ws.merge_cells(start_row=start_row + 4, start_column=TGT_COL["coupling"],
                              end_row=start_row + 5, end_column=TGT_COL["coupling"])


def main():
    parser = argparse.ArgumentParser(
        description="Update DFA Analysis-CutSet sheet from Cut-Set List sheet (Order 2/3 only)."
    )
    parser.add_argument("excel_path", help="Path to the Excel workbook (.xlsx)")
    parser.add_argument("--source-sheet", help="Exact source sheet name (auto-detected if omitted)")
    parser.add_argument("--target-sheet", help="Exact target sheet name (auto-detected if omitted)")
    parser.add_argument("--order", nargs="+", type=int, default=list(DEFAULT_ORDERS),
                        help="Which Order values to process (default: 2 3)")
    parser.add_argument("--backup", action="store_true", help="Create a .bak copy before modifying")
    args = parser.parse_args()

    orders = tuple(args.order)
    path = Path(args.excel_path)
    if not path.exists():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(1)

    wb = load_workbook(path)
    source_ws = wb[args.source_sheet] if args.source_sheet else find_source_sheet(wb, "Cut-Set List")
    target_ws = wb[args.target_sheet] if args.target_sheet else find_target_sheet(wb, "DFA Analysis-CutSet")

    if source_ws is None:
        print("[ERROR] Could not find source sheet containing 'Cut-Set List'", file=sys.stderr)
        sys.exit(1)
    if target_ws is None:
        print("[ERROR] Could not find target sheet containing 'DFA Analysis-CutSet'", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Source sheet: {source_ws.title}")
    print(f"[INFO] Target sheet: {target_ws.title}")
    print(f"[INFO] Processing Order values: {list(orders)}")

    order_map = build_order_map(wb, "Cut-Set List")
    rows = read_source_rows(source_ws, orders=orders)
    grouped = group_by_cutset(rows)
    print(f"[INFO] Order map covers {len(order_map)} cut-set names")
    print(f"[INFO] Found {len(rows)} source rows, {len(grouped)} unique cutsets (Order {list(orders)})")

    if args.backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        wb.save(backup_path)
        print(f"[INFO] Backup saved: {backup_path}")

    update_target(grouped, target_ws, order_map, orders=orders)

    wb.save(path)
    print(f"[OK] Workbook updated: {path}")


if __name__ == "__main__":
    main()
