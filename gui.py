from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QFont

from data_mouse import X8Pro


class MouseWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.battery = 0
        self.drag_position = None

        # -------------------------------------------------
        # Окно
        # -------------------------------------------------

        self.setFixedSize(240, 290)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        # -------------------------------------------------
        # Мышь
        # -------------------------------------------------

        self.mouse = X8Pro()

        # -------------------------------------------------
        # Таймер обновления
        # -------------------------------------------------

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_battery
        )

        # Обновляем каждую минуту
        self.timer.start(60000)

        # Сразу получаем значение
        self.update_battery()

    # =====================================================
    # Получение батареи
    # =====================================================

    def update_battery(self):

        battery = self.mouse.get_battery()

        if battery is not None:

            self.battery = max(
                0,
                min(100, battery)
            )

            self.update()

    # =====================================================
    # Рисование
    # =====================================================

    def paintEvent(self, event):

        painter = QPainter()

        painter.begin(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # -------------------------------------------------
        # Фон
        # -------------------------------------------------

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QColor(25, 25, 28, 235)
        )

        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            24,
            24
        )

        # -------------------------------------------------
        # Заголовок
        # -------------------------------------------------

        painter.setPen(
            QColor(255, 255, 255)
        )

        title_font = QFont()

        title_font.setPixelSize(16)
        title_font.setWeight(
            QFont.Weight.DemiBold
        )

        painter.setFont(title_font)

        painter.drawText(
            0,
            30,
            self.width(),
            30,
            Qt.AlignmentFlag.AlignCenter,
            "X8 PRO"
        )

        # -------------------------------------------------
        # Круг
        # -------------------------------------------------

        circle_size = 155

        circle_x = (
            self.width() - circle_size
        ) // 2

        circle_y = 65

        rect = (
            circle_x,
            circle_y,
            circle_size,
            circle_size
        )

        # -------------------------------------------------
        # Цвет батареи
        # -------------------------------------------------

        if self.battery <= 15:

            battery_color = QColor(
                255, 70, 70
            )

        elif self.battery <= 30:

            battery_color = QColor(
                255, 170, 50
            )

        else:

            battery_color = QColor(
                255, 255, 255
            )

        # -------------------------------------------------
        # Фоновое кольцо
        # -------------------------------------------------

        background_pen = QPen(
            QColor(65, 65, 70),
            12
        )

        background_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(background_pen)

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawArc(
            *rect,
            90 * 16,
            -360 * 16
        )

        # -------------------------------------------------
        # Заряд
        # -------------------------------------------------

        battery_pen = QPen(
            battery_color,
            12
        )

        battery_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(battery_pen)

        span = int(
            -360 * 16 * self.battery / 100
        )

        painter.drawArc(
            *rect,
            90 * 16,
            span
        )

        # -------------------------------------------------
        # Процент
        # -------------------------------------------------

        painter.setPen(
            QColor(255, 255, 255)
        )

        percent_font = QFont()

        percent_font.setPixelSize(32)
        percent_font.setWeight(
            QFont.Weight.Bold
        )

        painter.setFont(percent_font)

        painter.drawText(
            *rect,
            Qt.AlignmentFlag.AlignCenter,
            f"{self.battery}%"
        )

        # -------------------------------------------------
        # Статус
        # -------------------------------------------------

        status_font = QFont()
        status_font.setPixelSize(12)

        painter.setFont(status_font)

        painter.setPen(
            QColor(150, 150, 155)
        )

        painter.drawText(
            0,
            245,
            self.width(),
            25,
            Qt.AlignmentFlag.AlignCenter,
            "Wireless"
        )

        painter.end()

    # =====================================================
    # Перемещение окна
    # =====================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if (
            event.buttons()
            & Qt.MouseButton.LeftButton
        ):

            if self.drag_position is not None:

                self.move(
                    event.globalPosition().toPoint()
                    - self.drag_position
                )

                event.accept()

    def mouseReleaseEvent(self, event):

        self.drag_position = None

        event.accept()

    # =====================================================
    # Закрытие
    # =====================================================

    def closeEvent(self, event):

        self.timer.stop()
        self.mouse.disconnect()

        event.accept()
