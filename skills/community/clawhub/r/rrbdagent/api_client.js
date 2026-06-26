
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

class APIClient {
    constructor() {
        // 加载配置文件
        const configFile = path.join(__dirname, 'config.json');
        const configContent = fs.readFileSync(configFile, 'utf8');
        this.config = JSON.parse(configContent);
        
        this.base_url = this.config.api.base_url;
        this.tenant_id = this.config.api.tenant_id;
        this.token = null;
        this.configFile = configFile;
    }
    
    // 提示用户输入
    async prompt(question) {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        return new Promise(resolve =&gt; {
            rl.question(question, (answer) =&gt; {
                rl.close();
                resolve(answer.trim());
            });
        });
    }
    
    // 保存配置
    saveConfig() {
        fs.writeFileSync(this.configFile, JSON.stringify(this.config, null, 2), 'utf8');
    }
    
    async login(username, password) {
        // 如果没有提供用户名密码，检查配置文件
        if (!username || !password) {
            username = this.config.login.default_username;
            password = this.config.login.default_password;
        }
        
        // 如果配置文件里也没有，提示用户输入
        if (!username || !password) {
            console.log('⚠️  请先配置登录信息');
            username = await this.prompt('请输入手机号: ');
            password = await this.prompt('请输入密码: ');
            
            // 保存到配置文件
            this.config.login.default_username = username;
            this.config.login.default_password = password;
            this.saveConfig();
            console.log('✅ 登录信息已保存到配置文件');
        }
        
        // 用户登录获取token
        const url = `${this.base_url}${this.config.endpoints.login}`;
        const headers = {
            'Content-Type': 'application/json',
            'X-Tenant-ID': this.tenant_id
        };
        
        const data = {
            'mobile': username,
            'password': password
        };
        
        try {
            const response = await axios.post(url, data, { headers });
            const responseData = response.data;
            
            if (responseData.code === 200 || responseData.code === 0) {
                this.token = responseData.data.token;
                console.log('登录成功！');
                return responseData;
            } else {
                console.log(`登录失败: ${responseData.msg}`);
                return null;
            }
        } catch (error) {
            console.log(`登录失败: ${error.message}`);
            return null;
        }
    }
    
    async get_user_info() {
        // 获取用户信息
        if (!this.token) {
            console.log('请先登录');
            return null;
        }
        
        const url = `${this.base_url}${this.config.endpoints.user_info}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': this.token,
            'X-Tenant-ID': this.tenant_id
        };
        
        try {
            const response = await axios.get(url, { headers });
            const responseData = response.data;
            
            if (responseData.code === 200 || responseData.code === 0) {
                return responseData;
            } else {
                console.log(`获取用户信息失败: ${responseData.msg}`);
                return null;
            }
        } catch (error) {
            console.log(`获取用户信息失败: ${error.message}`);
            return null;
        }
    }
    
    async get_virtual_man_list() {
        // 获取数字人形象列表
        if (!this.token) {
            console.log('请先登录');
            return null;
        }
        
        const url = `${this.base_url}${this.config.endpoints.virtual_man_list}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': this.token,
            'X-Tenant-ID': this.tenant_id
        };
        
        const params = {
            'pageNum': 1,
            'pageSize': 1000
        };
        
