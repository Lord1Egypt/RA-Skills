# 使用示例

## 基本示例

### 1. 简单搜索
```bash
python3 ../scripts/tavily_search.py --query "OpenClaw是什么"
```

### 2. 包含答案摘要
```bash
python3 ../scripts/tavily_search.py \
  --query "人工智能的最新发展" \
  --include-answer \
  --max-results 3
```

### 3. Markdown格式输出
```bash
python3 ../scripts/tavily_search.py \
  --query "Python编程教程" \
  --format md \
  --max-results 5
```

## 高级示例

### 4. 使用高级搜索深度
```bash
python3 ../scripts/tavily_search.py \
  --query "复杂的机器学习算法" \
  --search-depth advanced \
  --timeout 45 \
  --verbose
```

### 5. 启用缓存
```bash
# 第一次搜索（会缓存结果）
python3 ../scripts/tavily_search.py \
  --query "常见问题" \
  --cache-ttl 600  # 缓存10分钟

# 第二次搜索相同查询（从缓存加载）
python3 ../scripts/tavily_search.py \
  --query "常见问题"
```

### 6. 清除缓存
```bash
# 清除所有缓存
python3 ../scripts/tavily_search.py --clear-cache

# 禁用缓存进行搜索
python3 ../scripts/tavily_search.py \
  --query "最新新闻" \
  --no-cache
```

## 集成示例

### 7. 在脚本中使用
```python
#!/usr/bin/env python3
import subprocess
import json

def search_with_tavily(query, max_results=3):
    """使用Tavily搜索并返回结果"""
    cmd = [
        "python3", "/root/.openclaw/skills/tavily-search/scripts/tavily_search.py",
        "--query", query,
        "--max-results", str(max_results),
        "--format", "json"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"搜索失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    results = search_with_tavily("OpenClaw功能", 5)
    if results:
        for item in results.get("results", []):
            print(f"- {item.get('title')}: {item.get('url')}")
```

### 8. 批量搜索
```bash
#!/bin/bash
# batch_search.sh

QUERIES=(
    "机器学习"
    "深度学习"
    "自然语言处理"
    "计算机视觉"
)

for query in "${QUERIES[@]}"; do
    echo "搜索: $query"
    python3 ../scripts/tavily_search.py \
        --query "$query" \
        --max-results 2 \
        --format md \
        --cache-ttl 3600  # 缓存1小时
    echo "---"
done
```

## 故障排除示例

### 9. 检查配置
```bash
# 检查API密钥
python3 -c "
import os
key = os.environ.get('TAVILY_API_KEY')
if key:
    print(f'API密钥已设置: {key[:10]}...')
else:
    print('API密钥未设置')
"

# 测试网络连接
curl -I https://api.tavily.com
```

### 10. 调试模式
```bash
# 启用详细输出查看详细信息
python3 ../scripts/tavily_search.py \
  --query "测试" \
  --verbose \
  --timeout 10
```

## 最佳实践

1. **合理使用缓存**: 对重复查询启用缓存
2. **控制结果数量**: 默认3-5个结果以减少token消耗
3. **选择适当超时**: 根据网络状况调整超时时间
4. **监控API使用**: 注意Tavily的速率限制
5. **错误处理**: 总是检查返回结果的有效性