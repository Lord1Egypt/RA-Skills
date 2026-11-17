#!/usr/bin/env node
'use strict';
const { run } = require('../index');
const result = run();
console.log(JSON.stringify(result, null, 2));
if (result.skills_failed.length > 0) process.exit(1);
process.exit(0);
