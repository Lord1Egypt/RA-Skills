#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""声誉体温计 - 舆情风险预诊工具 v4.1 (精简版)"""
import json,sys,io,math
from datetime import datetime
from typing import Dict,List,Any,Tuple
from collections import defaultdict

if sys.platform=='win32':
    sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
    sys.stderr=io.TextIOWrapper(sys.stderr.buffer,encoding='utf-8',errors='replace')

EMOTION_KW="anger:愤怒，气愤，恶心，垃圾，骗子，黑心，维权，曝光，投诉，强烈，退款，欺诈，倒闭，坑人，智商税，潜规则，拖欠，克扣，滚蛋，滚出，抵制，侮辱，丑化，抹黑，傲慢，恶意|fear:害怕，恐惧，危险，安全，威胁，紧急，救命，求助，裁员，癌症，无助，封杀，辞退|sadness:悲伤，绝望，心痛，遗憾，可怜，悲剧，失望，去世，死了，死亡，受伤，呕吐，腹泻，送医，抢救，病危，婴儿，儿童，孩子|disgust:恶心，肮脏，无耻，垃圾，老鼠，虫子，地沟油，三聚氰胺，过期，虐待，偷税，吸毒，出轨，阴间审美，蜥蜴|surprise:震惊，意外，没想到，居然，竟然|contempt:呵呵，冷笑，鄙视，可笑，笑话，旱涝保收，专家，建议，肉糜，房租，闲置，吃不起饭"
VIRAL_KW="热搜，转发，扩散，爆料，曝光，真相，紧急，速看，震惊，突发，刚刚，实锤，明星，死亡，受伤，中毒，疫苗，过期，婴儿，儿童，幼儿园，跑路，暴雷，维权，拉横幅，围堵，偷税，吸毒，虐待，地沟油，三聚氰胺，火灾，爆炸，坍塌，事故，裁员，996，加班，欺诈，差评，避雷，老鼠，虫子，呕吐，腹泻，潜规则，出轨，塌房，拒赔，泄露，泄漏，数据安全，隐私，黑客，攻击，漏洞，违规，违法，监管，处罚，立案，调查，实名，身份证，手机号，银行卡，密码，账户，500 万，千万，百万，用户信息，个人信息，数据库，公网，备份，没钱，兑付，理财，利息，拆东墙，创始人，赶紧跑，被逼，滚出中国，抵制，丑化，侮辱，抹黑，辱华，傲慢，阴间审美，龙，蜥蜴，东方，文化，民族，品牌，广告，恶意，赚中国人的钱，小动作，国际品牌，内部消息，囤物资，交通管制，交警严查，紧急通知，谣言，造谣，恐慌"
SENSITIVE_KW="死亡，婴儿，儿童，孩子，幼儿，学生，中毒，病危，抢救，三聚氰胺，爆炸，坍塌，吸毒，偷税，未成年，虐待，地沟油，食品安全，群体中毒，多人死亡，药品，工业原料，爆料，拿命，老鼠，呕吐，潜规则，出轨，拒赔，暴雷，跑路，失联，无法兑付，投资人，血本无归，百亿，误诊，病情，数据泄露，隐私泄露，信息泄露，泄露，泄漏，黑客，攻击，漏洞，违规，违法，监管，处罚，立案，调查，实名，身份证，手机号，银行卡，密码，账户，用户信息，个人信息，数据库，网络安全，数据安全，没钱，兑付，理财，利息，拆东墙补西墙，创始人，赶紧跑，被逼，资金链断裂，庞氏骗局，丑化，侮辱，抹黑，辱华，傲慢，阴间审美，文化侮辱，民族情绪，抵制，滚出中国，国际品牌，内部消息，囤物资，交通管制，谣言，造谣，恐慌，全市，封路，封锁，紧急通知"
AI_PATTERNS="据知情人士，内部消息，独家渠道，匿名人士，网传，疑似，震惊！,重磅！,刚刚！,声音平稳，无呼吸，无停顿，AI 合成，AI 伪造，深度伪造，语音合成，TTS"
INDUSTRY_KW="food:中毒，腹泻，呕吐，老鼠，地沟油|medical:死亡，误诊，疫苗，红包|education:体罚，虐待，跑路，校车|finance:暴雷，跑路，失联，无法兑付|entertainment:吸毒，出轨，偷税，塌房|workplace:996，加班，裁员，pua"
ML_DATA="工厂爆炸 3 人死亡=黑|幼儿园校车侧翻儿童受伤=黑|奶粉检出三聚氰胺=黑|食物中毒 50 名儿童送医=黑|数据泄露 500 万用户信息曝光=黑|数据库公开到公网涉及百万实名=黑|用户隐私泄露监管立案调查=黑|理财平台暴雷无法兑付=红|创始人录音曝光公司没钱了=红|庞氏骗局拆东墙补西墙=红|品牌广告丑化中国抵制滚出中国=红|国际品牌辱华赚中国人的钱=红|紧急通知交通管制囤物资=黑|内部消息全市封路别出门=黑|歌手吸毒被抓=红|导演潜规则曝光=红|明星偷税漏税=红|保险公司拒赔=红|餐厅吃出老鼠=橙|医院误诊=橙|幼儿园虐待儿童=橙|食堂吃出虫子=橙|4S 店卖事故车=橙|专家建议吃不起饭可以吃肉糜=黄|没工作的人把闲置房租出去=黄|公司 996 加班=黄|年终奖缩水=黄|领导 pua 员工=黄|手机卡顿=黄|APP 闪退=黄|这家餐厅很好吃=蓝|快递很快=蓝|客服态度好=蓝|产品质量不错=蓝|明天公司团建=蓝"

