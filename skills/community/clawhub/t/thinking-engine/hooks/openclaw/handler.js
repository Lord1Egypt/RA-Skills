// hooks/openclaw/handler.js
// OpenClaw hook for multi-angle-thinking skill
// Injects a reminder when deep analysis is needed

const TRIGGER_PHRASES = [
  'analyze', 'analyse', 'simulation', 'simulate',
  'think deeply', 'multiple angles', 'challenge my thinking',
  'what am i missing', 'hidden risks', 'what would happen',
  'فكر معي', 'حلل', 'زوايا', 'نتائج غير متوقعة', 'ماذا سيحدث'
];

const REMINDER = `[multi-angle-thinking] Deep analysis requested. 
Run the full pipeline:
1. 🔍 Intelligence: gather real data via web_search (max 6 queries)
2. ⚡ 11 Lenses: philosophical, ethical, practical, historical, psychological, systems, financial, technological, adversarial, societal, counterfactual
3. 🌍 Build World: create 3-5 realistic characters with stakes, fears, blind spots
4. 👁️ Live Narrative: run simulation to completion — narrative + findings + surprises
5. 🔮 Synthesis: convergences, tensions, the unexpected discovery, open questions
Guardrails: max 6 searches, label real-person simulations as fictional inference, user-invoked only.`;

module.exports = {
  name: 'multi-angle-thinking',
  event: 'UserPromptSubmit',
  handler: (context) => {
    const prompt = (context.prompt || '').toLowerCase();
    const shouldActivate = TRIGGER_PHRASES.some(phrase => 
      prompt.includes(phrase.toLowerCase())
    );
    if (shouldActivate) {
      return { inject: REMINDER };
    }
    return null;
  }
};
