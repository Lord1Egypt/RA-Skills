import assert from 'node:assert/strict';
const scenario = process.env.RECEIPT_TEST_SCENARIO;
const post = { id: 456, date: '2026-11-07T12:00:00', status: 'publish', link: 'https://example.test/post/', title: { rendered: 'Test' } };
if (scenario === 'foreign') post.link = 'https://other.invalid/post/';
if (scenario === 'wrong-id') post.id = 999;
if (scenario === 'draft') post.status = 'draft';
globalThis.fetch = async (input, options = {}) => {
  const url = String(input);
  assert.equal(options.redirect, 'error');
  if (scenario === 'no-network') throw new Error('UNEXPECTED_NETWORK');
  if (url.startsWith('https://example.test/wp-json/wp/v2/posts')) {
    if (options.method === 'POST') {
      const body = JSON.parse(options.body);
      assert.ok(['publish', 'draft'].includes(body.status));
      post.status = body.status;
      return Response.json(post);
    }
    if (url.includes('/posts?')) return Response.json(scenario === 'duplicate-failure' ? [post] : []);
    return Response.json(post);
  }
  assert.equal(url, 'https://example.test/post/');
  assert.equal(options.headers?.Authorization, undefined);
  if (scenario === 'redirect') throw new TypeError('redirect rejected');
  return new Response('page', {status: scenario === 'duplicate-failure' ? 404 : 200});
};
