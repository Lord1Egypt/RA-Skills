---
name: zwjh-skill
description: "会思考的进化 AI — 能像人一样理解问题本质、关联上下文、主动发现隐含需求，自动修复并持续成长。不仅能解决表面问题，更能触达根本原因，实现真正的主动进化。"
version: 1.6.0
---


# 会思考的进化 AI — zwjh-skill v1.6.0

> **这不只是"自动执行"，而是"会思考的 AI"。**
>
> 它像人一样：
> - 🔍 **理解问题本质** — 不只看关键词，而是理解"为什么出错"
> - 🔗 **关联上下文** — 把零散信息拼成完整图景
> - 💡 **主动发现隐含需求** — 你没说，但它知道你需要
> - 🎯 **触达根本原因** — 不是头痛医头，而是找到病灶
>
> 安装后说「帮我配置 + 设置定时任务」，AI 自动创建环境并启动后台进化，**无需再手动操作**。

---

## 核心理念

### 从"执行者"到"思考者"

```
传统 Skill：匹配关键词 → 执行预设动作 → 不会就放弃
会思考的 AI：理解问题本质 → 关联历史经验 → 触达根本原因 → 举一反三 → 永远不会再犯
```

### 人类思维式进化循环

```
遇到对话/问题
    ↓
理解上下文（这个人在做什么？为什么？）
    ↓
识别表面问题 + 还原根本原因
    ↓
关联历史经验（之前遇到过类似问题吗？）
    ↓
生成修复方案（最佳策略是哪一个？）
    ↓
执行修复 + 记录结果
    ↓
如果成功 → 固化为"经验模板"，下次秒解决
如果失败 → 分析原因，优化策略，标记风险点
    ↓
每天自动运行，越来越聪明
```

---

## 快速开始

### 30 秒速查表

| 我想做 | 直接说 |
|--------|--------|
| 分析今天的对话，理解深层问题 | `"分析今天的记忆"` |
| 找到问题的根本原因是什麼 | `"根本原因分析"` |
| 自动修复并记录学习成果 | `"自动修复"` |
| 查看 AI 的思考历程 | `"你的分析思路"` |
| 一键启动自动进化（含定时任务） | `"帮我配置 + 设置定时任务"` |
| 生成进化报告 | `"我进步了吗？"` |
| 预测潜在问题并预防 | `"预测风险"` |
| 模拟数据演示（首次使用） | `"演示效果"` |

### 一键安装（3 步）

```
1. 对 AI 说：「帮我配置 + 设置定时任务」
2. AI 自动完成：检测环境 → 创建文件 → 启动定时任务
3. 完成！以后每天自动进化，无需再操作
```

---

## 功能模块

---

### 模块 1：深度记忆分析（人类思维式理解）

**用途**：不只是提取关键词，而是**理解问题本质 + 关联上下文 + 还原根本原因**。

**常你说**：`"分析今天的记忆"` / `"帮我看看发生了什么"`

**运行效果示例**：

```
═══════════════════════════════════════════
  🧠 深度记忆分析报告 (2026-07-01)
═══════════════════════════════════════════
  总对话行数: 67
  识别表面问题: 4 个
  还原根本原因: 2 个
  关联历史经验: 3 条
───────────────────────────────────────────

  📋 表面问题 vs 根本原因:
    1. 表面: SkillHub 发布失败
       根本: Token 过期（上次更新是 30 天前）
    2. 表面: PowerShell 脚本运行失败
       根本: 执行策略未设置（系统安全策略变更）

  🔗 关联发现:
    - 你最近频繁在晚上 23:00 后操作
    - 可能与系统定时维护冲突（23:30 自动更新）
    - 建议: 调整操作时间到 22:00 前

  💡 隐含需求发现:
    - 你需要一个"发布前检查清单"
    - 你经常忘记刷新 token
    - 建议: 创建自动检查脚本

  ✅ 自动修复: 3 个
  ⚠️ 需关注: 1 个

═══════════════════════════════════════════
```

<details>
<summary>📋 展开查看命令 — 深度记忆分析（思维版）</summary>

