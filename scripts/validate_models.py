#!/usr/bin/env python3
"""Structural checks for the generated GLB models (standard library only)."""

import json
import math
import struct
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parents[1] / "assets" / "models"
EXPECTED = {
    "battery-aa.glb", "switch.glb", "incandescent-bulb.glb", "led.glb",
    "copper-wire.glb", "aluminum-strip.glb", "graphite-pencil.glb",
    "plastic-ruler.glb", "rubber-eraser.glb", "wooden-stick.glb",
}


def read_glb(path):
    data = path.read_bytes()
    assert len(data) >= 20, f"{path.name}: truncated GLB"
    magic, version, total_length = struct.unpack_from("<4sII", data, 0)
    assert magic == b"glTF", f"{path.name}: bad GLB magic"
    assert version == 2, f"{path.name}: expected glTF 2.0"
    assert total_length == len(data), f"{path.name}: incorrect file length"

    json_length, json_type = struct.unpack_from("<I4s", data, 12)
    assert json_type == b"JSON", f"{path.name}: missing JSON chunk"
    start = 20
    gltf = json.loads(data[start : start + json_length].decode("utf-8").rstrip(" \t\r\n\x00"))
    bin_header = start + json_length
    bin_length, bin_type = struct.unpack_from("<I4s", data, bin_header)
    assert bin_type == b"BIN\x00", f"{path.name}: missing binary chunk"
    binary = data[bin_header + 8 : bin_header + 8 + bin_length]
    assert gltf["buffers"][0]["byteLength"] <= len(binary), f"{path.name}: buffer out of bounds"
    return gltf, binary


def validate(path):
    gltf, binary = read_glb(path)
    assert gltf["asset"]["version"] == "2.0"
    assert gltf["nodes"] and gltf["meshes"] and gltf["materials"], f"{path.name}: empty model"
    assert len(gltf["nodes"]) == len(gltf["meshes"]), f"{path.name}: unexpected mesh/node mismatch"

    for accessor in gltf["accessors"]:
        view = gltf["bufferViews"][accessor["bufferView"]]
        start = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
        end = start + view["byteLength"]
        assert 0 <= start <= end <= len(binary), f"{path.name}: accessor outside BIN chunk"

    for mesh in gltf["meshes"]:
        for primitive in mesh["primitives"]:
            position = gltf["accessors"][primitive["attributes"]["POSITION"]]
            normal = gltf["accessors"][primitive["attributes"]["NORMAL"]]
            indices = gltf["accessors"][primitive["indices"]]
            assert position["count"] == normal["count"], f"{path.name}: missing normals"
            assert indices["count"] % 3 == 0, f"{path.name}: non-triangle index list"
            assert primitive["material"] < len(gltf["materials"]), f"{path.name}: invalid material"

    return len(binary), sum(a["count"] for a in gltf["accessors"] if a["type"] == "VEC3")


def main():
    existing = {path.name for path in MODEL_DIR.glob("*.glb")}
    assert existing == EXPECTED, f"Expected {sorted(EXPECTED)}, found {sorted(existing)}"
    for filename in sorted(EXPECTED):
        size, vec3_count = validate(MODEL_DIR / filename)
        print(f"OK {filename}: GLB 2.0, {size:,} BIN bytes, {vec3_count:,} VEC3 values")
    print(f"Validated {len(EXPECTED)} GLB models.")


if __name__ == "__main__":
    main()
