#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供应商IQC质量分析脚本
功能：分析Excel数据结构、清洗数据、计算质量指标
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np


class IQCAnalyzer:
    """IQC质量分析器"""

    # 标准字段定义
    STANDARD_FIELDS = {
        'supplier_name': ['供应商名称', '供应商', '厂商', '供方名称', 'supplier'],
        'material_code': ['物料编码', '物料号', '零件号', '料号', 'material', 'part_no'],
        'batch_no': ['批次号', '批次', '批号', '送货单号', 'batch', 'lot_no'],
        'inspect_date': ['检验日期', '检验时间', '来料日期', 'inspect_date', 'date'],
        'quantity': ['来料数量', '来料数', '送检数量', 'quantity', 'qty'],
        'defect_qty': ['不良数量', '不良数', '缺陷数量', 'defect_qty', 'defects'],
        'defect_type': ['不良类型', '不良类别', '缺陷类型', 'defect_type'],
        'inspect_item': ['检验项目', '检验项', '检测项目', 'inspect_item']
    }

    def __init__(self, file_path):
        """初始化分析器"""
        self.file_path = Path(file_path)
        self.sheets = {}
        self.field_mapping = {}

    def load_excel(self):
        """加载Excel文件所有sheet"""
        try:
            excel_file = pd.ExcelFile(self.file_path)
            self.sheets = {sheet: pd.read_excel(excel_file, sheet_name=sheet)
                          for sheet in excel_file.sheet_names}
            return True, f"成功加载{len(self.sheets)}个Sheet"
        except Exception as e:
            return False, f"加载Excel失败: {str(e)}"

    def analyze_structure(self):
        """分析数据结构"""
        if not self.sheets:
            success, msg = self.load_excel()
            if not success:
                return {"success": False, "message": msg}

        structure_info = {
            "success": True,
            "file_name": self.file_path.name,
            "sheet_count": len(self.sheets),
            "sheets": {},
            "field_suggestions": {},
            "relationship_suggestions": []
        }

        # 分析每个sheet
        for sheet_name, df in self.sheets.items():
            structure_info["sheets"][sheet_name] = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns)
            }

        # 识别字段
        all_columns = set()
        for df in self.sheets.values():
            all_columns.update(df.columns)

        for std_field, aliases in self.STANDARD_FIELDS.items():
            for col in all_columns:
                if any(alias.lower() in str(col).lower() for alias in aliases):
                    if std_field not in structure_info["field_suggestions"]:
                        structure_info["field_suggestions"][std_field] = col
                    break

        # 识别关联关系
        if len(self.sheets) > 1:
            common_columns = set(self.sheets[list(self.sheets.keys())[0]].columns)
            for df in list(self.sheets.values())[1:]:
                common_columns &= set(df.columns)

            # 优先推荐批次号、物料编码作为关联键
            priority_keys = ['batch_no', 'material_code', 'supplier_name']
            for key in priority_keys:
                if key in structure_info["field_suggestions"]:
                    suggested_col = structure_info["field_suggestions"][key]
                    if suggested_col in common_columns:
                        structure_info["relationship_suggestions"].append({
                            "type": "主键关联",
                            "field": suggested_col,
                            "description": f"建议通过'{suggested_col}'字段关联所有Sheet"
                        })
                        break

        return structure_info

    def apply_mapping(self, mapping):
        """应用字段映射"""
        self.field_mapping = mapping

    def get_standard_column(self, df, std_field):
        """获取标准字段对应的列名"""
        if std_field in self.field_mapping:
            return self.field_mapping[std_field]
        if std_field in self.STANDARD_FIELDS:
            for col in df.columns:
                if any(alias.lower() in str(col).lower() for alias in self.STANDARD_FIELDS[std_field]):
                    return col
        return None

    def clean_and_merge_data(self):
        """清洗和合并数据"""
        # 检查必需字段
        first_df = list(self.sheets.values())[0]
        required_fields = ['supplier_name', 'quantity', 'defect_qty', 'defect_type']
        missing_fields = []

        for field in required_fields:
            col = self.get_standard_column(first_df, field)
            if col is None:
                missing_fields.append(field)

        if missing_fields:
            return False, f"缺少必需字段: {', '.join(missing_fields)}"

        # 合并多个sheet（如果有）
        if len(self.sheets) == 1:
            merged_df = list(self.sheets.values())[0].copy()
        else:
            # 尝试通过关联键合并
            merge_key = None
            for key in ['batch_no', 'material_code']:
                col = self.get_standard_column(first_df, key)
                if col:
                    merge_key = col
                    break

            if merge_key is None:
                return False, "无法识别关联字段，请提供字段映射"

            # 合并所有sheet
            merged_df = pd.concat(self.sheets.values(), ignore_index=True)

        # 标准化列名
        column_mapping = {}
        for std_field in ['supplier_name', 'material_code', 'batch_no',
                         'inspect_date', 'quantity', 'defect_qty',
                         'defect_type', 'inspect_item']:
            col = self.get_standard_column(merged_df, std_field)
            if col:
                column_mapping[col] = std_field

        merged_df = merged_df.rename(columns=column_mapping)

        # 数据清洗
        # 1. 删除全空行
        merged_df = merged_df.dropna(how='all')

        # 2. 填充空值
        if 'defect_qty' in merged_df.columns:
            merged_df['defect_qty'] = merged_df['defect_qty'].fillna(0)

        if 'quantity' in merged_df.columns:
            merged_df['quantity'] = merged_df['quantity'].fillna(0)

        # 3. 日期格式转换
        if 'inspect_date' in merged_df.columns:
            merged_df['inspect_date'] = pd.to_datetime(
                merged_df['inspect_date'], errors='coerce'
            )

        # 4. 数值转换
        numeric_cols = ['quantity', 'defect_qty']
        for col in numeric_cols:
            if col in merged_df.columns:
                merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(0)

        # 5. 删除重复批次（保留最新记录）
        if 'batch_no' in merged_df.columns and 'inspect_date' in merged_df.columns:
            merged_df = merged_df.sort_values('inspect_date', ascending=False)
            merged_df = merged_df.drop_duplicates(subset=['batch_no'], keep='first')

        self.merged_data = merged_df
        return True, f"数据清洗完成，共{len(merged_df)}条记录"

    def calculate_metrics(self):
        """计算质量指标"""
        df = self.merged_data

        # 基础汇总
        total_batches = len(df)
        total_quantity = df['quantity'].sum()
        total_defects = df['defect_qty'].sum()

        # 批次合格率
        df['is_pass'] = df['defect_qty'] == 0
        pass_batches = df['is_pass'].sum()
        batch_pass_rate = (pass_batches / total_batches * 100) if total_batches > 0 else 0

        # PPM
        ppm = (total_defects / total_quantity * 1000000) if total_quantity > 0 else 0

        # 单供应商汇总
        supplier_summary = []
        if 'supplier_name' in df.columns:
            for supplier in df['supplier_name'].unique():
                supplier_df = df[df['supplier_name'] == supplier]
                sup_batches = len(supplier_df)
                sup_quantity = supplier_df['quantity'].sum()
                sup_defects = supplier_df['defect_qty'].sum()
                sup_pass = supplier_df['is_pass'].sum()
                sup_pass_rate = (sup_pass / sup_batches * 100) if sup_batches > 0 else 0
                sup_ppm = (sup_defects / sup_quantity * 1000000) if sup_quantity > 0 else 0

                # 风险评级
                if sup_pass_rate >= 98 and sup_ppm <= 500:
                    risk_level = 'A'
                    risk_class = 'risk-a'
                elif sup_pass_rate >= 95 and sup_ppm <= 2000:
                    risk_level = 'B'
                    risk_class = 'risk-b'
                else:
                    risk_level = 'C'
                    risk_class = 'risk-c'

                supplier_summary.append({
                    'supplier': supplier,
                    'batches': sup_batches,
                    'quantity': int(sup_quantity),
                    'defects': int(sup_defects),
                    'pass_rate': round(sup_pass_rate, 2),
                    'ppm': round(sup_ppm, 2),
                    'risk_level': risk_level,
                    'risk_class': risk_class
                })

        # 不良类型TOP
        defect_type_top = []
        if 'defect_type' in df.columns:
            defect_counts = df[df['defect_qty'] > 0]['defect_type'].value_counts().head(5)
            total_defect_records = len(df[df['defect_qty'] > 0])
            for defect_type, count in defect_counts.items():
                defect_type_top.append({
                    'defect_type': str(defect_type),
                    'count': int(count),
                    'percentage': round(count / total_defect_records * 100, 2) if total_defect_records > 0 else 0
                })

        # 检验项目TOP
        inspect_item_top = []
        if 'inspect_item' in df.columns:
            item_counts = df[df['defect_qty'] > 0]['inspect_item'].value_counts().head(5)
            total_item_records = len(df[df['defect_qty'] > 0])
            for inspect_item, count in item_counts.items():
                inspect_item_top.append({
                    'inspect_item': str(inspect_item),
                    'count': int(count),
                    'percentage': round(count / total_item_records * 100, 2) if total_item_records > 0 else 0
                })

        # 供应商横向对标
        supplier_comparison = []
        if len(supplier_summary) > 1:
            # 计算综合得分（合格率权重60%，PPM权重40%）
            max_ppm = max([s['ppm'] for s in supplier_summary])
            for sup in supplier_summary:
                pass_score = sup['pass_rate']
                ppm_score = (1 - sup['ppm'] / max_ppm) * 100 if max_ppm > 0 else 100
                total_score = round(pass_score * 0.6 + ppm_score * 0.4, 2)
                supplier_comparison.append({
                    'supplier': sup['supplier'],
                    'pass_rate': sup['pass_rate'],
                    'ppm': sup['ppm'],
                    'score': total_score
                })
            # 按综合得分排序
            supplier_comparison.sort(key=lambda x: x['score'], reverse=True)

        # 趋势分析（按月）
        trend_data = []
        if 'inspect_date' in df.columns:
            df['month'] = df['inspect_date'].dt.to_period('M')
            monthly_stats = df.groupby('month').agg({
                'is_pass': 'mean',
                'quantity': 'sum',
                'defect_qty': 'sum'
            }).reset_index()
            monthly_stats['pass_rate'] = monthly_stats['is_pass'] * 100

            for _, row in monthly_stats.iterrows():
                trend_data.append({
                    'period': str(row['month']),
                    'pass_rate': round(row['pass_rate'], 2)
                })

        # 生成分析结论
        conclusions = []
        conclusions.append(f"本次分析共涵盖{len(supplier_summary)}家供应商，{total_batches}批次来料数据")
        conclusions.append(f"整体批次合格率为{batch_pass_rate:.2f}%，来料不良PPM为{ppm:.2f}")

        if ppm > 2000:
            conclusions.append(f"<span class='highlight'>不良率偏高</span>，PPM达到{ppm:.2f}，建议重点关注不良TOP1项：{defect_type_top[0]['defect_type'] if defect_type_top else '无'}")
        else:
            conclusions.append(f"<span class='good-highlight'>整体质量良好</span>，PPM控制在{ppm:.2f}，符合质量要求")

        if defect_type_top:
            top_defect = defect_type_top[0]
            conclusions.append(f"主要不良类型为'{top_defect['defect_type']}'，占比{top_defect['percentage']:.2f}%，建议供应商针对性改善")

        if len(supplier_summary) > 1:
            worst_supplier = supplier_comparison[-1]['supplier']
            conclusions.append(f"多供应商对标中，'{worst_supplier}'综合表现最差，建议重点跟进并约谈改善")

        return {
            "success": True,
            "summary": {
                "supplier_count": len(supplier_summary),
                "total_batches": total_batches,
                "total_quantity": int(total_quantity),
                "total_defects": int(total_defects),
                "batch_pass_rate": round(batch_pass_rate, 2),
                "ppm": round(ppm, 2)
            },
            "supplier_summary": supplier_summary,
            "defect_type_top": defect_type_top,
            "inspect_item_top": inspect_item_top,
            "supplier_comparison": supplier_comparison,
            "trend_data": trend_data,
            "conclusions": conclusions,
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def main():
    parser = argparse.ArgumentParser(description='供应商IQC质量分析工具')
    parser.add_argument('--file', required=True, help='Excel文件路径')
    parser.add_argument('--action', required=True,
                       choices=['analyze_structure', 'analyze'],
                       help='执行操作：analyze_structure(分析结构) 或 analyze(执行分析)')
    parser.add_argument('--mapping', help='字段映射JSON字符串')

    args = parser.parse_args()

    analyzer = IQCAnalyzer(args.file)

    if args.action == 'analyze_structure':
        result = analyzer.analyze_structure()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == 'analyze':
        # 检查字段映射
        if args.mapping:
            try:
                mapping = json.loads(args.mapping)
                analyzer.apply_mapping(mapping)
            except json.JSONDecodeError:
                print(json.dumps({
                    "success": False,
                    "message": "字段映射JSON格式错误"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
        else:
            # 尝试自动识别
            structure_info = analyzer.analyze_structure()
            if 'supplier_name' not in structure_info.get('field_suggestions', {}):
                print(json.dumps({
                    "success": False,
                    "message": "无法识别供应商字段，请提供字段映射",
                    "structure_info": structure_info
                }, ensure_ascii=False, indent=2))
                sys.exit(1)

        # 加载并清洗数据
        success, msg = analyzer.clean_and_merge_data()
        if not success:
            print(json.dumps({
                "success": False,
                "message": msg
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        # 计算指标
        result = analyzer.calculate_metrics()
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
