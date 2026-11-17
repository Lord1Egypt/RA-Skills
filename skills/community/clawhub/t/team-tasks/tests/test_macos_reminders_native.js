#!/usr/bin/env node
'use strict';

// Offline JXA stand-in: batch collections expose array projections, scalar reads fail.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const context = vm.createContext({Date});
vm.runInContext(fs.readFileSync(path.join(__dirname, '../scripts/macos_reminders.js'), 'utf8'), context);
const LIST_NAME = '团队待办（team-tasks）';
const NAMESPACE = 'a'.repeat(64);
const OTHER_NAMESPACE = 'b'.repeat(64);
const FIELDS = ['id', 'name', 'body', 'priority', 'flagged', 'completed', 'completionDate',
    'modificationDate', 'dueDate', 'alldayDueDate', 'remindMeDate', 'creationDate'];
const plain = value => JSON.parse(JSON.stringify(value));

function item(number = 1, overrides = {}, namespace = NAMESPACE) {
    const taskId = `T-261013-${String(number).padStart(3, '0')}`;
    const marker = `[team-tasks:v1:${namespace}:${taskId}]`;
    return {taskId, marker, name: `事项 ${number}`, body: `${marker}\n负责人：老王\n描述：跟进事项`,
        priority: 5, flagged: false, completed: false, due: {kind: 'none'}, ...overrides};
}
function request(mode, extras = {}, namespace = NAMESPACE) {
    return {mode, listName: LIST_NAME, namespace, ...extras};
}
function nativeFields(task) {
    const fields = Object.fromEntries(['name', 'body', 'priority', 'flagged', 'completed'].map(key => [key, task[key]]));
    fields.dueDate = null;
    fields.alldayDueDate = null;
    fields.remindMeDate = null;
    if (task.due.kind === 'timed') {
        fields.dueDate = new Date(task.due.at);
        fields.remindMeDate = new Date(task.due.at);
    } else if (task.due.kind === 'allDay') {
        const [year, month, day] = task.due.date.split('-').map(Number);
        fields.alldayDueDate = new Date(year, month - 1, day, 12);
        fields.dueDate = fields.alldayDueDate;
    }
    return fields;
}

