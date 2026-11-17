/* Fixed JXA bridge: one JSON request file, no generated code or UI scripting. */
var SNAPSHOT_FIELDS = ['id', 'modificationDate', 'name', 'body', 'priority', 'flagged', 'completed',
    'completionDate', 'dueDate', 'alldayDueDate',
    'remindMeDate', 'creationDate'];

function syncFailure(code, message) {
    var error = new Error(message);
    error.syncCode = code;
    throw error;
}

function own(object, key) { return Object.prototype.hasOwnProperty.call(object, key); }
function markerFor(namespace, taskId) { return '[team-tasks:v1:' + namespace + ':' + taskId + ']'; }
function firstLine(body) { return (body || '').split('\n')[0]; }

function taskFromMarker(body, namespace) {
    var line = firstLine(body);
    var prefix = '[team-tasks:v1:' + namespace + ':';
    if (line.indexOf(prefix) !== 0 || line.charAt(line.length - 1) !== ']') return null;
    var taskId = line.slice(prefix.length, -1);
    return /^T-\d{6}-\d{3,}$/.test(taskId) ? taskId : null;
}

function isoDate(value) {
    if (value === null || value === undefined) return null;
    if (!(value instanceof Date) || !isFinite(value.getTime())) {
        syncFailure('macos_snapshot_invalid', 'A native date field could not be read reliably');
    }
    return value.toISOString();
}

function pad(number, count) {
    var value = String(number);
    while (value.length < count) value = '0' + value;
    return value;
}

function calendarDate(value) {
    if (!(value instanceof Date) || !isFinite(value.getTime())) {
        syncFailure('macos_snapshot_invalid', 'A native all-day date could not be read reliably');
    }
    return pad(value.getFullYear(), 4) + '-' + pad(value.getMonth() + 1, 2) + '-' + pad(value.getDate(), 2);
}

function dayDate(text) {
    var parts = text.split('-').map(Number);
    // Noon avoids DST midnight transitions; setFullYear also handles years below 100.
    var date = new Date(2000, 0, 1, 12, 0, 0);
    date.setFullYear(parts[0], parts[1] - 1, parts[2]);
    return date;
}

function sameInstant(left, right) {
    if (left === null || right === null) return left === right;
    return new Date(left).getTime() === new Date(right).getTime();
}

function snapshotDeadline(due, allDay, alarm) {
    // Reminders may populate all three properties for either deadline kind.
    // A due time distinct from the all-day anchor is the reliable timed signal.
    if (due && (!allDay || !sameInstant(due, allDay))) {
        return {due: {kind: 'timed', at: isoDate(due)}, remindMeDate: isoDate(alarm)};
    }
    if (allDay) {
        return {due: {kind: 'allDay', date: calendarDate(allDay)},
            remindMeDate: alarm && sameInstant(alarm, allDay) ? null : isoDate(alarm)};
    }
    return {due: {kind: 'none'}, remindMeDate: isoDate(alarm)};
}

function validateItem(item, namespace, taskId) {
    var marker = markerFor(namespace, taskId);
    if (!item || !/^T-\d{6}-\d{3,}$/.test(taskId) || item.taskId !== taskId ||
            item.marker !== marker || typeof item.name !== 'string' || !item.name.trim() ||
            typeof item.body !== 'string' || firstLine(item.body) !== marker ||
            typeof item.completed !== 'boolean' || typeof item.flagged !== 'boolean' ||
            [1, 5, 9].indexOf(item.priority) === -1 || !item.due ||
            ['none', 'allDay', 'timed'].indexOf(item.due.kind) === -1) {
        syncFailure('invalid_request', 'Invalid item for ' + taskId);
    }
    if (item.due.kind === 'timed' && (typeof item.due.at !== 'string' ||
            !/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(item.due.at) ||
            !isFinite(new Date(item.due.at).getTime()))) {
        syncFailure('invalid_request', 'Invalid timed deadline for ' + taskId);
    }
    if (item.due.kind === 'allDay' && (typeof item.due.date !== 'string' ||
            !/^\d{4}-\d{2}-\d{2}$/.test(item.due.date) ||
            calendarDate(dayDate(item.due.date)) !== item.due.date)) {
        syncFailure('invalid_request', 'Invalid all-day deadline for ' + taskId);
    }
}

