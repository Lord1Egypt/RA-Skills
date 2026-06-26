#!/usr/bin/env node
/**
 * restaurant-hooks.js
 * Generates viral hooks for restaurant TikTok/Instagram content.
 * 
 * Usage:
 *   node restaurant-hooks.js --type "pizza" --style "curiosity" --count 10
 *   node restaurant-hooks.js --type "sushi" --style "all" --location "Antwerp"
 * 
 * Hook styles: curiosity | shock | emotion | asmr | challenge | comparison | story | all
 */

'use strict';

// ─── Hook Database ───────────────────────────────────────────────────────────

const HOOK_STYLES = {
  curiosity: {
    name: 'Curiosity / Forbidden Knowledge',
    description: 'Makes viewer feel they\'re discovering a secret',
    bestFor: 'Process reveals, ingredient stories, behind the scenes',
    templates: [
      'What {restaurantType} restaurants don\'t want you to know about {dish}',
      'The real reason our {dish} tastes different from everyone else\'s',
      'We\'ve never shown this before. The secret behind our {dish}.',
      'I worked at 5 {restaurantType} restaurants. Here\'s what I learned.',
      'Why chefs hate this one thing about making {dish} — and we do it anyway',
      'What happens in our kitchen that we don\'t show on the menu',
      'The ingredient in our {dish} that nobody ever guesses',
      'This is what {dish} looks like when it\'s made properly vs. cut corners',
      'Why our {dish} takes twice as long to make as our competitors',
      'The technique we stole from a Michelin-star restaurant for our {dish}',
    ],
  },
  shock: {
    name: 'Size / Value Shock',
    description: 'Triggers disbelief at price-to-value ratio',
    bestFor: 'Portion reveals, price comparisons, quantity videos',
    templates: [
      'I paid €{price} for THIS amount of {dish}. Worth it? 👀',
      'This is what €{price} gets you at {restaurantName} in {location}',
      'POV: you ordered the biggest {dish} on the menu',
      'Nobody told me it would be this big 😱',
      'We challenged ourselves to make the biggest {dish} in {location}',
      'The {dish} that makes people question if they can finish it',
      '{number} pieces for €{price}. We might be crazy.',
      'Our portions are getting out of hand and we\'re not sorry',
      'When the kitchen said "extra large" they meant it',
      'I thought I ordered a normal {dish}. I was wrong. 💀',
    ],
  },
  emotion: {
    name: 'Emotional / Story Hook',
    description: 'Creates personal connection and shares',
    bestFor: 'Chef stories, family recipes, anniversary posts',
    templates: [
      'He\'s been making this {dish} for {years} years. Here\'s his story.',
      'My grandmother taught me this recipe. I\'ve never shared it. Until now.',
      'We almost closed during COVID. This is why we kept going.',
      'The regular customer who comes every week — and what he always orders.',
      '{years} years in {location}. This is what we\'ve learned.',
      'This dish was on the menu on day 1. We\'ll never remove it.',
      'The chef who left a 3-star restaurant to make simple, honest food.',
      'My father built this place with his hands. I cook here every day.',
      'The moment I knew this was the right career.',
      'We had our worst night ever last month. Here\'s what it taught us.',
    ],
  },
  asmr: {
    name: 'ASMR / Sensory Hook',
    description: 'Pure visual/audio satisfaction — no text needed',
    bestFor: 'Cooking processes, textures, sizzling, cutting',
    templates: [
      '🔇 Watch with sound. You\'re welcome.',
      'The sound of a perfect {dish}. You\'ll know it when you hear it.',
      'ASMR: {dish} edition 🎧',
      'No words needed. Just watch.',
      'That sizzle tho 🔥',
      'Close your eyes and listen. That\'s the sound of fresh {dish}.',
      'Satisfying {dish} prep. Watch all the way through.',
      'The crunch. The steam. The reveal. 😮',
      'This video has no words. Just {dish}. Just vibes.',
      'Put your phone down after this. You won\'t be hungry anymore.',
    ],
  },
  challenge: {
    name: 'Challenge / Dare Hook',
    description: 'Invites participation and comments',
    bestFor: 'Spicy food, big portions, eating challenges',
    templates: [
      'Finish this in {time} and it\'s free. Has anyone done it?',
      'I dare you to not get hungry watching this.',
      'We bet you can\'t name a better {dish} in {location}. Tell us in the comments.',
      'Challenge accepted: can we make {dish} in under {time} minutes?',
      'If you can name the secret ingredient, free {dish} on us.',
      'Rating every {dish} on our menu. Brutally honestly.',
      'We tried every {cuisine} in {location}. Here\'s the ranking.',
      'Hot sauce challenge with our staff. Who lasts longest?',
      'Can you eat this alone? Most people can\'t.',
      'We gave this to 100 people. Only {number} finished it.',
    ],
  },
  comparison: {
    name: 'Us vs Them / Comparison',
    description: 'Creates relatability through contrast',
    bestFor: 'Quality positioning, price comparison, before/after',
    templates: [
      'What {amount} of {dish} gets you at fast food vs our place',
      'Cheap {dish} vs. our {dish}. The difference is obvious.',
      'Before we perfected our recipe vs. now',
      'Generic {cuisine} restaurant vs. {restaurantName}',
      'What {dish} looks like when it\'s made with love vs. made to fill a quota',
      'We raised our prices. Here\'s what changed (and what didn\'t).',
      'Why our {dish} costs €{price} more — and why it\'s worth it',
      'The difference {years} years of practice makes',
      '{location}\'s most expensive {dish} vs. most affordable. We\'re neither.',
      'Takeaway {dish} vs. dining in at {restaurantName}. Same kitchen.',
    ],
  },
  pov: {
    name: 'POV / Immersive',
    description: 'First-person experience format, very high watch time',
    bestFor: 'Kitchen tours, ordering experience, staff day-in-life',
    templates: [
      'POV: it\'s your first day working at {restaurantName}',
      'POV: you\'re watching your {dish} being made right now',
      'POV: you\'re the chef and you have 200 orders to fill tonight',
      'POV: you just walked into {restaurantName} for the first time',
      'POV: it\'s Friday night and we\'ve been open for {hours} hours',
      'POV: you ordered last before closing time and we\'re still smiling',
      'POV: you\'re a regular and you know exactly what you\'re getting',
      'POV: our dishwasher just called in sick and service starts in 30 minutes',
      'POV: you\'re the first customer on opening day',
      'POV: you ordered the chef\'s special and he\'s extra proud of this one',
    ],
  },
  story: {
    name: 'Story / Narrative',
    description: 'Watch-through format, strong saves and shares',
    bestFor: 'Brand story, dish origin, staff profiles',
    templates: [
      'How {restaurantName} went from {start} to what it is today',
      'The dish that almost didn\'t make it onto the menu',
      'Why we\'ve never changed our {dish} recipe in {years} years',
      'The supplier who\'s been delivering our {ingredient} for {years} years',
      'The night we had our first full house. We still talk about it.',
      'How we built {restaurantName} with {budget} and a dream',
      'The moment we knew the restaurant was going to work',
      'The dish our team argues about most (spoiler: it\'s the {dish})',
      'From home kitchen to {location}\'s most talked about {cuisine}',
      'Our worst online review — and what we did about it',
    ],
  },
};

