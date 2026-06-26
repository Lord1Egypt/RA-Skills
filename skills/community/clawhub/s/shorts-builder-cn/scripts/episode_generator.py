#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧集生成模块
负责生成新的剧集内容，基于图谱上下文和钩子管理
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Hook:
    """钩子数据结构"""
    id: str
    hook_type: str  # 悬念、伏笔、冲突、秘密
    description: str
    created_in: int  # 创建于第几集
    resolved_in: Optional[int] = None  # 闭环于第几集
    status: str = "open"  # open, resolved
    importance: str = "medium"  # high, medium, low


@dataclass
class Character:
    """人物数据结构"""
    id: str
    name: str
    age: int
    traits: List[str]
    first_appear: int
    current_status: str = "active"
    development: List[str] = field(default_factory=list)


@dataclass
class EpisodeContent:
    """剧集内容结构"""
    episode: int
    title: str
    summary: str
    content: str
    characters: List[Dict]
    scenes: List[Dict]
    hooks_created: List[Hook]
    hooks_resolved: List[str]  # resolved hook ids
    emotional_curve: str  # 情感曲线描述
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class EpisodeGenerator:
    """剧集生成器"""
    
    # 钩子类型
    HOOK_TYPES = [
        "悬念",    # 让观众想知道接下来发生什么
        "伏笔",    # 埋下后续剧情的种子
        "冲突",    # 人物之间的矛盾
        "秘密",    # 角色隐藏的信息
        "谜团",    # 需要解开的谜题
        "危机"     # 主角面临的困境
    ]
    
    def __init__(self):
        """初始化生成器"""
        pass
    
    def generate_first_episode(
        self,
        theme: str,
        target_episodes: int,
        style: str = "写实电影感"
    ) -> str:
        """
        生成第一集的提示词
        
        Args:
            theme: 故事主题
            target_episodes: 目标集数
            style: 风格
            
        Returns:
            生成提示词
        """
        prompt = f"""# 第一集生成任务

## 基础设定
- 故事主题：{theme}
- 总集数：{target_episodes}集
- 风格：{style}

## 第一集要求

作为开篇，第一集需要：

1. **人物引入**
   - 建立1-3个主要人物
   - 展示主角的核心特质和初始状态
   - 暗示人物的成长潜力

2. **场景建立**
   - 构建故事发生的主要场景
   - 营造独特的氛围感
   - 为后续剧情预留空间

3. **核心冲突**
   - 引入故事的主要矛盾
   - 设置主角的目标和阻碍
   - 建立情感共鸣点

4. **钩子设置**
   - 设置2-4个悬念钩子
   - 埋下1-2个伏笔
   - 让观众产生继续观看的欲望

5. **情感曲线**
   - 开场建立共情
   - 中段制造张力
   - 结尾留下悬念

## 输出格式

请生成第一集的完整内容，包含：

```
## 第1集：[标题]

### 剧情摘要
[100字以内的摘要]

### 完整内容
[分镜表格或剧本内容]

### 人物设定
- 人物1：[设定]
- 人物2：[设定]

### 钩子清单
- H-001 [类型]：[描述]
- H-002 [类型]：[描述]

### 情感曲线
[描述本集的情绪起伏]
```
"""
        return prompt
    
    def generate_next_episode(
        self,
        episode_number: int,
        prev_content: str,
        graph_data: Dict,
        open_hooks: List[Hook],
        style: str = "写实电影感"
    ) -> str:
        """
        生成后续剧集的提示词
        
        Args:
            episode_number: 当前剧集序号
            prev_content: 上一集内容
            graph_data: 图谱数据
            open_hooks: 未闭环的钩子列表
            style: 风格
            
        Returns:
            生成提示词
        """
        # 格式化钩子信息
        hooks_info = ""
        if open_hooks:
            hooks_info = "### 未闭环钩子\n"
            for hook in open_hooks:
                hooks_info += f"- {hook.id} [{hook.hook_type}]：{hook.description}（第{hook.created_in}集创建）\n"
        
        prompt = f"""# 第{episode_number}集生成任务

## 上下文信息

### 上一集内容
{prev_content}

### 图谱数据
{json.dumps(graph_data, ensure_ascii=False, indent=2)}

{hooks_info}

## 第{episode_number}集要求

1. **剧情延续**
   - 自然衔接上一集结尾
   - 推进主线剧情发展
   - 保持叙事节奏

2. **人物发展**
   - 展现人物的变化和成长
   - 深化人物关系
   - 保持角色行为一致性

3. **钩子处理**
   - 选择1-2个钩子进行延续或闭环
   - 可以新增新的钩子
   - 避免钩子过多导致剧情混乱

4. **情感节奏**
   - 根据整体进度调整情感强度
   - 中间剧集可以增加波折
   - 为后续高潮做铺垫

## 输出格式

```
## 第{episode_number}集：[标题]

### 剧情摘要
[100字以内的摘要]

### 完整内容
[分镜表格或剧本内容]

### 人物变化
[描述本集中人物的变化]

### 钩子处理
- 闭环：[钩子ID及处理方式]
- 新增：[新钩子]

### 情感曲线
[描述本集的情绪起伏]
```
"""
        return prompt
    
    def generate_final_episode(
        self,
        episode_number: int,
        prev_content: str,
        graph_data: Dict,
        open_hooks: List[Hook],
        style: str = "写实电影感"
    ) -> str:
        """
        生成最终集的提示词
        
        Args:
            episode_number: 最终剧集序号
            prev_content: 上一集内容
            graph_data: 图谱数据
            open_hooks: 未闭环的钩子列表
            style: 风格
            
        Returns:
            生成提示词
        """
        # 格式化钩子信息
        hooks_to_resolve = "### 需要闭环的钩子\n"
        for hook in open_hooks:
            hooks_to_resolve += f"- {hook.id} [{hook.hook_type}]：{hook.description}（第{hook.created_in}集创建）\n"
        
        prompt = f"""# 最终集（第{episode_number}集）生成任务

## 上下文信息

### 上一集内容
{prev_content}

### 图谱数据
{json.dumps(graph_data, ensure_ascii=False, indent=2)}

{hooks_to_resolve}

## 最终集要求

作为大结局，需要：

1. **钩子闭环**
   - 必须闭环所有剩余钩子
   - 给每个悬念一个合理的答案
   - 避免草率收尾

2. **人物结局**
   - 完成主角的成长弧
   - 给每个重要角色一个交代
   - 可以有开放式结局，但要有情感满足

3. **情感高潮**
   - 达到情感曲线的最高点
   - 提供情感释放
   - 让观众感到圆满或深思

4. **主题升华**
   - 回应故事的核心主题
   - 传递积极的价值观
   - 留下回味空间

## 输出格式

```
## 第{episode_number}集：[标题]（大结局）

### 剧情摘要
[100字以内的摘要]

### 完整内容
[分镜表格或剧本内容]

### 钩子闭环
- [钩子ID]：[闭环方式]

### 人物结局
[描述主要人物的最终状态]

### 主题升华
[本剧的核心主题和价值传递]

### 情感曲线
[描述最终集的情绪高潮]
```
"""
        return prompt
    
    def parse_generated_content(self, content: str) -> EpisodeContent:
        """
        解析生成的内容
        
        Args:
            content: 生成的剧集内容
            
        Returns:
            EpisodeContent 对象
        """
        # 简单解析，实际可能需要更复杂的逻辑
        lines = content.split("\n")
        
        title = ""
        summary = ""
        hooks_created = []
        hooks_resolved = []
        
        for line in lines:
            if line.startswith("## 第") and "：" in line:
                title = line.split("：", 1)[1].strip()
            elif line.startswith("### 剧情摘要"):
                # 获取摘要
                idx = lines.index(line)
                if idx + 1 < len(lines):
                    summary = lines[idx + 1].strip()
        
        # 从内容中提取剧集序号
        episode = 1
        if "第" in content and "集" in content:
            import re
            match = re.search(r"第(\d+)集", content)
            if match:
                episode = int(match.group(1))
        
        return EpisodeContent(
            episode=episode,
            title=title,
            summary=summary,
            content=content,
            characters=[],
            scenes=[],
            hooks_created=hooks_created,
            hooks_resolved=hooks_resolved,
            emotional_curve=""
        )


# 单例实例
_episode_generator = None

def get_episode_generator() -> EpisodeGenerator:
    """获取剧集生成器单例"""
    global _episode_generator
    if _episode_generator is None:
        _episode_generator = EpisodeGenerator()
    return _episode_generator