function readListIndex(app, listName) {
    var ids = app.lists.id();
    var names = app.lists.name();
    if (!Array.isArray(ids) || !Array.isArray(names) || ids.length !== names.length) {
        syncFailure('macos_snapshot_unstable', 'List membership changed while reading');
    }
    var target = null;
    var count = 0;
    var known = Object.create(null);
    ids.forEach(function (id, index) {
        if (typeof id !== 'string' || !id || known[id]) {
            syncFailure('macos_snapshot_invalid', 'Invalid native list identifier');
        }
        known[id] = true;
        if (names[index] === listName) { target = id; count += 1; }
    });
    if (count > 1) syncFailure('macos_list_conflict', 'Multiple lists are named ' + listName);
    return {ids: ids, names: names, target: target, known: known};
}

function readContainerIds(app, ids) {
    try {
        // A composed object specifier retrieves all container IDs in one AppleEvent.
        var projected = app.reminders.container.id();
        if (Array.isArray(projected) && projected.length === ids.length &&
                projected.every(function (id) { return typeof id === 'string' && id.length > 0; })) {
            return projected;
        }
    } catch (error) {
        if (error.errorNumber === -1743) throw error;
    }
    // An alternate composed projection still retrieves one batch of plain records.
    // Do not flatten subtask ancestry into list membership: doing so hides cascaded deletion.
    try {
        var records = app.reminders.container.properties();
        if (Array.isArray(records) && records.length === ids.length && records.every(function (record) {
            return record && typeof record.id === 'string' && record.id.length > 0;
        })) return records.map(function (record) { return record.id; });
    } catch (propertiesError) {
        if (propertiesError.errorNumber === -1743) throw propertiesError;
    }
    syncFailure('macos_snapshot_invalid', 'Cannot batch-read raw reminder containers; refusing to guess mutation scope');
}

function buildAncestry(byId, knownLists) {
    // Resolve each edge once, without recursion or storing every node's full ancestor path.
    var resolved = Object.create(null);
    var visiting = Object.create(null);
    var order = [];
    var maxDepth = 0;
    Object.keys(byId).forEach(function (id) {
        if (resolved[id]) return;
        var path = [];
        var next = id;
        while (!knownLists[next] && !resolved[next]) {
            if (!next || visiting[next] || !byId[next]) {
                syncFailure('macos_snapshot_invalid', 'Cannot establish reminder ancestry: ' + id);
            }
            visiting[next] = true;
            path.push(next);
            next = byId[next].containerId;
        }
        var parent = resolved[next] || {listId: next, depth: -1};
        while (path.length) {
            var current = path.pop();
            var entry = {listId: parent.listId, depth: parent.depth + 1};
            resolved[current] = entry;
            visiting[current] = false;
            order.push(byId[current]);
            if (entry.depth > maxDepth) maxDepth = entry.depth;
            parent = entry;
        }
    });
    return {nodes: resolved, order: order, maxDepth: maxDepth};
}

function inList(row, listId, ancestry) {
    return !!(listId && row && ancestry[row.id] && ancestry[row.id].listId === listId);
}

