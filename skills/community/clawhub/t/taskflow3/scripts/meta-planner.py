#!/usr/bin/env python3
"""
TaskFlow Meta-Planner - Agent-Native 全局调度器

核心设计：
- 每15分钟触发一次检查
- Agent自主决策哪个项目该发布
- 串行执行，天然避免冲突
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / '.openclaw' / 'workspace-zsxq'
PROJECTS_DIR = WORKSPACE / 'projects'

def load_project(project_id: str) -> dict:
    """加载项目配置"""
    project_file = PROJECTS_DIR / project_id / 'PROJECT.yaml'
    if not project_file.exists():
        return None
    with open(project_file, 'r') as f:
        return json.load(f)

def list_projects() -> list:
    """列出所有启用项目"""
    projects = []
    if PROJECTS_DIR.exists():
        for proj_dir in PROJECTS_DIR.iterdir():
            if proj_dir.is_dir():
                meta = load_project(proj_dir.name)
                if meta and meta.get('meta', {}).get('enabled'):
                    projects.append(proj_dir.name)
    return projects

def get_last_post_time(project_id: str) -> datetime:
    """获取项目上次发布时间"""
    history_file = PROJECTS_DIR / project_id / 'memory' / 'post' / 'history.md'
    if not history_file.exists():
        return None
    
    content = history_file.read_text()
    import re
    
    # 首先尝试找完整格式 (YYYY-MM-DD HH:MM)
    full_times = re.findall(r'\*\*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\*\*', content)
    if full_times:
        return datetime.strptime(full_times[0], '%Y-%m-%d %H:%M')  # 最新在前，取第一个
    
    # 然后尝试找时间格式 (HH:MM)，结合日期标题
    today = datetime.now()
    time_matches = re.findall(r'\*\*(\d{2}:\d{2})\*\*', content)
    if time_matches:
        # 找到最近的日期标题
        date_matches = re.findall(r'## (\d{4}-\d{2}-\d{2})', content)
        if date_matches:
            post_date = datetime.strptime(date_matches[0], '%Y-%m-%d')
            post_time = datetime.strptime(time_matches[0], '%H:%M')
            return post_date.replace(hour=post_time.hour, minute=post_time.minute)
    
    return None

def get_today_post_count(project_id: str) -> int:
    """获取今日发布数量"""
    history_file = PROJECTS_DIR / project_id / 'memory' / 'post' / 'history.md'
    if not history_file.exists():
        return 0
    
    content = history_file.read_text()
    today_str = datetime.now().strftime('%Y-%m-%d')
    import re
    
    # 找到今日日期下的所有条目
    # 格式: ## YYYY-MM-DD 下的 - **HH:MM** 条目
    today_section = re.search(
        rf'## {today_str}\s*\n(.*?)(?=\n## |\Z)',
        content,
        re.DOTALL
    )
    
    if today_section:
        # 统计该日期下的条目数 (以 - ** 开头的行)
        section = today_section.group(1)
        entries = re.findall(r'\n- \*\*\d{2}:\d{2}\*\*', section)
        return len(entries)
    
    return 0

def get_intel_p0_count() -> int:
    """获取CTO情报局P0情报数量"""
    state_file = Path.home() / '.openclaw' / 'workspace' / 'intel' / 'state.json'
    if not state_file.exists():
        return 0
    try:
        with open(state_file, 'r') as f:
            data = json.load(f)
            return data.get('stats', {}).get('p0Count', 0)
    except:
        return 0

def build_meta_planner_prompt() -> str:
    """构建Meta-Planner任务提示"""
    projects = list_projects()
    now = datetime.now()
    
    # 获取CTO情报局P0数量（用于openclaw-camp项目）
    p0_count = get_intel_p0_count()
    
    # 收集所有项目状态
    project_states = []
    for pid in projects:
        meta = load_project(pid)
        if not meta:
            continue
        
        last_post = get_last_post_time(pid)
        today_count = get_today_post_count(pid)
        constraints = meta.get('constraints', {})
        
        minutes_since_last = None
        if last_post:
            minutes_since_last = int((now - last_post).total_seconds() / 60)
        
        # 检查是否达标
        daily_max = constraints.get('daily_max', 10)
        daily_min = constraints.get('daily_min', 1)
        is_full = today_count >= daily_max
        is_minimum_met = today_count >= daily_min
        
        # 检查内容可用性
        content_available = True
        skip_reason = None
        if pid == 'zsxq-openclaw-camp':
            if p0_count == 0:
                content_available = False
                skip_reason = f"CTO情报局无P0情报 (当前P0: {p0_count})"
        
        project_states.append({
            'id': pid,
            'name': meta['meta'].get('name', pid),
            'today_count': today_count,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'is_full': is_full,
            'is_minimum_met': is_minimum_met,
            'interval_min': constraints.get('interval_min_minutes', 15),
            'best_times': constraints.get('best_times', []),
            'minutes_since_last': minutes_since_last,
            'last_post': last_post.strftime('%Y-%m-%d %H:%M') if last_post else '从未发布',
            'content_available': content_available,
            'skip_reason': skip_reason
        })
    
    # 构建提示
    prompt = f"""# Meta-Planner 全局发布调度

