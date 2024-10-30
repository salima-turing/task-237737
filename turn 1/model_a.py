import unittest
import random


def convert_data_format(data, format_type):
    if format_type == "upper":
        return data.upper()
    elif format_type == "lower":
        return data.lower()
    else:
        raise ValueError("Invalid format type")


class FaultInjector:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.inject_fault(*args, **kwargs)

    def inject_fault(self, *args, **kwargs):
        # Customize fault injection logic here
        fault_type = random.choice(["none", "InvalidInput", "RandomError"])

        if fault_type == "InvalidInput":
            args = list(args)
            args[0] = "ïnvalid dâtà"
        elif fault_type == "RandomError":
            raise Exception("Random Error Occurred!")

        return self.func(*args, **kwargs)


class TestDataFormatConverter(unittest.TestCase):

    def setUp(self):
        self.converter = FaultInjector(convert_data_format)

    def test_fault_injection_scalability(self):
        for _ in range(100):  # Run the test multiple times with fault injection
            with self.subTest():
                try:
                    data = "hello"
                    result = self.converter(data, "upper")
                    self.assertEqual(result, "HELLO")

                    result = self.converter(data, "lower")
                    self.assertEqual(result, "hello")

                except Exception as e:
                    if isinstance(e, ValueError):
                        self.assertEqual(str(e), "Invalid format type")
                    else:
                        self.fail(f"Unexpected exception: {e}")


if __name__ == "__main__":
    unittest.main()
