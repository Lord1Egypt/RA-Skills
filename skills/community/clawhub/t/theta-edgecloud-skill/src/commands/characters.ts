// Data flow: sends the game-scoped Characters key and character/session payloads to
// https://ai-chars-api.thetaedgecloud.com only. Every non-GET route (create/update/delete, session
// create/delete/context/message) requires confirm:true here, before any request.
import { ThetaConfig } from '../config.js';
import { getJson, postJson, putJson, deleteEmpty } from '../clients/http.js';
import { redactObject } from '../redaction.js';
import { pathSegment } from '../security.js';
import { assertApproved } from '../approval.js';

// Theta's public AI Characters OpenAPI 1.0.0. Dashboard/game-key management
// deliberately excluded: those operations use different session credentials.
export const characterRoutes: Record<string, {method:string;path:string;fields:string[]}> = {
  list: {method:'GET',path:'/game/{gameId}/character/list',fields:['gameId']},
  get: {method:'GET',path:'/game/{gameId}/character/{characterId}',fields:['gameId','characterId']},
  create: {method:'POST',path:'/game/{gameId}/character',fields:['gameId']},
  update: {method:'PUT',path:'/game/{gameId}/character/{characterId}',fields:['gameId','characterId']},
  delete: {method:'DELETE',path:'/game/{gameId}/character/{characterId}',fields:['gameId','characterId']},
  'session.create': {method:'POST',path:'/session',fields:[]},
  'session.get': {method:'GET',path:'/session/{sessionId}',fields:['sessionId']},
  'session.delete': {method:'DELETE',path:'/session/{sessionId}',fields:['sessionId']},
  'session.list': {method:'GET',path:'/session/{gameId}/list',fields:['gameId']},
  'session.context': {method:'PUT',path:'/session/{sessionId}/context',fields:['sessionId']},
  'session.message': {method:'POST',path:'/session/{sessionId}/message',fields:['sessionId']},
  'session.messages': {method:'GET',path:'/session/{sessionId}/message/list',fields:['sessionId']}
};
export function characterRequest(cfg:ThetaConfig,name:string,args:Record<string,unknown>) {
  const route=characterRoutes[name];
  if(!route) throw new Error('Unknown AI Characters operation');
  let path=route.path;
  for(const field of route.fields){
    if(typeof args[field]!=='string'||!(args[field] as string).trim())throw new Error(`${field} must be a non-empty string`);
    path=path.replace(`{${field}}`,pathSegment(args[field] as string,field));
  }
  if(['POST','PUT'].includes(route.method)&&(!args.payload||typeof args.payload!=='object'||Array.isArray(args.payload))) throw new Error('payload must be an object');
  if(cfg.dryRun&&route.method!=='GET')return {dryRun:true,method:route.method,path,payload:redactObject((args.payload ?? {}) as Record<string, unknown>)};
  if(route.method!=='GET')assertApproved(cfg, args.confirm,`theta.characters.${name}`);
  if(!cfg.charactersApiKey)throw new Error('THETA_CHARACTERS_API_KEY missing; use a game-scoped key, not an on-demand key');
  const url=`https://ai-chars-api.thetaedgecloud.com${path}`;
  const opts={headers:{Authorization:`Bearer ${cfg.charactersApiKey}`},service:'theta-characters',timeoutMs:cfg.httpTimeoutMs,maxRetries:route.method==='GET'?cfg.httpMaxRetries:0,retryBackoffMs:cfg.httpRetryBackoffMs};
  if(route.method==='GET')return getJson(url,opts);
  if(route.method==='POST')return postJson(url,args.payload,opts);
  if(route.method==='PUT')return putJson(url,args.payload,opts);
  return deleteEmpty(url,opts);
}
