import sys
from PyQt6.QtWidgets import QApplication
from gui import MouseWidget

app = QApplication(sys.argv)

widget = MouseWidget()
widget.show()

sys.exit(app.exec())