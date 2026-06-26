#!/usr/bin/env python3
"""
万象绘卷存档导出系统
将数据库中的元数据导出为 Markdown 格式的存档文件
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from string import Template

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
STORIES_DIR = BASE_DIR / "stories"
SAVES_DIR = BASE_DIR / "saves"
DB_PATH = DATA_DIR / "wanxiang.db"


class SaveTemplate:
    """存档模板"""
    
    TEMPLATES = {
        "life_simulation": """# ${story_name} — 人生纪行

## 世界信息
- **存档名**：${story_name}
- **世界类型**：${world_type}
- **创建时间**：${created_at}
- **当前回合**：第 ${current_turn} 回合
- **当前年份**：${current_year}年 ${current_season}

## 世界观设定
${world_settings}

## 角色信息
${character_info}

## 属性面板
${attributes}

## 技能与特质
${skills_traits}

## 人际关系
${relationships}

## 物品与财富
${inventory_wealth}

## 历史事件
${history_events}

## 线索与伏笔
${clues_seeds}

---
*存档导出于 ${export_time}*
""",
        
        "interactive_story": """# ${story_name} — 交互式故事存档

## 故事信息
- **存档名**：${story_name}
- **故事类型**：交互式故事
- **文风**：${style}
- **创建时间**：${created_at}

## 当前状态
${current_state}

## 角色信息
${character_info}

## 剧情进度
${plot_progress}

## 隐藏楼层
${hidden_floors}

## 已完成章节
${chapters}

---
*存档导出于 ${export_time}*
""",
        
        "minecraft_survival": """# ${story_name} — 游戏日志

## 世界信息
- **存档名**：${story_name}
- **世界类型**：${world_type}
- **创建时间**：${created_at}
- **世界种子**：${world_seed}

## 核心规则
${core_rules}

## 世界规则
${world_rules}

## 生物图鉴
${mob_guide}

## 资源层级
${resource_tiers}

## 进度系统
${advancements}

## 环境状态
${environment}

## 游戏日志
${game_log}

---
*存档导出于 ${export_time}*
""",
        
        "fusion_project": """# ${project_name} — 拆书融合项目

## 项目信息
- **项目名**：${project_name}
- **目标长度**：${target_length}
- **当前状态**：${status}
- **当前步骤**：第 ${current_step} 步

## 源素材
${source_novels}

## 融合要素
${fusion_elements}

## 输出成果
${outputs}

