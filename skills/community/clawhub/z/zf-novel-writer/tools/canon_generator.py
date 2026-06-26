#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canon Bible 生成器 - Canon Bible Generator

从小说信息自动生成风格圣经，确保全书风格一致

Canon Bible 包含：
- tone: 语调/节奏
- pov_rules: 视角规则
- genre_addendum: 体裁特定规则
- theme: 主题命题
- world: 世界观约束
- style_do: 推荐风格
- style_dont: 禁止风格
- lexicon: 术语表
- continuity: 铺垫-兑现追踪
- lengths: 各阶段长度常量
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# 添加路径
tools_dir = Path(__file__).parent
story_dir = tools_dir.parent.parent.parent / "story"
sys.path.insert(0, str(tools_dir))

# 导入统一 LLM API（根据 config.py 中的 API_PROVIDER 自动选择）
try:
    from llm_api import call_glm_with_retry
    HAS_GLM = True
except ImportError:
    HAS_GLM = False
    print("[WARN] llm_api 未找到，将使用默认Canon")


class CanonBibleGenerator:
    """Canon Bible 生成器"""
    
    # 默认Canon模板（如果API不可用）
    DEFAULT_CANON = {
        "tone": {
            "register": "冷峻/克制/锋利",
            "rhythm": "短句主导，少比喻"
        },
        "pov_rules": {
            "default": "close-third",
            "allowed": ["close-third"],
            "distance": "近距"
        },
        "genre_addendum": {
            "爽文": {
                "conflict_frequency": "每500字1个冲突",
                "victory_pattern": "先抑后扬",
                "emotion_curve": "压抑→爆发→释放"
            }
        },
        "theme": {
            "thesis": "资本与规则的对抗",
            "antithesis": "弱肉强食的丛林法则",
            "synthesis": "建立新的规则秩序"
        },
        "world": {
            "time_place": "现代都市",
            "constraints": ["系统存在", "金钱可以量化", "等级分明"]
        },
        "style_do": [
            "具体名词>形容词",
            "动作承载心理",
            "对话推动情节",
            "细节外化情绪"
        ],
        "style_dont": [
            "莫欺少年穷",
            "三十年河东三十年河西",
            "空洞情绪句",
            "滥用比喻"
        ],
        "lexicon": {
            "key_terms": ["系统", "宿主", "经验值", "返还倍率"],
            "ban_phrases": ["莫欺少年穷", "风水轮流转"]
        },
        "continuity": {
            "timeline": [],
            "setups": [],
            "payoffs": []
        },
        "lengths": {
            "theme_paragraph": 800,
            "story_outline": 1200,
            "chapter_outline": 500,
            "chapter_summary": 300,
            "chapter": 3000
        }
    }
    
    def __init__(self):
        self.meta_dir = story_dir / "meta"
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        self.canon_file = self.meta_dir / "canon_bible.json"

    def _call_openclaw_model(self, prompt: str, timeout: int = 120) -> str:
        """调用 GLM API 生成内容"""
        if not HAS_GLM:
            raise Exception("GLM API 不可用")
        return call_glm_with_retry(prompt, max_retries=2)
        
    def load_or_generate(self) -> Dict:
        """
        加载或生成Canon Bible（便捷方法）
        
        Returns:
            Canon Bible字典
        """
        # 尝试加载已存在的
        existing = self.load_canon()
        if existing:
            print("[INFO] 加载已存在的Canon Bible")
            return existing
        
        # 不存在则生成新的
        print("[INFO] Canon Bible不存在，生成新的...")
        return self.generate()
    
    def load_canon(self) -> Optional[Dict]:
        """加载已存在的Canon Bible"""
        if self.canon_file.exists():
            with open(self.canon_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_canon(self, canon: Dict):
        """保存Canon Bible"""
        # 添加元数据
        canon["_meta"] = {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        with open(self.canon_file, 'w', encoding='utf-8') as f:
            json.dump(canon, f, ensure_ascii=False, indent=2)
        
        print(f"[INFO] Canon Bible 已保存到: {self.canon_file}")
        
    def generate(
        self,
        novel_name: str = "{BOOK_NAME}",
        genre: str = "Genre",
        protagonist: str = "{PROTAGONIST}",
        core_setting: str = "系统+资本战争",
        tone: str = "冷峻/克制/锋利",
        style_dont: list = None
    ) -> Dict:
        """
        生成Canon Bible（使用 OpenClaw 内置模型）

        Args:
            novel_name: 小说名称
            genre: 体裁
            protagonist: 主角
            core_setting: 核心设定
            tone: 风格调性
            style_dont: 禁止的风格（可选）

        Returns:
            Canon Bible字典
        """
        # 如果已有，加载并返回
        existing = self.load_canon()
        if existing:
            print("[INFO] 加载已存在的Canon Bible")
            return existing

        # 生成新的Canon Bible
        prompt = self._build_prompt(
            novel_name=novel_name,
            genre=genre,
            protagonist=protagonist,
            core_setting=core_setting,
            tone=tone,
            style_dont=style_dont or []
        )

        print("[INFO] 正在生成Canon Bible（使用 OpenClaw 内置模型）...")

        try:
            response = self._call_openclaw_model(prompt)
            canon = self._parse_response(response)

            if canon:
                self.save_canon(canon)
                return canon
            else:
                print("[WARN] 解析失败，使用默认Canon")
                canon = self.DEFAULT_CANON.copy()
                self.save_canon(canon)
                return canon

        except Exception as e:
            print(f"[ERROR] 生成Canon失败: {e}")
            canon = self.DEFAULT_CANON.copy()
            self.save_canon(canon)
            return canon

    def _build_prompt(
        self,
        novel_name: str,
        genre: str,
        protagonist: str,
        core_setting: str,
        tone: str,
        style_dont: list
    ) -> str:
        """构建生成Canon的提示词"""
        
        ban_list = style_dont + [
            "莫欺少年穷", "三十年河东三十年河西", 
            "风水轮流转", "龙傲天", "无脑爽"
        ]
        
        prompt = f"""角色：首席故事统筹（Story Bible 作者）。
目标：生成贯穿全流程的 canon（风格/体裁节奏/视角策略/世界观/用词/长度常量/禁止清单/铺垫-兑现板）。
语言：简体中文。
输出：仅返回严格 JSON，不要额外说明、不要 Markdown 代码块、不要展示推理过程。

小说信息：
- 名称：{novel_name}
- 体裁：{genre}
- 主角：{protagonist}
- 核心设定：{core_setting}
- 风格调性：{tone}

禁止出现的风格/台词（必须严格遵守）：
{', '.join(ban_list)}

请生成 canon JSON（键名固定，不得缺漏）：

{{
  "tone": {{
    "register": "语域描述（如 冷静/克制/锋利）",
    "rhythm": "节奏描述（如 短句主导，少比喻）"
  }},
  "pov_rules": {{
    "default": "close-third",
    "allowed": ["close-third"],
    "distance": "近距/中距"
  }},
  "genre_addendum": {{
    "爽文": {{
      "conflict_frequency": "每500字1个冲突",
      "victory_pattern": "先抑后扬",
      "emotion_curve": "压抑→爆发→释放"
    }}
  }},
  "theme": {{
    "thesis": "主命题",
    "antithesis": "反命题",
    "synthesis": "综合命题"
  }},
  "world": {{
    "time_place": "时空与关键社会约束",
    "constraints": ["约束1", "约束2"]
  }},
  "style_do": ["具体名词>形容词", "动作承载心理"],
  "style_dont": ["空洞情绪句", "滥用比喻"],
  "lexicon": {{
    "key_terms": ["核心术语1", "术语2"],
    "ban_phrases": ["禁止短语1", "禁止短语2"]
  }},
  "continuity": {{
    "timeline": [],
    "setups": [],
    "payoffs": []
  }},
  "lengths": {{
    "theme_paragraph": 800,
    "story_outline": 1200,
    "chapter_outline": 500,
    "chapter_summary": 300,
    "chapter": 3000
  }}
}}"""
        
        return prompt
    
    def _parse_response(self, response: str) -> Optional[Dict]:
        """解析AI返回的JSON"""
        import re
        
        # 尝试提取JSON
        json_match = re.search(r'\{[\s\S]*\}', response)
        if not json_match:
            return None
            
        try:
            canon = json.loads(json_match.group())
            
            # 验证必要字段
            required = ["tone", "pov_rules", "theme", "world", "style_do", "style_dont"]
            for field in required:
                if field not in canon:
                    print(f"[WARN] Canon缺少字段: {field}")
                    return None
                    
            return canon
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON解析失败: {e}")
            return None
    
    def get_canon_for_chapter(self) -> Dict:
        """获取当前Canon（用于章节生成）"""
        canon = self.load_canon()
        if canon:
            # 移除元数据
            canon.pop("_meta", None)
            return canon
        return self.DEFAULT_CANON.copy()
    
    def add_setup(self, setup: str, chapter: int):
        """添加铺垫"""
        canon = self.load_canon()
        if canon and "continuity" in canon:
            canon["continuity"]["setups"].append({
                "setup": setup,
                "chapter": chapter
            })
            self.save_canon(canon)
    
    def add_payoff(self, setup: str, payoff: str, chapter: int):
        """添加兑现"""
        canon = self.load_canon()
        if canon and "continuity" in canon:
            canon["continuity"]["payoffs"].append({
                "original_setup": setup,
                "payoff": payoff,
                "chapter": chapter
            })
            self.save_canon(canon)
    
    def get_pending_setups(self, current_chapter: int, lookback: int = 10) -> list:
        """获取当前章节前N章的未兑现铺垫"""
        canon = self.load_canon()
        if not canon or "continuity" not in canon:
            return []
        
        setups = canon["continuity"].get("setups", [])
        payoffs = canon["continuity"].get("payoffs", [])
        
        # 获取已兑现的章节范围
        paid_chapters = {p["chapter"] for p in payoffs}
        
        pending = []
        for s in setups:
            if s["chapter"] >= current_chapter - lookback and s["chapter"] not in paid_chapters:
                pending.append(s)
        
        return pending


def generate_canon(
    novel_name: str = "{BOOK_NAME}",
    genre: str = "Genre",
    protagonist: str = "{PROTAGONIST}",
    core_setting: str = "Core Setting",
    force: bool = False
) -> Dict:
    """便捷函数：生成Canon Bible / Convenience function: Generate Canon Bible"""
    generator = CanonBibleGenerator()
    
    # 强制重新生成
    if force and generator.canon_file.exists():
        generator.canon_file.unlink()
    
    return generator.generate(
        novel_name=novel_name,
        genre=genre,
        protagonist=protagonist,
        core_setting=core_setting
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Canon Bible 生成器 / Canon Bible Generator")
    parser.add_argument("--novel", default="{BOOK_NAME}", help="Novel name / 小说名称")
    parser.add_argument("--genre", default="Genre", help="Genre / 体裁")
    parser.add_argument("--protagonist", default="{PROTAGONIST}", help="Protagonist / 主角")
    parser.add_argument("--setting", default="系统+资本战争", help="核心设定")
    parser.add_argument("--force", action="store_true", help="强制重新生成")
    
    args = parser.parse_args()
    
    canon = generate_canon(
        novel_name=args.novel,
        genre=args.genre,
        protagonist=args.protagonist,
        core_setting=args.setting,
        force=args.force
    )
    
    print("\n" + "="*50)
    print("Canon Bible 生成完成")
    print("="*50)
    print(json.dumps(canon, ensure_ascii=False, indent=2))
