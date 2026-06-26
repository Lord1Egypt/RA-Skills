'use strict';

const { queryCallStatus, queryCallTurns } = require('./vox_call_result_client');
const { sendPostCallCallback } = require('./post_call_callback_client');

function startPostCallPolling({ job, credentials, store, env = process.env, fetchImpl = globalThis.fetch }) {
  const poller = new VoxResultPoller({ job, credentials, store, env, fetchImpl });
  poller.schedule(0);
  return poller;
}

class VoxResultPoller {
  constructor({ job, credentials, store, env = process.env, fetchImpl = globalThis.fetch }) {
    this.job = job;
    this.credentials = credentials;
    this.store = store;
    this.env = env;
    this.fetchImpl = fetchImpl;
    this.attempts = 0;
    this.maxAttempts = Number(env.VOX_RESULT_POLL_MAX_ATTEMPTS || 40);
    this.intervalMs = Number(env.VOX_RESULT_POLL_INTERVAL_MS || 15000);
    this.callbackMaxRetries = Number(env.POST_CALL_CALLBACK_MAX_RETRIES || 5);
  }

  schedule(delayMs) {
    const timer = setTimeout(() => this.tick().catch(() => {}), delayMs);
    if (timer.unref) timer.unref();
  }

  async tick() {
    this.attempts += 1;
    const status = await queryCallStatus({ credentials: this.credentials, callId: this.job.callId, fetchImpl: this.fetchImpl });
    this.store.updateJob(this.job.requestId, { status: status.status, lastStatus: status.status, pollAttempts: this.attempts });

    if (status.status === 'completed') {
      const turns = await queryCallTurns({ credentials: this.credentials, callId: this.job.callId, fetchImpl: this.fetchImpl });
      const result = {
        status: 'completed',
        turns: turns.turns,
        transcript: turns.transcript
      };
      this.store.markEnded(this.job.requestId, result);
      await this.sendCallbackWithRetry(result);
      return;
    }

    if (this.attempts >= this.maxAttempts) {
      const result = { status: status.status === 'not_found' ? 'not_found' : 'query_timeout', turns: [], transcript: [] };
      this.store.markEnded(this.job.requestId, result);
      await this.sendCallbackWithRetry(result);
      return;
    }

    this.schedule(this.intervalMs);
  }

  async sendCallbackWithRetry(result, attempt = 1) {
    try {
      const response = await sendPostCallCallback({ job: this.job, result, env: this.env, fetchImpl: this.fetchImpl });
      if (response.ok) {
        this.store.markCallbackSent(this.job.requestId);
        return;
      }
      throw new Error(`callback HTTP ${response.httpStatus || 'unknown'}`);
    } catch (error) {
      if (attempt >= this.callbackMaxRetries) {
        this.store.markCallbackFailed(this.job.requestId, error, null);
        return;
      }
      const retryAt = Date.now() + retryDelayMs(attempt);
      this.store.markCallbackFailed(this.job.requestId, error, retryAt);
      const timer = setTimeout(() => this.sendCallbackWithRetry(result, attempt + 1).catch(() => {}), retryDelayMs(attempt));
      if (timer.unref) timer.unref();
    }
  }
}

function retryDelayMs(attempt) {
  const delays = [60 * 1000, 5 * 60 * 1000, 15 * 60 * 1000, 60 * 60 * 1000, 6 * 60 * 60 * 1000];
  return delays[Math.min(attempt - 1, delays.length - 1)];
}

module.exports = { VoxResultPoller, startPostCallPolling, retryDelayMs };
