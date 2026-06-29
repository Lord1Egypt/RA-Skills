const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const helpers = require('../fetch_topics.js');

test('resolveToken only accepts non-empty ZSXQ_TOKEN from the environment', () => {
  assert.equal(helpers.resolveToken({ ZSXQ_TOKEN: ' abc123 ' }), 'abc123');
  assert.equal(helpers.resolveToken({ ZSXQ_TOKEN: '' }), '');
  assert.equal(helpers.resolveToken({}), '');
  assert.equal(helpers.resolveToken({ TOKEN_FILE: 'token.json' }), '');
});

test('resolveBackend defaults to official cli and only uses http when explicit', () => {
  assert.equal(helpers.resolveBackend({}, {}), 'cli');
  assert.equal(helpers.resolveBackend({ backend: 'http' }, {}), 'http');
  assert.equal(helpers.resolveBackend({ backend: 'cli' }, {}), 'cli');
  assert.equal(helpers.resolveBackend({ backend: 'http' }, { ZSXQ_BACKEND: 'cli' }), 'cli');
  assert.equal(helpers.resolveBackend({}, { ZSXQ_BACKEND: ' http ' }), 'http');
});

test('parseTopicId accepts raw IDs and Knowledge Planet topic URLs', () => {
  assert.equal(helpers.parseTopicId('82811454228448260'), '82811454228448260');
  assert.equal(helpers.parseTopicId('https://wx.zsxq.com/topic/82811454228448260'), '82811454228448260');
  assert.equal(helpers.parseTopicId('https://wx.zsxq.com/dweb2/index/topic_detail/82811454228448260'), '82811454228448260');
});

test('classifyTopicDate identifies in-range and before-range timestamps', () => {
  assert.equal(
    helpers.classifyTopicDate('2026-06-10T12:30:00.000+0800', '2026-06-01', '2026-06-13'),
    'in-range',
  );
  assert.equal(
    helpers.classifyTopicDate('2026-05-31T23:59:59.000+0800', '2026-06-01', '2026-06-13'),
    'before-range',
  );
  assert.equal(
    helpers.classifyTopicDate('2026-06-14T00:00:00.000+0800', '2026-06-01', '2026-06-13'),
    'after-range',
  );
});

test('attachment helpers generate stable directories and safe filenames', () => {
  assert.equal(
    helpers.getTopicAttachmentDir('/tmp/zsxq', 'group1', '2026-06-13'),
    path.join('/tmp/zsxq', 'group1', '2026-06-13'),
  );
  assert.equal(
    helpers.sanitizeAttachmentFilename('Lumentum Holdings Inc. LITE 纪要.pdf', 'fallback.pdf'),
    'Lumentum_Holdings_Inc._LITE_纪要.pdf',
  );
  assert.equal(
    helpers.sanitizeAttachmentFilename('天风证券-港股策略周观察：SpaceX历史级IPO将至，怎么看？.pdf', 'fallback.pdf'),
    '天风证券-港股策略周观察：SpaceX历史级IPO将至，怎么看？.pdf',
  );
  assert.equal(
    helpers.getAttachmentFilename('14422448224154122', '天风证券-港股策略周观察：SpaceX历史级IPO将至，怎么看？.pdf'),
    '14422448224154122_天风证券-港股策略周观察：SpaceX历史级IPO将至，怎么看？.pdf',
  );
  assert.equal(
    helpers.sanitizeAttachmentFilename('foo/bar:baz?.pdf', 'fallback.pdf'),
    'foo_bar_baz_.pdf',
  );
  assert.equal(helpers.sanitizeAttachmentFilename('', 'fallback.pdf'), 'fallback.pdf');
  assert.equal(helpers.getAttachmentFilename('topic1', 'report.pdf'), 'topic1_report.pdf');
  assert.equal(helpers.getAttachmentFilename('topic1', 'image 1.jpg'), 'topic1_image_1.jpg');
});

test('resolveAttachmentDir prefers environment variables over config', () => {
  assert.equal(
    helpers.resolveAttachmentDir({ attachment_dir: '/config/root' }, { ZSXQ_ATTACHMENT_DIR: '/env/root' }),
    '/env/root',
  );
  assert.equal(
    helpers.resolveAttachmentDir({ attachment_dir: '/config/root' }, { ATTACHMENT_DIR: '/alias/root' }),
    '/alias/root',
  );
  assert.equal(helpers.resolveAttachmentDir({ attachment_dir: '/config/root' }, {}), '/config/root');
});

test('getMarkdownPath stores markdown under attachment root and group by date', () => {
  assert.equal(
    helpers.getMarkdownPath('/tmp/zsxq', 'group1', '2026-06-13'),
    path.join('/tmp/zsxq', 'group1', '2026-06-13.md'),
  );
});

