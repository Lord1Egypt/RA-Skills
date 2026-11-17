import * as fs from "node:fs/promises";
import { constants } from "node:fs";
import { dirname, basename, join } from "node:path";
import { randomUUID } from "node:crypto";
import { DeliveryContractError } from "./contracts.mjs";

export class CommitOutcomeError extends DeliveryContractError {
  constructor(cause, outcome) { super("commit_failed", "durable commit did not return an acknowledgment"); this.cause=cause; this.outcome=outcome; }
}
async function syncDirectory(io, dir) {
  const handle=await io.open(dir, constants.O_RDONLY);
  try { await handle.sync(); } finally { await handle.close(); }
}
export async function durableReplace(file, body, {exclusive=false, io=fs}={}) {
  if (!Buffer.isBuffer(body) && typeof body!=="string") throw new DeliveryContractError("write_invalid","complete bytes are required");
  const dir=dirname(file), temp=join(dir,"."+basename(file)+".commit-"+randomUUID());
  let handle, visible=false, namespaceStarted=false;
  try {
    handle=await io.open(temp, "wx", 0o600);
    await handle.writeFile(body);
    await handle.sync();
    await handle.close(); handle=null;
    namespaceStarted=true;
    if(exclusive) { await io.link(temp,file); visible=true; await io.unlink(temp); }
    else { await io.rename(temp,file); visible=true; }
    await syncDirectory(io,dir);
    return {acknowledged:true};
  } catch(cause) {
    // After namespace mutation, failure is ambiguous until exact readback.
    // A thrown injected namespace operation may also have committed first.
    const ambiguous=visible || namespaceStarted || cause?.outcome==="unknown" || cause?.namespaceOutcome==="unknown";
    throw new CommitOutcomeError(cause,ambiguous?"unknown":"not_committed");
  } finally {
    if(handle) await handle.close().catch(()=>{});
    await io.unlink(temp).catch(()=>{});
  }
}
export async function durableAppend(file, record, {io=fs}={}) {
  const body=JSON.stringify(record);
  if(body===undefined || Buffer.byteLength(body)>65536) throw new DeliveryContractError("write_invalid","a bounded JSON record is required");
  let handle, started=false;
  try {
    handle=await io.open(file,constants.O_WRONLY|constants.O_APPEND|constants.O_CREAT|constants.O_NOFOLLOW,0o600);
    started=true;
    await handle.writeFile(body+"\n");
    await handle.sync();
    await handle.close(); handle=null;
    await syncDirectory(io,dirname(file));
    return {acknowledged:true};
  } catch(cause) { throw new CommitOutcomeError(cause,started?"unknown":"not_committed"); }
  finally { if(handle) await handle.close().catch(()=>{}); }
}
// Recovery never writes, renames, links, or appends. The caller retains its
// existing lock while checking these exact bytes and repeating both flushes.
export async function resyncExact(file, body, {io=fs}={}) {
  if (!Buffer.isBuffer(body) && typeof body!=="string") throw new DeliveryContractError("write_invalid","complete expected bytes are required");
  const expected=Buffer.isBuffer(body)?body:Buffer.from(body);
  let handle;
  try {
    handle=await io.open(file,constants.O_RDONLY|constants.O_NOFOLLOW);
    const info=await handle.stat();
    if (!info.isFile() || info.size!==expected.length || !(await handle.readFile()).equals(expected))
      throw new DeliveryContractError("readback_mismatch","recovery requires the complete expected bytes");
    await handle.sync();
    await handle.close(); handle=null;
    await syncDirectory(io,dirname(file));
    return {acknowledged:true,readback:true,resynced:true};
  } catch(cause) { throw new CommitOutcomeError(cause,"unknown"); }
  finally { if(handle) await handle.close().catch(()=>{}); }
}
export function hasExactRecord(parsed, record) {
  if (parsed.tornTail || !record?.commitId) return false;
  const matching=parsed.records.filter(row=>row.commitId===record.commitId);
  return matching.length===1 && JSON.stringify(matching[0])===JSON.stringify(record);
}
export function parseJournal(text,{maxBytes=8*1024*1024,maxRecords=10000}={}) {
  if(typeof text!=="string" || Buffer.byteLength(text)>maxBytes) throw new DeliveryContractError("journal_limit","journal exceeds read allowance");
  const pieces=text.split("\n"), tail=pieces.pop(), records=[];
  if(pieces.length>maxRecords) throw new DeliveryContractError("journal_limit","journal record count exceeds allowance");
  for(const line of pieces) {
    if(!line) throw new DeliveryContractError("journal_corrupt","empty complete journal record");
    let row;
    try { row=JSON.parse(line); } catch { throw new DeliveryContractError("journal_corrupt","malformed complete journal record"); }
    if(!row || typeof row!=="object" || Array.isArray(row)) throw new DeliveryContractError("journal_corrupt","journal record must be an object");
    records.push(row);
  }
  return {records,tornTail:tail.length>0,tailBytes:Buffer.byteLength(tail)};
}
// POSIX local filesystem, prevalidated owned parent, and caller-held serialization
// are required. Filesystem rollback/restored backups need an external witness;
// this helper does not promise to detect them or coordinate concurrent writers.
