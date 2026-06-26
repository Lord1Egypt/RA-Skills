# Async Reporting Rule

Use this reference when Workhorse Duo is operating in its normal async mode.

## Core rule

Async dispatch does **not** mean silent dispatch.

The required behavior is:
1. dispatch work to Xiaoma or Xiaoniu
2. return the main session to the user immediately
3. when the worker finishes, proactively report back in the main session
4. do not wait for the user to ask whether the task is done

## Required reporting behavior

### After dispatch

Tell the user:
- the task has been handed off
- the main session remains available
- you will report back when the worker finishes

### After completion

Report proactively with:
- what Xiaoma finished
- whether Xiaoniu passed it
- if not passed, only the concrete issues

### Do not do this

Do not:
- block the main session by default
- silently let the worker finish without following up
- wait for the user to ask for status before reporting completion

## Exception cases

Synchronous waiting is acceptable only for:
- smoke tests
- runtime debugging
- explicit live-monitor requests from the user