def parse_kws(s,sep1='|',sep2=':'): return {p.split(sep2)[0]:p.split(sep2)[1].split(',') for p in s.split(sep1)} if sep2 in s else s.split(',')
EMOTION_KEYWORDS=parse_kws(EMOTION_KW)
INDUSTRY_TEMPLATES={k:{"name":{"food":"食品/餐饮","medical":"医疗/健康","education":"教育/培训","finance":"金融/理财","entertainment":"娱乐/明星","workplace":"职场/劳动"}[k],"keywords":v.split(','),"response":{"food":"1h","medical":"1h","education":"2h","finance":"2h","entertainment":"4h","workplace":"12h"}[k]} for k,v in [p.split(':') for p in INDUSTRY_KW.split('|')]}
ML_DATA=[p.rsplit('=',1) for p in ML_DATA.split('|')]

class MLClassifier:
    def __init__(self):
        self.classes=["蓝","黄","橙","红","黑"]
        self.class_probs={}
        self.word_probs=defaultdict(lambda:defaultdict(float))
        self.train()
    def train(self):
        word_counts=defaultdict(lambda:defaultdict(int))
        class_counts=defaultdict(int)
        for text,label in ML_DATA:
            class_counts[label]+=1
            for char in text:
                if '\u4e00'<=char<='\u9fff': word_counts[label][char]+=1
        total_docs=len(ML_DATA)
        vocab_size=len(set(c for t,_ in ML_DATA for c in t if '\u4e00'<=c<='\u9fff'))
        for cls in self.classes:
            self.class_probs[cls]=class_counts[cls]/total_docs
            total_words=sum(word_counts[cls].values())
            for word in word_counts[cls]:
                self.word_probs[cls][word]=(word_counts[cls][word]+1)/(total_words+vocab_size)
    def predict(self,text:str)->Tuple[str,float]:
        log_probs={}
        for cls in self.classes:
            log_prob=math.log(self.class_probs.get(cls,0.01)+1e-10)
            for char in text:
                if '\u4e00'<=char<='\u9fff': log_prob+=math.log(self.word_probs[cls].get(char,1e-10)+1e-10)
            log_probs[cls]=log_prob
        if ("死亡" in text or "死了" in text) and ("儿童" in text or "婴儿" in text): log_probs["黑"]+=2.5
        if "中毒" in text and ("食物" in text or "儿童" in text): log_probs["黑"]+=2.0
        if any(k in text for k in ["暴雷","失联","跑路"]) and any(k in text for k in ["百亿","投资人"]): log_probs["红"]+=1.8
        if any(k in text for k in ["吸毒","出轨","偷税"]) and any(k in text for k in ["明星","演员"]): log_probs["红"]+=1.5
        best=max(log_probs,key=log_probs.get)
        max_p=log_probs[best]
        exp_p={c:math.exp(lp-max_p) for c,lp in log_probs.items()}
        return best,round(exp_p[best]/sum(exp_p.values()),2)