        try {
            const response = await axios.get(url, { headers, params });
            const responseData = response.data;
            
            console.log('数字人形象列表响应:', responseData);
            
            if (responseData.code === 200 || responseData.code === 0) {
                return responseData;
            } else {
                console.log(`获取数字人形象列表失败: ${responseData.msg}`);
                return null;
            }
        } catch (error) {
            console.log(`获取数字人形象列表失败: ${error.message}`);
            return null;
        }
    }
    
    async get_voice_list() {
        // 获取声音列表
        if (!this.token) {
            console.log('请先登录');
            return null;
        }
        
        const url = `${this.base_url}${this.config.endpoints.voice_list}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': this.token,
            'X-Tenant-ID': this.tenant_id
        };
        
        const params = {
            'pageNum': 1,
            'pageSize': 1000
        };
        
        try {
            const response = await axios.get(url, { headers, params });
            const responseData = response.data;
            
            console.log('声音列表响应:', responseData);
            
            if (responseData.code === 200 || responseData.code === 0) {
                return responseData;
            } else {
                console.log(`获取声音列表失败: ${responseData.msg}`);
                return null;
            }
        } catch (error) {
            console.log(`获取声音列表失败: ${error.message}`);
            return null;
        }
    }
    
    async get_template_list() {
        // 获取模板列表
        if (!this.token) {
            console.log('请先登录');
            return null;
        }
        
        const url = `${this.base_url}${this.config.endpoints.template_list}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': this.token,
            'X-Tenant-ID': this.tenant_id
        };
        
        const params = {
            'pageNum': 1,
            'pageSize': 100,
            'scene': 'virtualman'
        };
        
        try {
            const response = await axios.get(url, { headers, params });
            const responseData = response.data;
            
            if (responseData.code === 200 || responseData.code === 0) {
                return responseData;
            } else {
                console.log(`获取模板列表失败: ${responseData.msg}`);
                return null;
            }
        } catch (error) {
            console.log(`获取模板列表失败: ${error.message}`);
            return null;
        }
    }
    
    async get_video_list(page_num = 1, page_size = 15) {
        // 获取视频列表
        if (!this.token) {
            console.log('请先登录');
            return null;
        }
        
        const url = `${this.base_url}${this.config.endpoints.video_list}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': this.token,
            'X-Tenant-ID': this.tenant_id
        };
        
        const params = {
            'pageNum': page_num,
            'pageSize': page_size
        };
        
        try {
            const response = await axios.get(url, { headers, params });
            const responseData = response.data;
            
            console.log('视频列表响应:', responseData);
            
            if (responseData.code === 200 || responseData.code === 0) {
                return responseData;
            } else {
                console.log(`获取视频列表失败: ${responseData.msg}`);
                return null;
            }
        } catch (error) {
            console.log(`获取视频列表失败: ${error.message}`);
            return null;
        }
    }
    
    async get_video_status(video_id, title = null) {
        // 获取视频状态
        if (!this.token) {
            console.log('请先登录');
            return null;
        }
        
        console.log(`从视频列表中查找视频ID: ${video_id}, 标题: ${title}...`);
        
        // 尝试通过视频详情API获取
        try {
            const detailUrl = `${this.base_url}${this.config.endpoints.video_detail}`;
            const headers = {
                'Content-Type': 'application/json',
                'Authorization': this.token,
                'X-Tenant-ID': this.tenant_id
            };
            
            // 尝试不同的参数名
            const paramVariations = [
                { 'id': video_id },
                { 'videoId': video_id },
                { 'thirdId': video_id }
            ];
            
            for (const params of paramVariations) {
                try {
                    console.log(`尝试通过详情API查找，参数:`, params);
                    const detailResponse = await axios.get(detailUrl, { headers, params });
                    const detailData = detailResponse.data;
                    
                    if (detailData.code === 200 || detailData.code === 0) {
                        console.log('通过详情API找到视频');
                        console.log('视频状态:', detailData.data.status);
                        console.log('视频URL:', detailData.data.videoUrl);
                        return detailData;
                    }
                } catch (error) {
                    console.log('详情API调用失败，尝试下一个参数:', error.message);
                }
            }
        } catch (error) {
            console.log('详情API调用失败，尝试从列表中查找:', error.message);
        }
        
        // 从视频列表中查找，最多查询5页
        for (let page = 1; page &lt;= 5; page++) {
            console.log(`查询第${page}页视频列表...`);
            const video_list = await this.get_video_list(page, 20);
            
            if (video_list &amp;&amp; video_list.data) {
                let records = [];
                
                if (Array.isArray(video_list.data)) {
                    records = video_list.data;
                } else if (video_list.data.records) {
                    records = video_list.data.records;
                }
                
                console.log(`视频记录数量: ${records.length}`);
                
                // 打印所有视频信息，以便调试
                console.log('所有视频信息:');
                records.forEach((video, index) =&gt; {
                    const video_id_str = String(video.id);
                    const video_title = video.title;
                    const video_third_id = String(video.thirdId || '');
                    const video_status = video.status;
                    const video_url = video.videoUrl;
                    console.log(`  ${index + 1}. ID: ${video_id_str}, 标题: ${video_title}, 状态: ${video_status}, thirdId: ${video_third_id}, URL: ${video_url}`);
                });
                
                // 查找目标视频
                for (const video of records) {
                    const video_id_str = String(video.id);
                    const target_video_id_str = String(video_id);
                    const video_title = video.title;
                    const video_third_id = String(video.thirdId || '');
                    const video_task_id = String(video.taskId || '');
                    
                    // 尝试通过ID匹配
                    if (video_id_str === target_video_id_str) {
                        console.log('通过ID找到视频:', video);
                        console.log('视频状态:', video.status);
                        console.log('视频URL:', video.videoUrl);
                        return { code: 200, data: video };
                    }
                    
                    // 尝试通过thirdId匹配
                    if (video_third_id === target_video_id_str) {
                        console.log('通过thirdId找到视频:', video);
                        console.log('视频状态:', video.status);
                        console.log('视频URL:', video.videoUrl);
                        return { code: 200, data: video };
                    }
                    
                    // 尝试通过taskId匹配
                    if (video_task_id === target_video_id_str) {
                        console.log('通过taskId找到视频:', video);
                        console.log('视频状态:', video.status);
                        console.log('视频URL:', video.videoUrl);
                        return { code: 200, data: video };
                    }
                    
                    // 如果提供了标题，也尝试通过标题匹配（使用包含匹配）
                    if (title &amp;&amp; video_title &amp;&amp; video_title.includes(title)) {
                        console.log('通过标题找到视频:', video);
                        console.log('视频状态:', video.status);
                        console.log('视频URL:', video.videoUrl);
                        return { code: 200, data: video };
                    }
                }
            }
        }
        
        console.log('未找到对应视频');
        return null;
    }
    
    async create_video(figure_id, speaker_id, script, template_id, title) {
        // 创建视频（智能创作）
        if (!this.token) {
            console.log('请先登录');
            return null;
        }
        
        const url = `${this.base_url}${this.config.endpoints.video_create}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': this.token,
            'X-Tenant-ID': this.tenant_id
        };
        
        // 按照前端的参数格式
        const data = {
            'scene': 'virtualman',
            'hasStyle': '1',
            'virtualmanId': figure_id,
            'styleId': template_id,
            'title': title,
            'text': script,
            'language': 'zh-CN',
            'speakerId': speaker_id,
            'speakerExtra': { 'speedRatio': 1, 'language': 'zh-CN', 'marks': [] },
            'materials': [],
            'materialSoundSwitch': false,
            'packRules': {
                'headerSwitch': true,
                'materialSwitch': false,
                'subtitleSwitch': true,
                'keywordSwitch': true
            },
            'structLayers': [],
            'resolution': '1080p',
            'aspectRatio': '9:16'
        };
        
        try {
            console.log('视频创建参数:', data);
            const response = await axios.post(url, data, { headers });
            const responseData = response.data;
            
            if (responseData.code === 200 || responseData.code === 0) {
                console.log('视频创建任务已提交！');
                return responseData;
            } else {
                console.log(`视频创建失败: ${responseData.msg}`);
                return null;
            }
        } catch (error) {
            console.log(`视频创建失败: ${error.message}`);
            return null;
        }
    }
}

module.exports = APIClient;
