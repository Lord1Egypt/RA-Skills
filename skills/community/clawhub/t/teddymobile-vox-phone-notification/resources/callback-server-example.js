const express = require('express');

const app = express();
app.use(express.json());

function writeSse(res, payload) {
  res.write(`data: ${JSON.stringify(payload)}\n\n`);
}

async function* runNotificationAgentTurn({ body, notificationContext }) {
  const userMessage = body.message || '';

  if (!userMessage) {
    yield `您好，我是${notificationContext.agentName || '通知助手'}。`;
    yield notificationContext.notificationText || '这里有一条需要您关注的电话通知。';
    return;
  }

  yield notificationContext.notificationText || '这里有一条需要您关注的电话通知。';
}

app.post('/vox/callback', async (req, res) => {
  const body = req.body || {};
  const requestId = body.requestid;
  const notificationContext = {
    agentName: '账单提醒助手',
    notificationText: '您有一笔待处理账单，请及时登录系统处理。',
  };

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  req.on('close', () => {
    if (!res.writableEnded) {
      res.end();
    }
  });

  try {
    for await (const chunk of runNotificationAgentTurn({ body, notificationContext })) {
      if (res.writableEnded) break;

      writeSse(res, {
        id: requestId,
        created: Math.floor(Date.now() / 1000),
        message: chunk,
      });
    }

    if (!res.writableEnded) {
      res.write('data: [DONE]\n\n');
      res.end();
    }
  } catch (error) {
    if (!res.writableEnded) {
      res.end();
    }
  }
});

app.listen(3000, () => {
  console.log('Vox phone notification callback server listening on :3000');
});