// ─── Restaurant-Specific Amplifiers ──────────────────────────────────────────

const RESTAURANT_AMPLIFIERS = {
  pizza: {
    dishes: ['pizza', 'dough', 'calzone', 'tiramisu', 'focaccia'],
    uniqueAngles: ['cheese pull', 'wood-fired oven', 'hand-tossed dough', 'San Marzano tomatoes', 'mozzarella fior di latte'],
    localHashtags: ['#pizzalovers', '#pizzabelgium', '#italianfood', '#pizzatime', '#napolipizza'],
    sounds: ['dough slapping on counter', 'oven door creak', 'cheese bubble', 'crust crunch'],
  },
  sushi: {
    dishes: ['sashimi', 'salmon roll', 'nigiri', 'maki', 'temaki', 'chirashi'],
    uniqueAngles: ['knife skills', 'fish freshness', 'rice preparation', 'daily delivery from market'],
    localHashtags: ['#sushilover', '#sushitime', '#japanesefood', '#sushibelgium', '#omakase'],
    sounds: ['knife on cutting board', 'rice scooping', 'soy sauce pour'],
  },
  burger: {
    dishes: ['smash burger', 'double stack', 'bacon cheeseburger', 'loaded fries', 'milkshake'],
    uniqueAngles: ['smash technique', 'butter basting', 'brioche bun', 'dry-aged beef', 'house sauce'],
    localHashtags: ['#burgerlovers', '#smashburger', '#burgerbegium', '#foodporn', '#burgerjoint'],
    sounds: ['sizzle on griddle', 'crispy crunch', 'sauce squirt'],
  },
  kebab: {
    dishes: ['durum', 'döner kebab', 'pita', 'falafel', 'loaded kebab box'],
    uniqueAngles: ['meat rotation', 'fresh bread', 'house sauce recipe', 'open until late', 'generous portions'],
    localHashtags: ['#kebab', '#kebablovers', '#turkishfood', '#latenight', '#foodbelgium'],
    sounds: ['meat slicer', 'bread pressing', 'sauce drizzle'],
  },
  vegan: {
    dishes: ['buddha bowl', 'vegan burger', 'plant-based steak', 'cashew cheese', 'acai bowl'],
    uniqueAngles: ['zero-waste kitchen', 'local farmers', 'seasonal menu', 'no compromise on flavor'],
    localHashtags: ['#vegan', '#plantbased', '#veganfood', '#veganbelgium', '#govegan'],
    sounds: ['blender', 'vegetable chopping', 'nut grinding'],
  },
};

