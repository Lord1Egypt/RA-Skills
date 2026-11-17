import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
  dedupeParsedUrls,
  extractFigmaUrlsFromIssue,
  parseFigmaDesignUrl,
} from '../scripts/lib/figma-url.mjs';

describe('parseFigmaDesignUrl', () => {
  it('canonicalizes dash node ids and preserves the original node id', () => {
    const result = parseFigmaDesignUrl(
      'https://www.figma.com/design/VSfJU5zJ10wSdeMu2vk1Ar/File?node-id=6127-21193',
    );

    assert.equal(result.ok, true);
    assert.equal(result.fileKey, 'VSfJU5zJ10wSdeMu2vk1Ar');
    assert.equal(result.nodeId, '6127:21193');
    assert.equal(result.originalNodeId, '6127-21193');
    assert.equal(result.kind, 'design');
  });

  it('accepts already-canonical colon node ids', () => {
    const result = parseFigmaDesignUrl(
      'https://figma.com/design/VSfJU5zJ10wSdeMu2vk1Ar/File?node-id=6127:21193',
    );

    assert.equal(result.ok, true);
    assert.equal(result.nodeId, '6127:21193');
    assert.equal(result.originalNodeId, '6127:21193');
  });

  it('accepts figma.com and www.figma.com hosts', () => {
    const withoutWww = parseFigmaDesignUrl(
      'https://figma.com/design/fileKey123/File?node-id=1-2',
    );
    const withWww = parseFigmaDesignUrl(
      'https://www.figma.com/design/fileKey123/File?node-id=1-2',
    );

    assert.equal(withoutWww.ok, true);
    assert.equal(withWww.ok, true);
  });

  it('ignores unrelated query params and hash fragments', () => {
    const result = parseFigmaDesignUrl(
      'https://www.figma.com/design/VSfJU5zJ10wSdeMu2vk1Ar/File?node-id=6127-21193&t=abc&m=dev#section',
    );

    assert.equal(result.ok, true);
    assert.equal(result.fileKey, 'VSfJU5zJ10wSdeMu2vk1Ar');
    assert.equal(result.nodeId, '6127:21193');
  });

  it('returns stable missing_node_id when node-id is absent', () => {
    const result = parseFigmaDesignUrl(
      'https://www.figma.com/design/VSfJU5zJ10wSdeMu2vk1Ar/File?t=abc',
    );

    assert.equal(result.ok, false);
    assert.equal(result.errorCode, 'missing_node_id');
  });

  it('rejects unsupported Figma URL kinds with a stable code', () => {
    for (const kind of ['board', 'slides', 'make']) {
      const result = parseFigmaDesignUrl(
        `https://www.figma.com/${kind}/VSfJU5zJ10wSdeMu2vk1Ar/File?node-id=1-2`,
      );

      assert.equal(result.ok, false);
      assert.equal(result.errorCode, 'unsupported_figma_url_kind');
      assert.equal(result.kind, kind);
    }
  });

  it('rejects non-Figma hosts and malformed URLs with stable parse errors', () => {
    assert.deepEqual(
      {
        ok: parseFigmaDesignUrl('https://example.com/design/file/File?node-id=1-2').ok,
        errorCode: parseFigmaDesignUrl('https://example.com/design/file/File?node-id=1-2').errorCode,
      },
      { ok: false, errorCode: 'non_figma_host' },
    );

    const malformed = parseFigmaDesignUrl('not a url');
    assert.equal(malformed.ok, false);
    assert.equal(malformed.errorCode, 'malformed_url');
  });
});

describe('dedupeParsedUrls', () => {
  it('preserves ordinal and marks later duplicates', () => {
    const parsed = [
      parseFigmaDesignUrl('https://www.figma.com/design/fileKey123/File?node-id=1-2'),
      parseFigmaDesignUrl('https://figma.com/design/fileKey123/File?node-id=1:2&t=ignored'),
      parseFigmaDesignUrl('https://www.figma.com/design/fileKey123/File?node-id=2-3'),
    ];

    const deduped = dedupeParsedUrls(parsed);

    assert.deepEqual(
      deduped.map((entry) => ({
        ordinal: entry.ordinal,
        nodeId: entry.nodeId,
        duplicateOf: entry.duplicateOf,
      })),
      [
        { ordinal: 1, nodeId: '1:2', duplicateOf: null },
        { ordinal: 2, nodeId: '1:2', duplicateOf: 1 },
        { ordinal: 3, nodeId: '2:3', duplicateOf: null },
      ],
    );
  });
});

describe('extractFigmaUrlsFromIssue', () => {
  it('reads top-level figma_urls with fixed source metadata', () => {
    const result = extractFigmaUrlsFromIssue({
      figma_urls: ['https://figma.com/design/fileKey123/File?node-id=1-2'],
    });

    assert.equal(result.ok, true);
    assert.equal(result.source, 'figma_urls');
    assert.equal(result.inputShape, 'top-level');
    assert.deepEqual(result.urls, ['https://figma.com/design/fileKey123/File?node-id=1-2']);
  });

  it('reads issue.figma_urls with fixed source metadata', () => {
    const result = extractFigmaUrlsFromIssue({
      issue: { figma_urls: ['https://figma.com/design/fileKey123/File?node-id=1-2'] },
    });

    assert.equal(result.ok, true);
    assert.equal(result.source, 'issue.figma_urls');
    assert.equal(result.inputShape, 'issue-field');
  });

  it('reads data.figma_urls with fixed source metadata', () => {
    const result = extractFigmaUrlsFromIssue({
      data: { figma_urls: ['https://figma.com/design/fileKey123/File?node-id=1-2'] },
    });

    assert.equal(result.ok, true);
    assert.equal(result.source, 'data.figma_urls');
    assert.equal(result.inputShape, 'data-field');
  });

  it('ignores empty strings and returns figma_urls_empty when no non-empty arrays exist', () => {
    const result = extractFigmaUrlsFromIssue({
      figma_urls: ['', '   '],
      issue: { figma_urls: [] },
      data: { figma_urls: [] },
    });

    assert.equal(result.ok, false);
    assert.equal(result.errorCode, 'figma_urls_empty');
    assert.deepEqual(result.urls, []);
  });
});
