/**
 * Reading Notes Skill
 * Expand reading insights into detailed notes and reflections
 * 
 * SAFE VERSION: No external API calls, no filesystem access, pure local processing
 */

/**
 * Safe template-based reading notes expansion
 * 
 * This implementation uses only local templates and does NOT:
 * - Call external APIs
 * - Access filesystem
 * - Require API keys or secrets
 * - Send user data outside the local environment
 */
async function expandReadingNotes(options) {
    const { insight, depth = 'detailed', includeConnections = true } = options;
    // Safety note for users
    const safetyNotice = `*🔒 Security Note: These notes were generated locally without external API calls or data sharing.*`;
    // Enhanced templates with more variety
    const templates = {
        brief: `${safetyNotice}\n\n**Brief Reading Note:**\n\n**Insight:** "${insight}"\n\n**Key Takeaway:** This reading highlights important concepts worth exploring further. Consider how these ideas might apply to your current learning goals or projects.`,
        detailed: `${safetyNotice}\n\n**Detailed Reading Notes:**\n\n**Original Insight:**\n${insight}\n\n**Expanded Analysis:**\nThis reading touches on meaningful themes relevant to personal and professional growth. The concept mentioned suggests deeper implications for learning methodologies and knowledge application.\n\n**Key Themes Identified:**\n1. Learning and development principles\n2. Knowledge integration strategies\n3. Practical application frameworks\n\n**Personal Reflection Questions:**\n- How does this insight connect to your existing knowledge?\n- What specific actions could you take based on this understanding?\n- How might you share or discuss this perspective with others?\n\n**Note-Taking Tips:**\n- Consider creating a mind map around this concept\n- Link this insight to related notes in your system\n- Set a reminder to revisit this topic in 1-2 weeks`,
        comprehensive: `${safetyNotice}\n\n**Comprehensive Reading Analysis:**\n\n**Core Insight:**\n"${insight}"\n\n**Theoretical Context:**\nThis perspective connects to established frameworks in cognitive science, adult learning theory, and personal development methodologies. Similar concepts appear in discussions about deliberate practice, growth mindset, and knowledge synthesis.\n\n**Practical Applications:**\n1. **Immediate Implementation:** Identify one concrete way to apply this insight today\n2. **Integration Strategy:** Connect this concept to 2-3 related ideas you already know\n3. **Sharing Plan:** Prepare a brief explanation to share with a colleague or study partner\n\n**Learning Pathways:**\n- Foundational: Understanding basic principles and definitions\n- Intermediate: Exploring connections to related concepts\n- Advanced: Developing original applications and teaching others\n\n**Reflection Prompts:**\n- What surprised you about this insight?\n- How might your understanding evolve with further study?\n- What questions does this raise for future exploration?\n\n**Note Organization:**\n- Create a dedicated note or section for this topic\n- Use tags: #reading #insight #learning\n- Consider linking to practical examples or case studies\n\n**Summary:**\nA valuable perspective that merits thoughtful consideration, practical application, and systematic note-taking.`
    };
    let notes = templates[depth];
    if (includeConnections) {
        notes += `\n\n**Suggested Connections for Your Notes:**\n- Relates to principles of active learning and knowledge retention\n- Connects to frameworks for personal and professional development\n- Could be integrated with goal-setting and progress tracking practices\n- Consider linking to existing notes on related topics`;
    }
    return notes;
}

/**
 * Local concept suggestion (no external search)
 */
