const crypto = require('crypto');

function toGmtDate(date = new Date()) {
  return date.toUTCString();
}

function sortUriParams(uriParams) {
  if (!uriParams) return '';

  return uriParams
    .split('&')
    .filter(Boolean)
    .sort()
    .join('&');
}

function buildReferenceCanonicalMessage({ method, path, uriParams = '', appId, dateGmt }) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;

  return (
    [
    method.toUpperCase(),
    normalizedPath,
    sortUriParams(uriParams),
    appId,
    dateGmt,
    `HMAC-APPID:${appId}`,
    ].join('\n') + '\n'
  );
}

function buildSignature({
  method,
  path,
  uriParams = '',
  appId,
  dateGmt,
  secret,
  canonicalMessageBuilder = buildReferenceCanonicalMessage,
}) {
  const message = canonicalMessageBuilder({
    method,
    path,
    uriParams,
    appId,
    dateGmt,
  });

  return crypto.createHmac('sha256', secret).update(message, 'utf8').digest('base64');
}

function buildHeaders({
  appId,
  secret,
  method,
  path,
  uriParams = '',
  canonicalMessageBuilder,
  signedHeaders = 'HMAC-APPID',
  algorithm = 'hmac-sha256',
}) {
  const dateGmt = toGmtDate();
  const signature = buildSignature({
    method,
    path,
    uriParams,
    appId,
    dateGmt,
    secret,
    canonicalMessageBuilder,
  });

  return {
    'HMAC-APPID': appId,
    'HMAC-DATE': dateGmt,
    'HMAC-SIGNATURE': signature,
    'HMAC-ALGORITHM': algorithm,
    'HMAC-SIGNED-HEADERS': signedHeaders,
  };
}

async function createOutboundNotification({
  fetchImpl = fetch,
  baseUrl = 'https://vox.teddymobile.cn',
  appId,
  secret,
  botid,
  callee,
  requestId,
  notificationText,
  notificationTimes,
  canonicalMessageBuilder,
  signedHeaders,
  algorithm,
}) {
  const path = '/vox/v1/outbound';
  const headers = buildHeaders({
    appId,
    secret,
    method: 'POST',
    path,
    canonicalMessageBuilder,
    signedHeaders,
    algorithm,
  });

  const requestBody = buildNotificationRequestBody({
    appId,
    botid,
    callee,
    requestId,
    notificationText,
    notificationTimes,
  });

  const response = await fetchImpl(`${baseUrl}${path}`, {
    method: 'POST',
    headers: {
      ...headers,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const bodyText = await response.text();
    throw new Error(`Vox outbound request failed: ${response.status} ${bodyText}`);
  }

  return response.json();
}

function buildNotificationRequestBody({
  appId,
  botid,
  callee,
  requestId,
  notificationText,
  notificationTimes,
}) {
  const extra =
    notificationText == null
      ? undefined
      : JSON.stringify({
          notification: {
            text: notificationText,
            ...(notificationTimes == null ? {} : { times: notificationTimes }),
          },
        });

  return {
    ...(appId == null ? {} : { appId }),
    ...(botid == null ? {} : { botid }),
    callee,
    requestId,
    ...(extra == null ? {} : { extra }),
  };
}

async function createTrialOutboundNotification({
  fetchImpl = fetch,
  baseUrl = 'https://vox.teddymobile.cn',
  callee,
  requestId,
  notificationText,
  notificationTimes,
}) {
  const path = '/vox/v2/outbound';
  const requestBody = buildNotificationRequestBody({
    callee,
    requestId,
    notificationText,
    notificationTimes,
  });

  const response = await fetchImpl(`${baseUrl}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const bodyText = await response.text();
    throw new Error(`Vox trial outbound request failed: ${response.status} ${bodyText}`);
  }

  return response.json();
}

module.exports = {
  toGmtDate,
  sortUriParams,
  buildReferenceCanonicalMessage,
  buildSignature,
  buildHeaders,
  buildNotificationRequestBody,
  createOutboundNotification,
  createTrialOutboundNotification,
};
