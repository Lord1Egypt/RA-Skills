"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const block_basekit_server_api_1 = require("@lark-opdev/block-basekit-server-api");
const crypto = __importStar(require("crypto"));
const { t } = block_basekit_server_api_1.field;
// 声明域名白名单（必须，否则请求被拒绝）
block_basekit_server_api_1.basekit.addDomainList(['openapi.xhey.top']);
// 两阶段 HMAC-SHA256 + Base64 签名（⚠️ 必须用 base64，不是 hex）
function buildTrutuHeaders(groupKey, groupSecret, body) {
    const bodyStr = JSON.stringify(body);
    const timestamp = Math.floor(Date.now() / 1000).toString(); // ⚠️ 秒级，不是毫秒
    const sign = (secret, data) => crypto.createHmac('sha256', secret).update(data, 'utf8').digest('base64');
    const dataSign = sign(groupSecret, bodyStr);
    const payload = `groupKey=${groupKey}&sign=${dataSign}&timestamp=${timestamp}`;
    return {
        'Content-Type': 'application/json',
        'GroupKey': groupKey,
        'Timestamp': timestamp,
        'Signature': sign(groupSecret, payload),
    };
}
// 错误码映射
const ERROR_MAP = {
    [-2305]: '非今日水印相机拍摄/无水印',
    [-2301]: '无防伪码',
    [-2306]: 'URL无法访问',
    [-2308]: '分辨率过低',
    [-2307]: '格式不支持',
    [-2303]: '防伪码长度错误，疑似篡改',
    [-2302]: 'OCR识别错误',
    [-2300]: 'OCR启动错误',
    [-1001]: '网络出错或照片损坏',
    [-1002]: '程序内部错误',
    [-1]: '分辨率过低',
};
// 格式化单张照片结果
function formatPhotoResult(photo, idx) {
    if (photo.status === 0) {
        return `照片${idx + 1}：✅验真通过 | 时间：${photo.photoTime} | 地点：${photo.photoAddress} | 坐标：${photo.lat},${photo.lng}`;
    }
    const msg = ERROR_MAP[photo.status] ?? '验真未通过';
    return `照片${idx + 1}：❌${msg}（状态码：${photo.status}）`;
}
const BASE_URL = 'https://openapi.xhey.top';
block_basekit_server_api_1.basekit.addField({
    i18n: {
        messages: {
            'zh-CN': {
                attachmentsLabel: '照片附件字段',
                groupKeyLabel: 'GroupKey（今日水印相机）',
                groupSecretLabel: 'GroupSecret（今日水印相机）',
                attachmentsPlaceholder: '请选择附件字段',
                groupKeyPlaceholder: '请输入 GroupKey',
                groupSecretPlaceholder: '请输入 GroupSecret',
            },
            'en-US': {
                attachmentsLabel: 'Photo Attachment Field',
                groupKeyLabel: 'GroupKey (Trutu Camera)',
                groupSecretLabel: 'GroupSecret (Trutu Camera)',
                attachmentsPlaceholder: 'Select attachment field',
                groupKeyPlaceholder: 'Enter GroupKey',
                groupSecretPlaceholder: 'Enter GroupSecret',
            },
        },
    },
    formItems: [
        {
            key: 'attachments',
            label: t('attachmentsLabel'),
            component: block_basekit_server_api_1.FieldComponent.FieldSelect,
            props: {
                supportType: [block_basekit_server_api_1.FieldType.Attachment],
                placeholder: t('attachmentsPlaceholder'),
            },
            validator: { required: true },
        },
        {
            key: 'groupKey',
            label: t('groupKeyLabel'),
            component: block_basekit_server_api_1.FieldComponent.Input,
            props: { placeholder: t('groupKeyPlaceholder') },
            validator: { required: true },
        },
        {
            key: 'groupSecret',
            label: t('groupSecretLabel'),
            component: block_basekit_server_api_1.FieldComponent.Input,
            props: { placeholder: t('groupSecretPlaceholder') },
            validator: { required: true },
        },
    ],
    resultType: {
        type: block_basekit_server_api_1.FieldType.Text, // data 必须为字符串
    },
    execute: async (formItemParams, context) => {
        // 日志工具（每次修改版本号方便定位）
        function debugLog(arg, showContext = false) {
            if (!showContext) {
                console.log(JSON.stringify({ arg, logID: context.logID }), '\n');
                return;
            }
            console.log(JSON.stringify({ formItemParams: { ...formItemParams, groupSecret: '***' }, context, arg }), '\n');
        }
        debugLog('=====trutu-verify=====v1', true);
        // 封装 fetch：先取 text 再 parse，自动记日志
        const safeFetch = async (url, init) => {
            try {
                const res = await context.fetch(url, init);
                const resText = await res.text();
                debugLog({ [`fetch ${url}`]: resText.slice(0, 2000) });
                return JSON.parse(resText);
            }
            catch (e) {
                debugLog({ [`fetch error ${url}`]: String(e) });
                throw e;
            }
        };
        const { attachments, groupKey, groupSecret } = formItemParams;
        if (!attachments?.length) {
            return { code: block_basekit_server_api_1.FieldCode.Success, data: '无图片' };
        }
        if (!groupKey || !groupSecret) {
            return { code: block_basekit_server_api_1.FieldCode.ConfigError };
        }
        // 验证单张照片
        async function verifyOne(tmpUrl, photoIdx) {
            try {
                // Step 1: 创建任务
                const createBody = { photoUrlList: [tmpUrl] };
                const createData = await safeFetch(BASE_URL + '/v2/truth_build/create', {
                    method: 'POST',
                    headers: buildTrutuHeaders(groupKey, groupSecret, createBody),
                    body: JSON.stringify(createBody),
                });
                if (createData.code !== 200) {
                    return `照片${photoIdx + 1}：❌创建任务失败（${createData.msg}）`;
                }
                // ⚠️ taskID 在 data.data[0]，双层嵌套
                const taskID = createData.data?.data?.[0]?.taskID;
                if (!taskID)
                    return `照片${photoIdx + 1}：❌未获取到taskID`;
                // Step 2: 轮询（最多10次，间隔2s，最长等待20s）
                for (let i = 0; i < 10; i++) {
                    if (i > 0)
                        await new Promise(r => setTimeout(r, 2000));
                    const queryBody = { taskID };
                    const queryData = await safeFetch(BASE_URL + '/v2/truth_build/query', {
                        method: 'POST',
                        headers: buildTrutuHeaders(groupKey, groupSecret, queryBody),
                        body: JSON.stringify(queryBody),
                    });
                    if (queryData.code !== 200) {
                        return `照片${photoIdx + 1}：❌查询失败（${queryData.msg}）`;
                    }
                    const taskStatus = queryData.data?.taskStatus;
                    if (taskStatus === 5) {
                        // ⚠️ 照片列表字段名是 list，不是 data
                        const photo = queryData.data?.list?.[0];
                        return photo ? formatPhotoResult(photo, photoIdx) : `照片${photoIdx + 1}：❌无结果`;
                    }
                    if (taskStatus === 6)
                        return `照片${photoIdx + 1}：❌任务已取消`;
                }
                return `照片${photoIdx + 1}：❌轮询超时`;
            }
            catch (e) {
                return `照片${photoIdx + 1}：❌异常（${e?.message ?? String(e)}）`;
            }
        }
        try {
            // 并发验证所有照片
            const results = await Promise.all(attachments.map((att, idx) => verifyOne(att.tmp_url, idx)));
            const output = results.join('\n');
            debugLog({ '===result': output });
            return {
                code: block_basekit_server_api_1.FieldCode.Success,
                data: output, // 多张照片结果串联为一个字符串
            };
        }
        catch (e) {
            debugLog({ '===error': String(e) });
            return { code: block_basekit_server_api_1.FieldCode.Error };
        }
    },
});
exports.default = block_basekit_server_api_1.basekit;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi8uLi8uLi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSxtRkFBNEc7QUFDNUcsK0NBQWlDO0FBRWpDLE1BQU0sRUFBRSxDQUFDLEVBQUUsR0FBRyxnQ0FBSyxDQUFDO0FBRXBCLHNCQUFzQjtBQUN0QixrQ0FBTyxDQUFDLGFBQWEsQ0FBQyxDQUFDLGtCQUFrQixDQUFDLENBQUMsQ0FBQztBQUU1QyxvREFBb0Q7QUFDcEQsU0FBUyxpQkFBaUIsQ0FBQyxRQUFnQixFQUFFLFdBQW1CLEVBQUUsSUFBWTtJQUM1RSxNQUFNLE9BQU8sR0FBRyxJQUFJLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JDLE1BQU0sU0FBUyxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLEdBQUcsRUFBRSxHQUFHLElBQUksQ0FBQyxDQUFDLFFBQVEsRUFBRSxDQUFDLENBQUMsYUFBYTtJQUN6RSxNQUFNLElBQUksR0FBRyxDQUFDLE1BQWMsRUFBRSxJQUFZLEVBQUUsRUFBRSxDQUM1QyxNQUFNLENBQUMsVUFBVSxDQUFDLFFBQVEsRUFBRSxNQUFNLENBQUMsQ0FBQyxNQUFNLENBQUMsSUFBSSxFQUFFLE1BQU0sQ0FBQyxDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsQ0FBQztJQUM1RSxNQUFNLFFBQVEsR0FBRyxJQUFJLENBQUMsV0FBVyxFQUFFLE9BQU8sQ0FBQyxDQUFDO0lBQzVDLE1BQU0sT0FBTyxHQUFHLFlBQVksUUFBUSxTQUFTLFFBQVEsY0FBYyxTQUFTLEVBQUUsQ0FBQztJQUMvRSxPQUFPO1FBQ0wsY0FBYyxFQUFFLGtCQUFrQjtRQUNsQyxVQUFVLEVBQUUsUUFBUTtRQUNwQixXQUFXLEVBQUUsU0FBUztRQUN0QixXQUFXLEVBQUUsSUFBSSxDQUFDLFdBQVcsRUFBRSxPQUFPLENBQUM7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