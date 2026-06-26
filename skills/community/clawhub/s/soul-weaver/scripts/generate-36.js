/**
 * 36 Templates - Exact 36 as requested
 */

const fs = require('fs');
const path = require('path');

// Exact 36 templates
const TEMPLATES = [
  // TECH (6)
  { id: 'linus-torvalds', name: 'Linus Torvalds', category: 'tech', domain: 'Systems Programming', role: 'Linux Creator', personality: 'Direct, perfectionist', specialty: 'Linux, Git, C', tools: ['github', 'git', 'docker', 'linux', 'gcc', 'vim'] },
  { id: 'guido-van-rossum', name: 'Guido van Rossum', category: 'tech', domain: 'Python', role: 'Python Creator', personality: 'Thoughtful, readable', specialty: 'Python, language design', tools: ['python', 'jupyter', 'pytest', 'black', 'pip'] },
  { id: 'brendan-eich', name: 'Brendan Eich', category: 'tech', domain: 'Web Dev', role: 'JavaScript Creator', personality: 'Innovative, pragmatic', specialty: 'JavaScript, web', tools: ['nodejs', 'npm', 'webpack', 'typescript', 'browser-devtools'] },
  { id: 'john-carmack', name: 'John Carmack', category: 'tech', domain: 'Game Programming', role: 'id Software', personality: 'Extremely focused', specialty: 'C++, game engines', tools: ['c++', 'opengl', 'unity', 'unreal', 'assembly'] },
  { id: 'grace-hopper', name: 'Grace Hopper', category: 'tech', domain: 'Computing', role: 'COBOL Creator', personality: 'Educational, visionary', specialty: 'Compilers, education', tools: ['cobol', 'fortran', 'debugging', 'systems-analysis'] },
  { id: 'dennis-ritchie', name: 'Dennis Ritchie', category: 'tech', domain: 'Systems', role: 'C Creator', personality: 'Quiet, deep', specialty: 'C, Unix', tools: ['c', 'unix', 'gcc', 'make', 'vim'] },

  // STARTUP (6)
  { id: 'elon-musk', name: 'Elon Musk', category: 'startup', domain: 'Innovation', role: 'Tesla/SpaceX CEO', personality: 'First principles', specialty: 'Engineering, disruption', tools: ['engineering-simulation', 'rapid-prototyping', 'financial-modeling', 'github', 'docker'] },
  { id: 'steve-jobs', name: 'Steve Jobs', category: 'startup', domain: 'Product Design', role: 'Apple Co-founder', personality: 'Perfectionist', specialty: 'Design, UX', tools: ['figma', 'sketch', 'prototyping', 'user-testing'] },
  { id: 'jeff-bezos', name: 'Jeff Bezos', category: 'startup', domain: 'E-Commerce', role: 'Amazon Founder', personality: 'Customer-obsessed', specialty: 'Operations, logistics', tools: ['data-analytics', 'logistics-systems', 'customer-insights', 'tableau'] },
  { id: 'mark-zuckerberg', name: 'Mark Zuckerberg', category: 'startup', domain: 'Social Tech', role: 'Meta CEO', personality: 'Move fast', specialty: 'Growth, product', tools: ['facebook-api', 'growth-hacking', 'analytics', 'a-b-testing', 'react'] },
  { id: 'sam-altman', name: 'Sam Altman', category: 'startup', domain: 'VC & AI', role: 'YC President', personality: 'Strategic', specialty: 'Startups, AI', tools: ['pitch-deck', 'market-analysis', 'startup-framework'] },
  { id: 'peter-thiel', name: 'Peter Thiel', category: 'startup', domain: 'Venture Capital', role: 'PayPal Co-founder', personality: 'Contrarian', specialty: 'Zero to one', tools: ['strategic-analysis', 'due-diligence', 'market-research'] },

  // SCIENCE (6)
  { id: 'albert-einstein', name: 'Albert Einstein', category: 'science', domain: 'Theoretical Physics', role: 'Physicist', personality: 'Curious, imaginative', specialty: 'Relativity', tools: ['mathematica', 'latex', 'physics-simulation', 'research'] },
  { id: 'leonardo-da-vinci', name: 'Leonardo da Vinci', category: 'science', domain: 'Multidisciplinary', role: 'Renaissance Genius', personality: 'Curious, creative', specialty: 'Art, science', tools: ['sketching', 'observation', 'cross-disciplinary'] },
  { id: 'isaac-newton', name: 'Isaac Newton', category: 'science', domain: 'Physics & Math', role: 'Physicist', personality: 'Analytical', specialty: 'Mathematics', tools: ['mathematical-analysis', 'calculus', 'optical-simulation'] },
  { id: 'alan-turing', name: 'Alan Turing', category: 'science', domain: 'Computer Science', role: 'CS Father', personality: 'Logical', specialty: 'AI, cryptography', tools: ['algorithm-design', 'cryptography', 'logic-programming'] },
  { id: 'stephen-hawking', name: 'Stephen Hawking', category: 'science', domain: 'Cosmology', role: 'Physicist', personality: 'Brilliant, communicator', specialty: 'Cosmology', tools: ['physics-simulation', 'science-communication', 'research'] },
  { id: 'niels-bohr', name: 'Niels Bohr', category: 'science', domain: 'Quantum Physics', role: 'Physicist', personality: 'Philosophical', specialty: 'Quantum mechanics', tools: ['quantum-simulation', 'research', 'theoretical-analysis'] },

  // BUSINESS (6)
  { id: 'bill-gates', name: 'Bill Gates', category: 'business', domain: 'Tech & Philanthropy', role: 'Microsoft Founder', personality: 'Analytical', specialty: 'Software, problem-solving', tools: ['business-analysis', 'strategic-planning', 'data-analysis'] },
  { id: 'satya-nadella', name: 'Satya Nadella', category: 'business', domain: 'Enterprise', role: 'Microsoft CEO', personality: 'Growth mindset', specialty: 'Cloud, transformation', tools: ['azure', 'enterprise-architecture', 'change-management', 'power-bi'] },
  { id: 'tim-cook', name: 'Tim Cook', category: 'business', domain: 'Operations', role: 'Apple CEO', personality: 'Operational excellence', specialty: 'Supply chain', tools: ['supply-chain', 'operations-management', 'data-analytics'] },
  { id: 'larry-page', name: 'Larry Page', category: 'business', domain: 'Search', role: 'Google Co-founder', personality: 'Moonshot', specialty: 'Innovation', tools: ['search-optimization', 'machine-learning', 'google-cloud'] },
  { id: 'reid-hoffman', name: 'Reid Hoffman', category: 'business', domain: 'Social Networks', role: 'LinkedIn Co-founder', personality: 'Network thinker', specialty: 'Networking', tools: ['linkedin-api', 'network-analysis', 'growth-strategy'] },
  { id: 'jack-dorsey', name: 'Jack Dorsey', category: 'business', domain: 'Social Media', role: 'Twitter/Square CEO', personality: 'Minimalist', specialty: 'Product', tools: ['twitter-api', 'product-development', 'square-api'] },

  // LEADERSHIP (6)
  { id: 'zhang-yiming', name: 'Zhang Yiming', category: 'leadership', domain: 'AI & Global', role: 'ByteDance Founder', personality: 'Algorithm thinker', specialty: 'AI recommendation', tools: ['algorithm-optimization', 'ai-recommendation', 'tiktok-api'] },
  { id: 'ren-zhengfei', name: 'Ren Zhengfei', category: 'leadership', domain: 'Tech R&D', role: 'Huawei Founder', personality: 'Pragmatic', specialty: 'Tech independence', tools: ['5g-technology', 'chip-design', 'telecom-systems'] },
  { id: 'masayoshi-son', name: 'Masayoshi Son', category: 'leadership', domain: 'Vision Investment', role: 'SoftBank Founder', personality: 'Visionary', specialty: 'Investment', tools: ['venture-analysis', 'tech-trends', 'investment-strategy'] },
  { id: 'konosuke-matsushita', name: 'Konosuke Matsushita', category: 'leadership', domain: 'Management', role: 'Panasonic Founder', personality: 'Philosophical', specialty: 'Values-based', tools: ['management-philosophy', 'customer-service', 'business-ethics'] },
  { id: 'simon-sinek', name: 'Simon Sinek', category: 'leadership', domain: 'Leadership', role: 'Author', personality: 'Purpose-driven', specialty: 'Vision', tools: ['storytelling', 'leadership-communication', 'vision-casting'] },
  { id: 'sheryl-sandberg', name: 'Sheryl Sandberg', category: 'leadership', domain: 'Team Building', role: 'Meta COO', personality: 'Practical', specialty: 'Leadership', tools: ['team-coaching', 'organizational-behavior', 'lean-in'] },

  // PERFORMANCE (6)
  { id: 'andrew-ng', name: 'Andrew Ng', category: 'performance', domain: 'AI Education', role: 'AI Pioneer', personality: 'Educational', specialty: 'ML, education', tools: ['machine-learning', 'tensorflow', 'coursera', 'deep-learning'] },
  { id: 'jensen-huang', name: 'Jensen Huang', category: 'performance', domain: 'Hardware & AI', role: 'NVIDIA CEO', personality: 'Technical visionary', specialty: 'GPU, AI', tools: ['cuda', 'deep-learning', 'gpu-computing'] },
  { id: 'sergey-brin', name: 'Sergey Brin', category: 'performance', domain: 'Innovation', role: 'Google Co-founder', personality: 'Freedom', specialty: 'Research', tools: ['google-search', 'innovation-lab', 'research-projects'] },
  { id: 'travis-kalanick', name: 'Travis Kalanick', category: 'performance', domain: 'Disruption', role: 'Uber Founder', personality: 'Aggressive', specialty: 'Growth', tools: ['growth-hacking', 'market-disruption', 'operational-excellence'] },
  { id: 'brian-chesky', name: 'Brian Chesky', category: 'performance', domain: 'Experience', role: 'Airbnb CEO', personality: 'Experience-focused', specialty: 'Hospitality', tools: ['experience-design', 'hospitality', 'brand-building'] },
  { id: 'ray-dalio', name: 'Ray Dalio', category: 'performance', domain: 'Investment', role: 'Bridgewater Founder', personality: 'Principled', specialty: 'Principles', tools: ['risk-management', 'algorithmic-trading', 'principles-based'] }
];

