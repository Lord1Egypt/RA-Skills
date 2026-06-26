#!/usr/bin/env node
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const walvisDir = join(homedir(), '.walvis');
const spacesDir = join(walvisDir, 'spaces');

// Ensure directories exist
mkdirSync(spacesDir, { recursive: true });

const mockItems = [
  // Link bookmarks with screenshots
  {
    id: 'mock-1',
    type: 'link',
    url: 'https://example.com/deep-sea-creatures',
    title: 'Bioluminescent Organisms of the Deep Sea',
    summary: 'Exploring the fascinating world of creatures that produce their own light in the darkest depths of the ocean.',
    tags: ['marine-biology', 'bioluminescence', 'deep-sea'],
    content: 'A comprehensive guide to bioluminescent organisms...',
    createdAt: '2026-03-01T10:30:00Z',
    updatedAt: '2026-03-02T14:20:00Z',
    source: 'telegram',
    analyzedBy: 'gpt-4o',
    screenshot: 'https://picsum.photos/seed/deepsea1/800/600',
    notes: 'Great reference for the project aesthetic'
  },
  {
    id: 'mock-2',
    type: 'link',
    url: 'https://example.com/walrus-protocol',
    title: 'Walrus Protocol: Decentralized Storage Architecture',
    summary: 'Technical deep-dive into Walrus blob storage, erasure coding, and the Sui blockchain integration.',
    tags: ['walrus', 'blockchain', 'storage', 'sui'],
    content: 'Walrus uses erasure coding to distribute data...',
    createdAt: '2026-02-28T09:15:00Z',
    source: 'web',
    analyzedBy: 'claude-3-opus',
    screenshot: 'https://picsum.photos/seed/walrus2/800/450'
  },
  {
    id: 'mock-3',
    type: 'link',
    url: 'https://example.com/tanstack-router',
    title: 'TanStack Router: Type-Safe Routing for React',
    summary: 'Modern file-based routing with full TypeScript support, search params validation, and nested layouts.',
    tags: ['react', 'routing', 'typescript', 'tanstack'],
    content: 'TanStack Router provides a fully type-safe routing solution...',
    createdAt: '2026-02-27T16:45:00Z',
    updatedAt: '2026-03-01T11:00:00Z',
    source: 'telegram',
    analyzedBy: 'gpt-4o',
    screenshot: 'https://picsum.photos/seed/router3/800/500',
    notes: 'Check out the search params API'
  },
  {
    id: 'mock-4',
    type: 'link',
    url: 'https://example.com/mymind-design',
    title: 'mymind: Visual Bookmarking Done Right',
    summary: 'Case study on mymind\'s minimalist, image-first approach to personal knowledge management.',
    tags: ['design', 'ui-ux', 'bookmarks', 'inspiration'],
    content: 'mymind revolutionized bookmarking with its visual-first approach...',
    createdAt: '2026-02-26T13:20:00Z',
    source: 'web',
    analyzedBy: 'claude-3-opus',
    screenshot: 'https://picsum.photos/seed/mymind4/800/550'
  },
  {
    id: 'mock-5',
    type: 'link',
    url: 'https://example.com/openclaw-skills',
    title: 'Building OpenClaw Skills: A Developer Guide',
    summary: 'Complete guide to creating custom OpenClaw skills with SKILL.md, hooks, and Telegram integration.',
    tags: ['openclaw', 'telegram', 'ai-agents', 'tutorial'],
    content: 'OpenClaw skills are defined using SKILL.md frontmatter...',
    createdAt: '2026-02-25T08:00:00Z',
    source: 'telegram',
    analyzedBy: 'gpt-4o',
    screenshot: 'https://picsum.photos/seed/openclaw5/800/480'
  },
  // Text/note bookmarks
  {
    id: 'mock-6',
    type: 'note',
    title: 'Hackathon Submission Checklist',
    summary: 'Final items to complete before OpenClaw x Sui hackathon deadline.',
    tags: ['hackathon', 'todo', 'deadline'],
    content: '- [ ] Test all Telegram commands\n- [ ] Deploy web UI to Walrus Sites\n- [ ] Record demo video\n- [ ] Write submission description\n- [ ] Submit to DeepSurge platform',
    createdAt: '2026-03-04T18:30:00Z',
    updatedAt: '2026-03-05T09:00:00Z',
    source: 'telegram',
    analyzedBy: 'gpt-4o',
    notes: 'Deadline: March 3, 2026 23:00 PST'
  },
  {
    id: 'mock-7',
    type: 'text',
    title: 'Design Philosophy: Deep-Sea Bioluminescence',
    summary: 'Core aesthetic principles for WALVIS UI inspired by deep-sea creatures.',
    tags: ['design', 'aesthetic', 'walvis'],
    content: 'Dark backgrounds (#0a0e1a) with glowing accents (#00d9ff, #7c3aed). Subtle animations mimicking bioluminescent pulses. Syne for headings (geometric, modern), DM Mono for code/data (technical precision). Minimal borders, soft glows, depth through layering.',
    createdAt: '2026-02-24T14:00:00Z',
    source: 'manual',
    analyzedBy: 'claude-3-opus'
  },
  {
    id: 'mock-8',
    type: 'note',
    title: 'Walrus Testnet Endpoints',
    summary: 'Quick reference for Walrus API endpoints and blob operations.',
    tags: ['walrus', 'api', 'reference'],
    content: 'Publisher: https://publisher.walrus-testnet.walrus.space\nAggregator: https://aggregator.walrus-testnet.walrus.space\n\nUpload: PUT /v1/blobs?epochs=5\nDownload: GET /v1/blobs/{blobId}\n\nResponse paths:\n- newlyCreated.blobObject.blobId\n- alreadyCertified.blobId',
    createdAt: '2026-02-23T11:45:00Z',
    source: 'manual',
    analyzedBy: 'gpt-4o'
  },
  // Image bookmarks
  {
    id: 'mock-9',
    type: 'image',
    url: 'https://picsum.photos/seed/wireframe9/1200/800',
    title: 'WALVIS Web UI Wireframe',
    summary: 'Initial wireframe sketch for masonry layout and detail modal.',
    tags: ['design', 'wireframe', 'ui'],
    content: 'https://picsum.photos/seed/wireframe9/1200/800',
    createdAt: '2026-02-22T16:30:00Z',
    source: 'telegram',
    analyzedBy: 'gpt-4o',
    notes: 'Approved by team'
  },
  {
    id: 'mock-10',
    type: 'image',
    url: 'https://picsum.photos/seed/logo10/600/600',
    title: 'WALVIS Logo Concept',
    summary: 'Logo design featuring a stylized walrus with bioluminescent accents.',
    tags: ['branding', 'logo', 'design'],
    content: 'https://picsum.photos/seed/logo10/600/600',
    createdAt: '2026-02-21T10:00:00Z',
    updatedAt: '2026-02-22T12:00:00Z',
    source: 'web',
    analyzedBy: 'claude-3-opus'
  }
];

const defaultSpace = {
  id: 'default',
  name: 'Default Space',
  description: 'Your main collection',
  items: mockItems,
  createdAt: '2026-02-20T08:00:00Z',
  updatedAt: '2026-03-05T09:00:00Z'
};

const filePath = join(spacesDir, 'default.json');
writeFileSync(filePath, JSON.stringify(defaultSpace, null, 2));

console.log(`✓ Seeded 10 mock items to ${filePath}`);
