"""Opaque drawer metadata passthrough helpers."""

import json
from typing import Any, Optional

DRAWER_METADATA_FIELD = "metadata"


def encode_drawer_metadata(metadata: Optional[dict[str, Any]]) -> Optional[str]:
    """Serialize caller-owned drawer metadata for ChromaDB storage."""
    if metadata is None:
        return None
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dict")
    return json.dumps(metadata, separators=(",", ":"))


def decode_drawer_metadata(value: Any) -> Optional[dict[str, Any]]:
    """Decode optional drawer metadata from storage into the public shape."""
    if value is None or value == "":
        return None
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        return None
    try:
        decoded = json.loads(value)
    except (TypeError, ValueError):
        return None
    return decoded if isinstance(decoded, dict) else None