// ─── Core Generator ───────────────────────────────────────────────────────────

function fillTemplate(template, vars = {}) {
  return template.replace(/\{(\w+)\}/g, (match, key) => {
    return vars[key] !== undefined ? vars[key] : match;
  });
}

function getRestaurantVars(restaurantType, options = {}) {
  const baseVars = {
    restaurantType: restaurantType || 'restaurant',
    restaurantName: options.name || 'ons restaurant',
    location: options.location || 'België',
    dish: options.dish || getDishForType(restaurantType),
    years: options.years || String(Math.floor(Math.random() * 15) + 5),
    price: options.price || String(Math.floor(Math.random() * 15) + 8),
    number: options.number || String(Math.floor(Math.random() * 150) + 50),
    time: options.time || '10',
    amount: options.amount || '€15',
    hours: options.hours || '10',
    budget: options.budget || 'almost nothing',
    start: options.start || 'a small window',
    ingredient: options.ingredient || 'geheim ingredient',
    cuisine: restaurantType || 'food',
  };

  const amplifier = RESTAURANT_AMPLIFIERS[restaurantType.toLowerCase()];
  if (amplifier) {
    baseVars.dish = options.dish || amplifier.dishes[0];
    baseVars.uniqueAngle = amplifier.uniqueAngles[0];
    baseVars.sounds = amplifier.sounds.join(', ');
  }

  return baseVars;
}

function getDishForType(type) {
  const defaults = {
    pizza: 'pizza', pizzeria: 'pizza',
    sushi: 'sashimi', japans: 'sushi roll',
    burger: 'smash burger', burgers: 'double stack',
    kebab: 'döner kebab', shawarma: 'wrap',
    vegan: 'buddha bowl',
    asian: 'pad thai', wok: 'wok dish',
    bakery: 'croissant', patisserie: 'tart',
  };
  return defaults[type.toLowerCase()] || 'signature dish';
}

function generateHooks(options = {}) {
  const {
    restaurantType = 'restaurant',
    hookStyle = 'all',
    count = 10,
    location = 'België',
    name = 'ons restaurant',
    platform = 'tiktok',
  } = options;

  const vars = getRestaurantVars(restaurantType, { location, name });
  const results = [];

  const stylesToUse = hookStyle === 'all'
    ? Object.keys(HOOK_STYLES)
    : [hookStyle];

  // Collect all matching hooks
  const pool = [];
  stylesToUse.forEach(style => {
    const styleData = HOOK_STYLES[style];
    if (!styleData) return;
    styleData.templates.forEach(template => {
      pool.push({
        style: styleData.name,
        styleKey: style,
        rawTemplate: template,
        hook: fillTemplate(template, vars),
        description: styleData.description,
        bestFor: styleData.bestFor,
      });
    });
  });

  // Shuffle and pick `count` hooks
  const shuffled = pool.sort(() => Math.random() - 0.5);
  const selected = shuffled.slice(0, Math.min(count, shuffled.length));

  // Add platform-specific metadata
  selected.forEach((item, i) => {
    results.push({
      rank: i + 1,
      ...item,
      platform,
      tipsForUse: getHookTips(item.styleKey, platform),
      exampleCaption: buildExampleCaption(item.hook, restaurantType, location),
    });
  });

  return {
    meta: {
      restaurantType,
      location,
      hookStyle,
      platform,
      count: results.length,
      generatedAt: new Date().toISOString(),
    },
    hooks: results,
    bonusTips: getBonusTips(platform),
  };
}

function getHookTips(styleKey, platform) {
  const tips = {
    curiosity: [
      'Pause on the "secret" moment — don\'t reveal too fast',
      'Let comments ask "what is it?" — don\'t answer immediately',
      'Works best when the reveal is genuinely surprising',
    ],
    shock: [
      'Show the full portion BEFORE price reveal',
      'Film the dish next to something for scale (hand, plate, person)',
      'React authentically — your face matters',
    ],
    emotion: [
      'Keep it under 60 seconds — emotion hits harder when compressed',
      'Add subtitles — many people watch without sound',
      'End with a quiet moment, not a hard CTA',
    ],
    asmr: [
      'No music — pure ambient sound',
      'Microphone close to the action',
      'Film in 4K if possible — texture needs detail',
    ],
    challenge: [
      'Pin a comment with the rules or the prize',
      'Follow up with results video — it drives return viewers',
      'Be authentic about whether anyone actually beat the challenge',
    ],
    comparison: [
      'Side-by-side format works best',
      'Don\'t mock competitors — focus on your strengths',
      'The contrast should be obvious within 3 seconds',
    ],
    pov: [
      'Mount camera on head, hat, or pocket for true POV',
      'Switch perspectives (kitchen, customer, cashier) for variety',
      'The more immersive, the better — keep it shaky and real',
    ],
    story: [
      'Save the most emotional moment for the last 10 seconds',
      'Use old photos or footage if available',
      'Voiceover works better than talking-head for storytelling',
    ],
  };
  return tips[styleKey] || ['Keep it authentic', 'Film vertically (9:16)', 'Sound matters'];
}

