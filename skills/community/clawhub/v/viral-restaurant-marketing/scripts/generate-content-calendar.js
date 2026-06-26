#!/usr/bin/env node
/**
 * generate-content-calendar.js
 * Generates a weekly content calendar for restaurant social media marketing.
 * 
 * Usage:
 *   node generate-content-calendar.js --type "pizza" --location "Leuven" --frequency 4
 *   node generate-content-calendar.js --type "sushi" --frequency 5 --output json
 * 
 * Or require as module:
 *   const { generateCalendar } = require('./generate-content-calendar.js');
 */

'use strict';

// ─── Content Library ────────────────────────────────────────────────────────

const CONTENT_FORMATS = {
  behind_scenes: {
    name: 'Behind the Scenes',
    description: 'Show kitchen prep, staff, processes',
    platforms: ['tiktok', 'instagram'],
    duration: '15-30s',
    effort: 'low',
    viralPotential: 'high',
  },
  product_showcase: {
    name: 'Product Showcase',
    description: 'Feature your best-looking dish',
    platforms: ['tiktok', 'instagram'],
    duration: '10-20s',
    effort: 'low',
    viralPotential: 'medium',
  },
  chef_story: {
    name: 'Chef/Staff Story',
    description: 'Personal story from the team',
    platforms: ['instagram', 'tiktok'],
    duration: '30-60s',
    effort: 'medium',
    viralPotential: 'high',
  },
  transformation: {
    name: 'Raw → Ready Transformation',
    description: 'Show the full cooking process timelapse',
    platforms: ['tiktok', 'instagram'],
    duration: '15-30s',
    effort: 'low',
    viralPotential: 'very_high',
  },
  customer_reaction: {
    name: 'Customer Reaction',
    description: 'Film a real customer trying your dish',
    platforms: ['tiktok', 'instagram'],
    duration: '10-20s',
    effort: 'medium',
    viralPotential: 'very_high',
  },
  slideshow: {
    name: 'TikTok Slideshow',
    description: 'Photo carousel: dish + story + CTA',
    platforms: ['tiktok'],
    duration: 'N/A (photos)',
    effort: 'very_low',
    viralPotential: 'medium',
  },
  review_feature: {
    name: 'Google Review Feature',
    description: 'Show off a glowing 5-star review',
    platforms: ['instagram', 'tiktok'],
    duration: '10-15s',
    effort: 'very_low',
    viralPotential: 'low',
  },
  day_in_life: {
    name: 'Day in the Life',
    description: 'Follow chef/staff through a full shift',
    platforms: ['tiktok', 'instagram'],
    duration: '45-90s',
    effort: 'high',
    viralPotential: 'very_high',
  },
};

