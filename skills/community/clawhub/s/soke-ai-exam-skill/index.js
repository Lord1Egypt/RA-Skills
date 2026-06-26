import { config, updateConfig } from './config.js';
import { examService } from './exam-service.js';
import { departmentService, userService } from './services.js';
import apiClient from './api-client.js';

/**
 * OpenClaw Skill 主类
 */
class AiExamSkill {
  constructor() {
    this.name = '授客AI智能出题考试系统';
    this.version = '1.0.0';
  }

  /**
   * 初始化配置
   */
  async initialize(appKey, appSecret, corpId) {
    updateConfig({ appKey, appSecret, corpId });
    console.log('✓ 配置初始化成功');
  }

  /**
   * 完整流程：上传文档 -> AI出题 -> 指派考试
   * @param {Object} options - 配置选项
   */
  async createAndAssignExam(options) {
    const {
      filePath,
      examTitle,
      questionTypes,
      creatorUserId,
      creatorUserName,
      creatorDeptUserId,
      creatorDeptUserName,
      assignUserNames = [],
      assignDeptNames = []
    } = options;

    console.log(`\n📝 开始创建考试: ${examTitle}`);

    // 1. 上传文件
    console.log('\n1️⃣ 上传文档到AI系统...');
    const fileInfo = await examService.uploadFile(filePath);
    console.log(`✓ 文件上传成功: ${fileInfo.filename}`);
    console.log(`  文件ID: ${fileInfo.id}`);

    // 2. AI出题
    console.log('\n2️⃣ AI智能出题中...');
    const examInfo = await examService.createExam({
      fileIds: [fileInfo.id],
      questionTypes,
      title: examTitle,
      userId: creatorUserId,
      userName: creatorUserName,
      deptUserId: creatorDeptUserId,
      deptUserName: creatorDeptUserName
    });
    console.log(`✓ 出题成功!`);
    console.log(`  考试ID: ${examInfo.uuid}`);
    console.log(`  题目数量: ${examInfo.question_count}`);
    console.log(`  总分: ${examInfo.total_score}`);
    console.log(`  及格分: ${examInfo.pass_score}`);

    // 3. 查询指派对象
    console.log('\n3️⃣ 查询指派对象...');
    const assignUserIds = [];
    const assignDeptIds = [];

    // 查询用户ID
    for (const userName of assignUserNames) {
      try {
        console.log(`  正在查询用户: ${userName}`);
        const users = await userService.searchByName(userName);
        console.log(`  查询结果: 找到 ${users.length} 个匹配用户`);
        if (users.length > 0) {
          users.forEach((u, idx) => {
            console.log(`    [${idx}] ${u.dept_user_name} (ID: ${u.dept_user_id})`);
          });
        }

        const userId = await userService.getUserId(userName);
        assignUserIds.push(userId);
        console.log(`✓ 找到用户: ${userName} (${userId})`);
      } catch (error) {
        console.log(`✗ 未找到用户: ${userName} - 错误: ${error.message}`);
      }
    }

    // 查询部门ID并获取部门下的人员
    for (const deptName of assignDeptNames) {
      try {
        const deptId = await departmentService.getDeptId(deptName);
        assignDeptIds.push(deptId);
        console.log(`✓ 找到部门: ${deptName} (${deptId})`);
        
        // 查询部门下的人员
        try {
          const deptUsers = await apiClient.request(
            'GET',
            '/oa/departmentUser/list',
            null,
            { dept_id: deptId, page_size: 100 }
          );
          
          if (deptUsers.data && deptUsers.data.list && deptUsers.data.list.length > 0) {
            const deptUserIds = deptUsers.data.list.map(u => u.dept_user_id);
            assignUserIds.push(...deptUserIds);
            console.log(`  └─ 找到 ${deptUserIds.length} 个部门成员`);
          } else {
            console.log(`  └─ 部门下没有成员`);
          }
        } catch (error) {
          console.log(`  └─ 查询部门成员失败: ${error.message}`);
        }
      } catch (error) {
        console.log(`✗ 未找到部门: ${deptName}`);
      }
    }

    // 4. 指派考试（只按用户ID指派）
    if (assignUserIds.length > 0) {
      console.log('\n4️⃣ 指派考试...');
      console.log(`  考试ID: ${examInfo.uuid}`);
      console.log(`  指派用户ID列表: ${assignUserIds.join(', ')}`);
      console.log(`  操作者: ${creatorUserName} (${creatorDeptUserId})`);

      try {
        const result = await examService.assignExam(
          examInfo.uuid,
          assignUserIds,
          [], // 不传递部门ID，只按用户ID指派
          {
            userId: creatorUserId,
            userName: creatorUserName,
            deptUserId: creatorDeptUserId,
            deptUserName: creatorDeptUserName
          }
        );
        console.log(`✓ 指派成功!`);
        console.log(`  API响应: ${JSON.stringify(result)}`);
        console.log(`  指派用户数: ${assignUserIds.length}`);
      } catch (error) {
        console.log(`✗ 指派失败: ${error.message}`);
        throw error;
      }
    } else {
      console.log('\n⚠️  未找到有效的指派对象，跳过指派步骤');
    }

    console.log('\n✅ 考试创建完成!\n');

    return {
      examId: examInfo.uuid,
      examTitle: examInfo.title,
      questionCount: examInfo.question_count,
      totalScore: examInfo.total_score,
      passScore: examInfo.pass_score,
      assignedUsers: assignUserIds.length,
      assignedDepts: assignDeptIds.length
    };
  }

