#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界上下文加载器 - World Context Loader v5
从 canon_bible.json、story_outline.xlsx、WORLD_SETTING.md 读取数据

数据源：
- canon_bible.json: 主角+纪元(含反派)+女主+风格+铺垫
- story_outline.xlsx: 章节规划
- WORLD_SETTING.md: 世界观+沈烬+情绪周期+终局
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List


class WorldContextLoader:
    """世界上下文加载器"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.parent.parent.parent
        self.story_dir = self.workspace / 'story'
        self.meta_dir = self.story_dir / "meta"
        self.canon_file = self.meta_dir / "canon_bible.json"
        self.excel_path = self.story_dir / "story_outline.xlsx"
        self.summaries_dir = self.story_dir / "summaries_json"
        self.world_setting_file = self.story_dir / "WORLD_SETTING.md"
        
        self._canon_cache = None
        self._world_setting_cache = None
    
    # ==================== Canon Bible ====================
    def _load_canon(self) -> Dict[str, Any]:
        """加载 Canon Bible"""
        if self._canon_cache is not None:
            return self._canon_cache
        
        if not self.canon_file.exists():
            return {}
        
        try:
            with open(self.canon_file, 'r', encoding='utf-8-sig') as f:
                self._canon_cache = json.load(f)
            return self._canon_cache
        except Exception as e:
            print(f"[ERROR] 加载 canon_bible.json 失败: {e}")
            return {}
    
    def get_protagonist(self) -> Dict[str, Any]:
        """获取主角设定"""
        canon = self._load_canon()
        return canon.get('protagonist', {
            'name': '陈安', 'age': 20,
            'core_traits': ['冷静理性', '逻辑至上'],
            'must_do': ['有恩必报', '有仇必报'],
            'must_not_do': ['忍气吞声', '圣母心态']
        })
    
    def get_era_info(self, chapter_num: int) -> Dict[str, Any]:
        """根据章节号获取纪元信息（含反派和沈烬状态）"""
        canon = self._load_canon()
        eras = canon.get('eras', [])
        
        for era in eras:
            chapters = era.get('chapters', '')
            if '-' in chapters:
                start, end = map(int, chapters.split('-'))
                if start <= chapter_num <= end:
                    return era
    
    def get_heroines(self) -> List[Dict[str, Any]]:
        """获取女主列表"""
        canon = self._load_canon()
        return canon.get('heroines', [])
    
    def get_heroine_phases(self, chapter_num: int) -> List[Dict[str, Any]]:
        """获取当前章节的女主阶段"""
        heroines = self.get_heroines()
        result = []
        
        for heroine in heroines:
            phases = heroine.get('phases', [])
            for phase in phases:
                chapters = phase.get('chapters', '')
                if '-' in chapters:
                    start, end = map(int, chapters.split('-'))
                    if start <= chapter_num <= end:
                        result.append({
                            'name': heroine.get('name'),
                            'type': heroine.get('type'),
                            'phase': phase.get('label')
                        })
                        break
        
        return result
    
    def get_style_rules(self) -> Dict[str, Any]:
        """获取风格规则"""
        canon = self._load_canon()
        return {
            'style_do': canon.get('style_do', []),
            'style_dont': canon.get('style_dont', []),
            'tone': canon.get('tone', {}),
            'theme': canon.get('theme', {})
        }
    
    def get_villain(self, chapter_num: int) -> Dict[str, str]:
        """获取当前章节的反派"""
        era_info = self.get_era_info(chapter_num)
        return {
            'name': era_info.get('villain', '未知'),
            'type': era_info.get('villain_type', '未知')
        }
    
    def get_shen_jin_status(self, chapter_num: int) -> str:
        """获取沈烬当前状态"""
        era_info = self.get_era_info(chapter_num)
        return era_info.get('shen_jin', '海外崛起')
    
    def get_pending_setups(self, current_chapter: int) -> List[Dict[str, Any]]:
        """获取未兑现的铺垫（动态计算）"""
        canon = self._load_canon()
        continuity = canon.get('continuity', {})
        
        # 获取所有铺垫
        setups = continuity.get('setups', [])
        
        # 获取已兑现的铺垫 ID
        payoffs = continuity.get('payoffs', [])
        paid_ids = set()
        for p in payoffs:
            # payoffs 可能有 original_setup 或 id 字段
            setup_id = p.get('original_setup') or p.get('id', '')
            if setup_id:
                paid_ids.add(setup_id)
        
        # 过滤：只返回当前章节之前的、未兑现的、活跃的铺垫
        pending = [
            s for s in setups 
            if s.get('chapter', 0) < current_chapter 
            and s.get('id') not in paid_ids
            and s.get('status', 'active') == 'active'
        ]
        
        return pending
    
    # ==================== WORLD_SETTING.md ====================
    def get_world_setting(self) -> str:
        """获取世界设定（AI参考）"""
        if self._world_setting_cache is not None:
            return self._world_setting_cache
        
        if not self.world_setting_file.exists():
            return ""
        
        try:
            with open(self.world_setting_file, 'r', encoding='utf-8') as f:
                self._world_setting_cache = f.read()
            return self._world_setting_cache
        except Exception as e:
            print(f"[ERROR] 加载 WORLD_SETTING.md 失败: {e}")
            return ""
    
    # ==================== story_outline.xlsx ====================
    def load_chapter_info(self, chapter_num: int) -> Optional[Dict[str, Any]]:
        """
        从 Excel 加载章节信息
        
        Excel 列结构（v2）：
        0. 章
        1. 标题
        2. 核心事件
        3. 对手
        4. 女主
        5. 剧情核心
        6. 冲突类型
        7. 系统提示
        8. 系统级别
        9. 阶段
        10. 已激活属性
        11. 爽点
        12. 信息增量
        13. 高维片段
        """
        if not self.excel_path.exists():
            return None
        
        try:
            import openpyxl
            wb = openpyxl.load_workbook(self.excel_path)
            ws = wb.active
            
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0] == chapter_num:
                    system_level = row[8] if len(row) > 8 else '青铜'
                    era_stage = row[9] if len(row) > 9 else '初始阶段'
                    
                    return {
                        'chapter': chapter_num,
                        'title': row[1] if len(row) > 1 else '',
                        'core_event': row[2] if len(row) > 2 else '',
                        'opponent': row[3] if len(row) > 3 else '',
                        'heroine': row[4] if len(row) > 4 else '',
                        'plot_core': row[5] if len(row) > 5 else '',
                        'conflict_type': row[6] if len(row) > 6 else '',
                        'system_hint': row[7] if len(row) > 7 else '',
                        'system_level': system_level,
                        'era_stage': era_stage,
                        'full_era_stage': f"{system_level}{era_stage}",
                        'active_attribute': row[10] if len(row) > 10 else '',
                        'cool_point': row[11] if len(row) > 11 else '',
                        'info_increment': row[12] if len(row) > 12 else '',
                        'high_dimension': row[13] if len(row) > 13 else ''
                    }
        except Exception as e:
            print(f"[ERROR] 读取Excel失败: {e}")
        
        return None
    
    def load_previous_summaries(self, chapter_num: int, count: int = 1) -> List[Dict[str, Any]]:
        """
        加载前一章的概要
        
        只支持新格式: chapter_XXX.json
        只读取前一章（count=1）
        """
        summaries = []
        
        # 只读取前一章
        prev_chapter = chapter_num - 1
        if prev_chapter < 1:
            return summaries
        
        summary_file = self.summaries_dir / f"chapter_{prev_chapter:03d}.json"
        
        if summary_file.exists():
            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                summaries.append({'chapter': prev_chapter, 'data': data})
            except Exception as e:
                print(f"[WARN] 读取summary失败: {e}")
        
        return summaries
    
    def load_previous_chapter_ending(self, chapter_num: int) -> Optional[Dict[str, Any]]:
        """
        加载前一章的结尾信息（用于衔接）
        
        Returns:
            {
                "time": "2019年4月15日晚上",  # 时间点
                "scene": "林晚晴敲门，陈安准备开门",  # 场景描述
                "emotion": "悬念/紧张",  # 情绪状态
                "last_300_chars": "陈安的手放在门把上..."  # 正文最后300字
            }
            如果不存在则返回 None
        """
        prev_chapter = chapter_num - 1
        if prev_chapter < 1:
            return None
        
        result = {}
        
        # 1. 从 JSON 读取 ending 字段
        summary_file = self.summaries_dir / f"chapter_{prev_chapter:03d}.json"
        if summary_file.exists():
            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                ending = data.get('ending', {})
                if ending:
                    result['time'] = ending.get('time', '')
                    result['scene'] = ending.get('scene', '')
                    result['emotion'] = ending.get('emotion', '')
            except Exception as e:
                print(f"[WARN] 读取ending失败: {e}")
        
        # 2. 从正文文件读取最后300字
        chapters_dir = self.story_dir / "chapters"
        if chapters_dir.exists():
            # 查找前一章的正文文件（支持中英文文件名）
            import glob
            patterns = [
                f"chapter-{prev_chapter}_*.txt",
                f"chapter_{prev_chapter}_*.txt",
                f"chapter{prev_chapter}_*.txt"
            ]
            
            chapter_file = None
            for pattern in patterns:
                matches = list(chapters_dir.glob(pattern))
                if matches:
                    chapter_file = matches[0]
                    break
            
            if chapter_file and chapter_file.exists():
                try:
                    with open(chapter_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 去除【变量更新】及其之后的内容
                    if '【变量更新】' in content:
                        content = content.split('【变量更新】')[0]
                    
                    # 去除其他元数据
                    if '【本章创建的铺垫】' in content:
                        content = content.split('【本章创建的铺垫】')[0]
                    
                    # 取最后300字
                    content = content.strip()
                    if len(content) > 300:
                        result['last_300_chars'] = content[-300:]
                    else:
                        result['last_300_chars'] = content
                except Exception as e:
                    print(f"[WARN] 读取正文失败: {e}")
        
        # 如果有内容则返回
        if result:
            return result
        return None
    
    def get_protagonist_state(self, chapter_num: int) -> Dict[str, Any]:
        """
        获取当前章节主角状态（从上一章的 summary JSON 读取）
        
        Returns:
            {
                "age": 23,  # 当前年龄
                "location": "上沪市城中村出租屋",  # 当前位置
                "status": "回溯后刚觉醒",  # 当前状态
                "timeline": "2019年3月15日"  # 时间线
            }
            如果不存在则返回默认值
        """
        # 第一章的特殊处理：根据剧情设定
        if chapter_num == 1:
            return {
                'age': 34,  # 第1章是原时间线末尾，主角34岁
                'location': '三十八层会议厅',
                'status': '资产被冻结，系统未响应',
                'timeline': '原时间线（回溯前）'
            }
        
        # 从上一章的 summary JSON 读取
        prev_chapter = chapter_num - 1
        summary_file = self.summaries_dir / f"chapter_{prev_chapter:03d}.json"
        
        if summary_file.exists():
            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                protagonist_state = data.get('protagonist_state', {})
                if protagonist_state:
                    return protagonist_state
            except Exception as e:
                print(f"[WARN] 读取protagonist_state失败: {e}")
        
        # 默认值
        return {
            'age': 23,
            'location': '未知',
            'status': '未知',
            'timeline': '未知'
        }
    
    # ==================== 综合上下文 ====================
    def get_context(self, chapter_num: int) -> Dict[str, Any]:
        """
        获取完整上下文
        
        Returns:
            - protagonist: 主角设定
            - protagonist_state: 主角当前状态（年龄、位置、状态、时间线）
            - era_info: 纪元信息（含反派、沈烬状态）
            - heroines: 女主列表
            - heroine_phases: 当前女主阶段
            - style_rules: 风格规则
            - villain: 当前反派
            - shen_jin_status: 沈烬状态
            - pending_setups: 未兑现铺垫
            - chapter_info: 章节规划信息
            - prev_summaries: 前章概要
            - prev_ending: 前章结尾信息（用于衔接）
            - world_setting: 世界设定（AI参考）
            - canon: 完整 canon 数据（用于健康度检查）
        """
        canon = self._load_canon()
        
        return {
            'protagonist': self.get_protagonist(),
            'protagonist_state': self.get_protagonist_state(chapter_num),
            'era_info': self.get_era_info(chapter_num),
            'heroines': self.get_heroines(),
            'heroine_phases': self.get_heroine_phases(chapter_num),
            'style_rules': self.get_style_rules(),
            'villain': self.get_villain(chapter_num),
            'shen_jin_status': self.get_shen_jin_status(chapter_num),
            'pending_setups': self.get_pending_setups(chapter_num),
            'chapter_info': self.load_chapter_info(chapter_num),
            'prev_summaries': self.load_previous_summaries(chapter_num),
            'prev_ending': self.load_previous_chapter_ending(chapter_num),
            'world_setting': self.get_world_setting(),
            'canon': canon
        }


# ==================== CLI 测试 ====================
if __name__ == '__main__':
    import sys
    chapter = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    loader = WorldContextLoader()
    context = loader.get_context(chapter)
    
    print(f"=== 第{chapter}章上下文 ===")
    print(f"主角: {context['protagonist']['name']}")
    print(f"纪元: {context['era_info']['level']}")
    print(f"反派: {context['villain']['name']} ({context['villain']['type']})")
    print(f"沈烬: {context['shen_jin_status']}")
    print(f"女主: {len(context['heroine_phases'])}人当前阶段")
    print(f"铺垫: {len(context['pending_setups'])}个未兑现")
    print(f"世界设定: {len(context['world_setting'])}字节")