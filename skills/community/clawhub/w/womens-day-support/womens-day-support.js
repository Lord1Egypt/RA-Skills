#!/usr/bin/env node

// Women's Day Support Skill
// Provides resources, inspiration, and practical tools for women

const WOMENS_DAY_RESOURCES = {
  globalHotlines: {
    "International Women's Helpline": "+1-800-799-7233",
    "UN Women Global Hotline": "+1-212-906-5000",
    "Global Fund for Women": "https://www.globalfundforwomen.org/"
  },
  
  mentalHealthResources: [
    "National Alliance on Mental Illness (NAMI) Helpline: 1-800-950-NAMI",
    "Crisis Text Line: Text HOME to 741741",
    "Women's Mental Health Resources: https://www.womenshealth.gov/mental-health"
  ],
  
  careerSupport: [
    "Lean In Circles: https://leanin.org/circles",
    "Girls Who Code: https://girlswhocode.com/",
    "Women Who Code: https://www.womenwhocode.com/",
    "Ellevate Network: https://ellevatenetwork.com/"
  ],
  
  inspirationalQuotes: [
    "Here's to strong women: May we know them, may we be them, may we raise them. - Unknown",
    "I am not free while any woman is unfree, even when her shackles are very different from my own. - Audre Lorde",
    "Well-behaved women seldom make history. - Laurel Thatcher Ulrich",
    "A woman with a voice is, by definition, a strong woman. - Melinda Gates"
  ]
};

function getRandomQuote() {
  const quotes = WOMENS_DAY_RESOURCES.inspirationalQuotes;
  return quotes[Math.floor(Math.random() * quotes.length)];
}

function getLocalResources(countryCode) {
  // This would be expanded with country-specific resources
  const localResources = {
    "CN": {
      "hotlines": ["Women's Rights Hotline: 12338"],
      "organizations": ["All-China Women's Federation: http://www.women.org.cn/"]
    },
    "US": {
      "hotlines": ["National Domestic Violence Hotline: 1-800-799-7233"],
      "organizations": ["American Association of University Women: https://www.aauw.org/"]
    }
  };
  
  return localResources[countryCode] || localResources["US"];
}

// Main skill function
async function womensDaySupport(context) {
  const { countryCode = "US", resourceType = "all" } = context;
  
  let response = `🌸 Happy International Women's Day! 🌸\n\n`;
  
  // Add inspirational quote
  response += `✨ ${getRandomQuote()}\n\n`;
  
  // Add resources based on type requested
  if (resourceType === "all" || resourceType === "mental") {
    response += `🧠 **Mental Health Resources:**\n${WOMENS_DAY_RESOURCES.mentalHealthResources.map(r => `- ${r}`).join('\n')}\n\n`;
  }
  
  if (resourceType === "all" || resourceType === "career") {
    response += `💼 **Career Support:**\n${WOMENS_DAY_RESOURCES.carealSupport.map(r => `- ${r}`).join('\n')}\n\n`;
  }
  
  if (resourceType === "all" || resourceType === "local") {
    const local = getLocalResources(countryCode);
    response += `🌍 **Local Resources (${countryCode}):**\n`;
    response += `Hotlines:\n${local.hotlines.map(h => `- ${h}`).join('\n')}\n`;
    response += `Organizations:\n${local.organizations.map(o => `- ${o}`).join('\n')}\n\n`;
  }
  
  response += `💡 **Self-Care Reminder:** Take time today to honor yourself and your achievements. You matter!\n\n`;
  
  return response;
}

// Export for OpenClaw integration
module.exports = { womensDaySupport };