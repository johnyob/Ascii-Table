from functools import reduce

from ascii_table.Column import Column


class Table:

    def __init__(self, contents):
        self._header = Column(None, contents).get_header()
        self._columns = [{
                "Column": column,
                "Width": max(map(lambda x: sum(map(len, x)), column.get_rows())),
                "Number Of Columns": max(map(len, column.get_rows())),
                "Height": len(column.get_rows())
            } for column in self._header.get_children()
        ]

        assert len(set(map(lambda x: x["Height"], self._columns))) == 1
        self._height = self._columns[0]["Height"]

    def __repr__(self):
        return "\n".join(self._get_rows())

    def _get_row(self, row_index):
        for column in self._columns:
            cells = column["Column"].get_rows()[row_index]
            padding = column["Number Of Columns"] - len(cells)

            cell_length = (column["Width"] // len(cells)) + padding
            for cell in cells:
                yield (cell.format(cell_length), padding + 1, cell.is_header())

    def _join_cells(self, character, cells):
        cells = map(lambda x: (x[1] * " ") + x[0] + (x[1] * " "), cells)
        return " " + character + character.join(cells) + character

    def _join_lines(self, character, lines):
        lines = map(lambda x: (x[1] * x[2]) + x[0] + (x[1] * x[2]), lines)
        return " " + character + character.join(lines) + character

    def _get_line(self, row):
        for cell in row:
            character = "-" if cell[2] else " "
            yield (character * (len(cell[0])), cell[1], character)

    def _format_row(self, row_index):
        row = list(self._get_row(row_index))
        yield self._join_cells("|", row)
        if True in map(lambda x: x[2], row):
            yield self._join_lines("+", self._get_line(row))

    def _get_rows(self):
        yield self._join_lines("+", self._get_line(self._get_row(0)))
        for row in range(self._height):
            yield "\n".join(self._format_row(row))
        yield self._join_lines("+", self._get_line(
            map(lambda x: (x[0], x[1], True), self._get_row(-1))
        ))
