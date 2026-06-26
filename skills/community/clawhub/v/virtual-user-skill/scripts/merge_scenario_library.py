#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场景库合并处理脚本 - 处理新增的 27 个 Excel 文件

功能：
1. 读取所有 Excel 文件并合并
2. 脱敏处理（公司名→"旅行平台"，姓名→英文名）
3. 情绪标签提取（固定分类）
4. 数据去重
5. 加密存储

使用方式：
    python3 merge_scenario_library.py

输出：
    - data/scenario_library.json.enc（加密的场景库）
    - data/scenario_embeddings.npy（预计算的向量）
    - outputs/merge_report.md（处理报告）
"""

import sys
import json
import random
import hashlib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
import re

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from encrypt import EncryptManager


# ==================== 配置区 ====================

# 下载目录
DOWNLOADS_DIR = Path.home() / "Downloads"

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "data"
REPORTS_DIR = Path(__file__).parent.parent / "outputs"

# 向量化模型
MODEL_NAME = 'shibing624/text2vec-base-chinese'

# 需要排除的文件（重复文件）
EXCLUDE_FILES = [
    '出境游专项 3719-已上传 AI studio (1).xlsx',  # 重复文件
]


# ==================== 情绪标签分类体系 ====================

EMOTION_CATEGORIES = {
    '愤怒': ['愤怒', '生气', '恼火', '不满', '气愤', '怒火', '暴躁'],
    '焦虑': ['焦虑', '着急', '紧张', '担忧', '不安', '恐慌', '急躁', '紧迫'],
    '失望': ['失望', '沮丧', '失落', '灰心', '绝望', '无奈', '遗憾'],
    '困惑': ['困惑', '迷茫', '不解', '疑惑', '糊涂', '搞不懂', '莫名其妙'],
    '满意': ['满意', '开心', '高兴', '愉快', '舒适', '顺心', '如意'],
    '惊喜': ['惊喜', '意外', '惊喜', '赞叹', '惊艳', '出乎意料'],
    '感激': ['感激', '感谢', '感动', '欣慰', '温暖'],
    '疲惫': ['疲惫', '累', '辛苦', '疲倦', '乏力', '心力交瘁'],
    '期待': ['期待', '盼望', '希望', '憧憬', '向往'],
    '中性': ['中性', '平静', '客观', '陈述']
}

EMOTION_LABELS = list(EMOTION_CATEGORIES.keys())


# ==================== 英文名映射表 ====================

LAST_NAME_MAP = {
    '廖': 'Johnson', '沈': 'Smith', '张': 'Williams', '王': 'Brown', '李': 'Jones',
    '刘': 'Garcia', '陈': 'Miller', '杨': 'Davis', '赵': 'Rodriguez', '黄': 'Martinez',
    '周': 'Hernandez', '吴': 'Lopez', '徐': 'Gonzalez', '孙': 'Wilson', '胡': 'Anderson',
    '朱': 'Thomas', '马': 'Moore', '高': 'Jackson', '林': 'Martin', '何': 'Lee',
    '郭': 'Perez', '罗': 'Thompson', '郑': 'White', '梁': 'Harris', '谢': 'Sanchez',
    '宋': 'Clark', '唐': 'Ramirez', '许': 'Lewis', '韩': 'Robinson', '冯': 'Walker',
    '邓': 'Young', '曹': 'Allen', '彭': 'King', '曾': 'Wright', '萧': 'Scott',
    '田': 'Torres', '董': 'Nguyen', '袁': 'Hill', '潘': 'Flores', '蔡': 'Green',
    '蒋': 'Adams', '余': 'Nelson', '杜': 'Baker', '叶': 'Hall', '程': 'Rivera',
    '魏': 'Campbell', '吕': 'Mitchell', '丁': 'Carter', '任': 'Roberts', '姚': 'Gomez',
    '卢': 'Phillips', '傅': 'Evans', '钟': 'Turner', '汪': 'Diaz', '谭': 'Parker',
    '邹': 'Cruz', '石': 'Edwards', '熊': 'Collins', '金': 'Reyes', '邱': 'Stewart',
    '侯': 'Morris', '邵': 'Morales', '孟': 'Murphy', '龙': 'Cook', '段': 'Rogers',
    '雷': 'Gutierrez', '钱': 'Ortiz', '汤': 'Morgan', '尹': 'Cooper', '黎': 'Peterson',
    '易': 'Bailey', '常': 'Reed', '武': 'Kelly', '乔': 'Howard', '贺': 'Ramos',
    '赖': 'Kim', '龚': 'Cox', '文': 'Ward', '樊': 'Richardson', '兰': 'Watson',
    '殷': 'Brooks', '施': 'Chavez', '洪': 'Wood', '包': 'James', '诸': 'Bennett',
    '毕': 'Mendoza', '狄': 'Ruiz', '计': 'Hughes', '成': 'Price', '戴': 'Alvarez',
    '盛': 'Castillo', '滕': 'Sanders', '严': 'Patel', '迟': 'Myers', '尤': 'Long',
    '屈': 'Ross', '花': 'Foster', '莫': 'Jimenez', '谈': 'Powell', '茅': 'Jenkins',
    '浦': 'Perry', '费': 'Powell', '柏': 'Long', '窦': 'Patterson', '章': 'Hughes',
    '干': 'Flores', '景': 'Washington', '全': 'Butler', '米': 'Simmons', '贝': 'Foster',
    '边': 'Gonzales', '胥': 'Alexander', '南': 'Russell', '党': 'Griffin', '燕': 'Diaz',
    '冀': 'Hayes', '练': 'Myers', '楼': 'Ford', '解': 'Graham', '应': 'Sullivan',
    '宗': 'Wallace', '欧': 'Woods', '耿': 'Cole', '向': 'Jordan', '匡': 'Reynolds',
    '国': 'Fisher', '戎': 'Harrison', '后': 'Gibson', '邬': 'Mcdonald', '冷': 'Cruz',
    '晏': 'Marshall', '席': 'Ortiz', '危': 'Gomez', '和': 'Murray', '邰': 'Freeman',
    '井': 'Wells', '印': 'Webb', '农': 'Simpson', '能': 'Stevens', '劳': 'Tucker',
    '盖': 'Porter', '益': 'Hunter', '衡': 'Hicks', '步': 'Crawford', '都': 'Henry',
    '弘': 'Mason', '库': 'Morales', '乜': 'Kennedy', '过': 'Warren', '运': 'Dixon',
    '那': 'Ramos', '第五': 'Burns',
}

FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Donald', 'Sandra', 'Mark', 'Ashley',
    'Paul', 'Kimberly', 'Steven', 'Emily', 'Andrew', 'Donna', 'Kenneth', 'Michelle',
    'Joshua', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa',
    'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
    'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Gary', 'Nicholas', 'Angela',
    'Eric', 'Shirley', 'Jonathan', 'Anna', 'Stephen', 'Brenda', 'Larry', 'Pamela',
    'Justin', 'Emma', 'Scott', 'Nicole', 'Brandon', 'Helen'
]


# ==================== 工具函数 ====================

def safe_str(value) -> str:
    """安全转换为字符串，处理 NaN 和 float"""
    if pd.isna(value):
        return ''
    return str(value)


def extract_last_name(chinese_name: str) -> str:
    """从中文姓名中提取姓氏"""
    double_surnames = ['第五', '欧阳', '司马', '上官', '诸葛', '夏侯', '东方', '皇甫']
    
    for surname in double_surnames:
        if chinese_name.startswith(surname):
            return surname
    
    if chinese_name and chinese_name[0] in LAST_NAME_MAP:
        return chinese_name[0]
    
    return None


def anonymize_name(chinese_name: str, name_cache: dict) -> str:
    """将中文姓名替换为英文名"""
    if not chinese_name or chinese_name.strip() == '':
        return ''
    
    if chinese_name in name_cache:
        return name_cache[chinese_name]
    
    last_name = extract_last_name(chinese_name)
    en_last = LAST_NAME_MAP.get(last_name, 'Smith') if last_name else 'Smith'
    en_first = random.choice(FIRST_NAMES)
    en_name = f"{en_first} {en_last}"
    
    name_cache[chinese_name] = en_name
    return en_name


def sanitize_text(text: str) -> str:
    """脱敏处理：替换敏感词汇"""
    if not text:
        return ''
    
    sensitive_words = {
        '飞猪': '旅行平台',
        '阿里': '旅行平台',
        '阿里巴巴': '旅行平台',
        '淘宝': '旅行平台',
        '千问': '旅行平台',
        '天猫': '旅行平台',
        '支付宝': '支付平台',
        '高德': '地图平台',
        '饿了么': '外卖平台',
        '盒马': '零售平台',
        '菜鸟': '物流平台',
        '钉钉': '办公平台',
        '优酷': '视频平台',
        '虾米': '音乐平台',
        '闲鱼': '二手平台',
        '1688': '批发平台',
        '聚划算': '团购平台',
        '口碑': '本地生活平台',
        '考拉': '跨境电商平台',
        'Lazada': '电商平台',
        '速卖通': '跨境电商平台',
        '国际站': '跨境电商平台',
        '中国站': '国内平台',
        '蚂蚁': '金融平台',
        '网商': '金融平台',
        '网商银行': '网上银行',
        '花呗': '消费信贷',
        '借呗': '消费信贷',
        '余额宝': '理财产品',
        '余利宝': '理财产品',
        '相互宝': '互助平台',
        '好医保': '保险产品',
        '相互险': '保险产品',
    }
    
    result = text
    for sensitive, replacement in sensitive_words.items():
        result = result.replace(sensitive, replacement)
    
    return result


def extract_emotion_label(scenario: dict) -> str:
    """从场景中提取情绪标签"""
    text_parts = []
    for field in ['痛点', '爽点', '用户具体场景', '任务', '底层需求', '期待效果']:
        value = scenario.get(field)
        if value:
            text_parts.append(safe_str(value))
    
    full_text = ' '.join(text_parts)
    
    emotion_priority = ['愤怒', '焦虑', '失望', '困惑', '惊喜', '感激', '满意', '期待', '疲惫', '中性']
    
    for emotion in emotion_priority:
        keywords = EMOTION_CATEGORIES[emotion]
        for keyword in keywords:
            if keyword in full_text:
                return emotion
    
    return '中性'


def generate_record_hash(scenario: dict) -> str:
    """生成记录的唯一 Hash（用于去重）"""
    key_fields = ['用户姓名和背景信息', '用户具体场景', '任务', '痛点', '底层需求']
    
    hash_content = '|'.join([
        safe_str(scenario.get(field, '')) for field in key_fields
    ])
    
    return hashlib.md5(hash_content.encode('utf-8')).hexdigest()


def load_all_excel_files() -> list:
    """加载所有 Excel 文件并合并"""
    print("\n" + "=" * 60)
    print("📂 步骤 1: 加载所有 Excel 文件")
    print("=" * 60)
    
    excel_files = [f for f in DOWNLOADS_DIR.iterdir() 
                   if f.suffix == '.xlsx' and not f.name.startswith('.')]
    
    excel_files = [f for f in excel_files if f.name not in EXCLUDE_FILES]
    
    print(f"📁 找到 {len(excel_files)} 个 Excel 文件（已排除 {len(EXCLUDE_FILES)} 个重复文件）")
    
    all_scenarios = []
    file_stats = []
    
    for i, file_path in enumerate(sorted(excel_files), 1):
        try:
            print(f"\n[{i}/{len(excel_files)}] 读取：{file_path.name}")
            
            # 自动检测第一个 Sheet
            xl_file = pd.ExcelFile(file_path)
            sheet_name = xl_file.sheet_names[0]
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            scenarios = df.to_dict('records')
            
            for s in scenarios:
                s['_source_file'] = file_path.name
            
            all_scenarios.extend(scenarios)
            
            file_stats.append({
                'file': file_path.name,
                'rows': len(scenarios)
            })
            
            print(f"   ✅ 加载 {len(scenarios)} 条记录 (Sheet: {sheet_name})")
            
        except Exception as e:
            print(f"   ❌ 读取失败：{e}")
            file_stats.append({
                'file': file_path.name,
                'rows': 0,
                'error': str(e)
            })
    
    print(f"\n✅ 总计加载：{len(all_scenarios)} 条记录")
    
    return all_scenarios, file_stats


def preprocess_data(scenarios: list) -> list:
    """预处理数据：脱敏、情绪标签"""
    print("\n" + "=" * 60)
    print("📝 步骤 2: 数据预处理（脱敏 + 情绪标签）")
    print("=" * 60)
    
    name_cache = {}
    processed_scenarios = []
    
    for i, scenario in enumerate(scenarios, 1):
        if i % 5000 == 0:
            print(f"   处理进度：{i}/{len(scenarios)} ({i/len(scenarios)*100:.1f}%)")
        
        # 1. 标准化字段
        processed = {
            '序号': safe_str(scenario.get('序号', '')),
            '用户姓名和背景信息': safe_str(scenario.get('用户姓名和背景信息', '')),
            '内容范围': safe_str(scenario.get('内容范围', '')),
            '是否出境游': safe_str(scenario.get('是否出境游', '')),
            '用户具体场景': safe_str(scenario.get('用户具体场景', '')),
            '任务': safe_str(scenario.get('任务', '')),
            '期待效果': safe_str(scenario.get('期待效果', '')),
            '当前方案': safe_str(scenario.get('当前方案', '')),
            '爽点': safe_str(scenario.get('爽点', '')),
            '痛点': safe_str(scenario.get('痛点', '')),
            '改进方向': safe_str(scenario.get('改进方向', '')),
            '底层需求': safe_str(scenario.get('底层需求', '')),
            '场景总分': safe_str(scenario.get('场景总分', '')),
            '质量分明细': safe_str(scenario.get('质量分明细', '')),
        }
        
        # 2. 脱敏处理：公司名
        for field in ['用户姓名和背景信息', '用户具体场景', '任务', '当前方案', '改进方向']:
            if processed.get(field):
                processed[field] = sanitize_text(processed[field])
        
        # 3. 脱敏处理：姓名
        if processed.get('用户姓名和背景信息'):
            name_match = re.search(r'姓名\[([^\]]+)\]', processed['用户姓名和背景信息'])
            if name_match:
                chinese_name = name_match.group(1)
                en_name = anonymize_name(chinese_name, name_cache)
                processed['用户姓名和背景信息'] = processed['用户姓名和背景信息'].replace(
                    f'姓名[{chinese_name}]', f'姓名[{en_name}]'
                )
        
        # 4. 情绪标签
        processed['情绪标签'] = extract_emotion_label(scenario)
        
        # 5. 生成 Hash
        processed['_record_hash'] = generate_record_hash(processed)
        
        # 6. 保留来源文件
        processed['_source_file'] = scenario.get('_source_file', '')
        
        processed_scenarios.append(processed)
    
    print(f"\n✅ 预处理完成：{len(processed_scenarios)} 条记录")
    print(f"   姓名缓存：{len(name_cache)} 个唯一姓名")
    
    return processed_scenarios


def deduplicate_scenarios(scenarios: list) -> list:
    """去重处理"""
    print("\n" + "=" * 60)
    print("🔄 步骤 3: 数据去重")
    print("=" * 60)
    
    hash_map = {}
    unique_scenarios = []
    duplicate_count = 0
    
    for scenario in scenarios:
        record_hash = scenario['_record_hash']
        
        if record_hash not in hash_map:
            hash_map[record_hash] = scenario
            unique_scenarios.append(scenario)
        else:
            duplicate_count += 1
    
    print(f"   原始数据：{len(scenarios)} 条")
    print(f"   去重后：{len(unique_scenarios)} 条")
    print(f"   重复数据：{duplicate_count} 条")
    
    return unique_scenarios


def compute_embeddings(scenarios: list) -> np.ndarray:
    """计算场景向量"""
    print("\n" + "=" * 60)
    print("📐 步骤 4: 计算向量")
    print("=" * 60)
    
    print(f"🤖 加载向量化模型：{MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    
    print("📐 计算向量...")
    
    texts = []
    for scenario in scenarios:
        text_parts = []
        
        if scenario.get('用户具体场景'):
            text_parts.append(f"场景：{scenario['用户具体场景']}")
        
        if scenario.get('任务'):
            text_parts.append(f"任务：{scenario['任务']}")
        
        if scenario.get('痛点'):
            text_parts.append(f"痛点：{scenario['痛点']}")
        
        if scenario.get('底层需求'):
            text_parts.append(f"需求：{scenario['底层需求']}")
        
        if scenario.get('用户姓名和背景信息'):
            text_parts.append(f"用户：{scenario['用户姓名和背景信息']}")
        
        texts.append(" | ".join(text_parts))
    
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    print(f"✅ 向量计算完成，形状：{embeddings.shape}")
    
    return embeddings


def save_encrypted_data(scenarios: list, output_file: str):
    """保存加密的场景库数据"""
    print("\n" + "=" * 60)
    print("🔒 步骤 5: 加密保存")
    print("=" * 60)
    
    clean_scenarios = []
    for scenario in scenarios:
        clean = {k: v for k, v in scenario.items() if not k.startswith('_')}
        clean_scenarios.append(clean)
    
    json_data = json.dumps(clean_scenarios, ensure_ascii=False, indent=2)
    
    manager = EncryptManager()
    encrypted = manager.encrypt_data(json_data.encode('utf-8'))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted)
    
    print(f"✅ 已保存加密数据：{output_file}")
    print(f"   数据量：{len(clean_scenarios)} 条")


def generate_report(file_stats: list, scenarios: list, unique_scenarios: list):
    """生成处理报告"""
    print("\n" + "=" * 60)
    print("📊 步骤 6: 生成报告")
    print("=" * 60)
    
    emotion_stats = {}
    for scenario in unique_scenarios:
        emotion = scenario.get('情绪标签', '中性')
        emotion_stats[emotion] = emotion_stats.get(emotion, 0) + 1
    
    report = f"""# 场景库合并处理报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 处理概览

