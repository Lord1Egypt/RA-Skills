# Skill Router — 智能技能路由引擎入口
# 用法: from skill_router import SkillRouter

from pathlib import Path
from router_top5 import Top5Router as _Top5Router


class SkillRouter(_Top5Router):
    """Skill Router — 智能技能路由引擎
    
    用法:
        from skill_router import SkillRouter
        router = SkillRouter()
        router.route_formatted("做一篇系统综述")
    """
    def __init__(self):
        skill_dir = Path(__file__).parent
        index_path = skill_dir / "skill_index.json"
        super().__init__(index_path=index_path)


__all__ = ["SkillRouter"]