const HOOK_TEMPLATES_BY_TYPE = {
  pizza: [
    'POV: you work at the best pizza place in {location}',
    'We asked 100 people what the best pizza in {location} is. They all said us.',
    'I\'ve been making this dough for {years} years. Here\'s the secret.',
    'Why does our pizza taste different? Watch until the end.',
    'The cheese pull that broke the internet 🧀',
    'We make {number} pizzas every Friday. Here\'s how.',
    'Honest review: we tried our own pizza and here\'s what we think',
  ],
  sushi: [
    'This is what real sushi looks like at {restaurantName}',
    'How we cut salmon for {number} rolls — every morning at 7am',
    'POV: you\'re watching our chef prepare your order',
    'The difference between cheap sushi and ours (shown in 20 seconds)',
    'ASMR: knife meets fish. Watch with sound 🔇',
    'We\'ve been making this roll for {years} years. Never changing it.',
    'What €{price} of sushi actually looks like at our place',
  ],
  burger: [
    'The smash burger that made our restaurant go viral',
    'We added a new burger. Here\'s the HONEST verdict from our chef.',
    'Behind the grill: what happens when you order a burger from us',
    'That sauce drip tho 👀',
    'We challenged ourselves: can we make a better burger than McDonald\'s?',
    'First bite reaction: our {name} burger hits different',
    'How we stack the perfect burger every single time',
  ],
  kebab: [
    'You won\'t believe how much meat is in this kebab 👀',
    'The kebab that\'s making everyone drive to {location}',
    'Real talk: this is how we make our {product} every day',
    'POV: it\'s 2am and you need the best kebab in {location}',
    'We tried every kebab in {location}. We still think ours is better.',
    'How we prep {number}kg of meat before we even open',
    'When the customer said our kebab was too big 😂',
  ],
  finedining: [
    'What €{price} fine dining in {location} actually looks like',
    'Our chef plated this dish {number} times before he was happy with it',
    'Behind the kitchen pass: the 3 seconds that matter most',
    'What diners don\'t see before their plate arrives',
    'We changed our tasting menu. Here\'s why.',
    'From garden to plate — where our {ingredient} comes from',
    'The dish that took {years} years to perfect',
  ],
  vegan: [
    'Wait — this is 100% plant-based? 🌱',
    'We turned {meat dish} into a vegan masterpiece. Taste test inside.',
    'The best vegan {dish} in {location} (no, really)',
    'People keep asking if our {dish} contains meat. It doesn\'t.',
    'How we make vegan comfort food that actually hits',
    'We challenged a meat-lover to try our menu. Here\'s what happened.',
    'The plant-based protein hack our chef uses every day',
  ],
  asian: [
    'The wok technique that took 10 years to master',
    'Why our {dish} tastes different from every other Asian place in {location}',
    'We import our {ingredient} directly from {country}. Here\'s why.',
    'Authentic {cuisine} in {location} — this is what it looks like',
    'ASMR: wok on fire 🔥 watch with sound',
    'How our chef makes {dish} in under 3 minutes',
    'The secret spice blend we\'ve never shared publicly (until now)',
  ],
  bakery: [
    'Croissant layers: {number} — count them 🥐',
    'We start baking at 4am so you can have this by 7',
    'The sound of a perfect croissant. You\'ll know it when you hear it.',
    'How we make {number} croissants before sunrise',
    'Our baker has been doing this since {year}. Watch his hands.',
    'The glaze pour that made 2 million people hungry',
    'Why our bread is different (it\'s the {ingredient})',
  ],
  general: [
    'This is what we do every morning before we open',
    'The dish our regulars order every single week',
    'We\'ve been in {location} for {years} years. Here\'s our story.',
    'What happens in our kitchen while you wait for your order',
    'POV: your food is being prepared right now',
    'The secret ingredient in our most popular dish',
    'Why our {dish} has a {waitlist/lineup} every weekend',
  ],
};

const CTAS = {
  engagement: [
    'Comment your order below 👇',
    'Tag someone you\'d bring here 👇',
    'Drop a 🍕 if you want this',
    'What should we show next? Tell us 👇',
    'Rate this from 1-10 in the comments',
    'Would you try this? Yes or No 👇',
  ],
  conversion: [
    'Link in bio to order now 🔗',
    'Book your table — link in bio',
    'Order tonight — we close at {time}',
    'Call us or DM to reserve',
    'Tap the link to see our full menu',
    'Swipe up to book your spot this weekend',
  ],
  sharing: [
    'Share this with someone who needs to eat here',
    'Send this to your foodie friend',
    'Tag the person who would finish this alone',
    'Share if this made you hungry 🤤',
    'Save this for your next night out 📌',
  ],
  social_proof: [
    'Over {number} 5-star reviews. See why.',
    'This is why we\'re the #1 rated {cuisine} in {location}',
    'Our customers keep coming back. Here\'s why.',
    'Join {number}+ happy customers this month',
  ],
};

const WEEKLY_SCHEDULE = {
  3: ['tuesday', 'thursday', 'saturday'],
  4: ['monday', 'wednesday', 'friday', 'saturday'],
  5: ['monday', 'tuesday', 'thursday', 'friday', 'saturday'],
  6: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
  7: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
};

