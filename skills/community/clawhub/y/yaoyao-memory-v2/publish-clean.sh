#!/bin/bash
# 预发布清理脚本 - 删除用户隐私数据
# 使用方法: ./publish-clean.sh

cd "$(dirname "$0")"

echo "🧹 开始预发布清理..."

# 1. config 目录下的用户数据（精确匹配）
rm -f config/embeddings_cache.json
rm -f config/persona_update.json
rm -f config/user_config.json
rm -f config/samba.json
rm -f config/llm_config.json
rm -f config/embedding_config.json

# 2. 脚本中的硬编码密钥占位符还原
sed -i 's/YOUR_API_KEY/你的API_KEY/g' scripts/warmup.py 2>/dev/null || true

# 2. 脚本中的硬编码密钥占位符还原
sed -i 's/YOUR_API_KEY/你的API_KEY/g' scripts/warmup.py 2>/dev/null || true

# 2. 内存目录（运行时数据）
rm -f ../memory/.meta.json
rm -f ../memory/heartbeat-state.json
rm -f ../memory/token-state.json
rm -f ../memory/.boost_log.json
rm -f ../memory/.heat_data.json
rm -f ../memory/.memory_graph.json
rm -f ../memory/.predictive_cache.json
rm -rf ../memory/chroma_db/
rm -rf ../memory/cache/
rm -rf ../memory/backups/

echo "✅ 清理完成！可以安全发布了。"
