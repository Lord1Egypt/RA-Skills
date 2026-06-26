const fs = require('fs');
const path = require('path');
const https = require('https');
const { URL } = require('url');

const root = path.join(__dirname, '..');
const dataDir = path.join(root, 'data');
const preferencePath = path.join(dataDir, 'preference.json');

function ensureFile(file, fallback) {
  if (!fs.existsSync(file)) fs.writeFileSync(file, JSON.stringify(fallback, null, 2) + '\n');
}

function readJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return fallback;
  }
}

function requestJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, { method: 'GET', headers: { 'User-Agent': 'OpenClaw/TeletalkAllJobsSkill' } }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch { resolve({ raw: body, statusCode: res.statusCode }); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

function formatDeadline(value) {
  if (!value) return value;
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Dhaka',
    dateStyle: 'medium',
    timeStyle: 'short',
    hour12: true,
  }).format(d);
}

function isOverdue(value) {
  const d = new Date(value);
  return !Number.isNaN(d.getTime()) && d.getTime() < Date.now();
}

(async () => {
  ensureFile(preferencePath, { keyboard: '', excluded: [] });
  const prefs = readJson(preferencePath, { keyboard: '', excluded: [] });
  const keyword = String(prefs.keyboard || '').trim();
  const excluded = Array.isArray(prefs.excluded) ? prefs.excluded.map(x => String(x).trim()).filter(Boolean) : [];

  if (!keyword) throw new Error('Missing preference.keyboard');

  const url = new URL('https://alljobs.teletalk.com.bd/api/v1/published-jobs/search');
  url.searchParams.set('searchKeyword', keyword);
  const res = await requestJson(url.toString());
  const jobs = Array.isArray(res?.govtJobs) ? res.govtJobs : [];

  const filtered = jobs.filter(job => {
    const title = String(job.job_title || '').toLowerCase();
    return !excluded.some(word => title.includes(word.toLowerCase())) && !isOverdue(job.deadline_date);
  }).map(job => ({
    job_primary_id: job.job_primary_id,
    job_title: job.job_title,
    job_title_bn: job.job_title_bn,
    org_name: job.org_name,
    org_name_bn: job.org_name_bn,
    vacancy: job.vacancy,
    deadline_date: formatDeadline(job.deadline_date),
    application_site_url: job.application_site_url,
  }));

  console.log(JSON.stringify(filtered, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
