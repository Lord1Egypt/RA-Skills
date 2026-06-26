#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help || !named.order || !named.rating) {
  console.error('Usage: submit-review.mjs --order <id> --rating <1-5> [--comment "..."]');
  process.exit(2);
}

const body = { rating: Number.parseInt(named.rating, 10) };
if (named.comment) body.comment = named.comment;

const data = await tmrFetch("POST", `/reviews/order/${named.order}`, body);
console.log(`Review submitted for order ${named.order} (rating: ${body.rating})`);
console.log(JSON.stringify(data, null, 2));
