const { randomUUID } = require('node:crypto');

// TODO: replace with real Apify actor call using APIFY_TOKEN
async function fetchConnections() {
  return [
    {
      id: randomUUID(),
      name: 'Leila Park',
      role: 'ML Engineer',
      company: 'OpenAI',
      location: 'San Francisco, CA',
      platforms: ['LinkedIn', 'Instagram'],
      tags: ['AI', 'Engineering'],
      lastInteraction: '2026-03-18',
      notes: 'Interested in founder tooling and AI developer workflows.',
    },
    {
      id: randomUUID(),
      name: 'James Tao',
      role: 'Research Scientist',
      company: 'Anthropic',
      location: 'San Francisco, CA',
      platforms: ['LinkedIn'],
      tags: ['AI', 'Research'],
      lastInteraction: '2026-03-14',
      notes: 'Open to technical founder chats and product feedback.',
    },
    {
      id: randomUUID(),
      name: 'Nina Solis',
      role: 'Product Lead',
      company: 'Cohere',
      location: 'San Francisco, CA',
      platforms: ['LinkedIn', 'Instagram'],
      tags: ['AI', 'Product'],
      lastInteraction: '2026-03-12',
      notes: 'Strong GTM and product strategy perspective.',
    },
    {
      id: randomUUID(),
      name: 'Sara Reyes',
      role: 'Product Manager',
      company: 'Stripe',
      location: 'San Francisco, CA',
      platforms: ['LinkedIn'],
      tags: ['Fintech', 'Hiring'],
      lastInteraction: '2026-03-10',
      notes: 'Can advise on hiring loops for early-stage PM teams.',
    },
    {
      id: randomUUID(),
      name: 'Marcus Kim',
      role: 'Founder',
      company: 'YC W24',
      location: 'New York, NY',
      platforms: ['Instagram'],
      tags: ['Founder', 'SaaS'],
      lastInteraction: '2026-03-09',
      notes: 'Building a B2B workflow startup; open to partnerships.',
    },
    {
      id: randomUUID(),
      name: 'Dan Walsh',
      role: 'Investor',
      company: 'Andreessen Horowitz',
      location: 'Menlo Park, CA',
      platforms: ['LinkedIn'],
      tags: ['Investor', 'AI'],
      lastInteraction: '2026-03-06',
      notes: 'Tracks applied AI companies at seed and Series A stages.',
    },
  ];
}

module.exports = {
  fetchConnections,
};