| 指标 | 数值 |
|:---|:---|
| 处理文件数 | {len(file_stats)} 个 |
| 原始数据量 | {len(scenarios):,} 条 |
| 去重后数据量 | {len(unique_scenarios):,} 条 |
| 重复数据 | {len(scenarios) - len(unique_scenarios):,} 条 |
| 去重比例 | {(len(scenarios) - len(unique_scenarios)) / len(scenarios) * 100:.2f}% |

---

## 📁 文件处理详情

| 序号 | 文件名 | 行数 | 状态 |
|:---|:---|:---|:---|
"""
    
    for i, stat in enumerate(file_stats, 1):
        status = '✅ 成功' if stat['rows'] > 0 else f"❌ 失败：{stat.get('error', '未知')}"
        report += f"| {i} | {stat['file']} | {stat['rows']:,} | {status} |\n"
    
    report += f"""
---

## 😊 情绪标签分布

| 情绪标签 | 数量 | 占比 |
|:---|:---|:---|
"""
    
    for emotion in sorted(emotion_stats.keys(), key=lambda x: emotion_stats[x], reverse=True):
        count = emotion_stats[emotion]
        ratio = count / len(unique_scenarios) * 100
        report += f"| {emotion} | {count:,} | {ratio:.2f}% |\n"
    
    report += f"""
