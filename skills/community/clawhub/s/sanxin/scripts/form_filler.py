# -*- coding: utf-8 -*-
"""
智能申报表填写脚本
功能：将申报报告内容智能填入申请表对应位置
作者：小龙虾
版本：1.0.0

使用方法：
1. 设置 source_doc（申报报告路径）
2. 设置 form_doc（申请表路径）
3. 设置 output_path（输出路径）
4. 配置 content_map（章节内容映射）
"""

import win32com.client

def fill_form(source_doc, form_doc, output_path, content_map, table_index=2):
    """
    填写申报表
    
    Args:
        source_doc: 申报报告路径（用于提取内容）
        form_doc: 申请表路径（空表）
        output_path: 输出文件路径
        content_map: 章节内容映射 {行号: 内容}
        table_index: 主表格索引（默认为第2个表格）
    
    Returns:
        bool: 是否成功
    """
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = True
    
    try:
        doc = word.Documents.Open(form_doc)
        main_table = doc.Tables(table_index)
        
        print("开始填写申报表...")
        
        for row_idx, content in content_map.items():
            try:
                cell = main_table.Cell(row_idx, 1)
                
                # 获取原有标题（第一行）
                original = cell.Range.Text
                original = original.replace('\r', '').replace('\x07', '').strip()
                title = original.split('\n')[0] if '\n' in original else original
                
                # 记录标题长度
                title_len = len(title)
                
                # 清空单元格
                cell.Range.Delete()
                
                # 写入标题
                cell.Range.InsertAfter(title)
                
                # 设置标题格式
                title_range = doc.Range(cell.Range.Start, cell.Range.Start + title_len)
                set_format(title_range)
                
                # 记录标题结束位置
                title_end = cell.Range.End
                
                # 写入换行和内容
                cell.Range.InsertAfter("\n" + content)
                
                # 设置内容格式
                content_start = title_end + 1
                content_end = cell.Range.End
                
                if content_start < content_end:
                    content_range = doc.Range(content_start, content_end)
                    set_format(content_range)
                
                print(f"[OK] 第{row_idx}节已填写")
                
            except Exception as e:
                print(f"[FAIL] 第{row_idx}节失败: {e}")
        
        # 调整表格行高
        adjust_table_height(main_table)
        
        # 保存
        doc.SaveAs2(output_path, FileFormat=16)
        print(f"\n[OK] 已保存到：{output_path}")
        
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        return False


def set_format(range_obj):
    """设置文本格式：宋体、小四、黑色、无下划线、不加粗"""
    try:
        range_obj.Font.Name = "宋体"
        range_obj.Font.NameFarEast = "宋体"
        range_obj.Font.Size = 12  # 小四
        range_obj.Font.Color = 0  # 黑色
        range_obj.Font.Bold = False
        range_obj.Font.Italic = False
        range_obj.Font.Underline = 0  # 无下划线
    except:
        pass


def adjust_table_height(table):
    """调整表格行高为自动"""
    try:
        for row_idx in range(1, table.Rows.Count + 1):
            try:
                row = table.Rows(row_idx)
                row.HeightRule = 0  # wdRowHeightAuto
            except:
                pass
        table.Rows.AllowBreakAcrossPages = True
        print("[OK] 表格行高已调整为自动")
    except:
        pass


def clean_control_chars(text):
    """清理控制字符"""
    return text.replace('\r\x07', '').replace('\x07', '').replace('_x0007_', '')


# 示例用法
if __name__ == "__main__":
    # 示例配置
    source_doc = r"C:\Users\xxx\Downloads\申报报告.docx"
    form_doc = r"C:\Users\xxx\Desktop\空表申报表.doc"
    output_path = r"C:\Users\xxx\Desktop\申报表_已填写.docx"
    
    # 章节内容映射（需要根据实际情况填写）
    content_map = {
        1: "第一章内容...",
        2: "第二章内容...",
        # ...
    }
    
    fill_form(source_doc, form_doc, output_path, content_map)