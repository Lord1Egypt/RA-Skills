#!/usr/bin/env python3
"""
Soul Memory Keyword Mapping v3.3 - Generic/Universal Schema
核心改進：分層關鍵詞字典 + 權重化標籤
特性：使用通用術語，無需硬編碼用戶特定字眼
"""

# ============================================
# 分層關鍵詞字典（通用 Schema）
# ============================================
# 這是通用模板，可以根據實際需求擴展關鍵詞
# 不包含任何用戶特定字眼（如 QST、秦王等）
# ============================================

KEYWORD_MAPPING = {
    # 理論框架類
    'Theory': {
        'primary': [
            # 核心框架標識
            ('framework', 10, ['framework', 'theory', 'core']),
            ('schema', 9, ['schema', 'structure', 'pattern']),
            ('model', 8, ['model', 'simulation', 'computation']),
        ],
        'secondary': [
            # 文檔和導出
            ('document', 7, ['document', 'export', 'format']),
            ('version', 6, ['version', 'iteration', 'update']),
            ('manifest', 5, ['manifest', 'metadata', 'spec']),
        ],
        'tertiary': [
            # 討論和分析
            ('analysis', 3, ['analysis', 'discussion', 'review']),
        ]
    },

    # 系統配置類
    'System': {
        'primary': [
            # 核心配置
            ('api_key', 10, ['api_key', 'secret', 'token', 'credential']),
            ('config_file', 9, ['config_file', 'setting', 'parameter']),
            ('ssh_key', 8, ['ssh_key', 'auth', 'connection']),
        ],
        'secondary': [
            # 平台和服務
            ('repository', 7, ['repository', 'git', 'version_control']),
            ('web_server', 6, ['web_server', 'apache', 'nginx', 'httpd']),
            ('service_endpoint', 5, ['endpoint', 'url', 'api']),
        ],
        'tertiary': [
            # 系統檢查
            ('heartbeat', 3, ['heartbeat', 'check', 'monitor']),
        ]
    },

    # 部署和網站類
    'Deployment': {
        'primary': [
            # 網站部署
            ('deployment_target', 10, ['deploy', 'publish', 'release']),
            ('website_url', 9, ['website', 'domain', 'host']),
            ('file_path', 8, ['file_path', 'directory', 'location']),
        ],
        'secondary': [
            # 靜態文件
            ('static_file', 7, ['html', 'css', 'js', 'static']),
            ('asset', 6, ['asset', 'resource', 'file']),
        ],
        'tertiary': [
            # 部署記錄
            ('deployment_log', 3, ['deployed', 'uploaded', 'synced']),
        ]
    },

    # 項目和倉庫類
    'Project': {
        'primary': [
            # 倉庫操作
            ('branch', 10, ['branch', 'merge', 'pull_request']),
            ('commit', 9, ['commit', 'history', 'revision']),
            ('remote', 8, ['remote', 'origin', 'upstream']),
        ],
        'secondary': [
            # 項目管理
            ('workspace', 7, ['workspace', 'project_dir', 'root']),
            ('backup', 6, ['backup', 'archive', 'snapshot']),
        ],
        'tertiary': [
            # 記錄
            ('changelog', 3, ['change', 'update', 'note']),
        ]
    },

    # 數據和配置類
    'Data': {
        'primary': [
            # 數據源
            ('data_source', 10, ['data_source', 'database', 'dataset']),
            ('api_endpoint', 9, ['api', 'endpoint', 'service']),
        ],
        'secondary': [
            # 數據格式
            ('json', 7, ['json', 'structured_data']),
            ('markdown', 6, ['markdown', 'md', 'doc']),
        ],
        'tertiary': [
            # 數據處理
            ('transformation', 3, ['transform', 'convert', 'process']),
        ]
    },

    # 網絡和安全類
    'Network': {
        'primary': [
            ('firewall', 10, ['firewall', 'security_rule', 'filter']),
            ('vpn', 9, ['vpn', 'tunnel', 'secure_connection']),
        ],
        'secondary': [
            ('host', 7, ['host', 'server', 'ip']),
            ('port', 6, ['port', 'socket', 'endpoint']),
        ],
        'tertiary': [
            ('network_log', 3, ['log', 'audit', 'trace']),
        ]
    }
}

# ============================================
# 使用者配置範例
# ============================================
# 用戶可以在運行時動態添加自己的關鍵詞映射
# 無需修改核心代碼
# ============================================

USER_KEYWORDS = {
    # 範例：添加用戶特定的關鍵詞
    'MyDomain': {
        'primary': [
            ('my_framework', 10, ['my_framework', 'my_theory']),
            ('my_project', 8, ['my_project', 'my_repo']),
        ]
    }
}

# 合併用戶關鍵詞到主映射（可選）
def merge_user_keywords(user_mapping=None):
    """合併用戶自定義關鍵詞"""
    merged = KEYWORD_MAPPING.copy()
    if user_mapping:
        for category, layers in user_mapping.items():
            if category not in merged:
                merged[category] = {}
            for layer, items in layers.items():
                if layer not in merged[category]:
                    merged[category][layer] = []
                merged[category][layer].extend(items)
    return merged

# ============================================
# 分類函數
# ============================================

def classify_content(content, custom_mapping=None):
    """
    內容分類（基於分層關鍵詞匹配）
    
    Args:
        content (str): 要分類的內容
        custom_mapping (dict): 用戶自定義關鍵詞映射（可選）
    
    Returns:
        list: [(tag, score), ...] 按權重排序的標籤列表
    """
    mapping = merge_user_keywords(custom_mapping) if custom_mapping else KEYWORD_MAPPING
    
    scores = {}
    
    for category, layers in mapping.items():
        for layer, items in layers.items():
            for keyword, weight, tags in items:
                if keyword in content:
                    for tag in tags:
                        if tag not in scores:
                            scores[tag] = 0
                        scores[tag] += weight
    
    # 返回按權重排序的標籤（取前 5）
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]


def get_priority_from_tags(tags):
    """
    根據標籤權重確定優先級
    
    Args:
        tags (list): [(tag, score), ...]
    
    Returns:
        str: 'C', 'I', or 'N'
    """
    if not tags:
        return 'N'
    
    highest_score = tags[0][1]
    
    if highest_score >= 9:
        return 'C'  # Critical
    elif highest_score >= 5:
        return 'I'  # Important
    else:
        return 'N'  # Normal


# ============================================
# 測試代碼
# ============================================

if __name__ == '__main__':
    # 測試用例
    test_cases = [
        "部署 framework 版本到 website",
        "api_key 配置成功",
        "推送 commit 到 repository",
        "安裝 apache web_server",
    ]
    
    print("=" * 60)
    print("Soul Memory Keyword Mapping v3.3 - 測試")
    print("=" * 60)
    
    for i, content in enumerate(test_cases, 1):
        print(f"\n測試 {i}: {content}")
        tags = classify_content(content)
        priority = get_priority_from_tags(tags)
        print(f"  標籤: {[t[0] for t in tags]}")
        print(f"  優先級: [{priority}]")
