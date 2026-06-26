/**
 * Sensitive Data Detection and Protection
 */

const SENSITIVE_PATTERNS = [
  { type: 'email', pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, description: 'Email address' },
  { type: 'phone', pattern: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/, description: 'Phone number' },
  { type: 'credit_card', pattern: /\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/, description: 'Credit card' },
  { type: 'api_key', pattern: /\b(?:api[_-]?key)[=:]\s*['"]?[A-Za-z0-9_-]{16,}['"]?/i, description: 'API Key' },
  { type: 'password', pattern: /\b(?:password|passwd)[=:]\s*['"]?[^\s'"]]{4,}['"]?/i, description: 'Password' },
];

export function detectSensitive(text) {
  const findings = [];
  for (const { type, pattern, description } of SENSITIVE_PATTERNS) {
    let match;
    const regex = new RegExp(pattern.source, 'gi');
    while ((match = regex.exec(text)) !== null) {
      findings.push({ type, value: match[0], description, start: match.index, end: match.index + match[0].length });
    }
  }
  return findings;
}

export function redactSensitive(text, replacement = '[REDACTED]') {
  const findings = detectSensitive(text);
  let result = text;
  let offset = 0;
  for (const finding of findings) {
    const start = finding.start + offset;
    const end = start + finding.value.length;
    result = result.substring(0, start) + replacement + result.substring(end);
    offset += replacement.length - finding.value.length;
  }
  return result;
}

export function hasSensitive(text) {
  return detectSensitive(text).length > 0;
}

if (require.main === module) {
  const text = process.argv.slice(2).join(' ') || 'test@example.com is my email';
  const findings = detectSensitive(text);
  console.log('\n🔒 Sensitive Data Detection\n');
  console.log(`  Text: ${text}\n`);
  if (findings.length === 0) console.log('  ✅ No sensitive data detected');
  else { for (const f of findings) console.log(`    - ${f.type}: ${f.description}`); }
  console.log(`\n  Redacted: ${redactSensitive(text)}`);
  console.log('');
}
