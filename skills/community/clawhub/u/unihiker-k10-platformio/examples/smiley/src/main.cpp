#include <math.h>
#include "unihiker_k10.h"

UNIHIKER_K10 k10;
uint8_t screen_dir = 2;

// ================= 配色（0xRRGGBB） =================
#define C_BG      0xEAF4FF   // 屏幕背景：淡蓝
#define C_FACE    0xFFCE36   // 脸：暖黄
#define C_LINE    0x33261A   // 描边：深棕（比纯黑柔和）
#define C_CHEEK   0xFFA3B5   // 腮红
#define C_WHITE   0xFFFFFF   // 眼睛高光
#define C_MOUTH   0xD93B4C   // 张嘴：玫红
#define C_TONGUE  0xFF8C9B   // 舌头

// ================= 脸部几何参数 =================
#define CX      120          // 脸中心 X
#define CY      160          // 脸中心 Y
#define FACE_R  95           // 脸半径
#define EYE_Y   126          // 眼睛 Y
#define EYE_LX  88           // 左眼 X
#define EYE_RX  152          // 右眼 X
#define EYE_R   15           // 眼睛半径

#define DEG     0.0174533f   // 1 度 = 0.01745 弧度

bool          laughMode = false;   // false=微笑  true=大笑
bool          eyeClosed = false;   // 是否正在眨眼
volatile bool btnFlag   = false;   // 按键标记（回调里只置位）
uint32_t      tBlink    = 0;       // 眨眼计时

void onButtonA() { btnFlag = true; }

// ---------------- 眼睛：睁开 ----------------
void drawEyeOpen(int x) {
  k10.canvas->canvasSetLineWidth(4);
  k10.canvas->canvasCircle(x, EYE_Y, EYE_R, C_LINE, C_LINE, true);
  k10.canvas->canvasSetLineWidth(1);
  k10.canvas->canvasCircle(x - 5, EYE_Y - 5, 4, C_WHITE, C_WHITE, true);
}

// ---------------- 眼睛：闭合（^ 形笑眯眯眼） ----------------
void drawEyeClosed(int x) {
  k10.canvas->canvasSetLineWidth(1);
  k10.canvas->canvasCircle(x, EYE_Y, EYE_R + 6, C_FACE, C_FACE, true); // 只擦这一小块
  k10.canvas->canvasSetLineWidth(6);
  k10.canvas->canvasLine(x - 13, EYE_Y + 5, x, EYE_Y - 4, C_LINE);
  k10.canvas->canvasLine(x, EYE_Y - 4, x + 13, EYE_Y + 5, C_LINE);
}

// ---------------- 腮红 ----------------
void drawCheeks() {
  k10.canvas->canvasSetLineWidth(1);
  k10.canvas->canvasCircle(52, 190, 12, C_CHEEK, C_CHEEK, true);
  k10.canvas->canvasCircle(188, 190, 12, C_CHEEK, C_CHEEK, true);
}

// ---------------- 嘴巴：微笑 / 大笑 ----------------
void drawMouth() {
  // 1. 只擦嘴部那一小块（局部刷新，不闪屏）
  k10.canvas->canvasSetLineWidth(1);
  k10.canvas->canvasRectangle(58, 158, 124, 58, C_FACE, C_FACE, true);
  // 2. 被擦到的腮红重新补上
  drawCheeks();

  if (!laughMode) {
    // 微笑：用短线段拼出一段圆弧
    k10.canvas->canvasSetLineWidth(9);
    int px = CX + (int)(58 * cos(30 * DEG));
    int py = 140 + (int)(58 * sin(30 * DEG));
    for (int a = 40; a <= 150; a += 10) {
      int nx = CX + (int)(58 * cos(a * DEG));
      int ny = 140 + (int)(58 * sin(a * DEG));
      k10.canvas->canvasLine(px, py, nx, ny, C_LINE);
      px = nx;
      py = ny;
    }
  } else {
    // 大笑：张开的嘴 + 舌头
    k10.canvas->canvasSetLineWidth(5);
    k10.canvas->canvasCircle(CX, 190, 26, C_LINE, C_MOUTH, true);
    k10.canvas->canvasSetLineWidth(1);
    k10.canvas->canvasCircle(CX, 200, 13, C_TONGUE, C_TONGUE, true);
  }
}

void setup() {
  k10.begin();
  k10.initScreen(screen_dir);
  k10.creatCanvas();
  k10.setScreenBackground(C_BG);          // 只在开机时整屏铺一次底色

  // 脸：黄色填充 + 深棕描边
  k10.canvas->canvasSetLineWidth(6);
  k10.canvas->canvasCircle(CX, CY, FACE_R, C_LINE, C_FACE, true);

  // 五官
  drawCheeks();
  drawEyeOpen(EYE_LX);
  drawEyeOpen(EYE_RX);
  drawMouth();

  k10.buttonA->setPressedCallback(onButtonA);  // A 键切换表情
  k10.canvas->updateCanvas();
}

void loop() {
  // A 键：微笑 <-> 大笑
  if (btnFlag) {
    btnFlag = false;
    laughMode = !laughMode;
    drawMouth();
    k10.canvas->updateCanvas();
  }

  // 自动眨眼：每 3.2 秒眨一次，闭合 140 毫秒
  if (!eyeClosed && millis() - tBlink > 3200) {
    eyeClosed = true;
    drawEyeClosed(EYE_LX);
    drawEyeClosed(EYE_RX);
    k10.canvas->updateCanvas();
    tBlink = millis();
  } else if (eyeClosed && millis() - tBlink > 140) {
    eyeClosed = false;
    drawEyeOpen(EYE_LX);
    drawEyeOpen(EYE_RX);
    k10.canvas->updateCanvas();
    tBlink = millis();
  }
}