const POSTING_TIMES = {
  tiktok: {
    weekday: ['17:30', '19:00', '21:00'],
    weekend: ['12:00', '17:00', '20:00'],
  },
  instagram: {
    weekday: ['11:00', '17:00', '20:00'],
    weekend: ['10:00', '14:00', '19:00'],
  },
};

const WEEKEND_DAYS = ['friday', 'saturday', 'sunday'];

// ─── Core Functions ──────────────────────────────────────────────────────────

function getRandomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function fillTemplate(template, vars = {}) {
  return template.replace(/\{(\w+)\}/g, (match, key) => vars[key] || match);
}

function getHooksForType(restaurantType) {
  const type = restaurantType.toLowerCase();
  const typeMap = {
    pizza: 'pizza', pizzeria: 'pizza',
    sushi: 'sushi', japans: 'sushi', japanese: 'sushi',
    burger: 'burger', burgers: 'burger', smashburger: 'burger',
    kebab: 'kebab', turks: 'kebab', shawarma: 'kebab', döner: 'kebab',
    'fine dining': 'finedining', finedining: 'finedining', gastronomisch: 'finedining',
    vegan: 'vegan', vegetarisch: 'vegan', vegetarian: 'vegan', plantbased: 'vegan',
    aziatisch: 'asian', asian: 'asian', chinees: 'asian', thai: 'asian', wok: 'asian',
    bakkerij: 'bakery', bakery: 'bakery', patisserie: 'bakery', brood: 'bakery',
  };

  const key = typeMap[type] || 'general';
  return HOOK_TEMPLATES_BY_TYPE[key] || HOOK_TEMPLATES_BY_TYPE.general;
}

function getFormatRotation(postsPerWeek) {
  const formats = [
    'behind_scenes',
    'transformation',
    'product_showcase',
    'chef_story',
    'customer_reaction',
    'slideshow',
    'review_feature',
    'day_in_life',
  ];
  // Prioritize high-viral formats first
  const prioritized = [
    'transformation',
    'behind_scenes',
    'customer_reaction',
    'chef_story',
    'product_showcase',
    'slideshow',
    'review_feature',
    'day_in_life',
  ];
  return prioritized.slice(0, postsPerWeek);
}

function buildPost(day, formatKey, restaurantType, location, vars = {}) {
  const format = CONTENT_FORMATS[formatKey];
  const hooks = getHooksForType(restaurantType);
  const hook = fillTemplate(getRandomItem(hooks), { location, ...vars });

  const isWeekend = WEEKEND_DAYS.includes(day.toLowerCase());
  const tiktokTime = getRandomItem(POSTING_TIMES.tiktok[isWeekend ? 'weekend' : 'weekday']);
  const igTime = getRandomItem(POSTING_TIMES.instagram[isWeekend ? 'weekend' : 'weekday']);

  const ctaType = ['engagement', 'conversion', 'sharing', 'social_proof'];
  const ctaKey = day === 'friday' || day === 'saturday' ? 'conversion' : getRandomItem(ctaType);
  const cta = fillTemplate(getRandomItem(CTAS[ctaKey] || CTAS.engagement), { location, ...vars });

  return {
    day,
    format: format.name,
    formatKey,
    hook,
    cta,
    platforms: format.platforms,
    duration: format.duration,
    effort: format.effort,
    viralPotential: format.viralPotential,
    postingTimes: {
      tiktok: tiktokTime,
      instagram: igTime,
    },
    caption: `${hook}\n\n${cta}\n\n#${restaurantType.toLowerCase().replace(/\s+/g, '')} #${location.toLowerCase().replace(/\s+/g, '')} #restaurant #food #foodie`,
    filmingNotes: getFilmingNotes(formatKey, restaurantType),
  };
}

