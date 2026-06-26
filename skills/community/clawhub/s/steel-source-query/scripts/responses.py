#!/usr/bin/env python3
"""
用户对话响应模板
提供友好、专业、有服务意识的回复
"""

from typing import Dict, Optional, List
from datetime import datetime

class ResponseBuilder:
    """响应构建器 - 提供友好专业的回复"""
    
    # 欢迎语
    WELCOME_MESSAGES = [
        "您好！我是您的钢材价格助手，很高兴为您服务 😊",
        "您好！有什么钢材相关的问题，随时问我~",
        "欢迎！需要查询价格、分析走势还是管理库存？",
    ]
    
    # 帮助提示
    HELP_HINTS = [
        "您可以这样问我：",
        "试试这样说：",
        "支持的查询方式：",
    ]
    
    # 友好结束语
    CLOSING_MESSAGES = [
        "如有其他问题，随时找我！",
        "希望对您有帮助，随时为您服务~",
        "有问题随时咨询，祝您生意兴隆！",
    ]
    
    @staticmethod
    def welcome() -> str:
        """欢迎语"""
        return """您好！我是您的钢材价格助手 😊

我可以帮您：
• 查询实时钢材价格
• 分析价格走势
• 管理库存数据
• 导出价格报表

请告诉我您需要什么帮助？"""
    
    @staticmethod
    def price_query_prompt() -> str:
        """价格查询引导"""
        return """请告诉我您要查询的钢材信息：

📍 地区：如唐山、上海、广州等
🔩 品种：如螺纹钢、热轧板卷等  
📏 规格（可选）：如 Φ12-14 HRB400E

例如：
• 唐山螺纹钢多少钱？
• 查一下上海热轧板卷价格
• 冷轧板卷什么价？

回复【列表】查看所有支持的地区和品种~"""
    
    @staticmethod
    def price_result(data: Dict) -> str:
        """价格查询结果"""
        if not data or not data.get("price"):
            return """抱歉，暂时未能查询到该品种的价格。

可能的原因：
• 该品种在该地区暂无报价
• 网络连接问题

建议您：
• 换个地区或品种试试
• 稍后再试
• 回复【列表】查看支持的品种"""
        
        lines = []
        lines.append("✅ 查询成功！")
        lines.append("")
        lines.append(f"📍 {data.get('region', '-')} {data.get('type', '-')}")
        if data.get('spec'):
            lines.append(f"📏 规格：{data['spec']}")
        lines.append("")
        lines.append(f"💰 今日价格：{data['price']} 元/吨")
        lines.append(f"📡 数据来源：{data.get('source', '找钢网')}")
        lines.append(f"🕐 更新时间：{data.get('date', datetime.now().strftime('%Y-%m-%d'))}")
        
        if data.get('note'):
            lines.append(f"💡 {data['note']}")
        
        lines.append("")
        lines.append("需要我帮您：")
        lines.append("• 分析价格走势")
        lines.append("• 对比其他地区价格")
        lines.append("• 导出价格表")
        
        return "\n".join(lines)
    
    @staticmethod
    def trend_analysis(result: Dict) -> str:
        """走势分析结果"""
        if result.get("trend_direction") == "unknown":
            return """📊 走势分析

抱歉，目前数据不足，无法分析走势。

建议您：
• 稍后再试，系统需要积累更多价格数据
• 先查询几次价格，再进行分析"""
        
        trend_emojis = {"up": "📈", "down": "📉", "stable": "➡️"}
        trend_texts = {"up": "上涨", "down": "下跌", "stable": "平稳"}
        
        trend = result.get("trend_direction", "stable")
        
        lines = []
        lines.append("📊 价格走势分析")
        lines.append(f"分析周期：{result['dates']['start']} 至 {result['dates']['end']}")
        lines.append("")
        lines.append(f"{trend_emojis.get(trend, '📊')} 走势：{trend_texts.get(trend, '平稳')}")
        lines.append(f"📈 涨跌幅：{result['total_change_percent']:+.2f}%")
        lines.append(f"💰 涨跌额：{result['total_change']:+.0f} 元/吨")
        lines.append("")
        lines.append("📋 价格区间：")
        lines.append(f"  • 最高价：{result['high']:.0f} 元/吨")
        lines.append(f"  • 最低价：{result['low']:.0f} 元/吨")
        lines.append(f"  • 平均价：{result['avg']:.0f} 元/吨")
        lines.append(f"  • 波动率：{result['volatility']:.2f}%")
        lines.append("")
        lines.append(f"🔮 短期预测：{result['forecast']}")
        lines.append("")
        lines.append(f"💡 操作建议：{result['recommendation']}")
        
        return "\n".join(lines)
    
    @staticmethod
    def inventory_empty() -> str:
        """库存为空"""
        return """📦 当前库存

您还没有录入库存数据。

您可以通过以下方式添加：
1. Excel批量导入（推荐）
   • 发送【导出模板】获取Excel模板
   • 填写后发送Excel文件给我

2. 手动添加
   • 回复【添加库存】逐条录入

需要我为您导出模板吗？"""
    
    @staticmethod
    def inventory_list(items: List[Dict]) -> str:
        """库存列表"""
        if not items:
            return ResponseBuilder.inventory_empty()
        
        lines = []
        lines.append(f"📦 库存列表 (共 {len(items)} 条)")
        lines.append("")
        
        # 按供应商分组
        by_supplier = {}
        for item in items:
            supplier = item.get("supplier", "未分类")
            if supplier not in by_supplier:
                by_supplier[supplier] = []
            by_supplier[supplier].append(item)
        
        for supplier, items_list in by_supplier.items():
            lines.append(f"【{supplier}】")
            for item in items_list:
                lines.append(f"  • {item.get('type', '-')} {item.get('spec', '-')}：{item.get('price', '-')}元/吨")
            lines.append("")
        
        lines.append("💡 回复【导入库存】可批量添加更多")
        
        return "\n".join(lines)
    
    @staticmethod
    def excel_template_guide() -> str:
        """Excel模板使用说明"""
        return """📄 库存Excel模板使用说明

我已经为您准备好模板，请按以下步骤操作：

第一步：下载模板
模板已发送到文件传输助手，请查收

第二步：填写数据
请填写以下字段：
• 品种（必填）：如螺纹钢、热轧板卷
• 规格（必填）：如 Φ12-14 HRB400E
• 价格（必填）：单价，元/吨
• 数量：库存数量，吨
• 供应商：钢贸商名称
• 联系人、电话、地区、备注（选填）

第三步：上传文件
填写完成后，直接发送Excel文件给我即可

注意事项：
• 支持多个钢贸商同时录入
• 价格请填写数字，不要带单位
• 规格尽量详细，便于匹配

有什么不清楚的随时问我！"""
    
    @staticmethod
    def excel_import_success(count: int, supplier: str = "") -> str:
        """Excel导入成功"""
        msg = f"✅ 导入成功！\n\n已成功导入 {count} 条库存记录"
        if supplier:
            msg += f"\n供应商：{supplier}"
        msg += "\n\n回复【查看库存】可查看全部数据"
        return msg
    
    @staticmethod
    def excel_import_error(error_msg: str) -> str:
        """Excel导入失败"""
        return f"""❌ 导入失败

错误信息：{error_msg}

可能的原因：
• Excel格式不正确
• 缺少必填字段（品种、规格、价格）
• 价格列包含非数字内容

建议您：
1. 检查Excel格式
2. 确认必填字段已填写
3. 回复【导出模板】获取标准模板

需要重新上传吗？"""
    
    @staticmethod
    def data_source_status(sources: List[Dict]) -> str:
        """数据源状态"""
        lines = []
        lines.append("📡 数据源状态")
        lines.append("")
        
        for source in sources:
            status = "✅ 正常" if source.get("enabled") and source.get("fail_count", 0) < 3 else "❌ 不可用"
            lines.append(f"{status} {source['name']}")
            lines.append(f"   优先级：{source.get('priority', '-')}")
            if source.get("last_success"):
                lines.append(f"   最后成功：{source['last_success'][:10]}")
            lines.append("")
        
        lines.append("💡 系统会自动选择最优数据源")
        return "\n".join(lines)
    
    @staticmethod
    def error_general(error: str = "") -> str:
        """通用错误"""
        return f"""😅 抱歉，出了一点小状况

{error if error else "操作未能完成，请稍后重试"}

您可以：
• 稍后重试
• 换个方式描述您的需求
• 回复【帮助】查看使用指南

感谢您的理解！"""
    
    @staticmethod
    def closing() -> str:
        """结束语"""
        import random
        return random.choice(ResponseBuilder.CLOSING_MESSAGES)


# 快捷函数
def welcome():
    return ResponseBuilder.welcome()

def price_query_prompt():
    return ResponseBuilder.price_query_prompt()

def price_result(data):
    return ResponseBuilder.price_result(data)

def trend_analysis(result):
    return ResponseBuilder.trend_analysis(result)

def inventory_list(items):
    return ResponseBuilder.inventory_list(items)

def inventory_empty():
    return ResponseBuilder.inventory_empty()

if __name__ == "__main__":
    # 测试
    print(ResponseBuilder.welcome())
    print("\n" + "="*40 + "\n")
    print(ResponseBuilder.price_query_prompt())
    print("\n" + "="*40 + "\n")
    print(ResponseBuilder.inventory_empty())
