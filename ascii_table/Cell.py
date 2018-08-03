from ascii_table.Align import Align


class Cell:

    def __init__(self, text, align=Align.LEFT, parent=None):
        self._text = text
        self._align = align

        self._parent = parent
        self._children = []

    def add_child(self, text, align=Align.LEFT):
        return self._add_cell(Cell(text, align))

    def add_cell(self, cell):
        self._add_cell(cell)
        return self

    def _add_cell(self, cell):
        self._children.append(cell)
        return cell

    def is_leaf(self):
        return len(self._children) == 0

    def get_text(self):
        return self._text

    def get_children(self):
        return self._children

    def get_rows(self):
        queue, rows = [], []
        queue.append((self, 0))

        while len(queue) > 0:
            cell, row = queue.pop(0)

            if row + 1 > len(rows):
                rows.append([])
            rows[row].append(cell)

            for child in cell.get_children():
                queue.append((child, row + 1))

        return rows

    def format(self, cell_length):
        return format(self._text, "{0}{1}".format(self._align, cell_length))

    def is_header(self):
        return self._align == Align.CENTER

    def __len__(self):
        return len(self._text)

    def __repr__(self):
        return self._text
