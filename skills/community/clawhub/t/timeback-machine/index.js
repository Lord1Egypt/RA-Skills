// index.js
/** * OpenClaw Skill: TimeMachine * Author: Cortez_1 * Version: 1.0.0 */

// 一个更通用的提示函数，优先使用OpenClaw API，否则降级为alert
function showPrompt(title, message, onConfirm, onCancel) {
    if (typeof window !== 'undefined' && window.openclawAPI && window.openclawAPI.showModal) {
        window.openclawAPI.showModal({
            title: title,
            message: message,
            options: [
                { label: "继续处理", action: onCancel, type: "secondary" },
                { label: "立即回滚", action: onConfirm, type: "primary_danger" }
            ]
        });
    } else {
        const result = confirm(message);
        if (result) {
            onConfirm();
        } else {
            onCancel();
        }
    }
}

class TimeMachineSkill {
    constructor(config = {}) {
        this.config = {
            timeoutMs: 300000, // 5 minutes in ms
            onSaveState: (state) => this._deepClone(state), // 默认深拷贝
            onRestoreState: (savedData) => savedData, // 默认直接返回
            ...config,
        };
        this.savedState = null;
        this.isTaskActive = false;
        this.timerId = null;
        this.taskDescription = "";
    }

    startTask(currentState, taskDescription = "当前任务") {
        if (this.isTaskActive) {
            console.warn("TimeMachine: 一个任务正在进行中，无法启动新任务。");
            return false;
        }
        this.taskDescription = taskDescription;
        this.savedState = this.config.onSaveState(currentState);
        this.isTaskActive = true;
        console.info(`TimeMachine: 任务 "${taskDescription}" 已开始，将在 ${this.config.timeoutMs / 1000} 秒后询问是否回滚。`);
        this.timerId = setTimeout(() => {
            this._showRollbackPrompt();
        }, this.config.timeoutMs);
        return true;
    }

    triggerManualRollback() {
        if (!this.isTaskActive) {
            console.warn("TimeMachine: 没有活跃的任务可以回滚。");
            return;
        }
        if (this.timerId) {
            clearTimeout(this.timerId);
            this.timerId = null;
        }
        this._showRollbackPrompt();
    }

    rollback() {
        if (!this.savedState) {
            console.error("TimeMachine: 无可用的存档进行回滚。");
            return false;
        }
        console.info("TimeMachine: 正在执行回滚...");
        try {
            this.config.onRestoreState(this.savedState);
            this._cleanup();
            console.info("TimeMachine: 回滚成功！");
            return true;
        } catch (error) {
            console.error("TimeMachine: 回滚过程中发生错误", error);
            return false;
        }
    }

    confirmAndContinue() {
        console.info("TimeMachine: 用户确认继续，已放弃回滚选项。");
        this._cleanup();
    }

    _showRollbackPrompt() {
        showPrompt(
            "⚠️ 任务执行检测",
            `任务 "${this.taskDescription}" 已执行较长时间。是否需要撤销当前操作并回滚？`,
            () => this.rollback(),
            () => this.confirmAndContinue()
        );
    }

    _cleanup() {
        if (this.timerId) {
            clearTimeout(this.timerId);
            this.timerId = null;
        }
        this.isTaskActive = false;
        this.savedState = null;
        this.taskDescription = "";
    }

    _deepClone(obj) {
        try {
            return JSON.parse(JSON.stringify(obj));
        } catch(e) {
            console.warn("TimeMachine: 对象包含无法序列化的属性，可能无法完全备份。", e);
            return obj;
        }
    }
}

// 导出类以供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TimeMachineSkill;
} else if (typeof define === 'function' && define.amd) {
    define([], function() { return TimeMachineSkill; });
} else {
    window.TimeMachineSkill = TimeMachineSkill;
}

export default TimeMachineSkill;