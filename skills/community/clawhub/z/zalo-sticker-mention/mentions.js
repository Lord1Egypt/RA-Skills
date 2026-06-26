/**
 * Patch @openclaw/zalouser to support outgoing @mentions and stickers in group messages.
 * 
 * Run: node skills/zalo-sticker-mention/mentions.js
 */
const fs = require('fs');
const path = require('path');

const searchDirs = [
  '/root/project/.openclaw/extensions/zalouser/dist',
  '/root/project/.openclaw/npm/node_modules/@openclaw/zalouser/dist',
  '/home/node/project/.openclaw/extensions/zalouser/dist',
  '/home/node/project/.openclaw/npm/node_modules/@openclaw/zalouser/dist'
];

// Scan dynamic projects inside npm/projects/
const projectBases = ['/root/project/.openclaw', '/home/node/project/.openclaw'];
for (const base of projectBases) {
  const projectsDir = path.join(base, 'npm', 'projects');
  if (fs.existsSync(projectsDir)) {
    try {
      const dirs = fs.readdirSync(projectsDir);
      for (const projectDir of dirs) {
        const candidateDist = path.join(projectsDir, projectDir, 'node_modules', '@openclaw', 'zalouser', 'dist');
        if (fs.existsSync(candidateDist)) {
          searchDirs.push(candidateDist);
        }
      }
    } catch (_) {}
  }
}

const filesToPatch = [];
for (const dir of searchDirs) {
  if (fs.existsSync(dir)) {
    const files = fs.readdirSync(dir);
    const found = files.find(f => f.startsWith('zalo-js-') && f.endsWith('.js') && !f.endsWith('.bak'));
    if (found) {
      filesToPatch.push(path.join(dir, found));
    }
  }
}

if (filesToPatch.length === 0) {
  console.error('[patch-mentions] Error: Zalo JS files not found.');
  process.exit(1);
}

if (process.argv.includes('--restore')) {
  let restoredCount = 0;
  for (const FILE of filesToPatch) {
    const BACKUP = FILE + '.bak';
    if (fs.existsSync(BACKUP)) {
      console.log('[patch-mentions] Restoring ' + FILE + ' from backup...');
      fs.copyFileSync(BACKUP, FILE);
      restoredCount++;
    }
  }
  console.log('[patch-mentions] Restored ' + restoredCount + ' file(s) successfully.');
  process.exit(0);
}

