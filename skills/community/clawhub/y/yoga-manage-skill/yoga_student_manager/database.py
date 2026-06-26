import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "yoga_students.db"

# 允许 update 方法修改的字段白名单，防止SQL注入
STUDENT_UPDATABLE_FIELDS = {'name', 'phone', 'wechat', 'notes'}


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                wechat TEXT,
                notes TEXT,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_type TEXT NOT NULL CHECK(course_type IN ('online', 'offline')),
                package_type TEXT NOT NULL CHECK(package_type IN ('yearly', 'hourly')),
                total_hours INTEGER,
                remaining_hours INTEGER,
                start_date TEXT,
                end_date TEXT,
                price REAL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deduction_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                deducted_hours INTEGER NOT NULL,
                remaining_before INTEGER NOT NULL,
                remaining_after INTEGER NOT NULL,
                class_date TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES student_courses(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
    finally:
        conn.close()


class Student:
    @staticmethod
    def create(name, phone=None, wechat=None, notes=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO students (name, phone, wechat, notes, created_at) VALUES (?, ?, ?, ?, ?)",
                (name, phone, wechat, notes, now)
            )
            student_id = cursor.lastrowid
            conn.commit()
            return student_id
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(student_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def update(student_id, **kwargs):
        # 白名单过滤，防止任意字段注入
        safe_fields = {k: v for k, v in kwargs.items() if k in STUDENT_UPDATABLE_FIELDS}
        if not safe_fields:
            return

        conn = get_connection()
        try:
            cursor = conn.cursor()
            fields = []
            values = []
            for k, v in safe_fields.items():
                fields.append(f"{k} = ?")
                values.append(v)
            values.append(student_id)
            cursor.execute(f"UPDATE students SET {', '.join(fields)} WHERE id = ?", values)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(student_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM deduction_logs WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM student_courses WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def search(keyword):
        """按姓名/电话/微信模糊搜索"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE name LIKE ? OR phone LIKE ? OR wechat LIKE ? ORDER BY created_at DESC",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()


class StudentCourse:
    @staticmethod
    def create(student_id, course_type, package_type, total_hours=None, remaining_hours=None, start_date=None, end_date=None, price=None):
        if package_type == 'hourly':
            if total_hours is None or remaining_hours is None:
                raise ValueError("包课时课程必须提供总课时和剩余课时")

        conn = get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute(
                """INSERT INTO student_courses
                   (student_id, course_type, package_type, total_hours, remaining_hours, start_date, end_date, price, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (student_id, course_type, package_type, total_hours, remaining_hours, start_date, end_date, price, now)
            )
            course_id = cursor.lastrowid
            conn.commit()
            return course_id
        finally:
            conn.close()

    @staticmethod
    def get_by_student(student_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student_courses WHERE student_id = ?", (student_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(course_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student_courses WHERE id = ?", (course_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def deduct_hours(course_id, hours=1, class_date=None, notes=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM student_courses WHERE id = ?", (course_id,))
            course = cursor.fetchone()
            if not course:
                raise ValueError("课程不存在")

            course_dict = dict(course)
            if course_dict['package_type'] != 'hourly':
                raise ValueError("只有包课时课程可以扣除课时")

            remaining = course_dict['remaining_hours']
            if remaining is None or remaining < hours:
                raise ValueError("剩余课时不足")

            new_remaining = remaining - hours
            now = datetime.now().isoformat()
            class_date = class_date or now[:10]

            cursor.execute(
                "UPDATE student_courses SET remaining_hours = ? WHERE id = ?",
                (new_remaining, course_id)
            )

            cursor.execute(
                """INSERT INTO deduction_logs
                   (student_id, course_id, deducted_hours, remaining_before, remaining_after, class_date, notes, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (course_dict['student_id'], course_id, hours, remaining, new_remaining, class_date, notes, now)
            )

            log_id = cursor.lastrowid
            conn.commit()

            return {
                'log_id': log_id,
                'student_id': course_dict['student_id'],
                'course_id': course_id,
                'deducted_hours': hours,
                'remaining_before': remaining,
                'remaining_after': new_remaining,
                'class_date': class_date,
                'notes': notes,
                'created_at': now
            }
        finally:
            conn.close()

    @staticmethod
    def add_hours(course_id, hours):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student_courses WHERE id = ?", (course_id,))
            course = cursor.fetchone()
            if not course:
                raise ValueError("课程不存在")

            course_dict = dict(course)
            if course_dict['package_type'] != 'hourly':
                raise ValueError("只有包课时课程可以增加课时")

            new_remaining = (course_dict['remaining_hours'] or 0) + hours
            new_total = (course_dict['total_hours'] or 0) + hours

            cursor.execute(
                "UPDATE student_courses SET remaining_hours = ?, total_hours = ? WHERE id = ?",
                (new_remaining, new_total, course_id)
            )
            conn.commit()
            return new_remaining
        finally:
            conn.close()


class DeductionLog:
    @staticmethod
    def get_by_student(student_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM deduction_logs WHERE student_id = ? ORDER BY created_at DESC",
                (student_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_course(course_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM deduction_logs WHERE course_id = ? ORDER BY created_at DESC",
                (course_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM deduction_logs ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()


def get_full_student_data(student_id):
    student = Student.get_by_id(student_id)
    if not student:
        return None
    student['courses'] = StudentCourse.get_by_student(student_id)
    student['deduction_logs'] = DeductionLog.get_by_student(student_id)
    return student


def get_all_data():
    students = Student.get_all()
    for s in students:
        s['courses'] = StudentCourse.get_by_student(s['id'])
        s['deduction_logs'] = DeductionLog.get_by_student(s['id'])
    return students
