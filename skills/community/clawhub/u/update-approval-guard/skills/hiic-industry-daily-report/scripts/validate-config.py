#!/usr/bin/env python3
"""
HIIC日报配置验证脚本
验证配置文件是否符合 schema 规范
"""

import json
import sys
from pathlib import Path

def validate_json_file(file_path):
    """验证JSON文件格式是否正确"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSON格式错误: {e}"
    except FileNotFoundError:
        return False, f"文件不存在"
    except Exception as e:
        return False, f"未知错误: {e}"

def validate_industries_config(config):
    """验证产业配置"""
    errors = []
    
    if 'industries' not in config:
        errors.append("缺少 'industries' 字段")
        return errors
    
    for i, industry in enumerate(config['industries']):
        # 必需字段
        required_fields = ['id', 'name', 'keywords', 'topics', 'enabled']
        for field in required_fields:
            if field not in industry:
                errors.append(f"产业 {i}: 缺少必需字段 '{field}'")
        
        # 类型检查
        if 'keywords' in industry and not isinstance(industry['keywords'], list):
            errors.append(f"产业 {i}: 'keywords' 必须是数组")
        
        if 'topics' in industry and not isinstance(industry['topics'], list):
            errors.append(f"产业 {i}: 'topics' 必须是数组")
        
        if 'enabled' in industry and not isinstance(industry['enabled'], bool):
            errors.append(f"产业 {i}: 'enabled' 必须是布尔值")
    
    return errors

def validate_sources_config(config):
    """验证数据源配置"""
    errors = []
    
    if 'sources' not in config:
        errors.append("缺少 'sources' 字段")
        return errors
    
    for i, source in enumerate(config['sources']):
        # 必需字段
        required_fields = ['id', 'type', 'name', 'enabled']
        for field in required_fields:
            if field not in source:
                errors.append(f"数据源 {i}: 缺少必需字段 '{field}'")
        
        # 类型检查
        valid_types = ['rss', 'twitter', 'web', 'github', 'reddit']
        if 'type' in source and source['type'] not in valid_types:
            errors.append(f"数据源 {i}: 'type' 必须是 {valid_types} 之一")
        
        # RSS源必须有URL
        if source.get('type') == 'rss' and 'url' not in source:
            errors.append(f"数据源 {i}: RSS源必须有 'url' 字段")
    
    return errors

def validate_topics_config(config):
    """验证主题配置"""
    errors = []
    
    if 'topics' not in config:
        errors.append("缺少 'topics' 字段")
        return errors
    
    for i, topic in enumerate(config['topics']):
        # 必需字段
        required_fields = ['id', 'label']
        for field in required_fields:
            if field not in topic:
                errors.append(f"主题 {i}: 缺少必需字段 '{field}'")
    
    return errors

def main():
    """主函数"""
    config_dir = Path(__file__).parent.parent / 'config' / 'defaults'
    
    print("=== HIIC日报配置验证 ===\n")
    
    all_valid = True
    
    # 验证 industries.json
    print("📄 验证 industries.json...")
    industries_path = config_dir / 'industries.json'
    valid, error = validate_json_file(industries_path)
    
    if valid:
        with open(industries_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        errors = validate_industries_config(config)
        
        if errors:
            print("❌ 验证失败:")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
        else:
            print(f"✅ 验证通过 ({len(config['industries'])} 个产业)")
    else:
        print(f"❌ {error}")
        all_valid = False
    
    print()
    
    # 验证 sources.json
    print("📄 验证 sources.json...")
    sources_path = config_dir / 'sources.json'
    valid, error = validate_json_file(sources_path)
    
    if valid:
        with open(sources_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        errors = validate_sources_config(config)
        
        if errors:
            print("❌ 验证失败:")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
        else:
            enabled_count = sum(1 for s in config['sources'] if s.get('enabled', False))
            print(f"✅ 验证通过 ({enabled_count}/{len(config['sources'])} 个数据源启用)")
    else:
        print(f"❌ {error}")
        all_valid = False
    
    print()
    
    # 验证 topics.json
    print("📄 验证 topics.json...")
    topics_path = config_dir / 'topics.json'
    valid, error = validate_json_file(topics_path)
    
    if valid:
        with open(topics_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        errors = validate_topics_config(config)
        
        if errors:
            print("❌ 验证失败:")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
        else:
            print(f"✅ 验证通过 ({len(config['topics'])} 个主题)")
    else:
        print(f"❌ {error}")
        all_valid = False
    
    print()
    
    if all_valid:
        print("🎉 所有配置验证通过！")
        sys.exit(0)
    else:
        print("❌ 配置验证失败，请修复上述错误")
        sys.exit(1)

if __name__ == "__main__":
    main()
