#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
走访管理数据管理模块
负责读取和写入Excel数据
"""

import pandas as pd
import os
from datetime import datetime

class DataManager:
    """走访管理数据管理类"""
    
    def __init__(self, excel_path="/Users/mac/美兰中心C+服务.xlsx"):
        """初始化"""
        self.excel_path = excel_path
        
    def read_customer_data(self):
        """读取客户数据"""
        try:
            # 读取客户信息表
            df = pd.read_excel(self.excel_path, sheet_name='客户信息')
            return df
        except Exception as e:
            print(f"读取客户数据失败: {e}")
            return pd.DataFrame()
    
    def read_visit_history(self):
        """读取走访历史记录"""
        try:
            # 读取走访记录表
            df = pd.read_excel(self.excel_path, sheet_name='走访记录')
            
            # 数据清洗和转换
            df['走访日期'] = pd.to_datetime(df['走访日期']).dt.date
            df['开始时间'] = pd.to_datetime(df['开始时间'], errors='coerce').dt.date
            df['结束时间'] = pd.to_datetime(df['结束时间'], errors='coerce').dt.date
            
            return df
        except Exception as e:
            print(f"读取走访历史失败: {e}")
            return pd.DataFrame()
    
    def read_visit_plan(self):
        """读取走访计划"""
        try:
            # 读取走访计划表
            df = pd.read_excel(self.excel_path, sheet_name='走访计划')
            
            # 数据清洗和转换
            df['计划日期'] = pd.to_datetime(df['计划日期']).dt.date
            df['实际走访日期'] = pd.to_datetime(df['实际走访日期'], errors='coerce').dt.date
            
            return df
        except Exception as e:
            print(f"读取走访计划失败: {e}")
            return pd.DataFrame()
    
    def save_visit_history(self, visit_data):
        """保存走访历史记录"""
        try:
            # 写入Excel
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                visit_data.to_excel(writer, sheet_name='走访记录', index=False)
            
            print("走访历史记录已保存")
            return True
        except Exception as e:
            print(f"保存走访历史失败: {e}")
            return False
    
    def save_visit_plan(self, plan_data):
        """保存走访计划"""
        try:
            # 写入Excel
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                plan_data.to_excel(writer, sheet_name='走访计划', index=False)
            
            print("走访计划已保存")
            return True
        except Exception as e:
            print(f"保存走访计划失败: {e}")
            return False
    
    def add_visit_record(self, visit_record):
        """添加走访记录"""
        try:
            # 读取现有记录
            if os.path.exists(self.excel_path):
                df = pd.read_excel(self.excel_path, sheet_name='走访记录')
            else:
                df = pd.DataFrame(columns=[
                    '走访ID', '客户ID', '客户名称', '房号', '走访日期', 
                    '走访人员', '走访目的', '走访内容', '走访结果', 
                    '状态', '开始时间', '结束时间', '满意度评分'
                ])
            
            # 添加新记录
            new_record = pd.DataFrame([visit_record])
            df = pd.concat([df, new_record], ignore_index=True)
            
            # 保存
            self.save_visit_history(df)
            
            print(f"走访记录已添加: {visit_record.get('走访ID', '')}")
            return True
        except Exception as e:
            print(f"添加走访记录失败: {e}")
            return False
    
    def update_visit_status(self, visit_id, status, **kwargs):
        """更新走访状态"""
        try:
            # 读取现有记录
            df = pd.read_excel(self.excel_path, sheet_name='走访记录')
            
            # 找到对应记录
            idx = df[df['走访ID'] == visit_id].index
            if len(idx) > 0:
                # 更新状态
                df.loc[idx[0], '状态'] = status
                
                # 更新其他字段
                for key, value in kwargs.items():
                    if key in df.columns:
                        df.loc[idx[0], key] = value
                
                # 保存
                self.save_visit_history(df)
                
                print(f"走访ID {visit_id} 状态更新为: {status}")
                return True
            else:
                print(f"未找到走访ID: {visit_id}")
                return False
        except Exception as e:
            print(f"更新走访状态失败: {e}")
            return False
    
    def get_visits_by_date_range(self, start_date, end_date):
        """按日期范围获取走访记录"""
        try:
            df = self.read_visit_history()
            
            if df.empty:
                return pd.DataFrame()
            
            # 筛选日期范围
            mask = (df['走访日期'] >= start_date) & (df['走访日期'] <= end_date)
            return df[mask]
        except Exception as e:
            print(f"按日期范围获取走访记录失败: {e}")
            return pd.DataFrame()
    
    def get_customer_visit_stats(self, customer_id):
        """获取客户走访统计"""
        try:
            df = self.read_visit_history()
            
            if df.empty:
                return {}
            
            # 筛选客户记录
            customer_visits = df[df['客户ID'] == customer_id]
            
            if customer_visits.empty:
                return {
                    'total_visits': 0,
                    'last_visit_date': None,
                    'avg_satisfaction': 0
                }
            
            # 计算统计信息
            total_visits = len(customer_visits)
            last_visit_date = customer_visits['走访日期'].max()
            
            # 计算平均满意度
            satisfaction_scores = customer_visits['满意度评分'].dropna()
            avg_satisfaction = satisfaction_scores.mean() if not satisfaction_scores.empty else 0
            
            return {
                'total_visits': total_visits,
                'last_visit_date': last_visit_date,
                'avg_satisfaction': round(avg_satisfaction, 2)
            }
        except Exception as e:
            print(f"获取客户走访统计失败: {e}")
            return {}
    
    def backup_excel(self):
        """备份Excel文件"""
        try:
            backup_dir = "/Users/mac/.qclaw/skills/visit-management/backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f"美兰中心C+服务_{timestamp}.xlsx")
            
            # 复制文件
            import shutil
            shutil.copy2(self.excel_path, backup_path)
            
            print(f"Excel文件已备份: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"备份失败: {e}")
            return None