test('renderTopicMarkdown references local image and file attachments relatively', () => {
  const markdownPath = path.join('/tmp/zsxq', 'group1', '2026-06-13.md');
  const topic = {
    topic_id: 'topic1',
    text: 'Hello **world**',
    create_time: '2026-06-13T10:30:00.000+0800',
    owner: { name: 'Alice' },
    likes_count: 2,
    comments_count: 3,
    reading_count: 4,
    attachments_local: [
      { type: 'image', filename: 'topic1_image_1.jpg', path: path.join('/tmp/zsxq', 'group1', '2026-06-13', 'topic1_image_1.jpg') },
      { type: 'file', filename: 'topic1_report.pdf', path: path.join('/tmp/zsxq', 'group1', '2026-06-13', 'topic1_report.pdf') },
    ],
  };

  const markdown = helpers.renderTopicMarkdown(topic, markdownPath, 1);

  assert.match(markdown, /## 1\. Alice/);
  assert.match(markdown, /原帖: https:\/\/wx\.zsxq\.com\/topic\/topic1/);
  assert.match(markdown, /!\[topic1_image_1\.jpg\]\(2026-06-13\/topic1_image_1\.jpg\)/);
  assert.match(markdown, /\[topic1_report\.pdf\]\(2026-06-13\/topic1_report\.pdf\)/);
});

test('writeMarkdownByDate writes date-split markdown under attachment root and group', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'zsxq-md-test-'));
  const paths = helpers.writeMarkdownByDate({
    group_id: 'group1',
    topics: [{
      topic_id: 'topic1',
      text: 'Daily note',
      create_time: '2026-06-13T10:30:00.000+0800',
      owner: { name: 'Alice' },
      attachments_local: [
        { type: 'file', filename: 'topic1_report.pdf', path: path.join(root, 'group1', '2026-06-13', 'topic1_report.pdf') },
      ],
    }],
  }, root);

  assert.deepEqual(paths, [path.join(root, 'group1', '2026-06-13.md')]);
  const markdown = fs.readFileSync(paths[0], 'utf8');
  assert.match(markdown, /^# 知识星球帖子导出 - 2026-06-13/m);
  assert.match(markdown, /\[topic1_report\.pdf\]\(2026-06-13\/topic1_report\.pdf\)/);
});

test('createBrowserHeaders includes browser identity and fetch metadata', () => {
  const headers = helpers.createBrowserHeaders();

  assert.match(headers['User-Agent'], /Chrome\/\d+/);
  assert.equal(headers['Accept-Language'], 'zh-CN,zh;q=0.9,en;q=0.8');
  assert.equal(headers.Origin, 'https://wx.zsxq.com');
  assert.equal(headers.Referer, 'https://wx.zsxq.com/');
  assert.equal(headers['Sec-Fetch-Site'], 'same-site');
  assert.equal(headers['Sec-Fetch-Mode'], 'cors');
  assert.equal(headers['Sec-Fetch-Dest'], 'empty');
  assert.match(headers['sec-ch-ua'], /Chromium/);
  assert.equal(headers['sec-ch-ua-mobile'], '?0');
  assert.equal(headers['sec-ch-ua-platform'], '"macOS"');
});

test('createAuthHeaders adds cookie and a fresh timestamp for every request', () => {
  const originalNow = Date.now;
  try {
    Date.now = () => 1781348688000;
    const first = helpers.createAuthHeaders('token-one');
    Date.now = () => 1781348699000;
    const second = helpers.createAuthHeaders('token-one');

    assert.equal(first.Cookie, 'zsxq_access_token=token-one');
    assert.equal(first['X-Timestamp'], '1781348688');
    assert.equal(second['X-Timestamp'], '1781348699');
    assert.notEqual(first['X-Timestamp'], second['X-Timestamp']);
  } finally {
    Date.now = originalNow;
  }
});

test('calculateRetryDelayMs applies exponential backoff with bounded jitter', () => {
  assert.equal(helpers.calculateRetryDelayMs(0, { random: () => 0.5 }), 2000);
  assert.equal(helpers.calculateRetryDelayMs(1, { random: () => 0.5 }), 4000);
  assert.equal(helpers.calculateRetryDelayMs(2, { random: () => 0.5 }), 8000);
  assert.equal(helpers.calculateRetryDelayMs(0, { random: () => 0 }), 1500);
  assert.equal(helpers.calculateRetryDelayMs(0, { random: () => 1 }), 2500);
  assert.equal(helpers.calculateRetryDelayMs(4, { random: () => 0.5, maxMs: 10000 }), 10000);
  assert.equal(helpers.calculateRetryDelayMs(4, { random: () => 1, maxMs: 10000 }), 10000);
});

