# Smart Skill Finder - Usage Examples

## Basic Usage

### Example 1: Simple Skill Discovery
**User Query**: "How do I prevent conversation hangs?"

**Agent Response**:
```
I found some relevant skills for your needs:

🥇 **conversation-flow-monitor** (Clawhub)
   • Prevents conversations from getting stuck due to YAML front matter issues
   • Relevance: 94%
   • ✅ Security verified  
   • Install: clawhub install edkuo7/conversation-flow-monitor

🥈 **agent-browser** (Skills CLI)
   • Reliable browser automation with built-in timeout protection
   • Relevance: 87%
   • ✅ Security verified
   • Install: npx skills add vercel-labs/agent-browser@agent-browser

🥉 **reliable-agent-guardian** (GitHub)
   • General conversation reliability toolkit  
   • Relevance: 82%
   • ⚠️ Security scan pending
   • Install: git clone https://github.com/user/reliable-agent-guardian.git ~/.openclaw/skills/reliable-agent-guardian

Review the skill details before installing. Would you like me to explain any of these options?
```

### Example 2: Web Development Skills
**User Query**: "I need help with React performance optimization"

**Agent Response**:
```
I found some relevant skills for your needs:

🥇 **vercel-react-best-practices** (Skills CLI)
   • React and Next.js performance optimization guidelines from Vercel Engineering
   • Relevance: 96%
   • ✅ Security verified (Official Vercel Labs)
   • Install: npx skills add vercel-labs/agent-skills@vercel-react-best-practices

🥈 **web-design-guidelines** (Skills CLI)
   • Comprehensive web performance and design best practices
   • Relevance: 89%
   • ✅ Security verified (Official Vercel Labs)
   • Install: npx skills add vercel-labs/agent-skills@web-design-guidelines

🥉 **next-best-practices** (Skills CLI)
   • Next.js specific performance and optimization patterns
   • Relevance: 85%
   • ✅ Security verified (Official Vercel Labs)
   • Install: npx skills add vercel-labs/next-skills@next-best-practices

These official Vercel skills are highly trusted and widely used. Would you like installation guidance for any of these?
```

### Example 3: No Results Found
**User Query**: "How do I build a quantum computing compiler?"

**Agent Response**:
```
I searched across multiple skill ecosystems but didn't find specific skills for "quantum computing compiler". 

However, I can help you directly with this task! Would you like me to:
1. Provide general guidance on quantum computing compiler development
2. Help you create your own skill for this specific need
3. Search more broadly for related quantum computing resources
```

## Advanced Usage

### Example 4: Browser Fallback - APIs Unavailable
**Scenario**: External APIs are temporarily unavailable or rate-limited

**Agent Response**:
```
I found some relevant skills for your needs:

🥇 **conversation-flow-monitor** (Clawhub)
   • Prevents conversations from getting stuck due to YAML front matter issues
   • Relevance: 92%
   • ✅ Security verified  
   • Install: clawhub install edkuo7/conversation-flow-monitor

🥈 **agent-browser** (Skills CLI)
   • Reliable browser automation with built-in timeout protection
   • Relevance: 85%
   • ✅ Security verified
   • Install: npx skills add vercel-labs/agent-browser@agent-browser

🥉 **browser-use** (Skills CLI)
   • Robust browser control capabilities that can be used to monitor and recover from stuck conversations
   • Relevance: 79%
   • ✅ Security verified
   • Install: npx skills add browser-use/browser-use

Even when external APIs are temporarily unavailable, I can still find relevant skills using browser automation. Review the skill details before installing.
```

### Example 5: Natural Language Understanding
**User Query**: "My conversations keep getting stuck when I'm doing browser automation. It seems like something with the skill files isn't right."

**Agent Analysis**: 
- Domain: "conversation reliability"
- Task: "prevent conversation hangs during browser automation"
- Keywords: ["browser", "automation", "conversation", "hang", "stuck", "skill", "yaml"]

**Agent Response**: Same as Example 1, but with higher relevance scores due to better understanding.

## Integration Patterns

### With Other Skills
The Smart Skill Finder works well with:

- **self-improving-agent**: Logs skill discovery patterns and user feedback
- **conversation-flow-monitor**: Recommends itself when users have conversation hang issues
- **ontology**: Can store discovered skills as entities for future reference

### In Workflows
```python
# Instead of manual skill searching
user_query = "How do I handle PDF documents in my agent?"
recommended_skills = intelligent_skill_finder.find_skills_for_query(user_query)
print(recommended_skills)
```

## Best Practices

1. **Be specific in queries**: "React performance" works better than just "performance"
2. **Use natural language**: The skill understands conversational queries
3. **Review security status**: Always check the security verification status before installing
4. **Start with top recommendations**: The first 1-2 skills are usually the most relevant
5. **Provide feedback**: If recommendations aren't helpful, the skill can learn from your feedback

## Troubleshooting

### Common Issues and Solutions

**Issue**: "No skills found for my query"
- **Solution**: Try rephrasing your query or be more specific about your domain

**Issue**: "Skills CLI not working"
- **Solution**: The skill will automatically fall back to Clawhub and GitHub searches

**Issue**: "Slow response times"
- **Solution**: Network calls to external APIs may take 2-5 seconds; this is normal

**Issue**: "Security status shows 'pending'"
- **Solution**: New skills may not have completed security scanning yet; review the source before installing

This skill is designed to make finding and installing relevant agent skills as easy and safe as possible!