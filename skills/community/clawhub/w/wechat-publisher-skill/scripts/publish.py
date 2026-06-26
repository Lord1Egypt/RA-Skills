#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布脚本 - OpenClaw 技能版 V1.0
支持：Windows / macOS / Linux
功能：自动发布 AI 新闻到微信公众号草稿箱
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 缺少依赖：requests")
    print("请运行：pip install requests")
    sys.exit(1)


class WeChatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, config_path=None):
        """初始化发布器"""
        # 路径设置
        self.script_dir = Path(__file__).parent
        self.config_path = config_path or self.script_dir / "config" / "config.json"
        self.memory_dir = self.script_dir / "memory"
        self.templates_dir = self.script_dir / "templates"
        self.log_path = self.memory_dir / "wechat-publish.log"
        self.status_path = self.memory_dir / "publish-status.json"
        self.token_cache_path = self.memory_dir / "token-cache.json"
        self.license_path = self.memory_dir / "license.json"
        self.usage_path = self.memory_dir / "usage.json"
        
        # 确保目录存在
        self.memory_dir.mkdir(exist_ok=True)
        
        # 配置日志
        self._setup_logging()
        self.logger.info("========== 发布脚本启动 ==========")
        self.start_time = datetime.now()
        
        # 加载配置
        self.config = self._load_config()
        self._update_status("Initializing", "Load config")
        
        # 初始化授权管理器
        self.free_tries = self.config.get("trial_count", 50)  # 50 次免费试用
    
    def _setup_logging(self):
        """配置日志"""
        self.logger = logging.getLogger("WeChatPublisher")
        self.logger.setLevel(logging.INFO)
        
        # 文件处理器
        file_handler = logging.FileHandler(self.log_path, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.logger.info("配置加载成功")
            return config
        except Exception as e:
            self.logger.error(f"配置加载失败：{e}")
            self._update_status("Failed", "Load config", error=str(e))
            sys.exit(1)
    
    def _update_status(self, status, step, draft_id=None, error=None):
        """更新状态文件"""
        status_data = {
            "status": status,
            "step": step,
            "start_time": self.start_time.isoformat(),
            "update_time": datetime.now().isoformat(),
            "draft_id": draft_id,
            "error": error
        }
        try:
            with open(self.status_path, "w", encoding="utf-8") as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"状态文件写入失败：{e}")
    
    def _get_app_secret(self):
        """从环境变量或配置获取 AppSecret"""
        # 优先从环境变量读取
        app_secret = os.environ.get("WECHAT_APP_SECRET")
        if app_secret:
            self.logger.info("AppSecret 从环境变量读取成功")
            return app_secret
        
        # 从配置文件读取
        app_secret = self.config.get("app_secret")
        if app_secret:
            self.logger.info("AppSecret 从配置文件读取成功")
            return app_secret
        
        self.logger.error("AppSecret 未配置，请设置环境变量或配置文件")
        self._update_status("Failed", "AppSecret missing", error="AppSecret not configured")
        sys.exit(1)
    
    def _get_token(self):
        """获取 Token（带缓存和重试）"""
        self._update_status("Running", "Getting Token")
        
        # 检查缓存
        if self.token_cache_path.exists():
            try:
                with open(self.token_cache_path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                cache_time = datetime.fromisoformat(cache["time"])
                cache_age = (datetime.now() - cache_time).total_seconds() / 60
                if cache_age < 115:  # 115 分钟
                    remaining = 115 - cache_age
                    self.logger.info(f"使用缓存 Token（剩余有效期：{remaining:.1f} 分钟）")
                    return cache["token"]
            except Exception as e:
                self.logger.warning(f"Token 缓存读取失败：{e}")
        
        # 获取新 Token
        app_secret = self._get_app_secret()
        token_url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.config["app_id"],
            "secret": app_secret
        }
        
        # 重试机制
        retry_count = self.config.get("retry_count", 3)
        retry_delay = self.config.get("retry_delay", 5)
        
        for i in range(1, retry_count + 1):
            try:
                self.logger.info(f"获取 Token（尝试 {i}/{retry_count}）")
                response = requests.get(token_url, params=params, timeout=30)
                response.raise_for_status()
                result = response.json()
                
                if "access_token" not in result:
                    raise Exception(f"Token 返回格式错误：{result}")
                
                token = result["access_token"]
                
                # 缓存 Token
                cache_data = {
                    "token": token,
                    "time": datetime.now().isoformat(),
                    "expires_in": result.get("expires_in", 7200)
                }
                with open(self.token_cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache_data, f, indent=2, ensure_ascii=False)
                self.logger.info("Token 已缓存")
                
                self.logger.info(f"Token 获取成功（有效期：{result.get('expires_in', 7200)} 秒）")
                return token
                
            except Exception as e:
                self.logger.error(f"Token 获取失败：{e}")
                if i == retry_count:
                    self._update_status("Failed", "Get Token", error=str(e))
                    sys.exit(1)
                self.logger.info(f"{retry_delay} 秒后重试...")
                time.sleep(retry_delay)
    
    def _load_template(self):
        """加载 HTML 模板"""
        template_name = self.config.get("template", "v5-simple")
        template_path = self.templates_dir / f"{template_name}.html"
        
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            self.logger.warning(f"模板文件不存在：{template_path}，使用内置模板")
            return self._get_builtin_template()
    
    def _get_builtin_template(self):
        """内置 V5 简洁模板"""
        return """
<section style="max-width:670px;margin:0 auto;background:#ffffff;">
<section style="background:linear-gradient(135deg,#4a4a4a,#1a1a1a);padding:35px 25px;text-align:center;">
    <h1 style="font-size:22px;font-weight:600;color:#ffffff;">📰 AI 新闻早报</h1>
</section>
<section style="padding:20px 18px;">
    <p style="font-size:15px;color:#333333;">{content}</p>
</section>
</section>
"""
    
    def _prepare_content(self):
        """准备发布内容"""
        self._update_status("Running", "Preparing content")
        
        today = datetime.now().strftime("%Y 年 %-m 月 %-d 日" if sys.platform != "win32" else "%Y 年 %#m 月 %#d 日")
        today_date = datetime.now().strftime("%Y-%m-%d")
        title = f"【AI 日报】{today} - AI 行业热点新闻"
        
        # 加载模板并替换占位符
        template = self._load_template()
        content = template.replace("{DATE}", today_date)
        content = content.replace("{SUMMARY}", "Anthropic 发布 Claude 3.7 Sonnet 性能提升 40%；Google 推出 TurboQuant 内存压缩算法。")
        content = content.replace("{HEADLINE1_TITLE}", "Anthropic 发布 Claude 3.7 Sonnet")
        content = content.replace("{HEADLINE1_CONTENT}", "Anthropic 正式推出 Claude 3.7 Sonnet，采用混合架构设计，性能提升约 40%。")
        content = content.replace("{HEADLINE2_TITLE}", "Google 发布 TurboQuant")
        content = content.replace("{HEADLINE2_CONTENT}", "Google 推出全新量化算法，可将 AI 工作内存缩小多达 6 倍。")
        
        # 内容检查
        if len(content) > 50000:
            raise Exception(f"内容超长（{len(content)} 字，最大 50000 字）")
        if len(title) > 64:
            raise Exception(f"标题超长（{len(title)} 字，最大 64 字）")
        
        self.logger.info(f"内容准备完成：{title}")
        return title, content
    
    def _check_license(self):
        """检查授权状态"""
        # 检查是否专业版
        if self.license_path.exists():
            with open(self.license_path, "r", encoding="utf-8") as f:
                license_data = json.load(f)
            if license_data.get("type") == "lifetime":
                return True, "pro"
        
        # 检查试用次数
        usage = {"count": 0, "max_tries": self.free_tries}
        if self.usage_path.exists():
            with open(self.usage_path, "r", encoding="utf-8") as f:
                usage = json.load(f)
        
        # 从配置读取最大试用次数（允许动态调整）
        max_tries = self.config.get("trial_count", 50)
        remaining = max_tries - usage["count"]
        
        if remaining > 0:
            return True, "trial", remaining
        
        return False, "expired", 0
    
    def _record_usage(self):
        """记录使用次数"""
        usage = {"count": 0, "max_tries": self.free_tries}
        if self.usage_path.exists():
            with open(self.usage_path, "r", encoding="utf-8") as f:
                usage = json.load(f)
        
        usage["count"] += 1
        usage["last_used"] = datetime.now().isoformat()
        usage["max_tries"] = self.config.get("trial_count", 50)
        
        with open(self.usage_path, "w", encoding="utf-8") as f:
            json.dump(usage, f, indent=2, ensure_ascii=False)
    
    def _create_draft(self, token, title, content):
        """创建草稿（带重试）"""
        self._update_status("Running", "Creating draft")
        
        draft_url = "https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {"access_token": token}
        
        data = {
            "articles": [
                {
                    "title": title,
                    "author": "小蛋蛋",
                    "digest": "15 条 AI 新闻",
                    "content": content,
                    "thumb_media_id": self.config.get("cover_media_id", ""),
                    "show_cover_pic": 1
                }
            ]
        }
        
        # 重试机制
        retry_count = self.config.get("retry_count", 3)
        retry_delay = self.config.get("retry_delay", 5)
        
        for i in range(1, retry_count + 1):
            try:
                self.logger.info(f"创建草稿（尝试 {i}/{retry_count}）")
                response = requests.post(
                    draft_url,
                    params=params,
                    json=data,
                    headers={"Content-Type": "application/json; charset=utf-8"},
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()
                
                if "media_id" not in result:
                    raise Exception(f"草稿创建失败：{result.get('errmsg', '未知错误')}")
                
                draft_id = result["media_id"]
                self.logger.info(f"草稿创建成功！DraftID: {draft_id}")
                
                # 写入结果文件
                result_path = self.memory_dir / f"wechat-publish-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
                result_content = f"# ✅ 发布成功\n\n**执行时间：** {datetime.now().strftime('%H:%M:%S')}\n\n**DraftID:** `{draft_id}`\n\n**标题:** {title}\n\n请老李登录公众号后台预览发布"
                with open(result_path, "w", encoding="utf-8") as f:
                    f.write(result_content)
                self.logger.info(f"结果已写入：{result_path}")
                
                # 更新状态
                self._update_status("Completed", "Done", draft_id=draft_id)
                
                print(f"SUCCESS: DraftID={draft_id}")
                return draft_id
                
            except Exception as e:
                self.logger.error(f"草稿创建失败：{e}")
                if i == retry_count:
                    self._update_status("Failed", "Create draft", error=str(e))
                    sys.exit(1)
                self.logger.info(f"{retry_delay} 秒后重试...")
                time.sleep(retry_delay)
    
    def run(self, no_wait=False):
        """运行发布流程"""
        # 检查授权
        can_use, status, *args = self._check_license()
        
        if not can_use:
            remaining = self.free_tries - usage.get("count", 0)
            print(f"""
╔════════════════════════════════════════════════════╗
║                                                    ║
║   授权状态：❌ 试用次数已用完 ({usage.get('count', 0)}/{self.free_tries})              ║
║                                                    ║
║   📊 已使用：{usage.get('count', 0)} 次 / 总计：{self.free_tries}次                   ║
║                                                    ║
║   💎 专业版：8.8 元 永久买断                        ║
║      运行：openclaw skill buy wechat-publisher     ║
║                                                    ║
║  ✨ 专业版权益：                                    ║
║     - 无限次使用                                   ║
║     - 全部 5 套模板                                 ║
║     - 自动更新支持                                 ║
║     - 优先技术支持                                 ║
║                                                    ║
╚════════════════════════════════════════════════════╝
            """)
            sys.exit(1)
        
        # 记录使用次数
        if status == "trial":
            self._record_usage()
            remaining = args[0] if args else 0
            self.logger.info(f"剩余试用次数：{remaining} 次")
        
        # 等待
        if not no_wait:
            wait_seconds = self.config.get("wait_seconds", 300)
            self.logger.info(f"等待：{wait_seconds} 秒")
            self._update_status("Waiting", f"Waiting {wait_seconds} seconds")
            for i in range(wait_seconds, 0, -1):
                if i % 60 == 0:
                    self.logger.info(f"剩余等待时间：{i//60} 分钟")
                time.sleep(1)
            self.logger.info("等待完成")
        
        # 获取 Token
        token = self._get_token()
        
        # 准备内容
        title, content = self._prepare_content()
        
        # 创建草稿
        draft_id = self._create_draft(token, title, content)
        
        self.logger.info("========== 发布脚本执行完成 ==========")
        return draft_id


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号发布脚本 - OpenClaw 技能版")
    parser.add_argument("--no-wait", action="store_true", help="立即执行（不等待）")
    parser.add_argument("--config", type=str, help="配置文件路径")
    args = parser.parse_args()
    
    publisher = WeChatPublisher(config_path=args.config)
    publisher.run(no_wait=args.no_wait)


if __name__ == "__main__":
    main()
