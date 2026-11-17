#!/usr/bin/env node
import { pathToFileURL } from 'node:url';
import { realpathSync } from 'node:fs';
import { lookupWeather, renderWeatherLookup } from '../lib/weather-lookup.mjs';

const HELP = `Spidey weather (Node.js >=22)
Usage: node scripts/weather.mjs [--location "City, Region"] [--country-code US] [--day today|tomorrow] [--json]
Defaults: Los Angeles, today; Fahrenheit and mph. No API key required.
`;

export async function runWeatherCli(argv, {
  lookup = lookupWeather, stdout = text => process.stdout.write(text),
  stderr = text => process.stderr.write(text),
} = {}) {
  const params = {};
  let json = false;
  const seen = new Set();
  try {
    if (argv.length === 1 && ['--help', '-h'].includes(argv[0])) {
      stdout(HELP); return 0;
    }
    for (let i = 0; i < argv.length; i++) {
      const flag = argv[i];
      if (seen.has(flag)) throw new Error('Duplicate option.');
      seen.add(flag);
      if (flag === '--json') { json = true; continue; }
      if (!flag.startsWith('--')) throw new Error('Unknown option.');
      const key = { '--location': 'location', '--country-code': 'countryCode', '--day': 'day' }[flag];
      if (!key) throw new Error('Unknown option.');
      const value = argv[++i];
      if (!value || value.startsWith('--')) throw new Error('Missing option value.');
      params[key] = value;
    }
    if (params.day && !['today', 'tomorrow'].includes(params.day)) throw new Error('Use today or tomorrow.');
    if (params.countryCode && !/^[a-z]{2}$/i.test(params.countryCode)) throw new Error('Use a two-letter country code.');
    if (params.location !== undefined && (!/^[\p{L}\p{M}\p{N} ,.'’()-]{2,120}$/u.test(params.location.trim()) || params.location.split(',').length > 3)) {
      throw new Error('Use a public city name with optional region and country.');
    }
  } catch (error) {
    stderr(`${error.message}\n${HELP}`); return 2;
  }
  let weather;
  try { weather = await lookup(params); }
  catch { weather = { status: 'error', error: 'WEATHER_UNAVAILABLE', day: params.day ?? 'today' }; }
  const report = renderWeatherLookup(weather);
  stdout((json ? JSON.stringify({ status: weather.status, report, weather }, null, 2) : report) + '\n');
  return weather.status === 'error' ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  if (Number(process.versions.node.split('.')[0]) < 22) {
    process.stderr.write('Spidey weather requires Node.js 22 or newer.\n'); process.exitCode = 2;
  } else process.exitCode = await runWeatherCli(process.argv.slice(2));
}