test('builds official zsxq-cli commands for groups topics and topic detail', () => {
  assert.deepEqual(
    helpers.buildCliGroupsArgs(),
    ['group', '+list', '--json', '--limit', '200', '--scope', 'all'],
  );
  assert.deepEqual(
    helpers.buildCliTopicsArgs('group1', { limit: 50 }),
    ['group', '+topics', '--group-id', 'group1', '--limit', '30', '--json'],
  );
  assert.deepEqual(
    helpers.buildCliTopicsArgs('group1', { limit: 10, endTime: '2026-06-13T10:30:00.000+0800' }),
    ['group', '+topics', '--group-id', 'group1', '--limit', '10', '--end-time', '2026-06-13T10:30:00.000+0800', '--json'],
  );
  assert.deepEqual(
    helpers.buildCliTopicDetailArgs('82811454228448260'),
    ['topic', '+detail', '--topic-id', '82811454228448260', '--json'],
  );
});

test('normalizes zsxq-cli topic JSON into the existing topic model', () => {
  const topic = helpers.normalizeCliTopic({
    topic_id: 123,
    type: 'talk',
    title: '周观察',
    create_time: '2026-06-13T10:30:00.000+0800',
    is_digested: true,
    likes_count: 2,
    comments_count: 3,
    reading_count: 4,
    readers_count: 5,
    talk: {
      text: 'SpaceX IPO 观察',
      owner: { user_id: 456, name: 'Alice' },
      images: [{ image_id: 'img1', type: 'png', large: { url: 'https://img.example/1.png' } }],
      files: [{
        file_id: 'file1',
        name: '天风证券-港股策略周观察：SpaceX历史级IPO将至，怎么看？.pdf',
        size: 1024,
        download_url: 'https://file.example/report.pdf',
      }],
    },
  });

  assert.equal(topic.topic_id, '123');
  assert.equal(topic.text, 'SpaceX IPO 观察');
  assert.deepEqual(topic.owner, { user_id: '456', name: 'Alice' });
  assert.equal(topic.digested, true);
  assert.equal(topic.image_count, 1);
  assert.equal(topic.file_count, 1);
  assert.equal(topic.images[0].large.url, 'https://img.example/1.png');
  assert.equal(topic.files[0].name, '天风证券-港股策略周观察：SpaceX历史级IPO将至，怎么看？.pdf');
});

test('normalizes zsxq-cli groups and detects digest marker availability', () => {
  assert.deepEqual(helpers.normalizeCliGroup({
    id: 123,
    name: '研究星球',
    description: '长期研究',
    stats: { members: 10, topics: 20 },
    owner: { id: 456, name: 'Owner' },
  }), {
    group_id: '123',
    name: '研究星球',
    description: '长期研究',
    member_count: 10,
    topics_count: 20,
    owner: { user_id: '456', name: 'Owner' },
  });

  assert.equal(helpers.topicHasDigestMarker({ digested: false }), true);
  assert.equal(helpers.topicHasDigestMarker({ is_digested: true }), true);
  assert.equal(helpers.topicHasDigestMarker({ topic_id: 1, talk: { text: 'no marker' } }), false);
});

test('runZsxqCliJson maps CLI failures to clear JSON errors', async () => {
  const missing = await helpers.runZsxqCliJson(['group', '+list'], async () => {
    const err = new Error('spawn zsxq-cli ENOENT');
    err.code = 'ENOENT';
    throw err;
  });
  assert.equal(missing.ok, false);
  assert.equal(missing.error, 'zsxq_cli_missing');
  assert.match(missing.hint, /npm install -g zsxq-cli/);

  const unauthenticated = await helpers.runZsxqCliJson(['group', '+list'], async () => ({
    code: 1,
    stdout: '',
    stderr: 'not logged in; please run zsxq-cli auth login',
  }));
  assert.equal(unauthenticated.ok, false);
  assert.equal(unauthenticated.error, 'zsxq_cli_not_authenticated');
  assert.match(unauthenticated.hint, /zsxq-cli auth login/);

  const nonJson = await helpers.runZsxqCliJson(['group', '+list'], async () => ({
    code: 0,
    stdout: 'login required',
    stderr: '',
  }));
  assert.equal(nonJson.ok, false);
  assert.equal(nonJson.error, 'zsxq_cli_non_json');

  const ok = await helpers.runZsxqCliJson(['group', '+list'], async () => ({
    code: 0,
    stdout: '{"groups":[]}',
    stderr: '',
  }));
  assert.equal(ok.ok, true);
  assert.deepEqual(ok.data, { groups: [] });
});