def detect_industry(text:str)->str:
    for ind,t in INDUSTRY_TEMPLATES.items():
        if any(k in text for k in t["keywords"]): return ind
    return "general"

def analyze_emotion(text:str)->Dict:
    scores={e:min(sum(1 for k in kws if k in text)*2,10) for e,kws in EMOTION_KEYWORDS.items()}
    matched=[e for e,s in scores.items() if s>0]
    return {"score":max(scores.values()) if scores else 0,"emotions":matched}

def analyze_viral(text:str)->Dict:
    viral=sum(1 for k in VIRAL_KW.split('，') if k in text)
    sensitive=sum(1 for k in SENSITIVE_KW.split('，') if k in text)
    return {"score":min(round(viral*1.5+sensitive*2,1),10),"keywords":viral,"sensitive":sensitive}

def analyze_ai(text:str)->Dict:
    patterns=sum(1 for p in AI_PATTERNS.split('，') if p in text)
    exclam=text.count("！")+text.count("!")
    ai_score=patterns*2+min(exclam,5)
    if "声音" in text and ("平稳" in text or "无呼吸" in text or "无停顿" in text): ai_score+=4
    if "录音" in text and ("转录" in text or "合成" in text or "伪造" in text): ai_score+=3
    return {"score":min(ai_score,10),"patterns":patterns}

def calc_risk(emotion:int,viral:int,ai:int,text:str,ml_level:str,ml_conf:float)->Dict:
    harm=emotion*0.5+viral*0.4+ai*0.1
    if ("死亡" in text or "死了" in text) and ("儿童" in text or "婴儿" in text): harm+=2
    if "中毒" in text and ("群体" in text or "多人" in text): harm+=2
    if "三聚氰胺" in text: harm+=2
    if ("儿童" in text or "婴儿" in text or "孩子" in text or "幼儿" in text) and ("药" in text or "中毒" in text or "原料" in text or "食品" in text): harm+=2
    if "爆料" in text or "内部" in text: harm+=1
    if ("泄露" in text or "泄漏" in text or "公开" in text) and ("数据" in text or "信息" in text or "数据库" in text):
        harm+=3 if any(k in text for k in ["500 万","千万","百万","大规模"]) else 2
    if any(k in text for k in ["隐瞒","不上报","偷偷","当没发生过"]): harm+=2
    if any(k in text for k in ["监管","违法","违规","处罚"]): harm+=1
    if any(k in text for k in ["理财","兑付","利息"]) and any(k in text for k in ["没钱","无法","暴雷"]): harm+=2
    if any(k in text for k in ["拆东墙补西墙","庞氏骗局"]): harm+=2
    if any(k in text for k in ["创始人","董事长","CEO","老板"]) and any(k in text for k in ["跑路","被抓","录音"]): harm+=2
    if any(k in text for k in ["丑化","侮辱","抹黑","辱华"]): harm+=2
    if any(k in text for k in ["国际品牌","外国品牌"]) and any(k in text for k in ["赚中国人的钱","抵制","滚出中国"]): harm+=2
    if any(k in text for k in ["阴间审美","文化侵略"]): harm+=1
    if any(k in text for k in ["紧急通知","内部消息"]) and any(k in text for k in ["交通管制","封路","封锁","囤物资"]): harm+=3
    if any(k in text for k in ["谣言","造谣"]): harm+=2
    if "专家" in text and any(k in text for k in ["建议","肉糜","房租","闲置"]): harm+=1
    harm=min(harm,10)
    ml_scores={"蓝":1,"黄":3,"橙":6,"红":8,"黑":10}
    trad=harm*0.5+viral*0.5
    if harm>=8: trad=trad*0.8+ml_scores.get(ml_level,5)*0.2
    elif ml_conf>=0.9: trad=trad*0.3+ml_scores.get(ml_level,5)*0.7
    elif ml_conf>0.7: trad=trad*0.5+ml_scores.get(ml_level,5)*0.5
    elif ml_conf>0.5: trad=trad*0.7+ml_scores.get(ml_level,5)*0.3
    score=round(max(1,min(10,trad)),1)
    if score>=8: level,sugg="黑","立即启动危机预案，1 小时内响应"
    elif score>=6: level,sugg="红","高度关注，2 小时内制定方案"
    elif score>=4: level,sugg="橙","建议关注，4 小时内评估"
    elif score>=2: level,sugg="黄","保持观察，24 小时内复盘"
    else: level,sugg="蓝","暂不处理，归档记录"
    return {"score":score,"level":level,"suggestion":sugg,"harm":round(harm,1),"spread":round(viral,1)}