function fakeApplication(seeds = [], options = {}) {
    const lists = [];
    const states = new Map();
    const writes = [];
    const reads = Object.create(null);
    let reminderCounter = 0;
    let listCounter = 0;
    let clock = Date.parse('2026-10-13T01:00:00Z');
    let failingField = null;
    let failAfterCreate = false;
    let failAfterDelete = false;
    let ignoreNextField = null;
    let failContainerProjection = false;
    let failAllContainerProjections = false;
    let denyReads = false;
    let reorderLastIds = false;
    let changeDuringRead = false;
    let denyAfterCreateRead = false;
    function readCount(key) {
        reads[key] = (reads[key] || 0) + 1;
        if (denyReads) {
            const error = new Error('Not authorized to send AppleEvents');
            error.errorNumber = -1743;
            throw error;
        }
    }
    function nativeReminder(seed = {}, listId) {
        const state = {name: '', body: '', priority: 0, flagged: false, completed: false,
            dueDate: null, alldayDueDate: null, remindMeDate: null, completionDate: null,
            modificationDate: new Date(clock), creationDate: new Date(clock),
            containerId: listId, ...seed, id: seed.id || `R-${++reminderCounter}`};
        if (state.completed && !state.completionDate) state.completionDate = new Date(clock);
        if (state.alldayDueDate && !state.dueDate) state.dueDate = state.alldayDueDate;
        if (options.normalizeDates) {
            if (state.alldayDueDate) {
                const day = state.alldayDueDate;
                state.alldayDueDate = new Date(day.getFullYear(), day.getMonth(), day.getDate());
                state.dueDate = new Date(state.alldayDueDate);
                state.remindMeDate = new Date(state.alldayDueDate);
            } else if (state.dueDate) {
                const due = state.dueDate;
                state.alldayDueDate = new Date(due.getFullYear(), due.getMonth(), due.getDate());
                state.remindMeDate = new Date(due);
            }
        }
        states.set(state.id, state);
        const reminder = {nativeId: state.id};
        for (const field of FIELDS) Object.defineProperty(reminder, field, {
            get: () => { throw new Error(`Forbidden per-object native getter: ${field}`); },
            set: value => {
                writes.push({op: 'set', id: state.id, field, value: plain(value)});
                if (failingField === field) { failingField = null; throw new Error(`Simulated write failure: ${field}`); }
                if (ignoreNextField === field) { ignoreNextField = null; return; }
                state[field] = value;
                state.modificationDate = new Date(++clock);
                if (field === 'dueDate') state.alldayDueDate = null;
                if (field === 'alldayDueDate') state.dueDate = value;
                if (field === 'completed') state.completionDate = value ? new Date(clock) : null;
            }
        });
        return reminder;
    }
    function isMember(state, listId) {
        let current = state.containerId;
        const seen = new Set();
        while (current) {
            if (current === listId) return true;
            if (seen.has(current) || !states.has(current)) return false;
            seen.add(current);
            current = states.get(current).containerId;
        }
        return false;
    }
    function collection(getStates, scope, allowPush) {
        const coll = () => { throw new Error('Per-object enumeration is forbidden'); };
        for (const field of FIELDS) Object.defineProperty(coll, field, {value: () => {
            readCount(`${scope}.${field}`);
            const result = getStates().map(state => state[field]);
            if (changeDuringRead && scope === 'reminders' && field === 'completed') {
                changeDuringRead = false;
                getStates()[0].completed = true;
                getStates()[0].completionDate = new Date(clock + 1);
                getStates()[0].modificationDate = new Date(++clock);
            }
            if (reorderLastIds && scope === 'reminders' && field === 'id' && reads['reminders.id'] === 2) result.reverse();
            return result;
        }, configurable: true});
        coll.container = {id: () => {
            readCount(`${scope}.container.id`);
            if (failContainerProjection || failAllContainerProjections) throw new Error('Projection unavailable');
            return getStates().map(state => state.containerId);
        }, properties: () => {
            readCount(`${scope}.container.properties`);
            if (failAllContainerProjections) throw new Error('Projection unavailable');
            return getStates().map(state => ({id: state.containerId}));
        }};
        coll.byId = id => {
            const state = states.get(id);
            if (!state) throw new Error(`Missing specifier ${id}`);
            return state.ref;
        };
        if (allowPush) coll.push = allowPush;
        return coll;
    }
    function nativeList(seed) {
        const list = {nativeId: seed.id || `L-${++listCounter}`, nativeName: seed.name};
        list.reminders = collection(() => [...states.values()].filter(state => isMember(state, list.nativeId)),
            `list:${list.nativeId}`, draft => {
                assert.equal(draft.type, 'reminder-draft');
                const ref = nativeReminder(draft.fields, list.nativeId);
                states.get(ref.nativeId).ref = ref;
                writes.push({op: 'create-reminder', id: ref.nativeId, listId: list.nativeId,
                    marker: draft.fields.body.split('\n')[0]});
                if (denyAfterCreateRead) { denyAfterCreateRead = false; denyReads = true; }
                if (failAfterCreate) { failAfterCreate = false; throw new Error('Lost response after create'); }
            });
        for (const seedReminder of seed.reminders || []) {
            const ref = nativeReminder(seedReminder, list.nativeId);
            states.get(ref.nativeId).ref = ref;
        }
        return list;
    }
    for (const seed of seeds) lists.push(nativeList(seed));
    const app = {
        lists: {
            id: () => { readCount('lists.id'); return lists.map(list => list.nativeId); },
            name: () => { readCount('lists.name'); return lists.map(list => list.nativeName); },
            byId: id => {
                const list = lists.find(candidate => candidate.nativeId === id);
                if (!list) throw new Error(`Missing list ${id}`);
                return list;
            }
        },
        reminders: collection(() => [...states.values()], 'reminders'),
        List: fields => ({type: 'list-draft', fields}),
        Reminder: fields => ({type: 'reminder-draft', fields}),
        defaultAccount: () => ({lists: {push: draft => {
            assert.equal(draft.type, 'list-draft');
            const list = nativeList(draft.fields);
            lists.push(list);
            writes.push({op: 'create-list', id: list.nativeId, name: list.nativeName});
        }}}),
        delete: specifier => {
            assert.ok(specifier.nativeId, 'Delete must use app.delete(object specifier)');
            assert.ok(states.has(specifier.nativeId), 'Deletion of an already cascaded child would fail');
            const cascaded = [...states.values()].filter(state =>
                state.id === specifier.nativeId || isMember(state, specifier.nativeId));
            for (const state of cascaded) states.delete(state.id);
            writes.push({op: 'delete-reminder', id: specifier.nativeId});
            if (failAfterDelete) { failAfterDelete = false; throw new Error('Lost response after delete'); }
        }
    };
    return {app, lists, reads, writes, states,
        failNextSetter: field => { failingField = field; },
        failAfterNextCreate: () => { failAfterCreate = true; },
        failAfterNextDelete: () => { failAfterDelete = true; },
        ignoreNextSetter: field => { ignoreNextField = field; },
        disableProjection: () => { failContainerProjection = true; },
        disableContainerReads: () => { failAllContainerProjections = true; },
        denyReads: () => { denyReads = true; },
        reorderRead: () => { reorderLastIds = true; },
        changeRead: () => { changeDuringRead = true; },
        denyAfterNextCreateRead: () => { denyAfterCreateRead = true; },
        get: id => plain({...states.get(id), ref: undefined}),
        targetList: () => lists.find(list => list.nativeName === LIST_NAME),
        taskState: task => [...states.values()].find(state => state.body.split('\n')[0] === task.marker)};
}
const call = (fake, payload) => plain(context.dispatch(payload, fake.app));
const read = fake => call(fake, request('read'));
function apply(fake, operations) {
    return call(fake, request('apply', {listId: fake.targetList().nativeId, operations}));
}
const createOp = task => ({action: 'create', taskId: task.taskId, item: task});
function updateOp(fake, task) {
    const state = fake.taskState(task);
    return {action: 'update', taskId: task.taskId, id: state.id,
        expectedModified: state.modificationDate ? state.modificationDate.toISOString() : null, item: task};
}
function assertItem(fake, task) {
    const state = fake.taskState(task);
    assert.ok(state);
    const actual = Object.fromEntries(Object.keys(nativeFields(task)).map(key => [key, state[key]]));
    assert.deepEqual(plain(actual), plain(nativeFields(task)));
}
const tests = [];
function test(name, run) { tests.push({name, run}); }

