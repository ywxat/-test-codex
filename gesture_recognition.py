"""实时手势识别示例。

运行方式：
    python gesture_recognition.py
"""
from __future__ import annotations

import cv2
import mediapipe as mp


class HandGestureRecognizer:
    """使用 MediaPipe Hands 进行摄像头实时手势识别。"""

    TIP_IDS = [4, 8, 12, 16, 20]

    def __init__(self) -> None:
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.mp_draw = mp.solutions.drawing_utils

    @staticmethod
    def _fingers_up(hand_landmarks, width: int, height: int) -> list[bool]:
        """返回 5 根手指是否伸出的布尔列表（拇指、食指、中指、无名指、小指）。"""
        coords = []
        for lm in hand_landmarks.landmark:
            coords.append((int(lm.x * width), int(lm.y * height)))

        fingers = []

        # 拇指：根据 x 轴判断（适用于大部分正对摄像头场景）
        thumb_tip_x = coords[4][0]
        thumb_ip_x = coords[3][0]
        wrist_x = coords[0][0]
        is_right_hand = coords[17][0] < coords[5][0]

        if is_right_hand:
            fingers.append(thumb_tip_x < thumb_ip_x)
        else:
            fingers.append(thumb_tip_x > thumb_ip_x)

        # 其余四指：tip 的 y 坐标小于 pip 表示抬起（图像坐标 y 向下）
        for tip_id in [8, 12, 16, 20]:
            pip_id = tip_id - 2
            fingers.append(coords[tip_id][1] < coords[pip_id][1])

        # 过滤掉与手腕太近的噪声状态
        for i, tip_id in enumerate(self.TIP_IDS):
            dist = abs(coords[tip_id][1] - coords[0][1])
            if dist < 20:
                fingers[i] = False

        return fingers

    @staticmethod
    def _classify_gesture(fingers: list[bool]) -> str:
        total = sum(fingers)

        if total == 0:
            return "FIST"
        if total == 5:
            return "PALM"

        thumb, index, middle, ring, pinky = fingers

        if index and middle and not ring and not pinky and not thumb:
            return "PEACE"
        if thumb and not index and not middle and not ring and not pinky:
            return "THUMBS_UP"
        if index and not middle and not ring and not pinky:
            return "ONE"
        if index and middle and ring and not pinky:
            return "THREE"

        return f"UNKNOWN ({total} FINGERS)"

    def run(self, camera_index: int = 0) -> None:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError(
                "无法打开摄像头。请确认摄像头未被占用，并尝试修改 camera_index。"
            )

        print("启动成功：按 q 退出。")

        while True:
            ok, frame = cap.read()
            if not ok:
                print("读取摄像头画面失败，程序结束。")
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            gesture_text = "NO HAND"

            if result.multi_hand_landmarks:
                for hand_lms in result.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_lms,
                        self.mp_hands.HAND_CONNECTIONS,
                    )
                    fingers = self._fingers_up(hand_lms, w, h)
                    gesture_text = self._classify_gesture(fingers)

            cv2.rectangle(frame, (10, 10), (380, 60), (0, 0, 0), -1)
            cv2.putText(
                frame,
                f"Gesture: {gesture_text}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Real-time Hand Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    recognizer = HandGestureRecognizer()
    recognizer.run(camera_index=0)


if __name__ == "__main__":
    main()
