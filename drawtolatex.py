import sys
import xml.etree.ElementTree as ET
import random
import logging


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


class Attribute(Pos):
    def __init__(self, x: float, y: float, id: str, name: str):
        super().__init__(x, y, id)
        self.name: str = name

    def __repr__(self):
        return f"{self.name}: Attribute (x: {self.x}, y: {self.y})"


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


tree = ET.parse(sys.argv[1])
root = tree.getroot()
diagram = root[0]
cells = diagram[0][0]
elems: list[Elem] = []
elem_map = {}
scaling_factor = 30

(minx, miny) = (sys.maxsize, sys.maxsize)

for cell in cells:
    id: str = cell.get("id")
    x: float = 0
    y: float = 0
    name: str = ""
    if cell.get("value") is not None:
        x = (float(cell[0].get("x")) + float(cell[0].get("width"))/2) / scaling_factor
        y = -(float(cell[0].get("y")) + float(cell[0].get("width"))/2) / scaling_factor
        minx = min(minx, abs(x))
        miny = -min(miny, abs(y))
        name = cell.get("value")
        elem_map[id] = name[0:4] + str(random.randint(0, 9))
    if cell.get("style") == "whiteSpace=wrap;html=1;align=center;":
        elems.append(Entity(x, y, id, name))
        logging.info("Normal entity set")
    elif cell.get("style") == "shape=ext;margin=3;double=1;whiteSpace=wrap;html=1;align=center;":
        elems.append(Entity(x, y, id, name, True))
        logging.info("Weak entity set")
    elif cell.get("style") == "ellipse;whiteSpace=wrap;html=1;align=center;":
        elems.append(Attribute(x, y, id, name))
        logging.info("Attribute")
    elif cell.get("style") == "shape=rhombus;double=1;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;align=center;":
        elems.append(Relationship(x, y, id, name, True))
        logging.info("Identifying relationship set")
    elif cell.get("source") is not None:
        source: str = cell.get("source")
        target: str = cell.get("target")
        elems.append(Arrow(source, target, id))
        logging.info("Arrow")

logging.info(elems)
logging.info(elem_map)

for elem in elems:
    if isinstance(elem, Entity):
        print(r"\draw " f"node[entity{f', double' if elem.weak else ''}] ({elem_map[elem.id]}) at {elem.x-minx, elem.y-miny} " + "{" + elem.name + "};")
for elem in elems:
    if isinstance(elem, Relationship):
        print(r"\draw " f"node[relationship{f', double' if elem.weak else ''}] ({elem_map[elem.id]}) at {elem.x-minx, elem.y-miny} " + "{" + elem.name + "};")
for elem in elems:
    if isinstance(elem, Attribute):
        print(r"\draw " f"node[attribute] ({elem_map[elem.id]}) at {elem.x-minx, elem.y-miny} " + "{" + elem.name + "};")
for elem in elems:
    if isinstance(elem, Arrow):
        print(r"\draw " f"({elem_map[elem.source]}) -- ({elem_map[elem.target]});")
