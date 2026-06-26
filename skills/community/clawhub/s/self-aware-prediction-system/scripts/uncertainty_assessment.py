# 预测不确定性提醒脚本

def assess_prediction_uncertainty(content, info_completeness, prediction_type):
    """
    评估预测的不确定性并返回置信度评分
    """
    # 信息完整性权重
    completeness_weights = {
        'high': 1.0,
        'medium': 0.7,
        'low': 0.4
    }
    
    # 预测类型权重
    type_weights = {
        'fact': 1.0,
        'trend': 0.7,
        'probability': 0.8,
        'speculation': 0.3
    }
    
    base_score = 7  # 基础分数
    
    # 根据信息完整性调整
    completeness_factor = completeness_weights.get(info_completeness, 0.5)
    # 根据预测类型调整
    type_factor = type_weights.get(prediction_type, 0.5)
    
    # 计算最终置信度
    confidence = base_score * completeness_factor * type_factor
    
    # 添加不确定性提醒
    uncertainty_notice = ""
    if confidence < 5:
        uncertainty_notice = "⚠️ 提醒：此预测不确定性较高，建议谨慎参考或寻求更多信息。"
    elif confidence < 7:
        uncertainty_notice = "ℹ️ 注意：此预测存在一定不确定性，请结合实际情况考虑。"
    
    return {
        'confidence_score': round(confidence, 1),
        'uncertainty_notice': uncertainty_notice,
        'risk_level': get_risk_level(confidence)
    }

def get_risk_level(confidence):
    """获取风险等级"""
    if confidence >= 8:
        return "低风险"
    elif confidence >= 5:
        return "中等风险"
    else:
        return "高风险"