#!/usr/bin/env python3
"""
智能门店选址引擎 (Smart Site Selection) - 主入口脚本
强制执行物理阻断机制，先追问用户补充参数，再生成报告
"""

import os
import sys
import json

# 检查环境变量
AMAP_KEY = os.environ.get('AMAP_WEBSERVICE_KEY')
if not AMAP_KEY:
    print("❌ 缺少环境变量 AMAP_WEBSERVICE_KEY")
    print("   请执行：export AMAP_WEBSERVICE_KEY=你的 key")
    sys.exit(1)

def check_required_params(user_input: str) -> dict:
    """
    检查用户输入是否包含必要参数（选址空间战略导向）
    Returns: {'has_audience': bool, 'has_strategy': bool, 'extracted': dict}
    """
    result = {
        'has_audience': False,
        'has_strategy': False,
        'audience_type': None,
        'strategy_type': None
    }
    
    # 检查客群定位关键词
    audience_keywords = ['学生', '白领', '商务', '社区', '居民', '高净值', '高端', '年轻人', '家庭']
    
    for keyword in audience_keywords:
        if keyword in user_input:
            result['has_audience'] = True
            result['audience_type'] = keyword
            break
    
    # 检查经营战略关键词
    strategy_keywords = ['外卖', '快取', '档口', '堂食', '社交', '体验', '旗舰', '大型', '小型', '精品']
    
    for keyword in strategy_keywords:
        if keyword in user_input:
            result['has_strategy'] = True
            result['strategy_type'] = keyword
            break
    
    return result


def generate_proactive_question(business_type: str) -> str:
    """根据业态生成针对性的追问问题（选址空间战略导向）"""
    
    # 默认问题（核心客群 + 经营战略）
    default_questions = [
        '您的核心客群定位是什么？（如：学生党/商务白领/社区居民/高净值人群）',
        '您的门店经营战略是什么？（如：外卖为主/快取档口店/社交体验旗舰店）'
    ]
    
    question_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 选址需求补充（必填项）

为了给您生成精准的商业选址报告，请补充以下 2 项核心信息：

① {default_questions[0]}
② {default_questions[1]}

💡 示例回复：
   "商务白领为主，快取档口店"
   或
   "学生党，外卖 + 堂食"
   或
   "社区居民，社交体验店"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return question_text.strip()


def main():
    """主执行流程"""
    print("\n" + "="*70)
    print("  智能门店选址引擎 (Smart Site Selection)")
    print("  v1.0.0 - SkillHub Release")
    print("="*70 + "\n")
    
    # 获取用户输入（从命令行参数或环境）
    user_input = os.environ.get('SITE_SELECTION_INPUT', '')
    
    if not user_input:
        print("❌ 未检测到选址需求输入")
        print("\n使用方法:")
        print("  export SITE_SELECTION_INPUT='我想在上海静安区开一家普拉提馆'")
        print("  python3 main.py")
        print("\n或在对话中直接触发技能")
        sys.exit(1)
    
    print(f"📝 用户需求：{user_input}\n")
    
    # 阶段 A：物理阻断检查
    print("【阶段 A】物理阻断与参数校验")
    
    params = check_required_params(user_input)
    
    # 提取业态类型
    business_type = user_input
    for keyword in ['开一家', '开一个', '开家', '开店', '做']:
        if keyword in business_type:
            business_type = business_type.split(keyword)[-1]
            break
    
    # 检查是否需要追问
    if not params['has_audience'] or not params['has_strategy']:
        print("  ❌ 缺失核心参数")
        print(f"     核心客群定位：{'✓' if params['has_audience'] else '✗'}")
        print(f"     门店经营战略：{'✓' if params['has_strategy'] else '✗'}")
        print()
        
        # 生成追问问题
        question = generate_proactive_question(business_type)
        
        print("【物理阻断激活】")
        print("  → 调用 proactive-agent 发送追问")
        print("  → 结束当前对话回合，等待用户补充")
        print()
        print(question)
        print()
        print("⏸️  已暂停，等待用户回复后再次触发...")
        
        # 保存追问状态
        state = {
            'status': 'waiting_for_input',
            'user_input': user_input,
            'business_type': business_type,
            'missing': {
                'audience': not params['has_audience'],
                'strategy': not params['has_strategy']
            }
        }
        
        state_file = '/tmp/site_selection_state.json'
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 状态已保存：{state_file}")
        sys.exit(0)
    
    # 参数齐全，继续执行
    print("  ✓ 核心客群定位：已提供")
    print("  ✓ 门店经营战略：已提供")
    print("  ✓ 参数齐全，进入阶段 B")
    print()
    
    # 阶段 B：坐标猎取（调用 Python 引擎）
    print("【阶段 B】坐标猎取 → 移交 Python 引擎")
    
    # 这里调用实际的选址引擎
    # 由于需要动态导入，使用 subprocess 或延迟导入
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
        from site_selection_engine import run_selection_engine
        
        # 注意：实际使用时需要从用户输入或配置中获取以下参数
        # 这里仅做演示，实际需要完整的参数传递逻辑
        
        print("\n⚠️  完整报告生成需要以下参数:")
        print("   - keyword: 业态关键词（如 '普拉提馆'）")
        print("   - broad_keyword: 防挂零降级词（如 '健身房'）")
        print("   - city: 城市 + 区域（如 '上海市静安区'）")
        print("   - raw_locations: Top 3 地段坐标列表")
        print("   - macro_insight: 宏观市场研判文本")
        print("   - amap_key: 高德 API Key")
        print()
        print("📄 完整流程请参考 scripts/site_selection_engine.py")
        
    except Exception as e:
        print(f"⚠️ 引擎调用异常：{e}")
        print("   请确保已安装依赖：pip install requests matplotlib")
    
    print()
    print("="*70)
    print("✅ 阶段 A 完成")
    print("="*70)


if __name__ == "__main__":
    main()