test('parseCliArgs recognizes search download attachment flag', () => {
  const cli = helpers.parseCliArgs([
    'node',
    'fetch_topics.js',
    'search',
    'group1',
    'SpaceX IPO',
    '20',
    '--markdown',
    '--download-attachments',
  ]);

  assert.equal(cli.subcommand, 'search');
  assert.deepEqual(cli.args, ['group1', 'SpaceX IPO', '20']);
  assert.equal(cli.markdown, true);
  assert.equal(cli.downloadAttachments, true);
});

test('builds official zsxq-cli MCP search_topics command', () => {
  assert.deepEqual(
    helpers.buildCliSearchTopicsArgs('group1', 'SpaceX IPO'),
    ['api', 'call', 'search_topics', '--params', '{"group_id":"group1","query":"SpaceX IPO"}', '--format', 'json'],
  );
});

test('shouldDownloadAttachments supports config defaults and per-command override', () => {
  assert.equal(helpers.shouldDownloadAttachments({ download_attachments: true }, {}), true);
  assert.equal(helpers.shouldDownloadAttachments({ download_attachments: false }, {}), false);
  assert.equal(helpers.shouldDownloadAttachments({ download_attachments: false }, { downloadAttachments: true }), true);
});

test('topicMatchesQuery searches title text owner and attachment names case-insensitively', () => {
  const topic = {
    title: '港股策略周观察',
    text: 'SpaceX IPO 将至',
    owner: { name: 'Alice' },
    files: [{ name: '天风证券-SpaceX.pdf' }],
  };

  assert.equal(helpers.topicMatchesQuery(topic, 'spacex'), true);
  assert.equal(helpers.topicMatchesQuery(topic, '港股'), true);
  assert.equal(helpers.topicMatchesQuery(topic, 'alice'), true);
  assert.equal(helpers.topicMatchesQuery(topic, '不存在'), false);
});

test('normalizeSearchResult keeps topic ids from common zsxq-cli search shapes', () => {
  assert.deepEqual(
    helpers.normalizeSearchResult({ topic_id: 123, text: 'hit' }),
    { topic_id: '123', raw: { topic_id: 123, text: 'hit' } },
  );
  assert.deepEqual(
    helpers.normalizeSearchResult({ topic: { id: 456, text: 'hit' } }),
    { topic_id: '456', raw: { topic: { id: 456, text: 'hit' } } },
  );
});

test('extractCliSearchTopics accepts common search result containers', () => {
  assert.deepEqual(
    helpers.extractCliSearchTopics({ data: { topics: [{ topic_id: 1 }] } }),
    [{ topic_id: 1 }],
  );
  assert.deepEqual(
    helpers.extractCliSearchTopics({ results: [{ topic_id: 2 }] }),
    [{ topic_id: 2 }],
  );
  assert.deepEqual(
    helpers.extractCliSearchTopics([{ topic_id: 3 }]),
    [{ topic_id: 3 }],
  );
});

test('collectSearchTopicsCli details hits, skips missing ids, and falls back when detail fails', async () => {
  const calls = [];
  const runner = async (args) => {
    calls.push(args);
    if (args[2] === 'search_topics') {
      return {
        ok: true,
        data: {
          results: [
            { title: 'missing id' },
            { topic_id: 1, text: 'SpaceX hit from search' },
            { topic_id: 2, text: 'fallback hit from search' },
          ],
        },
      };
    }
    if (args.includes('1')) {
      return {
        ok: true,
        data: {
          topic: {
            topic_id: 1,
            text: 'SpaceX detailed hit',
            create_time: '2026-06-13T10:30:00.000+0800',
          },
        },
      };
    }
    return { ok: false, error: 'zsxq_cli_failed', detail: 'detail unavailable' };
  };

  const result = await helpers.collectSearchTopicsCli({
    groupId: 'group1',
    query: 'SpaceX',
    count: 2,
    cli: { downloadAttachments: false },
    config: { download_attachments: false },
    runner,
    downloadAttachments: async () => {
      throw new Error('download should not run');
    },
  });

  assert.deepEqual(result.topics.map((topic) => topic.topic_id), ['1', '2']);
  assert.equal(result.topics[1].detail_error, 'zsxq_cli_failed');
  assert.equal(calls.filter((args) => args[0] === 'topic' && args[1] === '+detail').length, 2);
});

test('filterTopicsByQuery returns only matching normalized topics', () => {
  const topics = [
    { topic_id: '1', title: 'SpaceX IPO', text: '火箭公司', owner: { name: 'A' }, files: [] },
    { topic_id: '2', title: '消费', text: '港股策略', owner: { name: 'B' }, files: [] },
  ];

  assert.deepEqual(
    helpers.filterTopicsByQuery(topics, 'spacex').map((topic) => topic.topic_id),
    ['1'],
  );
});
