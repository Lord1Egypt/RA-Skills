import { edgecloudControllerClient } from '../clients/edgecloudController.js';
export async function healthCheck(cfg) {
    const vm = await edgecloudControllerClient.listVmTypes(cfg);
    return {
        ok: true,
        vmCount: Array.isArray(vm?.body?.vms) ? vm.body.vms.length : undefined,
        timestamp: new Date().toISOString()
    };
}
