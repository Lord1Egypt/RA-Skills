# 舵机控制排错指南


## 快速诊断流程

```
舵机不动？
  ├─ 1. 提醒用户检查接线是否正确
  ├─ 2. 提醒用户检查是否 5v 供电
  ├─ 3. 检查GPIO模式: pinctrl get <GPIO>
  └─ 4. 检查PWM信号: cat /sys/class/pwm/pwmchipX/pwmX/enable
```

## 流程示例

### 检查GPIO模式

```bash 
pinctrl get 12
```

正确输出应包含: GPIO12 = PWM0_CHAN0, 如果显示普通输出模式，说明pinctrl冲突.

### 检查PWM状态

```bash
ls -la /sys/class/pwm
cat /sys/class/pwm/pwmchip0/pwm0/enable
cat /sys/class/pwm/pwmchip0/pwm0/period
cat /sys/class/pwm/pwmchip0/pwm0/duty_cycle
```

## 模拟音频问题

在树莓派 5 之前, 耳机孔（模拟音频）是通过 PWM 硬件实现的. 如果你需要使用硬件 PWM 控制 GPIO，必须禁用板载音频:  
在 /boot/config.txt（或新系统的 /boot/firmware/config.txt）中，找到 `dtparam=audio=on` 并将其修改为 `dtparam=audio=off`

## 树莓派 5 的 RP1 南桥

在树莓派 5 上，由于引入了 RP1 南桥，PWM 芯片的索引号（pwmchipX）通常不再是固定的，且 PWM0 通道不一定对应 pwmchip2。


## 最小测试

如果所有方法都失败，参考这个最小测试示例：

```bash
# 导出PWM
echo 0 | sudo tee /sys/class/pwm/pwmchip2/export

# 设置周期
echo 20000000 | sudo tee /sys/class/pwm/pwmchip2/pwm0/period

# 循环摆动
while true; do
    echo 500000 | sudo tee /sys/class/pwm/pwmchip2/pwm0/duty_cycle   # 0度
    sleep 1
    echo 2500000 | sudo tee /sys/class/pwm/pwmchip2/pwm0/duty_cycle  # 180度
    sleep 1
done
```

如果舵机仍不动，检查：
1. 接线是否正确
2. 舵机是否损坏（换个试试）
3. 供电是否足够