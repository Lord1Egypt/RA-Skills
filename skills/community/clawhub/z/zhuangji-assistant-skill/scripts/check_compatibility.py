#!/usr/bin/env python3
"""装机兼容性检查引擎。

用法:
  python check_compatibility.py --cpu cpu-intel-i5-14400f --mb mb-asus-b760m-k-d4 \
    --mem mem-ddr4-3200-16-kingston-beast --gpu gpu-gigabyte-rtx5070-windforce-oc \
    --psu psu-msi-a750gl-pcie5 --case case-jonsbo-d31-mesh-black --cooler cooler-tr-pa120se
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

import yaml

from component_inference import enrich_item, infer_native_16pin_psu, infer_requires_16pin_gpu

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


class CompatibilityChecker:
    """装机兼容性检查引擎。

    检查 11 项兼容性: CPU↔主板, 内存↔主板(代际/数量/容量),
    显卡↔机箱, 硬盘↔主板, 电源↔功耗, 散热↔机箱, 机箱↔主板, 机箱↔电源。
    """

    # 机箱版型向下兼容表
    FORM_FACTOR_MAP = {
        "EATX": ["EATX", "ATX", "MATX", "ITX"],
        "ATX":  ["ATX", "MATX", "ITX"],
        "MATX": ["MATX", "ITX"],
        "M-ATX": ["MATX", "ITX"],
        "Mini-ITX": ["ITX"],
        "ITX": ["ITX"],
    }

    def _parse_num(self, val, default=0):
        """从字符串/数字中提取数值。"""
        if isinstance(val, (int, float)):
            return val if not (isinstance(val, float) and math.isnan(val)) else default
        if isinstance(val, str):
            cleaned = re.sub(r"[^\d.-]", "", val)
            try:
                return float(cleaned) if "." in cleaned else int(cleaned)
            except (ValueError, TypeError):
                return default
        return default

    def _parse_rated_wattage(self, psu):
        """Prefer the rated wattage in PSU model text over noisy imported fields."""
        if not psu:
            return 0
        model = str(psu.get("model", ""))
        match = re.search(r"额定\s*(\d{3,4})\s*W", model, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
        match = re.search(r"(\d{3,4})\s*W", model, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
        return self._parse_num(psu.get("wattage_w", 0))

    def _normalize(self, val):
        """移除非字母数字字符并转大写，用于接口/尺寸比较。"""
        if not val:
            return ""
        return re.sub(r"[^0-9a-zA-Z]", "", str(val)).upper()

    def _normalize_socket_list(self, val):
        """Normalize socket strings while preserving multi-socket separators."""
        if not val:
            return []
        parts = re.split(r"[/,|]", str(val))
        normalized = []
        for part in parts:
            socket = self._normalize(part)
            if socket.startswith("SOCKET"):
                socket = socket[len("SOCKET"):]
            if socket:
                normalized.append(socket)
        return normalized

    def _normalize_form_factor(self, ff):
        """标准化版型名称用于比较。"""
        if not ff:
            return ""
        ff = ff.upper().replace("-", "").replace("_", "").replace(" ", "")
        mapping = {"MATX": "MATX", "MINIITX": "ITX", "MICROATX": "MATX",
                   "EATX": "EATX", "ATX": "ATX"}
        return mapping.get(ff, ff)

    # --- 11 项检查函数 ---

    def check_cpu_motherboard(self, cpu, mb):
        """检查 CPU 和主板兼容性: socket 接口匹配。"""
        if not cpu or not mb:
            return {"type": "msg", "msg": f"缺少必要组件{('主板' if cpu else 'CPU')}"}
        cpu_sockets = self._normalize_socket_list(cpu.get("socket", ""))
        mb_sockets = self._normalize_socket_list(mb.get("socket", ""))
        if cpu_sockets and mb_sockets:
            if not set(cpu_sockets).intersection(mb_sockets):
                return {"type": "error",
                        "msg": f"接口不兼容，CPU【{cpu.get('socket')}】，主板【{mb.get('socket')}】"}
        return {"type": "success", "msg": f"CPU和主板接口兼容【{mb.get('socket')}】"}

    def check_memory_motherboard(self, memory_list, mb):
        """检查内存与主板兼容性: DDR 代际 + 频率。"""
        if not mb:
            return [{"type": "msg", "msg": "缺少必要组件主板"}]
        if not memory_list:
            return [{"type": "msg", "msg": "缺少必要组件内存"}]
        results = []
        for i, mem in enumerate(memory_list):
            label = str(i + 1) if len(memory_list) > 1 else ""
            mem_gen = mem.get("generation", "")
            mb_gens = mb.get("memory_generations", [])
            if not mem_gen or not mb_gens:
                results.append({"type": "msg", "msg": f"内存{label}缺少接口信息"})
                continue
            if mem_gen not in mb_gens:
                results.append({"type": "error",
                    "msg": f"主板和内存{label}接口不兼容，主板支持【{'/'.join(mb_gens)}】，内存【{mem_gen}】"})
                continue
            mem_freq = self._parse_num(mem.get("frequency_mt", 0))
            mb_freq = self._parse_num(mb.get("memory_freq_max", 0))
            if mem_freq and not mb_freq:
                results.append({"type": "skipped",
                    "msg": f"主板缺少内存最高频率字段，未检查内存{label}频率【{mem_freq}MHz】是否在主板支持范围内"})
            elif mem_freq and mb_freq and mem_freq > mb_freq:
                results.append({"type": "warn",
                    "msg": f"内存{label}频率【{mem_freq}MHz】超过主板支持【{mb_freq}MHz】，可能不稳定"})
            else:
                results.append({"type": "success", "msg": f"主板和内存{label}接口兼容【{mem_gen}】"})
        return results

    def check_memory_slots(self, memory_list, mb):
        """检查内存数量 vs 主板插槽数。"""
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        if not memory_list:
            return {}
        total_sticks = sum(self._parse_num(m.get("module_count", 1)) for m in memory_list)
        mb_slots = self._parse_num(mb.get("memory_slots", 0))
        if not total_sticks or not mb_slots:
            return {}
        if total_sticks > mb_slots:
            return {"type": "error",
                "msg": f"内存数量过多，已选【{total_sticks}条】，主板插槽数量【{mb_slots}个】"}
        return {"type": "success", "msg": "内存插槽数量充足"}

    def check_memory_capacity(self, memory_list, mb):
        """检查内存总容量 vs 主板最大容量。"""
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        if not memory_list:
            return {}
        total_gb = sum(self._parse_num(m.get("capacity_gb", 0)) for m in memory_list)
        max_gb = self._parse_num(mb.get("memory_max_gb", 0))
        if not total_gb or not max_gb:
            return {}
        if total_gb > max_gb:
            return {"type": "error",
                "msg": f"内存总容量【{total_gb}GB】超过主板最大支持【{max_gb}GB】"}
        return {"type": "success", "msg": "内存容量在主板支持范围内"}

    def check_gpu_case(self, gpu, case, index=""):
        """检查显卡长度 vs 机箱显卡限长。"""
        if not gpu:
            return {}
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        gpu_len = self._parse_num(gpu.get("length_mm", 0))
        case_limit = self._parse_num(case.get("gpu_length_mm", 0))
        if not gpu_len or not case_limit:
            return {}
        if gpu_len > case_limit:
            return {"type": "error",
                "msg": f"显卡{index}长度【{gpu_len}mm】超过机箱限制【{case_limit}mm】"}
        return {"type": "success", "msg": f"显卡{index}长度在机箱限制内"}

    def check_storage_motherboard(self, storage_list, mb):
        """检查硬盘接口 vs 主板接口。"""
        if not storage_list:
            return {"type": "msg", "msg": "缺少必要组件硬盘"}
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        m2_slots = self._parse_num(mb.get("m2_slots", 0))
        m2_count = sum(1 for s in storage_list
                       if "M.2" in s.get("form_factor", "") or "M.2" in s.get("interface", ""))
        if m2_count > 0 and not m2_slots:
            return {"type": "msg", "msg": "主板缺少M.2接口数量信息，需下单前复核"}
        if m2_count > 0 and m2_slots > 0 and m2_count > m2_slots:
            return {"type": "error",
                "msg": f"M.2硬盘数量【{m2_count}个】超过主板M.2接口数【{m2_slots}个】"}
        return {"type": "success", "msg": "硬盘接口兼容"}

    def check_sata_ports(self, storage_list, mb):
        """检查 SATA 设备数 vs 主板 SATA 口数。"""
        if not storage_list:
            return {}
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        sata_count = sum(1 for s in storage_list
                         if "SATA" in s.get("interface", "") and "M.2" not in s.get("form_factor", ""))
        sata_ports = self._parse_num(mb.get("sata_ports", 0))
        if not sata_count or not sata_ports:
            return {}
        if sata_count > sata_ports:
            return {"type": "error",
                "msg": f"SATA设备【{sata_count}个】超过主板SATA口【{sata_ports}个】"}
        return {"type": "success", "msg": "SATA接口数量充足"}

    def check_psu_power(self, psu, cpu, gpu_list, extra_w=50):
        """检查电源功率是否满足整机功耗。

        余量公式: recommended = ceil((cpu_w + gpu_w + extra) * 1.35)
        extra_w 默认 50W (主板+内存+硬盘+风扇)。
        """
        if not psu:
            return {"type": "msg", "msg": "缺少必要组件电源"}
        psu_w = self._parse_rated_wattage(psu)
        cpu_w = self._parse_num(cpu.get("power_w", 0)) if cpu else 0
        gpu_w = sum(self._parse_num(g.get("power_w", 0)) for g in (gpu_list or []))
        if not psu_w:
            return {"type": "msg", "msg": "电源缺少功率信息"}
        if cpu and not cpu_w:
            return {"type": "msg", "msg": "CPU缺少功耗信息，电源功率需人工复核"}
        if gpu_list and not gpu_w:
            return {"type": "msg", "msg": "显卡缺少功耗信息，电源功率需人工复核"}
        recommended = math.ceil((cpu_w + gpu_w + extra_w) * 1.35)
        if psu_w < recommended:
            return {"type": "error",
                "msg": f"电源功率【{psu_w}W】不足，建议≥{recommended}W (CPU {cpu_w}W + GPU {gpu_w}W + 其他 {extra_w}W ×1.35)"}
        margin = psu_w - recommended
        if margin < 50:
            return {"type": "warn",
                "msg": f"电源功率【{psu_w}W】刚好够用，建议功率≥{recommended + 50}W留更多余量"}
        return {"type": "success",
            "msg": f"电源功率【{psu_w}W】充足，推荐功率{recommended}W，余量{margin}W"}

    def check_gpu_power_connector(self, gpu, psu):
        """检查显卡供电接口兼容性。"""
        if not gpu or not psu:
            return {}
        requires_16pin = infer_requires_16pin_gpu(gpu)
        native_16pin = infer_native_16pin_psu(psu)
        if requires_16pin and native_16pin is True:
            return {"type": "success", "msg": "显卡16pin供电与电源原生接口匹配"}
        if requires_16pin and native_16pin is False:
            return {"type": "warn",
                "msg": "显卡需要16pin供电，当前电源未标明原生16pin接口，需复核线材；无原生线材时可使用转接线"}
        if requires_16pin:
            return {"type": "msg",
                "msg": "显卡需要16pin供电，电源缺少原生接口字段，需下单前复核线材；无原生线材时可使用转接线"}
        return {}

    def check_cooler_case(self, cooler, case):
        """检查散热器与机箱兼容性: 风冷高度/水冷冷排 vs 机箱限制。"""
        if not cooler:
            return {"type": "msg", "msg": "缺少必要组件散热"}
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        cooler = enrich_item("coolers", cooler)
        cooler_type = cooler.get("type", "air")
        if cooler_type == "air":
            cooler_height = self._parse_num(cooler.get("height_mm", 0))
            case_limit = self._parse_num(case.get("cpu_cooler_height_mm", 0))
            if cooler_height and case_limit:
                if cooler_height > case_limit:
                    return {"type": "error",
                        "msg": f"风冷高度【{cooler_height}mm】超过机箱限制【{case_limit}mm】"}
                return {"type": "success", "msg": "风冷高度在机箱限制内"}
        elif cooler_type in ("liquid", "water", "水冷"):
            radiator = cooler.get("radiator_mm", "")
            rad_support = case.get("radiator_support", [])
            if radiator and rad_support:
                rad_str = str(radiator)
                supported = any(rad_str in str(s) for s in rad_support)
                if not supported:
                    return {"type": "error",
                        "msg": f"冷排【{radiator}】不在机箱支持范围【{rad_support}】"}
                return {"type": "success", "msg": "冷排在机箱支持范围内"}
        return {}

    def check_case_motherboard(self, case, mb):
        """检查机箱是否支持主板版型。

        逻辑: 机箱支持列表中的每种版型，通过 FORM_FACTOR_MAP 向下兼容
        更小的版型。如果主板版型出现在任何机箱支持版型的兼容列表中，
        则机箱可以装下该主板。
        """
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        mb_ff = mb.get("form_factor", "")
        case_support = case.get("motherboard_support", [])
        ff_normalized = self._normalize_form_factor(mb_ff)
        support_normalized = [self._normalize_form_factor(s) for s in case_support]
        # 直接匹配
        if ff_normalized in support_normalized:
            return {"type": "success", "msg": f"机箱支持{mb_ff}版型"}
        # 向下兼容: 机箱支持的每种版型可以兼容更小的主板版型
        for case_ff in support_normalized:
            compatible_list = self.FORM_FACTOR_MAP.get(case_ff, [])
            if ff_normalized in compatible_list:
                return {"type": "success", "msg": f"机箱支持{mb_ff}版型(通过{case_ff}向下兼容)"}
        return {"type": "error",
            "msg": f"机箱与主板版型不匹配，机箱支持【{'/'.join(case_support)}】，主板【{mb_ff}】"}

    def check_case_psu(self, case, psu):
        """检查机箱电源位 vs 电源尺寸。"""
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        if not psu:
            return {}
        case_model = str(case.get("model", ""))
        case_psu_support = [self._normalize(s) for s in case.get("psu_support", ["ATX"])]
        model_special = any(
            term in case_model.upper()
            for term in ("ITX", "MINI", "SFX", "NAS", "HTPC", "卧式", "小型", "紧凑")
        )
        small_psu_forms = ("SFX", "SFXL", "TFX", "FLEX")
        small_psu_only = "ATX" not in case_psu_support and any(s in small_psu_forms for s in case_psu_support)
        special_case = model_special or small_psu_only
        psu_size = self._normalize(psu.get("form_factor"))
        if not psu_size:
            if "ATX" in case_psu_support and not special_case:
                psu_size = "ATX"
            else:
                return {"type": "msg", "msg": "小机箱或特殊电源位需要确认电源规格(ATX/SFX/SFX-L/FLEX)及限长/限高"}
        if not case_psu_support:
            return {"type": "msg", "msg": "机箱缺少电源规格支持信息，需下单前复核"}

        if "ATX" in case_psu_support and not special_case and psu_size in small_psu_forms:
            return {"type": "error",
                "msg": "普通ATX/MATX机箱默认不使用SFX/SFX-L/FLEX/TFX小电源；若明确复用小电源，需单独确认转接支架、线材长度和电源限长/限高"}

        psu_len = self._parse_num(psu.get("length_mm", 0))
        case_limit = self._parse_num(
            case.get("psu_length_mm", 0) or case.get("psu_max_length_mm", 0) or case.get("psu_clearance_mm", 0)
        )
        if psu_size in case_psu_support:
            if special_case and (not case_limit or not psu_len):
                return {"type": "skipped",
                    "msg": "小机箱或特殊电源位缺少机箱电源限长或电源长度字段，需下单前复核限长/限高、转接支架、线材弯折和硬盘笼空间"}
            if case_limit and psu_len and psu_len > case_limit:
                return {"type": "error",
                    "msg": f"电源长度【{psu_len}mm】超过机箱电源位限制【{case_limit}mm】"}
            if case_limit and psu_len and case_limit - psu_len < 20:
                return {"type": "warn",
                    "msg": f"电源长度【{psu_len}mm】接近机箱电源位限制【{case_limit}mm】，需复核线材弯折、限高和硬盘笼空间"}
            if case_limit and not psu_len and special_case:
                return {"type": "msg",
                    "msg": f"机箱电源位限制【{case_limit}mm】，电源缺少长度字段，需下单前复核限长/限高和线材空间"}
            return {"type": "success", "msg": "机箱和电源规格匹配"}
        return {"type": "error",
            "msg": f"机箱和电源规格不匹配，机箱支持【{case.get('psu_support')}】，电源【{psu.get('form_factor', psu_size)}】"}

    # --- 主入口 ---

    def _skipped(self, msg):
        return {"type": "skipped", "msg": msg}

    def _add_check(self, checks, name, result, skipped_msg="无可检查项"):
        checks.append((name, result or self._skipped(skipped_msg)))

    def check_all(self, build, strict=False, missing_ids=None):
        """检查完整配置的兼容性。

        Args:
            build: dict with keys: cpu, motherboard, memory (list),
                   storage (list), gpu (list), psu, cooler, case
            strict: final-build mode. Missing core parts become errors.
            missing_ids: IDs passed by the caller but not found in the library.
        Returns:
            {"overall": "pass"|"warn"|"fail", "checks": [...], "severity": {...}}
        """
        cpu = build.get("cpu")
        mb = build.get("motherboard")
        mem = build.get("memory", [])
        storage = build.get("storage", [])
        gpus = build.get("gpu", [])
        psu = build.get("psu")
        cooler = build.get("cooler")
        case = build.get("case")
        checks = []
        for missing_id in (missing_ids or []):
            checks.append(("ID校验", {"type": "error", "msg": f"未找到配件ID: {missing_id}"}))
        if strict:
            required = [
                ("CPU", cpu),
                ("主板", mb),
                ("内存", mem),
                ("硬盘", storage),
                ("显卡", gpus),
                ("电源", psu),
                ("散热", cooler),
                ("机箱", case),
            ]
            for label, value in required:
                if value is None or value == []:
                    checks.append(("完整性", {"type": "error", "msg": f"严格模式缺少{label}"}))
        self._add_check(checks, "CPU↔主板", self.check_cpu_motherboard(cpu, mb))
        mem_results = self.check_memory_motherboard(mem, mb)
        for r in mem_results:
            self._add_check(checks, "内存↔主板", r)
        self._add_check(checks, "内存插槽数", self.check_memory_slots(mem, mb), "未检查内存插槽数量")
        self._add_check(checks, "内存容量", self.check_memory_capacity(mem, mb), "未检查内存容量上限")
        for i, gpu in enumerate(gpus):
            self._add_check(checks, "显卡↔机箱", self.check_gpu_case(gpu, case, str(i+1) if len(gpus)>1 else ""))
        if not gpus:
            self._add_check(checks, "显卡↔机箱", {}, "未选择显卡，跳过显卡机箱限长检查")
        self._add_check(checks, "硬盘↔主板", self.check_storage_motherboard(storage, mb))
        self._add_check(checks, "SATA接口", self.check_sata_ports(storage, mb), "没有SATA设备或缺少SATA信息")
        self._add_check(checks, "电源功率", self.check_psu_power(psu, cpu, gpus))
        self._add_check(checks, "显卡供电", self.check_gpu_power_connector(gpus[0] if gpus else None, psu), "显卡未声明特殊供电需求")
        self._add_check(checks, "散热↔机箱", self.check_cooler_case(cooler, case))
        self._add_check(checks, "机箱↔主板", self.check_case_motherboard(case, mb))
        self._add_check(checks, "机箱↔电源", self.check_case_psu(case, psu), "未检查机箱电源尺寸")
        severity = {"error": 0, "warn": 0, "success": 0, "msg": 0, "skipped": 0}
        for _, r in checks:
            t = r.get("type", "")
            severity[t] = severity.get(t, 0) + 1
        if severity["error"] > 0:
            overall = "fail"
        elif severity["warn"] > 0:
            overall = "warn"
        else:
            overall = "pass"
        return {"overall": overall, "checks": checks, "severity": severity}


def load_components():
    """加载 components.yaml 和 cases.yaml。"""
    by_id = {}
    components_path = DATA / "components.yaml"
    if components_path.exists():
        with components_path.open("r", encoding="utf-8") as f:
            lib = yaml.safe_load(f)
        for section in ["cpus", "motherboards", "memory", "storage", "gpus", "coolers", "psus"]:
            for item in lib.get(section, []):
                by_id[item["id"]] = enrich_item(section, item)
    cases_path = DATA / "cases.yaml"
    if cases_path.exists():
        with cases_path.open("r", encoding="utf-8") as f:
            cases = yaml.safe_load(f)
        for item in cases.get("cases", []):
            by_id[item["id"]] = item
    return by_id


def main():
    parser = argparse.ArgumentParser(
        description="装机兼容性检查 — 11 项兼容性检查")
    parser.add_argument("--cpu", help="CPU ID")
    parser.add_argument("--mb", help="主板 ID")
    parser.add_argument("--mem", action="append", help="内存 ID (可多次指定)")
    parser.add_argument("--storage", action="append", help="硬盘 ID (可多次指定)")
    parser.add_argument("--gpu", action="append", help="显卡 ID (可多次指定)")
    parser.add_argument("--psu", help="电源 ID")
    parser.add_argument("--cooler", help="散热 ID")
    parser.add_argument("--case", help="机箱 ID")
    parser.add_argument("--strict", action="store_true", help="严格模式: 最终整机必须包含核心配件")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    by_id = load_components()
    missing_ids = []

    def get(id_str):
        if not id_str:
            return None
        item = by_id.get(id_str)
        if item is None:
            missing_ids.append(id_str)
        return item

    def get_list(id_list):
        items = []
        for id_str in id_list or []:
            item = get(id_str)
            if item is not None:
                items.append(item)
        return items

    build = {
        "cpu": get(args.cpu),
        "motherboard": get(args.mb),
        "memory": get_list(args.mem),
        "storage": get_list(args.storage),
        "gpu": get_list(args.gpu),
        "psu": get(args.psu),
        "cooler": get(args.cooler),
        "case": get(args.case),
    }

    checker = CompatibilityChecker()
    result = checker.check_all(build, strict=args.strict, missing_ids=missing_ids)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"兼容性检查结果: {result['overall'].upper()}")
        print(f"  错误: {result['severity']['error']}, "
              f"警告: {result['severity']['warn']}, "
              f"通过: {result['severity']['success']}, "
              f"跳过: {result['severity'].get('skipped', 0)}")
        print()
        for name, check in result["checks"]:
            if check.get("type"):
                icon = {"error": "❌", "warn": "⚠️", "success": "✅", "msg": "ℹ️", "skipped": "↷"}.get(check["type"], "  ")
                print(f"  {icon} {name}: {check['msg']}")


if __name__ == "__main__":
    main()
