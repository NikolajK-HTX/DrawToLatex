import xml.etree.ElementTree as ET

tree = ET.parse("er.xml")
root = tree.getroot()
diagram = root[0]
cells = diagram[0][0]

for cell in cells:
    if cell.get("style") == "whiteSpace=wrap;html=1;align=center;":
        print("Normal entity set")
    elif cell.get("style") == "shape=ext;margin=3;double=1;whiteSpace=wrap;html=1;align=center;":
        print("Weak entity set")
    elif cell.get("style") == "shape=rhombus;double=1;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;align=center;":
        print("Identifying relationship set")
    elif cell.get("source") is not None:
        print("Arrow")
