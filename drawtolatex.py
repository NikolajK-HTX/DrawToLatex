import sys
import xml.etree.ElementTree as ET


class Elem:
    def __init__(self, id: str):
        self.id = id


class Pos(Elem):
    def __init__(self, x: float, y: float, id: str):
        super().__init__(id)
        self.x: float = x
        self.y: float = y


class Entity(Pos):
    def __init__(self, x: float, y: float, id: str, name: str, weak: bool = False):
        super().__init__(x, y, id)
        self.weak: bool = weak
        self.name: str = name

    def __repr__(self):
        return f"{self.name}: {'Weak ' if self.weak else ''}Entity (x: {self.x}, y: {self.y})"


class Relationship(Pos):
    def __init__(self, x: float, y: float, id: str, name: str, weak: bool = False):
        super().__init__(x, y, id)
        self.name = name
        self.weak: bool = weak

    def __repr__(self):
        return f"{self.name}: {'Weak ' if self.weak else ''}Relationship (x: {self.x}, y: {self.y})"


class Arrow(Elem):
    def __init__(self, source: str, target: str, id: str):
        super().__init__(id)
        self.source: str = source
        self.target: str = target

    def __repr__(self):
        return f"Arrow from {self.source} to {self.target}"


tree = ET.parse("er.xml")
root = tree.getroot()
diagram = root[0]
cells = diagram[0][0]
elems: list[Elem] = []
elem_map = {}
scaling_factor = 100

(minx, miny) = (sys.maxsize, sys.maxsize)

for cell in cells:
    id: str = cell.get("id")
    x: float = 0
    y: float = 0
    name: str = ""
    if cell.get("value") is not None:
        x = float(cell[0].get("x")) / scaling_factor
        y = float(cell[0].get("y")) / scaling_factor
        minx = min(minx, x)
        miny = min(miny, y)
        name = cell.get("value")
        elem_map[id] = name
    if cell.get("style") == "whiteSpace=wrap;html=1;align=center;":
        elems.append(Entity(x, y, id, name))
        print("Normal entity set")
    elif cell.get("style") == "shape=ext;margin=3;double=1;whiteSpace=wrap;html=1;align=center;":
        elems.append(Entity(x, y, id, name, True))
        print("Weak entity set")
    elif cell.get("style") == "shape=rhombus;double=1;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;align=center;":
        elems.append(Relationship(x, y, id, name, True))
        print("Identifying relationship set")
    elif cell.get("source") is not None:
        source: str = cell.get("source")
        target: str = cell.get("target")
        elems.append(Arrow(source, target, id))
        print("Arrow")

print(elems)
print(elem_map)

for elem in elems:
    if isinstance(elem, Entity):
        print(r"\draw " f"node[entity] ({elem.name}) at {elem.x-minx, elem.y-miny} " + "{" + elem.name + "};")
