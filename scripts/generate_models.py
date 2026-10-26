#!/usr/bin/env python3
"""Build small, original low-poly GLB assets for the classroom circuit guide.

Only the Python standard library is used. These are illustrative visual models,
not dimensionally accurate CAD parts.
"""

from __future__ import annotations

import json
import math
import struct
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "models"

MATERIALS = {
    "silver": ([0.72, 0.78, 0.84, 1], 0.78, 0.24),
    "metal": ([0.42, 0.50, 0.58, 1], 0.72, 0.28),
    "red": ([0.78, 0.12, 0.15, 1], 0.12, 0.4),
    "blue": ([0.10, 0.32, 0.72, 1], 0.08, 0.36),
    "dark": ([0.12, 0.17, 0.24, 1], 0.08, 0.5),
    "black": ([0.035, 0.045, 0.06, 1], 0.08, 0.48),
    "brass": ([0.78, 0.50, 0.13, 1], 0.72, 0.26),
    "cream": ([0.97, 0.83, 0.57, 1], 0.05, 0.32),
    "glass": ([1.0, 0.72, 0.28, 0.48], 0.05, 0.12),
    "green": ([0.12, 0.72, 0.32, 0.82], 0.04, 0.16),
    "gold": ([0.92, 0.61, 0.16, 1], 0.68, 0.25),
    "wood": ([0.69, 0.44, 0.22, 1], 0.02, 0.75),
    "graphite": ([0.12, 0.14, 0.17, 1], 0.12, 0.65),
    "plastic": ([0.20, 0.58, 0.87, 0.78], 0.02, 0.24),
    "pink": ([0.91, 0.40, 0.53, 1], 0.0, 0.72),
    "white": ([0.9, 0.94, 0.98, 1], 0.0, 0.55),
    "copper": ([0.72, 0.34, 0.12, 1], 0.72, 0.28),
    "yellow": ([0.95, 0.68, 0.12, 1], 0.08, 0.43),
}


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, factor):
    return tuple(x * factor for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(v):
    length = math.sqrt(dot(v, v))
    return tuple(value / length for value in v) if length else (0.0, 1.0, 0.0)


class MeshBuilder:
    def __init__(self):
        self.parts = {}
        self.used_materials = []

    def _part(self, material):
        if material not in self.parts:
            self.parts[material] = {"positions": [], "normals": [], "indices": []}
            self.used_materials.append(material)
        return self.parts[material]

    @staticmethod
    def _quad(part, points, normals):
        base = len(part["positions"]) // 3
        for point, normal in zip(points, normals):
            part["positions"].extend(point)
            part["normals"].extend(normal)
        part["indices"].extend(
            [base, base + 1, base + 2, base, base + 2, base + 3]
        )

    def box(self, center, size, material):
        cx, cy, cz = center
        sx, sy, sz = (value / 2 for value in size)
        p = {
            "000": (cx - sx, cy - sy, cz - sz),
            "001": (cx - sx, cy - sy, cz + sz),
            "010": (cx - sx, cy + sy, cz - sz),
            "011": (cx - sx, cy + sy, cz + sz),
            "100": (cx + sx, cy - sy, cz - sz),
            "101": (cx + sx, cy - sy, cz + sz),
            "110": (cx + sx, cy + sy, cz - sz),
            "111": (cx + sx, cy + sy, cz + sz),
        }
        faces = [
            (("001", "101", "111", "011"), (0, 0, 1)),
            (("100", "000", "010", "110"), (0, 0, -1)),
            (("101", "100", "110", "111"), (1, 0, 0)),
            (("000", "001", "011", "010"), (-1, 0, 0)),
            (("010", "011", "111", "110"), (0, 1, 0)),
            (("000", "100", "101", "001"), (0, -1, 0)),
        ]
        part = self._part(material)
        for corners, normal in faces:
            self._quad(part, [p[key] for key in corners], [normal] * 4)

    def cylinder(self, center, radius_bottom, radius_top, height, material, segments=12):
        cx, cy, cz = center
        part = self._part(material)
        bottom_y, top_y = cy - height / 2, cy + height / 2
        slope = (radius_bottom - radius_top) / max(height, 1e-6)
        for index in range(segments):
            a0 = 2 * math.pi * index / segments
            a1 = 2 * math.pi * (index + 1) / segments
            r0, r1 = (math.cos(a0), math.sin(a0)), (math.cos(a1), math.sin(a1))
            points = [
                (cx + radius_bottom * r0[0], bottom_y, cz + radius_bottom * r0[1]),
                (cx + radius_top * r0[0], top_y, cz + radius_top * r0[1]),
                (cx + radius_top * r1[0], top_y, cz + radius_top * r1[1]),
                (cx + radius_bottom * r1[0], bottom_y, cz + radius_bottom * r1[1]),
            ]
            normals = [norm((r0[0], slope, r0[1])), norm((r0[0], slope, r0[1])),
                       norm((r1[0], slope, r1[1])), norm((r1[0], slope, r1[1]))]
            self._quad(part, points, normals)

            bottom_center = (cx, bottom_y, cz)
            top_center = (cx, top_y, cz)
            base = len(part["positions"]) // 3
            for point, normal in [
                (bottom_center, (0, -1, 0)),
                (points[3], (0, -1, 0)),
                (points[0], (0, -1, 0)),
                (top_center, (0, 1, 0)),
                (points[1], (0, 1, 0)),
                (points[2], (0, 1, 0)),
            ]:
                part["positions"].extend(point)
                part["normals"].extend(normal)
            part["indices"].extend([base, base + 1, base + 2, base + 3, base + 4, base + 5])

    def sphere(self, center, radius, material, rings=8, segments=12):
        cx, cy, cz = center
        part = self._part(material)
        base = len(part["positions"]) // 3
        for ring in range(rings + 1):
            theta = math.pi * ring / rings
            for segment in range(segments + 1):
                phi = 2 * math.pi * segment / segments
                normal = (
                    math.sin(theta) * math.cos(phi),
                    math.cos(theta),
                    math.sin(theta) * math.sin(phi),
                )
                part["positions"].extend(
                    (cx + radius * normal[0], cy + radius * normal[1], cz + radius * normal[2])
                )
                part["normals"].extend(normal)
        row = segments + 1
        for ring in range(rings):
            for segment in range(segments):
                a = base + ring * row + segment
                b, c, d = a + 1, a + row, a + row + 1
                part["indices"].extend([a, b, c, b, d, c])

    def rod(self, start, end, radius, material, segments=8):
        direction = norm(sub(end, start))
        reference = (1, 0, 0) if abs(direction[1]) > 0.94 else (0, 1, 0)
        u = norm(cross(direction, reference))
        v = norm(cross(direction, u))
        part = self._part(material)
        base = len(part["positions"]) // 3
        for endpoint in (start, end):
            for index in range(segments):
                angle = 2 * math.pi * index / segments
                radial = add(mul(u, math.cos(angle)), mul(v, math.sin(angle)))
                part["positions"].extend(add(endpoint, mul(radial, radius)))
                part["normals"].extend(radial)
        for index in range(segments):
            nxt = (index + 1) % segments
            b0, b1 = base + index, base + nxt
            t0, t1 = base + segments + index, base + segments + nxt
            part["indices"].extend([b0, b1, t1, b0, t1, t0])
        cap_base = len(part["positions"]) // 3
        part["positions"].extend(start)
        part["normals"].extend(mul(direction, -1))
        part["positions"].extend(end)
        part["normals"].extend(direction)
        for index in range(segments):
            nxt = (index + 1) % segments
            part["indices"].extend([cap_base, base + nxt, base + index])
            part["indices"].extend([cap_base + 1, base + segments + index, base + segments + nxt])

    def glb(self, name):
        binary = bytearray()
        buffer_views = []
        accessors = []
        meshes = []
        nodes = []
        materials = []

        for material_name in self.used_materials:
            color, metallic, roughness = MATERIALS[material_name]
            material = {
                "name": material_name,
                "pbrMetallicRoughness": {
                    "baseColorFactor": color,
                    "metallicFactor": metallic,
                    "roughnessFactor": roughness,
                },
            }
            if color[3] < 1:
                material["alphaMode"] = "BLEND"
                material["doubleSided"] = True
            materials.append(material)
        material_indices = {material: index for index, material in enumerate(self.used_materials)}

        def append_block(data, target):
            while len(binary) % 4:
                binary.append(0)
            offset = len(binary)
            binary.extend(data)
            view_index = len(buffer_views)
            buffer_views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(data), "target": target})
            return view_index

        for material_name in self.used_materials:
            part = self.parts[material_name]
            positions = part["positions"]
            normals = part["normals"]
            indices = part["indices"]
            pos_data = struct.pack("<" + "f" * len(positions), *positions)
            normal_data = struct.pack("<" + "f" * len(normals), *normals)
            index_data = struct.pack("<" + "I" * len(indices), *indices)

            pos_view = append_block(pos_data, 34962)
            pos_accessor = len(accessors)
            points = list(zip(positions[0::3], positions[1::3], positions[2::3]))
            accessors.append({
                "bufferView": pos_view,
                "componentType": 5126,
                "count": len(positions) // 3,
                "type": "VEC3",
                "min": [min(p[i] for p in points) for i in range(3)],
                "max": [max(p[i] for p in points) for i in range(3)],
            })

            normal_view = append_block(normal_data, 34962)
            normal_accessor = len(accessors)
            accessors.append({
                "bufferView": normal_view,
                "componentType": 5126,
                "count": len(normals) // 3,
                "type": "VEC3",
            })

            index_view = append_block(index_data, 34963)
            index_accessor = len(accessors)
            accessors.append({
                "bufferView": index_view,
                "componentType": 5125,
                "count": len(indices),
                "type": "SCALAR",
                "min": [min(indices)],
                "max": [max(indices)],
            })
            meshes.append({
                "name": f"{name}-{material_name}",
                "primitives": [{
                    "attributes": {"POSITION": pos_accessor, "NORMAL": normal_accessor},
                    "indices": index_accessor,
                    "material": material_indices[material_name],
                    "mode": 4,
                }],
            })
            nodes.append({"name": f"{name}-{material_name}", "mesh": len(meshes) - 1})

        gltf = {
            "asset": {"version": "2.0", "generator": "Aventura Electrica: generador GLB educativo"},
            "scene": 0,
            "scenes": [{"nodes": list(range(len(nodes)))}],
            "nodes": nodes,
            "meshes": meshes,
            "materials": materials,
            "accessors": accessors,
            "bufferViews": buffer_views,
            "buffers": [{"byteLength": len(binary)}],
        }
        json_chunk = json.dumps(gltf, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        json_chunk += b" " * ((-len(json_chunk)) % 4)
        binary.extend(b"\x00" * ((-len(binary)) % 4))
        total_length = 12 + 8 + len(json_chunk) + 8 + len(binary)
        return (
            struct.pack("<4sII", b"glTF", 2, total_length)
            + struct.pack("<I4s", len(json_chunk), b"JSON")
            + json_chunk
            + struct.pack("<I4s", len(binary), b"BIN\x00")
            + binary
        )


def make_battery():
    m = MeshBuilder()
    m.cylinder((0, 0, 0), 0.52, 0.52, 2.45, "blue", 16)
    m.cylinder((0, -1.24, 0), 0.53, 0.53, 0.16, "silver", 16)
    m.cylinder((0, 1.24, 0), 0.48, 0.48, 0.12, "dark", 16)
    m.cylinder((0, 1.38, 0), 0.18, 0.18, 0.18, "brass", 12)
    return m


def make_switch():
    m = MeshBuilder()
    m.box((0, 0, 0), (1.9, 0.28, 1.1), "dark")
    for x in (-0.58, 0.58):
        m.cylinder((x, 0.23, 0), 0.18, 0.18, 0.18, "brass", 12)
        m.cylinder((x, 0.42, 0), 0.085, 0.085, 0.28, "brass", 10)
    m.rod((-0.58, 0.58, 0), (0.25, 1.03, 0), 0.075, "silver", 10)
    return m


def make_bulb():
    m = MeshBuilder()
    m.sphere((0, 0.62, 0), 0.69, "glass", 10, 16)
    m.cylinder((0, -0.1, 0), 0.27, 0.36, 0.43, "silver", 14)
    for y in (-0.23, -0.09, 0.05):
        m.cylinder((0, y, 0), 0.36, 0.36, 0.045, "metal", 14)
    m.cylinder((0, -0.38, 0), 0.28, 0.31, 0.18, "dark", 14)
    m.rod((-0.12, 0.02, 0), (-0.12, 0.42, 0), 0.025, "silver")
    m.rod((0.12, 0.02, 0), (0.12, 0.42, 0), 0.025, "silver")
    m.rod((-0.12, 0.42, 0), (0.12, 0.42, 0), 0.025, "gold")
    return m


def make_led():
    m = MeshBuilder()
    m.rod((-0.13, -1.0, 0), (-0.13, -0.17, 0), 0.045, "silver")
    m.rod((0.13, -1.0, 0), (0.13, -0.32, 0), 0.045, "silver")
    m.cylinder((0, 0, 0), 0.33, 0.33, 0.62, "dark", 12)
    m.cylinder((0, 0.48, 0), 0.3, 0.27, 0.35, "green", 12)
    m.sphere((0, 0.66, 0), 0.27, "green", 7, 12)
    return m


def make_wire():
    m = MeshBuilder()
    points = []
    for index in range(13):
        angle = math.radians(35 + index * 25)
        points.append((1.0 * math.cos(angle), 0, 1.0 * math.sin(angle)))
    for start, end in zip(points, points[1:]):
        m.rod(start, end, 0.075, "red", 8)
    for point, direction in ((points[0], (-0.35, 0, -0.18)), (points[-1], (0.35, 0, 0.18))):
        exposed = add(point, direction)
        m.rod(point, exposed, 0.035, "copper", 8)
    return m


def make_aluminum():
    m = MeshBuilder()
    m.box((0, 0, 0), (2.0, 0.16, 0.72), "silver")
    m.box((0, 0.085, 0), (1.78, 0.02, 0.56), "metal")
    return m


def make_pencil():
    m = MeshBuilder()
    m.cylinder((0, -0.08, 0), 0.22, 0.22, 2.2, "yellow", 6)
    m.cylinder((0, 1.22, 0), 0.22, 0.035, 0.42, "wood", 6)
    m.cylinder((0, 1.45, 0), 0.035, 0.012, 0.12, "graphite", 6)
    return m


def make_ruler():
    m = MeshBuilder()
    m.box((0, 0, 0), (2.7, 0.09, 0.46), "plastic")
    for index in range(12):
        x = -1.15 + index * 0.21
        length = 0.19 if index % 5 == 0 else 0.1
        m.box((x, 0.052, 0.15), (0.025, 0.012, length), "white")
    return m


def make_eraser():
    m = MeshBuilder()
    m.box((0, 0, 0), (1.1, 0.52, 0.72), "pink")
    m.box((0, -0.08, 0), (1.11, 0.12, 0.73), "cream")
    return m


def make_wooden_stick():
    m = MeshBuilder()
    m.box((0, 0, 0), (0.48, 2.25, 0.18), "wood")
    m.sphere((0, 1.12, 0), 0.23, "wood", 5, 10)
    m.sphere((0, -1.12, 0), 0.23, "wood", 5, 10)
    return m


MODELS = {
    "battery-aa.glb": ("Pila AA", make_battery),
    "switch.glb": ("Interruptor", make_switch),
    "incandescent-bulb.glb": ("Bombillo incandescente", make_bulb),
    "led.glb": ("Diodo LED", make_led),
    "copper-wire.glb": ("Cable de cobre", make_wire),
    "aluminum-strip.glb": ("Lámina de aluminio", make_aluminum),
    "graphite-pencil.glb": ("Mina de grafito", make_pencil),
    "plastic-ruler.glb": ("Regla de plástico", make_ruler),
    "rubber-eraser.glb": ("Borrador de nata", make_eraser),
    "wooden-stick.glb": ("Palito de madera", make_wooden_stick),
}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, (name, factory) in MODELS.items():
        data = factory().glb(name)
        (OUT_DIR / filename).write_bytes(data)
        print(f"Generated {filename}: {len(data):,} bytes")


if __name__ == "__main__":
    main()
