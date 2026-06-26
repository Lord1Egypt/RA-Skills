#!/usr/bin/env python3
import json, sys
def assess(query):
    hours=5 if '2点' in query and '7点' in query else 7
    score=max(40, min(95, int(hours*10)))
    if '手机' in query or '刷' in query: score-=10
    if '很累' in query or '睡不着' in query: score-=8
    score=max(35, score)
    return score, hours
def handle(query):
    score,hours=assess(query)
    habits=[{'habit':'睡前使用手机','impact':'高','recommendation':'睡前1小时停止使用电子设备','alternative':'阅读纸质书或呼吸练习'}] if ('手机' in query or '刷' in query) else [{'habit':'作息不规律','impact':'中','recommendation':'固定上床与起床时间','alternative':'建立睡前仪式'}]
    return {'sleepAssessment':{'qualityScore':score,'durationHours':hours,'overallRating':'较差' if score<60 else '中等' if score<80 else '良好','strengths':['有改善空间'],'weaknesses':['睡眠不足' if hours<7 else '习惯需优化']},'bedtimeHabitAnalysis':habits,'scheduleAdjustment':{'targetBedtime':'23:00','targetWakeup':'07:00','adjustmentPlan':'每3天提前15-30分钟入睡'},'environmentOptimization':{'lighting':'保持黑暗','noise':'必要时使用耳塞/白噪音','temperature':'18-22°C'},'selfHelpRecommendations':['睡前1小时不用手机','下午减少咖啡因','白天适量运动','尝试4-7-8呼吸法'],'medicalAdvice':{'needConsultation':score<45,'suggestion':'如连续2周无改善，建议咨询睡眠专科医生。'},'disclaimer':'本工具仅提供健康生活建议，不替代专业医疗诊断。'}
if __name__=='__main__':
    q=' '.join(sys.argv[1:]) or '我最近总是凌晨2点才睡着，早上7点起床，很累'
    print(json.dumps(handle(q), ensure_ascii=False, indent=2))