  /**
   * 获取学员考试结果
   * @param {string} examId - 考试ID
   * @param {string} userName - 用户名
   */
  async getExamResult(examId, userName) {
    console.log(`\n📊 查询考试结果: ${userName}`);

    // 1. 查询用户ID
    const userId = await userService.getUserId(userName);
    console.log(`✓ 找到用户: ${userName} (${userId})`);

    // 2. 获取考试详情
    const examInfo = await examService.getUserExamInfo(examId, userId);

    console.log('\n考试结果:');
    console.log(`  考试名称: ${examInfo.target_title}`);
    console.log(`  分类: ${examInfo.category_title}`);
    console.log(`  总分: ${examInfo.total_score}`);
    console.log(`  及格分: ${examInfo.pass_score}`);
    console.log(`  最后得分: ${examInfo.last_score}`);
    console.log(`  考试次数: ${examInfo.attempt_times}`);
    console.log(`  通过状态: ${examInfo.pass_status === 'passed' ? '✓ 已通过' : '✗ 未通过'}`);
    console.log(`  平均用时: ${examInfo.avg_used_time}秒`);
    console.log(`  学分: ${examInfo.credit}`);

    return examInfo;
  }

  /**
   * 批量查询学员考试结果
   * @param {string} examId - 考试ID
   * @param {Array<string>} userNames - 用户名列表
   */
  async batchGetExamResults(examId, userNames) {
    console.log(`\n📊 批量查询考试结果 (共${userNames.length}人)`);

    const results = [];
    for (const userName of userNames) {
      try {
        const result = await this.getExamResult(examId, userName);
        results.push({ userName, success: true, data: result });
      } catch (error) {
        console.log(`✗ 查询失败: ${userName} - ${error.message}`);
        results.push({ userName, success: false, error: error.message });
      }
    }

    return results;
  }

  /**
   * 快速创建考试（使用默认题型配置）
   * @param {string} filePath - 文档路径
   * @param {string} examTitle - 考试标题
   * @param {Object} creator - 创建者信息
   */
  async quickCreateExam(filePath, examTitle, creator) {
    const defaultQuestionTypes = [
      { type: 'danxuan', count: 10 },    // 单选题
      { type: 'duoxuan', count: 5 },     // 多选题
      { type: 'panduan', count: 5 }      // 判断题
    ];

    return await this.createAndAssignExam({
      filePath,
      examTitle,
      questionTypes: defaultQuestionTypes,
      ...creator
    });
  }
}

export default new AiExamSkill();
