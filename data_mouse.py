import hid


class X8Pro:

    VENDOR_ID = 0x1D57
    PRODUCT_ID = 0xFA65
    USAGE_PAGE = 0xFF00

    READ_SIZE = 65
    TIMEOUT = 500

    def __init__(self):
        self.device = None
        self.path = None

    def connect(self):

        if self.device is not None:
            return True

        devices = hid.enumerate(
            self.VENDOR_ID,
            self.PRODUCT_ID
        )

        for dev in devices:

            if dev["usage_page"] == self.USAGE_PAGE:

                self.path = dev["path"]

                self.device = hid.device()
                self.device.open_path(self.path)

                return True

        return False

    def disconnect(self):

        if self.device is not None:

            try:
                self.device.close()
            except Exception:
                pass

            self.device = None
            self.path = None

    def get_battery(self):

        try:

            if not self.connect():
                return None

            data = self.device.read(
                self.READ_SIZE,
                timeout_ms=self.TIMEOUT
            )

            if not data:
                return None

            # Индекс 4 = заряд батареи
            return data[4]

        except Exception:

            self.disconnect()

            return None

