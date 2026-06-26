# 搜索关键词清单（Broad to Narrow 策略）

## Round 1: Broad Discovery（快速扫描）

```
"GitHub trending today"
"new AI tools 2026"
"Product Hunt top products today"
"Hacker News top stories"
"awesome-ai-tools recently added"
```

## Round 2: Deep Dive（深度分析）

### GitHub Trending
```
"site:github.com/trending AI automation"
"GitHub trending developer tools"
"GitHub trending self-hosted"
```

### Small Tools
```
"GitHub small tool automation"
"GitHub small tool productivity"
"awesome tools under 1000 stars"
```

### Money Projects
```
"Product Hunt today AI SaaS"
"Product Hunt top 5 today"
"indie hacker launched today"
```

### Tech Trends
```
"site:news.ycombinator.com AI framework"
"Hacker News AI discussion today"
"new AI model released 2026"
```

### Awesome Lists
```
"awesome-ai-tools new additions"
"awesome-selfhosted recently updated"
"site:github.com awesome-list stars:>1000"
```

## Round 3: Verification（验证）

```
"{project_name} review"
"{project_name} vs alternatives"
"{project_name} tutorial"
"site:github.com {project_name}"
```

## 搜索技巧

1. **时间限定**: `created:>2026-03-20`
2. **Star 范围**: `stars:200..3000`
3. **领域限定**: `topic:ai-tools`
4. **排除大项目**: `-stars:>10000`