function readBatchSnapshot(app, namespace, listName) {
    var lists = readListIndex(app, listName);
    var arrays = Object.create(null);
    SNAPSHOT_FIELDS.forEach(function (field) { arrays[field] = app.reminders[field](); });
    var ids = arrays.id;
    if (!Array.isArray(ids) || !SNAPSHOT_FIELDS.every(function (field) {
        return Array.isArray(arrays[field]) && arrays[field].length === ids.length;
    })) syncFailure('macos_snapshot_unstable', 'Reminder membership changed during batch read');
    var containers = readContainerIds(app, ids);
    var finalModified = app.reminders.modificationDate();
    var finalIds = app.reminders.id();
    if (!Array.isArray(finalIds) || finalIds.length !== ids.length || !ids.every(function (id, index) {
        return finalIds[index] === id;
    })) syncFailure('macos_snapshot_unstable', 'Reminder order changed during batch read');
    if (!Array.isArray(finalModified) || finalModified.length !== ids.length || !ids.every(function (id, index) {
        return sameInstant(isoDate(arrays.modificationDate[index]), isoDate(finalModified[index]));
    })) syncFailure('macos_snapshot_unstable', 'Reminder fields changed during batch read');
    var finalLists = readListIndex(app, listName);
    if (finalLists.ids.length !== lists.ids.length || !lists.ids.every(function (id, index) {
        return finalLists.ids[index] === id && finalLists.names[index] === lists.names[index];
    })) syncFailure('macos_snapshot_unstable', 'List membership changed during batch read');
    var byId = Object.create(null);
    var rows = ids.map(function (id, index) {
        if (typeof id !== 'string' || !id || byId[id] || lists.known[id]) {
            syncFailure('macos_snapshot_invalid', 'Invalid or duplicate native reminder identifier');
        }
        var allDay = arrays.alldayDueDate[index];
        var due = arrays.dueDate[index];
        var deadline = snapshotDeadline(due, allDay, arrays.remindMeDate[index]);
        var row = {id: id, containerId: containers[index], name: arrays.name[index],
            body: arrays.body[index] || '', priority: arrays.priority[index],
            flagged: arrays.flagged[index], completed: arrays.completed[index],
            completionDate: isoDate(arrays.completionDate[index]),
            modificationDate: isoDate(arrays.modificationDate[index]),
            due: deadline.due, remindMeDate: deadline.remindMeDate,
            creationDate: isoDate(arrays.creationDate[index])};
        if (typeof row.name !== 'string' || typeof row.body !== 'string' ||
                typeof row.completed !== 'boolean' || typeof row.flagged !== 'boolean' ||
                typeof row.priority !== 'number' || row.priority < 0 || row.priority > 9) {
            syncFailure('macos_snapshot_invalid', 'Invalid native reminder fields: ' + id);
        }
        byId[id] = row;
        return row;
    });
    var ancestry = buildAncestry(byId, lists.known);
    var visible = rows.filter(function (row) {
        return inList(row, lists.target, ancestry.nodes) || taskFromMarker(row.body, namespace) !== null;
    });
    return {snapshot: {listId: lists.target, reminders: visible}, rows: rows, byId: byId,
        knownLists: lists.known, ancestry: ancestry.nodes, ancestorOrder: ancestry.order, maxDepth: ancestry.maxDepth};
}

var NATIVE_TIMINGS = {nativeReadMs: 0, nativeReadCount: 0, nativeWriteMs: 0, nativeVerificationMs: 0};

function batchSnapshot(app, namespace, listName) {
    var started = Date.now();
    try { return readBatchSnapshot(app, namespace, listName); }
    finally {
        NATIVE_TIMINGS.nativeReadMs += Date.now() - started;
        NATIVE_TIMINGS.nativeReadCount += 1;
    }
}


function changesFor(row, item) {
    var changes = {};
    ['name', 'body', 'priority', 'flagged', 'completed'].forEach(function (key) {
        if (row[key] !== item[key]) changes[key] = item[key];
    });
    if (item.due.kind === 'timed') {
        var at = new Date(item.due.at);
        if (row.due.kind === 'allDay') changes.alldayDueDate = null;
        if (row.due.kind !== 'timed' || !sameInstant(row.due.at, item.due.at)) changes.dueDate = at;
        if (!sameInstant(row.remindMeDate, item.due.at)) changes.remindMeDate = at;
    } else if (item.due.kind === 'allDay') {
        if (row.due.kind !== 'allDay' || row.due.date !== item.due.date) {
            if (row.due.kind === 'timed') changes.dueDate = null;
            changes.alldayDueDate = dayDate(item.due.date);
        }
        if (row.remindMeDate !== null) changes.remindMeDate = null;
    } else {
        if (row.due.kind !== 'none') changes.dueDate = null;
        if (row.due.kind === 'allDay') changes.alldayDueDate = null;
        if (row.remindMeDate !== null) changes.remindMeDate = null;
    }
    return changes;
}

