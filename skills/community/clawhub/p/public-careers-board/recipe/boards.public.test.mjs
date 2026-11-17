import assert from "node:assert/strict";
import test from "node:test";
import { gateRequest, normalizeWorkday, normalizeAshby } from "./boards.mjs";

const ctx = {
  boardUrl: "https://acxiomllc.wd5.myworkdayjobs.com/en-US/AcxiomUSA",
  source: "https://acxiomllc.wd5.myworkdayjobs.com/wday/cxs/acxiomllc/AcxiomUSA/jobs",
  fetchedAt: "2026-10-07T00:00:00.000Z",
};
const ashbyCtx = {
  boardUrl: "https://jobs.ashbyhq.com/liveramp-inc",
  source: "https://api.ashbyhq.com/posting-api/job-board/liveramp-inc",
  fetchedAt: ctx.fetchedAt,
};
const good = { title: "One", externalPath: "/job/A/One_1", locationsText: "Remote" };
const first = { offset: 0, httpStatus: 200, body: { total: 1, jobPostings: [good] } };
const listed = { title: "Listed", location: "Remote", isListed: true,
  jobUrl: "https://jobs.ashbyhq.com/liveramp-inc/a" };

test("request gate rejects insecure protocols and embedded credentials", () => {
  for (const url of [
    "http://api.ashbyhq.com/posting-api/job-board/liveramp-inc",
    "https://user:secret@api.ashbyhq.com/posting-api/job-board/liveramp-inc",
    "https://api.ashbyhq.com.evil.example/posting-api/job-board/liveramp-inc",
  ]) assert.equal(gateRequest(url).ok, false);
  assert.equal(gateRequest(ashbyCtx.source).ok, true);
});

test("a missing-field past-end row cannot confirm a complete read", () => {
  const r = normalizeWorkday({ pages: [first], probe: {
    offset: 1, httpStatus: 200, body: { total: 1, jobPostings: [{ bulletFields: ["JR-MISSING"] }] },
  } }, ctx);
  assert.equal(r.rows.length, 1);
  assert.equal(r.coverage.status, "partial_past_end_incomplete");
  assert.equal(r.coverage.pastEnd.confirmed, false);
  assert.equal(r.coverage.pastEnd.unreadableRows, 1);
  assert.equal(r.coverage.missing.length, 1);
});

test("a malformed later page retains the useful earlier rows", () => {
  const r = normalizeWorkday({ pages: [
    { ...first, body: { total: 2, jobPostings: [good] } },
    { offset: 1, httpStatus: 200, body: { jobs: [] } },
  ] }, ctx);
  assert.equal(r.rows.length, 1);
  assert.equal(r.coverage.status, "partial");
  assert.equal(r.coverage.remaining, 1);
});

test("invalid totals or a noninitial page cannot define a board", () => {
  for (const total of [-1, 1.5, NaN, Infinity]) {
    const r = normalizeWorkday({ pages: [{ ...first, body: { total, jobPostings: [good] } }] }, ctx);
    assert.equal(r.coverage.status, "wrong_schema");
  }
  assert.equal(normalizeWorkday({ pages: [{ ...first, offset: 20 }] }, ctx).coverage.status, "wrong_schema");
});

test("Workday rows must use a posting path, not an arbitrary absolute-looking path", () => {
  for (const externalPath of ["/", "//evil.example/path", "/account/login", "/job"]) {
    const r = normalizeWorkday({ pages: [{ ...first,
      body: { total: 1, jobPostings: [{ ...good, externalPath }] } }] }, ctx);
    assert.equal(r.rows.length, 0);
    assert.equal(r.coverage.status, "partial");
  }
});

test("Ashby unknown listing authority is withheld and remains partial", () => {
  const { isListed, ...unknown } = listed;
  const r = normalizeAshby({ httpStatus: 200, body: { jobs: [unknown] } }, ashbyCtx);
  assert.equal(r.rows.length, 0);
  assert.equal(r.coverage.status, "partial");
  assert.equal(r.coverage.emptyBoard, false);
  assert.equal(r.coverage.missing[0].reason, "missing_isListed");
});

test("Ashby links stay inside the actual public board", () => {
  for (const jobUrl of [
    "https://evil.example/job",
    "https://jobs.ashbyhq.com/other-company/a",
    "https://user:secret@jobs.ashbyhq.com/liveramp-inc/a",
    "http://jobs.ashbyhq.com/liveramp-inc/a",
  ]) {
    const r = normalizeAshby({ httpStatus: 200, body: { jobs: [{ ...listed, jobUrl }] } }, ashbyCtx);
    assert.equal(r.rows.length, 0);
    assert.equal(r.coverage.status, "partial");
  }
  const fallback = normalizeAshby({ httpStatus: 200, body: { jobs: [{
    ...listed, jobUrl: "https://evil.example/job",
    applyUrl: listed.jobUrl + "/application",
  }] } }, ashbyCtx);
  assert.equal(fallback.rows.length, 1);
  assert.equal(fallback.rows[0].url, listed.jobUrl + "/application");
});

test("normal current rows and a repeated valid probe remain usable", () => {
  const workday = normalizeWorkday({ pages: [first], probe: { ...first, offset: 1 } }, ctx);
  assert.equal(workday.coverage.status, "complete_for_declared_total");
  assert.equal(workday.coverage.pastEnd.confirmed, true);
  assert.equal(workday.rows[0].url, ctx.boardUrl + good.externalPath);
  const ashby = normalizeAshby({ httpStatus: 200, body: { jobs: [listed] } }, ashbyCtx);
  assert.equal(ashby.rows.length, 1);
  assert.equal(ashby.coverage.status, "complete_for_returned_listed_set");
});