def analyze(text:str)->Dict:
    emotion=analyze_emotion(text)
    viral=analyze_viral(text)
    ai=analyze_ai(text)
    ml=MLClassifier()
    ml_level,ml_conf=ml.predict(text)
    industry=detect_industry(text)
    risk=calc_risk(emotion["score"],viral["score"],ai["score"],text,ml_level,ml_conf)
    tags=[]
    if emotion["emotions"]: tags.append(f"情绪:{','.join(emotion['emotions'])}")
    if viral["keywords"]>3: tags.append("高传播")
    if viral["sensitive"]>0: tags.append("高敏感")
    if ai["score"]>=6: tags.append("AI 嫌疑")
    return {"risk_score":risk["score"],"risk_level":risk["level"],"suggestion":risk["suggestion"],"industry":INDUSTRY_TEMPLATES.get(industry,INDUSTRY_TEMPLATES["workplace"])["name"],"ml_prediction":{"level":ml_level,"confidence":ml_conf},"dimensions":{"emotion":emotion,"viral":viral,"ai":ai},"matrix":{"harm":risk["harm"],"spread":risk["spread"]},"tags":tags or ["常规"]}

def format_report(r:Dict)->str:
    emoji={"黑":"⚫","红":"🔴","橙":"🟠","黄":"🟡","蓝":"🔵"}
    e,v,a,m=r["dimensions"]["emotion"],r["dimensions"]["viral"],r["dimensions"]["ai"],r["matrix"]
    return "\n".join(["="*60,"📊 声誉体温报告 v4.1 (精简版)","="*60,f"风险等级：{emoji.get(r['risk_level'],'⚪')} {r['risk_level']}级 | 评分：{r['risk_score']}/10",f"处理建议：{r['suggestion']}",f"行业：{r['industry']} | ML: {r['ml_prediction']['level']}级 ({int(r['ml_prediction']['confidence']*100)}%)",f"标签：{' | '.join(r['tags'])}","","维度分析:",f"  • 情绪：{e['score']}/10 ({','.join(e['emotions']) or '无'})",f"  • 传播：{v['score']}/10 (关键词:{v['keywords']},敏感:{v['sensitive']})",f"  • AI 嫌疑：{a['score']}/10 (模式:{a['patterns']})","","二维矩阵:",f"  危害力：{m['harm']}/10 | 传播力：{m['spread']}/10","="*60])

def main():
    import argparse
    parser=argparse.ArgumentParser(description='声誉体温计 v4.1')
    parser.add_argument('text',nargs='?',help='分析文本')
    parser.add_argument('--json','-j',action='store_true',help='仅 JSON')
    args=parser.parse_args()
    text=args.text if args.text else (sys.stdin.read().strip() if not sys.stdin.isatty() else "")
    if not text: print(json.dumps({"error":"请提供文本"},ensure_ascii=False,indent=2)); sys.exit(1)
    r=analyze(text)
    print(json.dumps(r,ensure_ascii=False,indent=2) if args.json else format_report(r))

if __name__=="__main__": main()
