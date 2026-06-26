# -*- coding: utf-8 -*-
"""
价格分析器
分析Excel数据，检测低价预警
"""

import os
import json
import datetime
import hashlib
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any

SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
DATA_DIR = SKILL_DIR / "data"


class PriceAnalyzer:
    def __init__(self):
        self.rules = self._load_rules()
        self._notified_cache: Dict[str, str] = {}
    
    def _load_rules(self) -> dict:
        rules_file = CONFIG_DIR / "rules.json"
        if rules_file.exists():
            with open(rules_file, 'r', encoding='utf-8') as f:
                return json.load(f) or {}
        return {"rules": []}
    
    def _save_rules(self):
        rules_file = CONFIG_DIR / "rules.json"
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)
    
    def get_rules(self) -> List[dict]:
        return self.rules.get("rules", [])
    
    def get_enabled_rules(self) -> List[dict]:
        return [r for r in self.get_rules() if r.get("enabled", True)]
    
    def add_rule(self, rule: dict) -> str:
        rule_id = f"rule_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        rule["id"] = rule_id
        rule["enabled"] = rule.get("enabled", True)
        
        if "rules" not in self.rules:
            self.rules["rules"] = []
        self.rules["rules"].append(rule)
        self._save_rules()
        return rule_id
    
    def update_rule(self, rule_id: str, updates: dict) -> bool:
        for rule in self.get_rules():
            if rule.get("id") == rule_id:
                rule.update(updates)
                self._save_rules()
                return True
        return False
    
    def delete_rule(self, rule_id: str) -> bool:
        self.rules["rules"] = [r for r in self.get_rules() if r.get("id") != rule_id]
        self._save_rules()
        return True
    
    def enable_rule(self, rule_id: str) -> bool:
        return self.update_rule(rule_id, {"enabled": True})
    
    def disable_rule(self, rule_id: str) -> bool:
        return self.update_rule(rule_id, {"enabled": False})
    
    def _parse_date(self, date_value) -> Optional[str]:
        if pd.isna(date_value):
            return None
        if isinstance(date_value, datetime.datetime):
            return date_value.strftime("%Y-%m-%d")
        if isinstance(date_value, datetime.date):
            return date_value.strftime("%Y-%m-%d")
        if isinstance(date_value, str):
            return date_value.split()[0] if ' ' in date_value else date_value
        return str(date_value)
    
    def _generate_alert_id(self, alert: dict) -> str:
        unique_str = f"{alert['pol']}-{alert['pod']}-{alert['carrier']}-{alert['box_type']}-{alert['etd']}"
        return hashlib.md5(unique_str.encode()).hexdigest()[:8]
    
    def _is_already_notified(self, alert_id: str) -> bool:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return self._notified_cache.get(alert_id) == today
    
    def _mark_as_notified(self, alert_id: str):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self._notified_cache[alert_id] = today
    
    def _check_valid_period(self, etd: str, valid_start: str, valid_end: str) -> bool:
        if not valid_start or not valid_end or not etd:
            return True
        try:
            etd_date = datetime.datetime.strptime(etd, "%Y-%m-%d")
            start_date = datetime.datetime.strptime(valid_start, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(valid_end, "%Y-%m-%d")
            return start_date <= etd_date <= end_date
        except:
            return True
    
    def analyze_excel(self, excel_path: str, rule: dict = None) -> List[dict]:
        if not excel_path or not os.path.exists(excel_path):
            return []
        
        try:
            df = pd.read_excel(excel_path)
        except Exception as e:
            print(f"读取Excel失败: {e}")
            return []
        
        alerts = []
        rules_to_check = [rule] if rule else self.get_enabled_rules()
        
        for r in rules_to_check:
            pol_list = [p.upper() for p in r.get("pol", [])]
            pod_list = [p.upper() for p in r.get("pod", [])]
            carrier_list = [c.upper() for c in r.get("carriers", [])]
            thresholds = r.get("thresholds", {})
            valid_period = r.get("valid_period", {})
            valid_start = valid_period.get("start")
            valid_end = valid_period.get("end")
            
            for _, row in df.iterrows():
                pol = str(row.get('POL', '')).strip().upper()
                pod = str(row.get('POD', '')).strip().upper()
                carrier = str(row.get('CARRIER', '')).strip().upper()
                etd = self._parse_date(row.get('ETD'))
                
                if pol_list and pol not in pol_list:
                    continue
                if pod_list and pod not in pod_list:
                    continue
                if carrier_list and carrier not in carrier_list:
                    continue
                
                if not self._check_valid_period(etd, valid_start, valid_end):
                    continue
                
                price_checks = [
                    ('20GP', row.get('20GP'), thresholds.get('20GP')),
                    ('40GP', row.get('40GP'), thresholds.get('40GP')),
                    ('40HQ', row.get('40HQ'), thresholds.get('40HQ'))
                ]
                
                for box_type, price, threshold in price_checks:
                    if threshold and pd.notna(price) and int(price) > 0 and int(price) < threshold:
                        alert = {
                            "rule_id": r.get("id"),
                            "rule_name": r.get("name", ""),
                            "pol": row.get('POL'),
                            "pod": row.get('POD'),
                            "carrier": row.get('CARRIER'),
                            "box_type": box_type,
                            "price": int(price),
                            "threshold": threshold,
                            "etd": etd
                        }
                        alert["alert_id"] = self._generate_alert_id(alert)
                        
                        if not self._is_already_notified(alert["alert_id"]):
                            alerts.append(alert)
                            self._mark_as_notified(alert["alert_id"])
        
        return alerts
    
    def analyze_all_rules(self, excel_path: str) -> List[dict]:
        return self.analyze_excel(excel_path)
    
    def get_rule_summary(self) -> List[dict]:
        return [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "enabled": r.get("enabled", True),
                "pol_count": len(r.get("pol", [])),
                "pod_count": len(r.get("pod", [])),
                "carriers": r.get("carriers", []),
                "thresholds": r.get("thresholds", {})
            }
            for r in self.get_rules()
        ]
