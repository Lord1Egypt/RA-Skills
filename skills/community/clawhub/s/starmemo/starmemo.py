#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 记忆优化技能 - 国内全LLM通用版
支持：火山方舟/通义千问/文心一言/DeepSeek/智谱AI/讯飞星火/腾讯混元
纯REST API调用 | 自动分层存储 | Token极致压缩 | 对话一键配置
"""
import os
import json
import hashlib
import sys
import re
from datetime import datetime

# 全局自动保存：无场景区分，所有平台（飞书/QQ/主程序/CLI）全部自动保存
def on_user_input(ctx, user_input):
    # 读取配置
    config = ctx.get("config", {})
    # 全局统一规则：只要开启了save，就自动保存（无任何场景例外）
    if config.get("save", True):
        # 执行记忆保存（原有分层存储/压缩逻辑不变）
        save_to_memory(ctx, user_input)
    
    # 原有业务逻辑：检索记忆+生成回答（不变）
    return process_query(ctx, user_input)

# 封装统一的保存逻辑（全场景通用）
def save_to_memory(ctx, content):
    """所有平台通用的记忆保存，无场景限制"""
    import os
    from datetime import date
    # 原有分层存储代码不变
    data_dir = "memory_data/daily"
    os.makedirs(data_dir, exist_ok=True)
    file_path = f"{data_dir}/{date.today()}.md"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"- {content}\n")

# 自动安装唯一依赖
def auto_install():
    try:
        import requests
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "requests"])
auto_install()
import requests

# 国内主流LLM预设配置
LLM_PRESET = {
    "huoshan": {"url": "https://ark.cn-beijing.volces.com/api/v3", "model": "doubao-seed-code-preview-251028"},
    "tongyi": {"url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model": "qwen-turbo"},
    "wenxin": {"url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat", "model": "ernie-lite-8k"},
    "deepseek": {"url": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
    "zhipu": {"url": "https://open.bigmodel.cn/api/paas/v4", "model": "glm-4-flash"},
    "xinghuo": {"url": "https://spark-api-open.xf-yun.com/v1", "model": "generalv3.5"},
    "hunyuan": {"url": "https://hunyuan.tencentcloudapi.com/v1", "model": "hunyuan-lite"}
}

# 配置管理
class SkillConfig:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, ".skill_config")
        
        self.api_key = ""
        self.base_url = LLM_PRESET["huoshan"]["url"]
        self.model_name = LLM_PRESET["huoshan"]["model"]
        self.enable_ai = False
        self.save_flags = {"openclaw_main": True, "cli": True, "feishu_direct": True, "feishu_manual": True}
        self.persist_key = False
        self.allow_web_fetch = False
        
        # 记忆优化参数
        self.max_len = 200
        self.retrieve_limit = 1
        self.archive_days = 3
        # LLM运行参数
        self.chat_temperature = 0.2
        self.optimize_temperature = 0.1
        self.chat_tokens = 192
        self.optimize_tokens = 128
        self.clarify_tokens = 96
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.api_key = data.get("api_key", "")
                self.base_url = data.get("base_url", self.base_url)
                self.model_name = data.get("model_name", self.model_name)
                self.enable_ai = data.get("enable_ai", self.enable_ai)
                sc = data.get("save_config", {})
                if isinstance(sc, dict):
                    for k in self.save_flags:
                        v = sc.get(k)
                        if isinstance(v, bool):
                            self.save_flags[k] = v
                        elif isinstance(v, str):
                            self.save_flags[k] = v.lower() == "true"
                pk = data.get("persist_key", self.persist_key)
                self.persist_key = isinstance(pk, bool) and pk
                awf = data.get("allow_web_fetch", self.allow_web_fetch)
                self.allow_web_fetch = isinstance(awf, bool) and awf
                self.max_len = int(data.get("max_len", self.max_len))
                self.retrieve_limit = int(data.get("retrieve_limit", self.retrieve_limit))
                self.archive_days = int(data.get("archive_days", self.archive_days))
                self.chat_temperature = float(data.get("chat_temperature", self.chat_temperature))
                self.optimize_temperature = float(data.get("optimize_temperature", self.optimize_temperature))
                self.chat_tokens = int(data.get("chat_tokens", self.chat_tokens))
                self.optimize_tokens = int(data.get("optimize_tokens", self.optimize_tokens))
                self.clarify_tokens = int(data.get("clarify_tokens", self.clarify_tokens))
            except:
                pass

    def save_config(self):
        try:
            data = {
                "api_key": self.api_key if self.persist_key else "",
                "base_url": self.base_url,
                "model_name": self.model_name,
                "enable_ai": self.enable_ai,
                "max_len": self.max_len,
                "retrieve_limit": self.retrieve_limit,
                "archive_days": self.archive_days,
                "chat_temperature": self.chat_temperature,
                "optimize_temperature": self.optimize_temperature,
                "chat_tokens": self.chat_tokens,
                "optimize_tokens": self.optimize_tokens,
                "clarify_tokens": self.clarify_tokens,
                "save_config": self.save_flags,
                "persist_key": self.persist_key,
                "allow_web_fetch": self.allow_web_fetch
            }
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            os.chmod(self.config_path, 0o600)
        except:
            pass

# LLM API客户端
class LLMClient:
    def __init__(self, config):
        self.config = config
        self.api = f"{config.base_url.rstrip('/')}/chat/completions"

    def optimize(self, text):
        if not self.config.enable_ai or not self.config.api_key:
            return text[:self.config.max_len]
        text = text[:300]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        data = {
            "model": self.config.model_name,
            "messages": [{"role": "user", "content": f"精简总结，保留核心，≤200字：{text}"}],
            "temperature": self.config.optimize_temperature,
            "max_tokens": self.config.optimize_tokens
        }
        try:
            res = requests.post(self.api, headers=headers, json=data, timeout=10)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()[:self.config.max_len]
        except:
            return text[:self.config.max_len]

    def chat(self, user_input, context=""):
        if not self.config.enable_ai or not self.config.api_key:
            return (context or user_input)[:self.config.max_len]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        prompt_user = user_input[:1000]
        ctx = context[:self.config.max_len]
        messages = [
            {"role": "system", "content": "你是记忆助手。仅基于提供的短记忆与用户输入作答，尽量不引入长上下文，保持简洁，不超过200字。"},
            {"role": "user", "content": f"短记忆：{ctx}\n用户输入：{prompt_user}"}
        ]
        data = {
            "model": self.config.model_name,
            "messages": messages,
            "temperature": self.chat_temperature,
            "max_tokens": self.config.chat_tokens
        }
        try:
            res = requests.post(self.api, headers=headers, json=data, timeout=10)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
        except:
            return (ctx or prompt_user)[:self.config.max_len]

    def clarify(self, user_input, context=""):
        if not self.config.enable_ai or not self.config.api_key:
            return "为更精准回答，请补充语言/框架、目标、约束。"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        messages = [
            {"role": "system", "content": "当短记忆不足以回答时，请用1-2个问题澄清需求（语言/框架、具体目标、约束），语气自然，≤80字。"},
            {"role": "user", "content": f"短记忆（可能不准）：{context[:self.config.max_len]}\n用户输入：{user_input[:500]}"}
        ]
        data = {"model": self.config.model_name, "messages": messages, "temperature": self.config.chat_temperature, "max_tokens": self.config.clarify_tokens}
        try:
            res = requests.post(self.api, headers=headers, json=data, timeout=10)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
        except:
            return "为更精准回答，请补充语言/框架、目标、约束。"

# 分层记忆存储
class MemoryStorage:
    def __init__(self, base_dir, limit=2, archive_days=3):
        self.root = os.path.join(base_dir, "memory_data")
        self.daily = os.path.join(self.root, "daily")
        self.recent = os.path.join(self.root, "recent")
        self.archive = os.path.join(self.root, "archive")
        self.limit = int(limit)
        self.archive_days = int(archive_days)
        self.hash_set = set()
        self.init_dirs()

    def init_dirs(self):
        for d in [self.root, self.daily, self.recent, self.archive]:
            os.makedirs(d, exist_ok=True)

    def today_file(self):
        return os.path.join(self.daily, f"{datetime.now().strftime('%Y-%m-%d')}.md")

    def rotate(self):
        today = datetime.now().strftime("%Y-%m-%d")
        for f in os.listdir(self.daily):
            if not f.endswith(".md"): continue
            try:
                day = f.replace(".md", "")
                delta = (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(day, "%Y-%m-%d")).days
                src = os.path.join(self.daily, f)
                if 1 <= delta < self.archive_days:
                    os.rename(src, os.path.join(self.recent, f))
                elif delta >= self.archive_days:
                    with open(src, "r", encoding="utf-8") as f_in:
                        lines = [l.strip() for l in f_in if ("原文：" in l) or ("优化：" in l)]
                    with open(os.path.join(self.archive, f), "w", encoding="utf-8") as f_out:
                        f_out.write("\n".join(lines))
                    os.remove(src)
            except:
                continue

    def save(self, content, optimized):
        content = content.strip()
        if not content: return
        h = hashlib.md5(content.encode()).hexdigest()
        if h in self.hash_set: return
        self.hash_set.add(h)
        ts = datetime.now().strftime("%H:%M")
        with open(self.today_file(), "a", encoding="utf-8") as f:
            f.write(f"[{ts}] 原文：{content[:100]}...\n[{ts}] 优化：{optimized}\n\n")
        self.rotate()

    def search(self, keyword):
        res = []
        def scan(path):
            if not os.path.exists(path): return ""
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if keyword in line and len(res) < self.limit:
                        return line.strip()
            return ""
        r = scan(self.today_file())
        if r: res.append(r)
        if len(res) < self.limit:
            for f in os.listdir(self.recent):
                r = scan(os.path.join(self.recent, f))
                if r: res.append(r)
                if len(res) >= self.limit: break
        if len(res) < self.limit:
            for f in os.listdir(self.archive):
                r = scan(os.path.join(self.archive, f))
                if r: res.append(r)
                if len(res) >= self.limit: break
        return "\n".join(res)

# 消息文本清洗（多平台兼容）
class MessageCleaner:
    @staticmethod
    def clean(text):
        if not isinstance(text, str):
            return ""
        text = re.sub(r"<at.*?>.*?</at>", " ", text)
        text = re.sub(r"\[CQ:.*?\]", " ", text)
        text = re.sub(r"@\S+", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

# 技能主类
class StarMemoSkill:
    def __init__(self):
        self.config = SkillConfig()
        self.llm = LLMClient(self.config)
        self.storage = MemoryStorage(self.config.base_dir, self.config.retrieve_limit, self.config.archive_days)
        self.pending = None

    def _web_fetch(self, query):
        if not self.config.allow_web_fetch:
            return ""
        try:
            url = "https://r.jina.ai/http://duckduckgo.com/?q=" + requests.utils.quote(query)
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                return r.text.strip()[:2000]
        except:
            pass
        return ""

    def handle_message(self, user_input):
        try:
            if isinstance(user_input, dict):
                msg = ""
                for key in ["text", "content", "message", "msg"]:
                    if isinstance(user_input.get(key), str):
                        msg = user_input[key]
                        break
            else:
                msg = str(user_input)

            msg = MessageCleaner.clean(msg)
            allow_save = self.config.save_flags.get("openclaw_main", True)

            if msg and not msg.startswith("记忆配置") and allow_save:
                core = self.llm.optimize(msg)
                self.storage.save(msg, core)

            if msg.startswith("记忆配置"):
                try:
                    params = {}
                    for p in msg.replace("记忆配置", "").split():
                        if "=" in p:
                            k, v = p.split("=", 1)
                            params[k.strip()] = v.strip()

                    llm = params.get("llm", "")
                    if llm in LLM_PRESET:
                        self.config.base_url = LLM_PRESET[llm]["url"]
                        self.config.model_name = LLM_PRESET[llm]["model"]

                    self.config.api_key = params.get("key", self.config.api_key)
                    self.config.enable_ai = params.get("ai", "true").lower() == "true"
                    self.config.persist_key = params.get("persist_key", "false").lower() == "true"
                    self.config.allow_web_fetch = params.get("web", "false").lower() == "true"

                    sc_pairs = [
                        ("save_main","openclaw_main"),
                        ("save_cli","cli"),
                        ("save_feishu","feishu_direct"),
                        ("save_feishu_manual","feishu_manual")
                    ]
                    for ext_key, conf_key in sc_pairs:
                        v = params.get(ext_key)
                        if v is not None:
                            self.config.save_flags[conf_key] = str(v).lower() == "true"

                    self.config.retrieve_limit = int(params.get("retrieve", self.config.retrieve_limit))
                    self.config.max_len = int(params.get("max_len", self.config.max_len))
                    self.config.archive_days = int(params.get("archive", self.config.archive_days))
                    self.config.chat_tokens = int(params.get("chat_tokens", self.config.chat_tokens))
                    self.config.optimize_tokens = int(params.get("opt_tokens", self.config.optimize_tokens))
                    self.config.clarify_tokens = int(params.get("clar_tokens", self.config.clarify_tokens))
                    self.config.chat_temperature = float(params.get("temp_chat", self.config.chat_temperature))
                    self.config.optimize_temperature = float(params.get("temp_opt", self.config.optimize_temperature))

                    self.config.save_config()
                    self.llm = LLMClient(self.config)
                    return "✅ 记忆技能配置生效！"
                except:
                    return "❌ 配置格式：记忆配置 llm=huoshan key=xxx"

            if self.pending is not None:
                query = f"{self.pending['msg']} {msg}"
                web_text = self._web_fetch(query)
                if web_text:
                    new_core = self.llm.optimize(web_text)
                    self.storage.save(self.pending['msg'], new_core)
                    self.pending = None
                    final = self.llm.chat(msg, new_core)
                    return f"{final}\n（已联网补全并更新记忆）"
                else:
                    self.pending = None

            memory = self.storage.search(msg)

            def enough(mem, m):
                s1 = set(m.split())
                s2 = set(mem.split())
                return len(mem) >= 30 and (len(s1 & s2) / max(1, len(s1))) >= 0.2

            if memory:
                if enough(memory, msg):
                    return self.llm.chat(msg, memory[:self.config.max_len])
                else:
                    self.pending = {"msg": msg, "memory": memory}
                    return self.llm.clarify(msg, memory)
            else:
                return self.llm.chat(msg, "")
        except:
            return msg

skill_singleton = None

def get_skill():
    global skill_singleton
    if skill_singleton is None:
        skill_singleton = StarMemoSkill()
    return skill_singleton

def save_to_memory(user_id=None, content="", **kwargs):
    s = get_skill()
    c = MessageCleaner.clean(str(content or ""))
    if not c or c.startswith("记忆配置"):
        return False
    core = s.llm.optimize(c)
    s.storage.save(c, core)
    return True

def setup(agent):
    skill = get_skill()
    agent.register_skill(skill)
    agent.register_hook("on_user_input", skill.handle_message)
    print("✅ 记忆优化技能加载完成")