test('read is nonmutating and includes completed, unmarked target and moved own items only', () => {
    const active = item(), complete = item(2, {completed: true}), moved = item(3);
    const fake = fakeApplication([
        {name: LIST_NAME, reminders: [nativeFields(active), nativeFields(complete), {name: '手工事项', body: ''}]},
        {name: '个人事项', reminders: [nativeFields(moved), nativeFields(item(4, {}, OTHER_NAMESPACE)), {name: '私事'}]}
    ]);
    const result = read(fake);
    assert.equal(result.ok, true, result.message);
    assert.equal(result.snapshot.listId, fake.targetList().nativeId);
    assert.equal(result.snapshot.reminders.length, 4);
    assert.ok(result.snapshot.reminders.find(row => row.name === complete.name).completionDate);
    assert.notEqual(result.snapshot.reminders.find(row => row.name === moved.name).containerId, result.snapshot.listId);
    assert.deepEqual(fake.writes, []);
});
test('array getter count stays constant for one versus 500 reminders', () => {
    const run = count => {
        const fake = fakeApplication([{name: LIST_NAME,
            reminders: Array.from({length: count}, (_, index) => nativeFields(item(index + 1)))}]);
        assert.equal(read(fake).snapshot.reminders.length, count);
        return plain(fake.reads);
    };
    assert.deepEqual(run(1), run(500));
});
test('deep ancestry, membership and deletion protection visit only linear parent edges', () => {
    const count = 20000;
    const byId = Object.create(null);
    let parentReads = 0;
    // Start at the deepest child to exercise path memoization without a recursion limit.
    for (let index = count - 1; index >= 0; index--) {
        const row = {id: `DEEP-${index}`, name: `事项 ${index}`, body: '', modificationDate: null};
        Object.defineProperty(row, 'containerId', {get: () => {
            parentReads += 1;
            return index ? `DEEP-${index - 1}` : 'L-TARGET';
        }});
        byId[row.id] = row;
    }
    const ancestry = context.buildAncestry(byId, {'L-TARGET': true});
    assert.equal(parentReads, count, 'Every raw parent edge is resolved exactly once');
    assert.equal(ancestry.maxDepth, count - 1);
    assert.equal(ancestry.order[0].id, 'DEEP-0');
    assert.equal(ancestry.order.at(-1).id, `DEEP-${count - 1}`);
    for (const row of Object.values(byId)) assert.equal(context.inList(row, 'L-TARGET', ancestry.nodes), true);
    assert.equal(parentReads, count, 'Membership must use the index without walking any parent edge');
    const native = {snapshot: {listId: 'L-TARGET'}, byId, rows: Object.values(byId),
        ancestry: ancestry.nodes, ancestorOrder: ancestry.order};
    const operations = Object.values(byId).map(row => ({action: 'delete', id: row.id,
        expectedModified: null, allowUnmarked: true}));
    const plan = context.preflight(request('apply', {listId: 'L-TARGET', operations}), native);
    assert.equal(plan.length, count);
    assert.ok(parentReads <= count * 3, 'Delete scope propagation must remain linear for deep parent chains');
});
test('unsupported container ID projection falls back to batch plain records, never per item', () => {
    const run = count => {
        const fake = fakeApplication([{name: LIST_NAME,
            reminders: Array.from({length: count}, (_, index) => nativeFields(item(index + 1)))}]);
        fake.disableProjection();
        const result = read(fake);
        assert.equal(result.ok, true, result.message);
        assert.equal(result.snapshot.reminders.length, count);
        return plain(fake.reads);
    };
    assert.deepEqual(run(1), run(500));
});
test('unknown raw container scope fails closed instead of flattening or guessing parents', () => {
    const fake = fakeApplication([{name: LIST_NAME, reminders: [{name: '手工事项'}]}]);
    fake.disableContainerReads();
    const result = apply(fake, [createOp(item())]);
    assert.equal(result.ok, false);
    assert.equal(result.code, 'macos_snapshot_invalid');
    assert.equal(result.partial, false);
    assert.deepEqual(fake.writes, []);
});
test('orphan and cyclic raw ancestors fail closed before initialization or updates', () => {
    for (const reminders of [[{id: 'ORPHAN', containerId: 'MISSING', name: '孤项'}],
        [{id: 'PARENT', containerId: 'CHILD', name: '父'}, {id: 'CHILD', containerId: 'PARENT', name: '子'}]]) {
        const fake = fakeApplication([{name: LIST_NAME, reminders}]);
        assert.equal(read(fake).code, 'macos_snapshot_invalid');
        assert.deepEqual(fake.writes, []);
    }
});
test('read absent list does not create it; ensure creates once and preserves its ID', () => {
    const fake = fakeApplication();
    assert.deepEqual(read(fake).snapshot, {listId: null, reminders: []});
    assert.equal(fake.writes.length, 0);
    const first = call(fake, request('ensure_list'));
    assert.equal(first.ok, true, first.message);
    assert.equal(first.listCreated, true);
    const second = call(fake, request('ensure_list'));
    assert.equal(second.ok, true);
    assert.equal(second.snapshot.listId, first.snapshot.listId);
    assert.equal(fake.writes.length, 1);
});
test('duplicate exact list names fail all modes before writes', () => {
    for (const mode of ['read', 'ensure_list', 'apply']) {
        const fake = fakeApplication([{name: LIST_NAME}, {name: LIST_NAME}]);
        const result = call(fake, request(mode, {listId: 'L-1', operations: [createOp(item())]}));
        assert.equal(result.ok, false);
        assert.equal(result.code, 'macos_list_conflict');
        assert.equal(result.partial, false);
        assert.deepEqual(fake.writes, []);
    }
});
test('batch creates all fields and returns IDs with constant array-read count', () => {
    const run = count => {
        const fake = fakeApplication([{name: LIST_NAME}]);
        const tasks = Array.from({length: count}, (_, index) => item(index + 1, {
            completed: index % 2 === 0, flagged: index % 3 === 0, priority: [1, 5, 9][index % 3],
            due: index % 3 === 0 ? {kind: 'timed', at: '2026-10-14T09:30:00+08:00'} :
                (index % 3 === 1 ? {kind: 'allDay', date: '2026-10-15'} : {kind: 'none'})
        }));
        const result = apply(fake, tasks.map(createOp));
        assert.equal(result.ok, true, result.message);
        assert.equal(result.results.length, count);
        assert.equal(new Set(result.results.map(row => row.id)).size, count);
        assert.ok(result.results.every(row => typeof row.id === 'string' && row.id));
        for (const task of tasks) assertItem(fake, task);
        return plain(fake.reads);
    };
    assert.deepEqual(run(1), run(500));
});
test('macOS-filled neighboring date fields round-trip timed and all-day creations', () => {
    const timed = item(1, {due: {kind: 'timed', at: '2026-10-14T09:30:00+08:00'}});
    const allDay = item(2, {due: {kind: 'allDay', date: '2026-10-15'}});
    const none = item(3);
    const fake = fakeApplication([{name: LIST_NAME}], {normalizeDates: true});
    const result = apply(fake, [createOp(timed), createOp(allDay), createOp(none)]);
    assert.equal(result.ok, true, result.message);
    const rows = result.snapshot.reminders;
    assert.deepEqual(plain(rows.find(row => row.name === timed.name).due),
        {kind: 'timed', at: new Date(timed.due.at).toISOString()});
    assert.deepEqual(plain(rows.find(row => row.name === allDay.name).due), allDay.due);
    assert.equal(rows.find(row => row.name === allDay.name).remindMeDate, null);
    assert.deepEqual(plain(rows.find(row => row.name === none.name).due), none.due);
    assert.equal(fake.get(fake.taskState(timed).id).alldayDueDate !== null, true);
    assert.equal(fake.get(fake.taskState(allDay).id).remindMeDate !== null, true);
});
test('different all-day reminder time remains visible for verification', () => {
    const allDay = item(1, {due: {kind: 'allDay', date: '2026-10-15'}});
    const fields = nativeFields(allDay);
    fields.remindMeDate = new Date('2026-10-15T09:00:00+08:00');
    const fake = fakeApplication([{name: LIST_NAME, reminders: [fields]}]);
    const row = read(fake).snapshot.reminders[0];
    assert.equal(row.remindMeDate, fields.remindMeDate.toISOString());
});
test('update all user fields, complete, reopen and date transitions', () => {
    const original = item();
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(original)]}]);
    const changed = {...original, name: '新标题', body: `${original.marker}\n负责人：李四`, priority: 1,
        flagged: true, completed: true, due: {kind: 'timed', at: '2026-10-16T18:45:00+08:00'}};
    assert.equal(apply(fake, [updateOp(fake, changed)]).ok, true);
    assertItem(fake, changed);
    assert.equal(fake.writes[0].field, 'completed');
    const deadlines = [{kind: 'allDay', date: '2026-10-17'}, {kind: 'allDay', date: '2026-10-18'},
        {kind: 'none'}, {kind: 'timed', at: '2026-10-19T16:00:00+08:00'}, {kind: 'none'},
        {kind: 'allDay', date: '2026-10-20'}, {kind: 'none'}];
    for (const due of deadlines) {
        const next = {...changed, due};
        const result = apply(fake, [updateOp(fake, next)]);
        assert.equal(result.ok, true, result.message);
        assertItem(fake, next);
        const before = fake.writes.length;
        assert.equal(apply(fake, [updateOp(fake, next)]).ok, true);
        assert.equal(fake.writes.length, before);
    }
    const reopened = {...changed, completed: false, flagged: false, due: {kind: 'allDay', date: '2026-10-21'}};
    assert.equal(apply(fake, [updateOp(fake, reopened)]).ok, true);
    assertItem(fake, reopened);
    assert.equal(fake.writes.at(-1).field, 'completed');
});
test('normal operations preserve manual reminders and other namespaces', () => {
    const task = item(), other = item(1, {name: '另一台账事项'}, OTHER_NAMESPACE);
    const fake = fakeApplication([{name: LIST_NAME, reminders: [{name: '手动', body: '说明'},
        {name: '后面的标记', body: `普通备注\n${task.marker}`}, nativeFields(other)]}]);
    const before = [...fake.states.values()].map(state => fake.get(state.id));
    assert.equal(apply(fake, [createOp(task)]).ok, true);
    for (const original of before) assert.deepEqual(fake.get(original.id), original);
    assertItem(fake, task);
});
test('full batch preflight rejects duplicate markers before any earlier mutation', () => {
    const original = item(), duplicate = item(2);
    const fake = fakeApplication([{name: LIST_NAME,
        reminders: [nativeFields(original), nativeFields(duplicate), nativeFields(duplicate)]}]);
    const result = apply(fake, [updateOp(fake, {...original, name: '不应更新'}), createOp(item(3))]);
    assert.equal(result.ok, false);
    assert.equal(result.code, 'macos_task_conflict');
    assert.equal(result.partial, false);
    assert.deepEqual(fake.writes, []);
});
test('stale modification and wrong ID marker fail before earlier creation', () => {
    const task = item();
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(task)]}]);
    const update = updateOp(fake, {...task, name: '新标题'});
    for (const mutation of [{...update, expectedModified: '2020-01-01T00:00:00Z'},
        {...update, taskId: item(2).taskId, item: item(2)}]) {
        const result = apply(fake, [createOp(item(3)), mutation]);
        assert.equal(result.ok, false);
        assert.equal(result.partial, false);
        assert.deepEqual(fake.writes, []);
    }
});
test('moved items remain visible but cannot be updated, deleted or recreated', () => {
    const task = item();
    const fake = fakeApplication([{name: LIST_NAME}, {name: '个人', reminders: [nativeFields(task)]}]);
    const state = fake.taskState(task);
    assert.equal(read(fake).snapshot.reminders.length, 1);
    for (const operation of [createOp(task), updateOp(fake, task),
        {action: 'delete', id: state.id, expectedModified: state.modificationDate.toISOString(), allowUnmarked: true}]) {
        const result = apply(fake, [operation]);
        assert.equal(result.ok, false);
        assert.deepEqual(fake.writes, []);
    }
});
test('first-line scope guard excludes manual updates and normal deletes', () => {
    const task = item();
    const fake = fakeApplication([{name: LIST_NAME, reminders: [{name: '手工', body: `普通备注\n${task.marker}`}]}]);
    const state = [...fake.states.values()][0];
    const condition = {id: state.id, expectedModified: state.modificationDate.toISOString()};
    for (const operation of [{action: 'update', ...condition, taskId: task.taskId, item: task},
        {action: 'delete', ...condition}]) {
        assert.equal(apply(fake, [operation]).code, 'macos_task_conflict');
        assert.deepEqual(fake.writes, []);
    }
});
test('explicit initialization deletes target entries, including duplicates and manual completed entries', () => {
    const task = item();
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(task), nativeFields(task),
        {name: '手工事项', body: '先快照再删除', completed: true}]},
        {name: '个人事项', reminders: [{name: '保留', body: ''}]}]);
    const operations = read(fake).snapshot.reminders.map(row => ({action: 'delete', id: row.id,
        expectedModified: row.modificationDate, allowUnmarked: true}));
    const result = apply(fake, [createOp(task), ...operations]);
    assert.equal(result.ok, true, result.message);
    assert.equal(result.results.filter(row => row.action === 'delete').length, 3);
    assert.equal(result.snapshot.reminders.length, 1);
    assertItem(fake, task);
    assert.ok([...fake.states.values()].find(state => state.name === '保留'));
});
test('subtasks use raw container IDs and target ancestor membership for read/delete', () => {
    const fake = fakeApplication([{id: 'L-TARGET', name: LIST_NAME, reminders: [
        {id: 'PARENT', name: '父事项'}, {id: 'CHILD', containerId: 'PARENT', name: '子事项'},
        {id: 'GRANDCHILD', containerId: 'CHILD', name: '孙事项'}]},
        {name: '其他', reminders: [{id: 'OTHER-PARENT', name: '其他父项'},
            {...nativeFields(item()), containerId: 'OTHER-PARENT'}]}]);
    const snapshot = read(fake).snapshot;
    assert.equal(snapshot.reminders.length, 4);
    assert.equal(snapshot.reminders.find(row => row.id === 'CHILD').containerId, 'PARENT');
    const row = snapshot.reminders.find(row => row.id === 'GRANDCHILD');
    const result = apply(fake, [{action: 'delete', id: row.id, expectedModified: row.modificationDate, allowUnmarked: true}]);
    assert.equal(result.ok, true, result.message);
    assert.equal(fake.states.has('GRANDCHILD'), false);
});
test('delete guards prevent unrequested descendant loss and explicit children are deleted first', () => {
    const fake = fakeApplication([{name: LIST_NAME, reminders: [
        {id: 'PARENT', name: '父项'}, {id: 'CHILD', containerId: 'PARENT', name: '子项'},
        {id: 'GRANDCHILD', containerId: 'CHILD', name: '孙项'}]}]);
    const rows = read(fake).snapshot.reminders;
    const operations = rows.map(row => ({action: 'delete', id: row.id,
        expectedModified: row.modificationDate, allowUnmarked: true}));
    const unsafe = apply(fake, operations.slice(0, 1));
    assert.equal(unsafe.ok, false);
    assert.equal(unsafe.code, 'macos_task_conflict');
    assert.deepEqual(fake.writes, []);
    const safe = apply(fake, operations);
    assert.equal(safe.ok, true, safe.message);
    assert.deepEqual(fake.writes.map(row => row.id), ['GRANDCHILD', 'CHILD', 'PARENT']);
    assert.equal(safe.snapshot.reminders.length, 0);
});
test('create response loss returns fresh snapshot and retry recovers marker without duplication', () => {
    const task = item(1, {completed: true, due: {kind: 'timed', at: '2026-10-19T11:20:00+08:00'}});
    const fake = fakeApplication([{name: LIST_NAME}]);
    fake.failAfterNextCreate();
    const failed = apply(fake, [createOp(task)]);
    assert.equal(failed.ok, false);
    assert.equal(failed.partial, true);
    assert.equal(failed.snapshot.reminders.length, 1);
    const recovered = apply(fake, [createOp(task)]);
    assert.equal(recovered.ok, true, recovered.message);
    assert.equal(recovered.results[0].id, fake.taskState(task).id);
    assert.equal(fake.states.size, 1);
    assert.equal(fake.writes.length, 1);
    assertItem(fake, task);
});
test('create retry refuses changed existing marker rather than overwriting remote edit', () => {
    const task = item();
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields({...task, completed: true})]}]);
    assert.equal(apply(fake, [createOp(task)]).code, 'macos_task_conflict');
    assert.equal(fake.taskState(task).completed, true);
    assert.deepEqual(fake.writes, []);
});
test('setter failure reports successful operations and current partial snapshot', () => {
    const task = item(), created = item(2);
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(task)]}]);
    fake.failNextSetter('remindMeDate');
    const changed = {...task, name: '更新部分', due: {kind: 'timed', at: '2026-10-20T10:00:00+08:00'}};
    const result = apply(fake, [createOp(created), updateOp(fake, changed)]);
    assert.equal(result.ok, false);
    assert.equal(result.partial, true);
    assert.equal(result.results.length, 1);
    assert.equal(result.results[0].id, fake.taskState(created).id);
    assert.equal(result.snapshot.reminders.length, 2);
    assert.equal(apply(fake, [updateOp(fake, changed)]).ok, true);
    assertItem(fake, changed);
});
test('lost delete response exposes deletion in fresh snapshot and touches no other ID', () => {
    const fake = fakeApplication([{name: LIST_NAME, reminders: [{name: '旧'}, {name: '保留'}]}]);
    const row = read(fake).snapshot.reminders[0];
    fake.failAfterNextDelete();
    const result = apply(fake, [{action: 'delete', id: row.id, expectedModified: row.modificationDate, allowUnmarked: true}]);
    assert.equal(result.ok, false);
    assert.equal(result.partial, true);
    assert.equal(result.snapshot.reminders.length, 1);
    assert.equal(result.snapshot.reminders[0].name, '保留');
});
test('one final batch verifies silent native setter failures', () => {
    const task = item();
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(task)]}]);
    fake.ignoreNextSetter('name');
    const result = apply(fake, [updateOp(fake, {...task, name: '没有保存'})]);
    assert.equal(result.ok, false);
    assert.equal(result.code, 'macos_verification_failed');
    assert.equal(result.partial, true);
    assert.equal(result.snapshot.reminders[0].name, task.name);
});
test('final read failure never returns a stale preflight snapshot after a creation', () => {
    const fake = fakeApplication([{name: LIST_NAME}]);
    fake.denyAfterNextCreateRead();
    const result = apply(fake, [createOp(item())]);
    assert.equal(result.ok, false);
    assert.equal(result.code, 'macos_permission_denied');
    assert.equal(result.partial, true);
    assert.equal(Object.hasOwn(result, 'snapshot'), false);
    assert.equal(fake.states.size, 1);
});
test('checking completion during batched properties read prevents stale state writes', () => {
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(item())]}]);
    fake.changeRead();
    const result = apply(fake, [createOp(item(2))]);
    assert.equal(result.code, 'macos_snapshot_unstable');
    assert.equal(result.partial, false);
    assert.deepEqual(fake.writes, []);
    assert.equal(fake.taskState(item()).completed, true, 'The remote check must survive the failed snapshot');
});
test('unstable native ID order fails before writes and permission error remains explicit', () => {
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(item()), nativeFields(item(2))]}]);
    fake.reorderRead();
    assert.equal(apply(fake, [createOp(item(3))]).code, 'macos_snapshot_unstable');
    assert.deepEqual(fake.writes, []);
    const denied = fakeApplication();
    denied.denyReads();
    assert.equal(read(denied).code, 'macos_permission_denied');
    assert.deepEqual(denied.writes, []);
});
test('malformed requests, missing preconditions and invalid calendar dates fail before writes', () => {
    const task = item();
    for (const bad of [{...task, marker: 'wrong'}, {...task, body: `\n${task.marker}`},
        {...task, due: {kind: 'timed', at: '2026-10-13'}}, {...task, due: {kind: 'allDay', date: '2026-02-31'}}]) {
        const fake = fakeApplication([{name: LIST_NAME}]);
        assert.equal(apply(fake, [createOp(bad)]).code, 'invalid_request');
        assert.deepEqual(fake.writes, []);
    }
    for (const extra of [{mode: 'sync'}, {namespace: 'invalid'}, {listName: ''}, {listName: '   '}, {listName: 'bad\nname'}, {listName: 'bad\x00name'}]) {
        const fake = fakeApplication();
        assert.equal(call(fake, {...request('read'), ...extra}).code, 'invalid_request');
        assert.deepEqual(fake.writes, []);
    }
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(task)]}]);
    assert.equal(apply(fake, [createOp(task), createOp(task)]).code, 'invalid_request');
    const noPrecondition = updateOp(fake, task);
    delete noPrecondition.expectedModified;
    assert.equal(apply(fake, [noPrecondition]).code, 'invalid_request');
    assert.deepEqual(fake.writes, []);
});
test('Unicode and code-like strings remain literal JSON data', () => {
    const text = '中文 🧑🏽‍💻 e\u0301 \u2028 \u2029 "\\\'; Application("Terminal"); //\n$(touch /tmp/never-run) `say bad`';
    const base = item(), task = {...base, name: text, body: `${base.marker}\n负责人：${text}`};
    const fake = fakeApplication([{name: LIST_NAME}]);
    assert.equal(apply(fake, [JSON.parse(JSON.stringify(createOp(task)))]).ok, true);
    assertItem(fake, task);
});