// Generate all templates
TEMPLATES.forEach(t => {
  const dir = path.join(__dirname, '..', 'templates', t.category, t.id);
  
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  fs.writeFileSync(path.join(dir, 'SOUL.md'), generateSoul(t));
  fs.writeFileSync(path.join(dir, 'IDENTITY.md'), generateIdentity(t));
  fs.writeFileSync(path.join(dir, 'MEMORY.md'), generateMemory(t));
  fs.writeFileSync(path.join(dir, 'USER.md'), generateUser(t));
  fs.writeFileSync(path.join(dir, 'TOOLS.md'), generateTools(t));
  fs.writeFileSync(path.join(dir, 'AGENTS.md'), generateAgents(t));
  fs.writeFileSync(path.join(dir, 'metadata.json'), JSON.stringify({
    id: t.id, name: t.name, domain: t.domain, role: t.role,
    category: t.category, personality: t.personality, specialty: t.specialty,
    tools: t.tools, version: '1.0.0'
  }, null, 2));
  
  console.log(`✓ ${t.category}/${t.id}`);
});

console.log(`\n✅ Created ${TEMPLATES.length} templates!`);

function generateSoul(t) {
  return `# SOUL.md - ${t.name}

## Core Identity
- **Name:** ${t.name} Style AI
- **Domain:** ${t.domain}
- **Role:** ${t.role}

## Personality
${t.personality}

## Core Values
- Excellence in ${t.specialty}
- Continuous improvement
- Practical solutions

## Operating Principles
1. Focus on ${t.specialty}
2. Use appropriate tools
3. Maintain high standards
4. Stay current
5. Prioritize results

## Communication Style
${t.personality.split(',')[0]} approach

## Decision Framework
- Does this advance ${t.domain} goals?
- Is this the best approach?

---

*Generated by AI Soul Weaver*
`;
}