for (const FILE of filesToPatch) {
  const BACKUP = FILE + '.bak';
  if (fs.existsSync(BACKUP)) {
    console.log('[patch-mentions] Restoring ' + FILE + ' from backup to ensure clean patch...');
    fs.copyFileSync(BACKUP, FILE);
  } else {
    console.log('[patch-mentions] Creating backup for ' + FILE);
    fs.copyFileSync(FILE, BACKUP);
  }

  let code = fs.readFileSync(FILE, 'utf8');

// ─────────────────────────────────────────────────────────────────────────────
// PATCH 1: Helper Functions, Cache & Sticker Delay
// ─────────────────────────────────────────────────────────────────────────────
const HELPER = `
// ── [PATCH] Auto-Mention & Sticker Resolution for outgoing group messages ──
const _mentionMemberCache = new Map();
const _lastGroupSender = new Map();
const _MENTION_CACHE_TTL = 5 * 60 * 1000;

function _saveActiveSenderToCache(threadId, name, uid) {
  if (!threadId || !name || !uid) return;
  let cached = _mentionMemberCache.get(threadId);
  if (!cached) {
    cached = { ts: Date.now(), membersMap: {} };
    _mentionMemberCache.set(threadId, cached);
  }
  cached.membersMap[name.toString().trim().toLowerCase()] = uid.toString();
}

async function _sendStickerAfterDelay(api, threadId, type, stickerConfig) {
  if (!stickerConfig) return;
  await new Promise(resolve => setTimeout(resolve, 500));
  try {
    let finalSticker = null;
    if (stickerConfig.keyword) {
      let kw = stickerConfig.keyword.trim().toLowerCase();
      const kwMap = {
        // ôm, tim, love
        "ôm": "love",
        "om": "love",
        "tim": "love",
        "love": "love",
        "ôm tim": "love",
        "om tim": "love",
        
        // cà khịa, lêu lêu, tát
        "cà khịa": "ca khia",
        "ca khia": "ca khia",
        "lêu lêu": "leu leu",
        "leu leu": "leu leu",
        "tát": "ca khia",
        "tat": "ca khia",
        
        // hehe, haha, há há
        "hehe": "haha",
        "haha": "haha",
        "há há": "haha",
        "ha ha": "haha",
        "cười": "haha",
        "cuoi": "haha",

        // khóc, sad
        "khóc": "sad",
        "khoc": "sad",
        "sad": "sad",
        "buồn": "sad",
        "buon": "sad",

        // hết hồn, giật mình
        "hết hồn": "giat minh",
        "het hon": "giat minh",
        "giật mình": "giat minh",
        "giat minh": "giat minh",

        // tức giận, angry
        "tức giận": "tuc gian",
        "tuc gian": "tuc gian",
        "tức": "tuc gian",
        "giận": "tuc gian",
        "angry": "tuc gian",

        // chán, nóng
        "chán": "chan",
        "chan": "chan",
        "nóng": "chan",
        "nong": "chan",

        // thank you, cảm ơn
        "thank you": "thank you",
        "thanks": "thank you",
        "cảm ơn": "thank you",
        "cảm on": "thank you",
        "cam on": "thank you",

        // xin lỗi
        "xin lỗi": "xin loi",
        "xin loi": "xin loi",

        // chào, hi
        "chào": "hi",
        "chao": "hi",
        "hi": "hi",
        "hello": "hi"
      };
      if (kwMap[kw]) {
        console.log('[patch-mentions] Mapping keyword "' + kw + '" to "' + kwMap[kw] + '"');
        kw = kwMap[kw];
      }
      console.log('[patch-mentions] Searching sticker for keyword:', kw);
      const stickerIds = await api.getStickers(kw);
      if (stickerIds && stickerIds.length > 0) {
        const details = await api.getStickersDetail(stickerIds.slice(0, 5));
        if (details && details.length > 0) {
          const selected = details[0];
          finalSticker = {
            id: selected.id,
            cateId: selected.cateId,
            type: selected.type
          };
          console.log('[patch-mentions] Resolved keyword to sticker:', JSON.stringify(finalSticker));
        }
      }
      if (!finalSticker) {
        console.warn('[patch-mentions] No sticker found for keyword:', kw);
        return;
      }
    } else {
      finalSticker = {
        id: stickerConfig.id,
        cateId: stickerConfig.cateId,
        type: stickerConfig.type
      };
    }

    await api.sendSticker(finalSticker, threadId, type);
    console.log('[patch-mentions] Sticker sent successfully:', finalSticker.id, 'with type:', finalSticker.type);
  } catch (err) {
    console.error("[patch-mentions] Failed to send sticker:", err);
  }
}

async function _resolveAutoMentions(api, threadId, text, isGroup) {
  if (!isGroup || !text) return null;
  
  let membersMap = null;
  let cached = _mentionMemberCache.get(threadId);
  if (cached && (Date.now() - cached.ts < _MENTION_CACHE_TTL)) {
    membersMap = cached.membersMap;
  } else {
    try {
      const info = (await api.getGroupInfo(threadId)).gridInfoMap;
      const gInfo = info ? info[threadId] : null;
      if (gInfo && Array.isArray(gInfo.currentMems)) {
        membersMap = {};
        for (const member of gInfo.currentMems) {
          if (!member) continue;
          const id = member.id || member.uid;
          const name = member.dName || member.zaloName;
          if (id && name) {
            membersMap[name.toString().trim().toLowerCase()] = id.toString();
          }
        }
        _mentionMemberCache.set(threadId, {
          ts: Date.now(),
          membersMap
        });
      }
    } catch (e) {
      console.error("[patch-mentions] Failed to fetch group members for mention resolution:", e);
      if (cached) membersMap = cached.membersMap;
    }
  }

  if (!membersMap) return null;

  // Add "all" and "cả nhóm" to membersMap pointing to "-1"
  membersMap["all"] = "-1";
  membersMap["cả nhóm"] = "-1";

  // Sort names by length descending
  const sortedNames = Object.keys(membersMap).sort((a, b) => b.length - a.length);

  const mentions = [];
  let maskedText = text;

  for (const name of sortedNames) {
    const escapedName = name.replace(/[-\\/\\\\^$*+?.()|[\\]{}]/g, '\\\\$&');
    const regex = new RegExp('@' + escapedName + '(?!\\\\p{L}|\\\\p{N})', 'gui');
    
    let match;
    while ((match = regex.exec(maskedText)) !== null) {
      const pos = match.index;
      const matchedString = match[0];
      const len = matchedString.length;
      const uid = membersMap[name];
      
      mentions.push({ pos, len, uid });
      maskedText = maskedText.substring(0, pos) + ' '.repeat(len) + maskedText.substring(pos + len);
      regex.lastIndex = 0;
    }
  }

  mentions.sort((a, b) => a.pos - b.pos);
  return mentions.length > 0 ? mentions : null;
}
`;

// Insert HELPER before toInboundMessage
const TO_INBOUND_ANCHOR = 'function toInboundMessage(message, ownUserId) {';
if (!code.includes(TO_INBOUND_ANCHOR)) {
  console.error('[patch-mentions] Error: TO_INBOUND_ANCHOR not found!');
  process.exit(1);
}
code = code.replace(TO_INBOUND_ANCHOR, () => HELPER + '\n' + TO_INBOUND_ANCHOR);

// ─────────────────────────────────────────────────────────────────────────────
// PATCH 2: Save active sender and track last sender of group
// ─────────────────────────────────────────────────────────────────────────────
const INBOUND_RESOLVE_ANCHOR = `\tconst senderId = toNumberId(data.uidFrom);
\tconst threadId = isGroup ? toNumberId(data.idTo) : toNumberId(data.uidFrom) || toNumberId(data.idTo);`;

const INBOUND_RESOLVE_PATCH = `\tconst senderId = toNumberId(data.uidFrom);
\tconst threadId = isGroup ? toNumberId(data.idTo) : toNumberId(data.uidFrom) || toNumberId(data.idTo);
\t// [PATCH] Save sender info and track last active sender (excluding bot itself)
\tif (isGroup && senderId && data.dName && threadId && senderId.toString() !== ownUserId?.toString()) {
\t\t_saveActiveSenderToCache(threadId, data.dName, senderId);
\t\t_lastGroupSender.set(threadId, {
\t\t\tuid: senderId.toString(),
\t\t\tname: data.dName.toString().trim(),
\t\t\ttimestamp: Date.now()
\t\t});
\t}`;

if (!code.includes(INBOUND_RESOLVE_ANCHOR)) {
  console.error('[patch-mentions] Error: INBOUND_RESOLVE_ANCHOR not found!');
  process.exit(1);
}
code = code.replace(INBOUND_RESOLVE_ANCHOR, () => INBOUND_RESOLVE_PATCH);

// ─────────────────────────────────────────────────────────────────────────────
// PATCH 3: Add sticker config parser to sendZaloTextMessage start
// ─────────────────────────────────────────────────────────────────────────────
const SEND_TEXT_FUNC_ANCHOR = 'async function sendZaloTextMessage(threadId, text, options = {}) {';
const SEND_TEXT_FUNC_PATCH = `async function sendZaloTextMessage(threadId, text, options = {}) {
	// [PATCH] Parse sticker config and strip from text
	let stickerConfig = null;
	const stickerRegex = /\\[Sticker:\\s*([^\\]]+)\\]/i;
	if (text && typeof text === 'string') {
		const match = text.match(stickerRegex);
		if (match) {
			const parts = match[1].split(':');
			if (parts.length >= 2) {
				stickerConfig = {
					id: parts[0].trim(),
					cateId: parts[1].trim(),
					type: parts[2] ? parseInt(parts[2].trim(), 10) : 30
				};
			} else {
				stickerConfig = {
					keyword: parts[0].trim()
				};
			}
			text = text.replace(stickerRegex, '').trim();
		}
	}`;

if (!code.includes(SEND_TEXT_FUNC_ANCHOR)) {
  console.error('[patch-mentions] Error: SEND_TEXT_FUNC_ANCHOR not found!');
  process.exit(1);
}
code = code.replace(SEND_TEXT_FUNC_ANCHOR, () => SEND_TEXT_FUNC_PATCH);

// ─────────────────────────────────────────────────────────────────────────────
// PATCH 4: Intercept sendZaloTextMessage and resolve auto-tagging
// ─────────────────────────────────────────────────────────────────────────────

// 4a. In mediaUrl path (const media to const textStyles):
const MEDIA_URL_RESOLVE_ANCHOR = `\t\t\t\tconst media = await loadOutboundMediaFromUrl(options.mediaUrl.trim(), {
\t\t\t\t\tmediaLocalRoots: options.mediaLocalRoots,
\t\t\t\t\tmediaReadFile: options.mediaReadFile
\t\t\t\t});
\t\t\t\tconst fileName = resolveMediaFileName({
\t\t\t\t\tmediaUrl: options.mediaUrl,
\t\t\t\t\tfileName: media.fileName,
\t\t\t\t\tcontentType: media.contentType,
\t\t\t\t\tkind: media.kind
\t\t\t\t});
\t\t\t\tconst payloadText = (text || options.caption || "").slice(0, 2e3);
\t\t\t\tconst textStyles = clampTextStyles(payloadText, options.textStyles);`;

const MEDIA_URL_RESOLVE_PATCH = `\t\t\t\tconst media = await loadOutboundMediaFromUrl(options.mediaUrl.trim(), {
\t\t\t\t\tmediaLocalRoots: options.mediaLocalRoots,
\t\t\t\t\tmediaReadFile: options.mediaReadFile
\t\t\t\t});
\t\t\t\tconst fileName = resolveMediaFileName({
\t\t\t\t\tmediaUrl: options.mediaUrl,
\t\t\t\t\tfileName: media.fileName,
\t\t\t\t\tcontentType: media.contentType,
\t\t\t\t\tkind: media.kind
\t\t\t\t});
\t\t\t\tlet payloadText = (text || options.caption || "").slice(0, 2e3);
\t\t\t\tconst textStyles = clampTextStyles(payloadText, options.textStyles);
\t\t\t\tlet mentions = null;
\t\t\t\tif (options.isGroup) {
\t\t\t\t\tmentions = await _resolveAutoMentions(api, trimmedThreadId, payloadText, options.isGroup);
\t\t\t\t\tconst lastSender = _lastGroupSender.get(trimmedThreadId);
\t\t\t\t\tif (lastSender && (Date.now() - lastSender.timestamp < 5 * 60 * 1000)) {
\t\t\t\t\t\tconst alreadyTagged = mentions && mentions.some(m => m.uid === lastSender.uid);
\t\t\t\t\t\tif (!alreadyTagged) {
\t\t\t\t\t\t\tconst tagText = \`@\${lastSender.name} \`;
\t\t\t\t\t\t\tpayloadText = tagText + payloadText;
\t\t\t\t\t\t\tconst newMention = {
\t\t\t\t\t\t\t\tpos: 0,
\t\t\t\t\t\t\t\tlen: tagText.length - 1,
\t\t\t\t\t\t\t\tuid: lastSender.uid
\t\t\t\t\t\t\t};
\t\t\t\t\t\t\tif (mentions) {
\t\t\t\t\t\t\t\tmentions = mentions.map(m => ({ ...m, pos: m.pos + tagText.length }));
\t\t\t\t\t\t\t\tmentions.unshift(newMention);
\t\t\t\t\t\t\t} else {
\t\t\t\t\t\t\t\tmentions = [newMention];
\t\t\t\t\t\t\t}
\t\t\t\t\t\t\tif (textStyles) {
\t\t\t\t\t\t\t\tfor (const style of textStyles) {
\t\t\t\t\t\t\t\t\tif (style && typeof style.start === 'number') {
\t\t\t\t\t\t\t\t\t\tstyle.start += tagText.length;
\t\t\t\t\t\t\t\t\t}
\t\t\t\t\t\t\t\t}
\t\t\t\t\t\t\t}
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t}`;

if (!code.includes(MEDIA_URL_RESOLVE_ANCHOR)) {
  console.error('[patch-mentions] Error: MEDIA_URL_RESOLVE_ANCHOR not found!');
  process.exit(1);
}
code = code.replace(MEDIA_URL_RESOLVE_ANCHOR, () => MEDIA_URL_RESOLVE_PATCH);

// 4b. Inject mentions to api.sendMessage with attachments & send sticker:
const MEDIA_SEND_MESSAGE_ANCHOR = `\t\t\t\tconst messageId = extractSendMessageId(await api.sendMessage({
\t\t\t\t\tmsg: payloadText,
\t\t\t\t\t...textStyles ? { styles: textStyles } : {},
\t\t\t\t\tattachments: [{
\t\t\t\t\t\tdata: media.buffer,
\t\t\t\t\t\tfilename: fileName.includes(".") ? fileName : \`\${fileName}.bin\`,
\t\t\t\t\t\tmetadata: { totalSize: media.buffer.length }
\t\t\t\t\t}]
\t\t\t\t}, trimmedThreadId, type));
\t\t\t\treturn {
\t\t\t\t\tok: true,
\t\t\t\t\tmessageId,
\t\t\t\t\treceipt: createZalouserSendReceipt({
\t\t\t\t\t\tmessageId,
\t\t\t\t\t\tthreadId: trimmedThreadId,
\t\t\t\t\t\tkind: "media"
\t\t\t\t\t})
\t\t\t\t};`;

const MEDIA_SEND_MESSAGE_PATCH = `\t\t\t\tconst messageId = extractSendMessageId(await api.sendMessage({
\t\t\t\t\tmsg: payloadText,
\t\t\t\t\t...textStyles ? { styles: textStyles } : {},
\t\t\t\t\t...(mentions ? { mentions } : {}),
\t\t\t\t\tattachments: [{
\t\t\t\t\t\tdata: media.buffer,
\t\t\t\t\t\tfilename: fileName.includes(".") ? fileName : \`\${fileName}.bin\`,
\t\t\t\t\t\tmetadata: { totalSize: media.buffer.length }
\t\t\t\t\t}]
\t\t\t\t}, trimmedThreadId, type));
\t\t\t\tif (stickerConfig) {
\t\t\t\t\tawait _sendStickerAfterDelay(api, trimmedThreadId, type, stickerConfig);
\t\t\t\t}
\t\t\t\treturn {
\t\t\t\t\tok: true,
\t\t\t\t\tmessageId,
\t\t\t\t\treceipt: createZalouserSendReceipt({
\t\t\t\t\t\tmessageId,
\t\t\t\t\t\tthreadId: trimmedThreadId,
\t\t\t\t\t\tkind: "media"
\t\t\t\t\t})
\t\t\t\t};`;

if (!code.includes(MEDIA_SEND_MESSAGE_ANCHOR)) {
  console.error('[patch-mentions] Error: MEDIA_SEND_MESSAGE_ANCHOR not found!');
  process.exit(1);
}
code = code.replace(MEDIA_SEND_MESSAGE_ANCHOR, () => MEDIA_SEND_MESSAGE_PATCH);

// 4c. In plain-text path (auto-tag & send sticker):
const PLAIN_TEXT_SEND_ANCHOR = `\t\t\tconst payloadText = text.slice(0, 2e3);
\t\t\tconst textStyles = clampTextStyles(payloadText, options.textStyles);
\t\t\tconst messageId = extractSendMessageId(await api.sendMessage(textStyles ? {
\t\t\t\tmsg: payloadText,
\t\t\t\tstyles: textStyles
\t\t\t} : payloadText, trimmedThreadId, type));
\t\t\treturn {
\t\t\t\tok: true,
\t\t\t\tmessageId,
\t\t\t\treceipt: createZalouserSendReceipt({
\t\t\t\t\tmessageId,
\t\t\t\t\tthreadId: trimmedThreadId,
\t\t\t\t\tkind: "text"
\t\t\t\t})
\t\t\t};`;

const PLAIN_TEXT_SEND_PATCH = `\t\t\tlet payloadText = text.slice(0, 2e3);
\t\t\tconst textStyles = clampTextStyles(payloadText, options.textStyles);
\t\t\tlet mentions = null;
\t\t\tif (options.isGroup) {
\t\t\t\tmentions = await _resolveAutoMentions(api, trimmedThreadId, payloadText, options.isGroup);
\t\t\t\tconst lastSender = _lastGroupSender.get(trimmedThreadId);
\t\t\t\tif (lastSender && (Date.now() - lastSender.timestamp < 5 * 60 * 1000)) {
\t\t\t\t\tconst alreadyTagged = mentions && mentions.some(m => m.uid === lastSender.uid);
\t\t\t\t\tif (!alreadyTagged) {
\t\t\t\t\t\tconst tagText = \`@\${lastSender.name} \`;
\t\t\t\t\t\tpayloadText = tagText + payloadText;
\t\t\t\t\t\tconst newMention = {
\t\t\t\t\t\t\tpos: 0,
\t\t\t\t\t\t\tlen: tagText.length - 1,
\t\t\t\t\t\t\tuid: lastSender.uid
\t\t\t\t\t\t};
\t\t\t\t\t\tif (mentions) {
\t\t\t\t\t\t\tmentions = mentions.map(m => ({ ...m, pos: m.pos + tagText.length }));
\t\t\t\t\t\t\tmentions.unshift(newMention);
\t\t\t\t\t\t} else {
\t\t\t\t\t\t\tmentions = [newMention];
\t\t\t\t\t\t}
\t\t\t\t\t\tif (textStyles) {
\t\t\t\t\t\t\tfor (const style of textStyles) {
\t\t\t\t\t\t\t\tif (style && typeof style.start === 'number') {
\t\t\t\t\t\t\t\t\tstyle.start += tagText.length;
\t\t\t\t\t\t\t\t}
\t\t\t\t\t\t\t}
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t}
\t\t\t}
\t\t\tconst messageObj = {
\t\t\t\tmsg: payloadText,
\t\t\t\t...(textStyles ? { styles: textStyles } : {}),
\t\t\t\t...(mentions ? { mentions } : {})
\t\t\t};
\t\t\tconst messageId = extractSendMessageId(await api.sendMessage(messageObj, trimmedThreadId, type));
\t\t\tif (stickerConfig) {
\t\t\t\tawait _sendStickerAfterDelay(api, trimmedThreadId, type, stickerConfig);
\t\t\t}
\t\t\treturn {
\t\t\t\tok: true,
\t\t\t\tmessageId,
\t\t\t\treceipt: createZalouserSendReceipt({
\t\t\t\t\tmessageId,
\t\t\t\t\tthreadId: trimmedThreadId,
\t\t\t\t\tkind: "text"
\t\t\t\t})
\t\t\t};`;

if (!code.includes(PLAIN_TEXT_SEND_ANCHOR)) {
  console.error('[patch-mentions] Error: PLAIN_TEXT_SEND_ANCHOR not found!');
  process.exit(1);
}
code = code.replace(PLAIN_TEXT_SEND_ANCHOR, () => PLAIN_TEXT_SEND_PATCH);

// ─────────────────────────────────────────────────────────────────────────────
// PATCH 5: Intercept sendZaloTextMessage with sticker search command
// ─────────────────────────────────────────────────────────────────────────────
const WITH_ZALO_API_ANCHOR = `\treturn await withZaloApi(profile, async (api) => {
\t\tconst type = options.isGroup ? ThreadType.Group : ThreadType.User;`;

const WITH_ZALO_API_PATCH = `\treturn await withZaloApi(profile, async (api) => {
\t\t// [PATCH] Temporary sticker search command interceptor
\t\tif (text && text.startsWith('/search-sticker ')) {
\t\t\tconst keyword = text.replace('/search-sticker ', '').trim();
\t\t\ttry {
\t\t\t\tconst stickerIds = await api.getStickers(keyword);
\t\t\t\tif (!stickerIds || stickerIds.length === 0) {
\t\t\t\t\ttext = "Không tìm thấy sticker nào cho từ khóa này.";
\t\t\t\t} else {
\t\t\t\t\tconst details = await api.getStickersDetail(stickerIds.slice(0, 20));
\t\t\t\t\tconst list = details.map(d => \`- \${d.text || 'sticker'}: [Sticker: \${d.id}:\${d.cateId}] (id: \${d.id}, cateId: \${d.cateId})\`).join('\\n');
\t\t\t\t\ttext = "Kết quả tìm kiếm sticker cho '" + keyword + "':\\n" + list;
\t\t\t\t}
\t\t\t} catch (e) {
\t\t\t\ttext = "Lỗi khi tìm sticker: " + e.message;
\t\t\t}
\t\t}
\t\tconst type = options.isGroup ? ThreadType.Group : ThreadType.User;`;

if (!code.includes(WITH_ZALO_API_ANCHOR)) {
  console.error('[patch-mentions] Error: WITH_ZALO_API_ANCHOR not found!');
  process.exit(1);
}
code = code.replace(WITH_ZALO_API_ANCHOR, () => WITH_ZALO_API_PATCH);

  // Write modified file
  fs.writeFileSync(FILE, code, 'utf8');
  console.log('[patch-mentions] File successfully patched: ' + FILE);
}
