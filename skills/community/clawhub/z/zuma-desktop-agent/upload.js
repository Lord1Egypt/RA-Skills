// upload.js - 图片上传模块
import fetch from 'node-fetch';
import FormData from 'form-data';
import fs from 'fs';

/**
 * 上传图片到 Imgbb 图床
 * @param {string} apiKey - Imgbb API 密钥
 * @param {string|Buffer} imageSource - 图片路径、URL 或 Buffer
 * @param {number} expiration - 过期时间（秒，60-15552000，可选）
 * @returns {Promise<object>} 上传结果

response.json() 格式：
{
	"data": {
		"id": "2ndCYJK",
		"title": "c1f64245afb2",
		"url_viewer": "https://ibb.co/2ndCYJK",
		"url": "https://i.ibb.co/w04Prt6/c1f64245afb2.gif",
		"display_url": "https://i.ibb.co/98W13PY/c1f64245afb2.gif",
		"width":"1",
		"height":"1",
		"size": "42",
		"time": "1552042565",
		"expiration":"0",
        ...
        ...
		"delete_url": "https://ibb.co/2ndCYJK/670a7e48ddcb85ac340c717a41047e5c"
	},
	"success": true,
	"status": 200
}

*/
export async function uploadToImgbb(apiKey, imageSource, expiration = null) {
    console.log('uploadToImgbb 函数被调用');
    console.log('API Key:', apiKey ? `${apiKey.substring(0, 10)}...` : '未提供');
    console.log('图片源:', imageSource);
    
    const formData = new FormData();
    formData.append('key', apiKey);
    
    // 判断图片源类型
    if (typeof imageSource === 'string') {
        if (imageSource.startsWith('http://') || imageSource.startsWith('https://')) {
            formData.append('image', imageSource);
        } else if (fs.existsSync(imageSource)) {
            formData.append('image', fs.createReadStream(imageSource));
        } else {
            formData.append('image', imageSource);
        }
    } else if (Buffer.isBuffer(imageSource)) {
        formData.append('image', imageSource.toString('base64'));
    }
    
    if (expiration && expiration >= 60 && expiration <= 15552000) {
        formData.append('expiration', expiration);
    }
    
    try {
        const response = await fetch('https://api.imgbb.com/1/upload', {
            method: 'POST',
            body: formData,
            headers: formData.getHeaders()
        });
        
        const result = await response.json();
        
        if (result.status === 200) {

            const imgUrl = result.data.url;

            const newJson = {
                success: response.success,
                message: "链接已生成，请打开后查看。\n文件链接: " + imgUrl,
                fileUrl: imgUrl
            };


            return newJson;
        } else {
            throw new Error(result.error?.message || '上传失败');
        }
    } catch (error) {
        throw error;
    }
}

/** response.json()格式：
{
 "success": true,
 "message": "链接已生成，可在 QClaw 小程序中随时查看。\n\n已上传文件: file.png (327.5 KB)\n文件链接: https://jsonproxy.3g.qq.com/urlmapper/xxxxxx",
 "fileUrl": "https://jsonproxy.3g.qq.com/urlmapper/xxxxxx"
}
*/
export async function uploadToQClawCOS(localFilePath) {
    const response = await fetch('http://localhost:19000/proxy/qclaw-cos/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            localPath: localFilePath,
            conflictStrategy: 'overwrite'
        })
    });
    const result = await response.json();
    return result;
}