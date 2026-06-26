// Central placeholder dataset for quick swapping with backend data later.
export const statsData = [
  {
    label: 'Total connections',
    value: '1,847',
    subtext: '+12 this week',
    subtextClass: 'text-emerald-600',
  },
  {
    label: 'LinkedIn',
    value: '1,203',
    subtext: '2nd+ degree: 8.4k',
    subtextClass: 'text-zinc-500',
  },
  {
    label: 'Instagram',
    value: '644',
    subtext: 'Mutual follows: 312',
    subtextClass: 'text-zinc-500',
  },
  {
    label: 'Overlap',
    value: '89',
    subtext: 'on both platforms',
    subtextClass: 'text-zinc-500',
  },
];

export const recentConnections = [
  {
    id: 'sara-reyes',
    initials: 'SR',
    avatarClass: 'bg-rose-100 text-rose-700',
    name: 'Sara Reyes',
    roleCompany: 'PM at Stripe',
    location: 'SF',
    platforms: ['LI'],
  },
  {
    id: 'marcus-kim',
    initials: 'MK',
    avatarClass: 'bg-orange-100 text-orange-700',
    name: 'Marcus Kim',
    roleCompany: 'Founder · YC W24',
    location: '',
    platforms: ['IG'],
  },
  {
    id: 'leila-park',
    initials: 'LP',
    avatarClass: 'bg-violet-100 text-violet-700',
    name: 'Leila Park',
    roleCompany: 'ML Eng · OpenAI',
    location: '',
    platforms: ['LI', 'IG'],
  },
  {
    id: 'dan-walsh',
    initials: 'DW',
    avatarClass: 'bg-emerald-100 text-emerald-700',
    name: 'Dan Walsh',
    roleCompany: 'VC · Andreessen',
    location: '',
    platforms: ['LI'],
  },
];

export const initialChatMessages = [
  {
    id: 'm1',
    role: 'assistant',
    text: "Hi! I've indexed your 1,847 connections. Ask me anything - introductions, warm paths, or actions.",
  },
  {
    id: 'm2',
    role: 'user',
    text: 'Who in my network works in AI and is based in SF?',
  },
  {
    id: 'm3',
    role: 'assistant',
    text: 'Found 34 contacts in AI + SF. Top matches: Leila Park (OpenAI), James Tao (Anthropic), Nina Solis (Cohere). Want intros or a shortlist?',
  },
];

export const suggestedActionItems = [
  {
    id: 'a1',
    title: 'Warm path to Stripe hiring',
    description: 'Sara Reyes -> James Tao (mutual)',
    buttonLabel: 'Draft intro',
  },
  {
    id: 'a2',
    title: '89 contacts on both platforms',
    description: 'Merge profiles for full view',
    buttonLabel: 'Merge',
  },
  {
    id: 'a3',
    title: '12 new connections this week',
    description: 'Send personalized follow-ups',
    buttonLabel: 'Review',
  },
];

export const networkMapNodes = [
  { id: 'you', x: 230, y: 120, r: 12, color: '#8b5cf6', label: 'You' },
  { id: 'n1', x: 135, y: 75, r: 8, color: '#14b8a6' },
  { id: 'n2', x: 320, y: 70, r: 8, color: '#f97316' },
  { id: 'n3', x: 88, y: 150, r: 8, color: '#3b82f6' },
  { id: 'n4', x: 175, y: 195, r: 8, color: '#22c55e' },
  { id: 'n5', x: 300, y: 192, r: 8, color: '#ef4444' },
  { id: 'n6', x: 375, y: 142, r: 8, color: '#a855f7' },
  { id: 'n7', x: 250, y: 42, r: 7, color: '#0ea5e9' },
];

export const networkMapEdges = [
  ['you', 'n1'],
  ['you', 'n2'],
  ['you', 'n3'],
  ['you', 'n4'],
  ['you', 'n5'],
  ['you', 'n6'],
  ['you', 'n7'],
  ['n1', 'n3'],
  ['n2', 'n6'],
  ['n4', 'n5'],
];
