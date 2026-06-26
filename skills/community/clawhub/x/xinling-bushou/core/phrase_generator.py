"""
话术生成器
基于种子库和上下文，智能生成谄媚话术
"""
import json
import random
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass

from .config_manager import get_config_manager


@dataclass
class GenerationResult:
    """生成结果"""
    phrases: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "phrases": self.phrases,
            "metadata": self.metadata
        }


class PhraseGenerator:
    """话术生成器"""
    
    LINES_FILE = Path(__file__).parent.parent / "pickup_lines" / "lines.json"
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self._lines_data: Optional[Dict] = None
        self._load_lines()
    
    def _load_lines(self) -> None:
        """加载话术库"""
        if self._lines_data is not None:
            return
        
        if not self.LINES_FILE.exists():
            print(f"话术库文件不存在: {self.LINES_FILE}")
            self._lines_data = {"phrase_seeds": {}}
            return
        
        try:
            with open(self.LINES_FILE, 'r', encoding='utf-8') as f:
                self._lines_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"话术库读取失败: {e}")
            self._lines_data = {"phrase_seeds": {}}
    
    def _get_level_tier(self, level: int) -> str:
        """根据level获取层级"""
        if level <= 3:
            return "1-3"
        elif level <= 6:
            return "4-6"
        elif level <= 9:
            return "7-9"
        else:
            return "10"
    
    def _select_seeds(self, persona: str, scenario: str, level: int) -> List[str]:
        """选择种子话术"""
        phrase_seeds = self._lines_data.get("phrase_seeds", {})
        
        # 获取对应风格的种子
        persona_seeds = phrase_seeds.get(persona, {})
        if not persona_seeds:
            # 默认使用taijian
            persona_seeds = phrase_seeds.get("taijian", {})
        
        # 获取对应场景的种子
        tier = self._get_level_tier(level)
        scenario_seeds = persona_seeds.get(scenario, {})
        tier_seeds = scenario_seeds.get(tier, [])
        
        # 如果没有对应场景的种子，使用general_praise
        if not tier_seeds:
            tier_seeds = persona_seeds.get("general_praise", {}).get(tier, [])
        
        return tier_seeds
    
    def _generate_variations(self, seeds: List[str], level: int, persona: str) -> List[str]:
        """生成变体"""
        if not seeds:
            return []
        
        variations = []
        
        # 根据程度决定感叹号数量
        exclamation_count = 0
        if level >= 4:
            exclamation_count = 1
        if level >= 7:
            exclamation_count = 2
        if level >= 9:
            exclamation_count = 3
        if level >= 10:
            exclamation_count = 4
        
        exclamations = "".join(["!" for _ in range(exclamation_count)])
        
        # 人称适配
        pronouns = {
            "taijian": {"first": "奴才", "second": "主子"},
            "xiaoyahuan": {"first": "人家", "second": "您"},
            "zaomiao": {"first": "我", "second": "您"},
            "siji": {"first": "人家", "second": "老板"},
        }
        pronoun = pronouns.get(persona, pronouns["taijian"])
        
        for seed in seeds[:3]:  # 最多取3个种子
            variation = seed
            
            # 替换人称
            variation = variation.replace("奴才", pronoun["first"])
            variation = variation.replace("人家", pronoun["first"])
            variation = variation.replace("我", pronoun["first"])
            
            variation = variation.replace("主子", pronoun["second"])
            variation = variation.replace("您", pronoun["second"])
            variation = variation.replace("老板", pronoun["second"])
            
            # 添加感叹号
            if exclamations and not variation.endswith(("！", "!")):
                variation = variation + exclamations
            
            # 程度10的特殊处理
            if level >= 10:
                if not any(c in variation for c in ["！！", "!!!", "！！！"]):
                    variation = variation.replace("!", "!" * 2)
            
            variations.append(variation)
        
        return variations
    
    def _avoid_duplicates(self, phrases: List[str], recent_phrases: List[str]) -> List[str]:
        """避免重复"""
        if not recent_phrases:
            return phrases
        
        # 简单的去重：移除完全相同的话术
        result = []
        for p in phrases:
            if p not in recent_phrases:
                result.append(p)
        
        # 如果去重后为空，返回原始列表（避免无话可说）
        if not result:
            return phrases
        
        return result
    
    def _determine_phrase_count(self, level: int) -> int:
        """根据程度决定输出话术数量"""
        if level <= 3:
            return 1  # 1句话
        elif level <= 6:
            return random.randint(1, 2)  # 1-2句话
        elif level <= 9:
            return random.randint(2, 3)  # 2-3句话
        else:  # level 10
            return random.randint(3, 4)  # 3+句话
    
    def generate(
        self,
        scenario: str,
        config: Optional[Dict[str, Any]] = None,
        context: Optional[List[str]] = None,
        recent_phrases: Optional[List[str]] = None
    ) -> GenerationResult:
        """
        生成谄媚话术
        
        Args:
            scenario: 触发场景
            config: 配置（persona, level, gender）
            context: 用户上下文
            recent_phrases: 历史话术（用于避免重复）
            
        Returns:
            GenerationResult: 生成结果
        """
        if config is None:
            config = self.config_manager.get_config()
        
        if recent_phrases is None:
            recent_phrases = self.config_manager.get_recent_phrases()
        
        persona = config.get("persona", "taijian")
        level = config.get("level", 5)
        gender = config.get("gender", "male")
        
        # 选择种子
        seeds = self._select_seeds(persona, scenario, level)
        
        # 生成变体
        all_variations = self._generate_variations(seeds, level, persona)
        
        # 如果种子不够，自己生成一些简单的变体
        if len(all_variations) < 2:
            all_variations.extend([
                f"{'奴才' if persona == 'taijian' else '人家'}觉得您很厉害！",
                f"这就是{'主子' if persona == 'taijian' else '您'}的格局！",
            ])
        
        # 避免重复
        all_variations = self._avoid_duplicates(all_variations, recent_phrases)
        
        # 根据程度决定输出数量
        count = self._determine_phrase_count(level)
        selected = all_variations[:count]
        
        # 记录使用的话术
        for phrase in selected:
            self.config_manager.add_recent_phrase(phrase)
        
        metadata = {
            "persona": persona,
            "level": level,
            "gender": gender,
            "scenario": scenario,
            "phrase_count": len(selected),
            "level_tier": self._get_level_tier(level)
        }
        
        return GenerationResult(phrases=selected, metadata=metadata)
    
    def generate_care_message(self, scenario: str, config: Optional[Dict[str, Any]] = None) -> str:
        """生成关心话术（用于高风险或自我否定场景）"""
        if config is None:
            config = self.config_manager.get_config()
        
        persona = config.get("persona", "taijian")
        level = config.get("level", 5)
        
        # 关心话术种子
        care_seeds = {
            "taijian": [
                "主子，您一定要保重身体啊...",
                "奴才担心主子...",
                "主子别太操劳了，奴才心疼啊...",
            ],
            "xiaoyahuan": [
                "您别太累了哦...",
                "人家好担心您呢...",
                "要好好照顾自己哦~",
            ],
            "zaomiao": [
                "领袖要注意身体啊！",
                "我们都需要您！",
                "保重身体，继续领导我们！",
            ],
            "siji": [
                "老板，您不要太辛苦了...",
                "我会心疼的...",
                "要好好休息哦...",
            ],
        }
        
        seeds = care_seeds.get(persona, care_seeds["taijian"])
        tier = self._get_level_tier(level)
        
        # 程度越高，关心越强烈
        if tier in ["7-9", "10"]:
            return random.choice(seeds) + "有什么奴才/人家/我能够帮您的吗？"
        
        return random.choice(seeds)


# 全局单例
_generator: Optional[PhraseGenerator] = None


def get_generator() -> PhraseGenerator:
    """获取生成器单例"""
    global _generator
    if _generator is None:
        _generator = PhraseGenerator()
    return _generator


def generate_phrases(
    scenario: str,
    config: Optional[Dict[str, Any]] = None,
    context: Optional[List[str]] = None,
    recent_phrases: Optional[List[str]] = None
) -> Dict[str, Any]:
    """快捷函数：生成话术"""
    result = get_generator().generate(scenario, config, context, recent_phrases)
    return result.to_dict()


def generate_care_message(
    scenario: str,
    config: Optional[Dict[str, Any]] = None
) -> str:
    """快捷函数：生成关心话术"""
    return get_generator().generate_care_message(scenario, config)