function applyChanges(reminder, changes) {
    // Complete before moving alarms; reopen only after all other property setters.
    if (changes.completed === true) reminder.completed = true;
    ['dueDate', 'alldayDueDate', 'remindMeDate'].forEach(function (key) {
        if (changes[key] === null) reminder[key] = null;
    });
    ['name', 'body', 'priority', 'flagged', 'dueDate', 'alldayDueDate',
        'remindMeDate', 'completed'].forEach(function (key) {
        if (changes[key] === null || (key === 'completed' && changes.completed === true)) return;
        if (own(changes, key)) reminder[key] = changes[key];
    });
}

function creationFields(item) {
    var fields = {};
    ['name', 'body', 'priority', 'flagged', 'completed'].forEach(function (key) { fields[key] = item[key]; });
    if (item.due.kind === 'timed') {
        fields.dueDate = new Date(item.due.at);
        fields.remindMeDate = new Date(item.due.at);
    } else if (item.due.kind === 'allDay') {
        fields.alldayDueDate = dayDate(item.due.date);
    }
    return fields;
}

function preflight(request, native) {
    if (typeof request.listId !== 'string' || !request.listId ||
            native.snapshot.listId !== request.listId || !Array.isArray(request.operations)) {
        syncFailure('macos_list_conflict', 'The bound native list is missing or changed');
    }
    if (own(request, 'initializationMarkers')) {
        if (!Array.isArray(request.initializationMarkers)) {
            syncFailure('invalid_request', 'Invalid initialization markers');
        }
        var allowed = Object.create(null);
        request.initializationMarkers.forEach(function (marker) {
            if (typeof marker !== 'string' || firstLine(marker) !== marker ||
                    !taskFromMarker(marker, request.namespace) || allowed[marker]) {
                syncFailure('invalid_request', 'Invalid initialization marker');
            }
            allowed[marker] = true;
        });
        native.rows.forEach(function (row) {
            if (inList(row, request.listId, native.ancestry) && !allowed[firstLine(row.body)]) {
                syncFailure('initialization_target_not_empty', 'Unowned content appeared during initialization; preserve it');
            }
        });
        if (request.operations.some(function (op) { return !op || op.action === 'delete'; })) {
            syncFailure('invalid_request', 'Initialization never deletes native content');
        }
    }
    var deleteIds = Object.create(null);
    var touchedIds = Object.create(null);
    var touchedTasks = Object.create(null);
    request.operations.forEach(function (op) {
        if (!op || ['delete', 'create', 'update'].indexOf(op.action) === -1) {
            syncFailure('invalid_request', 'Invalid native operation');
        }
        if (op.action !== 'delete') {
            validateItem(op.item, request.namespace, op.taskId);
            if (own(request, 'initializationMarkers') && !allowed[op.item.marker]) {
                syncFailure('invalid_request', 'Operation is outside the initialization task set');
            }
            if (touchedTasks[op.taskId]) syncFailure('invalid_request', 'Duplicate requested task: ' + op.taskId);
            touchedTasks[op.taskId] = true;
        }
        if (op.action !== 'create') {
            if (typeof op.id !== 'string' || !op.id || touchedIds[op.id] || !own(op, 'expectedModified') ||
                    (op.expectedModified !== null && (typeof op.expectedModified !== 'string' ||
                        !isFinite(new Date(op.expectedModified).getTime())))) {
                syncFailure('invalid_request', 'Missing or invalid native mutation precondition');
            }
            touchedIds[op.id] = true;
            var row = native.byId[op.id];
            if (!row || !inList(row, request.listId, native.ancestry) ||
                    !sameInstant(row.modificationDate, op.expectedModified)) {
                syncFailure('macos_native_conflict', 'Reminder changed, moved or disappeared: ' + op.id);
            }
            if (op.action === 'update' && firstLine(row.body) !== op.item.marker) {
                syncFailure('macos_task_conflict', 'Update identifier does not match the exact first-line task marker');
            }
            if (op.action === 'delete') {
                if (op.allowUnmarked !== true && !taskFromMarker(row.body, request.namespace)) {
                    syncFailure('macos_task_conflict', 'Deleting an unowned item requires explicit initialization permission');
                }
                deleteIds[op.id] = true;
            }
        }
    });
    var deletedAbove = Object.create(null);
    native.ancestorOrder.forEach(function (row) {
        var ancestorDeleted = !!(deleteIds[row.containerId] || deletedAbove[row.containerId]);
        deletedAbove[row.id] = ancestorDeleted;
        if (!deleteIds[row.id] && ancestorDeleted) {
            syncFailure('macos_task_conflict', 'Deleting a parent requires explicit descendant IDs: ' + row.id);
        }
    });
    var markers = Object.create(null);
    native.rows.forEach(function (row) {
        if (deleteIds[row.id]) return;
        var taskId = taskFromMarker(row.body, request.namespace);
        if (!taskId) return;
        if (markers[taskId]) syncFailure('macos_task_conflict', 'Duplicate native task marker: ' + taskId);
        markers[taskId] = row;
    });
    return request.operations.map(function (op) {
        if (op.action === 'delete') return {op: op, row: native.byId[op.id]};
        var row = op.action === 'update' ? native.byId[op.id] : markers[op.taskId];
        if (op.action === 'create' && row) {
            if (!inList(row, request.listId, native.ancestry) ||
                    Object.keys(changesFor(row, op.item)).length) {
                syncFailure('macos_task_conflict', 'A create marker already exists; read and replan: ' + op.taskId);
            }
            return {op: op, row: row, changes: {}, recovered: true};
        }
        return {op: op, row: row || null, changes: row ? changesFor(row, op.item) : null};
    });
}

