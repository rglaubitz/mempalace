"""Tests for shared palace collection helpers."""

import logging


def test_get_closets_collection_falls_back_to_legacy_compressed_once(tmp_path, caplog):
    """Existing 3.3.x palaces with only mempalace_compressed stay readable."""
    from mempalace.palace import get_closets_collection, get_collection

    palace_path = str(tmp_path / "palace")
    legacy = get_collection(palace_path, "mempalace_compressed", create=True)
    legacy.upsert(
        ids=["drawer-legacy"],
        documents=["legacy compressed closet body"],
        metadatas=[{"wing": "legacy", "room": "closets", "source_file": "legacy.md"}],
    )

    caplog.set_level(logging.WARNING, logger="mempalace_mcp")

    first = get_closets_collection(palace_path, create=False)
    first_result = first.get(ids=["drawer-legacy"], include=["documents", "metadatas"])
    assert first_result["ids"] == ["drawer-legacy"]
    assert first_result["documents"] == ["legacy compressed closet body"]

    second = get_closets_collection(palace_path, create=False)
    second_result = second.get(ids=["drawer-legacy"], include=["documents", "metadatas"])
    assert second_result["ids"] == ["drawer-legacy"]

    warnings = [
        record
        for record in caplog.records
        if "mempalace_compressed" in record.getMessage()
        and "mempalace_closets" in record.getMessage()
    ]
    assert len(warnings) == 1
