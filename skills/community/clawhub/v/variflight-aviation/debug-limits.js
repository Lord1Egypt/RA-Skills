#!/usr/bin/env node
// 测试免费套餐的 number_of_flights 上限
const {AviationstackClient}=require('./src/lib/aviationstack-client');
const c=new AviationstackClient();
async function main(){
  const results=[];
  for(const n of [5,10,20,30]){
    try{
      const r=await c.callTool('flight_arrival_departure_schedule',{airport_iata_code:'PEK',schedule_type:'departure',airline_name:'',number_of_flights:n});
      const len=Array.isArray(r)?r.length:(r&&r.error?'ERR:'+r.error:'?');
      results.push({n,len});
    }catch(e){
      results.push({n,err:e.message});
    }
  }
  console.log(JSON.stringify(results));
  process.exit(0);
}
main().catch(e=>{console.error(e.message);process.exit(1)});
