/**
 * Generate a unique ID with a given prefix.
 * Format: {prefix}_{timestamp}_{6-char-random-hex}
 * Example: msg_1711360000000_a1b2c3
 *
 * @param {string} prefix
 * @returns {string}
 */
export function createId(prefix) {
  const ts = Date.now();
  const rand = Math.floor(Math.random() * 0xffffff)
    .toString(16)
    .padStart(6, '0');
  return `${prefix}_${ts}_${rand}`;
}

/**
 * Create a routable message object.
 *
 * @param {{from: string, to: string, content: string, topic?: string|null, contentType?: string}} opts
 * @returns {object}
 */
export function createMessage({ from, to, content, topic = null, contentType = 'text' }) {
  return {
    id: createId('msg'),
    type: 'message',
    from,
    to,
    content,
    contentType,
    topic,
    ts: Date.now(),
  };
}

/**
 * Create a system event object (session_joined, session_left, etc.).
 *
 * @param {{event: string, session: string, data?: any}} opts
 * @returns {object}
 */
export function createSystemEvent({ event, session, data = null }) {
  return {
    id: createId('sys'),
    type: 'system',
    event,
    session,
    data,
    ts: Date.now(),
  };
}

/**
 * Validate an incoming message.
 * Checks required fields exist and have the correct types.
 *
 * @param {any} msg
 * @returns {{valid: boolean, error?: string}}
 */
export function validateMessage(msg) {
  if (msg === null || typeof msg !== 'object') {
    return { valid: false, error: 'message must be a JSON object' };
  }

  const { type } = msg;

  if (typeof type !== 'string' || type.length === 0) {
    return { valid: false, error: 'missing or invalid field: type' };
  }

  // Validate routable messages
  if (type === 'message') {
    if (typeof msg.from !== 'string' || msg.from.length === 0) {
      return { valid: false, error: 'missing or invalid field: from' };
    }
    if (typeof msg.to !== 'string' || msg.to.length === 0) {
      return { valid: false, error: 'missing or invalid field: to' };
    }
    if (msg.content === undefined || msg.content === null) {
      return { valid: false, error: 'missing field: content' };
    }
    return { valid: true };
  }

  // Validate control messages
  if (type === 'register') {
    if (typeof msg.name !== 'string' || msg.name.length === 0) {
      return { valid: false, error: 'missing or invalid field: name' };
    }
    return { valid: true };
  }

  if (type === 'subscribe' || type === 'unsubscribe') {
    if (typeof msg.topic !== 'string' || msg.topic.length === 0) {
      return { valid: false, error: 'missing or invalid field: topic' };
    }
    return { valid: true };
  }

  if (type === 'ping') {
    return { valid: true };
  }

  // Unknown types are allowed through (hub can decide what to do)
  return { valid: true };
}