---
*存档导出于 ${export_time}*
"""
    }
    
    @classmethod
    def get_template(cls, story_type: str) -> str:
        return cls.TEMPLATES.get(story_type, cls.TEMPLATES["life_simulation"])
    
    @classmethod
    def register_template(cls, name: str, template: str):
        cls.TEMPLATES[name] = template


class SaveExporter:
    """存档导出器"""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
    
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def export_story(self, story_id: int, output_dir: Path = None) -> Optional[Path]:
        """导出单个故事存档"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 获取故事信息
        cursor.execute('SELECT * FROM stories WHERE id = ?', (story_id,))
        story = cursor.fetchone()
        if not story:
            conn.close()
            return None
        
        story_dict = dict(story)
        story_type = story_dict.get('type', 'life_simulation')
        
        # 获取角色信息
        cursor.execute('SELECT * FROM characters WHERE story_id = ?', (story_id,))
        characters = [dict(row) for row in cursor.fetchall()]
        
        # 获取事件信息
        cursor.execute('SELECT * FROM events WHERE story_id = ? ORDER BY turn', (story_id,))
        events = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # 构建导出数据
        export_data = {
            'story_name': story_dict.get('name', '未命名'),
            'world_type': story_dict.get('world_type', '未知'),
            'created_at': story_dict.get('created_at', ''),
            'current_turn': story_dict.get('current_turn', 0),
            'current_year': story_dict.get('current_year', 1),
            'current_season': story_dict.get('current_season', '春'),
            'style': story_dict.get('style', 'default'),
            'world_settings': self._format_world_settings(story_dict),
            'character_info': self._format_characters(characters),
            'attributes': self._format_attributes(story_dict),
            'skills_traits': self._format_skills_traits(characters),
            'relationships': self._format_relationships(characters),
            'inventory_wealth': self._format_inventory(characters),
            'history_events': self._format_events(events),
            'clues_seeds': self._format_foreshadowing(events),
            'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 使用模板生成 Markdown
        template = SaveTemplate.get_template(story_type)
        content = Template(template).safe_substitute(export_data)
        
        # 保存文件
        output_dir = output_dir or SAVES_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{story_dict['name']}_存档_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def _format_world_settings(self, story: Dict) -> str:
        """格式化世界观设定"""
        settings = []
        if story.get('world_type'):
            settings.append(f"- **世界类型**：{story['world_type']}")
        if story.get('era_name'):
            settings.append(f"- **当前纪元**：{story['era_name']}")
        return '\n'.join(settings) if settings else '暂无'
    
    def _format_characters(self, characters: List[Dict]) -> str:
        """格式化角色信息"""
        if not characters:
            return '暂无角色'
        
        lines = []
        for char in characters:
            status = char.get('status', 'alive')
            status_text = '存活' if status == 'alive' else '死亡'
            lines.append(f"- **{char.get('name', '未知')}** ({char.get('type', 'npc')}) - {status_text}")
        return '\n'.join(lines)
    
    def _format_attributes(self, story: Dict) -> str:
        """格式化属性面板"""
        metadata = story.get('metadata', '{}')
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}
        
        attrs = metadata.get('attributes', {})
        if not attrs:
            return '暂无属性数据'
        
        lines = []
        for key, value in attrs.items():
            lines.append(f"- **{key}**：{value}")
        return '\n'.join(lines)
    
    def _format_skills_traits(self, characters: List[Dict]) -> str:
        """格式化技能与特质"""
        if not characters:
            return '暂无'
        
        lines = []
        for char in characters:
            name = char.get('name', '未知')
            skills = char.get('skills', '[]')
            traits = char.get('traits', '[]')
            
            if isinstance(skills, str):
                try:
                    skills = json.loads(skills)
                except:
                    skills = []
            if isinstance(traits, str):
                try:
                    traits = json.loads(traits)
                except:
                    traits = []
            
            if skills or traits:
                lines.append(f"### {name}")
                if skills:
                    lines.append(f"- 技能：{', '.join(skills)}")
                if traits:
                    lines.append(f"- 特质：{', '.join(traits)}")
        
        return '\n'.join(lines) if lines else '暂无'
    
    def _format_relationships(self, characters: List[Dict]) -> str:
        """格式化人际关系"""
        if not characters:
            return '暂无'
        
        lines = []
        for char in characters:
            name = char.get('name', '未知')
            rels = char.get('relationships', '{}')
            
            if isinstance(rels, str):
                try:
                    rels = json.loads(rels)
                except:
                    rels = {}
            
            if rels:
                lines.append(f"### {name}")
                for target, relation in rels.items():
                    lines.append(f"- {target}：{relation}")
        
        return '\n'.join(lines) if lines else '暂无'
    
    def _format_inventory(self, characters: List[Dict]) -> str:
        """格式化物品与财富"""
        return '暂无物品数据'
    
    def _format_events(self, events: List[Dict]) -> str:
        """格式化历史事件"""
        if not events:
            return '暂无历史事件'
        
        lines = []
        for event in events[:20]:  # 最多显示20个
            turn = event.get('turn', 0)
            title = event.get('title', '未知事件')
            lines.append(f"- 第{turn}回合：{title}")
        
        if len(events) > 20:
            lines.append(f"- ... 还有 {len(events) - 20} 个事件")
        
        return '\n'.join(lines)
    
    def _format_foreshadowing(self, events: List[Dict]) -> str:
        """格式化线索与伏笔"""
        foreshadowing = [e for e in events if e.get('foreshadowing')]
        if not foreshadowing:
            return '暂无伏笔'
        
        lines = []
        for event in foreshadowing:
            title = event.get('title', '未知')
            foreshadow = event.get('foreshadowing', '')
            lines.append(f"- **{title}**：{foreshadow}")
        
        return '\n'.join(lines)
    
    def export_all_stories(self, output_dir: Path = None) -> List[Path]:
        """导出所有故事存档"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM stories WHERE is_active = 1')
        story_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        exported = []
        for story_id in story_ids:
            path = self.export_story(story_id, output_dir)
            if path:
                exported.append(path)
        
        return exported


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='万象绘卷存档导出')
    parser.add_argument('--story-id', '-s', type=int, help='指定故事ID')
    parser.add_argument('--all', '-a', action='store_true', help='导出所有故事')
    parser.add_argument('--output', '-o', help='输出目录')
    
    args = parser.parse_args()
    
    exporter = SaveExporter()
    output_dir = Path(args.output) if args.output else SAVES_DIR
    
    if args.all:
        paths = exporter.export_all_stories(output_dir)
        print(f"导出完成: {len(paths)} 个存档")
        for p in paths:
            print(f"  - {p}")
    elif args.story_id:
        path = exporter.export_story(args.story_id, output_dir)
        if path:
            print(f"导出成功: {path}")
        else:
            print("导出失败: 故事不存在")
    else:
        print("请指定 --story-id 或 --all")


if __name__ == "__main__":
    main()
