/**
 * Goal Parser - Extract intent and keywords from natural language goals
 */

export function parseGoal(goal) {
  const lower = goal.toLowerCase();
  
  // Intent detection
  const intents = [];
  if (lower.includes('write') || lower.includes('create') || lower.includes('implement') || lower.includes('build') || lower.includes('make') || lower.includes('add') || lower.includes('setup')) {
    intents.push('write');
  }
  if (lower.includes('fix') || lower.includes('bug') || lower.includes('error') || lower.includes('repair') || lower.includes('resolve')) {
    intents.push('fix');
  }
  if (lower.includes('secure') || lower.includes('vulnerability') || lower.includes('sanitize')) {
    intents.push('security');
  }
  if (lower.includes('optimize') || lower.includes('performance') || lower.includes('speed')) {
    intents.push('optimize');
  }
  if (lower.includes('test') || lower.includes('spec')) {
    intents.push('test');
  }
  if (lower.includes('refactor') || lower.includes('cleanup')) {
    intents.push('refactor');
  }
  if (lower.includes('debug') || lower.includes('troubleshoot')) {
    intents.push('debug');
  }
  // Default to 'write' if nothing detected
  if (intents.length === 0) {
    intents.push('write');
  }

  // Language/framework detection
  const languages = [];
  const langPatterns = {
    'javascript': /\b(js|javascript|node|nodejs|express|jwt|react|vue|angular)\b/,
    'typescript': /\b(ts|typescript)\b/,
    'python': /\b(python|py|django|flask|fastapi)\b/,
    'rust': /\b(rust|rs)\b/,
    'go': /\b(go|golang)\b/,
    'java': /\b(java|spring)\b/,
    'c#': /\b(c#|csharp|\.net|asp\.net)\b/,
    'sql': /\b(sql|mysql|postgres|postgresql|mongodb|redis)\b/,
    'html': /\b(html|css|frontend)\b/,
    'bash': /\b(bash|shell|sh|script|dockerfile|docker)\b/,
    'docker': /\b(docker|dockerfile|container)\b/,
  };

  for (const [lang, pattern] of Object.entries(langPatterns)) {
    if (pattern.test(lower)) {
      languages.push(lang);
    }
  }

  // Security level
  let securityLevel = 'normal';
  if (lower.includes('secure') || lower.includes('vulnerability') || lower.includes('exploit')) {
    securityLevel = 'high';
  } else if (lower.includes('public') || lower.includes('api')) {
    securityLevel = 'medium';
  }

  // Extract keywords (simple extraction)
  const stopWords = ['write', 'create', 'implement', 'fix', 'error', 'with', 'the', 'this', 'that', 'from', 'have', 'some'];
  const keywords = goal
    .split(/\s+/)
    .filter(w => w.length > 2 && !stopWords.includes(w.toLowerCase()))
    .slice(0, 10);

  // Always include intents as keywords for pattern matching
  const allKeywords = [...new Set([...intents, ...keywords])];

  return {
    original: goal,
    intents,
    languages,
    securityLevel,
    keywords: allKeywords,
    timestamp: new Date().toISOString()
  };
}