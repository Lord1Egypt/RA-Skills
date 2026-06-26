from unittest.mock import patch

from sherpamind.automation import MANAGED_CRON_NAMES, doctor_automation


def test_doctor_automation_detects_absent_legacy_cron_jobs() -> None:
    with patch('sherpamind.automation.managed_jobs', return_value=[]):
        report = doctor_automation()
    assert report['status'] == 'absent'
    assert report['managed_cron_names'] == MANAGED_CRON_NAMES


def test_doctor_automation_detects_duplicates() -> None:
    with patch('sherpamind.automation.managed_jobs', return_value=[
        {'name': 'sherpamind:hot-open-sync'},
        {'name': 'sherpamind:hot-open-sync'},
    ]):
        report = doctor_automation()
    assert report['duplicates']['sherpamind:hot-open-sync'] == 2
    assert report['status'] == 'present'