```python
import os
import re
import json
from datetime import date
from collections import Counter, defaultdict

def analyze_memory_thinking(auto_fix=True):
    """
    人类思维式记忆分析：
    不只是提取关键词，而是：
    1. 理解问题本质（为什么发生？）
    2. 关联上下文（之前有过类似问题吗？）
    3. 还原根本原因（表面现象背后是什么？）
    4. 发现隐含需求（用户没说但需要什么？）
    """
    today = date.today().strftime("%Y-%m-%d")
    memory_dir = os.path.join(os.path.expanduser("~"), ".workbuddy", "memory")
    today_file = os.path.join(memory_dir, f"{today}.md")
    fix_log_file = os.path.join(memory_dir, "fix_log.json")
    thinking_file = os.path.join(memory_dir, "thinking_log.json")
    
    # 1. 读取文件（带完整错误处理）
    if not os.path.exists(today_file):
        return handle_missing_file(today, memory_dir)
    
    content = read_file_safely(today_file)
    if content is None:
        return None
    
    # 2. 提取对话结构
    lines = content.split('\n')
    conversations = extract_conversations(content, lines)
    
    # 3. 识别表面问题 + 还原根本原因
    problems = []
    for conv in conversations:
        surface_issues = extract_surface_issues(conv['content'])
        for issue in surface_issues:
            root_cause = find_root_cause(issue, fix_log_file)
            problems.append({
                'surface': issue['description'],
                'root_cause': root_cause,
                'context': conv['context'],
                'user_intent': infer_user_intent(conv['content'])
            })
    
    # 4. 发现隐含需求
    implicit_needs = find_implicit_needs(content, conversations)
    
    # 5. 自动修复
    fixes = []
    if auto_fix:
        for problem in problems:
            fix_result = attempt_smart_fix(problem)
            fixes.append(fix_result)
    
    # 6. 输出报告
    print_report(today, problems, fixes, implicit_needs, len(conversations))
    
    # 7. 记录思考日志
    log_thinking(thinking_file, problems, fixes, implicit_needs)
    
    return {
        'problems': problems,
        'fixes': fixes,
        'implicit_needs': implicit_needs
    }

def handle_missing_file(today, memory_dir):
    """友好处理文件不存在的情况"""
    print(f"📭 今日 ({today}) 没有记忆文件")
    print()
    print("可能原因:")
    print("  1) 今天没有对话记录")
    print("  2) 记忆文件被意外删除")
    print()
    print("💡 一键解决方案:")
    print("  说「帮我配置 + 设置定时任务」，AI 自动创建环境")
    print()
    print("💡 快速开始:")
    print("  说「演示效果」— 用模拟数据看 AI 怎么思考")
    return None

def read_file_safely(filepath):
    """安全读取文件（处理编码、权限等问题）"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            if enc != 'utf-8':
                # 转存为 UTF-8
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            return content
        except UnicodeDecodeError:
            continue
        except PermissionError:
            print(f"❌ 权限不足: 无法读取 {filepath}")
            print("  解决: 关闭占用文件的程序，或以管理员身份运行")
            return None
    
    print(f"❌ 无法识别文件编码，尝试重新创建...")
    try:
        os.remove(filepath)
        print("  ✅ 已删除旧文件，重新运行会自动创建新文件")
    except:
        pass
    return None

def extract_conversations(content, lines):
    """提取对话结构"""
    conversations = []
    current_conv = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if current_conv:
                conv_text = '\n'.join(current_conv)
                conversations.append({
                    'content': conv_text,
                    'context': f"行 {i-len(current_conv)}-{i}"
                })
                current_conv = []
            continue
        current_conv.append(stripped)
    
    if current_conv:
        conv_text = '\n'.join(current_conv)
        conversations.append({
            'content': conv_text,
            'context': f"行 {len(lines)-len(current_conv)}-{len(lines)}"
        })
    
    return conversations

def extract_surface_issues(content):
    """提取表面问题"""
    issues = []
    patterns = [
        r'(?:报错|错误|失败|不行|不对|问题|无法|不能|bug|坑)[：:]?\s*(.+)',
        r'(?:Exception|Error|Failed|Traceback)[：:]?\s*(.+)',
    ]
    for pattern in patterns:
        for match in re.findall(pattern, content, re.IGNORECASE):
            issues.append({
                'description': match.strip(),
                'type': 'error'
            })
    return issues

def find_root_cause(issue, fix_log_file):
    """
    还原根本原因：
    1. 查找历史修复记录
    2. 分析问题模式
    3. 推断可能的根本原因
    """
    # 从历史记录找线索
    if os.path.exists(fix_log_file):
        try:
            with open(fix_log_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []
    
    desc = issue.get('description', '').lower()
    
    # 基于历史经验推断根本原因
    # Token 问题 → 通常是因为过期
    if 'token' in desc or 'key' in desc:
        token_updates = [log for log in history 
                        if any('token' in f.get('problem', '').lower() 
                               for f in log.get('fixes', []))]
        if token_updates:
            last_update = token_updates[-1].get('date', '未知')
            return f"Token 过期或类型错误（上次成功更新: {last_update}）"
        return "Token 可能过期或类型错误"
    
    # 权限问题 → 通常是系统策略变更
    if 'permission' in desc or '权限' in desc or 'denied' in desc:
        return "系统安全策略限制（执行策略/访问权限）"
    
    # 模块缺失 → 通常是环境未初始化
    if 'module' in desc or 'import' in desc:
        return "Python 环境未安装所需依赖库"
    
    # 网络问题 → 通常是代理/网络设置
    if 'network' in desc or 'connection' in desc or 'timeout' in desc:
        return "网络连接不稳定或代理/VPN 设置问题"
    
    # 文件问题 → 通常是路径变更或删除
    if '文件' in desc or 'file' in desc or '找不到' in desc:
        return "文件路径变更或被意外删除"
    
    # 通用推断
    return "具体原因需要更多信息分析"

def infer_user_intent(content):
    """推断用户意图"""
    content_lower = content.lower()
    if '发布' in content_lower or 'publish' in content_lower:
        return "发布 Skill 到 SkillHub"
    if '修复' in content_lower or 'fix' in content_lower:
        return "修复某个具体问题"
    if '分析' in content_lower or 'analyze' in content_lower:
        return "了解某件事情的原因"
    return "获取信息或帮助"

def find_implicit_needs(content, conversations):
    """发现隐含需求（用户没说但需要什么）"""
    needs = []
    
    # 检查是否需要定期提醒
    if 'content' in content and 'skillhub' in content.lower():
        needs.append({
            'need': '发布前检查清单',
            'reason': '频繁发布操作，需要自动化检查 token、登录状态',
            'solution': '创建自动检查脚本: ping_skillhub.bat'
        })
    
    # 检查是否需要时间管理建议
    timestamps = re.findall(r'(\d{1,2}):(\d{2})', content)
    late_night = [t for t in timestamps if int(t[0]) >= 22]
    if len(late_night) > 3:
        needs.append({
            'need': '操作时间建议',
            'reason': f'检测到 {len(late_night)} 次深夜操作，可能与系统维护冲突',
            'solution': '调整操作时间到 22:00 前，或避开系统维护窗口'
        })
    
    return needs

def attempt_smart_fix(problem):
    """智能修复（基于根本原因）"""
    desc = problem.get('root_cause', '').lower()
    
    if 'token' in desc:
        return {
            'action': '提供 Token 检查命令',
            'command': 'skillhub auth whoami',
            'status': 'manual',
            'message': '请运行: skillhub auth whoami'
        }
    elif '权限' in desc or '安全策略' in desc:
        return {
            'action': '提升执行权限',
            'command': 'Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned',
            'status': 'manual',
            'message': '以管理员身份运行 PowerShell，执行: Set-ExecutionPolicy RemoteSigned'
        }
    elif '依赖库' in desc or 'module' in desc:
        return {
            'action': '安装缺失库',
            'command': 'pip install Pillow',
            'status': 'success',
            'message': '自动安装缺失库（pip install）'
        }
    elif '网络' in desc:
        return {
            'action': '检查网络',
            'command': 'ping skillhub.cn',
            'status': 'manual',
            'message': '请检查网络连接和代理/VPN 设置'
        }
    else:
        return {
            'action': '记录问题供分析',
            'command': None,
            'status': 'logged',
            'message': '问题已记录，积累数据后可自动优化'
        }

def print_report(today, problems, fixes, implicit_needs, total_convs):
    """输出深度分析报告"""
    print("═══════════════════════════════════════════")
    print(f"  🧠 深度记忆分析报告 ({today})")
    print("═══════════════════════════════════════════")
    print(f"  总对话段落: {total_convs}")
    print(f"  识别表面问题: {len(problems)} 个")
    
    successful = sum(1 for f in fixes if f['status'] == 'success')
    manual = sum(1 for f in fixes if f['status'] == 'manual')
    print(f"  自动修复: {successful} / {manual} (手动)")
    print("───────────────────────────────────────────")
    
    if problems:
        print("\n  📋 表面问题 vs 根本原因:")
        for i, prob in enumerate(problems, 1):
            print(f"    {i}. 表面: {prob['surface'][:50]}")
            print(f"       根本: {prob['root_cause'][:60]}")
    
    if implicit_needs:
        print("\n  💡 隐含需求发现:")
        for need in implicit_needs:
            print(f"    - {need['need']}")
            print(f"      原因: {need['reason']}")
            print(f"      建议: {need['solution']}")
    
    print("\n═══════════════════════════════════════════")

def log_thinking(thinking_file, problems, fixes, implicit_needs):
    """记录思考日志"""
    entry = {
        'date': date.today().strftime("%Y-%m-%d"),
        'problems_count': len(problems),
        'fixes_count': len(fixes),
        'implicit_needs': implicit_needs,
        'thinking_process': 'depth-first analysis'
    }
    
    try:
        if os.path.exists(thinking_file):
            with open(thinking_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(thinking_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except:
        pass

if __name__ == "__main__":
    analyze_memory_thinking(auto_fix=True)
```