---

## 🔧 处理说明

### 脱敏规则
1. **公司名替换**: 飞猪/阿里/淘宝/天猫等 → "旅行平台"
2. **姓名替换**: 中文姓名 → 英文名（随机生成，保持一致性）

### 情绪标签分类
- 愤怒、焦虑、失望、困惑、满意、惊喜、感激、疲惫、期待、中性

### 去重规则
- 基于关键字段 Hash：用户姓名和背景信息 + 用户具体场景 + 任务 + 痛点 + 底层需求
- Hash 相同视为重复数据

---

## ✅ 输出文件

- `data/scenario_library.json.enc` - 加密的场景库
- `data/scenario_embeddings.npy` - 预计算的向量
- `outputs/merge_report.md` - 处理报告（本文件）

---

**处理完成！** 🎉
"""
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / "merge_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 已保存报告：{report_file}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🚀 场景库合并处理脚本")
    print("=" * 60)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 加载所有 Excel 文件
    scenarios, file_stats = load_all_excel_files()
    
    if not scenarios:
        print("\n❌ 没有加载到任何数据，退出")
        sys.exit(1)
    
    # 2. 预处理数据（脱敏 + 情绪标签）
    processed_scenarios = preprocess_data(scenarios)
    
    # 3. 去重处理
    unique_scenarios = deduplicate_scenarios(processed_scenarios)
    
    # 4. 计算向量
    embeddings = compute_embeddings(unique_scenarios)
    
    # 5. 保存加密数据
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    encrypted_file = OUTPUT_DIR / "scenario_library.json.enc"
    save_encrypted_data(unique_scenarios, str(encrypted_file))
    
    # 6. 保存向量
    embeddings_file = OUTPUT_DIR / "scenario_embeddings.npy"
    np.save(str(embeddings_file), embeddings)
    print(f"✅ 已保存向量：{embeddings_file}")
    
    # 7. 生成报告
    generate_report(file_stats, processed_scenarios, unique_scenarios)
    
    # 8. 保存示例数据（前 5 条）
    sample_file = OUTPUT_DIR / "sample_scenarios.json"
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(unique_scenarios[:5], f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存示例数据（前 5 条）：{sample_file}")
    
    print("\n" + "=" * 60)
    print("✅ 场景库合并处理完成！")
    print("=" * 60)
    print(f"\n输出文件：")
    print(f"  - {encrypted_file}（加密的场景库）")
    print(f"  - {embeddings_file}（预计算的向量）")
    print(f"  - {REPORTS_DIR / 'merge_report.md'}（处理报告）")
    print(f"\n下一步：")
    print(f"  python3 src/main.py \"测试问题\"")
    
    print(f"\n结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    random.seed(42)
    main()
