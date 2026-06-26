# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
执行引擎 (v0.4 - 纯调度器设计)

核心原则:
- SkillPilot 只做调度和评测，不自己实现调用逻辑
- 借用 OpenClaw 现有能力执行技能
- 全量模式：调用多个技能 → 收集结果 → 对比质量 → 选出最优
"""

import os
import sys
import time
import importlib
from typing import Dict, Any, Optional, List
from .models import SkillRequest, SkillResult
from .registry import SkillRegistry
from .decision import RouteDecision
from .fallback import FallbackHandler
from .mode import ModeManager


class ExecutionEngine:
    """执行引擎 - 纯调度器"""
    
    def __init__(self, skills_dir: str = None, mode: str = None):
        self.skills_dir = skills_dir or os.path.expanduser("~/.openclaw/workspace/skills")
        self.registry = SkillRegistry(self.skills_dir)
        self.decider = RouteDecision(self.registry)
        self.fallback = FallbackHandler(self.registry, self)
        self.fallback.set_engine(self)
        self.skill_cache: Dict[str, Any] = {}
        self.mode_manager = ModeManager()
        if mode:
            self.mode_manager.set_mode(mode)
    
    def search(self, query: str, mode: str = None, **kwargs) -> SkillResult:
        """搜索"""
        request = SkillRequest(category="search", query=query, **kwargs)
        return self._execute(request, mode=mode)
    
    def fetch(self, url: str, mode: str = None, **kwargs) -> SkillResult:
        """抓取"""
        request = SkillRequest(category="fetch", url=url, **kwargs)
        return self._execute(request, mode=mode)
    
    def summarize(self, content: str, mode: str = None, **kwargs) -> SkillResult:
        """总结"""
        request = SkillRequest(category="summarize", content=content, **kwargs)
        return self._execute(request, mode=mode)
    
    def _execute(self, request: SkillRequest, mode: str = None) -> SkillResult:
        """执行请求"""
        # 自动判断模式
        if mode is None:
            query_text = (request.query or request.url or request.content or "").lower()
            if "全量" in query_text or "full" in query_text or "对比" in query_text:
                exec_mode = "full"
            else:
                exec_mode = "default"
        else:
            exec_mode = mode
        
        # 获取工具列表
        if exec_mode == "full":
            tools = self.mode_manager.get_tools_for_task(request.category, "full")
            return self._execute_all_tools(request, tools)
        else:
            tools = self.mode_manager.get_tools_for_task(request.category, "default")
            default_tool = tools[0] if tools else None
            return self._execute_single_tool(request, default_tool)
    
    def _execute_all_tools(self, request: SkillRequest, tools: List[str]) -> SkillResult:
        """全量模式：执行所有工具并对比"""
        results = []
        
        for tool_name in tools:
            print(f"\n  → 执行工具：{tool_name}")
            start_time = time.time()
            
            try:
                result_dict = self.call_skill(tool_name, request)
                response_time = (time.time() - start_time) * 1000
                
                success = result_dict.get('success', False)
                content = result_dict.get('content', '')
                error = result_dict.get('error', '')
                quality_score = self._evaluate_result_quality(content) if success else 0
                
                self.mode_manager.record_performance(
                    request.category, tool_name,
                    success, response_time, quality_score
                )
                
                results.append({
                    'tool': tool_name,
                    'success': success,
                    'response_time': response_time,
                    'quality_score': quality_score,
                    'result_dict': result_dict,
                })
                
                # 根据实际成功/失败状态显示
                if success and content:
                    print(f"     ✓ 成功，响应：{response_time:.0f}ms，质量：{quality_score:.1f}")
                elif success and not content:
                    print(f"     ⚠ 空结果，响应：{response_time:.0f}ms，质量：{quality_score:.1f}")
                else:
                    error_msg = error[:50] if error else '未知错误'
                    print(f"     ✗ 失败：{error_msg}...")
                
            except Exception as e:
                print(f"     ✗ 失败：{e}")
                results.append({
                    'tool': tool_name,
                    'success': False,
                    'response_time': (time.time() - start_time) * 1000,
                    'quality_score': 0,
                    'error': str(e),
                })
        
        if not results:
            return SkillResult(success=False, error="所有工具执行失败")
        
        successful_results = [r for r in results if r['success']]
        if successful_results:
            best = max(successful_results, key=lambda x: x['quality_score'])
            best_tool = best['tool']
            
            current_default = self.mode_manager.default_tools.get(request.category)
            if best_tool != current_default:
                print(f"\n🏆 工具对比完成：{best_tool} 表现最佳")
                print(f"   原默认：{current_default} → 新默认：{best_tool}")
                self.mode_manager.set_default_tool(request.category, best_tool)
            else:
                print(f"\n🏆 工具对比完成：{best_tool} 保持默认")
            
            return SkillResult(
                success=True,
                content=best['result_dict'].get('content'),
                used_skill=best_tool,
                response_time=best['response_time'],
                metadata={'mode': 'full', 'all_results': results}
            )
        else:
            return SkillResult(success=False, error="所有工具执行失败")
    
    def _execute_single_tool(self, request: SkillRequest, tool_name: str) -> SkillResult:
        """默认模式：执行单个工具"""
        if not tool_name:
            return SkillResult(success=False, error=f"未找到 {request.category} 类别的默认工具")
        
        start_time = time.time()
        
        try:
            result_dict = self.call_skill(tool_name, request)
            response_time = (time.time() - start_time) * 1000
            
            success = result_dict.get('success', False)
            content = result_dict.get('content', '')
            quality_score = self._evaluate_result_quality(content) if success else 0
            
            self.mode_manager.record_performance(
                request.category, tool_name,
                success, response_time, quality_score
            )
            
            return SkillResult(
                success=success,
                content=content,
                used_skill=tool_name,
                response_time=response_time,
                metadata={'mode': 'default'}
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e), used_skill=tool_name)
    
    def _evaluate_result_quality(self, content: str) -> float:
        """评估结果质量 (0-1)"""
        if not content:
            return 0.0
        
        length = len(content)
        if 100 <= length <= 5000:
            length_score = 1.0
        elif length < 100:
            length_score = length / 100
        else:
            length_score = max(0.5, 5000 / length)
        
        has_text = any(c.isalnum() for c in content)
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in content)
        info_score = 0.5
        if has_text:
            info_score += 0.3
        if has_chinese:
            info_score += 0.2
        
        return min(1.0, length_score * 0.6 + info_score * 0.4)
    
    def call_skill(self, skill_name: str, request: SkillRequest) -> Dict:
        """
        调用具体技能
        
        设计原则：
        - 不自己实现调用逻辑
        - 根据技能类型选择合适的调用方式
        - 有脚本 → 执行脚本
        - 无脚本 → 通过 OpenClaw 通道调用
        """
        skill = self._load_skill(skill_name)
        
        if not skill:
            raise Exception(f"技能 {skill_name} 不存在")
        
        # 根据类别调用对应方法
        if request.category == "search":
            return skill.search(request.query)
        elif request.category == "fetch":
            return skill.fetch(request.url)
        elif request.category == "summarize":
            return skill.summarize(request.content)
        else:
            return skill.execute(request)
    
    def _load_skill(self, skill_name: str) -> Optional[Any]:
        """
        加载技能实例
        
        优先级：
        1. 有 Python 模块 (scripts/main.py) → 导入
        2. 有脚本文件 (scripts/search.py/mjs/js/sh) → SkillExecutor
        3. 无脚本 → OpenClawCaller (通过 OpenClaw 通道)
        """
        if skill_name in self.skill_cache:
            return self.skill_cache[skill_name]
        
        try:
            # 1. 尝试导入 Python 模块
            skill_path = f"skills.{skill_name.replace('-', '_')}.scripts.main"
            module = importlib.import_module(skill_path)
            
            if hasattr(module, 'Skill'):
                skill = module.Skill()
                self.skill_cache[skill_name] = skill
                return skill
            else:
                raise Exception(f"技能 {skill_name} 未定义 Skill 类")
                
        except ImportError:
            # 2. 检查是否有脚本文件
            skill_dir = os.path.expanduser(f"~/.openclaw/workspace/skills/{skill_name}")
            has_script = any([
                os.path.exists(os.path.join(skill_dir, 'scripts', 'search.py')),
                os.path.exists(os.path.join(skill_dir, 'scripts', 'search.mjs')),
                os.path.exists(os.path.join(skill_dir, 'scripts', 'search.js')),
                os.path.exists(os.path.join(skill_dir, 'scripts', 'search.sh')),
            ])
            
            if has_script:
                # 有脚本文件，使用 SkillExecutor
                print(f"  ⚠ 技能 {skill_name} 无 Python 模块，通过 exec 调用脚本")
                return SkillExecutor(skill_name)
            else:
                # 3. 无脚本，通过 OpenClawCaller 调用
                print(f"  ⚠ 技能 {skill_name} 无脚本，通过 OpenClaw 通道调用")
                return OpenClawCaller(skill_name)
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "skills": self.registry.get_status(),
            "circuits": self.fallback.get_circuit_status(),
            "total_skills": len(self.registry.skills),
            "categories": list(self.registry.categories.keys())
        }
    
    def discover_skills(self) -> int:
        """重新发现技能"""
        self.skill_cache.clear()
        count = self.registry.auto_discover()
        self.registry.save_state()
        return count


class SkillExecutor:
    """
    技能执行器 - 用于有脚本文件的技能
    
    设计原则：
    - 直接执行技能脚本
    - 传递环境变量 (如 TAVILY_API_KEY)
    - 验证输入参数安全
    """
    
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.skill_dir = os.path.expanduser(f"~/.openclaw/workspace/skills/{skill_name}")
    
    def _validate_args(self, args: list) -> bool:
        """验证参数安全性"""
        if not args:
            return True
        
        dangerous_chars = [';', '|', '&', '$', '`', '(', ')', '{', '}', '<', '>', '\n', '\r', '\\']
        for arg in args:
            if not isinstance(arg, str):
                return False
            if len(arg) > 1000:
                return False
            for char in dangerous_chars:
                if char in arg:
                    return False
        return True
    
    def _run_script(self, script_name: str, args: list = None, timeout: int = 30) -> Dict:
        """执行技能脚本"""
        import subprocess
        import json
        import os
        
        # 安全验证
        if args and not self._validate_args(args):
            return {
                "success": False,
                "error": "参数包含不安全字符，已拒绝执行",
                "metadata": {"skill": self.skill_name, "security": "input_validation_failed"}
            }
        
        # 查找脚本
        script_paths = [
            os.path.join(self.skill_dir, 'scripts', f'{script_name}.py'),
            os.path.join(self.skill_dir, 'scripts', f'{script_name}.mjs'),
            os.path.join(self.skill_dir, 'scripts', f'{script_name}.js'),
            os.path.join(self.skill_dir, 'scripts', f'{script_name}.sh'),
        ]
        
        for script_path in script_paths:
            if os.path.exists(script_path):
                try:
                    if script_path.endswith('.py'):
                        cmd = ['python3', script_path] + (args or [])
                    elif script_path.endswith('.mjs') or script_path.endswith('.js'):
                        cmd = ['node', script_path] + (args or [])
                    elif script_path.endswith('.sh'):
                        cmd = ['bash', script_path] + (args or [])
                    else:
                        continue
                    
                    # 执行脚本，继承环境变量
                    env = os.environ.copy()
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        env=env
                    )
                    
                    if result.returncode == 0:
                        try:
                            return json.loads(result.stdout)
                        except json.JSONDecodeError:
                            # 非 JSON 输出，包装为标准格式
                            return {
                                "success": True,
                                "content": result.stdout.strip(),
                                "metadata": {
                                    "skill": self.skill_name,
                                    "script": script_name,
                                    "output_format": "text",
                                }
                            }
                    else:
                        return {
                            "success": False,
                            "error": result.stderr.strip(),
                            "metadata": {"skill": self.skill_name, "script": script_name}
                        }
                        
                except subprocess.TimeoutExpired:
                    return {
                        "success": False,
                        "error": f"脚本执行超时 ({timeout}秒)",
                        "metadata": {"skill": self.skill_name, "script": script_name}
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "metadata": {"skill": self.skill_name, "script": script_name}
                    }
        
        return {
            "success": False,
            "error": f"未找到技能 {self.skill_name} 的脚本文件",
            "metadata": {"skill": self.skill_name}
        }
    
    def search(self, query: str) -> Dict:
        return self._run_script('search', [query])
    
    def fetch(self, url: str) -> Dict:
        return self._run_script('fetch', [url])
    
    def summarize(self, content: str) -> Dict:
        return self._run_script('summarize', [content])
    
    def execute(self, request: Any = None) -> Dict:
        return self._run_script('execute')


class OpenClawCaller:
    """
    OpenClaw 通道调用器 - 用于无脚本的技能
    
    设计原则：
    - 不自己实现调用逻辑
    - 通过 OpenClaw 现有工具/通道调用
    - 对于 search 类技能，使用 OpenClaw 的 web_search 或 browser 工具
    - 对于 fetch 类技能，使用 OpenClaw 的 web_fetch 工具
    """
    
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
    
    def search(self, query: str) -> Dict:
        """
        搜索 - 通过 OpenClaw 工具调用
        
        对于 multi-search-engine 等技能：
        - 使用 OpenClaw 的 web_search 工具 (如果可用)
        - 或使用 browser 工具抓取搜索引擎页面
        """
        # 根据技能类型选择合适的 OpenClaw 工具
        if self.skill_name == 'multi-search-engine':
            # 使用 OpenClaw 的 web_search 工具
            return self._call_openclaw_web_search(query)
        
        elif self.skill_name == 'exa-web-search-free':
            # 使用 mcporter 调用 Exa MCP
            return self._call_mcporter_exa(query)
        
        else:
            # 默认：使用 web_search 工具
            return self._call_openclaw_web_search(query)
    
    def _call_openclaw_web_search(self, query: str) -> Dict:
        """
        调用 OpenClaw web_search 工具
        
        注意：这需要 OpenClaw Gateway 配置了 web_search 工具
        """
        import subprocess
        import os
        
        try:
            # 通过 openclaw agent 命令调用 web_search
            # 这是一种通用的方式，适用于所有 OpenClaw 工具
            cmd = [
                'openclaw', 'agent',
                '--message', f'使用 web_search 工具搜索：{query}',
                '--timeout', '30',
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env=os.environ.copy()
            )
            
            output = result.stdout.strip()
            error_output = result.stderr.strip()
            
            # 检查是否有实际内容返回
            has_content = output and len(output) > 50  # 至少有一些内容
            has_error = error_output and ('Error' in error_output or 'failed' in error_output.lower())
            
            if result.returncode == 0 and has_content and not has_error:
                return {
                    "success": True,
                    "content": output[:2000],
                    "metadata": {"skill": self.skill_name, "source": "openclaw_web_search"}
                }
            else:
                error_msg = error_output if error_output else '无输出'
                if not has_content:
                    error_msg = 'web_search 返回空结果 (可能需要配置 API Key)'
                return {
                    "success": False,
                    "error": f"web_search 调用失败：{error_msg}",
                    "metadata": {"skill": self.skill_name}
                }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "OpenClaw CLI 未找到",
                "metadata": {"skill": self.skill_name}
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "搜索超时 (30 秒)",
                "metadata": {"skill": self.skill_name}
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"web_search 调用失败：{str(e)}",
                "metadata": {"skill": self.skill_name}
            }
    
    def _call_mcporter_exa(self, query: str) -> Dict:
        """调用 mcporter exa 工具"""
        import subprocess
        import os
        
        try:
            safe_query = query.replace('"', '').replace("'", '')[:500]
            cmd = [
                'mcporter', 'call',
                f'exa.web_search_exa(query: "{safe_query}", numResults: 5)'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env=os.environ.copy()
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "content": result.stdout.strip(),
                    "metadata": {"skill": self.skill_name, "source": "exa"}
                }
            else:
                return {
                    "success": False,
                    "error": f"mcporter 调用失败：{result.stderr.strip()}",
                    "metadata": {"skill": self.skill_name}
                }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "mcporter 未找到",
                "metadata": {"skill": self.skill_name}
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"exa 调用失败：{str(e)}",
                "metadata": {"skill": self.skill_name}
            }
    
    def fetch(self, url: str) -> Dict:
        """抓取 - 通过 OpenClaw web_fetch 工具"""
        import subprocess
        import os
        
        try:
            cmd = ['web_fetch', url, '--max-chars', '5000']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env=os.environ.copy()
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return {
                    "success": True,
                    "content": result.stdout.strip()[:2000],
                    "metadata": {"skill": self.skill_name, "source": "web_fetch"}
                }
            else:
                return {
                    "success": False,
                    "error": f"web_fetch 失败：{result.stderr.strip() or '无输出'}",
                    "metadata": {"skill": self.skill_name}
                }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "web_fetch 工具未找到",
                "metadata": {"skill": self.skill_name}
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"web_fetch 失败：{str(e)}",
                "metadata": {"skill": self.skill_name}
            }
    
    def summarize(self, content: str) -> Dict:
        """总结 - 通过 OpenClaw summarize 工具"""
        # 对于 summarize，通常需要调用外部 API
        # 这里返回提示，让用户配置相应的工具
        return {
            "success": False,
            "error": f"技能 {self.skill_name} 需要配置 summarize 工具",
            "metadata": {"skill": self.skill_name, "hint": "配置 summarize CLI 或使用其他总结工具"}
        }
    
    def execute(self, request: Any = None) -> Dict:
        """通用执行"""
        return {
            "success": False,
            "error": f"技能 {self.skill_name} 不支持 execute 调用",
            "metadata": {"skill": self.skill_name}
        }
