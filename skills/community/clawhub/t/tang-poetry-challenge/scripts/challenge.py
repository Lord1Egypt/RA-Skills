import json
import random
import time

class TangPoetryChallenge:
    """
    唐诗三百首对诗挑战类
    """
    
    def __init__(self, data_file):
        """
        初始化挑战类
        :param data_file: 唐诗数据文件路径
        """
        self.data_file = data_file
        self.poems = []
        self.load_data()
        self.challenge_questions = []
        self.user_answers = []
        self.correct_answers = []
        self.start_time = 0
        self.end_time = 0
    
    def load_data(self):
        """
        加载唐诗数据
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.poems = data.get('poems', [])
        except Exception as e:
            print(f"加载数据失败: {e}")
    
    def generate_questions(self, num_questions=10):
        """
        生成挑战题目
        :param num_questions: 题目数量
        :return: 生成的题目列表
        """
        if not self.poems:
            return []
        
        # 随机选择诗歌
        selected_poems = random.sample(self.poems, min(num_questions, len(self.poems)))
        
        questions = []
        for poem in selected_poems:
            # 随机选择诗句作为上句（避免选择最后一句）
            max_line_index = len(poem['lines']) - 1
            if max_line_index > 0:
                line_index = random.randint(0, max_line_index - 1)
                question = {
                    'id': poem['id'],
                    'title': poem['title'],
                    'author': poem['author'],
                    'dynasty': poem['dynasty'],
                    'upper_line': poem['lines'][line_index],
                    'lower_line': poem['lines'][line_index + 1],
                    'line_index': line_index
                }
                questions.append(question)
        
        self.challenge_questions = questions
        return questions
    
    def start_challenge(self):
        """
        开始挑战，记录开始时间
        """
        self.start_time = time.time()
        self.user_answers = []
        self.correct_answers = []
    
    def end_challenge(self):
        """
        结束挑战，记录结束时间
        """
        self.end_time = time.time()
    
    def check_answer(self, question_index, user_answer):
        """
        检查用户答案
        :param question_index: 题目索引
        :param user_answer: 用户答案
        :return: (是否正确, 正确答案)
        """
        if 0 <= question_index < len(self.challenge_questions):
            question = self.challenge_questions[question_index]
            correct_answer = question['lower_line']
            
            # 去除空格和标点符号后比较
            def clean_text(text):
                import re
                return re.sub(r'[\s，。！？；：,.:;?!]', '', text)
            
            is_correct = clean_text(user_answer) == clean_text(correct_answer)
            
            # 记录答案
            self.user_answers.append(user_answer)
            self.correct_answers.append(correct_answer)
            
            return is_correct, correct_answer
        return False, ""
    
    def calculate_score(self):
        """
        计算得分
        :return: (正确数量, 总题目数, 用时(秒))
        """
        correct_count = sum(1 for i, answer in enumerate(self.user_answers) if 
                           self.check_answer(i, answer)[0])
        total_questions = len(self.challenge_questions)
        time_used = self.end_time - self.start_time if self.end_time > self.start_time else 0
        
        return correct_count, total_questions, time_used
    
    def get_score_level(self, correct_count, total_questions):
        """
        获取评分等级
        :param correct_count: 正确数量
        :param total_questions: 总题目数
        :return: 评分等级和评语
        """
        if total_questions == 0:
            return "无", "暂无评分"
        
        percentage = correct_count / total_questions
        
        if percentage == 1:
            return "优秀", "您对唐诗的掌握非常出色！"
        elif percentage >= 0.8:
            return "良好", "您对唐诗有较好的掌握，继续努力！"
        elif percentage >= 0.6:
            return "及格", "您对唐诗有一定了解，建议多背诵！"
        else:
            return "需要加强", "建议您多学习唐诗，提高诗词素养！"
    
    def get_incorrect_questions(self):
        """
        获取错题列表
        :return: 错题列表
        """
        incorrect = []
        for i, (user_answer, question) in enumerate(zip(self.user_answers, self.challenge_questions)):
            is_correct, correct_answer = self.check_answer(i, user_answer)
            if not is_correct:
                incorrect.append({
                    'question': question,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer
                })
        return incorrect

if __name__ == "__main__":
    # 测试代码
    challenge = TangPoetryChallenge('references/tang_poetry.json')
    questions = challenge.generate_questions(5)
    
    print("唐诗三百首对诗挑战开始！")
    challenge.start_challenge()
    
    for i, q in enumerate(questions):
        print(f"\n第{i+1}题，请对出下句：")
        print(q['upper_line'])
        user_input = input("您的回答：")
        is_correct, correct_answer = challenge.check_answer(i, user_input)
        
        if is_correct:
            print("回答正确！")
        else:
            print(f"回答错误，正确答案是：{correct_answer}")
    
    challenge.end_challenge()
    correct_count, total, time_used = challenge.calculate_score()
    level, comment = challenge.get_score_level(correct_count, total)
    
    print(f"\n挑战结束！")
    print(f"得分：{correct_count}/{total}")
    print(f"用时：{time_used:.2f}秒")
    print(f"评分：{level}")
    print(f"评语：{comment}")
    
    incorrect = challenge.get_incorrect_questions()
    if incorrect:
        print("\n错题分析：")
        for i, item in enumerate(incorrect):
            print(f"\n第{i+1}题：")
            print(f"题目：{item['question']['upper_line']}")
            print(f"您的回答：{item['user_answer']}")
            print(f"正确答案：{item['correct_answer']}")
            print(f"出自：{item['question']['title']} - {item['question']['author']}")
    else:
        print("\n错题分析：无错题，继续保持！")