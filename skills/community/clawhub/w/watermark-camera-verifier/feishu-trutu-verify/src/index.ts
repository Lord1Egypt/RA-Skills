import { basekit, FieldType, field, FieldComponent, FieldCode } from '@lark-opdev/block-basekit-server-api';
import * as crypto from 'crypto';

const { t } = field;

// 声明域名白名单（必须，否则请求被拒绝）
basekit.addDomainList(['openapi.xhey.top']);

// 两阶段 HMAC-SHA256 + Base64 签名（⚠️ 必须用 base64，不是 hex）
function buildTrutuHeaders(groupKey: string, groupSecret: string, body: object): Record<string, string> {
  const bodyStr = JSON.stringify(body);
  const timestamp = Math.floor(Date.now() / 1000).toString(); // ⚠️ 秒级，不是毫秒
  const sign = (secret: string, data: string) =>
    crypto.createHmac('sha256', secret).update(data, 'utf8').digest('base64');
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
const ERROR_MAP: Record<number, string> = {
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
function formatPhotoResult(photo: any, idx: number): string {
  if (photo.status === 0) {
    return `照片${idx + 1}：✅验真通过 | 时间：${photo.photoTime} | 地点：${photo.photoAddress} | 坐标：${photo.lat},${photo.lng}`;
  }
  const msg = ERROR_MAP[photo.status] ?? '验真未通过';
  return `照片${idx + 1}：❌${msg}（状态码：${photo.status}）`;
}

const BASE_URL = 'https://openapi.xhey.top';

basekit.addField({
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
      component: FieldComponent.FieldSelect,
      props: {
        supportType: [FieldType.Attachment],
        placeholder: t('attachmentsPlaceholder'),
      },
      validator: { required: true },
    },
    {
      key: 'groupKey',
      label: t('groupKeyLabel'),
      component: FieldComponent.Input,
      props: { placeholder: t('groupKeyPlaceholder') },
      validator: { required: true },
    },
    {
      key: 'groupSecret',
      label: t('groupSecretLabel'),
      component: FieldComponent.Input,
      props: { placeholder: t('groupSecretPlaceholder') },
      validator: { required: true },
    },
  ],
  resultType: {
    type: FieldType.Text, // data 必须为字符串
  },
  execute: async (
    formItemParams: {
      attachments: Array<{ name: string; size: number; type: string; tmp_url: string }>;
      groupKey: string;
      groupSecret: string;
    },
    context,
  ) => {
    // 日志工具（每次修改版本号方便定位）
    function debugLog(arg: any, showContext = false) {
      if (!showContext) {
        console.log(JSON.stringify({ arg, logID: context.logID }), '\n');
        return;
      }
      console.log(JSON.stringify({ formItemParams: { ...formItemParams, groupSecret: '***' }, context, arg }), '\n');
    }

    debugLog('=====trutu-verify=====v1', true);

    // 封装 fetch：先取 text 再 parse，自动记日志
    const safeFetch = async (url: string, init: RequestInit): Promise<any> => {
      try {
        const res = await context.fetch(url, init);
        const resText = await res.text();
        debugLog({ [`fetch ${url}`]: resText.slice(0, 2000) });
        return JSON.parse(resText);
      } catch (e) {
        debugLog({ [`fetch error ${url}`]: String(e) });
        throw e;
      }
    };

    const { attachments, groupKey, groupSecret } = formItemParams;

    if (!attachments?.length) {
      return { code: FieldCode.Success, data: '无图片' };
    }
    if (!groupKey || !groupSecret) {
      return { code: FieldCode.ConfigError };
    }

    // 验证单张照片
    async function verifyOne(tmpUrl: string, photoIdx: number): Promise<string> {
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
        if (!taskID) return `照片${photoIdx + 1}：❌未获取到taskID`;

        // Step 2: 轮询（最多10次，间隔2s，最长等待20s）
        for (let i = 0; i < 10; i++) {
          if (i > 0) await new Promise(r => setTimeout(r, 2000));

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
          if (taskStatus === 6) return `照片${photoIdx + 1}：❌任务已取消`;
        }
        return `照片${photoIdx + 1}：❌轮询超时`;
      } catch (e: any) {
        return `照片${photoIdx + 1}：❌异常（${e?.message ?? String(e)}）`;
      }
    }

    try {
      // 并发验证所有照片
      const results = await Promise.all(
        attachments.map((att, idx) => verifyOne(att.tmp_url, idx)),
      );

      const output = results.join('\n');
      debugLog({ '===result': output });

      return {
        code: FieldCode.Success,
        data: output, // 多张照片结果串联为一个字符串
      };
    } catch (e: any) {
      debugLog({ '===error': String(e) });
      return { code: FieldCode.Error };
    }
  },
});

export default basekit;
