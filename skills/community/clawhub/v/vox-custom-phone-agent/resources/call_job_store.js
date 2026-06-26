'use strict';

class CallJobStore {
  constructor() {
    this.jobs = new Map();
  }

  createJob(job) {
    if (!job || !job.requestId) throw new Error('requestId is required');
    const now = Date.now();
    const value = {
      ...job,
      createdAt: job.createdAt || now,
      updatedAt: now,
      callbackAttempts: job.callbackAttempts || 0,
      callbackStatus: job.callbackStatus || 'polling',
      lastCallbackError: job.lastCallbackError || ''
    };
    this.jobs.set(value.requestId, value);
    return value;
  }

  getJobByRequestId(requestId) {
    return this.jobs.get(requestId) || null;
  }

  updateJob(requestId, patch = {}) {
    const existing = this.getJobByRequestId(requestId);
    if (!existing) return null;
    const next = { ...existing, ...patch, updatedAt: Date.now() };
    this.jobs.set(requestId, next);
    return next;
  }

  markEnded(requestId, result) {
    return this.updateJob(requestId, {
      status: 'ended',
      endedAt: Date.now(),
      result,
      callbackStatus: 'pending'
    });
  }

  markCallbackSent(requestId) {
    return this.updateJob(requestId, {
      callbackStatus: 'sent',
      callbackSentAt: Date.now(),
      lastCallbackError: ''
    });
  }

  markCallbackFailed(requestId, error, retryAt = null) {
    const existing = this.getJobByRequestId(requestId);
    return this.updateJob(requestId, {
      callbackStatus: retryAt ? 'failed_retryable' : 'failed_final',
      callbackAttempts: existing ? existing.callbackAttempts + 1 : 1,
      lastCallbackError: error && error.message ? error.message : String(error || 'unknown'),
      retryAt
    });
  }
}

const defaultCallJobStore = new CallJobStore();

module.exports = { CallJobStore, defaultCallJobStore };
