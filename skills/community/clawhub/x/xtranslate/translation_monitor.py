#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""翻译过程监控记录器"""

import json
import time
import os
from datetime import datetime
from pathlib import Path

class TranslationMonitor:
    def __init__(self, log_file="translation_monitor.json"):
        self.log_file = Path(log_file)
        self.records = []
        self.load_records()
        
    def load_records(self):
        """加载历史记录"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
                print(f"[监控] 已加载 {len(self.records)} 条历史记录")
            except Exception as e:
                print(f"[监控] 加载记录失败: {e}")
                self.records = []
        else:
            print("[监控] 创建新的监控记录文件")
            
    def save_records(self):
        """保存记录到文件"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[监控] 保存记录失败: {e}")
            
    def start_translation(self, file_path, engine, target_lang):
        """开始翻译时记录"""
        record = {
            "id": len(self.records) + 1,
            "timestamp": datetime.now().isoformat(),
            "file_path": str(file_path),
            "engine": engine,
            "target_lang": target_lang,
            "status": "started",
            "start_time": time.time(),
            "phases": {}
        }
        return record
        
    def record_phase(self, record, phase_name, details=None):
        """记录翻译阶段"""
        if "phases" not in record:
            record["phases"] = {}
            
        record["phases"][phase_name] = {
            "start_time": time.time(),
            "details": details or {}
        }
        
    def end_phase(self, record, phase_name, success=True, error_msg=None):
        """结束翻译阶段"""
        if phase_name in record["phases"]:
            phase = record["phases"][phase_name]
            phase["end_time"] = time.time()
            phase["duration"] = phase["end_time"] - phase["start_time"]
            phase["success"] = success
            if error_msg:
                phase["error"] = error_msg
                
    def finish_translation(self, record, success=True, result_stats=None, error_msg=None):
        """完成翻译记录"""
        record["end_time"] = time.time()
        record["duration"] = record["end_time"] - record["start_time"]
        record["status"] = "completed" if success else "failed"
        record["success"] = success
        
        if result_stats:
            record["result_stats"] = result_stats
            
        if error_msg:
            record["error"] = error_msg
            
        # 添加到记录并保存
        self.records.append(record)
        self.save_records()
        
        print(f"[监控] 翻译记录已保存 (ID: {record['id']})")
        
        # 检查是否需要总结
        if len(self.records) % 10 == 0:
            self.generate_summary()
            
    def generate_summary(self):
        """生成10次翻译总结"""
        if len(self.records) < 10:
            return
            
        # 获取最近10次记录
        recent_records = self.records[-10:]
        
        print("\n" + "="*60)
        print("翻译性能总结报告 (最近10次)")
        print("="*60)
        
        # 基本统计
        total_count = len(recent_records)
        successful_count = len([r for r in recent_records if r.get("success", False)])
        failed_count = total_count - successful_count
        
        print(f"\n📊 基本统计:")
        print(f"  总翻译次数: {total_count}")
        print(f"  成功次数: {successful_count}")
        print(f"  失败次数: {failed_count}")
        print(f"  成功率: {successful_count/total_count*100:.1f}%")
        
        # 时间统计
        durations = [r["duration"] for r in recent_records if "duration" in r]
        if durations:
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            print(f"\n⏱️  时间统计:")
            print(f"  平均耗时: {avg_duration:.1f}秒")
            print(f"  最短耗时: {min_duration:.1f}秒")
            print(f"  最长耗时: {max_duration:.1f}秒")
        
        # 引擎使用统计
        engines = {}
        for record in recent_records:
            engine = record.get("engine", "unknown")
            engines[engine] = engines.get(engine, 0) + 1
            
        print(f"\n⚙️  引擎使用:")
        for engine, count in engines.items():
            print(f"  {engine}: {count}次 ({count/total_count*100:.1f}%)")
        
        # 错误分析
        errors = []
        for record in recent_records:
            if not record.get("success", False) and "error" in record:
                errors.append(record["error"])
                
        if errors:
            print(f"\n❌ 错误分析:")
            error_types = {}
            for error in errors:
                # 简化错误类型
                if "API" in error or "key" in error.lower():
                    error_type = "API密钥问题"
                elif "timeout" in error.lower() or "time" in error.lower():
                    error_type = "超时问题"
                elif "memory" in error.lower() or "token" in error.lower():
                    error_type = "内存/token限制"
                else:
                    error_type = "其他错误"
                    
                error_types[error_type] = error_types.get(error_type, 0) + 1
                
            for error_type, count in error_types.items():
                print(f"  {error_type}: {count}次")
        
        # 性能建议
        print(f"\n💡 改进建议:")
        if successful_count/total_count < 0.8:
            print("  • 翻译成功率较低，建议检查网络连接和API密钥")
        
        if durations and avg_duration > 30:
            print("  • 平均翻译时间较长，可考虑:")
            print("    - 减少单次批次大小")
            print("    - 优化网络连接")
            print("    - 选择响应更快的模型")
            
        if "cloud" in engines and engines["cloud"] > 7:
            print("  • 过度依赖云模型，可适当使用本地模型分担负载")
            
        print("="*60)
        
        # 保存总结到单独文件
        summary_file = f"translation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.save_summary_to_file(summary_file, recent_records)
        
    def save_summary_to_file(self, filename, records):
        """将总结保存到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("翻译性能总结报告\n")
                f.write("="*50 + "\n\n")
                
                total_count = len(records)
                successful_count = len([r for r in records if r.get("success", False)])
                
                f.write(f"统计周期: 最近{total_count}次翻译\n")
                f.write(f"时间范围: {records[0]['timestamp']} 至 {records[-1]['timestamp']}\n\n")
                
                f.write(f"成功率: {successful_count/total_count*100:.1f}% ({successful_count}/{total_count})\n")
                
                durations = [r["duration"] for r in records if "duration" in r]
                if durations:
                    avg_duration = sum(durations) / len(durations)
                    f.write(f"平均耗时: {avg_duration:.1f}秒\n")
                    
        except Exception as e:
            print(f"[监控] 保存总结文件失败: {e}")

# 全局监控实例
monitor = TranslationMonitor()

def demo_usage():
    """演示如何使用监控器"""
    print("=== 翻译监控器使用演示 ===\n")
    
    # 模拟几次翻译过程
    test_files = [
        ("test1.docx", "cloud", "zh-CN"),
        ("test2.pdf", "ollama", "English"),
        ("test3.docx", "cloud", "Japanese")
    ]
    
    for i, (file_path, engine, target_lang) in enumerate(test_files, 1):
        print(f"模拟第{i}次翻译...")
        
        # 开始翻译
        record = monitor.start_translation(file_path, engine, target_lang)
        
        # 记录各个阶段
        monitor.record_phase(record, "文件解析")
        time.sleep(0.1)  # 模拟处理时间
        monitor.end_phase(record, "文件解析", success=True)
        
        monitor.record_phase(record, "AI翻译")
        time.sleep(0.2)  # 模拟处理时间
        monitor.end_phase(record, "AI翻译", success=True)
        
        monitor.record_phase(record, "格式恢复")
        time.sleep(0.05)  # 模拟处理时间
        monitor.end_phase(record, "格式恢复", success=True)
        
        # 完成翻译
        stats = {
            "total_segments": 50,
            "translated_segments": 50,
            "characters_processed": 2500
        }
        
        monitor.finish_translation(record, success=True, result_stats=stats)
        
        print(f"第{i}次翻译完成\n")
        
        # 模拟一次失败
        if i == 2:
            print("模拟一次失败的翻译...")
            failed_record = monitor.start_translation("failed.docx", "cloud", "zh-CN")
            monitor.record_phase(failed_record, "AI翻译")
            time.sleep(0.1)
            monitor.end_phase(failed_record, "AI翻译", success=False, error_msg="API timeout")
            monitor.finish_translation(failed_record, success=False, error_msg="API timeout")
            print("失败翻译记录完成\n")

if __name__ == "__main__":
    demo_usage()