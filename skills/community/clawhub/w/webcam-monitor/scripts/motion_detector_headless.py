#!/usr/bin/env python3.10
"""
Headless Motion Detection for Webcam
Runs without GUI, saves snapshots on motion
"""

import cv2
import numpy as np
import time
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
MOTION_THRESHOLD = 25          # Sensitivity (lower = more sensitive)
MIN_CONTOUR_AREA = 500         # Minimum area to trigger motion
SNAPSHOT_DIR = Path.home() / ".openclaw" / "workspace" / "camera" / "snapshots"
LOG_FILE = Path.home() / ".openclaw" / "workspace" / "camera" / "motion.log"
DEVICE_ID = 0                  # /dev/video0
SNAPSHOT_COOLDOWN = 5          # Seconds between snapshots

class HeadlessMotionDetector:
    def __init__(self):
        self.cap = None
        self.prev_frame = None
        self.motion_active = False
        self.motion_start_time = None
        self.last_snapshot = 0
        self.frame_count = 0
        self.motion_count = 0
        
        # Ensure snapshot directory exists
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        
    def log(self, message):
        """Log message to file and print"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry, flush=True)
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
    
    def init_camera(self):
        """Initialize camera capture"""
        self.log(f"Initializing camera (device {DEVICE_ID})...")
        self.cap = cv2.VideoCapture(DEVICE_ID)
        
        if not self.cap.isOpened():
            self.log("ERROR: Could not open camera!")
            return False
            
        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Warm up camera
        time.sleep(2)
        
        ret, frame = self.cap.read()
        if not ret:
            self.log("ERROR: Could not read from camera!")
            return False
            
        self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.prev_frame = cv2.GaussianBlur(self.prev_frame, (21, 21), 0)
        
        self.log("Camera initialized successfully")
        self.log(f"Resolution: {frame.shape[1]}x{frame.shape[0]}")
        return True
    
    def take_snapshot(self, frame, reason="motion"):
        """Save a snapshot image"""
        now = time.time()
        if now - self.last_snapshot < SNAPSHOT_COOLDOWN:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = SNAPSHOT_DIR / f"{reason}_{timestamp}.jpg"
        cv2.imwrite(str(filename), frame)
        self.last_snapshot = now
        self.log(f"Snapshot saved: {filename.name}")
        return filename
    
    def detect_motion(self, frame):
        """Detect motion in frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if self.prev_frame is None:
            self.prev_frame = gray
            return False, 0
        
        # Calculate difference
        frame_delta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frame_delta, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate to fill holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        max_area = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > MIN_CONTOUR_AREA:
                motion_detected = True
                max_area = max(max_area, area)
        
        self.prev_frame = gray
        return motion_detected, max_area
    
    def run(self):
        """Main detection loop"""
        if not self.init_camera():
            return 1
        
        self.log("Headless motion detection started")
        self.log("Press Ctrl+C to stop")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    self.log("ERROR: Failed to capture frame")
                    time.sleep(1)
                    continue
                
                self.frame_count += 1
                motion_detected, area = self.detect_motion(frame)
                
                # Handle motion events
                if motion_detected:
                    if not self.motion_active:
                        self.motion_active = True
                        self.motion_start_time = time.time()
                        self.motion_count += 1
                        self.log(f"Motion STARTED #{self.motion_count} (area: {int(area)})")
                        self.take_snapshot(frame, f"motion_{self.motion_count:04d}_start")
                    else:
                        # Still in motion - take periodic snapshots
                        if time.time() - self.last_snapshot > SNAPSHOT_COOLDOWN:
                            self.take_snapshot(frame, f"motion_{self.motion_count:04d}_active")
                else:
                    if self.motion_active:
                        duration = time.time() - self.motion_start_time
                        self.log(f"Motion ENDED (duration: {duration:.1f}s)")
                        self.motion_active = False
                
                # Status update every 60 seconds
                if self.frame_count % 1800 == 0:  # ~60 seconds at 30fps
                    status = "MOTION" if self.motion_active else "Idle"
                    self.log(f"Status: {status}, Frames: {self.frame_count}, Motions: {self.motion_count}")
                    
        except KeyboardInterrupt:
            self.log("Interrupted by user")
        finally:
            self.cleanup()
        
        return 0
    
    def cleanup(self):
        """Release resources"""
        if self.cap:
            self.cap.release()
        self.log(f"Motion detector stopped. Total frames: {self.frame_count}, Motions: {self.motion_count}")

if __name__ == "__main__":
    detector = HeadlessMotionDetector()
    sys.exit(detector.run())