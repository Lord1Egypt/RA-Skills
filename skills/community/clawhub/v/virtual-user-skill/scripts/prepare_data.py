#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据准备脚本 - 将 Excel 数据转换为加密格式并生成向量

使用方式：
    python prepare_data.py your_data.xlsx

输出：
    - data/scenario_library.json.enc（加密的场景库）
    - data/scenario_embeddings.npy（预计算的向量）
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from encrypt import EncryptManager


def load_excel_data(excel_file: str) -> list:
    """
    加载 Excel 数据
    
    Args:
        excel_file: Excel 文件路径
    
    Returns:
        list: 场景数据列表
    """
    print(f"📂 加载 Excel 文件：{excel_file}")
    
    # 读取 Excel（只读取 Sheet1）
    df = pd.read_excel(excel_file, sheet_name='Sheet1')
    
    print(f"✅ 加载完成，共 {len(df)} 条记录")
    print(f"📊 字段：{list(df.columns)}")
    
    # 转换为字典列表
    scenarios = df.to_dict('records')
    
    return scenarios


def preprocess_scenario(scenario: dict) -> dict:
    """
    预处理场景数据
    
    Args:
        scenario: 原始场景数据
    
    Returns:
        dict: 预处理后的场景数据
    """
    # 标准化字段名（根据你的 Excel 字段调整）
    processed = {
        '序号': scenario.get('序号', ''),
        '用户姓名和背景信息': scenario.get('用户姓名和背景信息', ''),
        '内容范围': scenario.get('内容范围', ''),
        '是否出境游': scenario.get('是否出境游', ''),
        '用户具体场景': scenario.get('用户具体场景', ''),
        '任务': scenario.get('任务', ''),
        '期待效果': scenario.get('期待效果', ''),
        '当前方案': scenario.get('当前方案', ''),
        '爽点': scenario.get('爽点', ''),
        '痛点': scenario.get('痛点', ''),
        '改进方向': scenario.get('改进方向', ''),
        '底层需求': scenario.get('底层需求', '')
    }
    
    return processed


def generate_vector_text(scenario: dict) -> str:
    """
    生成用于向量化的文本
    
    Args:
        scenario: 场景数据
    
    Returns:
        str: 向量化文本
    """
    # 组合关键字段用于向量化
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
    
    return " | ".join(text_parts)


def compute_embeddings(scenarios: list, model_name: str = 'shibing624/text2vec-base-chinese') -> np.ndarray:
    """
    计算场景向量
    
    Args:
        scenarios: 场景数据列表
        model_name: 向量化模型名称
    
    Returns:
        np.ndarray: 向量矩阵
    """
    print(f"🤖 加载向量化模型：{model_name}")
    model = SentenceTransformer(model_name)
    
    print("📐 计算向量...")
    # 生成向量化文本
    texts = [generate_vector_text(s) for s in scenarios]
    
    # 计算向量
    embeddings = model.encode(texts, show_progress_bar=True)
    
    print(f"✅ 向量计算完成，形状：{embeddings.shape}")
    
    return embeddings


def save_encrypted_data(scenarios: list, output_file: str):
    """
    保存加密的场景库数据
    
    Args:
        scenarios: 场景数据列表
        output_file: 输出文件路径
    """
    print(f"🔒 加密场景库数据...")
    
    # 转换为 JSON
    json_data = json.dumps(scenarios, ensure_ascii=False, indent=2)
    
    # 加密
    manager = EncryptManager()
    encrypted = manager.encrypt_data(json_data.encode('utf-8'))
    
    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted)
    
    print(f"✅ 已保存加密数据：{output_file}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python prepare_data.py <excel_file>")
        print("示例：python prepare_data.py scenario_library.xlsx")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    # 检查文件是否存在
    if not Path(excel_file).exists():
        print(f"❌ 文件不存在：{excel_file}")
        sys.exit(1)
    
    # 输出目录
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 加载 Excel 数据
    scenarios_raw = load_excel_data(excel_file)
    
    # 2. 预处理数据
    print("\n📝 预处理数据...")
    scenarios = [preprocess_scenario(s) for s in scenarios_raw]
    
    # 3. 计算向量
    print("\n📐 计算向量...")
    embeddings = compute_embeddings(scenarios)
    
    # 4. 保存加密数据
    print("\n🔒 保存数据...")
    encrypted_file = output_dir / "scenario_library.json.enc"
    save_encrypted_data(scenarios, str(encrypted_file))
    
    # 5. 保存向量
    embeddings_file = output_dir / "scenario_embeddings.npy"
    np.save(str(embeddings_file), embeddings)
    print(f"✅ 已保存向量：{embeddings_file}")
    
    # 6. 保存示例数据（可选，用于测试）
    sample_file = output_dir / "sample_scenarios.json"
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(scenarios[:5], f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存示例数据（前 5 条）：{sample_file}")
    
    print("\n" + "=" * 60)
    print("✅ 数据准备完成！")
    print("=" * 60)
    print(f"\n输出文件：")
    print(f"  - {encrypted_file}（加密的场景库）")
    print(f"  - {embeddings_file}（预计算的向量）")
    print(f"  - {sample_file}（示例数据，用于测试）")
    print(f"\n下一步：")
    print(f"  python src/main.py \"测试问题\"")


if __name__ == "__main__":
    main()
