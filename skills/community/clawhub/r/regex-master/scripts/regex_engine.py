"""
Regex Master - 正则表达式一站式工具引擎
"""
import re
from typing import List, Dict, Any, Optional, Union


class RegexMaster:
    """正则表达式生成、测试、解释与提取工具"""

    # 常用正则模板库
    TEMPLATES = {
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "phone_cn": r"^1[3-9]\d{9}$",
        "idcard": r"^[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]$",
        "url": r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
        "ipv4": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        "date_iso": r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$",
        "chinese_chars": r"[\u4e00-\u9fa5]+",
        "hex_color": r"^#(?:[0-9a-fA-F]{3}){1,2}$",
        "credit_card": r"^\d{13,19}$",
        "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
    }

    # 自然语言 -> 正则 映射表
    NL_PATTERNS = {
        "提取中国大陆手机号": r"1[3-9]\d{9}",
        "匹配邮箱地址": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "匹配 IPv4 地址": r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
        "匹配中文字符": r"[\u4e00-\u9fa5]",
        "匹配 URL 链接": r"https?://[^\s]+",
        "匹配日期 YYYY-MM-DD": r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])",
        "提取数字": r"\d+",
        "匹配身份证号": r"[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
    }

    def test(self, pattern: str, text: str, flags: int = 0) -> Dict[str, Any]:
        """测试正则表达式是否匹配目标文本"""
        try:
            compiled = re.compile(pattern, flags)
            match = compiled.match(text)
            if match:
                return {
                    "match": True,
                    "full_match": match.group(0) == text,
                    "groups": list(match.groups()) if match.groups() else [],
                    "groupdict": match.groupdict(),
                    "span": match.span(),
                }
            return {"match": False, "reason": "no match"}
        except re.error as e:
            return {"match": False, "reason": f"invalid pattern: {e}"}

    def explain(self, pattern: str) -> str:
        """将正则表达式翻译成人类可读的说明"""
        explanations = []

        # 分段解释常见模式
        mapping = {
            r"^": "字符串开头",
            r"$": "字符串结尾",
            r"\d+": "一个或多个数字",
            r"\d{3}": "恰好3位数字",
            r"\d{4}": "恰好4位数字",
            r"\d{8,}": "至少8位数字",
            r"\.": "一个点号",
            r"[A-Za-z0-9._%+-]+": "字母/数字/特殊字符组合",
            r"[a-zA-Z]+": "一个或多个英文字母",
            r"[\u4e00-\u9fa5]+": "一个或多个中文字符",
            r"(?=.*[A-Z])": "必须包含至少一个大写字母",
            r"(?=.*[a-z])": "必须包含至少一个小写字母",
            r"(?=.*\d)": "必须包含至少一个数字",
            r"(?=.*[!@#$%^&*])": "必须包含至少一个特殊符号",
            r".{8,}": "至少8个任意字符",
            r".{6,20}": "6到20个任意字符",
        }

        desc = pattern
        for pat, exp in mapping.items():
            if pat in pattern:
                explanations.append(exp)

        if not explanations:
            # 通用解释
            if pattern.startswith("^") and pattern.endswith("$"):
                return f"完整字符串匹配模式: 要求整个文本符合 '{pattern[1:-1]}' 的规则"
            return f"模式 '{pattern}' 的文本匹配规则"

        return "、".join(explanations)

    def generate(self, description: str) -> str:
        """根据自然语言描述生成正则表达式"""
        # 先匹配已知映射
        for key, pat in self.NL_PATTERNS.items():
            if key in description or description in key:
                return pat

        # 智能推断
        if "手机" in description or "电话" in description:
            return r"1[3-9]\d{9}"
        if "邮箱" in description or "email" in description.lower():
            return r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        if "url" in description.lower() or "链接" in description:
            return r"https?://[^\s]+"
        if "身份证" in description:
            return r"[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]"
        if "中文" in description:
            return r"[\u4e00-\u9fa5]+"
        if "数字" in description:
            return r"\d+"
        if "ipv4" in description.lower() or "ip 地址" in description:
            return r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"

        return r".*"  # 默认通配

    def extract_all(self, pattern: str, text: str, flags: int = 0) -> List[str]:
        """从文本中提取所有匹配项"""
        try:
            compiled = re.compile(pattern, flags)
            return compiled.findall(text)
        except re.error:
            return []

    def get_template(self, name: str) -> Optional[str]:
        """获取内置正则模板"""
        return self.TEMPLATES.get(name)

    def list_templates(self) -> Dict[str, str]:
        """列出所有可用模板"""
        return dict(self.TEMPLATES)

    def validate_pattern(self, pattern: str) -> Dict[str, Any]:
        """验证正则表达式语法是否合法"""
        try:
            re.compile(pattern)
            return {"valid": True, "message": "pattern is valid"}
        except re.error as e:
            return {"valid": False, "message": str(e), "position": e.pos if hasattr(e, "pos") else None}

    def replace(self, pattern: str, text: str, replacement: str, flags: int = 0) -> str:
        """使用正则替换文本"""
        try:
            return re.sub(pattern, replacement, text, flags=flags)
        except re.error:
            return text