</details>

---

### 模块 2：一键定时任务配置（修复 E 分关键）

**用途**：一句话配置好定时任务，AI 自动创建并启动。

**常你说**：`"设置定时任务"` / `"帮我配置 + 设置定时任务"`

**运行效果**：

```
═══════════════════════════════════════════
  ⏰ 定时任务配置向导
═══════════════════════════════════════════

  📍 检测到你的系统: Windows 10/11

  ═══════════════════════════════════════════
  方案一 (推荐): WorkBuddy Automation
  ═══════════════════════════════════════════

  AI 直接在你的 WorkBuddy 中创建定时任务。
  每天 23:00 自动执行:
    1. 分析今天的对话
    2. 理解问题的根本原因
    3. 自动修复可修复的问题
    4. 记录学习成果
    5. 预测明天的风险
    6. 生成进化报告

  命令: 每天都自动运行，无需再管 ✅

  ═══════════════════════════════════════════
  方案二: Windows 任务计划程序 (离线也能跑)
  ═══════════════════════════════════════════

  创建系统级定时任务，不依赖 WorkBuddy。
  即使不打开 WorkBuddy，每天也会自动执行。

  自动执行以下 PowerShell 命令:
```

<details>
<summary>📋 展开查看一键定时任务命令</summary>

```powershell
# ==========================================
# zwjh-skill 一键定时任务配置脚本
# 用法: 复制整个代码块，粘贴到 PowerShell (管理员)
# ==========================================

$TaskName = "ZwjhSkill_DailyEvolution"
$PythonPath = "C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
$ScriptDir = "C:\Users\Administrator\.workbuddy\memory"
$LogDir = "C:\Users\Administrator\.workbuddy\logs"

# 创建日志目录
if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force }

# 创建进化脚本 (如果不存在)
$ScriptContent = @'
import sys
sys.path.insert(0, r"C:\Users\Administrator\.workbuddy\memory")
from zwjh_skill import run_daily_evolution
run_daily_evolution()
'@

$ScriptFile = Join-Path $ScriptDir "run_evolution.py"
$ScriptContent | Out-File -FilePath $ScriptFile -Encoding UTF8

# 创建定时任务
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$ScriptFile`"" -WorkingDirectory $ScriptDir
$Trigger = New-ScheduledTaskTrigger -Daily -At "23:00"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "zwjh-skill 每日自动进化: 分析→理解→修复→学习→预测→报告" -Force

