# Failure Fallbacks

## usage limit exceeded

Meaning:
- provider accepted the route but quota is exhausted

Action:
- stop retry loops
- report real status
- switch to waiting or approved backup route

## token plan does not support model

Meaning:
- the account or plan does not support the selected model variant

Action:
- do not blindly retry the same model
- route to supported variant
- update policy notes for future runs

## success but no file_id

Meaning:
- task resolution is incomplete or provider response is malformed

Action:
- report as failed retrieval
- do not count as final success

## narration does not match subtitle text

Meaning:
- TTS used wrong or outdated text

Action:
- regenerate TTS from authoritative subtitle text
- invalidate mismatched audio mix

## ambience sounds like music, not environment

Meaning:
- fallback ambience generation produced a musical bed rather than environmental sound texture

Action:
- reject as ambience
- prefer local ambience asset or another approved fallback

## probe success mistaken as formal success

Meaning:
- a diagnostic task succeeded and was incorrectly counted as a final deliverable

Action:
- correct status immediately
- keep probe as optional preview only
