import re
from typing import List, Optional, Tuple
from core.types import ParsedIntent, ActionType, ElementType


class CommandParser:
    def __init__(self):
        self.action_aliases = {
            "点击": ActionType.CLICK,
            "点一下": ActionType.CLICK,
            "点": ActionType.CLICK,
            "单击": ActionType.CLICK,
            "双击": ActionType.CLICK,
            "输入": ActionType.TYPE,
            "填写": ActionType.TYPE,
            "键入": ActionType.TYPE,
            "粘贴": ActionType.TYPE,
            "访问": ActionType.NAVIGATE,
            "进入": ActionType.NAVIGATE,
            "导航到": ActionType.NAVIGATE,
            "前往": ActionType.NAVIGATE,
            "去": ActionType.NAVIGATE,
            "打开网页": ActionType.NAVIGATE,
            "打开网站": ActionType.NAVIGATE,
            "打开浏览器": ActionType.NAVIGATE,
            "截图": ActionType.SCREENSHOT,
            "截屏": ActionType.SCREENSHOT,
            "等待": ActionType.WAIT,
            "滚动": ActionType.SCROLL,
            "滚一下": ActionType.SCROLL,
            "向下滚": ActionType.SCROLL,
            "向上滚": ActionType.SCROLL,
        }
        self.position_keywords = ["左上", "右上", "左下", "右下", "中间", "顶部", "底部", "右侧", "左侧"]
        self.input_aliases = ["输入框", "搜索框", "文本框", "对话框", "聊天框", "消息框"]
        self.button_aliases = ["按钮", "发送", "确认", "提交", "搜索", "登录", "下一步", "确定"]
        self.leading_noise = ["请", "帮我", "请帮我", "麻烦", "一下", "先", "再", "然后", "接着"]
        self.browser_aliases = {
            "谷歌浏览器": "chrome",
            "chrome浏览器": "chrome",
            "谷歌": "chrome",
            "google chrome": "chrome",
            "谷歌chrome": "chrome",
            "火狐浏览器": "firefox",
            "firefox浏览器": "firefox",
            "火狐": "firefox",
            "微软浏览器": "edge",
            "edge浏览器": "edge",
        }

    def parse(self, command: str) -> ParsedIntent:
        normalized = self._normalize(command)
        parts = self._split_compound(normalized)
        if len(parts) > 1:
            children = [self._parse_single(p) for p in parts if p.strip()]
            confidence = sum(c.confidence for c in children) / max(len(children), 1)
            return ParsedIntent(action=ActionType.COMPOUND, raw_command=command, children=children, confidence=confidence)
        return self._parse_single(normalized)

    def _normalize(self, text: str) -> str:
        text = text.strip()
        replacements = {
            "，": ",", "。": ".", "：": ":", "；": ";",
            "“": '"', "”": '"', "‘": "'", "’": "'",
            "一下": "一下", "帮我": "", "请帮我": "", "麻烦": "",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"\s+", " ", text)
        text = self._rewrite_natural_command(text.strip())
        return text.strip()

    def _rewrite_natural_command(self, text: str) -> str:
        text = self._rewrite_browser_aliases(text)
        text = self._rewrite_open_browser(text)
        text = self._rewrite_search_command(text)
        text = self._rewrite_navigation_phrase(text)
        return text

    def _rewrite_open_browser(self, text: str) -> str:
        text = re.sub(r"^打开浏览器[，,\s]*$", "打开chrome", text)
        text = re.sub(r"^启动浏览器[，,\s]*$", "启动chrome", text)
        text = re.sub(r"^运行浏览器[，,\s]*$", "运行chrome", text)
        text = re.sub(r"^打开浏览器[，,\s]*(?:然后|并且|并|再)?[，,\s]*(在搜索框输入.+)$", r"打开chrome,然后\1", text)
        return text

    def _rewrite_browser_aliases(self, text: str) -> str:
        for src, dst in sorted(self.browser_aliases.items(), key=lambda item: len(item[0]), reverse=True):
            text = text.replace(src, dst)
        return text

    def _rewrite_search_command(self, text: str) -> str:
        patterns = [
            r"^(?:帮我)?搜索\s*['\"]?(.+?)['\"]?$",
            r"^(?:帮我)?搜一下\s*['\"]?(.+?)['\"]?$",
            r"^(?:帮我)?搜\s*['\"]?(.+?)['\"]?$",
            r"^(.*?)(?:然后|接着|并且|并|再|,)\s*(?:帮我)?搜索\s*['\"]?(.+?)['\"]?$",
            r"^(.*?)(?:然后|接着|并且|并|再|,)\s*(?:帮我)?搜一下\s*['\"]?(.+?)['\"]?$",
            r"^(.*?)(?:然后|接着|并且|并|再|,)\s*(?:帮我)?搜\s*['\"]?(.+?)['\"]?$",
        ]
        for pattern in patterns:
            m = re.search(pattern, text)
            if not m:
                continue
            if len(m.groups()) == 1:
                prefix = ""
                query = m.group(1)
            else:
                prefix = m.group(1).rstrip(" ,")
                query = m.group(2)
            query = query.strip(" ' \"，,.。")
            if not query:
                continue
            rewritten = f"在搜索框输入'{query}'"
            return f"{prefix}，然后{rewritten}" if prefix else rewritten
        return text

    def _rewrite_navigation_phrase(self, text: str) -> str:
        text = re.sub(r"\b(?:进入|去|前往)(?=(?:localhost|[\w-]+(?:\.[\w-]+)+)(?::\d+)?(?:/[^\s'\"]*)?)", "访问", text)
        text = re.sub(r"\b打开\s*((?:localhost|[\w-]+(?:\.[\w-]+)+)(?::\d+)?(?:/[^\s'\"]*)?)", r"访问 \1", text)
        return text

    def _split_compound(self, text: str) -> List[str]:
        protected = []

        def _hold(match):
            protected.append(match.group(0))
            return f"__Q{len(protected)-1}__"

        masked = re.sub(r"['\"].+?['\"]", _hold, text)
        parts = [p.strip() for p in re.split(r"(?:然后|接着|并且|并|再|,|，|;|；)", masked) if p.strip()]
        restored = []
        for part in parts:
            for idx, raw in enumerate(protected):
                part = part.replace(f"__Q{idx}__", raw)
            restored.append(part)
        return restored

    def _parse_single(self, text: str) -> ParsedIntent:
        url = self._extract_url(text)
        quoted = re.findall(r"['\"](.+?)['\"]", text)
        input_text = quoted[0] if quoted else self._extract_unquoted_input(text)
        action = self._detect_action(text, has_url=url is not None, has_input=input_text is not None)
        target_text, target_type = self._extract_target(text, action)
        position_hint = next((k for k in self.position_keywords if k in text), None)

        confidence = 0.30
        if action != ActionType.UNKNOWN:
            confidence += 0.28
        if url:
            confidence += 0.22
        if input_text:
            confidence += 0.18
        if target_text:
            confidence += 0.12
        if position_hint:
            confidence += 0.08

        return ParsedIntent(
            action=action,
            raw_command=text,
            target_text=target_text,
            target_type=target_type,
            input_text=input_text,
            url=url,
            app_name=self._extract_app_name(text),
            position_hint=position_hint,
            confidence=min(confidence, 0.99),
        )

    def _extract_url(self, text: str) -> Optional[str]:
        cleaned = re.sub(r"^(?:访问|进入|前往|去|打开网页|打开网站|打开浏览器)\s*", "", text.strip())
        patterns = [
            r"((?:https?|file)://[^\s'\"]+)",
            r"\b(about:[^\s'\"]+)\b",
            r"\b((?:[a-zA-Z]:\\[^\s'\"]+)|(?:[a-zA-Z]:/[^\s'\"]+))\b",
            r"\b((?:localhost|[\w-]+(?:\.[\w-]+)+)(?::\d+)?(?:/[^\s'\"]*)?)\b",
        ]
        for pattern in patterns:
            m = re.search(pattern, cleaned)
            if m:
                url = m.group(1)
                if re.match(r"^(localhost|[\w-]+(?:\.[\w-]+)+)(?::\d+)?(?:/.*)?$", url) and not re.match(r"^(?:https?|file|about):", url):
                    return "https://" + url
                return url
        return None

    def _extract_unquoted_input(self, text: str) -> Optional[str]:
        m = re.search(r"(?:输入|填写|键入|粘贴)\s+(.+)$", text)
        if not m:
            return None
        candidate = m.group(1).strip()
        for suffix in ["按钮", "输入框", "搜索框", "文本框"]:
            if candidate.endswith(suffix):
                return None
        return candidate

    def _detect_action(self, text: str, has_url: bool, has_input: bool) -> ActionType:
        stripped = text.strip(" ，,")
        if stripped in {"打开浏览器", "启动浏览器", "运行浏览器", "打开chrome", "启动chrome", "运行chrome"}:
            return ActionType.OPEN_APP
        if (stripped.startswith("打开浏览器") or stripped.startswith("启动浏览器") or stripped.startswith("运行浏览器")) and not has_url:
            return ActionType.OPEN_APP

        if has_url and any(k in text for k in ["访问", "进入", "打开网页", "打开网站", "打开浏览器", "导航", "前往", "去"]):
            return ActionType.NAVIGATE
        if has_input and any(k in text for k in ["输入", "填写", "键入", "粘贴"]):
            return ActionType.TYPE
        if has_url:
            return ActionType.NAVIGATE
        for alias, action in self.action_aliases.items():
            if alias in text:
                return action
        if (stripped.startswith("打开") or stripped.startswith("启动") or stripped.startswith("运行")) and "网站" not in stripped and "网页" not in stripped:
            return ActionType.OPEN_APP
        return ActionType.UNKNOWN

    def _extract_target(self, text: str, action: ActionType) -> Tuple[Optional[str], Optional[ElementType]]:
        if action == ActionType.TYPE:
            for alias in self.input_aliases:
                patterns = [
                    rf"在(.+?){alias}(?:中|里)?(?:输入|填写|键入|粘贴)",
                    rf"到(.+?){alias}(?:中|里)?(?:输入|填写|键入|粘贴)",
                    rf"(.+?){alias}(?:中|里)?(?:输入|填写|键入|粘贴)",
                ]
                for pattern in patterns:
                    m = re.search(pattern, text)
                    if m:
                        cleaned = self._clean_target_text(m.group(1))
                        if cleaned:
                            return cleaned, ElementType.INPUT
                if alias in text:
                    return alias.replace("框", ""), ElementType.INPUT
            return None, ElementType.INPUT

        click_patterns = [
            (r"点击(.+?)(按钮|输入框|复选框|链接)", True),
            (r"点一下(.+?)(按钮|输入框|复选框|链接)", True),
            (r"点击(.+)$", False),
            (r"点一下(.+)$", False),
            (r"单击(.+)$", False),
        ]
        for pattern, typed in click_patterns:
            m = re.search(pattern, text)
            if m:
                label = self._clean_target_text(m.group(1))
                suffix = m.group(2).strip() if typed else ""
                if label in self.button_aliases and not suffix:
                    suffix = "按钮"
                return label, self._map_element_type(suffix or label)

        if action == ActionType.CLICK:
            return None, ElementType.BUTTON
        return None, None

    def _clean_target_text(self, text: str) -> str:
        text = text.strip()
        for noise in ["一下", "这个", "那个", "右下角", "左上角", "中间", "右侧", "左侧", "里面", "里", "中"]:
            text = text.replace(noise, "")
        for prefix in self.leading_noise:
            if text.startswith(prefix):
                text = text[len(prefix):]
        text = re.sub(r"^(在|到)+", "", text)
        return text.strip(" ：:，,。.")

    def _map_element_type(self, token: str) -> ElementType:
        mapping = {
            "按钮": ElementType.BUTTON,
            "发送": ElementType.BUTTON,
            "确认": ElementType.BUTTON,
            "提交": ElementType.BUTTON,
            "搜索": ElementType.BUTTON,
            "登录": ElementType.BUTTON,
            "输入框": ElementType.INPUT,
            "搜索框": ElementType.INPUT,
            "文本框": ElementType.INPUT,
            "复选框": ElementType.CHECKBOX,
            "链接": ElementType.LINK,
        }
        return mapping.get(token, ElementType.UNKNOWN)

    def _extract_app_name(self, text: str):
        m = re.search(r"(?:打开|启动|运行)\s*(.+)$", text)
        if m and not self._extract_url(text) and "网站" not in text and "网页" not in text:
            return m.group(1).strip()
        return None
