
class AdvancedSecretary(EfficientSecretary):
    """高级秘书 v1.5（实体增强 + 多任务）"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_manager = TaskManager()
        self.entity_patterns = self._load_entity_patterns()
    
    def _load_entity_patterns(self):
        """加载实体识别模式"""
        return {
            "person": [
                r"[张王李赵刘陈][总经理经理工总]?",
                r"[A-Z][a-z]+ [A-Z][a-z]+"  # 英文名
            ],
            "location": [
                r"\d+楼",
                r"[大小]会议室",
                r"公司",
                r"办公室"
            ],
            "organization": [
                r"[^\s]+公司",
                r"[^\s]+部门",
                r"[^\s]+中心"
            ],
            "project": [
                r"项目 [A-Z]?",
                r"[A-Z]+ 工程",
                r"[\u4e00-\u9fff]+ 项目"
            ],
            "document": [
                r"报告",
                r"方案",
                r"合同",
                r"文档",
                r"邮件"
            ]
        }
    
    def extract_entities_advanced(self, text: str) -> Dict:
        """高级实体提取"""
        entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    if entity_type not in entities:
                        entities[entity_type] = []
                    entities[entity_type].extend(matches)
        
        # 时间表达式增强
        time_entities = self._extract_time_expressions(text)
        if time_entities:
            entities["time"] = time_entities
        
        return entities
    
    def _extract_time_expressions(self, text: str) -> List[str]:
        """提取时间表达式"""
        patterns = [
            r"今天 | 明日 | 后天",
            r"\d+ [点時]",
            r"上午 | 下午 | 晚上",
            r"\d+ 月\d+ 日",
            r"下周 | 上周 | 这周"
        ]
        
        entities = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            entities.extend(matches)
        
        return entities
    
    def respond_with_preaction(self, text: str) -> str:
        """带主动预判的响应"""
        # 理解意图
        intent = self.understand_intent(text)
        
        # 提取实体
        entities = self.extract_entities_advanced(text)
        
        # 主动预判
        preactions = self._generate_preactions(intent, entities)
        
        # 生成响应
        response = self._generate_efficient_response(text, intent)
        
        # 添加预判建议
        if preactions:
            response += f"\n\n💡 已为您准备：{', '.join(preactions)}"
        
        return response
    
    def _generate_preactions(self, intent: IntentResult, entities: Dict) -> List[str]:
        """生成预判行动"""
        preactions = []
        
        if intent.intent_type == IntentType.MEETING:
            preactions.append("会议室预定")
            if "person" in entities:
                preactions.append("参会人员通知")
            if "time" in entities:
                preactions.append("日程提醒设置")
        
        elif intent.intent_type == IntentType.EMAIL:
            preactions.append("邮件模板准备")
            if "person" in entities:
                preactions.append("联系人邮箱查找")
        
        elif intent.intent_type == IntentType.TASK:
            if "project" in entities:
                preactions.append("项目资料整理")
            if "time" in entities:
                preactions.append("时间节点规划")
        
        return preactions[:3]  # 最多 3 个预判

# 测试
def test_v1_5():
    secretary = AdvancedSecretary(verbose=True)
    
    test_cases = [
        "明天下午 2 点和张总在大会议室开会",
        "给李经理发邮件，关于项目 A 的方案",
        "提醒我下周提交报告",
    ]
    
    print("=== 高级秘书 v1.5 测试 ===\n")
    for text in test_cases:
        print(f"用户：{text}")
        response = secretary.respond_with_preaction(text)
        print(f"秘书：{response}\n")
        print("-" * 50)

if __name__ == "__main__":
    test_v1_5()
