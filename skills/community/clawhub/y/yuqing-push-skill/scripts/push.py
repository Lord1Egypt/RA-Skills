#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
舆情结果推送脚本
将标注完成的舆情结果推送到指定渠道
"""

import sys
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def push_result(labeled_data):
    """
    推送标注结果到目标渠道
    TODO: 替换为实际的推送逻辑
    """
    # 示例：统计各类情感
    sentiment_counts = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }
    risk_counts = {
        'low': 0,
        'medium': 0,
        'high': 0
    }
    
    for item in labeled_data:
        sentiment = item.get('sentiment', 'neutral')
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        risk = item.get('risk_level', 'low')
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    # TODO: 实际推送到飞书/多维表格/邮件等
    
    logger.info(f"统计完成: 正面{sentiment_counts['positive']} 中性{sentiment_counts['neutral']} 负面{sentiment_counts['negative']}")
    logger.info(f"风险分布: 低{risk_counts['low']} 中{risk_counts['medium']} 高{risk_counts['high']}")
    
    return True

def main():
    """
    主函数：读取标注结果并推送
    从stdin读取标注输出的JSON，推送后输出状态
    """
    try:
        input_data = json.load(sys.stdin)
    except Exception as e:
        logger.error(f"读取输入失败: {e}")
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)
    
    labeled_data = input_data.get('labeled_data', [])
    
    success = push_result(labeled_data)
    
    if success:
        result = {
            "status": "success",
            "pushed_count": len(labeled_data),
            "message": "舆情结果推送完成"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    else:
        result = {
            "status": "error",
            "message": "推送失败"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
