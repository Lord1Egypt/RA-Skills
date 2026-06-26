"""
Smart Model Selector Hook
在每次会话开始时自动激活，根据任务内容选择最优模型
"""

import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from model_selector import SmartModelSelector, hash_task


# 全局选择器实例
_selector = None


def get_selector() -> SmartModelSelector:
    """获取选择器单例"""
    global _selector
    if _selector is None:
        db_path = Path(__file__).parent.parent / 'data' / 'model_selection.db'
        db_path.parent.mkdir(exist_ok=True)
        _selector = SmartModelSelector(str(db_path))
    return _selector


def on_agent_bootstrap(bootstrap_info: dict) -> dict:
    """
    会话启动时调用（agent:bootstrap 事件）
    注入模型选择提示到上下文中
    """
    selector = get_selector()
    
    # 获取用户的第一个消息（如果有）
    first_message = bootstrap_info.get('first_message', '')
    
    if not first_message:
        return {'action': 'continue'}
    
    # 选择最优模型
    model, reason = selector.select_model(first_message)
    
    # 开始跟踪任务
    selector.start_task(first_message, model)
    
    # 返回模型建议和提示
    return {
        'action': 'inject_context',
        'context': f"""
<smart-model-selector>
🧠 **智能模型选择器已激活**
- 推荐模型：**{model}**
- 选择原因：{reason}
- 提示：你可以用 `/model-use <model>` 手动切换模型
</smart-model-selector>
"""
    }


def on_command(command_data: dict) -> dict:
    """
    用户输入命令时调用
    支持：
    - /model-stats: 查看统计
    - /model-reset: 重置选择器
    - /model-use <model>: 手动指定模型
    - /model-rate <1-5>: 评分
    - /model-select: 根据当前任务重新选择模型
    """
    selector = get_selector()
    
    # 解析命令
    cmd = command_data.get('command', '')
    args_str = command_data.get('args', '')
    args = args_str.split() if args_str else []
    
    # 处理 model 相关命令
    if cmd == 'model-stats':
        stats = selector.get_stats()
        return {
            'action': 'reply',
            'message': format_stats(stats)
        }
    
    elif cmd == 'model-reset':
        selector.reset()
        return {'action': 'reply', 'message': '✅ 已重置当前任务跟踪'}
    
    elif cmd == 'model-use' and args:
        model = args[0]
        if selector.current_task:
            selector.current_task.selected_model = model
        return {'action': 'reply', 'message': f'✅ 已手动指定模型：{model}'}
    
    elif cmd == 'model-rate' and args:
        try:
            rating = int(args[0])
            if 1 <= rating <= 5:
                selector.update_rating(rating)
                return {'action': 'reply', 'message': f'✅ 评分已记录：{rating}/5 ⭐'}
            else:
                return {'action': 'reply', 'message': '❌ 评分范围 1-5'}
        except ValueError:
            return {'action': 'reply', 'message': '❌ 无效的评分'}
    
    elif cmd == 'model-select':
        # 根据当前任务重新选择
        if selector.current_task:
            model, reason = selector.select_model(selector.current_task.task_text)
            return {
                'action': 'reply',
                'message': f"🧠 重新选择模型：**{model}**\n原因：{reason}"
            }
        else:
            return {'action': 'reply', 'message': '❌ 当前没有活动任务'}
    
    # 非 model 命令，继续处理
    return {'action': 'continue'}


def format_stats(stats: dict) -> str:
    """格式化统计信息"""
    if stats['total_tasks'] == 0:
        return "📊 **模型使用统计**\n\n暂无数据，开始使用后会积累统计信息。"
    
    return f"""📊 **模型使用统计**

总任务数：{stats['total_tasks']}
平均对话轮数：{stats['avg_rounds']}
高质量任务比例：{stats['high_score_ratio']*100:.0f}%

**各模型使用情况：**
""" + '\n'.join([
        f"- **{m}**: {d['count']}次，平均得分 {d['avg_score']:.1f}"
        for m, d in stats['model_usage'].items()
    ])


# Hook 入口点
def main(event_type: str, data: dict) -> dict:
    """
    Hook 主入口
    """
    handlers = {
        'agent:bootstrap': on_agent_bootstrap,
        'command': on_command,
    }
    
    handler = handlers.get(event_type)
    if handler:
        return handler(data)
    
    return {'action': 'continue'}
