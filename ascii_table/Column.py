from ascii_table.Cell import Cell
from ascii_table.Align import Align


class Column:

    def __init__(self, header, contents, parent=None):
        self._contents = [
            Column(content["Header"], content["Contents"], parent).get_header() if isinstance(content, dict) else content
            for content in contents
        ]

        self._header = Cell(header, Align.CENTER, parent=parent)
        self._add_contents(self._header, self._contents)

    def _add_contents(self, root, contents):
        if contents:
            method = root.add_cell if isinstance(contents[0], Cell) else root.add_child
            self._add_contents(method(contents[0]), contents[1:])

    def get_header(self):
        return self._header