function resolveResults(results, native, namespace) {
    var markerRows = Object.create(null);
    native.rows.forEach(function (row) {
        var taskId = taskFromMarker(row.body, namespace);
        if (taskId && !markerRows[taskId]) markerRows[taskId] = row;
    });
    results.forEach(function (entry) {
        if (entry.action === 'create' && !entry.id && markerRows[entry.taskId]) entry.id = markerRows[entry.taskId].id;
    });
}

function verifyPlan(plan, native, namespace) {
    var markerRows = Object.create(null);
    native.rows.forEach(function (row) {
        var taskId = taskFromMarker(row.body, namespace);
        if (!taskId) return;
        if (markerRows[taskId]) syncFailure('macos_task_conflict', 'Duplicate marker after native write: ' + taskId);
        markerRows[taskId] = row;
    });
    plan.forEach(function (entry) {
        var op = entry.op;
        if (op.action === 'delete') {
            if (native.byId[op.id]) syncFailure('macos_verification_failed', 'Deleted reminder still exists: ' + op.id);
            return;
        }
        var row = op.action === 'update' ? native.byId[op.id] : markerRows[op.taskId];
        if (!row || !inList(row, native.snapshot.listId, native.ancestry) ||
                firstLine(row.body) !== op.item.marker || Object.keys(changesFor(row, op.item)).length) {
            syncFailure('macos_verification_failed', 'Reminders did not retain all fields for ' + op.taskId);
        }
    });
}

