'use strict';

const { isReplyOrForward, hasRequestIntent, classifyThreadHint } =
  require('../dist/adapters/threadHints.js');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    passed++;
  } else {
    failed++;
    console.error(`  FAIL  ${label}`);
  }
}

console.log('\nthreadHints unit tests\n');

// --- isReplyOrForward ---
assert(isReplyOrForward('Re: Hello'), 'isReplyOrForward: Re: prefix');
assert(isReplyOrForward('RE: Hello'), 'isReplyOrForward: RE: uppercase');
assert(isReplyOrForward('re: hello'), 'isReplyOrForward: re: lowercase');
assert(isReplyOrForward('Fwd: Hello'), 'isReplyOrForward: Fwd: prefix');
assert(isReplyOrForward('FW: Hello'), 'isReplyOrForward: FW: prefix');
assert(isReplyOrForward('fw: hello'), 'isReplyOrForward: fw: lowercase');
assert(
  isReplyOrForward('Re: [패스트캠퍼스] 스노우 / 클로드 기반 AI Agent 과정 출강 요청드립니다'),
  'isReplyOrForward: Re: Korean subject'
);
assert(!isReplyOrForward('Hello'), 'isReplyOrForward: no prefix → false');
assert(!isReplyOrForward('Request for review'), 'isReplyOrForward: starts with Re but no colon → false');
assert(!isReplyOrForward(''), 'isReplyOrForward: empty string → false');

// --- hasRequestIntent — Korean ---
assert(hasRequestIntent('출강 요청드립니다'), 'hasRequestIntent: 요청드립니다');
assert(hasRequestIntent('확인 부탁드립니다'), 'hasRequestIntent: 확인 부탁드립니다');
assert(hasRequestIntent('회신 부탁드립니다'), 'hasRequestIntent: 회신 부탁드립니다');
assert(hasRequestIntent('가능하실까요'), 'hasRequestIntent: 가능하실까요');
assert(hasRequestIntent('검토 부탁드립니다'), 'hasRequestIntent: 검토 부탁드립니다');
assert(hasRequestIntent('답변 부탁드립니다'), 'hasRequestIntent: 답변 부탁드립니다');

// --- hasRequestIntent — English ---
assert(hasRequestIntent('please review this document'), 'hasRequestIntent: please review');
assert(hasRequestIntent('Can you confirm the date?'), 'hasRequestIntent: can you confirm');
assert(hasRequestIntent('Just following up on my last message'), 'hasRequestIntent: following up');
assert(hasRequestIntent('This is a request for information'), 'hasRequestIntent: request');
assert(hasRequestIntent('Could you check this?'), 'hasRequestIntent: could you');
assert(hasRequestIntent('Please send the updated file'), 'hasRequestIntent: please send');

// --- hasRequestIntent — no match ---
assert(!hasRequestIntent('Meeting notes from yesterday'), 'hasRequestIntent: no intent → false');
assert(!hasRequestIntent(''), 'hasRequestIntent: empty string → false');

// --- classifyThreadHint ---
assert(
  classifyThreadHint({
    subject: 'Re: [패스트캠퍼스] 스노우 / 클로드 기반 AI Agent 과정 출강 요청드립니다',
    snippet: '답변 부탁드립니다',
  }) === 'potential_open_loop',
  'classifyThreadHint: Korean request Re: thread → potential_open_loop'
);

assert(
  classifyThreadHint({
    subject: 'Re: Following up on the proposal review',
    snippet: 'Could you please send the updated deck?',
  }) === 'potential_open_loop',
  'classifyThreadHint: English request Re: thread → potential_open_loop'
);

assert(
  classifyThreadHint({
    subject: 'Re: Team offsite logistics',
    snippet: 'Just wanted to loop you in on the schedule change.',
  }) === 'needs_inspection',
  'classifyThreadHint: Re: thread without request phrases → needs_inspection'
);

assert(
  classifyThreadHint({
    subject: 'Fwd: Budget approval needed',
    snippet: 'please review before the deadline',
  }) === 'potential_open_loop',
  'classifyThreadHint: Fwd: with request phrase → potential_open_loop'
);

assert(
  classifyThreadHint({
    subject: 'New message from the team',
    snippet: 'please review this document',
  }) === null,
  'classifyThreadHint: non-reply thread → null (even with request phrase)'
);

assert(
  classifyThreadHint({ subject: '', snippet: 'please review' }) === null,
  'classifyThreadHint: empty subject → null'
);

assert(
  classifyThreadHint({ subject: undefined, snippet: undefined }) === null,
  'classifyThreadHint: undefined inputs → null'
);

// --- summary ---
console.log(`\n  ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  process.exit(1);
}
