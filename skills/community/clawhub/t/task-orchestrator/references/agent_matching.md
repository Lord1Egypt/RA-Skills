# Agent Matching Strategy

## Capability Matrix

| Skill | Applicable Task Types | Advantage Scenarios |
|-------|-----------------------|---------------------|
| web-search, deep-search-skill | Information gathering, research, search | Web search required, competitive analysis |
| doc-writing-skill | Document writing, report generation | Professional document format output required |
| image_generation | Image creation, design | Generating images, posters, covers |
| ppt-parser-local | PPT processing | Presentation parsing, content extraction |
| redbook, weavefox-xhs-intel | Xiaohongshu operations | Post publishing, content analysis, sentiment monitoring |
| video-script-generation-skill | Video scripts | Storyboarding, shooting scripts, short video content |
| wechat-article-generator | Official Account content | In-depth articles, content creation |
| storyboard-prompt-generator | Storyboard prompts | Animation storyboards, AI generation prompts |

## Matching Rules

### 1. Match by Task Type
```python
def match_agent(task_description):
    keywords = {
        "document|report|summary": ["doc-writing-skill"],
        "PPT|presentation|slides": ["ppt-parser-local"],
        "image|poster|cover|design": ["image_generation"],
        "search|research|query|gather": ["web-search", "deep-search-skill"],
        "Xiaohongshu|post|recommendation": ["redbook", "weavefox-xhs-intel"],
        "video|script|storyboard": ["video-script-generation-skill"],
        "Official Account|tweet": ["wechat-article-generator"]
    }
    for pattern, agents in keywords.items():
        if re.search(pattern, task_description):
            return agents
    return []
```

### 2. Load Balancing
- Avoid assigning too many tasks to the same agent simultaneously
- Prioritize agents currently idle
- Consider the agent's historical success rate

### 3. Cost Optimization
- Prioritize lightweight agents for simple tasks
- Use specialized agents for complex tasks
- Merge similar tasks for batch processing