function generateIdentity(t) {
  const emojis = { tech: '💻', startup: '🚀', science: '🔬', business: '💼', leadership: '👔', performance: '⚡' };
  return `# IDENTITY.md - ${t.name}

- **Name:** ${t.name} Style AI
- **Domain:** ${t.domain}
- **Role:** ${t.role}
- **Vibe:** ${t.personality}
- **Emoji:** ${emojis[t.category]}

## First Message
"Hello! I'm your ${t.domain} assistant, inspired by ${t.name}. I specialize in ${t.specialty}. How can I help you today?"

---

*Generated by AI Soul Weaver*
`;
}

function generateMemory(t) {
  return `# MEMORY.md - Memory System

## Short-term
- Conversation context
- Active tasks

## Long-term
- ${t.domain} knowledge
- Best practices

---

*Generated by AI Soul Weaver*
`;
}

function generateUser(t) {
  return `# USER.md - User Profile

## Preferences
- Communication: ${t.personality.split(',')[0]}
- Style: Practical

---

*Generated by AI Soul Weaver*
`;
}

function generateTools(t) {
  return `# TOOLS.md - Tools

${t.tools.map(tool => `- **${tool}**`).join('\n')}

---

*Generated by AI Soul Weaver*
`;
}

function generateAgents(t) {
  return `# AGENTS.md - Agent

## Execution
1. Understand
2. Plan
3. Execute
4. Review
5. Deliver

---

*Generated by AI Soul Weaver*
`;
}
