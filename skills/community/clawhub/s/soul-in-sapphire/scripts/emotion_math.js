// Coordinate handling only: interpretation remains with the caller.
export const AXES = ['arousal','valence','focus','confidence','stress','curiosity','social','solitude','joy','anger','sadness','fun','pain'];
export const SCALE = {version:2, baseline:0, min:-5, max:5};
export const NORMAL_HALF_LIFE_HOURS=24;
export function finiteNumber(value){
 if(value===null||value===undefined||value===''||typeof value==='boolean')return null;
 const n=Number(value);return Number.isFinite(n)?n:null;
}
export function centeredState(raw={}){
 const version=raw.__meta?.version??1;
 if(![1,2].includes(version))throw Error('Unsupported state scale version');
 const out=structuredClone(raw);
 for(const ax of AXES){
  const n=finiteNumber(raw[ax]);
  if(n===null){if(ax in raw)out[ax]=null;continue;}
  if(n<(version===1?0:-5)||n>(version===1?10:5))throw Error('Out-of-range state axis: '+ax);
  out[ax]=version===1?n-5:n;
 }
 out.__meta={...raw.__meta,...SCALE};
 return out;
}
export function projectState(raw,from,to){
 const state=centeredState(raw),start=Date.parse(from),end=Date.parse(to);
 if(!Number.isFinite(start)||!Number.isFinite(end))throw Error('Invalid state/event timestamp');
 if(end<start)throw Error('Event precedes base state; use historical repair, not a current tick');
 const hours=(end-start)/3600000,halfLives={};
 for(const imprint of state.imprints||[]){
  if(!AXES.includes(imprint.axis))continue;
  const explicit=finiteNumber(imprint.decay_half_life_hours);
  const severity=finiteNumber(imprint.severity)??0; // severity retains its original 0..10 meaning.
  halfLives[imprint.axis]=explicit>0?explicit:24*(1+Math.max(0,Math.min(10,severity)));
 }
 for(const ax of AXES){
  const n=finiteNumber(state[ax]);
  if(n!==null)state[ax]=n*Math.pow(0.5,hours/(halfLives[ax]||24));
 }
 return state;
}
export function advanceState(raw,from,to,emotions=[],event={}){
 const state=from?projectState(raw,from,to):centeredState(raw);
 for(const ax of AXES)if(!(ax in state))state[ax]=from?null:0;
 for(const emo of emotions){
  if(!AXES.includes(emo.axis))throw Error('Unsupported emotion axis: '+emo.axis);
  const level=finiteNumber(emo.level);
  if(level===null)continue; // Missing is not a measured zero.
  if(level<-5||level>5)throw Error('Emotion level must be -5..5');
  const current=finiteNumber(state[emo.axis]);
  if(current===null)throw Error('Cannot accumulate onto a missing state axis: '+emo.axis);
  state[emo.axis]=Math.max(-5,Math.min(5,current+level));
 }
 const imprints=structuredClone(state.imprints||[]);
 const control=finiteNumber(event.control);
 for(const emo of emotions){
  const level=finiteNumber(emo.level);
  if(level===null||level<4||(control!==null&&control>3))continue;
  const severity=level+5; // Preserve original strong-positive threshold and half-life.
  imprints.push({tag:'imprint:'+emo.axis+':'+(event.trigger||'event'),axis:emo.axis,severity,
   created_at:to,decay_half_life_hours:24*(1+severity),notes:emo.comment||''});
 }
 const seen=new Set();
 state.imprints=imprints.reverse().filter(i=>{const key=i.tag+'|'+i.created_at;if(seen.has(key))return false;seen.add(key);return true;}).reverse();
 state.__meta={...state.__meta,...SCALE};
 return state;
}
export function initialState(){return {...Object.fromEntries(AXES.map(ax=>[ax,0])),__meta:{...SCALE}};}
