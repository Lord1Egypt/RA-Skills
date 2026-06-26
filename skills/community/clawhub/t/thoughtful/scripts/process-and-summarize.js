#!/usr/bin/env node
/**
 * Thoughtful - Summary Processor + lightweight CRM
 *
 * Analyzes messages, tracks tasks/relationships, generates a human summary,
 * and maintains a per-person CRM so Neil can see who he owes replies to,
 * who owes him replies, and which conversations have gone quiet.
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = process.argv[2] || path.join(process.env.HOME, 'clawd', 'thoughtful-data');

function loadJSON(filename, fallback = null) {
  const filepath = path.join(DATA_DIR, filename);
  if (!fs.existsSync(filepath)) return fallback;
  return JSON.parse(fs.readFileSync(filepath, 'utf8'));
}

function saveJSON(filename, data) {
  const filepath = path.join(DATA_DIR, filename);
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
}

function parseTs(ts) {
  if (!ts) return null;
  const d = new Date(ts);
  return Number.isNaN(d.getTime()) ? null : d;
}

function hoursSince(ts, now = new Date()) {
  const d = parseTs(ts);
  if (!d) return null;
  return Math.round(((now - d) / 36e5) * 10) / 10;
}

function daysSince(ts, now = new Date()) {
  const h = hoursSince(ts, now);
  return h == null ? null : Math.round((h / 24) * 10) / 10;
}

function clip(text, max = 160) {
  const s = (text || '').replace(/\s+/g, ' ').trim();
  if (!s) return '';
  return s.length <= max ? s : `${s.slice(0, max - 1)}…`;
}

function isStatusChat(chat) {
  return chat?.JID === 'status@broadcast';
}

function isGroupChat(chat) {
  return chat?.Kind === 'group' || chat?.JID?.endsWith('@g.us');
}

function isPersonChat(chat) {
  if (!chat || isStatusChat(chat) || isGroupChat(chat)) return false;
  return true;
}

function isLikelyAutomatedContact(name = '', preview = '') {
  const hay = `${name} ${preview}`.toLowerCase();
  const keywords = [
    'bank', 'credit card', 'amount due', 'payment reminder', 'bill has been generated',
    'daily affirmation', 'monthly interest', 'renewal payment', 'otp', 'credited to',
    'text blast', 'furlenco', 'savesage', 'wint wealth', 'aadhar'
  ];
  return keywords.some(k => hay.includes(k));
}

function normalizeConfig(config) {
  const safe = config || {};
  safe.chats = safe.chats || {};
  safe.chats.whitelistGroups = safe.chats.whitelistGroups || [];
  safe.summary = safe.summary || {};
  safe.tracking = safe.tracking || {};
  safe.crm = safe.crm || {};
  safe.crm.replyOwedAfterHours = safe.crm.replyOwedAfterHours ?? 24;
  safe.crm.followUpAfterDays = safe.crm.followUpAfterDays ?? 7;
  safe.crm.quietAfterDays = safe.crm.quietAfterDays ?? 14;
  safe.crm.includeBusinessBroadcasts = safe.crm.includeBusinessBroadcasts ?? false;
  return safe;
}

function extractMessagesData(messagesData) {
  if (!messagesData) return [];
  if (Array.isArray(messagesData?.data?.messages)) return messagesData.data.messages;
  return [];
}

function extractChatsData(chatsData) {
  if (!chatsData) return [];
  if (Array.isArray(chatsData?.data)) return chatsData.data;
  return [];
}

function filterMessages(messages, chats, config) {
  const whitelistJIDs = new Set((config.chats.whitelistGroups || []).map(g => g.jid));
  const chatsByJid = new Map(chats.map(chat => [chat.JID, chat]));

  return messages.filter(msg => {
    const chat = chatsByJid.get(msg.ChatJID);
    if (!chat) return false;
    if (isStatusChat(chat)) return false;
    if (isPersonChat(chat)) return true;
    if (isGroupChat(chat) && whitelistJIDs.has(chat.JID)) return true;
    return false;
  });
}

function buildCRM(messages, chats, config, previousPeople = {}) {
  const now = new Date();
  const chatsByJid = new Map(chats.map(chat => [chat.JID, chat]));
  const grouped = new Map();

  for (const msg of messages) {
    const chat = chatsByJid.get(msg.ChatJID);
    if (!chat || !isPersonChat(chat)) continue;
    if (!grouped.has(msg.ChatJID)) grouped.set(msg.ChatJID, []);
    grouped.get(msg.ChatJID).push(msg);
  }

  const contacts = [];
  const previousContacts = previousPeople.contacts || {};

  for (const [chatJID, chatMessages] of grouped.entries()) {
    const chat = chatsByJid.get(chatJID);
    const sorted = [...chatMessages].sort((a, b) => new Date(a.Timestamp) - new Date(b.Timestamp));
    const inbound = sorted.filter(m => !m.FromMe);
    const outbound = sorted.filter(m => m.FromMe);
    const lastMessage = sorted[sorted.length - 1] || null;
    const lastInbound = inbound[inbound.length - 1] || null;
    const lastOutbound = outbound[outbound.length - 1] || null;
    const previous = previousContacts[chatJID] || {};
    const previewText = clip(lastMessage?.Text || lastMessage?.DisplayText || '[media]');
    const isSelfChat = (chat?.Name || '').trim().toLowerCase() === (config.user?.name || '').trim().toLowerCase();
    const isAutomated = isLikelyAutomatedContact(chat?.Name || previous.name || '', previewText);

    let relationshipState = 'idle';
    if (lastMessage && !lastMessage.FromMe) relationshipState = 'owes_reply';
    else if (lastOutbound) relationshipState = 'waiting_for_reply';

    const lastInboundAt = lastInbound?.Timestamp || null;
    const lastOutboundAt = lastOutbound?.Timestamp || null;
    const replyDelayHours = relationshipState === 'owes_reply' ? hoursSince(lastInboundAt, now) : null;
    const followUpDelayDays = relationshipState === 'waiting_for_reply' ? daysSince(lastOutboundAt, now) : null;

    const contact = {
      jid: chatJID,
      name: chat?.Name || previous.name || chatJID,
      type: 'person',
      sourceKind: chat?.Kind || 'unknown',
      totalMessagesSeen: sorted.length,
      inboundCount: inbound.length,
      outboundCount: outbound.length,
      firstSeenAt: previous.firstSeenAt || sorted[0]?.Timestamp || null,
      lastSeenAt: lastMessage?.Timestamp || previous.lastSeenAt || null,
      lastInboundAt,
      lastOutboundAt,
      lastMessageFromMe: !!lastMessage?.FromMe,
      lastMessagePreview: previewText,
      lastInboundPreview: clip(lastInbound?.Text || lastInbound?.DisplayText || '[media]'),
      lastOutboundPreview: clip(lastOutbound?.Text || lastOutbound?.DisplayText || '[media]'),
      relationshipState,
      replyDelayHours,
      followUpDelayDays,
      owesReply: relationshipState === 'owes_reply',
      followUpCandidate: relationshipState === 'waiting_for_reply' && (followUpDelayDays ?? 0) >= config.crm.followUpAfterDays,
      quietConversation: (daysSince(lastMessage?.Timestamp, now) ?? 0) >= config.crm.quietAfterDays,
      entityType: isSelfChat ? 'self' : (isAutomated ? 'automated' : 'person'),
      includeInOutreach: !isSelfChat && !isAutomated,
      priority: previous.priority || null,
      notes: previous.notes || '',
      tags: previous.tags || [],
      lastUpdatedAt: now.toISOString()
    };

    contacts.push(contact);
  }

  contacts.sort((a, b) => new Date(b.lastSeenAt || 0) - new Date(a.lastSeenAt || 0));

  const queues = {
    owesReply: contacts
      .filter(c => c.includeInOutreach && c.owesReply)
      .sort((a, b) => (b.replyDelayHours || 0) - (a.replyDelayHours || 0)),
    waitingForReply: contacts
      .filter(c => c.includeInOutreach && c.relationshipState === 'waiting_for_reply')
      .sort((a, b) => (b.followUpDelayDays || 0) - (a.followUpDelayDays || 0)),
    followUpCandidates: contacts
      .filter(c => c.includeInOutreach && c.followUpCandidate)
      .sort((a, b) => (b.followUpDelayDays || 0) - (a.followUpDelayDays || 0)),
    quietConversations: contacts
      .filter(c => c.includeInOutreach && c.quietConversation)
      .sort((a, b) => new Date(b.lastSeenAt || 0) - new Date(a.lastSeenAt || 0))
  };

  const crm = {
    version: '1.0',
    generatedAt: now.toISOString(),
    totals: {
      contacts: contacts.length,
      owesReply: queues.owesReply.length,
      waitingForReply: queues.waitingForReply.length,
      followUpCandidates: queues.followUpCandidates.length,
      quietConversations: queues.quietConversations.length
    },
    queues: {
      owesReply: queues.owesReply.slice(0, 25),
      waitingForReply: queues.waitingForReply.slice(0, 25),
      followUpCandidates: queues.followUpCandidates.slice(0, 25),
      quietConversations: queues.quietConversations.slice(0, 25)
    },
    contacts
  };

  const peopleJson = {
    version: '1.0',
    updatedAt: now.toISOString(),
    contacts: Object.fromEntries(
      contacts.map(contact => [contact.jid, {
        name: contact.name,
        relationshipState: contact.relationshipState,
        lastSeenAt: contact.lastSeenAt,
        lastInboundAt: contact.lastInboundAt,
        lastOutboundAt: contact.lastOutboundAt,
        owesReply: contact.owesReply,
        followUpCandidate: contact.followUpCandidate,
        quietConversation: contact.quietConversation,
        replyDelayHours: contact.replyDelayHours,
        followUpDelayDays: contact.followUpDelayDays,
        lastMessagePreview: contact.lastMessagePreview,
        tags: contact.tags,
        notes: contact.notes,
        priority: contact.priority,
        entityType: contact.entityType,
        includeInOutreach: contact.includeInOutreach
      }])
    ),
    notes: 'Per-person CRM for DM/business chats. Groups are tracked separately in summaries.'
  };

  return { crm, peopleJson };
}

function buildSummaryInput(messages, chats, tasks, people, config, crm) {
  const messagesByChat = {};
  const chatsByJid = new Map(chats.map(chat => [chat.JID, chat]));

  messages.forEach(msg => {
    if (!messagesByChat[msg.ChatJID]) messagesByChat[msg.ChatJID] = [];
    messagesByChat[msg.ChatJID].push(msg);
  });

  const dms = [];
  const groups = [];

  Object.entries(messagesByChat).forEach(([chatJID, chatMessages]) => {
    const chat = chatsByJid.get(chatJID);
    if (!chat) return;

    const chatSummary = {
      jid: chatJID,
      name: chat.Name || chatJID,
      kind: isPersonChat(chat) ? 'person' : chat.Kind,
      messageCount: chatMessages.length,
      messages: chatMessages.map(m => ({
        from: isPersonChat(chat)
          ? (m.FromMe ? config.user?.name || 'You' : m.ChatName || 'Unknown')
          : m.ChatName || 'Unknown',
        text: m.Text || m.DisplayText || '[media]',
        timestamp: m.Timestamp,
        fromMe: m.FromMe
      })),
      lastMessage: chat.LastMessageTS
    };

    if (isPersonChat(chat)) dms.push(chatSummary);
    else groups.push(chatSummary);
  });

  return {
    timeRange: config.summary.defaultTimeRange || '24 hours',
    dms,
    groups,
    pendingTasks: (tasks.tasks || []).filter(t => t.status === 'pending'),
    waitingOn: tasks.waitingOn || [],
    scheduled: tasks.scheduled || [],
    commitments: tasks.commitments || [],
    totalMessages: messages.length,
    crm: {
      totals: crm.totals,
      owesReply: crm.queues.owesReply.slice(0, 10),
      followUpCandidates: crm.queues.followUpCandidates.slice(0, 10),
      quietConversations: crm.queues.quietConversations.slice(0, 10)
    },
    config: {
      includeRelationshipInsights: config.summary.includeRelationshipInsights,
      communicationCoachMode: config.summary.communicationCoachMode,
      tone: config.summary.tone
    }
  };
}

function buildCommunicationCoachPrompt(input) {
  return `You are a thoughtful communication coach with a practical, emotionally intelligent lens.

Your role is to help Neil improve how he communicates in his relationships with peers, colleagues, and friends.

## Context

You have access to Neil's WhatsApp messages from the last ${input.timeRange}. Here's the data:

### Direct Conversations (${input.dms.length}):
${JSON.stringify(input.dms, null, 2)}

### Groups (${input.groups.length}):
${JSON.stringify(input.groups, null, 2)}

### Pending Tasks (${input.pendingTasks.length} items):
${JSON.stringify(input.pendingTasks, null, 2)}

### Waiting On (${input.waitingOn.length} items):
${JSON.stringify(input.waitingOn, null, 2)}

### CRM Signals:
${JSON.stringify(input.crm, null, 2)}

## Your Task

Create a warm, conversational summary that helps Neil:

1. Catch what is slipping
2. Notice tone shifts
3. Find good moments to check in
4. See who he owes a reply to
5. See who he may want to follow up with because they never replied or the thread went quiet
6. Get specific, natural conversation starters

## Format

**Morning, Neil! ☀️**

Here's your WhatsApp catch-up:

**🆕 WHAT'S NEW (last ${input.timeRange}):**

[For each meaningful direct conversation, write 2-3 sentences about what happened and if action is needed.]

[For groups, briefly summarize only if relevant.]

**📮 PEOPLE YOU OWE A REPLY TO:**

[Prioritize by urgency and how long it has been sitting.]

**🪃 PEOPLE YOU MAY WANT TO FOLLOW UP WITH:**

[People where Neil sent something and the thread died, especially when a follow-up would be useful.]

**⏰ STILL PENDING:**

[List pending tasks from earlier.]

**💡 COMMUNICATION INSIGHTS:**

[Analyze relationship dynamics.]

**Quiet conversations worth reviving:**
[Use the CRM quiet/follow-up signals, but only mention the genuinely useful ones.]

**📝 SUGGESTED ACTIONS:**

[For the 2-4 most important items, provide specific message drafts Neil can send. Keep them natural, warm, and direct.]

---

Did you complete: "[most urgent pending task or reply]"?

## Tone

${input.config.tone}

- No fluff, not robotic
- Like a smart friend who remembers social context
- Be concrete
- Flag when something is low-stakes so Neil does not feel fake urgency

Generate the summary now:`;
}

async function main() {
  console.log('📊 Loading tracking data...');

  const config = normalizeConfig(loadJSON('config.json', {}));
  const state = loadJSON('state.json', {
    version: '1.0',
    lastProcessed: null,
    lastSummaryGenerated: null,
    totalMessagesProcessed: 0,
    chatsTracked: 0,
    firstRun: true
  });
  const tasks = loadJSON('tasks.json', { version: '1.0', tasks: [], waitingOn: [], scheduled: [], commitments: [], decisions: [] });
  const people = loadJSON('people.json', { version: '1.0', contacts: {} });

  console.log('📥 Loading messages...');
  const messagesData = loadJSON('context/recent-messages.json');
  const chatsData = loadJSON('context/recent-chats.json');

  const messages = extractMessagesData(messagesData);
  const chats = extractChatsData(chatsData);

  if (!messages.length || !chats.length) {
    console.error('Failed to load usable message/chat data');
    process.exit(1);
  }

  console.log(`Loaded ${messages.length} messages from ${chats.length} chats`);

  const filteredMessages = filterMessages(messages, chats, config);
  console.log(`Filtered to ${filteredMessages.length} relevant messages`);

  const { crm, peopleJson } = buildCRM(messages, chats, config, people);
  saveJSON('crm.json', crm);
  saveJSON('people.json', peopleJson);
  console.log(`📇 Saved CRM with ${crm.totals.contacts} contacts`);

  const summaryInput = buildSummaryInput(filteredMessages, chats, tasks, peopleJson, config, crm);
  const prompt = buildCommunicationCoachPrompt(summaryInput);

  fs.writeFileSync(path.join(DATA_DIR, 'context/last-prompt.txt'), prompt);
  console.log(`💾 Saved prompt to ${DATA_DIR}/context/last-prompt.txt`);

  state.lastProcessed = new Date().toISOString();
  state.totalMessagesProcessed += filteredMessages.length;
  state.chatsTracked = chats.length;
  state.firstRun = false;
  saveJSON('state.json', state);

  console.log('\n📝 Summary input ready!');
  console.log('Next step: Use OpenClaw LLM to generate summary from prompt');
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
