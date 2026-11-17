#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
税务风险预警引擎（v4.4.0）
检测发票连号、大额整数、频繁开票、品名异常、进销项匹配等风险
输出三级预警：提示/关注/严重

v4.4.0 变化：
- 规则 YAML 化：从 references/risk_rules_config.yaml 读取，支持热加载
- 白名单机制：房租等天然整数金额可全局豁免或按规则豁免
- 规则开关：YAML 中可单独启停任一检测项
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from unified_invoice import UnifiedInvoice, RECEIPT_TYPES


# === 规则配置文件路径 ===
DEFAULT_RULES_PATH = Path(__file__).resolve().parent.parent / "references" / "risk_rules_config.yaml"


# === 零依赖 YAML 解析（PyYAML 不可用时降级） ===
def _scalar(text: str):
    """解析标量：内联列表 / 引号字符串 / 数字 / 布尔 / 空"""
    text = text.strip()
    # 去掉行尾注释（引号内的 # 不处理）
    if " #" in text and not (text.startswith('"') or text.startswith("'")):
        text = text.split(" #", 1)[0].strip()
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_scalar(x) for x in inner.split(",")]
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        return text[1:-1]
    low = text.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~", ""):
        return None
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


def _parse_block(lines: List[Tuple[int, str]], i: int, indent: int):
    """解析同一缩进层级的内容，返回 (值, 下一行索引)"""
    if i < len(lines) and lines[i][1].startswith("- "):
        result = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
            result.append(_scalar(lines[i][1][2:]))
            i += 1
        return result, i

    result: Dict[str, Any] = {}
    while i < len(lines) and lines[i][0] == indent:
        content = lines[i][1]
        if content.startswith("- "):
            break
        if ":" not in content:
            i += 1
            continue
        key, _, rest = content.partition(":")
        key = key.strip()
        i += 1
        if rest.strip():
            result[key] = _scalar(rest.strip())
        else:
            if i < len(lines) and lines[i][0] > indent:
                sub, i = _parse_block(lines, i, lines[i][0])
                result[key] = sub
            else:
                result[key] = {}
    return result, i


def mini_yaml_load(text: str) -> Dict[str, Any]:
    """极简 YAML 解析器：覆盖映射/列表/内联列表/标量，零第三方依赖"""
    lines: List[Tuple[int, str]] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append((len(raw) - len(raw.lstrip(" ")), stripped))
    value, _ = _parse_block(lines, 0, lines[0][0] if lines else 0)
    return value if isinstance(value, dict) else {}


def load_rules(path: Optional[str] = None) -> Dict[str, Any]:
    """
    读取规则配置：优先 PyYAML，缺失时降级到内置解析器
    """
    p = Path(path) if path else DEFAULT_RULES_PATH
    if not p.exists():
        return {}
    text = p.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except ImportError:
        return mini_yaml_load(text)
    except Exception:
        return mini_yaml_load(text)


def normalize_rules(raw: Dict[str, Any]) -> Dict[str, Any]:
    """把 YAML 的嵌套结构摊平成引擎可直接使用的配置项"""
    out: Dict[str, Any] = {}

    def _get(section: str, key: str, default=None):
        return (raw.get(section) or {}).get(key, default)

    out["consecutive_number_enabled"] = _get("consecutive_number_check", "enabled", True)
    out["consecutive_number_threshold"] = _get("consecutive_number_check", "threshold", 3)

    out["round_amount_enabled"] = _get("round_amount_check", "enabled", True)
    out["round_amount_threshold"] = _get("round_amount_check", "threshold", 10000)
    out["round_amount_min_digits"] = _get("round_amount_check", "min_digits", 5)

    out["frequent_invoicing_enabled"] = _get("frequent_invoicing_check", "enabled", True)
    out["frequent_invoicing_threshold"] = _get("frequent_invoicing_check", "threshold", 10)
    out["frequent_invoicing_days"] = _get("frequent_invoicing_check", "window_days", 30)

    out["scope_anomaly_enabled"] = _get("scope_anomaly_check", "enabled", True)
    out["scope_keywords"] = _get("scope_anomaly_check", "scope_keywords", {}) or {}
    out["anomaly_keywords_blacklist"] = _get("scope_anomaly_check", "anomaly_keywords_blacklist", []) or []

    out["input_output_match_enabled"] = _get("input_output_match_check", "enabled", True)
    out["input_output_similarity_threshold"] = _get(
        "input_output_match_check", "similarity_threshold", 0.1)

    out["whitelist"] = raw.get("whitelist") or {}
    out["anomaly_detection"] = raw.get("anomaly_detection") or {}
    out["certification"] = raw.get("certification") or {}
    return out