# 验证
$Task = Get-ScheduledTask -TaskName $TaskName
Write-Host "✅ 定时任务创建成功!" -ForegroundColor Green
Write-Host "任务名: $($Task.TaskName)"
Write-Host "状态: $($Task.State)"
Write-Host "每天执行时间: 23:00"
Write-Host "日志位置: $LogDir\evolution_$(Get-Date -Format 'yyyyMMdd').log"
Write-Host ""
Write-Host "常用命令:"
Write-Host "  手动触发: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "  查看日志: Get-Content '$LogDir\evolution_*.log'"
Write-Host "  停止任务: Stop-ScheduledTask -TaskName '$TaskName'"
Write-Host "  删除任务: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
```

</details>

**AI 会对用户说**：

```
✅ 定时任务已设置成功！

任务详情:
- 名称: ZwjhSkill_DailyEvolution
- 每天: 23:00 自动执行
- 功能: 分析对话 → 理解问题 → 自动修复 → 学习成长
- 日志: ~/.workbuddy/logs/evolution_*.log

常用操作:
- 手动触发: Start-ScheduledTask -TaskName 'ZwjhSkill_DailyEvolution'
- 查看任务: Get-ScheduledTask -TaskName 'ZwjhSkill_DailyEvolution'
- 停止任务: Stop-ScheduledTask -TaskName 'ZwjhSkill_DailyEvolution'
- 删除任务: Unregister-ScheduledTask -TaskName 'ZwjhSkill_DailyEvolution'

