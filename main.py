import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class RobFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(300, 300)
        self.robot_size = 24
        self.robot_x = 138  # Centered initial position
        self.robot_y = 138
        self.label = QLabel("Rob (GPS Map)", self)
        self.label.setFont(QFont("Arial", 14, QFont.Bold))
        self.label.setStyleSheet("color: #7cffd4; background: transparent; padding-left: 8px;")
        self.label.setGeometry(0, 0, 300, 28)
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, a0):
        super().paintEvent(a0)
        from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
        painter = QPainter(self)
        # Draw dark map background
        painter.setBrush(QColor(30, 40, 36))
        painter.setPen(QPen(QColor(0,0,0,0)))
        painter.drawRect(0, 28, self.width(), self.height()-28)
        # Draw grid lines
        grid_color = QColor(44, 66, 60)
        pen = QPen(grid_color, 1)
        painter.setPen(pen)
        grid_step = 30
        for x in range(0, self.width(), grid_step):
            painter.drawLine(x, 28, x, self.height())
        for y in range(28, self.height(), grid_step):
            painter.drawLine(0, y, self.width(), y)
        # Draw robot as a glowing dot
        painter.setPen(QPen(QColor(0,0,0,0)))
        painter.setBrush(QColor(60, 255, 120, 220))
        painter.drawEllipse(self.robot_x, self.robot_y, self.robot_size, self.robot_size)
        # Glow effect
        painter.setBrush(QColor(60, 255, 120, 80))
        painter.drawEllipse(self.robot_x-6, self.robot_y-6, self.robot_size+12, self.robot_size+12)
        # Draw coordinates
        painter.setPen(QColor(120,255,200))
        painter.setFont(QFont("Fira Mono", 10))
        coord_text = f"({self.robot_x}, {self.robot_y})"
        painter.drawText(10, self.height()-10, coord_text)

    def move_robot(self, direction):
        step = 15
        min_y = 28
        if direction == "up":
            self.robot_y = max(min_y, self.robot_y - step)
        elif direction == "down":
            self.robot_y = min(self.height() - self.robot_size, self.robot_y + step)
        elif direction == "left":
            self.robot_x = max(0, self.robot_x - step)
        elif direction == "right":
            self.robot_x = min(self.width() - self.robot_size, self.robot_x + step)
        self.update()

class InfraFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(300, 300)
        label = QLabel("Infra", self)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addStretch()

class VideoFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(300, 300)
        label = QLabel("Video", self)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addStretch()

class ControlPanel(QWidget):
    def __init__(self, move_callback):
        super().__init__()
        self.move_callback = move_callback
        grid = QGridLayout()
        # D-pad
        grid.addWidget(self._btn("↑", lambda: move_callback("up")), 0, 1)
        grid.addWidget(self._btn("←", lambda: move_callback("left")), 1, 0)
        grid.addWidget(self._btn("→", lambda: move_callback("right")), 1, 2)
        grid.addWidget(self._btn("↓", lambda: move_callback("down")), 2, 1)
        # Action buttons
        grid.addWidget(self._btn("A", lambda: move_callback("A")), 0, 3)
        grid.addWidget(self._btn("B", lambda: move_callback("B")), 2, 3)
        self.setLayout(grid)
    def _btn(self, text, slot):
        btn = QPushButton(text)
        btn.setFixedSize(40, 40)
        btn.clicked.connect(slot)
        return btn

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Simulation App")
        self.setMinimumSize(1000, 400)
        main_layout = QVBoxLayout(self)
        frames_layout = QHBoxLayout()
        self.rob_frame = RobFrame()
        self.infra_frame = InfraFrame()
        self.video_frame = VideoFrame()
        frames_layout.addWidget(self.rob_frame)
        frames_layout.addWidget(self.infra_frame)
        frames_layout.addWidget(self.video_frame)
        main_layout.addLayout(frames_layout)
        self.control_panel = ControlPanel(self.handle_control)
        main_layout.addWidget(self.control_panel)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a2421;
                color: #e0ffe0;
                font-family: 'Fira Mono', 'Consolas', 'DejaVu Sans Mono', monospace;
                font-size: 15px;
            }
            QFrame {
                background-color: #232e28;
                border-radius: 18px;
                border: 2px solid #2e4d36;
                margin: 8px;
            }
            QLabel {
                color: #aaffaa;
                font-size: 20px;
                font-weight: bold;
                padding: 8px 0 8px 0;
                letter-spacing: 1px;
            }
            QPushButton {
                background-color: #2e4d36;
                color: #e0ffe0;
                border: 2px solid #3a5c3a;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
                min-width: 40px;
                min-height: 40px;
                margin: 4px;
                transition: background 0.2s;
            }
            QPushButton:hover {
                background-color: #3a5c3a;
                color: #b6ffb6;
                border: 2px solid #5aff5a;
            }
            QPushButton:pressed {
                background-color: #1a2421;
                color: #aaffaa;
            }
            QGridLayout, QHBoxLayout, QVBoxLayout {
                spacing: 12px;
            }
        """)
    def handle_control(self, action):
        if action in ("up", "down", "left", "right"):
            self.rob_frame.move_robot(action)
        else:
            print(f"Control: {action}")
        # TODO: Implement Rob movement logic

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