function getFilmingNotes(formatKey, restaurantType) {
  const notes = {
    behind_scenes: [
      'Film from behind the counter/kitchen',
      'Use natural light if possible, avoid harsh overhead light',
      'Capture movement: stirring, plating, cutting',
      'Film in portrait (9:16) for TikTok/Reels',
    ],
    transformation: [
      'Start with raw ingredients close-up',
      'Film each major step (prep, cook, plate)',
      'Speed up to 2-3x in edit',
      'End on the final dish with a slow reveal',
    ],
    product_showcase: [
      'Clean surface + neutral background',
      'Good lighting (ring light or window light)',
      'Get close: texture, color, steam, drip',
      'Film at 1080p minimum, vertical format',
    ],
    chef_story: [
      'Interview format or voiceover while working',
      'Ask: why did you start? what makes you proud?',
      'Keep it under 60 seconds',
      'Subtitles are mandatory for this format',
    ],
    customer_reaction: [
      'Ask regular customer permission before filming',
      'Capture the first bite moment',
      'Film their face + the dish in one shot if possible',
      'Keep it spontaneous — don\'t over-direct',
    ],
    slideshow: [
      'Take 6-10 high-quality photos',
      'Mix: wide shot, close-up, detail, atmosphere',
      'Edit in TikTok app or CapCut',
      'Add trending music from TikTok Creative Center',
    ],
    review_feature: [
      'Screenshot a real 5-star review',
      'Animate it in CapCut or TikTok text tool',
      'Add a quick video of the dish being mentioned',
      'Thank the reviewer by name',
    ],
    day_in_life: [
      'Start filming when you arrive (before opening)',
      'Document each key moment: prep, opening, rush, closing',
      'Aim for 10-15 clips total',
      'Edit to 60-90 seconds with upbeat background music',
    ],
  };
  return notes[formatKey] || ['Film in portrait (9:16)', 'Good lighting', 'Short and punchy'];
}

// ─── Main Generator ──────────────────────────────────────────────────────────

function generateCalendar(options = {}) {
  const {
    restaurantType = 'restaurant',
    location = 'Belgium',
    postsPerWeek = 4,
    platforms = ['tiktok', 'instagram'],
    restaurantName = 'ons restaurant',
    years = '10',
    number = '200',
    price = '15',
    ingredient = 'ingredient',
    country = 'Japan',
  } = options;

  const days = WEEKLY_SCHEDULE[postsPerWeek] || WEEKLY_SCHEDULE[4];
  const formats = getFormatRotation(postsPerWeek);
  const vars = { restaurantName, years, number, price, ingredient, country, location };

  const week = days.map((day, index) => {
    const formatKey = formats[index % formats.length];
    return buildPost(day, formatKey, restaurantType, location, vars);
  });

  return {
    meta: {
      restaurantType,
      location,
      postsPerWeek,
      platforms,
      generatedAt: new Date().toISOString(),
      weekNumber: getWeekNumber(new Date()),
    },
    week,
    summary: generateSummary(week),
    tips: getWeeklyTips(postsPerWeek),
  };
}

function generateSummary(week) {
  const formats = week.map(p => p.format);
  const highViral = week.filter(p => ['very_high', 'high'].includes(p.viralPotential));
  return {
    totalPosts: week.length,
    formats: formats,
    highViralPosts: highViral.length,
    lowEffortPosts: week.filter(p => ['low', 'very_low'].includes(p.effort)).length,
    platforms: [...new Set(week.flatMap(p => p.platforms))],
  };
}

function getWeeklyTips(postsPerWeek) {
  const tips = [
    '🎬 Batch film on one day — film all videos for the week in 2 hours',
    '📱 Always film in portrait (9:16) for maximum real estate',
    '⚡ Post between 17:00-20:00 for highest dinner-time reach',
    '💬 Reply to EVERY comment in the first 30 minutes after posting',
    '📊 Check Sunday: which video performed best? Make 2 more like it',
    '🔄 Cross-post TikTok videos to Instagram Reels & YouTube Shorts',
    '🎵 Use trending audio from TikTok Creative Center for each video',
    '📝 Add captions/subtitles — 85% of videos are watched without sound',
  ];
  if (postsPerWeek >= 5) {
    tips.push('🔥 With 5+ posts/week, you\'re in growth mode — consistency is key, perfect is the enemy of done');
  }
  return tips;
}

