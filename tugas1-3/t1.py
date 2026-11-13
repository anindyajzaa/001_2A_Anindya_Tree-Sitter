import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

# Tiga potongan kode
fungsi = b"def sapa(nama):\n    return nama\n"
ifelse = b"if x > 1:\n    y = 1\nelse:\n    y = 2\n"
kelas = b"class Mobil:\n    def jalan(self):\n        pass\n"

# Potongan 1: fungsi
print("=== FUNGSI ===")
tree_fungsi = parser.parse(fungsi)
print(tree_fungsi.root_node)

# Potongan 2: if/else
print("=== IF/ELSE ===")
tree_ifelse = parser.parse(ifelse)
print(tree_ifelse.root_node)

# Potongan 3: kelas
print("=== KELAS ===")
tree_kelas = parser.parse(kelas)
print(tree_kelas.root_node)