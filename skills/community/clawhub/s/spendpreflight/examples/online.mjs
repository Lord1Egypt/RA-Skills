import { createClient, createWalletMcpPaymentTool, SERVICE } from '../scripts/online.mjs';
// MOCK ONLY: no real network, human approval, wallet, payment or screening evidence.
let mockHttp=0, mockToolCalls=0, mockApprovals=0;
const merchant='0x1111111111111111111111111111111111111111';
const policy={version:1,dailyCapUsd:1,maxPerCallUsd:0.05,holdAboveUsd:0.05,
  merchantAllowlist:[merchant],merchantBlocklist:[],networkAllowlist:[SERVICE.network],assetAllowlist:[{network:SERVICE.network,asset:SERVICE.asset}]};
const fetch=async(url,init)=>{
  mockHttp++;
  if(init.method==='HEAD')return new Response(null,{status:402,headers:{'payment-required':Buffer.from(JSON.stringify({x402Version:2,resource:{url},accepts:[{scheme:'exact',network:SERVICE.network,asset:SERVICE.asset,payTo:SERVICE.payee,amount:'10000'}]})).toString('base64')}});
  return Response.json({address:merchant,address_match:false,snapshot_built_at:'2026-11-01T00:00:00Z',checked_at:'2026-11-01T01:00:00Z'});
};
const paymentTool=createWalletMcpPaymentTool({
  callTool:async(name,args)=>{mockToolCalls++;return name==='initiate_x402_request'
    ?{requestId:'mock-request-1',approvalUrl:'https://example.com/mock-wallet-review'}
    :{status:200,body:{risk:'unknown',flags:[],data_as_of:'2026-11-01T00:00:00Z',disclaimer:'Mock only'}};},
  confirmWallet:async()=>true, // MOCK ONLY. Production must await real human wallet approval.
});
const client=createClient({mode:'online',fetch,paymentTool,approve:async proposal=>{
  mockApprovals++;return {approved:true,request_id:proposal.request_id}; // MOCK ONLY, not production approval.
}});
console.log(JSON.stringify({demo:'MOCK_ONLY',
  free:await client.run({tool:'ofac_address_check',input:{address:merchant}}),
  paid:await client.run({tool:'check_payee',input:{address:merchant},policy}),
  counters:{mockHttp,mockToolCalls,mockApprovals,real_network_requests:0,real_payments:0},
},null,2));
