import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { withPool } from '../src/ssh/pool.js';

describe('withPool', () => {
  it('runs all tasks and returns results in order', async () => {
    const tasks = [
      () => Promise.resolve('a'),
      () => Promise.resolve('b'),
      () => Promise.resolve('c'),
    ];
    const results = await withPool(tasks, 2);
    assert.equal(results.length, 3);
    assert.equal(results[0].status, 'fulfilled');
    assert.equal((results[0] as PromiseFulfilledResult<string>).value, 'a');
    assert.equal((results[2] as PromiseFulfilledResult<string>).value, 'c');
  });

  it('handles rejections without stopping others', async () => {
    const tasks = [
      () => Promise.resolve('ok'),
      () => Promise.reject(new Error('boom')),
      () => Promise.resolve('also ok'),
    ];
    const results = await withPool(tasks, 2);
    assert.equal(results.length, 3);
    assert.equal(results[0].status, 'fulfilled');
    assert.equal(results[1].status, 'rejected');
    assert.equal(results[2].status, 'fulfilled');
  });

  it('respects concurrency limit', async () => {
    let concurrent = 0;
    let maxConcurrent = 0;
    const tasks = Array.from({ length: 10 }, () => async () => {
      concurrent++;
      maxConcurrent = Math.max(maxConcurrent, concurrent);
      await new Promise((r) => setTimeout(r, 20));
      concurrent--;
      return 'done';
    });
    await withPool(tasks, 3);
    assert.ok(maxConcurrent <= 3, `max concurrent was ${maxConcurrent}, expected <=3`);
  });

  it('works with empty task list', async () => {
    const results = await withPool([], 5);
    assert.equal(results.length, 0);
  });
});
