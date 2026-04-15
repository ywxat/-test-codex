# Python 摄像头实时手势识别（PyCharm）

这是一个可以直接在 **PyCharm** 里运行的示例项目，使用：

- `OpenCV`：读取摄像头画面
- `MediaPipe Hands`：检测手部关键点
- 简单规则：把关键点转换为手势分类结果

## 1. 环境准备

建议 Python 版本：**3.10 ~ 3.12**。

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## 2. 在 PyCharm 中运行

1. `Open` 打开本项目目录。
2. `Settings -> Project -> Python Interpreter` 选择本项目虚拟环境 `.venv`。
3. 打开 `gesture_recognition.py`。
4. 点击右上角 `Run` 或直接运行 `main()`。
5. 首次运行如果系统提示摄像头权限，请选择允许。

## 3. 操作说明

- 启动后会弹出摄像头窗口。
- 画面左上角显示识别结果。
- 按 `q` 退出程序。

## 4. 当前支持的手势

- `FIST`（拳头）
- `PALM`（五指张开）
- `ONE`
- `THREE`
- `PEACE`
- `THUMBS_UP`

> 说明：该示例为入门规则法，受拍摄角度、光线和遮挡影响。

## 5. 常见问题

### Q1：无法打开摄像头

- 关闭占用摄像头的软件（会议软件、浏览器等）。
- 修改 `recognizer.run(camera_index=0)` 中的索引（如 `1`、`2`）。

### Q2：识别不稳定

- 保持手掌尽量正对摄像头。
- 提高环境光照。
- 手势尽量在画面中部，离摄像头不要太远。
