import hypothesis
from hypothesis import strategies as st
import pytest

def convert_data_format(data, format):
    if format == "json":
        import json
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError as e:
            raise ValueError("Invalid JSON data") from e
    elif format == "csv":
        import csv
        reader = csv.reader([data])
        try:
            return next(reader)
        except csv.Error as e:
            raise ValueError("Invalid CSV data") from e
    else:
        raise ValueError("Unsupported format")

@hypothesis.given(st.data(), st.one_of(st.text(), st.binary()), st.text())
def test_convert_data_format_fault_injection(data, input_data, format):
    try:
        if data.draw(st.booleans()):
            input_data = input_data + b"\x00"  # Introduce a null byte to cause errors

        result = convert_data_format(input_data, format)

    except ValueError as e:
        pass
    else:
        pytest.fail("Expected a ValueError")

    assert convert_data_format('{"key": "value"}', "json") == {"key": "value"}
    assert convert_data_format('"value"', "json") == "value"
    assert convert_data_format('key,value', "csv") == ["key", "value"]
    with pytest.raises(ValueError, match="Invalid JSON data"):
        convert_data_format('{invalid json', "json")
    with pytest.raises(ValueError, match="Invalid CSV data"):
        convert_data_format('key,value,', "csv")
    with pytest.raises(ValueError, match="Unsupported format"):
        convert_data_format('data', "invalid format")
