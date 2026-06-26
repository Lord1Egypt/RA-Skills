"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.STATUS_FILTER_REVERSE = exports.STATUS_REVERSE = exports.STATUS_MAP = void 0;
exports.STATUS_MAP = {
    bonding: 'rising',
    complete: 'ready',
    migrated: 'ascended',
    reclaimed: 'razed',
};
exports.STATUS_REVERSE = {
    rising: 'bonding',
    ready: 'complete',
    ascended: 'migrated',
    razed: 'reclaimed',
};
exports.STATUS_FILTER_REVERSE = {
    rising: 'bonding',
    ready: 'complete',
    ascended: 'migrated',
    razed: 'reclaimed',
    all: 'all',
};
