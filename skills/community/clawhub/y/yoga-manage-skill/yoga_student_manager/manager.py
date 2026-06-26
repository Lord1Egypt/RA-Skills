from database import Student, StudentCourse, DeductionLog, get_full_student_data, get_all_data
from email_sender import send_student_record
from config import get_alert_thresholds


class YogaManager:
    def __init__(self):
        from database import init_database
        init_database()

    # ===== 学员管理 =====
    def add_student(self, name, phone=None, wechat=None, notes=None):
        sid = Student.create(name, phone, wechat, notes)
        print(f"学员添加成功，ID: {sid}")
        return sid

    def list_students(self):
        students = Student.get_all()
        if not students:
            print("暂无学员")
            return
        print("\n学员列表:")
        print("-" * 60)
        for s in students:
            print(f"ID: {s['id']} | 姓名: {s['name']} | 电话: {s.get('phone', 'N/A')} | 微信: {s.get('wechat', 'N/A')}")
        print("-" * 60)
        return students

    def search_students(self, keyword):
        students = Student.search(keyword)
        if not students:
            print(f"未找到与「{keyword}」匹配的学员")
            return
        print(f"\n搜索结果（{len(students)} 条）：")
        print("-" * 60)
        for s in students:
            print(f"ID: {s['id']} | 姓名: {s['name']} | 电话: {s.get('phone', 'N/A')} | 微信: {s.get('wechat', 'N/A')}")
        print("-" * 60)
        return students

    def show_student(self, student_id):
        data = get_full_student_data(student_id)
        if not data:
            print("学员不存在")
            return

        thresholds = get_alert_thresholds()
        urgent = thresholds['urgent']
        warn = thresholds['warn']

        print("\n" + "=" * 60)
        print(f"学员详情: {data['name']}")
        print("=" * 60)
        print(f"ID: {data['id']}")
        print(f"电话: {data.get('phone', 'N/A')}")
        print(f"微信: {data.get('wechat', 'N/A')}")
        print(f"备注: {data.get('notes', 'N/A')}")
        print("")

        if data['courses']:
            print("课程信息:")
            for c in data['courses']:
                ctype = "线上" if c['course_type'] == 'online' else "线下"
                ptype = "包年" if c['package_type'] == 'yearly' else "包课时"
                print(f"  课程ID: {c['id']} | {ctype} | {ptype}")
                if c['package_type'] == 'hourly':
                    remaining = c['remaining_hours']
                    print(f"    总课时: {c['total_hours']} | 剩余课时: {remaining}")
                    if remaining == 0:
                        print(f"    ⚠️  课时已全部用完！")
                    elif remaining <= urgent:
                        print(f"    ⚠️  课时即将用完，仅剩 {remaining} 次")
                    elif remaining <= warn:
                        print(f"    提醒：剩余课时较少（{remaining} 次）")
                else:
                    print(f"    有效期: {c['start_date']} ~ {c['end_date']}")
        else:
            print("暂无课程")

        if data['deduction_logs']:
            print("\n课时扣除记录:")
            for log in data['deduction_logs']:
                print(f"  [{log['created_at'][:16]}] 扣除 {log['deducted_hours']} 课时 | 剩余: {log['remaining_after']}")
                if log['notes']:
                    print(f"    备注: {log['notes']}")
        else:
            print("\n暂无扣除记录")

        return data

    def update_student(self, student_id, **kwargs):
        Student.update(student_id, **kwargs)
        print("学员信息更新成功")

    def delete_student(self, student_id):
        Student.delete(student_id)
        print("学员删除成功")

    # ===== 课程管理 =====
    def add_course(self, student_id, course_type, package_type, total_hours=None, remaining_hours=None, start_date=None, end_date=None, price=None):
        cid = StudentCourse.create(student_id, course_type, package_type, total_hours, remaining_hours, start_date, end_date, price)
        print(f"课程添加成功，ID: {cid}")
        return cid

    def deduct_hours(self, course_id, hours=1, class_date=None, notes=None):
        result = StudentCourse.deduct_hours(course_id, hours, class_date, notes)
        remaining = result['remaining_after']
        thresholds = get_alert_thresholds()
        urgent = thresholds['urgent']
        warn = thresholds['warn']

        print(f"\n  课时扣除成功！扣除 {hours} 课时")
        print(f"  ==============================")
        print(f"  剩余课时: {remaining} 次")
        print(f"  ==============================")

        if remaining == 0:
            print("  ⚠️  警告：该课程课时已全部用完！")
        elif remaining <= urgent:
            print(f"  ⚠️  提醒：课时即将用完，仅剩 {remaining} 次，请及时联系学员续费")
        elif remaining <= warn:
            print(f"  ⚠️  提醒：剩余课时较少（{remaining} 次），建议关注学员续费意向")

        print("")

        # 获取完整学员数据并发送邮件
        student_data = get_full_student_data(result['student_id'])
        if student_data:
            print("正在发送邮件记录...")
            try:
                success = send_student_record(student_data, "[课时扣除] ")
                if success:
                    print("邮件发送成功！")
                else:
                    print("邮件发送失败，请检查邮箱配置")
            except Exception as e:
                print(f"邮件发送失败: {e}")
                print("提示: 请运行 '配置邮箱' 选项设置邮箱信息")

        return result

    def add_hours(self, course_id, hours):
        new_remaining = StudentCourse.add_hours(course_id, hours)
        print(f"课时增加成功！当前剩余 {new_remaining} 课时")
        return new_remaining

    # ===== 日志查询 =====
    def show_logs(self, student_id=None):
        if student_id:
            logs = DeductionLog.get_by_student(student_id)
            print(f"\n学员ID {student_id} 的扣除记录:")
        else:
            logs = DeductionLog.get_all()
            print("\n全部扣除记录:")

        if not logs:
            print("暂无记录")
            return

        print("-" * 60)
        for log in logs:
            print(f"[{log['created_at'][:16]}] 学员ID: {log['student_id']} | 课程ID: {log['course_id']} | 扣除: {log['deducted_hours']} | 剩余: {log['remaining_after']}")
        print("-" * 60)
        return logs

    def send_full_report(self):
        all_data = get_all_data()
        if not all_data:
            print("暂无学员数据")
            return
        print("正在发送完整报表...")
        try:
            success = send_student_record(all_data, "[完整报表] ")
            if success:
                print("报表邮件发送成功！")
            else:
                print("邮件发送失败")
        except Exception as e:
            print(f"邮件发送失败: {e}")
            print("提示: 请运行 '配置邮箱' 选项设置邮箱信息")
