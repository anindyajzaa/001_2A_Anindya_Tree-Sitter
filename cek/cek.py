import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

BATAS_BARIS = 30
LEWATI = {"venv", ".git", "node_modules"}

def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error(child)
        if hasil:
            return hasil
    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > BATAS_BARIS:
            print(f"{path}:{fungsi.start_point[0] + 1}: fungsi {nama} terlalu panjang ({jumlah} baris)")

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        node = cari_error(tree.root_node)
        baris = node.start_point[0] + 1 if node else 1
        print(f"{path}:{baris}: sintaks error")

folder = Path(sys.argv[1])
for path in folder.rglob("*.py"):
    if LEWATI.intersection(path.relative_to(folder).parts):
        continue
    cek_file(path)