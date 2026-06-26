'use strict';

const { StateStore } = require('./state-store');

const WALLET_KEY = 'subWalletId';
const API_KEY_KEY = 'apiKey';

class Memory {
  constructor() {
    this._stateStore = new StateStore();
  }

  rememberWallet(subWalletId) {
    this._stateStore.savePreference(WALLET_KEY, subWalletId);
  }

  recallWallet() {
    return this._stateStore.getPreference(WALLET_KEY, null);
  }

  forgetWallet() {
    this._stateStore.deletePreference(WALLET_KEY);
  }

  rememberApiKey(apiKey) {
    this._stateStore.savePreference(API_KEY_KEY, apiKey);
  }

  recallApiKey() {
    return this._stateStore.getPreference(API_KEY_KEY, null);
  }

  forgetApiKey() {
    this._stateStore.deletePreference(API_KEY_KEY);
  }
}

module.exports = { Memory };