async function suggestRelatedConcepts(insight, limit = 3) {
    // Local concept mapping - no external calls
    const conceptMap = {
        'learning': ['Deliberate Practice', 'Growth Mindset', 'Spaced Repetition', 'Active Recall'],
        'practice': ['Skill Acquisition', 'Feedback Loops', 'Performance Metrics', 'Deliberate Practice'],
        'knowledge': ['Knowledge Graphs', 'Concept Mapping', 'Information Synthesis', 'Mental Models'],
        'growth': ['Continuous Improvement', 'Adaptive Learning', 'Resilience Building', 'Kaizen'],
        'reading': ['Active Reading', 'Note-taking Systems', 'Critical Analysis', 'SQ3R Method'],
        'review': ['Retrospective Analysis', 'Progress Assessment', 'Learning Journals', 'Spaced Repetition'],
        'note': ['Zettelkasten', 'Digital Garden', 'Atomic Notes', 'Progressive Summarization'],
        'thinking': ['Critical Thinking', 'Systems Thinking', 'Design Thinking', 'First Principles']
    };
    const lowercaseInsight = insight.toLowerCase();
    const suggestions = [];
    // Find matching concepts
    for (const [keyword, concepts] of Object.entries(conceptMap)) {
        if (lowercaseInsight.includes(keyword)) {
            suggestions.push(...concepts.slice(0, 2));
        }
    }
    // Default suggestions if no match
    if (suggestions.length === 0) {
        return [
            'Learning Optimization',
            'Knowledge Integration',
            'Personal Development Frameworks',
            'Effective Study Techniques',
            'Cognitive Science Principles'
        ].slice(0, limit);
    }
    return [...new Set(suggestions)].slice(0, limit);
}

/**
 * Generate note-taking prompts for the insight
 */
async function generateNotePrompts(insight) {
    const prompts = [
        `What is the main argument or insight from this reading?`,
        `How does this connect to what I already know?`,
        `What specific examples or applications come to mind?`,
        `What questions does this raise for further exploration?`,
        `How might I explain this concept to someone else?`,
        `What action items or next steps does this suggest?`,
        `What are the limitations or counterarguments to consider?`,
        `How does this fit into a broader context or system?`
    ];
    return prompts.slice(0, 5); // Return top 5 prompts
}

/**
 * Main skill handler for OpenClaw - SAFE VERSION
 */
const readingNotesSkill = {
    name: 'reading-notes',
    description: 'Expand reading insights into detailed notes using local templates only',
    version: '1.0.0',
    commands: [
        {
            name: 'reading-notes',
            description: 'Expand a reading insight into detailed notes',
            handler: async (context, args) => {
                const insight = args.join(' ');
                if (!insight.trim()) {
                    return 'Please provide a reading insight. Example: /reading-notes Today I read about deliberate practice';
                }
                const notes = await expandReadingNotes({
                    insight,
                    depth: 'detailed',
                    includeConnections: true
                });
                return notes;
            }
        },
        {
            name: 'reading-brief',
            description: 'Generate a brief reading note',
            handler: async (context, args) => {
                const insight = args.join(' ');
                if (!insight.trim()) {
                    return 'Please provide a reading insight.';
                }
                const notes = await expandReadingNotes({
                    insight,
                    depth: 'brief',
                    includeConnections: false
                });
                return notes;
            }
        },
        {
            name: 'reading-related',
            description: 'Get related concepts for a reading insight',
            handler: async (context, args) => {
                const insight = args.join(' ');
                if (!insight.trim()) {
                    return 'Please provide a reading insight.';
                }
                const concepts = await suggestRelatedConcepts(insight, 5);
                const prompts = await generateNotePrompts(insight);
                return `**Related Concepts for "${insight}":**\n\n${concepts.map(c => `- ${c}`).join('\n')}\n\n**Note-Taking Prompts:**\n\n${prompts.map((p, i) => `${i + 1}. ${p}`).join('\n')}`;
            }
        },
        {
            name: 'reading-prompts',
            description: 'Get note-taking prompts for a reading insight',
            handler: async (context, args) => {
                const insight = args.join(' ');
                if (!insight.trim()) {
                    return 'Please provide a reading insight.';
                }
                const prompts = await generateNotePrompts(insight);
                return `**Note-Taking Prompts for "${insight}":**\n\n${prompts.map((p, i) => `${i + 1}. ${p}`).join('\n')}\n\n**Tips:**\n- Use these prompts to structure your notes\n- Focus on connections to existing knowledge\n- Consider practical applications`;
            }
        }
    ],
    tools: [],
    setup: async () => {
        console.log('Reading Notes Skill initialized - Safe local processing only');
        return { success: true };
    },
    teardown: async () => {
        console.log('Reading Notes Skill cleaned up');
        return { success: true };
    }
};

// Export for OpenClaw
module.exports = readingNotesSkill;
module.exports.expandReadingNotes = expandReadingNotes;
module.exports.suggestRelatedConcepts = suggestRelatedConcepts;
module.exports.generateNotePrompts = generateNotePrompts;
module.exports.readingNotesSkill = readingNotesSkill;