function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

// ─── Output Formatters ───────────────────────────────────────────────────────

function formatAsMarkdown(calendar) {
  const { meta, week, summary, tips } = calendar;
  let md = `# 📅 Content Calendar — Week ${meta.weekNumber}\n`;
  md += `**Restaurant:** ${meta.restaurantType} in ${meta.location}\n`;
  md += `**Posts this week:** ${meta.postsPerWeek} | **High-viral formats:** ${summary.highViralPosts}\n\n`;
  md += `---\n\n`;

  week.forEach((post, i) => {
    md += `## Day ${i + 1}: ${post.day.charAt(0).toUpperCase() + post.day.slice(1)}\n\n`;
    md += `**Format:** ${post.format} | **Effort:** ${post.effort} | **Viral Potential:** ${post.viralPotential}\n`;
    md += `**Platforms:** ${post.platforms.join(', ')} | **Duration:** ${post.duration}\n\n`;
    md += `### 🎣 Hook\n> ${post.hook}\n\n`;
    md += `### 📢 CTA\n> ${post.cta}\n\n`;
    md += `### 🕐 Best Posting Times\n`;
    post.platforms.forEach(p => {
      if (post.postingTimes[p]) md += `- ${p.charAt(0).toUpperCase() + p.slice(1)}: **${post.postingTimes[p]}**\n`;
    });
    md += `\n### 🎬 Filming Notes\n`;
    post.filmingNotes.forEach(note => md += `- ${note}\n`);
    md += `\n### 📝 Caption\n\`\`\`\n${post.caption}\n\`\`\`\n\n`;
    md += `---\n\n`;
  });

  md += `## 💡 Weekly Tips\n`;
  tips.forEach(tip => md += `${tip}\n`);

  return md;
}

function formatAsText(calendar) {
  const { meta, week } = calendar;
  let out = `CONTENT CALENDAR — Week ${meta.weekNumber} (${meta.restaurantType}, ${meta.location})\n`;
  out += `${'='.repeat(70)}\n\n`;
  week.forEach((post, i) => {
    out += `[${i + 1}] ${post.day.toUpperCase()} — ${post.format}\n`;
    out += `    Hook: "${post.hook}"\n`;
    out += `    CTA:  "${post.cta}"\n`;
    out += `    Post: TikTok @ ${post.postingTimes.tiktok || 'N/A'}, IG @ ${post.postingTimes.instagram || 'N/A'}\n\n`;
  });
  return out;
}

// ─── CLI Entry Point ─────────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  const getArg = (flag) => {
    const idx = args.indexOf(flag);
    return idx !== -1 ? args[idx + 1] : null;
  };

  const options = {
    restaurantType: getArg('--type') || 'restaurant',
    location: getArg('--location') || 'Belgium',
    postsPerWeek: parseInt(getArg('--frequency') || '4', 10),
    restaurantName: getArg('--name') || 'Our Restaurant',
  };

  const outputFormat = getArg('--output') || 'markdown';
  const calendar = generateCalendar(options);

  if (outputFormat === 'json') {
    console.log(JSON.stringify(calendar, null, 2));
  } else if (outputFormat === 'text') {
    console.log(formatAsText(calendar));
  } else {
    console.log(formatAsMarkdown(calendar));
  }
}

// ─── Module Exports ──────────────────────────────────────────────────────────

module.exports = {
  generateCalendar,
  formatAsMarkdown,
  formatAsText,
  getHooksForType,
  CONTENT_FORMATS,
  CTAS,
};