function dispatch(request, app) {
    NATIVE_TIMINGS = {nativeReadMs: 0, nativeReadCount: 0, nativeWriteMs: 0, nativeVerificationMs: 0};
    var result = {ok: false, code: 'macos_sync_error', results: [], partial: false};
    var native = null;
    var mutationStarted = false;
    var finalReadAttempted = false;
    try {
        if (!request || typeof request.listName !== 'string' || !request.listName.trim() ||
                /[\x00-\x1f\x7f-\x9f]/.test(request.listName) ||
                !/^[a-f0-9]{64}$/.test(request.namespace) ||
                ['read', 'probe', 'ensure_list', 'apply'].indexOf(request.mode) === -1) {
            syncFailure('invalid_request', 'Invalid Reminders bridge request');
        }
        if (request.mode === 'probe') {
            var probeStarted = Date.now();
            NATIVE_TIMINGS.nativeProbeCount = 1;
            try { result.snapshot = {listId: readListIndex(app, request.listName).target}; }
            finally { NATIVE_TIMINGS.nativeReadMs += Date.now() - probeStarted; }
            result.ok = true;
            result.code = 'native_probe';
            result.timings = NATIVE_TIMINGS;
            return result;
        }
        native = batchSnapshot(app, request.namespace, request.listName);
        result.snapshot = native.snapshot;
        if (request.mode === 'ensure_list' && !native.snapshot.listId) {
            mutationStarted = true;
            app.defaultAccount().lists.push(app.List({name: request.listName}));
            finalReadAttempted = true;
            delete result.snapshot;
            native = batchSnapshot(app, request.namespace, request.listName);
            result.snapshot = native.snapshot;
            if (!native.snapshot.listId) syncFailure('macos_list_conflict', 'Cannot resolve the newly created list');
            result.listCreated = true;
        } else if (request.mode === 'apply') {
            var plan = preflight(request, native);
            // Deletes first permit explicit initialization to replace existing owned markers.
            var deletionsByDepth = [];
            plan.forEach(function (entry) {
                if (entry.op.action !== 'delete') return;
                var depth = native.ancestry[entry.row.id].depth;
                if (!deletionsByDepth[depth]) deletionsByDepth[depth] = [];
                deletionsByDepth[depth].push(entry);
            });
            // Cocoa deletion can cascade to subtasks. Depth buckets keep child-first order linear.
            var ordered = [];
            for (var depth = native.maxDepth; depth >= 0; depth -= 1) {
                if (deletionsByDepth[depth]) deletionsByDepth[depth].forEach(function (entry) { ordered.push(entry); });
            }
            ordered = ordered.concat(plan.filter(function (entry) { return entry.op.action !== 'delete'; }));
            var writeStarted = Date.now();
            try {
                ordered.forEach(function (entry) {
                    var op = entry.op;
                    if (op.action === 'delete') {
                        mutationStarted = true;
                        app.delete(app.reminders.byId(op.id));
                        result.results.push({action: 'delete', id: op.id});
                    } else if (op.action === 'create' && !entry.row) {
                        mutationStarted = true;
                        // Marker and all requested fields are part of the creation AppleEvent.
                        app.lists.byId(request.listId).reminders.push(app.Reminder(creationFields(op.item)));
                        result.results.push({action: 'create', taskId: op.taskId, id: null});
                    } else {
                        if (Object.keys(entry.changes).length) {
                            mutationStarted = true;
                            applyChanges(app.reminders.byId(entry.row.id), entry.changes);
                        }
                        result.results.push({action: op.action, taskId: op.taskId, id: entry.row.id});
                    }
                });
            } finally { NATIVE_TIMINGS.nativeWriteMs += Date.now() - writeStarted; }
            finalReadAttempted = true;
            delete result.snapshot;
            native = batchSnapshot(app, request.namespace, request.listName);
            result.snapshot = native.snapshot;
            resolveResults(result.results, native, request.namespace);
            if (native.snapshot.listId !== request.listId) syncFailure('macos_list_conflict', 'Bound list changed during native write');
            var verifyStarted = Date.now();
            try { verifyPlan(plan, native, request.namespace); }
            finally { NATIVE_TIMINGS.nativeVerificationMs += Date.now() - verifyStarted; }
        }
        result.ok = true;
        result.code = 'ok';
    } catch (error) {
        result.code = error.syncCode || (error.errorNumber === -1743 ? 'macos_permission_denied' : 'macos_sync_error');
        result.message = String(error.message || error);
        result.partial = mutationStarted;
        if (mutationStarted && !finalReadAttempted) {
            try {
                native = batchSnapshot(app, request.namespace, request.listName);
                result.snapshot = native.snapshot;
                resolveResults(result.results, native, request.namespace);
            } catch (snapshotError) {
                // The preflight snapshot is stale after a possible write, so do not return it as current.
                delete result.snapshot;
                result.snapshotError = String(snapshotError.message || snapshotError);
            }
        }
    }
    result.timings = NATIVE_TIMINGS;
    return result;
}

function run(argv) {
    try {
        if (argv.length !== 1) syncFailure('invalid_request', 'Exactly one request file is required');
        ObjC.import('Foundation');
        var error = Ref();
        var data = $.NSString.stringWithContentsOfFileEncodingError(argv[0], $.NSUTF8StringEncoding, error);
        if (!data) syncFailure('invalid_request', 'Cannot read request JSON');
        var request = JSON.parse(ObjC.unwrap(data));
        return JSON.stringify(dispatch(request, Application('com.apple.reminders')));
    } catch (error) {
        return JSON.stringify({ok: false, code: error.syncCode || 'macos_bridge_error', partial: false,
            message: String(error.message || error)});
    }
}
