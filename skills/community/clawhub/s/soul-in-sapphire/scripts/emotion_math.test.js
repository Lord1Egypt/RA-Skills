import test from 'node:test';
import assert from 'node:assert/strict';
import {centeredState,advanceState,projectState,initialState} from './emotion_math.js';
const at='2026-10-05T09:00:00Z',before='2026-10-04T09:00:00Z';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-10,a+' != '+b);
test('legacy 0 is -5, not missing; centered 0 stays neutral',()=>{
 assert.equal(centeredState({anger:0}).anger,-5);
 assert.equal(centeredState({anger:0,__meta:{version:2}}).anger,0);
 assert.equal(centeredState({stress:null}).stress,null);
});
test('both sides decay toward zero and retain imprint half-life',()=>{
 near(projectState({joy:9},before,at).joy,2);
 near(projectState({joy:1},before,at).joy,-2);
 near(projectState({anger:0},before,at).anger,-2.5);
 near(projectState({joy:9,imprints:[{axis:'joy',severity:9,decay_half_life_hours:240}]},before,at).joy,4*Math.pow(0.5,.1));
});
test('neutral start, 0 value, null impulse and negative impulse are distinct',()=>{
 assert.equal(advanceState(initialState(),null,at,[{axis:'joy',level:1}]).joy,1);
 assert.equal(advanceState({anger:0},at,at,[{axis:'anger',level:1}]).anger,-4);
 assert.equal(advanceState({anger:0},at,at,[]).stress,null);
 assert.equal(advanceState(initialState(),null,at,[{axis:'stress',level:null}]).stress,0);
 assert.equal(advanceState(initialState(),null,at,[{axis:'stress',level:-2}]).stress,-2);
 assert.throws(()=>advanceState({stress:null},at,at,[{axis:'stress',level:1}]),/missing/);
});
test('ordinary daily +2 converges toward +4 and imprint semantics remain',()=>{
 let state=initialState(),from=null;
 for(let i=0;i<20;i++){const to=new Date(Date.parse(at)+i*86400000).toISOString();state=advanceState(state,from,to,[{axis:'joy',level:2}]);from=to;}
 near(state.joy,4-Math.pow(.5,19)*2);
 const strong=advanceState(initialState(),null,at,[{axis:'joy',level:4}],{control:2});
 assert.equal(strong.imprints[0].severity,9);assert.equal(strong.imprints[0].decay_half_life_hours,240);
});
test('invalid range, future base, unsupported version and axes fail',()=>{
 assert.throws(()=>centeredState({joy:11}),/range/);
 assert.throws(()=>projectState({joy:7},at,before),/precedes/);
 assert.throws(()=>centeredState({__meta:{version:99}}),/version/);
 assert.throws(()=>advanceState(initialState(),null,at,[{axis:'unknown',level:1}]),/axis/);
});
