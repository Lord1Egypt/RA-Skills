#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主调度程序 - 集成module1和module2的完整工作流
使用新的module2_summarize.py进行话题归纳
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import traceback

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class MainScheduler:
    """主调度程序"""
    
    def __init__(self):
        """初始化调度程序"""
        self.name = "财经热点新闻爬取与话题归纳系统"
        self.version = "3.0"
        
        # 加载配置文件
        self.config = self.load_config()
        if self.config:
            system_settings = self.config.get('system_settings', {})
            # 报告目录 - 使用reports_dir
            report_dir_str = system_settings.get('reports_dir', 'c:/SelfData/claw_temp/reports')
            self.report_dir = Path(report_dir_str)
            # 临时目录 - 使用temp_dir
            temp_dir_str = system_settings.get('temp_dir', 'c:/SelfData/claw_temp/temp')
            self.temp_dir = Path(temp_dir_str)
            # 日志目录 - 放在reports_dir下的logs子目录
            self.log_dir = self.report_dir / "logs"
            print(f"[INFO] 从配置文件加载路径成功")
        else:
            # 默认路径
            self.report_dir = Path("c:/SelfData/claw_temp/reports")
            self.temp_dir = Path("c:/SelfData/claw_temp/temp")
            self.log_dir = self.report_dir / "logs"
            print(f"[WARNING] 配置文件加载失败，使用默认路径")
        
        # 创建目录
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 日志文件
        self.log_file = self.log_dir / f"main_scheduler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        print(f"{self.name} v{self.version}")
        print("=" * 70)
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"报告目录: {self.report_dir}")
        print(f"临时目录: {self.temp_dir}")
        print(f"日志文件: {self.log_file}")
        print("=" * 70)
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        try:
            config_path = Path(__file__).parent / "url_config.json"
            if not config_path.exists():
                print(f"[WARNING] 配置文件不存在: {config_path}")
                return None
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"[INFO] 配置文件加载成功")
            return config
            
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            return None
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        
        # 打印到控制台
        print(log_message)
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    
    def check_dependencies(self) -> bool:
        """检查依赖"""
        self.log("检查系统依赖...")
        
        required_files = [
            "module1_main_sites.py",
            "module2_summarize_filtered.py",  # 使用过滤版
            "module3_news_flash.py",          # 重命名为新闻快讯模块
            "module4_report_generator.py",
            "jrj_hot_news.py",
            "stcn_hot_news.py",
            "cls_hot_news.py"
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            self.log(f"[ERROR] 缺少必要文件: {', '.join(missing_files)}", "ERROR")
            return False
        
        self.log("所有依赖文件检查通过")
        return True
    
    def run_module1(self) -> Tuple[bool, Dict[str, Any]]:
        """运行module1: 主力网站爬取"""
        self.log("=" * 50)
        self.log("开始执行 Module 1: 主力网站热点新闻爬取")
        self.log("=" * 50)
        
        try:
            # 动态导入module1
            import module1_main_sites as module1
            
            # 创建爬取模块实例
            crawler = module1.MainSitesCrawler()
            
            # 运行爬取
            start_time = time.time()
            articles = crawler.run()
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            if articles and isinstance(articles, list) and len(articles) > 0:
                self.log(f"Module 1 执行成功!")
                self.log(f"爬取结果: {len(articles)} 篇文章 (48小时内)")
                self.log(f"执行时间: {execution_time:.2f} 秒")
                
                # 获取输出目录信息 - Module 1输出到temp_dir/title_news_crawl
                output_dir = self.temp_dir / "title_news_crawl"
                
                result = {
                    'success': True,
                    'article_count': len(articles),
                    'execution_time': execution_time,
                    'metadata': {
                        'output_dir': output_dir,
                        'site_count': 3,  # CLS, JRJ, STCN
                        'time_filter': '48小时'
                    },
                    'articles_sample': articles[:3] if articles else []  # 只保存前3篇作为示例
                }
                return True, result
            else:
                self.log("[WARNING] Module 1 未爬取到文章", "WARNING")
                return False, {'error': '未爬取到文章', 'execution_time': execution_time}
                
        except Exception as e:
            self.log(f"[ERROR] Module 1 执行失败: {type(e).__name__}: {e}", "ERROR")
            traceback.print_exc()
            return False, {'error': str(e)}
    
    def run_module2(self) -> Tuple[bool, Dict[str, Any]]:
        """运行module2: 热点新闻话题归纳（过滤版）"""
        self.log("=" * 50)
        self.log("开始执行 Module 2: 热点新闻话题归纳（过滤版）")
        self.log("=" * 50)
        
        try:
            # 动态导入module2（使用过滤版）
            import module2_summarize_filtered as module2
            
            # 创建话题归纳器实例
            summarizer = module2.TopicSummarizerFiltered()
            
            # 运行话题归纳
            start_time = time.time()
            all_topics, top_topics = summarizer.run(top_n=5)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            if all_topics:
                self.log(f"Module 2 执行成功!")
                self.log(f"归纳结果: {len(all_topics)} 个话题")
                self.log(f"前5名热点话题: {len(top_topics)} 个")
                self.log(f"执行时间: {execution_time:.2f} 秒")
                self.log(f"输出目录: {summarizer.output_dir}")
                
                result = {
                    'success': True,
                    'topic_count': len(all_topics),
                    'top_topic_count': len(top_topics),
                    'execution_time': execution_time,
                    'top_topics_sample': top_topics[:3] if top_topics else []  # 只保存前3个作为示例
                }
                return True, result
            else:
                self.log("[WARNING] Module 2 未归纳出话题", "WARNING")
                return False, {'error': '未归纳出话题'}
                
        except Exception as e:
            self.log(f"[ERROR] Module 2 执行失败: {type(e).__name__}: {e}", "ERROR")
            traceback.print_exc()
            return False, {'error': str(e)}
    
    def run_module3(self, mode: str = "playwright") -> Tuple[bool, Dict[str, Any]]:
        """运行module3: 华尔街见闻快讯采集（只支持playwright模式）"""
        self.log("=" * 50)
        self.log(f"开始执行 Module 3: 华尔街见闻快讯采集 (模式: {mode})")
        self.log("=" * 50)
        
        try:
            # 动态导入module3（新闻快讯模块）
            import module3_news_flash as module3
            
            # 创建快讯采集器实例
            crawler = module3.WallStreetCrawler()
            
            # 运行快讯采集
            start_time = time.time()
            articles = crawler.run(mode=mode)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            if articles and isinstance(articles, list) and len(articles) > 0:
                self.log(f"Module 3 执行成功!")
                self.log(f"采集结果: {len(articles)} 条快讯")
                self.log(f"重要快讯: {sum(1 for a in articles if a.get('importance', False))} 条")
                self.log(f"执行时间: {execution_time:.2f} 秒")
                self.log(f"输出目录: {crawler.output_dir}")
                
                result = {
                    'success': True,
                    'article_count': len(articles),
                    'important_count': sum(1 for a in articles if a.get('importance', False)),
                    'execution_time': execution_time,
                    'mode': mode,
                    'metadata': {
                        'output_dir': str(crawler.output_dir),
                        'source': '华尔街见闻',
                        'url': 'https://wallstreetcn.com/live/global'
                    },
                    'articles_sample': articles[:5] if articles else []  # 只保存前5条作为示例
                }
                return True, result
            else:
                self.log("[WARNING] Module 3 未采集到快讯", "WARNING")
                return False, {'error': '未采集到快讯', 'execution_time': execution_time, 'mode': mode}
                
        except Exception as e:
            self.log(f"[ERROR] Module 3 执行失败: {type(e).__name__}: {e}", "ERROR")
            traceback.print_exc()
            return False, {'error': str(e), 'mode': mode}
    
    def run_module4(self) -> Tuple[bool, Dict[str, Any]]:
        """运行module4: 综合报告生成"""
        self.log("=" * 50)
        self.log("开始执行 Module 4: 综合报告生成")
        self.log("=" * 50)
        
        try:
            # 动态导入module4
            import module4_report_generator as module4
            
            # 创建报告生成器实例
            generator = module4.FinalReportGenerator()
            
            # 运行报告生成
            start_time = time.time()
            success = generator.run()
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            if success:
                self.log(f"Module 4 执行成功!")
                self.log(f"执行时间: {execution_time:.2f} 秒")
                self.log(f"输出目录: {generator.output_dir}")
                
                # 查找最新生成的文件
                output_dir = generator.output_dir
                txt_files = list(output_dir.glob("finance_report_*.txt"))
                html_files = list(output_dir.glob("finance_report_*.html"))
                
                latest_txt = max(txt_files, key=lambda f: f.stat().st_mtime) if txt_files else None
                latest_html = max(html_files, key=lambda f: f.stat().st_mtime) if html_files else None
                
                result = {
                    'success': True,
                    'execution_time': execution_time,
                    'metadata': {
                        'output_dir': str(output_dir),
                        'txt_report': str(latest_txt) if latest_txt else None,
                        'html_report': str(latest_html) if latest_html else None,
                        'report_type': '综合报告'
                    },
                    'files_generated': {
                        'txt': bool(latest_txt),
                        'html': bool(latest_html)
                    }
                }
                return True, result
            else:
                self.log("[WARNING] Module 4 报告生成失败", "WARNING")
                return False, {'error': '报告生成失败', 'execution_time': execution_time}
                
        except Exception as e:
            self.log(f"[ERROR] Module 4 执行失败: {type(e).__name__}: {e}", "ERROR")
            traceback.print_exc()
            return False, {'error': str(e)}
    
    def generate_report(self, module1_result: Dict[str, Any], module2_result: Dict[str, Any], 
                       module3_result: Dict[str, Any], module4_result: Dict[str, Any]) -> Path:
        """生成执行报告"""
        self.log("生成执行报告...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.report_dir / f"main_sites_report_{timestamp}.json"
        
        # 计算总执行时间（包含Module 4）
        total_execution_time = (
            module1_result.get('execution_time', 0) + 
            module2_result.get('execution_time', 0) + 
            module3_result.get('execution_time', 0) +
            module4_result.get('execution_time', 0)
        )
        
        # 判断总体状态（包含Module 4）
        module1_success = module1_result.get('success', False)
        module2_success = module2_result.get('success', False)
        module3_success = module3_result.get('success', False)
        module4_success = module4_result.get('success', False)
        
        if module1_success and module2_success and module3_success and module4_success:
            overall_status = 'SUCCESS'
        elif module1_success or module2_success or module3_success or module4_success:
            overall_status = 'PARTIAL_SUCCESS'
        else:
            overall_status = 'FAILED'
        
        report_data = {
            'system': {
                'name': self.name,
                'version': self.version,
                'execution_time': datetime.now().isoformat(),
                'total_execution_time': total_execution_time
            },
            'module1': module1_result,
            'module2': module2_result,
            'module3': module3_result,
            'module4': module4_result,
            'summary': {
                'total_articles': module1_result.get('article_count', 0),
                'total_topics': module2_result.get('topic_count', 0),
                'total_newsflash': module3_result.get('article_count', 0),
                'important_newsflash': module3_result.get('important_count', 0),
                'module4_success': module4_success,
                'overall_status': overall_status
            }
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        self.log(f"JSON报告已保存: {report_file}")
        
        # 生成文本格式的报告
        txt_file = self.report_dir / f"main_sites_report_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"{self.name} v{self.version} - 执行报告\n")
            f.write("=" * 70 + "\n")
            f.write(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总执行时间: {report_data['system']['total_execution_time']:.2f} 秒\n")
            f.write(f"总体状态: {report_data['summary']['overall_status']}\n")
            f.write("\n" + "=" * 70 + "\n\n")
            
            # Module 1 结果
            f.write("Module 1: 主力网站热点新闻爬取\n")
            f.write("-" * 70 + "\n")
            if module1_result.get('success'):
                f.write(f"状态: [OK] 执行成功\n")
                f.write(f"爬取文章数: {module1_result.get('article_count', 0)} 篇\n")
                f.write(f"执行时间: {module1_result.get('execution_time', 0):.2f} 秒\n")
                
                metadata = module1_result.get('metadata', {})
                f.write(f"网站数量: {metadata.get('site_count', 0)} 个\n")
                f.write(f"输出目录: {metadata.get('output_dir', '未知')}\n")
                
                # 显示示例文章
                articles_sample = module1_result.get('articles_sample', [])
                if articles_sample:
                    f.write(f"\n示例文章:\n")
                    for i, article in enumerate(articles_sample, 1):
                        f.write(f"  {i}. [{article.get('source', '未知')}] {article.get('title', '')[:60]}...\n")
            else:
                f.write(f"状态: [FAILED] 执行失败\n")
                f.write(f"错误: {module1_result.get('error', '未知错误')}\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            
            # Module 2 结果
            f.write("Module 2: 热点新闻话题归纳\n")
            f.write("-" * 70 + "\n")
            if module2_result.get('success'):
                f.write(f"状态: [OK] 执行成功\n")
                f.write(f"归纳话题数: {module2_result.get('topic_count', 0)} 个\n")
                f.write(f"前5名热点话题: {module2_result.get('top_topic_count', 0)} 个\n")
                f.write(f"执行时间: {module2_result.get('execution_time', 0):.2f} 秒\n")
                
                # 显示示例话题
                topics_sample = module2_result.get('top_topics_sample', [])
                if topics_sample:
                    f.write(f"\n示例话题:\n")
                    for i, topic in enumerate(topics_sample, 1):
                        f.write(f"  {i}. {topic.get('topic', '未知')} - 评分: {topic.get('score', 0):.2f}\n")
                        f.write(f"     总结: {topic.get('summary', '')[:80]}...\n")
                        f.write(f"     文章数: {topic.get('article_count', 0)} 篇\n")
            else:
                f.write(f"状态: [FAILED] 执行失败\n")
                f.write(f"错误: {module2_result.get('error', '未知错误')}\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            
            # Module 3 结果
            f.write("Module 3: 华尔街见闻快讯采集\n")
            f.write("-" * 70 + "\n")
            if module3_result.get('success'):
                f.write(f"状态: [OK] 执行成功\n")
                f.write(f"采集模式: {module3_result.get('mode', 'single')}\n")
                f.write(f"快讯数量: {module3_result.get('article_count', 0)} 条\n")
                f.write(f"重要快讯: {module3_result.get('important_count', 0)} 条\n")
                f.write(f"执行时间: {module3_result.get('execution_time', 0):.2f} 秒\n")
                
                metadata = module3_result.get('metadata', {})
                f.write(f"来源: {metadata.get('source', '未知')}\n")
                f.write(f"URL: {metadata.get('url', '未知')}\n")
                f.write(f"输出目录: {metadata.get('output_dir', '未知')}\n")
                
                # 显示示例快讯
                articles_sample = module3_result.get('articles_sample', [])
                if articles_sample:
                    f.write(f"\n示例快讯:\n")
                    for i, article in enumerate(articles_sample, 1):
                        importance = "[重要] " if article.get('importance', False) else ""
                        f.write(f"  {i}. [{article.get('timestamp', '未知')}] {importance}{article.get('title', '')[:60]}...\n")
            else:
                f.write(f"状态: [FAILED] 执行失败\n")
                f.write(f"错误: {module3_result.get('error', '未知错误')}\n")
                f.write(f"采集模式: {module3_result.get('mode', 'single')}\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            
            # Module 4 结果
            f.write("Module 4: 综合报告生成\n")
            f.write("-" * 70 + "\n")
            if module4_result.get('success'):
                f.write(f"状态: [OK] 执行成功\n")
                f.write(f"执行时间: {module4_result.get('execution_time', 0):.2f} 秒\n")
                
                metadata = module4_result.get('metadata', {})
                f.write(f"输出目录: {metadata.get('output_dir', '未知')}\n")
                
                files_generated = module4_result.get('files_generated', {})
                if files_generated.get('txt'):
                    f.write(f"文本报告: {metadata.get('txt_report', '未知')}\n")
                if files_generated.get('html'):
                    f.write(f"HTML报告: {metadata.get('html_report', '未知')}\n")
                
                f.write(f"报告类型: {metadata.get('report_type', '未知')}\n")
            else:
                f.write(f"状态: [FAILED] 执行失败\n")
                f.write(f"错误: {module4_result.get('error', '未知错误')}\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            
            # 总结
            f.write("执行总结\n")
            f.write("-" * 70 + "\n")
            f.write(f"总文章数: {report_data['summary']['total_articles']} 篇\n")
            f.write(f"总话题数: {report_data['summary']['total_topics']} 个\n")
            f.write(f"快讯数量: {report_data['summary']['total_newsflash']} 条\n")
            f.write(f"重要快讯: {report_data['summary']['important_newsflash']} 条\n")
            f.write(f"Module 4状态: {'成功' if report_data['summary']['module4_success'] else '失败'}\n")
            f.write(f"系统状态: {report_data['summary']['overall_status']}\n")
            
            # 建议
            f.write("\n建议:\n")
            if report_data['summary']['overall_status'] == 'SUCCESS':
                f.write("  1. 系统运行正常，可以定期执行\n")
                f.write("  2. 查看详细结果请访问输出目录\n")
                f.write("  3. 最新热点话题已保存到临时文件\n")
            elif report_data['summary']['overall_status'] == 'PARTIAL_SUCCESS':
                f.write("  1. 系统部分模块执行失败，请检查日志\n")
                f.write("  2. 可能需要检查网络连接或API密钥\n")
                f.write("  3. 建议重新执行或手动调试\n")
            else:
                f.write("  1. 系统执行失败，请检查错误信息\n")
                f.write("  2. 查看日志文件获取详细错误信息\n")
                f.write("  3. 可能需要修复代码或配置\n")
        
        self.log(f"文本报告已保存: {txt_file}")
        
        return report_file
    
    def display_latest_results(self):
        """显示最新的热点话题结果"""
        self.log("查找最新的热点话题结果...")
        
        # 查找最新的top5热点话题文件
        output_dir = self.output_dir
        pattern = "top5_hot_topics_*.txt"
        files = list(output_dir.glob(pattern))
        
        if not files:
            self.log("未找到热点话题结果文件", "WARNING")
            return
        
        # 按修改时间排序，获取最新的文件
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        
        self.log(f"显示最新热点话题结果: {latest_file.name}")
        print("\n" + "=" * 70)
        print("最新热点话题结果:")
        print("=" * 70)
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
        except Exception as e:
            self.log(f"读取结果文件失败: {e}", "ERROR")
    
    def open_html_report(self, html_report_path: str) -> None:
        """打开HTML报告文件
        
        Args:
            html_report_path: HTML报告文件路径
        """
        try:
            if not html_report_path or not os.path.exists(html_report_path):
                self.log(f"[WARNING] HTML报告文件不存在或路径为空: {html_report_path}", "WARNING")
                return
            
            self.log(f"打开HTML报告: {html_report_path}")
            
            # 使用os.startfile打开HTML文件（Windows）
            # 如果os.startfile不可用（非Windows），则使用其他方法
            try:
                os.startfile(html_report_path)
                self.log("[OK] HTML报告已打开 (使用os.startfile)")
            except AttributeError:
                # 非Windows系统，使用其他方法
                import subprocess
                import platform
                
                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.Popen(["open", html_report_path])
                elif system == "Linux":  # Linux
                    subprocess.Popen(["xdg-open", html_report_path])
                else:  # 其他系统，尝试使用默认浏览器
                    import webbrowser
                    webbrowser.open(f"file://{html_report_path}")
                
                self.log(f"[OK] HTML报告已打开 (使用{system}兼容方法)")
            
        except Exception as e:
            self.log(f"[ERROR] 打开HTML报告失败: {e}", "ERROR")
    
    def cleanup_old_files(self, hours: int = 24) -> None:
        """清理指定小时前的临时文件
        
        Args:
            hours: 清理多少小时前的文件（默认24小时）
        """
        try:
            import shutil
            from datetime import datetime, timedelta
            
            self.log(f"开始清理{hours}小时前的临时文件...")
            
            # 计算时间阈值
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # 需要清理的目录 - 从配置文件读取
            temp_dirs = []
            
            if self.config:
                system_settings = self.config.get('system_settings', {})
                wallstreet_config = self.config.get('wallstreetcn_module', {})
                
                # temp_dir下的所有子目录
                temp_dir = system_settings.get('temp_dir', 'c:/SelfData/claw_temp/temp')
                temp_dirs.append(Path(temp_dir))
                
                # 报告输出目录（只清理旧报告，不清理最新报告）
                reports_dir = system_settings.get('reports_dir', 'c:/SelfData/claw_temp/reports')
                temp_dirs.append(Path(reports_dir))
                
                self.log(f"[INFO] 从配置文件加载清理目录")
            else:
                # 默认目录（兼容旧版本）
                temp_dirs = [
                    Path("c:/SelfData/claw_temp/temp"),
                    Path("c:/SelfData/claw_temp/reports"),
                ]
                self.log(f"[WARNING] 配置文件未加载，使用默认清理目录")
            
            deleted_count = 0
            total_size = 0
            
            for temp_dir in temp_dirs:
                if not temp_dir.exists():
                    continue
                
                # 遍历目录中的所有文件
                for file_path in temp_dir.rglob("*"):
                    if file_path.is_file():
                        try:
                            # 获取文件修改时间
                            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                            
                            # 如果文件早于阈值，则删除
                            if mtime < cutoff_time:
                                file_size = file_path.stat().st_size
                                total_size += file_size
                                deleted_count += 1
                                
                                self.log(f"删除旧文件: {file_path.name} ({file_size:,} bytes, 修改于: {mtime})", "INFO")
                                file_path.unlink()
                                
                        except Exception as e:
                            self.log(f"[WARNING] 无法处理文件 {file_path}: {e}", "WARNING")
            
            # 清理空目录
            for temp_dir in temp_dirs:
                if temp_dir.exists():
                    try:
                        # 删除空目录（只删除叶子目录）
                        for dir_path in sorted(temp_dir.rglob("*"), reverse=True):
                            if dir_path.is_dir() and not any(dir_path.iterdir()):
                                try:
                                    dir_path.rmdir()
                                    self.log(f"删除空目录: {dir_path}")
                                except:
                                    pass
                    except Exception as e:
                        self.log(f"[WARNING] 清理目录时出错: {e}", "WARNING")
            
            self.log(f"清理完成: 删除 {deleted_count} 个文件，释放 {total_size:,} bytes")
            
        except Exception as e:
            self.log(f"[ERROR] 清理临时文件失败: {e}", "ERROR")
    
    def run(self, module3_mode: str = "single") -> bool:
        """运行主调度程序"""
        self.log("开始执行主调度程序")
        
        # 1. 检查依赖
        if not self.check_dependencies():
            self.log("[ERROR] 依赖检查失败，无法继续", "ERROR")
            return False
        
        # 2. 运行Module 1
        module1_success, module1_result = self.run_module1()
        
        # 3. 运行Module 2
        module2_success, module2_result = self.run_module2()
        
        # 4. 运行Module 3
        module3_success, module3_result = self.run_module3(mode=module3_mode)
        
        # 5. 运行Module 4（综合报告生成）
        module4_success, module4_result = self.run_module4()
        
        # 5.1 自动操作：打开HTML报告并清理旧文件（如果Module 4成功）
        if module4_success:
            try:
                # 获取最新生成的HTML报告路径
                html_report_path = module4_result.get('metadata', {}).get('html_report')
                if html_report_path and os.path.exists(html_report_path):
                    self.log(f"找到HTML报告: {html_report_path}")
                    
                    # 自动打开HTML报告
                    self.open_html_report(html_report_path)
                    
                    # 自动清理24小时前的临时文件
                    self.cleanup_old_files(hours=24)
                else:
                    # 尝试在输出目录中查找最新的HTML报告
                    output_dir = module4_result.get('metadata', {}).get('output_dir')
                    if output_dir:
                        output_path = Path(output_dir)
                        html_files = list(output_path.glob("*.html"))
                        if html_files:
                            latest_html = max(html_files, key=lambda f: f.stat().st_mtime)
                            self.log(f"自动找到HTML报告: {latest_html}")
                            self.open_html_report(str(latest_html))
                            self.cleanup_old_files(hours=24)
                        else:
                            self.log("[WARNING] 未找到HTML报告文件", "WARNING")
            except Exception as e:
                self.log(f"[ERROR] 自动操作执行失败: {e}", "ERROR")
        
        # 6. 生成报告
        if module1_success or module2_success or module3_success or module4_success:
            report_file = self.generate_report(module1_result, module2_result, module3_result, module4_result)
            self.log(f"执行报告已生成: {report_file}")
        
        # 7. 显示最新结果
        if module2_success:
            self.display_latest_results()
        
        # 8. 总结
        overall_success = module1_success and module2_success and module3_success and module4_success
        
        print("\n" + "=" * 70)
        print("执行完成!")
        print("=" * 70)
        
        if overall_success:
            print("[SUCCESS] 所有模块执行成功!")
            print(f"  爬取文章: {module1_result.get('article_count', 0)} 篇")
            print(f"  归纳话题: {module2_result.get('topic_count', 0)} 个")
            print(f"  热点话题: {module2_result.get('top_topic_count', 0)} 个")
            print(f"  采集快讯: {module3_result.get('article_count', 0)} 条")
            print(f"  重要快讯: {module3_result.get('important_count', 0)} 条")
            print(f"  生成报告: Module 4 综合报告")
        elif module1_success or module2_success or module3_success or module4_success:
            print("[PARTIAL SUCCESS] 部分模块执行成功")
            if module1_success:
                print(f"  [OK] Module 1: 爬取 {module1_result.get('article_count', 0)} 篇文章")
            else:
                print(f"  [ERROR] Module 1: 失败")
            
            if module2_success:
                print(f"  [OK] Module 2: 归纳 {module2_result.get('topic_count', 0)} 个话题")
            else:
                print(f"  [ERROR] Module 2: 失败")
            
            if module3_success:
                print(f"  [OK] Module 3: 采集 {module3_result.get('article_count', 0)} 条快讯")
            else:
                print(f"  [ERROR] Module 3: 失败")
            
            if module4_success:
                print(f"  [OK] Module 4: 生成综合报告")
            else:
                print(f"  [ERROR] Module 4: 失败")
        else:
            print("[FAILED] 所有模块执行失败")
        
        total_time = (
            module1_result.get('execution_time', 0) + 
            module2_result.get('execution_time', 0) + 
            module3_result.get('execution_time', 0) +
            module4_result.get('execution_time', 0)
        )
        
        print(f"\n总执行时间: {total_time:.2f} 秒")
        print(f"详细报告请查看: {self.report_dir}")
        print(f"日志文件: {self.log_file}")
        print("=" * 70)
        
        return overall_success


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='财经热点新闻爬取与话题归纳系统')
    parser.add_argument('--module3-mode', type=str, default='playwright',
                       choices=['playwright'],
                       help='Module 3采集模式: playwright (Playwright抓取，支持scrapling后备)')
    
    args = parser.parse_args()
    
    try:
        print("财经热点新闻爬取与话题归纳系统")
        print("=" * 70)
        print("工作流程:")
        print("  1. Module 1: 爬取CLS、JRJ、STCN三个主力网站的热点新闻")
        print("  2. Module 2: 使用summarize对新闻话题进行归纳")
        print(f"  3. Module 3: 华尔街见闻快讯采集 (playwright模式，支持scrapling后备)")
        print("  4. Module 4: 生成综合报告 (头条新闻TOP5 + 深度分析TOP3 + 快讯TOP10)")
        print("  5. 输出: 热点话题、代表性文章、话题评分、实时快讯、综合报告")
        print("=" * 70)
        
        # 创建调度程序
        scheduler = MainScheduler()
        
        # 运行调度程序
        success = scheduler.run(module3_mode=args.module3_mode)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n[INFO] 用户中断")
        return 0
    except Exception as e:
        print(f"\n[ERROR] 执行出错: {type(e).__name__}: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)