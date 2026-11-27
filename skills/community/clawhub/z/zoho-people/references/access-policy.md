# Zoho People access policy

An access policy limits which endpoints Zoho People connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-people#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho People: its 38 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-people --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/attendance/fetchLatestAttEntries"},
    {"method": "GET", "path": "people/api/attendance/getAttendanceEntries"},
    {"method": "GET", "path": "people/api/attendance/getShiftConfiguration"},
    {"method": "GET", "path": "people/api/attendance/getUserReport"},
    {"method": "GET", "path": "people/api/files/downloadFile"},
    {"method": "GET", "path": "people/api/forms"},
    {"method": "GET", "path": "people/api/forms/{id}/components"},
    {"method": "GET", "path": "api/v2/leavetracker/leaves/records"},
    {"method": "GET", "path": "people/api/leave/getHolidays"},
    {"method": "GET", "path": "people/api/leave/getLeaveTypeDetails"},
    {"method": "GET", "path": "people/api/v2/leavetracker/reports/bookedAndBalance"},
    {"method": "GET", "path": "people/api/v3/leave-tracker/compensatory"},
    {"method": "GET", "path": "people/api/v3/leave-tracker/grant"},
    {"method": "GET", "path": "people/api/v3/leave-tracker/holidays"},
    {"method": "GET", "path": "people/api/v3/leave-tracker/holidays/{id}"},
    {"method": "GET", "path": "people/api/v3/leave-tracker/leaves"},
    {"method": "GET", "path": "people/api/v3/leave-tracker/leaves/{id}"},
    {"method": "GET", "path": "api/forms/{id}/getDataByID"},
    {"method": "GET", "path": "api/forms/{id}/getRecordByID"},
    {"method": "GET", "path": "api/forms/{id}/getRelatedRecords"},
    {"method": "GET", "path": "api/forms/{id}/records"},
    {"method": "GET", "path": "people/api/forms/{id}/getDataByID"},
    {"method": "GET", "path": "people/api/forms/{id}/getRecordByID"},
    {"method": "GET", "path": "people/api/forms/{id}/getRecordCount"},
    {"method": "GET", "path": "people/api/forms/{id}/getRecords"},
    {"method": "GET", "path": "people/api/v3/time-attendance/settings/work-calendars"},
    {"method": "GET", "path": "people/api/v3/time-attendance/settings/work-calendars/{id}"},
    {"method": "GET", "path": "people/api/timetracker/getclients"},
    {"method": "GET", "path": "people/api/timetracker/getjobs"},
    {"method": "GET", "path": "people/api/timetracker/getprojectdetails"},
    {"method": "GET", "path": "people/api/timetracker/getprojects"},
    {"method": "GET", "path": "people/api/timetracker/gettimelogdetails"},
    {"method": "GET", "path": "people/api/timetracker/gettimelogs"},
    {"method": "GET", "path": "people/api/timetracker/gettimesheet"},
    {"method": "GET", "path": "people/api/timetracker/gettimesheetdetails"},
    {"method": "GET", "path": "people/api/timetracker/gettimetrackersettings"},
    {"method": "GET", "path": "people/api/v3/time-tracker/clients"},
    {"method": "GET", "path": "people/api/v3/time-tracker/projects"}
  ],
  "deny": []
}
```

## Endpoints

The Zoho People endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/attendance/fetchLatestAttEntries | read | attendance | Fetch attendance entries added or updated in the last few minutes. |
| POST | people/api/attendance | write | attendance | Check in or check out an employee. |
| POST | people/api/attendance/addRegularization | write | attendance | Add attendance regularization (also has a getExistingRecords type). |
| POST | people/api/attendance/bulkImport | write | attendance | Bulk import check-in and check-out entries. |
| GET | people/api/attendance/getAttendanceEntries | read | attendance | Get attendance entries of an employee for a date. |
| GET | people/api/attendance/getShiftConfiguration | read | attendance | Get shift details of an employee for a date range. |
| GET | people/api/attendance/getUserReport | read | attendance | Get the attendance report of employees for a date range. |
| DELETE | people/api/v3/attendance/entries | write | attendance | Delete all attendance entries of an employee for a day. |
| DELETE | people/api/v3/attendance/entries/{id} | write | attendance | Delete a specific attendance entry. |
| GET | people/api/files/downloadFile | read | files | Download a file by file ID. |
| POST | people/api/files/uploadFile | write | files | Upload a file. |
| POST | people/api/v3/time-attendance/file | write | files | Upload a file attachment for leave, time tracker or attendance. |
| GET | people/api/forms | read | forms | List all forms in the account. |
| GET | people/api/forms/{id}/components | read | forms | Lists the fields (components) of a form. |
| POST | api/leave/addBalance | write | leave | Add or deduct leave balance. |
| GET | api/v2/leavetracker/leaves/records | read | leave | List leave records for a date range. |
| PATCH | api/v2/leavetracker/leaves/records/cancel/{id} | write | leave | Cancel a leave record. |
| GET | people/api/leave/getHolidays | read | leave | Lists holidays for an employee. |
| GET | people/api/leave/getLeaveTypeDetails | read | leave | Get leave types with permitted, availed and balance counts for an employee. |
| GET | people/api/v2/leavetracker/reports/bookedAndBalance | read | leave | Get the leave booked and balance report. |
| GET | people/api/v3/leave-tracker/compensatory | read | leave | List compensatory off requests. |
| GET | people/api/v3/leave-tracker/grant | read | leave | Lists leave grants. |
| PATCH | people/api/v3/leave-tracker/grant/{id} | write | leave | Cancel a leave grant request. |
| GET | people/api/v3/leave-tracker/holidays | read | leave | Lists holidays. |
| GET | people/api/v3/leave-tracker/holidays/{id} | read | leave | Gets a holiday by ID. |
| GET | people/api/v3/leave-tracker/leaves | read | leave | List leave requests for a date range. |
| GET | people/api/v3/leave-tracker/leaves/{id} | read | leave | Gets a leave record by ID. |
| PUT | people/api/v3/leave-tracker/leaves/{id} | write | leave | Edit a leave request. |
| GET | api/forms/{id}/getDataByID | read | records | Fetch a single record by record ID. |
| GET | api/forms/{id}/getRecordByID | read | records | Fetch a single record section-wise by record ID. |
| GET | api/forms/{id}/getRelatedRecords | read | records | Fetch related records of a parent module record. |
| GET | api/forms/{id}/records | read | records | Fetch records through a form view. |
| POST | people/api/forms/json/{id}/insertRecord | write | records | Insert a record into a form (employee, department, leave, project, job and others). |
| POST | people/api/forms/json/{id}/updateRecord | write | records | Update a record in a form. |
| GET | people/api/forms/{id}/getDataByID | read | records | Fetch a single record by record ID. |
| GET | people/api/forms/{id}/getRecordByID | read | records | Fetch a single record section-wise by record ID. |
| GET | people/api/forms/{id}/getRecordCount | read | records | Returns the number of records in a form. |
| GET | people/api/forms/{id}/getRecords | read | records | Fetch records of a form in bulk, with optional search. |
| GET | people/api/v3/time-attendance/settings/work-calendars | read | settings | Lists work calendars. |
| GET | people/api/v3/time-attendance/settings/work-calendars/{id} | read | settings | Gets a work calendar by ID. |
| PUT | people/api/v3/time-attendance/settings/work-calendars/{id} | write | settings | Edit a work calendar. |
| DELETE | people/api/v3/time-attendance/settings/work-calendars/{id} | write | settings | Delete a work calendar. |
| POST | people/api/timetracker/addclient | write | timetracker | Add a client. |
| POST | people/api/timetracker/addtimelog | write | timetracker | Add a time log. |
| POST | people/api/timetracker/addupdatetimelogs | write | timetracker | Add or update time logs in bulk. |
| POST | people/api/timetracker/approvetimesheet | write | timetracker | Approve or reject a timesheet. |
| POST | people/api/timetracker/createtimesheet | write | timetracker | Create a timesheet. |
| POST | people/api/timetracker/deleteclient | write | timetracker | Delete a client. |
| POST | people/api/timetracker/deletejob | write | timetracker | Delete a job. |
| POST | people/api/timetracker/deleteproject | write | timetracker | Delete a project. |
| POST | people/api/timetracker/deletetimelog | write | timetracker | Delete a time log. |
| POST | people/api/timetracker/deletetimesheet | write | timetracker | Delete a timesheet. |
| POST | people/api/timetracker/edittimelog | write | timetracker | Edit a time log. |
| GET | people/api/timetracker/getclients | read | timetracker | List clients. |
| GET | people/api/timetracker/getjobs | read | timetracker | List jobs. |
| GET | people/api/timetracker/getprojectdetails | read | timetracker | Get details of a project. |
| GET | people/api/timetracker/getprojects | read | timetracker | List projects. |
| GET | people/api/timetracker/gettimelogdetails | read | timetracker | Get details of a time log. |
| GET | people/api/timetracker/gettimelogs | read | timetracker | List time logs. |
| GET | people/api/timetracker/gettimesheet | read | timetracker | List timesheets. |
| GET | people/api/timetracker/gettimesheetdetails | read | timetracker | Get details of a timesheet. |
| GET | people/api/timetracker/gettimetrackersettings | read | timetracker | Get time tracker general settings. |
| POST | people/api/timetracker/modifyclient | write | timetracker | Modify a client. |
| POST | people/api/timetracker/modifytimesheet | write | timetracker | Modify a timesheet. |
| POST | people/api/timetracker/timer | write | timetracker | Start, pause or resume a timer. |
| GET | people/api/v3/time-tracker/clients | read | timetracker | List clients (v3). |
| GET | people/api/v3/time-tracker/projects | read | timetracker | List projects (v3). |
