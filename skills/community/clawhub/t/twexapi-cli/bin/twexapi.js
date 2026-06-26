#!/usr/bin/env node

import { main } from "../src/index.js";

main().catch((error) => {
  console.error("Request failed.");
  if (error?.message) {
    console.error(error.message);
  }
  process.exit(1);
});
