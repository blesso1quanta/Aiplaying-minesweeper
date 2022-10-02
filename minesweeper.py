import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            print(f"known_mines in sentence;{self.cells}")
            return(self.cells)





    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            print(f"known_safes in sentence:{self.cells}")
            return(self.cells)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.

        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1
            return(self.cells)


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return (self.cells)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        for sentence in self.knowledge:
            print(f"this is the sentence in the self.knowledge:{sentence}")

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #see the order
        #self.safes.add(cell)
        #i think it will not slove the initial value problem
        #self.mark_safe(cell)
        cells = set()

        if not (cell[0] == 0 or cell[1] == 0 or cell[1] == 7 or cell[0] == 7):
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):
                    if (i, j) not in self.moves_made:
                        cells.add((i, j))
        if cell[0] == 0 and not cell[1] == 0 and not cell[1] == 7:
            for k in range(cell[0], cell[0] + 2):
                for l in range(cell[1] - 1, cell[1] + 2):
                    if (k, l) not in self.moves_made:
                        cells.add((k, l))
        if cell[0] == 7 and not cell[1] == 0 and not cell[1] == 7:
            for g in range(cell[0] - 1, cell[0] + 1):
                for h in range(cell[1] - 1, cell[1] + 2):
                    if (g, h) not in self.moves_made:
                        cells.add((g, h))
        if cell[1] == 0 and not cell[0] == 0 and not cell[0] == 7:
            for c in range(cell[0] - 1, cell[0] + 2):
                for d in range(cell[1], cell[1] + 2):
                    if (c, d) not in self.moves_made:
                        cells.add((c, d))
        if cell[1] == 7 and not cell[0] == 0 and not cell[0] == 7:
            for e in range(cell[0] - 1, cell[0] + 2):
                for f in range(cell[1] - 1, cell[1] + 1):
                    if (e, f) not in self.moves_made:
                        cells.add((e, f))
        if cell[0] == 0 and cell[1] == 0:
            for a in range(cell[0], cell[0] + 2):
                for b in range(cell[1], cell[1] + 2):
                    if (a, b) not in self.moves_made:
                        cells.add((a, b))
        if cell[0] == 0 and cell[1] == 7:
            for o in range(cell[0], cell[0] + 2):
                for n in range(cell[1] - 1, cell[1] + 1):
                    if (o, n) not in self.moves_made:
                        cells.add((o, n))
        if cell[0] == 7 and cell[1] == 0:
            for x in range(cell[0] - 1, cell[0] + 1):
                for y in range(cell[1], cell[1] + 2):
                    if (x, y) not in self.moves_made:
                        cells.add((x, y))
        if cell[0] == 7 and cell[1] == 7:
            for u in range(cell[0] - 1, cell[0] + 1):
                for v in range(cell[1] - 1, cell[1] + 1):
                    if (u, v) not in self.moves_made:
                        cells.add((u, v))

        new_sentence = Sentence(cells, count)
        self.knowledge.append(new_sentence)
        print(f"this the sentence gatehered:{new_sentence}")
        self.moves_made.add(cell)
        self.mark_safe(cell)
        #new_sentence.mark_safe(cell)
        #new_sentence.mark_mine(cell)
        #for forth {a,b,c,d)=2 and {c,d} = 1
        #length_of_newsentencecells = len(new_sentence.cells)
        copy_sentence = Sentence(cells, count)
        for sentence in self.knowledge:
            if sentence != new_sentence:
                if sentence.cells.issubset(new_sentence.cells) or new_sentence.cells.issubset(sentence.cells):
                    new_sentence.cells.symmetric_difference_update(sentence.cells)
                    new_sentence.count = abs(new_sentence.count - sentence.count)
                if copy_sentence != new_sentence:
                    self.knowledge.append(new_sentence)
        print(f"this is the sentence after the algorithm:{new_sentence}")
        self.knowledge.append(new_sentence)
        #see this part thoroughly for cells in sentence.cells this statement goes through every single cell in the sentence
        #for sentence in self.knowledge:
            #for cell in sentence.cells:
                #if len(cell) == sentence.count:
                    #self.mines.add(cell)
                    #sentence.mark_mine(cell)
                #if sentence.count == 0:
                    #self.safes.add(cell)
                    #sentence.mark_safe(cell)

        #now use known mines and known safes and upade the safes mines and mark those things
        for sentence in self.knowledge:
            print(sentence)
            safes = set()
            if sentence.count == 0:
                for cells in sentence.cells:
                    safes.add(cells)
            if safes != None:
                for cell in safes:
                    self.mark_safe(cell)
                print(f"this is the self.safes {self.safes}")
            mines = set()
            if len(sentence.cells) == sentence.count:
                #print(f"known_mines in sentence;{sentence.cells}")
                for cells in sentence.cells:
                    mines.add(cells)
            if mines != None:
                for cell in mines:
                    self.mark_mine(cell)










    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("MAKING A SAFE MOVE")
        for cells in self.safes:
            print(f"in making_safemoves:{cells}")
            print(self.moves_made)
            if cells not in self.moves_made:
                print(cells)
                return(cells)
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                moves = set()
                moves.add((i, j))
        moves.difference(self.moves_made.union(self.mines))
        if len(moves) != 0:
            while True:
                i = random.randrange(self.height)
                j = random.randrange(self.width)
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    randoms = (i, j)
                    print(randoms)
                    return randoms
        else:
            return None