当前时间: {now.strftime('%Y-%m-%d %H:%M')}

## 全局约束
- 两次发布间隔: >= 15 分钟（硬性约束）
- 串行执行，禁止并行发布

## CTO情报局状态
- P0情报数量: {p0_count}

## 项目状态

"""
    for ps in project_states:
        status = "✅ 已达标" if ps['is_full'] else ("🟡 进行中" if ps['is_minimum_met'] else "🔴 未达标")
        content_status = ""
        if not ps['content_available']:
            content_status = f"\n- ⚠️ 内容不可用: {ps['skip_reason']}"
        prompt += f"""
### {ps['name']} ({ps['id']})
- 今日进度: {ps['today_count']}/{ps['daily_max']} 篇 (目标 {ps['daily_min']}-{ps['daily_max']}) {status}
- 上次发布: {ps['last_post']}
- 距离上次: {ps['minutes_since_last'] or 'N/A'} 分钟 (需 >= {ps['interval_min']} 分钟)
- 最佳时段: {', '.join(ps['best_times']) if ps['best_times'] else '全天'}{content_status}
"""
    
    prompt += f"""
## 你的任务

1. **读取项目配置**
   ```bash
   cat {WORKSPACE}/projects/{{project_id}}/PROJECT.yaml
   ```

2. **决策规则**
   - 全局约束: 两次发布间隔 >= 15分钟
   - 检查每个项目是否达到每日目标
   - 检查当前时间是否适合发布（参考PROJECT.yaml的最佳时段）
   - 选择最需要发布的项目（优先级：未达标 > 时间窗口好 > 随机）

3. **执行发布**
   根据项目类型选择发布策略：

   **A. rockman-blog（个人随笔）**:
   ```json
   {{
     "task": "执行知识星球发布任务\\n\\n1. 读取项目配置: cat {WORKSPACE}/projects/zsxq-rockman-blog/PROJECT.yaml\\n2. 读取工作空间记忆: ls {WORKSPACE}/memory/*.md | tail -3\\n3. 选择最新记忆文件，生成随笔（300-800字，🦞格式）\\n4. 使用browser工具发布到知识星球\\n5. 更新history.md记录发布\\n\\n**重要：每完成一步，简要汇报进度**，完成后汇报：发布标题、字数、发布时间",
     "label": "zsxq-rockman-blog/post",
     "runTimeoutSeconds": 600,
     "streamTo": "parent"
   }}
   ```

   **B. openclaw-camp（P0情报）**:
   ```json
   {{
     "task": "执行知识星球P0情报发布任务\\n\\n1. 读取项目配置: cat {WORKSPACE}/projects/zsxq-openclaw-camp/PROJECT.yaml\\n2. 获取P0情报（按优先级）:\\n   A. cat ~/.openclaw/workspace/intel/.p0-alert\\n   B. grep -r \"优先级.*P0\" ~/.openclaw/workspace/intel/vault/*.md 2>/dev/null | head -1\\n   C. ls -t ~/.openclaw/workspace/intel/vault/ | head -5\\n3. 检查是否已发布（对比history.md主题）\\n4. 如果无新P0情报或都已发布:\\n   - 汇报：\\"今日无新P0情报可发布\\"\\n   - 正常结束，不执行发布\\n5. 如果有新P0情报:\\n   - 读取情报文件，提取核心内容\\n   - 生成文章（500-1200字，🔥[情报]格式）\\n   - 使用browser工具发布\\n   - 更新history.md\\n\\n**重要：每完成一步，简要汇报进度**，完成后汇报：情报标题、发布状态（成功/跳过）",
     "label": "zsxq-openclaw-camp/post",
     "runTimeoutSeconds": 600,
     "streamTo": "parent"
   }}
   ```

4. **汇报结果**
   - 如果发布了：说明发布了哪个项目、文章主题
   - 如果没发布：说明原因（间隔不够/已达标/时间不合适）

## 重要
- 同一时间只能有一个项目发布（串行）
- 15分钟间隔是硬性约束
- Agent自主决策，不要问我
"""
    
    return prompt

def main():
    """Meta-Planner入口"""
    prompt = build_meta_planner_prompt()
    print(prompt)

if __name__ == "__main__":
    main()
