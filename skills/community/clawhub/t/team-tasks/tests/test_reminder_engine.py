import datetime as dt
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import reminder_engine as engine
import task_store


NOW = dt.datetime.fromisoformat('2026-09-18T09:00:00+08:00')  # Friday


def task(identifier, **changes):
    value = {
        'id': identifier, 'title': identifier, 'priority': 'medium', 'isBlocking': False,
        'status': 'pending', 'assignee': 'Ada', 'dueDate': None, 'dueTime': None,
        'lastRemindedSlot': None,
    }
    value.update(changes)
    return value


class ReminderEngineTests(unittest.TestCase):
    def document(self, tasks, receipts=None):
        return {'version': '1.0', 'updatedAt': NOW.isoformat(), 'tasks': tasks,
                '_reminderReceipts': receipts or {}}

    def test_entries_are_separated_by_blank_lines_for_wechat(self):
        tasks = [task('T-{:03}'.format(index), dueDate='2026-09-18', dueTime='18:00') for index in range(2)]
        summary = engine.build_plan(self.document(tasks), NOW, '09:00', set())['text']
        focus = engine.render_focus([engine.classified(value, NOW) for value in tasks], '14:00')
        single = engine.render_task_reminder(engine.classified(task('one'), NOW))
        for rendered, block_count in ((summary, 4), (focus, 3), (single, 8)):
            with self.subTest(text=rendered):
                self.assertEqual(len(rendered.split('\n\n')), block_count)
                for block in rendered.split('\n\n'):
                    self.assertNotIn('\n', block)
        self.assertIn('另有 0 项待处理任务。', summary)
        self.assertIn('负责人：Ada', single)

    def test_renderers_emit_markdown_bold_for_wechat(self):
        tasks = [task('T-{:03}'.format(index), dueDate='2026-09-18', dueTime='18:00') for index in range(2)]
        summary = engine.build_plan(self.document(tasks), NOW, '09:00', set())['text']
        self.assertTrue(summary.startswith('**团队任务晨间摘要**\n\n'))
        self.assertIn('**[T-000]** T-000 ｜ 负责人：Ada', summary)

        focus = engine.render_focus([engine.classified(task('T-009'), NOW)], '14:00')
        self.assertTrue(focus.startswith('**团队任务重点提醒 14:00**\n\n'))
        self.assertIn('**[T-009]** T-009 ｜ 负责人：Ada', focus)

        single = engine.render_task_reminder(engine.classified(task('T-010'), NOW))
        self.assertTrue(single.startswith('**任务提醒**\n\n'))
        self.assertIn('**[T-010] T-010**\n\n', single)

    def test_markdown_bold_survives_line_separation_rules(self):
        current = engine.classified(task('stale', createdAt='2026-09-01T09:00:00+08:00'), NOW)
        self.assertTrue(current['attentionReasons'])
        for rendered in (engine.render_summary([current], 1), engine.render_focus([current], '10:00'),
                         engine.render_task_reminder(current)):
            with self.subTest(text=rendered):
                for block in rendered.split('\n\n'):
                    self.assertEqual(block.count('**') % 2, 0)
                self.assertIn(' ｜ 无有效进展：{} 个工作日 ｜ 上调原因：{}'.format(
                    current['staleWorkdays'], '；'.join(current['attentionReasons'])), rendered)

    def test_classification_and_attention_rules(self):
        overdue = engine.classified(task('overdue', dueDate='2026-09-17', dueTime='18:00'), NOW)
        today_high = engine.classified(task('today-high', priority='high', dueDate='2026-09-18', dueTime='18:00'), NOW)
        soon = engine.classified(task('soon', dueDate='2026-09-20', dueTime='08:00'), NOW)
        normal = engine.classified(task('normal', dueDate='2026-10-01'), NOW)
        unscheduled = engine.classified(task('none'), NOW)
        blocking = engine.classified(task('blocking', priority='high', isBlocking=True), NOW)
        self.assertEqual((overdue['urgency'], overdue['attentionLevel']), ('overdue', 'high'))
        self.assertEqual((today_high['urgency'], today_high['attentionLevel']), ('today', 'critical'))
        self.assertEqual(soon['urgency'], 'soon')
        self.assertEqual(normal['urgency'], 'normal')
        self.assertEqual(unscheduled['urgency'], 'none')
        self.assertEqual(blocking['attentionLevel'], 'critical')

    def test_summary_is_limited_and_includes_pending_total(self):
        tasks = [task('T-{:03}'.format(index), dueDate='2026-09-18', dueTime='18:00') for index in range(6)]
        plan = engine.build_plan(self.document(tasks), NOW, '09:00', set())
        self.assertFalse(plan['silent'])
        self.assertEqual(len(plan['tasks']), 5)
        self.assertIn('另有 1 项待处理任务。', plan['text'])
        self.assertIn('负责人：Ada', plan['text'])
        self.assertIn('紧急度：today', plan['text'])

    def test_focus_slots_only_include_critical_or_permitted_high_priority(self):
        tasks = [
            task('critical', priority='critical', dueDate='2026-09-18', dueTime='18:00'),
            task('high', priority='high', dueDate='2026-09-20', dueTime='08:00'),
            task('medium', priority='medium', dueDate='2026-09-18', dueTime='18:00'),
            task('unscheduled', priority='critical'),
        ]
        afternoon = engine.build_plan(self.document(tasks), NOW, '14:00', set())
        morning = engine.build_plan(self.document(tasks), NOW, '10:00', set())
        self.assertEqual([value['id'] for value in afternoon['tasks']], ['critical'])
        self.assertEqual({value['id'] for value in morning['tasks']}, {'critical', 'high'})
        self.assertIn('重要性：critical', afternoon['text'])
        self.assertIn('关注度：critical', afternoon['text'])

    def test_existing_slot_receipt_is_excluded(self):
        values = [task('once', priority='critical')]
        key = engine.slot_key(NOW, '10:00')
        plan = engine.build_plan(self.document(values, {'once': [key]}), NOW, '10:00', set())
        self.assertTrue(plan['silent'])
        self.assertEqual(plan['reason'], 'no_eligible_tasks')

    def test_weekend_and_holiday_are_silent(self):
        values = self.document([task('critical', priority='critical', dueDate='2026-09-20')])
        weekend = NOW + dt.timedelta(days=1)
        self.assertEqual(engine.build_plan(values, weekend, '09:00', set())['reason'], 'non_working_day')
        self.assertEqual(engine.build_plan(values, NOW, '09:00', {NOW.date()})['reason'], 'non_working_day')

    def test_structured_calendar_supports_makeup_workdays_and_rejects_conflicts(self):
        values = self.document([task('critical', priority='critical', dueDate='2026-09-20')])
        sunday = dt.datetime.fromisoformat('2026-09-20T09:00:00+08:00')
        calendar = {'holidays': {NOW.date()}, 'makeupWorkdays': {sunday.date()}}
        self.assertFalse(engine.build_plan(values, sunday, '09:00', calendar)['silent'])
        self.assertTrue(engine.build_plan(values, NOW, '09:00', calendar)['silent'])
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8') as calendar_file:
            json.dump({'holidays': ['2026-09-20'], 'makeupWorkdays': ['2026-09-20']}, calendar_file)
            calendar_file.flush()
            with self.assertRaises(engine.CalendarError) as error:
                engine.load_holidays(calendar_file.name)
        self.assertEqual(error.exception.code, 'calendar_conflict')
        self.assertEqual(error.exception.conflicts, ['2026-09-20'])
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8') as calendar_file:
            json.dump(['2026-09-25'], calendar_file)
            calendar_file.flush()
            legacy = engine.load_holidays(calendar_file.name)
        self.assertEqual(legacy, {'holidays': {dt.date(2026, 9, 25)}, 'makeupWorkdays': set()})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8') as calendar_file:
            json.dump({'holidays': ['2026-09-20'], 'makeupWorkdays': ['2026-09-20']}, calendar_file)
            calendar_file.flush()
            command = [sys.executable, str(SCRIPTS / 'reminder_engine.py'), '--data-dir', '/unused',
                       '--slot', '09:00', '--holiday-file', calendar_file.name,
                       '--now', NOW.isoformat()]
            completed = subprocess.run(command, capture_output=True, text=True)
        result = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(result['code'], 'calendar_conflict')
        self.assertEqual(result['conflicts'], ['2026-09-20'])

    def test_stale_workdays_use_calendar_and_snooze_history(self):
        now = dt.datetime.fromisoformat('2026-10-01T09:00:00+08:00')
        value = task('stale', createdAt='2026-09-21T09:00:00+08:00', history=[{
            'at': '2026-09-22T09:00:00+08:00', 'action': 'update', 'by': 'Ada',
            'detail': {'changes': {'snoozedUntil': '2026-09-24T09:00:00+08:00'}},
        }])
        # 22nd–24th are snoozed; 25th, 28th–30th are the four elapsed workdays.
        self.assertEqual(engine.stale_workdays_for(value, now), 4)
        classified = engine.classified(value, now)
        self.assertEqual(classified['attentionLevel'], 'high')
        self.assertIn('stale_over_3_workdays', classified['attentionReasons'])

    def test_snooze_intervals_skip_non_mapping_history_details(self):
        history = [
            {'at': '2026-09-22T09:00:00+08:00', 'action': 'progress', 'by': 'Ada', 'detail': '谈判推进中'},
            {'at': '2026-09-22T10:00:00+08:00', 'action': 'updated', 'by': 'Ada', 'detail': None},
            {'at': '2026-09-22T11:00:00+08:00', 'action': 'created', 'by': 'Ada', 'detail': 1},
            {'at': '2026-09-22T12:00:00+08:00', 'action': 'completed', 'by': 'Ada', 'detail': {}},
        ]
        value = task('legacy', history=history)
        self.assertEqual(engine.snooze_intervals(value, NOW), [])

        history.append({'at': '2026-09-23T09:00:00+08:00', 'action': 'update', 'by': 'Ada',
                        'detail': {'changes': {'snoozedUntil': '2026-09-25T09:00:00+08:00'}}})
        self.assertEqual(engine.snooze_intervals(value, NOW), [
            (dt.datetime.fromisoformat('2026-09-23T09:00:00+08:00'),
             dt.datetime.fromisoformat('2026-09-25T09:00:00+08:00')),
        ])

    def test_build_plan_accepts_valid_ledger_with_legacy_string_detail(self):
        with tempfile.TemporaryDirectory() as directory:
            store = task_store.TaskStore(directory)
            store.execute({'op': 'init'})
            store.execute({'op': 'create', 'actor': 'Ada', 'fields': {
                'title': '代理商谈判', 'priority': 'critical', 'dueDate': '2026-09-18'}})
            doc = store.execute({'op': 'read'})['ledgers'][task_store.MAIN]
            doc['tasks'][0]['createdAt'] = '2026-08-20T09:00:00+08:00'
            doc['tasks'][0]['history'].extend([
                {'at': '2026-08-27T15:42:31+08:00', 'action': 'progress', 'by': 'Ada',
                 'detail': '与代理商商务沟通，谈判推进中'},
                {'at': '2026-09-01T10:00:00+08:00', 'action': 'updated', 'by': 'Ada',
                 'detail': '等待对方回复'},
            ])
            task_store.validate(doc)
            plan = engine.build_plan(doc, NOW, '09:00', set())
            self.assertFalse(plan['silent'])
            self.assertEqual([item['id'] for item in plan['tasks']], [doc['tasks'][0]['id']])

    def test_marked_comments_reset_progress_but_plain_comments_do_not(self):
        now = dt.datetime.fromisoformat('2026-09-29T09:00:00+08:00')
        value = task('progress', createdAt='2026-09-18T09:00:00+08:00', comments=[
            {'at': '2026-09-25T10:00:00+08:00', 'from': 'bot', 'content': '同步完成'},
            {'at': '2026-09-28T10:00:00+08:00', 'from': 'Ada', 'content': '已推进', 'meaningfulProgress': True},
        ])
        self.assertEqual(engine.stale_workdays_for(value, now), 0)
        value['comments'][-1]['meaningfulProgress'] = False
        self.assertGreater(engine.stale_workdays_for(value, now), 3)

    def test_stale_unscheduled_tasks_have_controlled_delivery(self):
        now = dt.datetime.fromisoformat('2026-09-18T09:00:00+08:00')
        value = task('stale', createdAt='2026-09-01T09:00:00+08:00')
        current = engine.classified(value, now)
        self.assertIn('stale', [item['id'] for item in engine.selected_for_slot([current], '09:00')])
        self.assertIn('stale', [item['id'] for item in engine.selected_for_slot([current], '10:00')])
        self.assertNotIn('stale', [item['id'] for item in engine.selected_for_slot([current], '14:00')])

    def test_reservation_uses_safe_store_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            store = task_store.TaskStore(directory)
            store.execute({'op': 'init'})
            identifier = store.execute({'op': 'create', 'actor': 'test', 'fields': {
                'title': 'critical', 'priority': 'critical', 'dueDate': '2026-09-18', 'dueTime': '18:00'}})['id']
            first = engine.execute(Path(directory), NOW, '10:00', set(), reserve=True, delay_minutes=0)
            second = engine.execute(Path(directory), NOW, '10:00', set(), reserve=True, delay_minutes=0)
            saved = store.execute({'op': 'read'})['ledgers'][task_store.MAIN]
            saved_task = saved['tasks'][0]
            self.assertEqual(first['reserved'], [identifier])
            self.assertFalse(first['silent'])
            self.assertEqual(second['reserved'], [])
            self.assertTrue(second['silent'])
            self.assertEqual(saved_task['reminderCount'], 1)
            self.assertEqual(saved_task['lastRemindedSlot'], engine.slot_key(NOW, '10:00'))

    def test_cli_emits_a_message_and_random_delay_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            store = task_store.TaskStore(directory)
            store.execute({'op': 'init'})
            store.execute({'op': 'create', 'actor': 'test', 'fields': {
                'title': 'critical', 'priority': 'critical', 'dueDate': '2026-09-18', 'dueTime': '18:00'}})
            command = [sys.executable, str(SCRIPTS / 'reminder_engine.py'), '--data-dir', directory,
                       '--slot', '10:00', '--now', NOW.isoformat(), '--delay-minutes', '7']
            completed = subprocess.run(command, check=True, capture_output=True, text=True)
            result = json.loads(completed.stdout)
            self.assertTrue(result['ok'])
            self.assertFalse(result['silent'])
            self.assertEqual(result['delayMinutes'], 7)
            self.assertEqual(result['scheduledFor'], '2026-09-18T09:07+08:00')
            self.assertIn('重点提醒 10:00', result['text'])

    def test_specialized_reminder_uses_live_task_state_and_reserves(self):
        with tempfile.TemporaryDirectory() as directory:
            store = task_store.TaskStore(directory)
            store.execute({'op': 'init'})
            identifier = store.execute({'op': 'create', 'actor': 'test', 'fields': {
                'title': 'old title', 'assignee': 'Ada', 'dueDate': '2026-09-18'}})['id']
            store.execute({'op': 'update', 'actor': 'test', 'id': identifier,
                           'changes': {'title': 'latest title', 'assignee': 'Lin'},
                           'expected': {'title': 'old title', 'assignee': 'Ada'}})
            result = engine.resolve_task_reminder(directory, identifier, '2026-09-18T14:00+08:00', NOW,
                                                   reserve=True, delivery_reference='job-1')
            self.assertEqual(result['action'], 'deliver')
            self.assertEqual(result['deliveryReference'], 'job-1')
            self.assertIn('latest title', result['text'])
            self.assertIn('负责人：Lin', result['text'])
            duplicate = engine.resolve_task_reminder(directory, identifier, '2026-09-18T14:00+08:00', NOW,
                                                      reserve=True)
            self.assertEqual(duplicate['reason'], 'already_reserved')

    def test_specialized_reminder_silences_inactive_and_snoozed_tasks(self):
        with tempfile.TemporaryDirectory() as directory:
            store = task_store.TaskStore(directory)
            store.execute({'op': 'init'})
            identifier = store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': 'task'}})['id']
            store.execute({'op': 'status', 'actor': 'test', 'id': identifier, 'status': 'done',
                           'expected': {'status': 'pending'}})
            inactive = engine.resolve_task_reminder(directory, identifier, '2026-09-18T14:00+08:00', NOW)
            self.assertEqual((inactive['action'], inactive['reason']), ('silent', 'inactive_task'))
            reopened = store.execute({'op': 'reopen', 'actor': 'test', 'id': identifier,
                                      'expected': {'status': 'done'}})
            self.assertTrue(reopened['ok'])
            store.execute({'op': 'update', 'actor': 'test', 'id': identifier,
                           'changes': {'snoozedUntil': '2026-09-18T10:00:00+08:00'},
                           'expected': {'snoozedUntil': None}})
            paused = engine.resolve_task_reminder(directory, identifier, '2026-09-18T14:00+08:00', NOW)
            self.assertEqual((paused['action'], paused['reason']), ('silent', 'snoozed'))

    def test_specialized_reminder_uses_planned_slot_calendar_day(self):
        with tempfile.TemporaryDirectory() as directory:
            store = task_store.TaskStore(directory)
            store.execute({'op': 'init'})
            identifier = store.execute({'op': 'create', 'actor': 'test', 'fields': {'title': 'task'}})['id']
            slot = '2026-09-20T14:00+08:00'  # Sunday
            silent = engine.resolve_task_reminder(directory, identifier, slot, NOW, reserve=True,
                                                   calendar={'holidays': set(), 'makeupWorkdays': set()})
            self.assertEqual((silent['action'], silent['reason']), ('silent', 'non_working_day'))
            self.assertEqual(store.execute({'op': 'read'})['ledgers'][task_store.MAIN]['tasks'][0]['reminderCount'], 0)
            delivered = engine.resolve_task_reminder(directory, identifier, slot, NOW,
                                                      calendar={'holidays': set(),
                                                                'makeupWorkdays': {dt.date(2026, 9, 20)}})
            self.assertEqual(delivered['action'], 'deliver')


if __name__ == '__main__':
    unittest.main()