test('custom list names route independent namespaces without changing other lists', () => {
    const nameA = '团队待办 · 甲', nameB = '团队待办 · 乙 "$(literal)"';
    const fake = fakeApplication([{name: '个人', reminders: [{name: '保留'}]}]);
    const a = call(fake, request('ensure_list', {listName: nameA}));
    const b = call(fake, request('ensure_list', {listName: nameB}, OTHER_NAMESPACE));
    assert.equal(a.ok, true, a.message);
    assert.equal(b.ok, true, b.message);
    assert.notEqual(a.snapshot.listId, b.snapshot.listId);
    const taskA = item(1, {name: '甲的任务'});
    const taskB = item(1, {name: '乙的任务'}, OTHER_NAMESPACE);
    for (const [name, list, task, namespace] of [[nameA, a, taskA, NAMESPACE], [nameB, b, taskB, OTHER_NAMESPACE]]) {
        const result = call(fake, request('apply', {listName: name, listId: list.snapshot.listId,
            operations: [createOp(task)], initializationMarkers: [task.marker]}, namespace));
        assert.equal(result.ok, true, result.message);
        assert.equal(result.snapshot.reminders.length, 1);
        assert.equal(result.snapshot.reminders[0].body, task.body);
        assert.equal(fake.taskState(task).containerId, list.snapshot.listId);
    }
    const updated = {...taskA, completed: true};
    assert.equal(call(fake, request('apply', {listName: nameA, listId: a.snapshot.listId,
        operations: [updateOp(fake, updated)]})).ok, true);
    assert.equal(fake.taskState(taskB).completed, false);
});
test('duplicate custom names fail all modes before writes', () => {
    for (const mode of ['read', 'ensure_list', 'apply']) {
        const name = '项目同名';
        const fake = fakeApplication([{name}, {name}]);
        const result = call(fake, request(mode, {listName: name, listId: 'L-1', operations: []}));
        assert.equal(result.code, 'macos_list_conflict');
        assert.deepEqual(fake.writes, []);
    }
});
test('initialization preflight preserves manual completed foreign and nested content', () => {
    const task = item();
    for (const rows of [[{name: '手工'}], [{name: '已完成', completed: true}],
        [nativeFields(item(2, {}, OTHER_NAMESPACE))],
        [{id: 'PARENT', name: '手工父项'}, {id: 'CHILD', name: '子项', containerId: 'PARENT'}]]) {
        const fake = fakeApplication([{name: LIST_NAME, reminders: rows}]);
        const result = call(fake, request('apply', {listId: fake.targetList().nativeId,
            operations: [createOp(task)], initializationMarkers: [task.marker]}));
        assert.equal(result.code, 'initialization_target_not_empty');
        assert.equal(result.partial, false);
        assert.deepEqual(fake.writes, []);
    }
});
test('interrupted initialization resumes only its declared task set without deletion', () => {
    const first = item(), second = item(2);
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(first)]}]);
    const id = fake.taskState(first).id;
    const payload = request('apply', {listId: fake.targetList().nativeId,
        operations: [createOp(first), createOp(second)], initializationMarkers: [first.marker, second.marker]});
    const result = call(fake, payload);
    assert.equal(result.ok, true, result.message);
    assert.equal(fake.taskState(first).id, id);
    assert.equal(result.snapshot.reminders.length, 2);
    assert.equal(call(fake, payload).ok, true);
    assert.equal(call(fake, request('apply', {listId: fake.targetList().nativeId,
        operations: [createOp(item(3))], initializationMarkers: [first.marker, second.marker]})).code, 'invalid_request');
    assert.equal(call(fake, request('apply', {listId: fake.targetList().nativeId,
        operations: [{action: 'delete', id, allowUnmarked: true}],
        initializationMarkers: [first.marker, second.marker]})).code, 'invalid_request');
});