# === 风险检测默认配置 ===
DEFAULT_CONFIG = {
    # 规则开关
    "consecutive_number_enabled": True,
    "round_amount_enabled": True,
    "frequent_invoicing_enabled": True,
    "scope_anomaly_enabled": True,
    "input_output_match_enabled": True,
    # 规则阈值
    "consecutive_number_threshold": 3,       # 连号检测阈值：同一供应商连续 N 张
    "round_amount_threshold": 10000,         # 大额整数阈值：金额 >= 此值且为整数
    "round_amount_min_digits": 5,            # 大额整数最少位数
    "frequent_invoicing_threshold": 10,      # 频繁开票阈值：N 天内开具 M 张
    "frequent_invoicing_days": 30,           # 频繁开票时间窗口（天）
    "input_output_similarity_threshold": 0.1,
    # 关键词与白名单
    "scope_keywords": {},
    "anomaly_keywords_blacklist": [],
    "whitelist": {},
}


# === 三级预警定义 ===
RISK_LEVELS = {
    "提示": {"priority": 1, "color": "green", "action": "建议关注"},
    "关注": {"priority": 2, "color": "orange", "action": "建议核实"},
    "严重": {"priority": 3, "color": "red", "action": "建议立即处理"},
}


class RiskDetector:
    """
    税务风险预警引擎
    
    检测方法：
    1. 连号检测：同一供应商连续开具多张连号发票
    2. 整数金额检测：大额整数金额（如 100000.00）
    3. 频繁开票检测：短时间内同一供应商开具大量发票
    4. 品名异常检测：品名与经营范围不符
    5. 进销项匹配检测：进项品名与销项品名不匹配
    """
    
    def __init__(self, config: Optional[Dict] = None,
                 rules_path: Optional[str] = None, auto_reload: bool = True):
        """
        Args:
            config: 手工覆盖的配置项（优先级最高）
            rules_path: 规则 YAML 路径，默认 references/risk_rules_config.yaml
            auto_reload: 每次 detect_all 前检查文件 mtime，变化则自动热加载
        """
        self.rules_path = Path(rules_path) if rules_path else DEFAULT_RULES_PATH
        self.auto_reload = auto_reload
        self._rules_mtime: Optional[float] = None
        self.raw_rules: Dict[str, Any] = {}

        merged = dict(DEFAULT_CONFIG)
        merged.update(normalize_rules(self._read_rules()))
        merged.update(config or {})
        self.config = merged

        self.findings: List[Dict[str, Any]] = []
        self.invoices: List[UnifiedInvoice] = []
        self.input_invoices: List[UnifiedInvoice] = []
        self.output_invoices: List[UnifiedInvoice] = []

    # ---------- 规则热加载 ----------

    def _read_rules(self) -> Dict[str, Any]:
        """读取 YAML 并记录 mtime"""
        if self.rules_path.exists():
            try:
                self._rules_mtime = os.path.getmtime(self.rules_path)
            except OSError:
                self._rules_mtime = None
            self.raw_rules = load_rules(str(self.rules_path))
        else:
            self.raw_rules = {}
        return self.raw_rules

    def reload_if_changed(self) -> bool:
        """文件变化时重新加载规则，返回是否发生了重载"""
        if not self.auto_reload or not self.rules_path.exists():
            return False
        try:
            mtime = os.path.getmtime(self.rules_path)
        except OSError:
            return False
        if self._rules_mtime is not None and mtime == self._rules_mtime:
            return False
        new_cfg = normalize_rules(self._read_rules())
        self.config.update(new_cfg)
        return True

    def reload(self) -> bool:
        """强制重载规则"""
        self.config.update(normalize_rules(self._read_rules()))
        return True

    # ---------- 白名单 ----------

    def _is_whitelisted(self, inv: UnifiedInvoice, rule: Optional[str] = None) -> bool:
        """
        白名单判定

        优先级：全局关键词豁免 > 规则级豁免
        - whitelist.sellers：销售方名称含关键词 → 全部规则豁免
        - whitelist.categories：费用类型命中 → 全部规则豁免
        - whitelist.rules.<rule>：仅对该规则豁免
        """
        wl = self.config.get("whitelist") or {}
        if not wl:
            return False

        seller = inv.seller_name or ""
        category = inv.expense_category or ""

        for kw in wl.get("sellers") or []:
            if kw and kw in seller:
                return True
        for kw in wl.get("categories") or []:
            if kw and kw in category:
                return True

        if rule:
            for kw in (wl.get("rules") or {}).get(rule) or []:
                if kw and (kw in seller or kw in category or kw in (inv.raw_text or "")):
                    return True
        return False

    def _eligible(self, rule: str, invoices: Optional[List[UnifiedInvoice]] = None):
        """返回未命中白名单的票据"""
        src = invoices if invoices is not None else self.invoices
        return [inv for inv in src if not self._is_whitelisted(inv, rule)]

    def load_invoices(self, invoices: List[UnifiedInvoice]) -> 'RiskDetector':
        """加载进项发票列表"""
        self.invoices = invoices
        return self
    
    def load_input_invoices(self, invoices: List[UnifiedInvoice]) -> 'RiskDetector':
        """加载进项发票"""
        self.input_invoices = invoices
        return self
    
    def load_output_invoices(self, invoices: List[UnifiedInvoice]) -> 'RiskDetector':
        """加载销项发票"""
        self.output_invoices = invoices
        return self
    
    def detect_all(self) -> Dict[str, Any]:
        """
        运行所有风险检测
        
        Returns:
            dict: 包含所有检测结果和综合评估报告
        """
        self.findings = []

        # 规则热加载：文件被改动则自动生效
        reloaded = self.reload_if_changed()

        # 1. 连号检测
        if self.config.get("consecutive_number_enabled", True):
            self._detect_consecutive_numbers()

        # 2. 整数金额检测
        if self.config.get("round_amount_enabled", True):
            self._detect_round_amounts()

        # 3. 频繁开票检测
        if self.config.get("frequent_invoicing_enabled", True):
            self._detect_frequent_invoicing()

        # 4. 品名异常检测
        if self.config.get("scope_anomaly_enabled", True):
            self._detect_scope_anomaly()

        # 5. 进销项匹配检测
        if self.config.get("input_output_match_enabled", True):
            self._detect_input_output_match()

        # 生成综合报告
        report = self._generate_report()
        report["rules_path"] = str(self.rules_path)
        report["rules_reloaded"] = reloaded
        return report
    
    def _detect_consecutive_numbers(self):
        """连号检测：同一供应商连续开具多张连号发票"""
        # 按供应商分组（白名单票据不参与）
        supplier_invoices = defaultdict(list)
        for inv in self._eligible("consecutive_numbers"):
            if inv.seller_name:
                supplier_invoices[inv.seller_name].append(inv)
        
        threshold = self.config["consecutive_number_threshold"]
        
        for supplier, invs in supplier_invoices.items():
            # 按发票号码排序
            sorted_invs = sorted(invs, key=lambda x: x.invoice_number or "")
            
            # 检测连续号码
            consecutive_groups = []
            current_group = []
            
            for inv in sorted_invs:
                if not inv.invoice_number:
                    continue
                try:
                    num = int(inv.invoice_number)
                except (ValueError, TypeError):
                    continue
                
                if not current_group or num == int(current_group[-1].invoice_number or 0) + 1:
                    current_group.append(inv)
                else:
                    if len(current_group) >= threshold:
                        consecutive_groups.append(current_group)
                    current_group = [inv]
            
            if len(current_group) >= threshold:
                consecutive_groups.append(current_group)
            
            # 记录发现
            for group in consecutive_groups:
                numbers = [inv.invoice_number for inv in group]
                total_amount = sum(inv.total or 0 for inv in group)
                self.findings.append({
                    "type": "consecutive_numbers",
                    "level": "关注",
                    "supplier": supplier,
                    "description": f"检测到 {len(group)} 张连号发票：{numbers[0]} 至 {numbers[-1]}",
                    "details": {
                        "invoice_numbers": numbers,
                        "count": len(group),
                        "total_amount": total_amount,
                        "invoices": [inv.to_dict() for inv in group],
                    },
                    "suggestion": "建议核实是否存在拆分收入风险，确认业务真实性",
                })
    
    def _detect_round_amounts(self):
        """整数金额检测：大额整数金额"""
        threshold = self.config["round_amount_threshold"]
        min_digits = self.config["round_amount_min_digits"]
        
        for inv in self._eligible("round_amount"):
            if inv.total is None:
                continue
            
            # 检查是否为整数
            if inv.total != int(inv.total):
                continue
            
            # 检查是否达到阈值
            if inv.total >= threshold and len(str(int(inv.total))) >= min_digits:
                self.findings.append({
                    "type": "round_amount",
                    "level": "提示",
                    "invoice_number": inv.invoice_number,
                    "description": f"大额整数金额：{inv.total:.2f} 元",
                    "details": {
                        "amount": inv.total,
                        "invoice": inv.to_dict(),
                    },
                    "suggestion": "建议关注大额整数金额发票的业务真实性",
                })
    
    def _detect_frequent_invoicing(self):
        """频繁开票检测：短时间内同一供应商开具大量发票"""
        threshold = self.config["frequent_invoicing_threshold"]
        window_days = self.config["frequent_invoicing_days"]
        
        # 按供应商分组（白名单票据不参与）
        supplier_invoices = defaultdict(list)
        for inv in self._eligible("frequent_invoicing"):
            if inv.seller_name:
                supplier_invoices[inv.seller_name].append(inv)
        
        now = datetime.now()
        window_start = now - timedelta(days=window_days)
        
        for supplier, invs in supplier_invoices.items():
            # 筛选时间窗口内的发票
            recent_invs = []
            for inv in invs:
                try:
                    date_str = inv.billing_date or inv.travel_date
                    if date_str:
                        inv_date = datetime.strptime(date_str, '%Y-%m-%d')
                        if inv_date >= window_start:
                            recent_invs.append(inv)
                except (ValueError, TypeError):
                    continue
            
            if len(recent_invs) >= threshold:
                total_amount = sum(inv.total or 0 for inv in recent_invs)
                self.findings.append({
                    "type": "frequent_invoicing",
                    "level": "关注",
                    "supplier": supplier,
                    "description": f"近 {window_days} 天内开具 {len(recent_invs)} 张发票，合计 {total_amount:.2f} 元",
                    "details": {
                        "count": len(recent_invs),
                        "window_days": window_days,
                        "total_amount": total_amount,
                        "invoices": [inv.to_dict() for inv in recent_invs],
                    },
                    "suggestion": "建议核实是否存在虚开风险，确认业务真实性",
                })
    
    def _detect_scope_anomaly(self):
        """品名异常检测：品名与经营范围不符"""
        if not self.config.get("scope_anomaly_enabled"):
            return
        
        # 内置行业关键词表，YAML 的 scope_keywords 会扩充/覆盖
        SCOPE_KEYWORDS = {
            "餐饮": ["餐饮", "饭店", "酒楼", "餐厅", "食品", "小吃"],
            "技术服务": ["技术", "软件", "开发", "咨询", "顾问"],
            "建筑": ["建筑", "工程", "施工", "装修", "建材"],
            "零售": ["百货", "超市", "零售", "商店", "商贸"],
            "运输": ["运输", "物流", "快递", "货运", "客运"],
        }
        for scope, kws in (self.config.get("scope_keywords") or {}).items():
            if isinstance(kws, list):
                base = SCOPE_KEYWORDS.get(scope, [])
                SCOPE_KEYWORDS[scope] = list(dict.fromkeys(list(base) + list(kws)))

        # 品名关键词黑名单：命中即预警
        blacklist = self.config.get("anomaly_keywords_blacklist") or []

        # 行业与品名的错配规则（YAML 中 scope_keywords 用于扩充行业识别词）
        ANOMALY_RULES = [
            {"scope": "餐饮", "anomaly_keywords": ["技术服务", "软件开发", "建筑"]},
            {"scope": "建筑", "anomaly_keywords": ["餐饮", "零售百货"]},
            {"scope": "零售", "anomaly_keywords": ["建筑", "工程施工"]},
        ]

        for inv in self._eligible("scope_anomaly"):
            if not inv.seller_name or not inv.raw_text:
                continue

            for kw in blacklist:
                if kw and kw in (inv.raw_text or ""):
                    self.findings.append({
                        "type": "blacklist_keyword",
                        "level": "关注",
                        "seller_name": inv.seller_name,
                        "description": f"品名命中黑名单关键词「{kw}」",
                        "details": {"keyword": kw, "invoice": inv.to_dict()},
                        "suggestion": "建议核实品名与实际业务是否一致",
                    })
            
            # 推断供应商行业
            supplier_scope = None
            for scope, keywords in SCOPE_KEYWORDS.items():
                if any(kw in (inv.seller_name or "") for kw in keywords):
                    supplier_scope = scope
                    break
            
            if not supplier_scope:
                continue
            
            # 检查品名是否异常
            for rule in ANOMALY_RULES:
                if rule["scope"] == supplier_scope:
                    for anomaly_kw in rule["anomaly_keywords"]:
                        if anomaly_kw in (inv.raw_text or ""):
                            self.findings.append({
                                "type": "scope_anomaly",
                                "level": "关注",
                                "seller_name": inv.seller_name,
                                "description": f"供应商「{supplier_scope}」行业开具「{anomaly_kw}」品名发票",
                                "details": {
                                    "supplier_scope": supplier_scope,
                                    "anomaly_keyword": anomaly_kw,
                                    "invoice": inv.to_dict(),
                                },
                                "suggestion": "建议核实品名与实际业务是否一致",
                            })
    
    def _detect_input_output_match(self):
        """进销项匹配检测：进项品名与销项品名是否匹配"""
        if not self.config.get("input_output_match_enabled"):
            return
        
        # 简化的品名关键词提取
        def extract_keywords(text: str) -> set:
            """从文本提取关键词"""
            if not text:
                return set()
            # 简单分词（实际可用 jieba 等分词库）
            words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
            return set(words)
        
        # 收集进项品名词汇（白名单票据不参与）
        input_keywords = set()
        for inv in self._eligible("input_output_match", self.input_invoices):
            input_keywords.update(extract_keywords(inv.raw_text))
        
        # 收集销项品名词汇（白名单票据不参与）
        output_keywords = set()
        for inv in self._eligible("input_output_match", self.output_invoices):
            output_keywords.update(extract_keywords(inv.raw_text))
        
        # 计算匹配度（简单 Jaccard 系数）
        min_similarity = self.config.get("input_output_similarity_threshold", 0.1)
        if input_keywords and output_keywords:
            intersection = input_keywords & output_keywords
            union = input_keywords | output_keywords
            similarity = len(intersection) / len(union) if union else 0
            
            if similarity < min_similarity:  # 匹配度低于阈值
                self.findings.append({
                    "type": "input_output_mismatch",
                    "level": "严重",
                    "description": f"进销项品名匹配度过低（{similarity:.1%}）",
                    "details": {
                        "input_keywords": list(input_keywords)[:20],
                        "output_keywords": list(output_keywords)[:20],
                        "similarity": similarity,
                    },
                    "suggestion": "建议重点核实进销项业务一致性，防范虚开风险",
                })
    
    def _generate_report(self) -> Dict[str, Any]:
        """生成综合风险报告"""
        # 按预警级别分组
        findings_by_level = defaultdict(list)
        for finding in self.findings:
            findings_by_level[finding["level"]].append(finding)
        
        # 确定综合风险等级
        if findings_by_level.get("严重"):
            overall_level = "严重"
        elif findings_by_level.get("关注"):
            overall_level = "关注"
        elif findings_by_level.get("提示"):
            overall_level = "提示"
        else:
            overall_level = "无风险"
        
        return {
            "report_date": datetime.now().isoformat(),
            "total_invoices_checked": len(self.invoices),
            "total_findings": len(self.findings),
            "overall_risk_level": overall_level,
            "findings_by_level": {
                level: findings_by_level.get(level, [])
                for level in ["提示", "关注", "严重"]
            },
            "all_findings": self.findings,
            "config_used": self.config,
        }


def detect_risks(invoices: List[UnifiedInvoice], config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    便捷函数：检测发票风险
    
    Args:
        invoices: 发票列表
        config: 自定义检测配置（可选）
    
    Returns:
        dict: 风险检测报告
    """
    detector = RiskDetector(config)
    detector.load_invoices(invoices)
    return detector.detect_all()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python risk_detector.py <path_to_invoices_json>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        invoices = [UnifiedInvoice(**item) for item in data]
        report = detect_risks(invoices)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"检测失败: {e}", file=sys.stderr)
        sys.exit(1)