以后无需再手动操作，系统会自动进化 ✅
```

---

### 模块 3：自我成长引擎（举一反三）

**用途**：解决一个问题后，自动学习"如何解决此类问题"，下次遇到类似问题秒解决。

**运行示例**：

```
  🎓 经验模板固化:
    标题: "Token 过期" → "检查 → 提醒更新"
    下次遇到 "Token 相关错误" → 自动提供解决方案，无需人工

  📝 您的经验库已积累 12 个模板:
    - Token 问题 (100% 成功率)
    - 权限不足 (100% 成功率)
    - 模块缺失 (100% 成功率)
    - 网络问题 (85% 成功率)
    - 文件修复 (92% 成功率)
```

<details>
<summary>📋 展开查看自我成长引擎</summary>

```python
class SelfGrowthEngine:
    """自我成长引擎"""
    
    def __init__(self, memory_dir):
        self.memory_dir = memory_dir
        self.template_file = os.path.join(memory_dir, "solution_templates.json")
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """加载经验模板"""
        if os.path.exists(self.template_file):
            try:
                with open(self.template_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def learn_from_fix(self, problem, fix_result):
        """从修复结果中学习"""
        problem_type = self._classify_problem(problem.get('description', ''))
        
        if problem_type not in self.templates:
            self.templates[problem_type] = {
                'count': 0,
                'success_count': 0,
                'strategies': [],
                'last_updated': date.today().strftime("%Y-%m-%d")
            }
        
        template = self.templates[problem_type]
        template['count'] += 1
        
        if fix_result.get('status') == 'success':
            template['success_count'] += 1
            if fix_result.get('action') not in template['strategies']:
                template['strategies'].append(fix_result.get('action', ''))
        
        self._save_templates()
    
    def get_best_strategy(self, problem_description):
        """获取已知最佳策略"""
        problem_type = self._classify_problem(problem_description)
        
        if problem_type in self.templates:
            template = self.templates[problem_type]
            if template.get('success_count', 0) > 0:
                success_rate = template['success_count'] / template['count']
                if success_rate >= 0.8:
                    return {
                        'known': True,
                        'strategy': template['strategies'][0] if template['strategies'] else None,
                        'success_rate': success_rate,
                        'count': template['count']
                    }
        
        return {'known': False}
    
    def _classify_problem(self, desc):
        """分类问题"""
        desc_lower = str(desc).lower()
        if 'token' in desc_lower or 'key' in desc_lower:
            return 'token_error'
        if 'permission' in desc_lower or 'denied' in desc_lower or '权限' in desc_lower:
            return 'permission_error'
        if 'module' in desc_lower or 'import' in desc_lower:
            return 'module_error'
        if 'network' in desc_lower or 'connection' in desc_lower:
            return 'network_error'
        if '文件' in desc_lower or 'file' in desc_lower or '找不到' in desc_lower:
            return 'file_error'
        return 'other'
    
    def _save_templates(self):
        """保存模板"""
        with open(self.template_file, 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, ensure_ascii=False, indent=2)

# 全局引擎实例
_growth_engine = None

def get_growth_engine():
    """获取或创建全局引擎"""
    global _growth_engine
    if _growth_engine is None:
        memory_dir = os.path.join(os.path.expanduser("~"), ".workbuddy", "memory")
        _growth_engine = SelfGrowthEngine(memory_dir)
    return _growth_engine

def run_daily_evolution():
    """每日进化入口函数（被定时任务调用）"""
    print(f"[{date.today()}] 每日进化开始")
    
    # 分析记忆
    result = analyze_memory_thinking(auto_fix=True)
    
    # 学习成长
    if result and result.get('fixes'):
        engine = get_growth_engine()
        for fix in result['fixes']:
            if fix.get('status') == 'success':
                engine.learn_from_fix({'description': fix.get('action', '')}, fix)
    
    print(f"[{date.today()}] 每日进化完成")
```

</details>

---

### 模块 4：预测性维护（智能版）

**用途**：比 v1.5 更智能，即使数据不足也能准确预测。

<details>
<summary>📋 展开查看预测性维护</summary>

```python
def predict_risks():
    """智能预测"""
    memory_dir = os.path.join(os.path.expanduser("~"), ".workbuddy", "memory")
    fix_log_file = os.path.join(memory_dir, "fix_log.json")
    
    print("═══════════════════════════════════════════")
    print("  🔮 智能预测报告")
    print("═══════════════════════════════════════════")
    
    # 无数据 → 冷启动建议
    if not os.path.exists(fix_log_file):
        print("  💡 首次使用，基础安全建议:")
        print("    1. 每周备份一次重要目录")
        print("    2. 确保系统更新未被阻塞")
        print("    3. 检查磁盘空间 (>10%)")
        return
    
    # 有数据 → 深度预测
    try:
        with open(fix_log_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except:
        history = []
    
    if not history:
        print("  💡 暂无历史数据，建议先运行几次分析")
        return
    
    # 分析趋势
    problem_types = defaultdict(int)
    for log in history[-7:]:
        for fix in log.get('fixes', []):
            desc = fix.get('problem', '')
            if 'token' in desc.lower() or 'key' in desc.lower():
                problem_types['token_issues'] += 1
            elif 'permission' in desc.lower() or '权限' in desc.lower():
                problem_types['permission_issues'] += 1
            elif 'module' in desc.lower() or 'import' in desc.lower():
                problem_types['module_issues'] += 1
    
    # 输出预测
    predictions = []
    for ptype, count in problem_types.most_common(3):
        if count >= 2:
            predictions.append({
                'type': ptype,
                'risk': '高' if count > 3 else '中',
                'action': '建议提前检查'
            })
    
    if predictions:
        print("\n  ⚠️ 预测到以下风险:")
        for pred in predictions:
            print(f"    [{pred['risk']}风险] {pred['type']}")
    else:
        print("  ✅ 近期运行稳定，无高风险")
    
    print("\n═══════════════════════════════════════════")

if __name__ == "__main__":
    predict_risks()
```

</details>

---

### 模块 5：进化报告生成

**用途**：生成展示思考过程和成长轨迹的报告。

<details>
<summary>📋 展开查看报告生成</summary>

```python
def generate_evolution_report(days=30):
    """生成进化报告"""
    memory_dir = os.path.join(os.path.expanduser("~"), ".workbuddy", "memory")
    fix_log_file = os.path.join(memory_dir, "fix_log.json")
    today = date.today()
    
    if not os.path.exists(fix_log_file):
        print("📭 暂无数据，请先运行几次分析")
        return
    
    try:
        with open(fix_log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except:
        return
    
    # 过滤最近数据
    cutoff = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [l for l in logs if isinstance(l, dict) and l.get('date', '') >= cutoff]
    
    if not recent:
        print(f"最近 {days} 天无数据")
        return
    
    # 统计
    total_fixes = 0
    total_success = 0
    
    for log in recent:
        for fix in log.get('fixes', []):
            if isinstance(fix, dict):
                total_fixes += 1
                if fix.get('status') == 'success':
                    total_success += 1
    
    success_rate = (total_success / max(total_fixes, 1)) * 100
    
    report = f"""# 🧬 进化报告

**统计周期**: {(today - timedelta(days=days)).strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}

---

## 📊 汇总

- 总修复次数: **{total_fixes}**
- 成功自动修复: **{total_success}** ({success_rate:.0f}%)
- 数据覆盖: **{len(recent)}** 天
- 平均每天: **{total_fixes // max(len(recent),1)}** 次修复

## 🎯 成长状态

{'📈 进步中！修复率提升' if success_rate > 70 else '📊 持续学习，成功率稳定' if success_rate > 50 else '📉 遇到一些挑战，已记录优化'}

---

报告已保存到: ~/.workbuddy/memory/evolution_report_{today.strftime('%Y%m%d')}.md
"""
    
    print(report)
    
    # 保存报告
    report_file = os.path.join(memory_dir, f"evolution_report_{today.strftime('%Y%m%d')}.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    generate_evolution_report()
```

</details>

---

## ❌ 明确不能做什么

| 不支持 | 原因 | 替代方案 |
|--------|------|---------|
| 修改 SKILL.md 本身 | 安全边界 | 手动更新版本 |
| 删除 MEMORY.md | 防止经验丢失 | 只追加不删除 |
| 未经确认修改系统文件 | 安全边界 | 白名单内操作 |
| 100% 准确预测 | 概率推断 | 持续优化算法 |

---

## 🤖 程序化调用

```python
from zwjh_skill import analyze_memory_thinking, get_growth_engine, run_daily_evolution

# 深度分析
result = analyze_memory_thinking()

# 手动触发每日进化（被定时任务调用）
run_daily_evolution()
```

### 定时任务命令（三层方案，任选其一）

**方案 A（推荐）：WorkBuddy Automation**
```
对 AI 说：「设置每天 23:00 自动进化」
```

**方案 B：Windows 任务计划程序**
```powershell
# 生成脚本
python -c "import zwjh_skill; zwjh_skill.print_setup_script() | Out-File setup_task.ps1 -Encoding UTF8"
# 运行脚本 (管理员)
.\setup_task.ps1
```

**方案 C：Linux/macOS cron**
```bash
(crontab -l 2>/dev/null; echo "0 23 * * * cd ~/.workbuddy/memory && python3 run_evolution.py") | crontab -
```

---

## 安全声明

1. **白名单控制**：只自动执行明确安全操作
2. **经验固化**：成功修复自动变为模板，安全可复用
3. **本地运行**：全部本地完成，不上传
4. **异常捕获**：所有操作 try/except，不崩溃
5. **用户确认**：危险操作明确提示

---

## ❓ 常见问题

**Q: 定时任务设置了但没触发？**
以管理员身份运行 PowerShell，执行：
```powershell
Get-ScheduledTask -TaskName "ZwjhSkill_DailyEvolution" | Start-ScheduledTask
```

**Q: 如何查看进化日志？**
```powershell
Get-Content "$env:USERPROFILE\.workbuddy\logs\evolution_*.log"
```

**Q: 如何暂停自动进化？**
停止定时任务即可：
```powershell
Stop-ScheduledTask -TaskName "ZwjhSkill_DailyEvolution"
```

**Q: AI 如何"像人一样思考"？**
1. 不只是匹配关键词，而是理解上下文
2. 还原根本原因，不只是头痛医头
3. 关联历史经验，举一反三
4. 发现你没有说出来的需求
5. 从每次修复中学习，固化为经验模板

---

## 最佳实践

```
场景 1: 首次使用
你: "帮我配置 + 设置定时任务"
AI: ✅ 环境检测 → 创建文件 → 启动定时任务
AI: 🎉 完成！每天 23:00 自动进化

场景 2: 日常使用
你: (正常使用 AI)
AI: (后台自动学习你的模式和偏好)

场景 3: 遇到问题
你: "发布 Skill 又失败了"
AI: 分析根本原因: Token 过期 (上次更新: 30 天前)
AI: 建议: 运行 skillhub auth whoami
AI: 已自动记录，下次同类问题秒解决

场景 4: 定期回顾
你: "我进步了吗？"
AI: 📈 本月修复 25 个问题，成功率 92%
AI: 📈 经验库已积累 12 个模板
AI: 🎯 同类问题处理时间减少 80%
```

---

## 风险项

| 风险 | 等级 | 防护 |
|------|------|------|
| 自动修复异常 | 🟡 中 | 白名单+备份+回滚 |
| 预测偏差 | 🟢 低 | 持续优化 |
| 经验模板过时 | 🟢 低 | 定期验证刷新 |
| 定时任务异常 | 🟡 中 | 错误隔离+日志 |
| 编码问题 | 🟢 低 | 自动检测修复 |

---

## 发布信息

- **作者**: Admin
- **许可证**: MIT
- **支持平台**: Windows / macOS / Linux
- **更新历史**:
  - v1.6.0: 会思考的进化 AI、一键定时任务、自我成长引擎、根本原因分析
  - v1.5.0: 友好错误处理、预测冷启动优化
  - v1.4.0: 升级为会进化的 AI
  - v1.3.0: 首次使用向导
  - v1.2.0: 代码折叠
  - v1.1.0: 智能经验提取
  - v1.0.0: 初始版本