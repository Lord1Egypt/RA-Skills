---
name: qianfan-clawhub
description: Search and install Baidu Qianfan ecosystem skills with fuzzy matching across slug, name, and description fields
metadata: { "openclaw": { "emoji": "🔍︎", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# Qianfan Skills Marketplace

A dedicated search and installation tool for Baidu Qianfan ecosystem skills. Provides secure skill discovery and management through Baidu Cloud services.

## ✨ Core Capabilities

1. **Multi-field Fuzzy Matching** - Search skills by matching keywords across slug, name, and description fields
2. **Precise Installation** - Install skills using complete slug names  
3. **Flexible Workspace** - Customize installation directory via `--workdir` parameter
4. **Automated Management** - Integrated download, extraction, verification, and installation
5. **Language-aware Search** - Prefers English keywords, falls back to Chinese if no results

## 📋 Usage Examples

### 🔍 Search Skills
```bash
# Basic search across slug, name, and description fields
python3 scripts/qianfanclawhub.py search "ai"

# Search by skill name (matches in name field)
python3 scripts/qianfanclawhub.py search "web" --limit 15

# Search by description keywords (matches in description field)
python3 scripts/qianfanclawhub.py search "搜索"

# Search by exact slug (matches in slug field)
python3 scripts/qianfanclawhub.py search "baidu-search"

# Limit results
python3 scripts/qianfanclawhub.py search "ppt" --limit 10

# Search with custom workspace
python3 scripts/qianfanclawhub.py search "keyword" --workdir "/custom/path"
```

### ⬇️ Install Skills  
```bash
# Install to default location (~/.qianfan/workspace/skills/)
python3 scripts/qianfanclawhub.py install "baidu-search"

# Force overwrite existing skill
python3 scripts/qianfanclawhub.py install "ai-ppt-generate" --force

# Install to custom directory
python3 scripts/qianfanclawhub.py install "skill-name" --workdir "/shared/skills"

# Install with custom directory and force overwrite
python3 scripts/qianfanclawhub.py install "skill-name" --workdir "./project/.skills" --force
```

## ⚠️ Key Points
- **Search Strategy**: Use English keywords first, Chinese as fallback
- **Search Fields**: Keywords are matched across three fields:
  1. **slug** - Skill's unique identifier (e.g., "baidu-search")
  2. **name** - Skill's display name (e.g., "Baidu Search")
  3. **description** - Skill's description text
- **Match Logic**: Any field containing the keyword will match
- **Installation**: Requires exact skill slug name
- **Security**: Requires BAIDU_API_KEY for authenticated access
- **Work Directory**: Use `--workdir` to install/search in custom location

## 🎯 Recommended Search Workflow
1. **Try English first**: `python3 scripts/qianfanclawhub.py search "english-keyword"`
2. **Fallback to Chinese**: If no results, try Chinese keyword
3. **Experiment with keywords**: Try different terms from slug, name, or description
4. **Copy slug name**: Copy exact slug from search results
5. **Install**: `python3 scripts/qianfanclawhub.py install "slug-name"`

## 🔗 Related Skills
This skill works best with the `baidu-search` skill, enabling quick access to Baidu ecosystem skills and optimizing the development experience in Chinese environments.