function buildExampleCaption(hook, restaurantType, location) {
  const hashtags = [
    `#${restaurantType.toLowerCase().replace(/\s+/g, '')}`,
    `#${location.toLowerCase().replace(/\s+/g, '')}`,
    '#foodtiktok',
    '#restaurant',
    '#foodie',
    '#viral',
  ].join(' ');
  return `${hook}\n\nTag iemand die dit moet proberen 👇\n\n${hashtags}`;
}

function getBonusTips(platform) {
  const tips = {
    tiktok: [
      '🎣 Your hook determines if TikTok shows your video. Spend 50% of your effort on the first 2 seconds.',
      '📊 TikTok pushes videos that get rewatched — create "earn the rewatch" moments',
      '💬 Comment strategy: ask a question that has a short answer (not yes/no)',
      '🔁 Reply to comments with videos — TikTok loves this and boosts reach',
      '⏰ Post between 17:00-21:00 for restaurant content — dinner decision time',
    ],
    instagram: [
      '📸 Instagram rewards consistency — post Reels at the same time each day',
      '📌 Save-worthy content performs better — make people want to revisit your post',
      '🔗 Instagram Stories convert better — add "Reserve" sticker to story posts',
      '📊 Use Instagram Insights weekly — check which content drives profile visits',
      '🎯 Hashtags still matter — 15-20 relevant hashtags, mix of sizes',
    ],
  };
  return tips[platform] || tips.tiktok;
}

// ─── Output Formatters ─────────────────────────────────────────────────────

function formatAsMarkdown(result) {
  const { meta, hooks, bonusTips } = result;
  let md = `# 🎣 Viral Hook Generator — ${meta.restaurantType} in ${meta.location}\n\n`;
  md += `**Platform:** ${meta.platform} | **Style:** ${meta.hookStyle} | **Generated:** ${new Date(meta.generatedAt).toLocaleDateString()}\n\n`;
  md += `---\n\n`;

  hooks.forEach(h => {
    md += `## Hook #${h.rank} — ${h.style}\n\n`;
    md += `> **"${h.hook}"**\n\n`;
    md += `📍 Best for: *${h.bestFor}*\n\n`;
    md += `### 📝 Example Caption\n\`\`\`\n${h.exampleCaption}\n\`\`\`\n\n`;
    md += `### 💡 Tips for using this hook\n`;
    h.tipsForUse.forEach(tip => md += `- ${tip}\n`);
    md += `\n---\n\n`;
  });

  md += `## 🔥 Platform Tips for ${meta.platform.charAt(0).toUpperCase() + meta.platform.slice(1)}\n`;
  bonusTips.forEach(tip => md += `${tip}\n`);

  return md;
}

function formatAsText(result) {
  const { meta, hooks } = result;
  let out = `VIRAL HOOKS — ${meta.restaurantType.toUpperCase()} | ${meta.location}\n`;
  out += `${'='.repeat(60)}\n\n`;
  hooks.forEach(h => {
    out += `[${h.rank}] ${h.style.toUpperCase()}\n`;
    out += `    "${h.hook}"\n\n`;
  });
  return out;
}

// ─── CLI Entry Point ──────────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  const getArg = (flag) => {
    const idx = args.indexOf(flag);
    return idx !== -1 ? args[idx + 1] : null;
  };

  const options = {
    restaurantType: getArg('--type') || 'restaurant',
    hookStyle: getArg('--style') || getArg('--hook-style') || 'all',
    count: parseInt(getArg('--count') || '10', 10),
    location: getArg('--location') || 'België',
    name: getArg('--name') || 'Ons Restaurant',
    platform: getArg('--platform') || 'tiktok',
  };

  const outputFormat = getArg('--output') || 'markdown';
  const result = generateHooks(options);

  if (outputFormat === 'json') {
    console.log(JSON.stringify(result, null, 2));
  } else if (outputFormat === 'text') {
    console.log(formatAsText(result));
  } else {
    console.log(formatAsMarkdown(result));
  }
}

// ─── Module Exports ───────────────────────────────────────────────────────────

module.exports = {
  generateHooks,
  formatAsMarkdown,
  formatAsText,
  HOOK_STYLES,
  RESTAURANT_AMPLIFIERS,
};