test('stage timings count snapshots per dispatch and retain partial failure timing', () => {
    const fake = fakeApplication([{name: LIST_NAME, reminders: []}]);
    const before = read(fake);
    assert.equal(before.timings.nativeReadCount, 1);
    const created = apply(fake, [createOp(item())]);
    assert.equal(created.ok, true, created.message);
    assert.equal(created.timings.nativeReadCount, 2);
    for (const field of ['nativeReadMs', 'nativeWriteMs', 'nativeVerificationMs']) {
        assert.ok(created.timings[field] >= 0);
    }
    assert.equal(read(fake).timings.nativeReadCount, 1);
    fake.disableContainerReads();
    const failed = read(fake);
    assert.equal(failed.ok, false);
    assert.equal(failed.timings.nativeReadCount, 1);
});

test('native probe reads only list identity and never reads or mutates reminders', () => {
    const fake = fakeApplication([{name: LIST_NAME, reminders: [nativeFields(item())]}]);
    fake.disableContainerReads();
    const result = call(fake, request('probe'));
    assert.equal(result.ok, true, result.message);
    assert.equal(result.snapshot.listId, fake.targetList().nativeId);
    assert.equal(result.timings.nativeReadCount, 0);
    assert.ok(Object.keys(fake.reads).every(key => key.startsWith('lists.')));
    assert.deepEqual(fake.writes, []);
    const absent = call(fakeApplication(), request('probe'));
    assert.equal(absent.snapshot.listId, null);
    const duplicate = call(fakeApplication([{name: LIST_NAME}, {name: LIST_NAME}]), request('probe'));
    assert.equal(duplicate.code, 'macos_list_conflict');
});

let failed = 0;
for (const {name, run} of tests) {
    try { run(); process.stdout.write(`PASS ${name}\n`); }
    catch (error) { failed += 1; process.stderr.write(`FAIL ${name}\n${error.stack}\n`); }
}
process.stdout.write(`${tests.length - failed}/${tests.length} native adapter tests passed\n`);
process.exitCode = failed ? 1 : 0;
