// @ts-nocheck
import { DbConnection } from '../sdk';

const argsStr = process.argv[2] || "{}";
const args = JSON.parse(argsStr);

const content = args.content;
const tags = args.tags || [];

const URL = 'http://127.0.0.1:3001';
const DB_NAME = 'stdb-memory-1vgys';

async function main() {
  let db: any;
  await new Promise<void>((resolve, reject) => {
    const builder = DbConnection.builder()
      .withUri(URL)
      .withDatabaseName(DB_NAME)
      .onConnect((connection, identity, token) => {
        resolve();
      })
      .onConnectError((ctx, err) => {
        reject(err);
      });
      
    db = builder.build();
  });

  const id = Date.now().toString() + Math.floor(Math.random() * 1000).toString();
  const timestamp = BigInt(Date.now()) * 1000n; 

  // Call the reducer
  db.reducers.storeMemory({ id, content, timestamp, tags });

  // Wait for the reducer to be committed
  await new Promise(resolve => setTimeout(resolve, 500));

  console.log(JSON.stringify({ status: "success", id, content, tags }));
  db.disconnect();
  process.exit(0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});