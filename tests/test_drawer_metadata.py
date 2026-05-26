import logging

from mempalace.drawer_metadata import decode_drawer_metadata


def test_decode_drawer_metadata_warns_once_for_corrupted_json(caplog):
    caplog.set_level(logging.WARNING, logger="mempalace_mcp")

    assert decode_drawer_metadata("not json at all") is None

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.name == "mempalace_mcp"
    assert record.levelno == logging.WARNING
    assert record.value_head == "not json at all"


def test_decode_drawer_metadata_warns_for_json_non_dict(caplog):
    caplog.set_level(logging.WARNING, logger="mempalace_mcp")

    assert decode_drawer_metadata("[1,2,3]") is None

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.name == "mempalace_mcp"
    assert record.levelno == logging.WARNING
    assert record.value_head == "[1,2,3]"


def test_decode_drawer_metadata_keeps_legitimate_missing_paths_silent(caplog):
    caplog.set_level(logging.WARNING, logger="mempalace_mcp")

    assert decode_drawer_metadata(None) is None
    assert decode_drawer_metadata("") is None
    assert decode_drawer_metadata({"k": "v"}) == {"k": "v"}

    assert caplog.records == []
