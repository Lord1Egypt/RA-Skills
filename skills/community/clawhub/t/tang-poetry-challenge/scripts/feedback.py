class FeedbackGenerator:
    """
    错误提示和错题分析生成器
    """
    
    def __init__(self):
        """
        初始化反馈生成器
        """
        self.tips = {
            'rhythm': ["提示：注意诗句的韵律和节奏", "提示：考虑诗句的平仄对仗"],
            'meaning': ["提示：结合上句的意境来思考", "提示：想想这句诗表达的情感"],
            'author': ["提示：这首诗的作者是{author}", "提示：回忆一下{author}的诗歌风格"],
            'title': ["提示：这首诗的题目是{title}", "提示：想想《{title}》的内容"],
            'keyword': ["提示：注意上句中的关键词{keyword}", "提示：上句提到了{keyword}，下句可能与之相关"]
        }
    
    def generate_tip(self, question, attempt=1):
        """
        生成错误提示
        :param question: 题目信息
        :param attempt: 尝试次数
        :return: 提示信息
        """
        import random
        
        # 根据尝试次数选择不同类型的提示
        if attempt == 1:
            # 第一次错误，提供一般性提示
            tip_types = ['rhythm', 'meaning']
        elif attempt == 2:
            # 第二次错误，提供作者相关提示
            tip_types = ['author', 'title']
        else:
            # 多次错误，提供关键词提示
            tip_types = ['keyword']
        
        tip_type = random.choice(tip_types)
        tip_template = random.choice(self.tips[tip_type])
        
        # 替换模板中的变量
        if tip_type == 'author':
            tip = tip_template.format(author=question['author'])
        elif tip_type == 'title':
            tip = tip_template.format(title=question['title'])
        elif tip_type == 'keyword':
            # 提取上句中的关键词
            upper_line = question['upper_line']
            # 简单提取最后一个词作为关键词
            keyword = upper_line.split(' ')[-1] if ' ' in upper_line else upper_line[-2:]
            tip = tip_template.format(keyword=keyword)
        else:
            tip = tip_template
        
        return tip
    
    def generate_analysis(self, incorrect_questions):
        """
        生成错题分析
        :param incorrect_questions: 错题列表
        :return: 分析结果
        """
        if not incorrect_questions:
            return "无错题，继续保持！"
        
        analysis = []
        for i, item in enumerate(incorrect_questions):
            question = item['question']
            user_answer = item['user_answer']
            correct_answer = item['correct_answer']
            
            # 分析用户错误原因
            error_reason = self._analyze_error(user_answer, correct_answer)
            
            # 生成详细分析
            item_analysis = f"\n第{i+1}题：\n"
            item_analysis += f"题目：{question['upper_line']}\n"
            item_analysis += f"您的回答：{user_answer}\n"
            item_analysis += f"正确答案：{correct_answer}\n"
            item_analysis += f"出自：《{question['title']}》 - {question['author']}\n"
            item_analysis += f"错误原因：{error_reason}\n"
            item_analysis += f"解析：{self._generate_explanation(question)}"
            
            analysis.append(item_analysis)
        
        return ''.join(analysis)
    
    def _analyze_error(self, user_answer, correct_answer):
        """
        分析错误原因
        :param user_answer: 用户答案
        :param correct_answer: 正确答案
        :return: 错误原因
        """
        # 简单的错误分析逻辑
        if len(user_answer) != len(correct_answer):
            return "诗句长度不匹配"
        
        # 检查是否有相同的字词
        common_chars = set(user_answer) & set(correct_answer)
        if not common_chars:
            return "与正确答案差异较大"
        
        # 检查是否是顺序错误
        if sorted(user_answer) == sorted(correct_answer):
            return "字词顺序错误"
        
        return "部分字词错误"
    
    def _generate_explanation(self, question):
        """
        生成诗句解析
        :param question: 题目信息
        :return: 解析内容
        """
        # 简单的解析生成逻辑
        explanations = {
            "静夜思": "这首诗表达了诗人李白在异乡对故乡的思念之情，语言简洁却意境深远。",
            "春晓": "这首诗描绘了春天早晨的景象，表达了诗人对春天的喜爱之情。",
            "望庐山瀑布": "诗人李白用夸张的手法描绘了庐山瀑布的壮观景象，展现了大自然的雄伟。",
            "赠汪伦": "这首诗表达了诗人李白与汪伦之间深厚的友谊。",
            "黄鹤楼送孟浩然之广陵": "诗人李白通过描绘送别场景，表达了对友人的不舍之情。",
            "早发白帝城": "这首诗描绘了诗人李白流放途中遇赦返回时的喜悦心情。",
            "望天门山": "诗人李白描绘了天门山的雄伟景象，展现了大自然的鬼斧神工。",
            "绝句": "杜甫通过描绘春天的景象，表达了对大自然的热爱之情。",
            "春夜喜雨": "这首诗描绘了春雨的特点，表达了诗人对春雨的喜爱之情。",
            "望岳": "杜甫通过描绘泰山的雄伟景象，表达了自己的豪情壮志。",
            "登鹳雀楼": "这首诗通过描绘登楼所见的景象，表达了诗人积极向上的人生态度。",
            "凉州词": "这首诗描绘了边塞的荒凉景象，表达了戍边将士的思乡之情。",
            "枫桥夜泊": "这首诗描绘了夜晚泊船枫桥的景象，表达了诗人的羁旅之愁。",
            "清明": "这首诗描绘了清明时节的景象，表达了诗人的思乡之情。",
            "山行": "杜牧通过描绘秋天的山林景象，表达了对秋天的喜爱之情。",
            "泊秦淮": "这首诗通过描绘秦淮夜景，表达了诗人对晚唐社会的忧虑。",
            "乐游原": "李商隐通过描绘夕阳西下的景象，表达了对美好时光易逝的感慨。",
            "夜雨寄北": "这首诗表达了诗人李商隐对妻子的思念之情。",
            "九月九日忆山东兄弟": "王维通过描绘重阳节的习俗，表达了对家乡兄弟的思念之情。",
            "送元二使安西": "王维通过描绘送别场景，表达了对友人的不舍之情。"
        }
        
        return explanations.get(question['title'], "这是一首经典的唐诗，具有很高的艺术价值。")

if __name__ == "__main__":
    # 测试代码
    generator = FeedbackGenerator()
    
    # 测试生成提示
    test_question = {
        'title': '静夜思',
        'author': '李白',
        'upper_line': '床前明月光'
    }
    
    print("测试错误提示：")
    for i in range(1, 4):
        tip = generator.generate_tip(test_question, i)
        print(f"尝试{i}次错误：{tip}")
    
    # 测试生成分析
    test_incorrect = [
        {
            'question': test_question,
            'user_answer': '疑是地上霜',
            'correct_answer': '疑是地上霜'
        },
        {
            'question': {
                'title': '春晓',
                'author': '孟浩然',
                'upper_line': '春眠不觉晓'
            },
            'user_answer': '处处闻啼鸟',
            'correct_answer': '处处闻啼鸟'
        }
    ]
    
    print("\n测试错题分析：")
    analysis = generator.generate_analysis(test_incorrect)
    print(analysis)